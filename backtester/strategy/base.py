"""Strategy base class — the API user strategies are written against.

Lifecycle: the engine calls ``init()`` once (build indicators here), then
``on_bar(bar)`` for every bar. Inside ``on_bar``, ``self.i`` is the current
bar index and indicator arrays may be read **up to and including** ``self.i``
(reading beyond it is look-ahead bias; the crossover helpers respect this).

Orders placed in ``on_bar`` fill at the next bar's open, matching how a live
EA acting on a closed bar would fill.
"""

from __future__ import annotations

from types import SimpleNamespace

import pandas as pd

from backtester.engine.broker import _KEEP, SimBroker
from backtester.engine.events import BarEvent
from backtester.engine.orders import Direction, Order, Position

from .indicators import IndicatorFactory


class Strategy:
    #: Override in subclasses; every key becomes a field on ``self.p`` and a
    #: tunable parameter in the GUI (later phases).
    params: dict = {}

    def __init__(self, **overrides):
        unknown = set(overrides) - set(self.params)
        if unknown:
            raise ValueError(
                f"Unknown parameter(s) for {type(self).__name__}: {', '.join(sorted(unknown))}"
            )
        self.p = SimpleNamespace(**{**self.params, **overrides})
        self.i = -1
        self.df: pd.DataFrame | None = None
        self.broker: SimBroker | None = None
        self.ind: IndicatorFactory | None = None

    # ------------------------------------------------------- engine wiring

    def bind(self, df: pd.DataFrame, broker: SimBroker) -> None:
        self.df = df
        self.broker = broker
        self.ind = IndicatorFactory(df)
        # Price series use plural names so they don't shadow the trading
        # methods (``self.close`` is the close-a-position call, ``self.closes``
        # is the close-price array).
        self.time = df["time"].to_numpy()
        self.opens = df["open"].to_numpy(dtype=float)
        self.highs = df["high"].to_numpy(dtype=float)
        self.lows = df["low"].to_numpy(dtype=float)
        self.closes = df["close"].to_numpy(dtype=float)

    def step(self, i: int) -> None:
        self.i = i
        self.on_bar(
            BarEvent(i, self.time[i], self.opens[i], self.highs[i], self.lows[i], self.closes[i])
        )

    # ------------------------------------------------------ user overrides

    def init(self) -> None:
        """Called once before the first bar. Build indicators here."""

    def on_bar(self, bar: BarEvent) -> None:
        """Called for every bar. Trade decisions go here."""

    # ------------------------------------------------------- trading calls

    def buy(self, lots: float = 0.1, *, sl: float | None = None, tp: float | None = None,
            sl_pips: float | None = None, tp_pips: float | None = None,
            comment: str = "") -> Order:
        return self.broker.market_order(
            Direction.LONG, lots, sl=sl, tp=tp, sl_pips=sl_pips, tp_pips=tp_pips,
            comment=comment,
        )

    def sell(self, lots: float = 0.1, *, sl: float | None = None, tp: float | None = None,
             sl_pips: float | None = None, tp_pips: float | None = None,
             comment: str = "") -> Order:
        return self.broker.market_order(
            Direction.SHORT, lots, sl=sl, tp=tp, sl_pips=sl_pips, tp_pips=tp_pips,
            comment=comment,
        )

    def buy_limit(self, price: float, lots: float = 0.1, **kwargs) -> Order:
        return self.broker.limit_order(Direction.LONG, lots, price, **kwargs)

    def sell_limit(self, price: float, lots: float = 0.1, **kwargs) -> Order:
        return self.broker.limit_order(Direction.SHORT, lots, price, **kwargs)

    def buy_stop(self, price: float, lots: float = 0.1, **kwargs) -> Order:
        return self.broker.stop_order(Direction.LONG, lots, price, **kwargs)

    def sell_stop(self, price: float, lots: float = 0.1, **kwargs) -> Order:
        return self.broker.stop_order(Direction.SHORT, lots, price, **kwargs)

    def cancel(self, order: Order) -> None:
        self.broker.cancel_order(order)

    def modify(self, position: Position, sl=_KEEP, tp=_KEEP) -> None:
        self.broker.modify_position(position, sl=sl, tp=tp)

    def close(self, position: Position) -> None:
        self.broker.close_position(position)

    def close_all(self) -> None:
        self.broker.close_all()

    # ---------------------------------------------------------- inspection

    @property
    def positions(self) -> list[Position]:
        return self.broker.positions

    @property
    def position(self) -> Position | None:
        """The oldest open position, or None."""
        return self.broker.positions[0] if self.broker.positions else None

    @property
    def balance(self) -> float:
        return self.broker.balance

    # ------------------------------------------------------------- helpers

    def cross_over(self, a, b) -> bool:
        """True if series ``a`` crossed above ``b`` on the current bar."""
        i = self.i
        if i < 1:
            return False
        prev_a, prev_b, cur_a, cur_b = a[i - 1], b[i - 1], a[i], b[i]
        if any(pd.isna(v) for v in (prev_a, prev_b, cur_a, cur_b)):
            return False
        return prev_a <= prev_b and cur_a > cur_b

    def cross_under(self, a, b) -> bool:
        """True if series ``a`` crossed below ``b`` on the current bar."""
        i = self.i
        if i < 1:
            return False
        prev_a, prev_b, cur_a, cur_b = a[i - 1], b[i - 1], a[i], b[i]
        if any(pd.isna(v) for v in (prev_a, prev_b, cur_a, cur_b)):
            return False
        return prev_a >= prev_b and cur_a < cur_b
