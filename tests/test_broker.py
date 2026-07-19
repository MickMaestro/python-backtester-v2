"""Fill mechanics: market/pending orders, SL/TP, spread, commission, swap."""

import pytest

from backtester.engine.backtester import BacktestConfig, Backtester
from backtester.engine.events import (
    OrderCancelled,
    PositionClosed,
    PositionModified,
    PositionOpened,
)
from backtester.engine.orders import CloseReason, Direction

from tests.engine_utils import Scripted, events_of, make_df

CONTRACT = 100_000.0
FLAT = [(1.1000, 1.1010, 1.0990, 1.1005)] * 6


def run(df, script, **config_kwargs):
    strategy = Scripted(script)
    bt = Backtester(df, strategy, BacktestConfig(**config_kwargs))
    events = list(bt.run())
    return bt.result(), events


def test_market_buy_fills_next_open_with_spread():
    df = make_df(
        [
            (1.1000, 1.1010, 1.0990, 1.1005),
            (1.1020, 1.1030, 1.1010, 1.1025),  # entry here at open ask
            (1.1040, 1.1050, 1.1030, 1.1045),  # close requested on this bar
            (1.1060, 1.1070, 1.1050, 1.1065),  # exit here at open bid
        ]
    )
    result, events = run(
        df,
        {0: [lambda s: s.buy(lots=1.0)], 2: [lambda s: s.close_all()]},
        spread_points=20,  # 0.0002 on a 5-digit pair
    )

    opened = events_of(events, PositionOpened)[0]
    assert opened.index == 1
    assert opened.position.entry_price == pytest.approx(1.1020 + 0.0002)

    closed = events_of(events, PositionClosed)[0]
    assert closed.index == 3
    trade = closed.trade
    assert trade.reason is CloseReason.MANUAL
    assert trade.exit_price == pytest.approx(1.1060)  # longs close at bid
    assert trade.profit == pytest.approx((1.1060 - 1.1022) * CONTRACT)
    assert result.final_balance == pytest.approx(10_000 + trade.net)


def test_long_sl_fills_at_level():
    df = make_df(
        [
            (1.1000, 1.1010, 1.0990, 1.1005),
            (1.1000, 1.1010, 1.0990, 1.1005),  # entry at open 1.1000
            (1.1000, 1.1005, 1.0945, 1.0990),  # low pierces SL 1.0950
            (1.1000, 1.1010, 1.0990, 1.1005),
        ]
    )
    result, events = run(df, {0: [lambda s: s.buy(lots=1.0, sl=1.0950)]})

    trade = result.trades[0]
    assert trade.reason is CloseReason.STOP_LOSS
    assert trade.exit_index == 2
    assert trade.exit_price == pytest.approx(1.0950)
    assert trade.profit == pytest.approx((1.0950 - 1.1000) * CONTRACT)


def test_long_tp_gap_fills_at_open():
    df = make_df(
        [
            (1.1000, 1.1010, 1.0990, 1.1005),
            (1.1000, 1.1010, 1.0990, 1.1080),  # entry at 1.1000
            (1.1150, 1.1160, 1.1140, 1.1155),  # gaps above TP 1.1100
        ]
    )
    result, _ = run(df, {0: [lambda s: s.buy(lots=1.0, tp=1.1100)]})

    trade = result.trades[0]
    assert trade.reason is CloseReason.TAKE_PROFIT
    assert trade.exit_price == pytest.approx(1.1150)  # open, not the level


def test_sl_checked_before_tp_in_same_bar():
    df = make_df(
        [
            (1.1000, 1.1010, 1.0990, 1.1005),
            (1.1000, 1.1200, 1.0900, 1.1005),  # bar range covers both levels
        ]
    )
    result, _ = run(
        df, {0: [lambda s: s.buy(lots=1.0, sl=1.0950, tp=1.1100)]}
    )
    assert result.trades[0].reason is CloseReason.STOP_LOSS


def test_short_sl_triggers_on_ask():
    # Short from 1.1000 (bid). SL 1.1030 on ask; spread 20 pts. The bar high
    # of 1.1029 has ask 1.1031 >= SL, so it must trigger even though the bid
    # never reached the level.
    df = make_df(
        [
            (1.1000, 1.1010, 1.0990, 1.1005),
            (1.1000, 1.1010, 1.0990, 1.1005),  # entry at open bid 1.1000
            (1.1010, 1.1029, 1.1000, 1.1010),
        ]
    )
    result, _ = run(
        df, {0: [lambda s: s.sell(lots=1.0, sl=1.1030)]}, spread_points=20
    )

    trade = result.trades[0]
    assert trade.reason is CloseReason.STOP_LOSS
    assert trade.exit_price == pytest.approx(1.1030)
    assert trade.profit == pytest.approx(-(1.1030 - 1.1000) * CONTRACT)


def test_sl_pips_converted_at_fill_price():
    df = make_df(FLAT)
    _, events = run(df, {0: [lambda s: s.buy(lots=1.0, sl_pips=50, tp_pips=100)]})

    position = events_of(events, PositionOpened)[0].position
    assert position.sl == pytest.approx(position.entry_price - 0.0050)
    assert position.tp == pytest.approx(position.entry_price + 0.0100)


def test_commission_charged_per_side():
    df = make_df(FLAT)
    result, _ = run(
        df,
        {0: [lambda s: s.buy(lots=0.5)], 2: [lambda s: s.close_all()]},
        commission_per_lot=7.0,
    )
    trade = result.trades[0]
    assert trade.commission == pytest.approx(7.0)  # 2 sides x 7.0/lot x 0.5 lots
    assert result.final_balance == pytest.approx(
        10_000 + trade.profit - trade.commission
    )


def test_swap_accrues_per_night():
    # Hourly bars from 22:00 crossing one midnight; long 2.0 lots, -2.5/lot/night.
    df = make_df(FLAT[:5], start="2024-01-01 22:00")
    result, _ = run(
        df, {0: [lambda s: s.buy(lots=2.0)]}, swap_long=-2.5
    )
    trade = result.trades[0]
    assert trade.swap == pytest.approx(-5.0)
    assert trade.reason is CloseReason.END_OF_DATA
    assert result.final_balance == pytest.approx(10_000 + trade.profit - 5.0)


def test_buy_limit_fills_at_level():
    df = make_df(
        [
            (1.1000, 1.1010, 1.0990, 1.1005),
            (1.1000, 1.1010, 1.0990, 1.1005),  # never reaches 1.0950
            (1.1000, 1.1005, 1.0940, 1.0980),  # dips through the limit
        ]
    )
    _, events = run(df, {0: [lambda s: s.buy_limit(1.0950, lots=1.0)]})

    opened = events_of(events, PositionOpened)[0]
    assert opened.index == 2
    assert opened.position.entry_price == pytest.approx(1.0950)
    assert opened.position.direction is Direction.LONG


def test_untriggered_pending_cancelled_at_end():
    df = make_df(FLAT)
    result, events = run(df, {0: [lambda s: s.buy_stop(1.2000, lots=1.0)]})

    assert result.trades == []
    assert len(events_of(events, OrderCancelled)) == 1


def test_modify_position_emits_event_and_new_sl_applies():
    df = make_df(
        [
            (1.1000, 1.1010, 1.0990, 1.1005),
            (1.1000, 1.1010, 1.0990, 1.1005),  # entry, SL 1.0900
            (1.1000, 1.1010, 1.0990, 1.1005),  # SL moved to 1.0995
            (1.1000, 1.1005, 1.0993, 1.1000),  # low 1.0993 hits new SL only
        ]
    )
    result, events = run(
        df,
        {
            0: [lambda s: s.buy(lots=1.0, sl=1.0900)],
            2: [lambda s: s.modify(s.position, sl=1.0995)],
        },
    )

    modified = events_of(events, PositionModified)[0]
    assert modified.old_sl == pytest.approx(1.0900)
    assert modified.position.sl == pytest.approx(1.0995)

    trade = result.trades[0]
    assert trade.reason is CloseReason.STOP_LOSS
    assert trade.exit_price == pytest.approx(1.0995)
