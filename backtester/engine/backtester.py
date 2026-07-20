"""The backtest event loop.

``Backtester.run()`` is a generator yielding engine events (see events.py):
per bar a ``BarEvent``, any order/position events, then one ``EquityEvent``.
The replay UI steps this generator on a timer; ``run_all()`` drains it as
fast as possible and returns a ``BacktestResult``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterator

import numpy as np
import pandas as pd

from .broker import SimBroker
from .events import BarEvent, EquityEvent
from .instrument import InstrumentSpec
from .orders import CloseReason
from .stats import compute_stats

_REQUIRED = ("time", "open", "high", "low", "close")


@dataclass
class BacktestConfig:
    initial_balance: float = 10_000.0
    spread_points: int | None = None    # None → use the data's spread column
    commission_per_lot: float = 0.0     # per side, account currency
    swap_long: float = 0.0              # per lot per night, account currency
    swap_short: float = 0.0
    instrument: InstrumentSpec = field(default_factory=InstrumentSpec.forex_major)


@dataclass
class BacktestResult:
    initial_balance: float
    final_balance: float
    trades: list
    equity: pd.DataFrame                # columns: time, balance, equity
    stats: dict
    config: "BacktestConfig | None" = None  # run settings (instrument, costs)

    @property
    def net_profit(self) -> float:
        return self.final_balance - self.initial_balance


class Backtester:
    def __init__(
        self,
        df: pd.DataFrame,
        strategy,
        config: BacktestConfig | None = None,
        intrabar_df: pd.DataFrame | None = None,
    ):
        """``intrabar_df``: optional finer-timeframe bars of the same symbol.
        When given, SL/TP and pending-order triggers are resolved sub-bar by
        sub-bar inside each main bar, so "which was hit first, SL or TP?" is
        answered from data instead of the pessimistic assumption. Main bars
        not covered by the finer data fall back to single-bar resolution.
        """
        missing = [c for c in _REQUIRED if c not in df.columns]
        if missing:
            raise ValueError(f"Data is missing column(s): {', '.join(missing)}")
        if len(df) == 0:
            raise ValueError("Data is empty.")

        self.df = df.reset_index(drop=True)
        self.config = config or BacktestConfig()

        self.time = self.df["time"].to_numpy()
        self.open = self.df["open"].to_numpy(dtype=float)
        self.high = self.df["high"].to_numpy(dtype=float)
        self.low = self.df["low"].to_numpy(dtype=float)
        self.close = self.df["close"].to_numpy(dtype=float)
        if self.config.spread_points is not None:
            self.spread = np.full(len(self.df), self.config.spread_points, dtype=float)
        elif "spread" in self.df.columns:
            self.spread = self.df["spread"].to_numpy(dtype=float)
        else:
            self.spread = np.zeros(len(self.df))

        self.broker = SimBroker(
            spec=self.config.instrument,
            initial_balance=self.config.initial_balance,
            commission_per_lot=self.config.commission_per_lot,
            swap_long=self.config.swap_long,
            swap_short=self.config.swap_short,
        )
        self.strategy = strategy
        strategy.bind(self.df, self.broker)

        self._sub = None
        if intrabar_df is not None and len(intrabar_df) > 0:
            sub = intrabar_df.reset_index(drop=True)
            # Map sub-bars to main bars by time: sub-bar j belongs to main bar
            # i when time[i] <= t(j) < time[i] + bar_duration. Bounding by the
            # bar's own duration keeps disjoint/far sub-data from spilling into
            # the last main bar.
            main_ns = self.time.astype("datetime64[ns]").astype("int64")
            sub_ns = sub["time"].to_numpy().astype("datetime64[ns]").astype("int64")
            if len(main_ns) > 1:
                gaps = np.diff(main_ns)
                dur = np.append(gaps, int(np.median(gaps)))
            else:
                dur = np.array([86_400_000_000_000], dtype="int64")  # 1 day
            starts = np.searchsorted(sub_ns, main_ns, side="left")
            ends = np.searchsorted(sub_ns, main_ns + dur, side="left")
            self._sub = {
                "open": sub["open"].to_numpy(dtype=float),
                "high": sub["high"].to_numpy(dtype=float),
                "low": sub["low"].to_numpy(dtype=float),
                "close": sub["close"].to_numpy(dtype=float),
                "spread": (
                    sub["spread"].to_numpy(dtype=float)
                    if "spread" in sub.columns and self.config.spread_points is None
                    else None
                ),
                "starts": starts,
                "ends": ends,
            }

        self._equity_rows: list[tuple[Any, float, float]] = []
        self._finished = False

    # ---------------------------------------------------------------- run

    def run(self) -> Iterator[Any]:
        """Yield engine events bar by bar (see module docstring)."""
        broker = self.broker
        # Nights held = calendar days crossed between consecutive bar times.
        days = self.time.astype("datetime64[D]").astype("int64")

        self.strategy.init()
        n = len(self.df)
        stopped_out = False

        for i in range(n):
            o, h, l, c = self.open[i], self.high[i], self.low[i], self.close[i]
            ask_off = self.spread[i] * self.config.instrument.point

            broker.begin_bar(i, self.time[i])
            yield BarEvent(i, self.time[i], o, h, l, c)

            if i > 0:
                broker.apply_swap(int(days[i] - days[i - 1]))
            broker.process_open(o, ask_off)
            self._resolve_intrabar(i, o, h, l, c, ask_off)
            yield from self._drain()

            self.strategy.step(i)
            yield from self._drain()

            equity = broker.equity(c, ask_off)
            if equity <= 0:
                broker.close_all_now(c, ask_off, CloseReason.STOP_OUT)
                yield from self._drain()
                equity = broker.balance
                stopped_out = True

            self._equity_rows.append((self.time[i], broker.balance, equity))
            yield EquityEvent(i, self.time[i], broker.balance, equity)

            if stopped_out:
                break

        if not stopped_out and (broker.positions or broker.pending):
            last = n - 1
            ask_off = self.spread[last] * self.config.instrument.point
            had_positions = bool(broker.positions)
            broker.close_all_now(self.close[last], ask_off, CloseReason.END_OF_DATA)
            yield from self._drain()
            if had_positions:
                self._equity_rows[-1] = (self.time[last], broker.balance, broker.balance)
                yield EquityEvent(last, self.time[last], broker.balance, broker.balance)

        self._finished = True

    def run_all(self) -> BacktestResult:
        for _ in self.run():
            pass
        return self.result()

    def result(self) -> BacktestResult:
        if not self._finished:
            raise RuntimeError("Backtest has not finished; call run_all() or drain run().")
        equity = pd.DataFrame(
            self._equity_rows, columns=["time", "balance", "equity"]
        )
        return BacktestResult(
            initial_balance=self.config.initial_balance,
            final_balance=self.broker.balance,
            trades=list(self.broker.trades),
            equity=equity,
            stats=compute_stats(
                self.broker.trades, equity, self.config.initial_balance
            ),
            config=self.config,
        )

    # ------------------------------------------------------------ helpers

    def _resolve_intrabar(
        self, i: int, o: float, h: float, l: float, c: float, ask_off: float
    ) -> None:
        """Trigger pendings and SL/TP for bar ``i``, sub-bar by sub-bar when
        finer data covers it, else against the single main bar."""
        sub = self._sub
        if sub is not None and sub["ends"][i] > sub["starts"][i]:
            point = self.config.instrument.point
            for j in range(sub["starts"][i], sub["ends"][i]):
                if sub["spread"] is not None:
                    off = sub["spread"][j] * point
                else:
                    off = ask_off
                so, sh = sub["open"][j], sub["high"][j]
                sl_, sc = sub["low"][j], sub["close"][j]
                self.broker.process_pending(so, sh, sl_, sc, off)
                self.broker.process_sl_tp(so, sh, sl_, sc, off)
        else:
            self.broker.process_pending(o, h, l, c, ask_off)
            self.broker.process_sl_tp(o, h, l, c, ask_off)

    def _drain(self):
        events = self.broker.events[:]
        self.broker.events.clear()
        return events
