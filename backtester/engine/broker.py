"""Simulated broker: order matching, fills, SL/TP, commission, and swap.

Price model (MT5 convention): stored bars are **bid** prices; ask = bid +
spread. Longs open at ask and close at bid; shorts open at bid and close at
ask. SL/TP for longs trigger on bid, for shorts on ask. When both SL and TP
fall inside one bar the SL is assumed to hit first (pessimistic, since OHLC
bars don't reveal the intrabar path).

Timing model: the strategy decides on a bar's close; market orders and manual
closes execute at the *next* bar's open. SL/TP and pending-order triggers are
evaluated against each bar's full range.
"""

from __future__ import annotations

from typing import Any

from .events import (
    OrderCancelled,
    OrderPlaced,
    PositionClosed,
    PositionModified,
    PositionOpened,
)
from .instrument import InstrumentSpec
from .orders import CloseReason, Direction, Order, OrderType, Position, Trade

_KEEP = object()  # sentinel: "leave this SL/TP level unchanged" in modify()


class SimBroker:
    def __init__(
        self,
        spec: InstrumentSpec,
        initial_balance: float,
        commission_per_lot: float = 0.0,   # per side, account currency
        swap_long: float = 0.0,            # per lot per night, account currency
        swap_short: float = 0.0,
    ) -> None:
        self.spec = spec
        self.balance = initial_balance
        self.commission_per_lot = commission_per_lot
        self.swap_long = swap_long
        self.swap_short = swap_short

        self.positions: list[Position] = []
        self.pending: list[Order] = []
        self.trades: list[Trade] = []
        self.events: list[Any] = []        # buffered; the engine drains per bar

        self._market_queue: list[Order] = []
        self._close_queue: list[int] = []  # position ids to close at next open
        self._next_id = 1
        self._index = 0                    # current bar index (set by engine)
        self._time: Any = None

    # ------------------------------------------------- strategy-facing API

    def market_order(
        self,
        direction: Direction,
        lots: float,
        sl: float | None = None,
        tp: float | None = None,
        sl_pips: float | None = None,
        tp_pips: float | None = None,
        comment: str = "",
    ) -> Order:
        order = self._make_order(
            OrderType.MARKET, direction, lots, None, sl, tp, sl_pips, tp_pips, comment
        )
        self._market_queue.append(order)
        return order

    def limit_order(
        self, direction: Direction, lots: float, price: float, **kwargs
    ) -> Order:
        order = self._make_order(
            OrderType.LIMIT, direction, lots, price,
            kwargs.get("sl"), kwargs.get("tp"),
            kwargs.get("sl_pips"), kwargs.get("tp_pips"), kwargs.get("comment", ""),
        )
        self.pending.append(order)
        return order

    def stop_order(
        self, direction: Direction, lots: float, price: float, **kwargs
    ) -> Order:
        order = self._make_order(
            OrderType.STOP, direction, lots, price,
            kwargs.get("sl"), kwargs.get("tp"),
            kwargs.get("sl_pips"), kwargs.get("tp_pips"), kwargs.get("comment", ""),
        )
        self.pending.append(order)
        return order

    def cancel_order(self, order: Order) -> None:
        if order in self.pending:
            self.pending.remove(order)
            self.events.append(OrderCancelled(self._index, order))

    def modify_position(self, position: Position, sl=_KEEP, tp=_KEEP) -> None:
        """Change SL/TP immediately. Pass ``None`` to remove a level."""
        old_sl, old_tp = position.sl, position.tp
        if sl is not _KEEP:
            position.sl = sl
        if tp is not _KEEP:
            position.tp = tp
        if (position.sl, position.tp) != (old_sl, old_tp):
            self.events.append(
                PositionModified(self._index, position, old_sl, old_tp)
            )

    def close_position(self, position: Position) -> None:
        """Request a close; fills at the next bar's open."""
        if position in self.positions and position.id not in self._close_queue:
            self._close_queue.append(position.id)

    def close_all(self) -> None:
        for position in list(self.positions):
            self.close_position(position)

    # --------------------------------------------------- engine-facing API

    def begin_bar(self, index: int, time: Any) -> None:
        self._index = index
        self._time = time

    def process_open(self, open_bid: float, ask_off: float) -> None:
        """Fill queued manual closes and market orders at the bar open."""
        for position_id in self._close_queue:
            position = self._find_position(position_id)
            if position is not None:
                price = open_bid if position.is_long else open_bid + ask_off
                self._close(position, price, CloseReason.MANUAL)
        self._close_queue.clear()

        for order in self._market_queue:
            price = open_bid + ask_off if order.direction is Direction.LONG else open_bid
            self._open(order, price)
        self._market_queue.clear()

    def process_pending(
        self, o: float, h: float, l: float, c: float, ask_off: float
    ) -> None:
        """Trigger limit/stop orders against the bar's range."""
        for order in list(self.pending):
            fill = self._pending_fill_price(order, o, h, l, ask_off)
            if fill is not None:
                self.pending.remove(order)
                self._open(order, fill)

    def process_sl_tp(
        self, o: float, h: float, l: float, c: float, ask_off: float
    ) -> None:
        """Close positions whose SL/TP falls inside the bar's range.

        A level gapped over at the open fills at the open price; otherwise it
        fills exactly at the level. SL is checked before TP (pessimistic).
        """
        for position in list(self.positions):
            sl, tp = position.sl, position.tp
            if position.is_long:  # levels compared against bid
                if sl is not None and o <= sl:
                    self._close(position, o, CloseReason.STOP_LOSS)
                elif sl is not None and l <= sl:
                    self._close(position, sl, CloseReason.STOP_LOSS)
                elif tp is not None and o >= tp:
                    self._close(position, o, CloseReason.TAKE_PROFIT)
                elif tp is not None and h >= tp:
                    self._close(position, tp, CloseReason.TAKE_PROFIT)
            else:  # levels compared against ask
                ask_o, ask_h, ask_l = o + ask_off, h + ask_off, l + ask_off
                if sl is not None and ask_o >= sl:
                    self._close(position, ask_o, CloseReason.STOP_LOSS)
                elif sl is not None and ask_h >= sl:
                    self._close(position, sl, CloseReason.STOP_LOSS)
                elif tp is not None and ask_o <= tp:
                    self._close(position, ask_o, CloseReason.TAKE_PROFIT)
                elif tp is not None and ask_l <= tp:
                    self._close(position, tp, CloseReason.TAKE_PROFIT)

    def apply_swap(self, nights: int) -> None:
        if nights <= 0:
            return
        for position in self.positions:
            rate = self.swap_long if position.is_long else self.swap_short
            position.swap += rate * position.lots * nights

    def equity(self, close_bid: float, ask_off: float) -> float:
        floating = 0.0
        for position in self.positions:
            price = close_bid if position.is_long else close_bid + ask_off
            floating += self._price_pnl(position, price) + position.swap
        return self.balance + floating

    def close_all_now(
        self, close_bid: float, ask_off: float, reason: CloseReason
    ) -> None:
        """Force-close everything at the current close (end of data/stop-out)."""
        for position in list(self.positions):
            price = close_bid if position.is_long else close_bid + ask_off
            self._close(position, price, reason)
        for order in list(self.pending):
            self.cancel_order(order)
        self._market_queue.clear()
        self._close_queue.clear()

    # ------------------------------------------------------------ internals

    def _make_order(self, type_, direction, lots, price, sl, tp, sl_pips, tp_pips, comment):
        if lots <= 0:
            raise ValueError(f"lots must be positive, got {lots}")
        order = Order(
            id=self._next_id, type=type_, direction=direction, lots=lots,
            price=price, sl=sl, tp=tp, sl_pips=sl_pips, tp_pips=tp_pips,
            comment=comment,
        )
        self._next_id += 1
        self.events.append(OrderPlaced(self._index, order))
        return order

    def _pending_fill_price(
        self, order: Order, o: float, h: float, l: float, ask_off: float
    ) -> float | None:
        if order.direction is Direction.LONG:  # buys trigger on ask
            ask_o, ask_h, ask_l = o + ask_off, h + ask_off, l + ask_off
            if order.type is OrderType.LIMIT:  # buy at or below price
                if ask_o <= order.price:
                    return ask_o
                if ask_l <= order.price:
                    return order.price
            else:                              # buy stop: at or above price
                if ask_o >= order.price:
                    return ask_o
                if ask_h >= order.price:
                    return order.price
        else:                                  # sells trigger on bid
            if order.type is OrderType.LIMIT:  # sell at or above price
                if o >= order.price:
                    return o
                if h >= order.price:
                    return order.price
            else:                              # sell stop: at or below price
                if o <= order.price:
                    return o
                if l <= order.price:
                    return order.price
        return None

    def _open(self, order: Order, fill_price: float) -> None:
        direction = order.direction
        sl, tp = order.sl, order.tp
        if sl is None and order.sl_pips is not None:
            sl = fill_price - direction * order.sl_pips * self.spec.pip
        if tp is None and order.tp_pips is not None:
            tp = fill_price + direction * order.tp_pips * self.spec.pip

        position = Position(
            id=order.id, direction=direction, lots=order.lots,
            entry_price=fill_price, entry_time=self._time,
            entry_index=self._index, sl=sl, tp=tp, comment=order.comment,
        )
        self.balance -= self.commission_per_lot * order.lots
        self.positions.append(position)
        self.events.append(PositionOpened(self._index, position))

    def _close(self, position: Position, price: float, reason: CloseReason) -> None:
        profit = self._price_pnl(position, price)
        side_commission = self.commission_per_lot * position.lots
        self.balance += profit + position.swap - side_commission
        self.positions.remove(position)
        if position.id in self._close_queue:
            self._close_queue.remove(position.id)

        trade = Trade(
            id=position.id, direction=position.direction, lots=position.lots,
            entry_price=position.entry_price, entry_time=position.entry_time,
            entry_index=position.entry_index,
            exit_price=price, exit_time=self._time, exit_index=self._index,
            profit=profit, commission=2 * side_commission, swap=position.swap,
            reason=reason, comment=position.comment,
        )
        self.trades.append(trade)
        self.events.append(PositionClosed(self._index, trade))

    def _price_pnl(self, position: Position, price: float) -> float:
        return (
            position.direction
            * (price - position.entry_price)
            * position.lots
            * self.spec.contract_size
        )

    def _find_position(self, position_id: int) -> Position | None:
        return next((p for p in self.positions if p.id == position_id), None)
