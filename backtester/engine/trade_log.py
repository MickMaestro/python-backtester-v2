"""Trade context logs: the bars and indicator values around every trade moment.

For each moment a trade had — its entry, every SL/TP modification, and its exit
— this writes the window of bars leading up to that moment together with every
indicator series the strategy computed, so a decision can be inspected as
*numbers* rather than eyeballed on a chart.

A run produces one folder:

    context.parquet   every moment's window, stacked into one tidy table
    manifest.csv      one row per moment: what happened, and its window
    indicators.csv    each indicator column and the call that produced it

``context.parquet`` is long-form — ``frame_id`` identifies the moment,
``offset`` is the bar's distance from it (0 is the moment itself, negative is
history) — so a whole run loads in one ``pd.read_parquet`` and slices by trade.

The window is either the last N bars up to the moment (no look-ahead, the same
view the strategy had) or the whole calendar day containing it (which does
include what came after — it is a review tool, not a decision input).

Nothing here imports Qt: the same pass runs from the GUI and from
``run_backtest.py``.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, replace
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Callable, Sequence

import numpy as np
import pandas as pd

from .events import PositionClosed, PositionModified, PositionOpened

ENTRY = "entry"
MODIFY = "modify"
EXIT = "exit"

CONTEXT_NAME = "context.parquet"
MANIFEST_NAME = "manifest.csv"
INDICATORS_NAME = "indicators.csv"

#: Columns identifying each row's moment, ahead of the bar and indicator data.
KEY_COLUMNS = ["frame_id", "trade_id", "kind", "event_index", "bar_index", "offset"]

MANIFEST_COLUMNS = [
    "frame_id", "trade_id", "kind", "bar_index", "time", "direction", "lots",
    "price", "sl", "tp", "old_sl", "old_tp", "net", "reason",
    "context_from", "context_to", "bars",
]

#: Series ``Strategy.bind`` puts on the strategy — bar data, not indicators.
_BAR_ATTRS = frozenset({"time", "opens", "highs", "lows", "closes"})


class ContextMode(str, Enum):
    BARS = "bars"      # the last N bars up to and including the moment
    DAY = "day"        # every bar of the calendar day the moment falls in

    @property
    def label(self) -> str:
        return "Last N bars" if self is ContextMode.BARS else "Whole day"


def event_kind(event) -> str | None:
    """The log kind of an engine event, or None if it isn't a trade moment."""
    if isinstance(event, PositionOpened):
        return ENTRY
    if isinstance(event, PositionModified):
        return MODIFY
    if isinstance(event, PositionClosed):
        return EXIT
    return None


@dataclass
class TradeLogSpec:
    """What to log. Plain data — the GUI persists it, the CLI builds one."""

    entries: bool = True
    modifications: bool = True
    exits: bool = True
    mode: ContextMode = ContextMode.BARS
    context_bars: int = 120
    max_moments: int = 1_000          # 0 = no limit

    @property
    def kinds(self) -> set[str]:
        chosen = set()
        if self.entries:
            chosen.add(ENTRY)
        if self.modifications:
            chosen.add(MODIFY)
        if self.exits:
            chosen.add(EXIT)
        return chosen


@dataclass
class TradeLogReport:
    folder: Path
    moments: int                      # windows written
    rows: int                         # bars written across them
    total: int                        # loggable moments the run produced
    cancelled: bool = False

    @property
    def truncated(self) -> bool:
        return not self.cancelled and self.moments < self.total

    def message(self) -> str:
        if self.cancelled:
            return (
                f"Trade log: cancelled after {self.moments:,} of {self.total:,} "
                f"moments → {self.folder.name}"
            )
        if self.moments == 0:
            return "Trade log: nothing to log."
        text = (
            f"Trade log: {self.moments:,} moments, {self.rows:,} bars "
            f"→ {self.folder.name}"
        )
        if self.truncated:
            text += f" (limit reached, of {self.total:,})"
        return text


def count_moments(events: Sequence, spec: TradeLogSpec) -> int:
    kinds = spec.kinds
    return sum(1 for event in events if event_kind(event) in kinds)


def run_folder_name(dataset_key: str, label: str, when: datetime | None = None) -> str:
    """``EURUSD_H1_ma_cross_20260727-194500`` — one folder per run."""
    stamp = (when or datetime.now()).strftime("%Y%m%d-%H%M%S")
    return f"{_safe(dataset_key)}_{_safe(label)}_{stamp}"


def _safe(text: str) -> str:
    cleaned = "".join(c if c.isalnum() or c in "-_." else "_" for c in text.strip())
    return cleaned.strip("_") or "run"


# ---------------------------------------------------------------- indicators


@dataclass
class Indicator:
    """One logged series: the column it is written as, and how it was built."""

    column: str
    values: np.ndarray
    recipe: str = ""                  # e.g. "ema(50, Typical)"
    attribute: str = ""               # what the strategy called it


def _unique_column(name: str, taken: set[str]) -> str:
    """A column name that can't shadow a bar column or another indicator."""
    column = name if name not in taken else f"ind_{name}"
    while column in taken:
        column += "_"
    taken.add(column)
    return column


def collect_indicators(strategy, length: int, reserved=()) -> list[Indicator]:
    """Every indicator series a strategy holds, named after its attribute.

    Strategies don't declare their indicators — they just assign them
    (``self.trend = self.ind.ema(50)``) — so they are found by inspecting the
    instance for numeric series as long as the data, minus the bar arrays
    ``bind`` attaches. Anything the IndicatorFactory built also carries its
    recipe, which is what makes the log self-describing.
    """
    factory = getattr(strategy, "ind", None)
    taken = set(reserved)
    found: list[Indicator] = []
    for name, value in vars(strategy).items():
        if name.startswith("_") or name in _BAR_ATTRS:
            continue
        if not isinstance(value, np.ndarray) or value.ndim != 1:
            continue
        if len(value) != length or not np.issubdtype(value.dtype, np.number):
            continue
        found.append(
            Indicator(
                column=_unique_column(name, taken),
                values=value,
                recipe=factory.recipe_for(value) if factory is not None else "",
                attribute=name,
            )
        )
    return found


# -------------------------------------------------------------------- writing


def write_trade_log(
    df: pd.DataFrame,
    events: Sequence,
    indicators: Sequence[Indicator],
    folder: Path | str,
    spec: TradeLogSpec | None = None,
    progress: Callable[[int, int], None] | None = None,
    should_cancel: Callable[[], bool] | None = None,
) -> TradeLogReport:
    """Write ``context.parquet`` + ``manifest.csv`` + ``indicators.csv``."""
    spec = spec or TradeLogSpec()
    kinds = spec.kinds
    folder = Path(folder)
    # Resolved here, not only in log_run: an indicator column called "close"
    # would otherwise overwrite the bar column rather than sit beside it.
    taken = set(KEY_COLUMNS) | set(df.columns)
    indicators = [
        replace(indicator, column=_unique_column(indicator.column, taken))
        for indicator in indicators
    ]
    total = count_moments(events, spec)
    limit = spec.max_moments if spec.max_moments > 0 else total
    planned = min(total, limit)
    if planned <= 0:
        return TradeLogReport(folder, 0, 0, total)

    times = df["time"].to_numpy()
    days = times.astype("datetime64[D]") if len(times) else times
    blocks: list[pd.DataFrame] = []
    manifest: list[dict] = []
    modifications: dict[int, int] = {}
    cancelled = False

    for event in events:
        kind = event_kind(event)
        if kind is None or kind not in kinds:
            continue
        if len(manifest) >= limit:
            break
        if should_cancel is not None and should_cancel():
            cancelled = True
            break
        index = int(event.index)
        start, end = _window(index, days, spec)
        frame_id = _frame_id(event, kind, modifications)
        blocks.append(_block(df, indicators, frame_id, kind, event, index, start, end))
        manifest.append(
            _manifest_row(event, kind, frame_id, times, index, start, end)
        )
        if progress is not None:
            progress(len(manifest), planned)

    if not blocks:
        return TradeLogReport(folder, 0, 0, total, cancelled)

    folder.mkdir(parents=True, exist_ok=True)
    context = pd.concat(blocks, ignore_index=True)
    context.to_parquet(folder / CONTEXT_NAME, index=False)
    _write_csv(folder / MANIFEST_NAME, MANIFEST_COLUMNS, manifest)
    _write_csv(
        folder / INDICATORS_NAME,
        ["column", "attribute", "recipe"],
        [
            {"column": i.column, "attribute": i.attribute, "recipe": i.recipe}
            for i in indicators
        ],
    )
    return TradeLogReport(folder, len(manifest), len(context), total, cancelled)


def _window(index: int, days: np.ndarray, spec: TradeLogSpec) -> tuple[int, int]:
    """The [start, end] bar range logged for a moment at ``index``."""
    # Converted, not compared with ``is``: ContextMode subclasses str, so a
    # plain "day" is a legitimate way to build a spec (the CLI passes one).
    if ContextMode(spec.mode) is ContextMode.DAY and len(days):
        day = days[index]
        # Bar times are sorted, so the day's bars are one contiguous run.
        start = int(np.searchsorted(days, day, "left"))
        end = int(np.searchsorted(days, day, "right")) - 1
        return start, end
    return max(0, index - max(1, spec.context_bars) + 1), index


def _block(
    df: pd.DataFrame,
    indicators: Sequence[Indicator],
    frame_id: str,
    kind: str,
    event,
    index: int,
    start: int,
    end: int,
) -> pd.DataFrame:
    bar_index = np.arange(start, end + 1)
    block = pd.DataFrame(
        {
            "frame_id": frame_id,
            "trade_id": _trade_id(event, kind),
            "kind": kind,
            "event_index": index,
            "bar_index": bar_index,
            "offset": bar_index - index,
        }
    )
    bars = df.iloc[start : end + 1]
    for column in bars.columns:
        block[column] = bars[column].to_numpy()
    for indicator in indicators:
        block[indicator.column] = indicator.values[start : end + 1]
    return block


def _trade_id(event, kind: str) -> int:
    return event.trade.id if kind == EXIT else event.position.id


def _frame_id(event, kind: str, modifications: dict[int, int]) -> str:
    trade_id = _trade_id(event, kind)
    if kind == MODIFY:
        nth = modifications[trade_id] = modifications.get(trade_id, 0) + 1
        return f"{trade_id:04d}_modify_{nth:02d}"
    return f"{trade_id:04d}_{kind}"


def _manifest_row(
    event, kind: str, frame_id: str, times, index: int, start: int, end: int
) -> dict:
    row = {column: "" for column in MANIFEST_COLUMNS}
    row.update(
        frame_id=frame_id,
        trade_id=_trade_id(event, kind),
        kind=kind,
        bar_index=index,
        # Timestamps go through pandas so the CSV reads "2024-01-05 13:00:00"
        # rather than numpy's "2024-01-05T13:00:00.000000".
        time=pd.Timestamp(times[index]),
        context_from=pd.Timestamp(times[start]),
        context_to=pd.Timestamp(times[end]),
        bars=end - start + 1,
    )
    if kind == EXIT:
        trade = event.trade
        row.update(
            direction=_side(trade.direction),
            lots=trade.lots,
            price=trade.exit_price,
            net=round(trade.net, 2),
            reason=trade.reason.value,
        )
        return row
    position = event.position
    row.update(
        direction=_side(position.direction),
        lots=position.lots,
        price=position.entry_price,
        sl="" if position.sl is None else position.sl,
        tp="" if position.tp is None else position.tp,
    )
    if kind == MODIFY:
        row["old_sl"] = "" if event.old_sl is None else event.old_sl
        row["old_tp"] = "" if event.old_tp is None else event.old_tp
    return row


def _side(direction) -> str:
    return "buy" if int(direction) > 0 else "sell"


def _write_csv(path: Path, columns: list[str], rows: list[dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def log_run(
    df: pd.DataFrame,
    result,
    strategy,
    folder: Path | str,
    spec: TradeLogSpec | None = None,
    **kwargs,
) -> TradeLogReport:
    """Convenience wrapper: collect the strategy's indicators, then write."""
    indicators = collect_indicators(strategy, len(df))
    return write_trade_log(df, result.events, indicators, folder, spec, **kwargs)
