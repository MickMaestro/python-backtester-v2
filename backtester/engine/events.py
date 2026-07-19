"""Events emitted by the engine while a backtest runs.

The engine's ``run()`` is a generator of these events. The fast path drains
them for results; the replay UI (Phase 4) consumes the same stream to animate
the chart. Per bar the order is: ``BarEvent``, then any order/position events,
then one ``EquityEvent``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .orders import Order, Position, Trade


@dataclass(frozen=True)
class BarEvent:
    index: int
    time: Any
    open: float
    high: float
    low: float
    close: float


@dataclass(frozen=True)
class OrderPlaced:
    index: int
    order: Order


@dataclass(frozen=True)
class OrderCancelled:
    index: int
    order: Order


@dataclass(frozen=True)
class PositionOpened:
    index: int
    position: Position


@dataclass(frozen=True)
class PositionModified:
    index: int
    position: Position
    old_sl: float | None
    old_tp: float | None


@dataclass(frozen=True)
class PositionClosed:
    index: int
    trade: Trade


@dataclass(frozen=True)
class EquityEvent:
    index: int
    time: Any
    balance: float
    equity: float
