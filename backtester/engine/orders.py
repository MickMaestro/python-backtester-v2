"""Order, position, and closed-trade value objects."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, IntEnum
from typing import Any


class Direction(IntEnum):
    LONG = 1
    SHORT = -1


class OrderType(Enum):
    MARKET = "market"
    LIMIT = "limit"   # buy below / sell above the current price
    STOP = "stop"     # buy above / sell below the current price


class CloseReason(Enum):
    STOP_LOSS = "sl"
    TAKE_PROFIT = "tp"
    MANUAL = "manual"
    END_OF_DATA = "end"
    STOP_OUT = "stop_out"


@dataclass
class Order:
    """A request to open a position.

    Market orders fill at the next bar's open; limit/stop orders wait for
    their trigger price. ``sl_pips``/``tp_pips`` are converted to absolute
    prices at fill time, relative to the actual fill price.
    """

    id: int
    type: OrderType
    direction: Direction
    lots: float
    price: float | None = None      # trigger price; None for market orders
    sl: float | None = None
    tp: float | None = None
    sl_pips: float | None = None
    tp_pips: float | None = None
    comment: str = ""


@dataclass
class Position:
    """An open position. ``swap`` accrues nightly and settles at close."""

    id: int
    direction: Direction
    lots: float
    entry_price: float
    entry_time: Any                 # pd.Timestamp
    entry_index: int
    sl: float | None = None
    tp: float | None = None
    swap: float = 0.0
    comment: str = ""

    @property
    def is_long(self) -> bool:
        return self.direction is Direction.LONG

    @property
    def is_short(self) -> bool:
        return self.direction is Direction.SHORT


@dataclass
class Trade:
    """A closed position, as recorded in the results."""

    id: int
    direction: Direction
    lots: float
    entry_price: float
    entry_time: Any
    entry_index: int
    exit_price: float
    exit_time: Any
    exit_index: int
    profit: float                   # price PnL in account currency
    commission: float               # total cost, both sides (positive)
    swap: float                     # signed (usually negative)
    reason: CloseReason
    comment: str = ""

    @property
    def net(self) -> float:
        return self.profit + self.swap - self.commission

    @property
    def is_win(self) -> bool:
        return self.net > 0
