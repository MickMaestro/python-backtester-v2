"""Core data structures shared across the data layer."""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from enum import Enum


class Timeframe(str, Enum):
    """Chart timeframes supported by the app (names follow MT5 conventions)."""

    M1 = "M1"
    M5 = "M5"
    M15 = "M15"
    M30 = "M30"
    H1 = "H1"
    H4 = "H4"
    D1 = "D1"
    W1 = "W1"
    MN1 = "MN1"

    @property
    def seconds(self) -> int:
        return _TIMEFRAME_SECONDS[self]


# MN1 is nominal (30 days); calendar months vary.
_TIMEFRAME_SECONDS: dict[Timeframe, int] = {
    Timeframe.M1: 60,
    Timeframe.M5: 300,
    Timeframe.M15: 900,
    Timeframe.M30: 1_800,
    Timeframe.H1: 3_600,
    Timeframe.H4: 14_400,
    Timeframe.D1: 86_400,
    Timeframe.W1: 604_800,
    Timeframe.MN1: 2_592_000,
}

#: Canonical column order for every bar DataFrame in the app.
#: ``time`` is a tz-naive datetime64[ns] in MT5 server time.
BAR_COLUMNS = [
    "time",
    "open",
    "high",
    "low",
    "close",
    "tick_volume",
    "spread",
    "real_volume",
]


@dataclass
class DatasetInfo:
    """Catalog entry describing one stored symbol/timeframe dataset."""

    symbol: str
    timeframe: str
    start: str
    end: str
    bars: int
    source: str
    saved_at: str
    filename: str
    # Instrument contract spec captured from MT5 at download time (None for
    # CSV imports or datasets saved before this field existed).
    point: float | None = None
    digits: int | None = None
    contract_size: float | None = None

    @property
    def key(self) -> str:
        return f"{self.symbol}_{self.timeframe}"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "DatasetInfo":
        known = {f.name for f in fields(cls)}
        return cls(**{k: v for k, v in data.items() if k in known})
