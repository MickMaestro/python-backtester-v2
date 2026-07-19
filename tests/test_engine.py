"""Engine-level behavior: event stream, bookkeeping, end of data, integration."""

import pytest

from backtester.engine.backtester import BacktestConfig, Backtester
from backtester.engine.events import BarEvent, EquityEvent, PositionClosed
from backtester.engine.orders import CloseReason
from backtester.strategy.examples import MaCross, RsiReversion

from tests.engine_utils import Scripted, events_of, make_df, make_wave

FLAT = [(1.1000, 1.1010, 1.0990, 1.1005)] * 6


def test_event_stream_shape():
    df = make_df(FLAT)
    events = list(Backtester(df, Scripted()).run())

    bar_events = events_of(events, BarEvent)
    equity_events = events_of(events, EquityEvent)
    assert len(bar_events) == len(df)
    assert [b.index for b in bar_events] == list(range(len(df)))
    assert len(equity_events) == len(df)
    assert isinstance(events[0], BarEvent)


def test_end_of_data_closes_open_position():
    df = make_df(FLAT)
    bt = Backtester(df, Scripted({0: [lambda s: s.buy(lots=1.0)]}))
    result = bt.run_all()

    assert len(result.trades) == 1
    trade = result.trades[0]
    assert trade.reason is CloseReason.END_OF_DATA
    assert trade.exit_index == len(df) - 1
    assert trade.exit_price == pytest.approx(df["close"].iloc[-1])
    assert bt.broker.positions == []
    # After everything is closed, equity equals balance.
    assert result.equity["equity"].iloc[-1] == pytest.approx(result.final_balance)


def test_balance_reconciles_with_trade_nets():
    strategy = MaCross(fast=5, slow=15, lots=0.3, sl_pips=30, tp_pips=60)
    config = BacktestConfig(commission_per_lot=6.0, spread_points=None)
    result = Backtester(make_wave(), strategy, config).run_all()

    assert len(result.trades) > 2
    net_sum = sum(t.net for t in result.trades)
    assert result.final_balance == pytest.approx(result.initial_balance + net_sum)
    assert result.stats["net_profit"] == pytest.approx(net_sum)
    assert result.stats["trades"] == len(result.trades)


def test_ma_cross_alternates_direction():
    result = Backtester(make_wave(), MaCross(fast=5, slow=20)).run_all()
    directions = [t.direction for t in result.trades]
    assert len(set(directions)) == 2  # both longs and shorts on a sine wave


def test_rsi_reversion_runs_and_reconciles():
    result = Backtester(make_wave(period=30), RsiReversion(period=7)).run_all()
    net_sum = sum(t.net for t in result.trades)
    assert result.final_balance == pytest.approx(result.initial_balance + net_sum)


def test_stats_drawdown_and_streaks_consistent():
    result = Backtester(make_wave(), MaCross(fast=5, slow=20)).run_all()
    stats = result.stats
    assert 0 <= stats["win_rate"] <= 1
    assert stats["max_drawdown"] >= 0
    assert 0 <= stats["max_drawdown_pct"] <= 100
    assert stats["wins"] + stats["losses"] == stats["trades"]


def test_events_match_result_trades():
    df = make_wave()
    bt = Backtester(df, MaCross(fast=5, slow=20))
    events = list(bt.run())
    result = bt.result()
    closed = events_of(events, PositionClosed)
    assert [c.trade.id for c in closed] == [t.id for t in result.trades]


def test_unknown_strategy_param_rejected():
    with pytest.raises(ValueError, match="Unknown parameter"):
        MaCross(fasst=10)


def test_empty_data_rejected():
    import pandas as pd

    empty = pd.DataFrame(columns=["time", "open", "high", "low", "close"])
    with pytest.raises(ValueError, match="empty"):
        Backtester(empty, Scripted())
