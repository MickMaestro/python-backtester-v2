"""Trade context logs: event recording, indicator collection, and the writer."""

import csv
import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import numpy as np
import pandas as pd
import pytest
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication

from backtester.engine.backtester import BacktestConfig, Backtester
from backtester.engine.events import PositionModified
from backtester.engine.trade_log import (
    CONTEXT_NAME,
    ENTRY,
    EXIT,
    INDICATORS_NAME,
    MANIFEST_NAME,
    MODIFY,
    ContextMode,
    TradeLogReport,
    TradeLogSpec,
    collect_indicators,
    count_moments,
    event_kind,
    log_run,
    run_folder_name,
)
from backtester.strategy.base import Strategy
from backtester.ui.trade_log import TradeLogDialog, TradeLogSettings
from tests.engine_utils import Scripted, make_df


@pytest.fixture(scope="module")
def qapp():
    return QApplication.instance() or QApplication([])


def flat_df(n: int = 12, freq: str = "1h"):
    """Flat bars: nothing triggers on its own, so the script drives every event."""
    return make_df([(1.0, 1.1, 0.9, 1.0)] * n, freq=freq)


ONE_TRADE = {
    0: [lambda s: s.buy(lots=0.1, sl=0.5, tp=1.5)],
    2: [lambda s: s.modify(s.position, sl=0.6)],
    4: [lambda s: s.modify(s.position, sl=0.7)],
    6: [lambda s: s.close_all()],
}


class Indicated(Scripted):
    """A scripted strategy that also builds indicators, like a real one."""

    def init(self):
        self.trend = self.ind.ema(3)
        self.rng = self.ind.atr(2)


def scripted_run(script=None, n=12, record=True, strategy=None, freq="1h"):
    df = flat_df(n, freq)
    if strategy is None:
        strategy = Scripted(ONE_TRADE if script is None else script)
    backtester = Backtester(
        df, strategy, BacktestConfig(spread_points=0), record_events=record
    )
    return df, backtester.run_all(), strategy


# ----------------------------------------------------------- event recording


def test_events_are_not_recorded_unless_asked():
    _df, result, _s = scripted_run(record=False)
    assert result.trades and result.events == []


def test_records_entry_modifications_and_exit_in_order():
    _df, result, _s = scripted_run()
    assert [event_kind(e) for e in result.events] == [ENTRY, MODIFY, MODIFY, EXIT]


def test_modification_events_keep_the_levels_of_their_moment():
    """The regression that matters: Position is mutable and keeps being
    modified, so a stored reference would report the *final* SL everywhere —
    every trailing-stop row in the log would be wrong."""
    _df, result, _s = scripted_run()
    modifications = [e for e in result.events if isinstance(e, PositionModified)]
    assert [e.position.sl for e in modifications] == [0.6, 0.7]
    assert [e.old_sl for e in modifications] == [0.5, 0.6]


def test_recorded_entry_keeps_its_original_stop():
    _df, result, _s = scripted_run()
    assert result.events[0].position.sl == 0.5      # not 0.7, where it ended


# -------------------------------------------------------------- indicators


def test_collect_indicators_finds_series_and_recipes():
    df, _result, strategy = scripted_run(strategy=Indicated(ONE_TRADE))
    found = {i.column: i for i in collect_indicators(strategy, len(df))}
    assert set(found) == {"trend", "rng"}
    assert found["trend"].recipe == "ema(3, Close)"
    assert found["rng"].recipe == "atr(2)"
    assert len(found["trend"].values) == len(df)


def test_collect_indicators_ignores_the_bar_arrays():
    """``bind`` attaches opens/highs/lows/closes/time — data, not indicators."""
    df, _result, strategy = scripted_run(strategy=Indicated(ONE_TRADE))
    columns = {i.column for i in collect_indicators(strategy, len(df))}
    assert not columns & {"time", "opens", "highs", "lows", "closes"}


def test_collect_indicators_renames_columns_that_clash_with_bar_data():
    class Clashing(Scripted):
        def init(self):
            self.close = self.ind.sma(3)     # would collide with the bar column

    df, _result, strategy = scripted_run(strategy=Clashing(ONE_TRADE))
    found = collect_indicators(strategy, len(df), reserved={"close", "offset"})
    assert [i.column for i in found] == ["ind_close"]
    assert found[0].attribute == "close"


def test_hand_rolled_series_are_logged_without_a_recipe():
    class Custom(Scripted):
        def init(self):
            self.mine = np.arange(len(self.closes), dtype=float)

    df, _result, strategy = scripted_run(strategy=Custom(ONE_TRADE))
    found = {i.column: i for i in collect_indicators(strategy, len(df))}
    assert found["mine"].recipe == ""        # not built by the factory


# ------------------------------------------------------------------ counting


def test_count_moments_follows_the_selected_kinds():
    _df, result, _s = scripted_run()
    events = result.events
    assert count_moments(events, TradeLogSpec()) == 4
    assert count_moments(events, TradeLogSpec(modifications=False)) == 2
    assert count_moments(
        events, TradeLogSpec(entries=False, modifications=False)
    ) == 1


def test_run_folder_name_is_filesystem_safe():
    name = run_folder_name("EURUSD_H1", "my strat/v2:test")
    assert name.startswith("EURUSD_H1_my_strat_v2_test_")
    assert not set(name) & set('\\/:*?"<>| ')


# -------------------------------------------------------------------- writing


def write_log(tmp_path, spec=None, n=12, **kwargs):
    df, result, strategy = scripted_run(strategy=Indicated(ONE_TRADE), n=n)
    folder = tmp_path / "log"
    report = log_run(df, result, strategy, folder, spec or TradeLogSpec(), **kwargs)
    return df, folder, report


def read_context(folder):
    return pd.read_parquet(folder / CONTEXT_NAME)


def test_writes_context_manifest_and_indicator_files(tmp_path):
    _df, folder, report = write_log(tmp_path)
    assert {p.name for p in folder.iterdir()} == {
        CONTEXT_NAME, MANIFEST_NAME, INDICATORS_NAME
    }
    assert report.moments == 4 and not report.truncated


def test_context_holds_one_window_per_moment(tmp_path):
    _df, folder, report = write_log(tmp_path)
    context = read_context(folder)
    assert list(context["frame_id"].unique()) == [
        "0001_entry", "0001_modify_01", "0001_modify_02", "0001_exit"
    ]
    assert len(context) == report.rows
    # Every window ends on its moment, and offsets count back from there.
    for frame_id, block in context.groupby("frame_id", sort=False):
        assert block["offset"].iloc[-1] == 0
        assert block["offset"].is_monotonic_increasing
        assert (block["bar_index"] - block["event_index"] == block["offset"]).all()


def test_context_carries_bar_and_indicator_columns(tmp_path):
    df, folder, _report = write_log(tmp_path)
    context = read_context(folder)
    for column in df.columns:
        assert column in context.columns
    assert {"trend", "rng"} <= set(context.columns)
    # Values line up with the source data at the same bar index.
    row = context.iloc[-1]
    i = int(row["bar_index"])
    assert row["close"] == pytest.approx(df["close"].iloc[i])
    assert row["time"] == df["time"].iloc[i]


def test_bars_mode_never_logs_past_the_moment(tmp_path):
    """The window is the history the strategy had — no look-ahead."""
    _df, folder, _report = write_log(tmp_path, TradeLogSpec(context_bars=4))
    context = read_context(folder)
    assert context["offset"].max() == 0
    # The exit is at bar 7, so its window is the full four bars 4..7.
    exit_window = context[context["frame_id"] == "0001_exit"]
    assert len(exit_window) == 4
    assert list(exit_window["offset"]) == [-3, -2, -1, 0]


def test_bars_mode_clips_at_the_start_of_the_data(tmp_path):
    _df, folder, _report = write_log(tmp_path, TradeLogSpec(context_bars=500))
    entry = read_context(folder).query("frame_id == '0001_entry'")
    assert entry["bar_index"].min() == 0         # no negative indices


def test_day_mode_logs_the_whole_calendar_day(tmp_path):
    # Hourly bars over three days; the trade happens on the first.
    _df, folder, _report = write_log(
        tmp_path, TradeLogSpec(mode=ContextMode.DAY), n=72
    )
    context = read_context(folder)
    entry = context[context["frame_id"] == "0001_entry"]
    assert len(entry) == 24
    assert entry["time"].dt.date.nunique() == 1
    # A day includes what came after the moment, unlike bars mode.
    assert entry["offset"].max() > 0


def test_manifest_describes_every_moment(tmp_path):
    df, folder, _report = write_log(tmp_path)
    with open(folder / MANIFEST_NAME, newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert [row["kind"] for row in rows] == [ENTRY, MODIFY, MODIFY, EXIT]
    assert {row["trade_id"] for row in rows} == {"1"}
    assert rows[0]["direction"] == "buy" and rows[0]["sl"] == "0.5"
    assert rows[1]["old_sl"] == "0.5" and rows[1]["sl"] == "0.6"
    assert rows[-1]["reason"] == "manual"
    # Each row states the window it wrote.
    for row in rows:
        assert int(row["bars"]) > 0
        assert row["context_from"] and row["context_to"]
        assert row["time"] == str(df["time"].iloc[int(row["bar_index"])])


def test_indicators_file_documents_each_column(tmp_path):
    _df, folder, _report = write_log(tmp_path)
    with open(folder / INDICATORS_NAME, newline="", encoding="utf-8") as handle:
        rows = {row["column"]: row for row in csv.DictReader(handle)}
    assert rows["trend"]["recipe"] == "ema(3, Close)"
    assert rows["rng"]["recipe"] == "atr(2)"
    assert rows["trend"]["attribute"] == "trend"


def test_log_honours_the_selected_kinds(tmp_path):
    _df, folder, report = write_log(
        tmp_path, TradeLogSpec(entries=False, modifications=False)
    )
    assert list(read_context(folder)["frame_id"].unique()) == ["0001_exit"]
    assert report.moments == 1 and report.total == 1


def test_log_stops_at_the_moment_limit(tmp_path):
    _df, folder, report = write_log(tmp_path, TradeLogSpec(max_moments=2))
    assert report.moments == 2 and report.total == 4 and report.truncated
    assert len(read_context(folder)["frame_id"].unique()) == 2


def test_log_can_be_cancelled(tmp_path):
    calls = []

    def should_cancel():
        calls.append(1)
        return len(calls) > 2

    _df, folder, report = write_log(tmp_path, should_cancel=should_cancel)
    assert report.cancelled and report.moments == 2
    assert (folder / MANIFEST_NAME).exists()     # keeps what it logged


def test_nothing_selected_writes_no_folder(tmp_path):
    _df, folder, report = write_log(
        tmp_path, TradeLogSpec(entries=False, modifications=False, exits=False)
    )
    assert report.moments == 0 and not folder.exists()


def test_a_run_without_trades_writes_nothing(tmp_path):
    df, result, strategy = scripted_run(script={})
    folder = tmp_path / "log"
    report = log_run(df, result, strategy, folder)
    assert report.total == 0 and not folder.exists()
    assert report.message() == "Trade log: nothing to log."


# ------------------------------------------------------------------ reporting


def test_report_messages_name_the_folder(tmp_path):
    folder = tmp_path / "EURUSD_H1_ma_cross_20260727-120000"
    assert "4 moments, 480 bars" in TradeLogReport(folder, 4, 480, 4).message()
    assert "limit reached" in TradeLogReport(folder, 2, 240, 9).message()
    assert "cancelled" in TradeLogReport(folder, 2, 240, 9, cancelled=True).message()
    assert folder.name in TradeLogReport(folder, 4, 480, 4).message()


# ------------------------------------------------------------------- settings


def test_settings_roundtrip(qapp, tmp_path, monkeypatch):
    ini = QSettings(str(tmp_path / "s.ini"), QSettings.Format.IniFormat)
    monkeypatch.setattr("backtester.ui.trade_log.app_settings", lambda: ini)

    TradeLogSettings(
        enabled=True,
        folder=str(tmp_path),
        spec=TradeLogSpec(
            entries=False, modifications=True, exits=False,
            mode=ContextMode.DAY, context_bars=250, max_moments=0,
        ),
    ).save()
    loaded = TradeLogSettings.load()
    assert loaded.enabled is True and loaded.directory() == tmp_path
    assert loaded.spec.entries is False and loaded.spec.mode is ContextMode.DAY
    assert loaded.spec.context_bars == 250
    assert loaded.spec.max_moments == 0            # 0 = no limit, not "unset"


def test_default_folder_used_when_unset():
    assert TradeLogSettings().directory().name == "trade_logs"


def test_dialog_reflects_edits(qapp):
    dialog = TradeLogDialog(TradeLogSettings(enabled=True))
    dialog.modify_check.setChecked(False)
    dialog.context_spin.setValue(300)
    dialog.max_spin.setValue(50)
    out = dialog.result_settings(enabled=True)
    assert out.enabled is True and out.spec.modifications is False
    assert out.spec.context_bars == 300 and out.spec.max_moments == 50
    assert out.spec.kinds == {ENTRY, EXIT}


def test_dialog_disables_bar_count_in_day_mode(qapp):
    dialog = TradeLogDialog(TradeLogSettings())
    assert dialog.context_spin.isEnabled()
    dialog.mode_combo.setCurrentIndex(dialog.mode_combo.findData(ContextMode.DAY))
    assert not dialog.context_spin.isEnabled()
    assert dialog.result_settings(enabled=False).spec.mode is ContextMode.DAY


def test_dialog_restore_defaults(qapp):
    dialog = TradeLogDialog(
        TradeLogSettings(spec=TradeLogSpec(modifications=False, context_bars=9))
    )
    dialog._restore_defaults()
    assert dialog.result_settings(enabled=False) == TradeLogSettings()
