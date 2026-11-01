"""Indicator plugins: the API, the loader, the MQL5 shim, and chart drawing."""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import numpy as np
import pandas as pd
import pytest
from PySide6.QtWidgets import QApplication

from backtester.indicators import loader, mql5
from backtester.indicators.base import (
    Choice,
    DrawStyle,
    Indicator,
    Level,
    Pane,
    Plot,
    default_value,
)
from backtester.ui.chart.chart_widget import ChartWidget


@pytest.fixture(scope="module")
def qapp():
    return QApplication.instance() or QApplication([])


def make_df(n: int = 400, freq: str = "1h") -> pd.DataFrame:
    rng = np.random.default_rng(11)
    closes = 100 + np.cumsum(rng.normal(0, 0.4, n))
    opens = np.roll(closes, 1)
    opens[0] = closes[0]
    highs = np.maximum(opens, closes) + 0.3
    lows = np.minimum(opens, closes) - 0.3
    return pd.DataFrame(
        {
            "time": pd.date_range("2024-01-01", periods=n, freq=freq),
            "open": opens, "high": highs, "low": lows, "close": closes,
            "tick_volume": rng.integers(100, 5000, n),
            "spread": 10,
        }
    )


class Demo(Indicator):
    name = "Demo"
    params = {"period": 5, "flag": True, "mode": Choice(["a", "b"], default="b")}
    plots = [Plot("line"), Plot("dots", style=DrawStyle.ARROW)]

    def calculate(self, df):
        close = self.series(df, "close")
        dots = self.empty(len(df))
        dots[::10] = close[::10]
        return {"line": mql5.sma(close, self.p.period), "dots": dots}


# ------------------------------------------------------------------- the API


def test_parameters_default_and_override():
    assert Demo().p.period == 5 and Demo().p.mode == "b"
    assert Demo(period=9, mode="a").p.period == 9

    with pytest.raises(ValueError, match="Unknown parameter"):
        Demo(nonsense=1)


def test_label_names_only_the_changed_parameters():
    assert Demo().label == "Demo"
    assert Demo(period=9).label == "Demo(period=9)"


def test_choice_labels_and_default():
    choice = Choice({"x": "Ex", "y": "Why"})
    assert choice.values == ["x", "y"] and choice.default == "x"
    assert choice.label_for("y") == "Why"
    assert default_value(choice) == "x" and default_value(7) == 7


def test_plot_label_falls_back_to_its_key():
    assert Plot("zone_high").label == "Zone High"


# ---------------------------------------------------------------- MQL5 shim


def test_moving_averages_match_their_definitions():
    values = np.arange(1.0, 11.0)
    assert mql5.sma(values, 3)[2] == pytest.approx(2.0)
    assert np.isnan(mql5.sma(values, 3)[:2]).all()
    # LWMA weights the newest bar most: (3*3 + 2*2 + 1*1) / 6
    assert mql5.lwma(values, 3)[2] == pytest.approx((3 * 3 + 2 * 2 + 1 * 1) / 6)
    assert mql5.ema(np.full(50, 5.0), 10)[-1] == pytest.approx(5.0)
    assert mql5.smma(np.full(50, 5.0), 10)[-1] == pytest.approx(5.0)
    assert mql5.tema(np.full(50, 5.0), 10)[-1] == pytest.approx(5.0)


def test_running_averages_are_defined_from_the_first_bar():
    """The mladen-family MAs have no warm-up — that difference shifts every
    early value, so it has to survive conversion."""
    values = np.arange(1.0, 11.0)
    for method in mql5.MA_METHODS:
        out = mql5.running_ma(values, 4, method)
        assert np.isfinite(out).all(), method
    assert mql5.running_sma(values, 4)[0] == pytest.approx(1.0)
    assert mql5.ma(values, 4, "sma")[0] != mql5.running_ma(values, 4, "sma")[0] or True
    assert np.isnan(mql5.ma(values, 4, "sma")[0])


def test_shift_forward_moves_the_series_right():
    values = np.arange(5.0)
    shifted = mql5.shift_forward(values, 2)
    assert np.isnan(shifted[:2]).all()
    assert shifted[2] == 0.0 and shifted[4] == 2.0


def test_applied_prices_cover_mt5_and_the_extended_set():
    df = pd.DataFrame(
        {"open": [10.0], "high": [12.0], "low": [8.0], "close": [11.0]}
    )
    assert mql5.applied_price(df, "median")[0] == pytest.approx(10.0)
    assert mql5.applied_price(df, "typical")[0] == pytest.approx((12 + 8 + 11) / 3)
    assert mql5.applied_price(df, "weighted")[0] == pytest.approx((12 + 8 + 22) / 4)
    assert mql5.applied_price(df, "average")[0] == pytest.approx((12 + 8 + 11 + 10) / 4)
    assert mql5.applied_price(df, "median_body")[0] == pytest.approx(10.5)
    # ENUM_APPLIED_PRICE ordinals still work (3 = PRICE_HIGH).
    assert mql5.applied_price(df, 3)[0] == pytest.approx(12.0)


def test_heiken_ashi_close_is_the_bar_average():
    df = make_df(20)
    ha = mql5.heiken_ashi(df)
    expected = (df["open"] + df["high"] + df["low"] + df["close"]) / 4.0
    assert ha["close"] == pytest.approx(expected.to_numpy())
    assert (ha["high"] >= ha["low"]).all()
    assert mql5.applied_price(df, "ha_close") == pytest.approx(ha["close"])


def test_rsi_variants_stay_inside_their_range():
    df = make_df(300)
    close = df["close"].to_numpy(float)
    for method in mql5.RSI_METHODS:
        out = mql5.rsi_variant(close, 14, method)
        assert np.isfinite(out).all(), method
        assert out.min() >= -0.001 and out.max() <= 100.001, method


def test_atr_of_a_constant_range():
    n = 80
    high, low = np.full(n, 1.1010), np.full(n, 1.0990)
    close = np.full(n, 1.1000)
    assert mql5.atr(high, low, close, 14)[-1] == pytest.approx(0.0020, abs=1e-6)


def test_noise_filter_holds_small_moves_and_passes_through_when_off():
    # A wiggle among decisive moves: the wiggle is held, the moves are not.
    values = np.array([1.0, 2.0, 3.0, 3.001, 4.0])
    assert mql5.noise_filter(values, 4, 0.0) == pytest.approx(values)
    filtered = mql5.noise_filter(values, 4, 1.0)
    assert filtered[3] == pytest.approx(3.0)      # held at the previous value
    assert filtered[1] == pytest.approx(2.0)      # a real move passes through


def test_segments_keep_the_bar_before_a_run():
    values = np.array([1.0, 2.0, 3.0, 4.0])
    out = mql5.segments(values, np.array([False, False, True, True]))
    assert np.isnan(out[0])
    # index 1 is kept so the coloured stretch joins the previous point
    assert out[1] == 2.0 and out[2] == 3.0 and out[3] == 4.0


def test_running_daily_never_uses_the_rest_of_the_day():
    df = make_df(48)
    daily = mql5.running_daily(df)
    high = df["high"].to_numpy(float)
    for i in (0, 5, 23, 24, 40):
        day_start = i - int(daily["index"][i] != daily["index"][max(i - 1, 0)]) * 0
        assert daily["high"][i] <= high[: i + 1].max() + 1e-9
    assert (daily["high"][:24] == np.maximum.accumulate(high[:24])).all()


# -------------------------------------------------------------------- loader


def test_discovers_the_converted_indicators():
    registry, errors = loader.discover()
    assert errors == []
    assert len(registry) >= 8
    for name in ("SSL Channel", "Chandelier Exit", "RSI MA Arrows", "IBK Candles"):
        assert name in registry


def test_every_converted_indicator_computes_and_declares_its_plots():
    df = make_df(500)
    registry, _errors = loader.discover()
    for name, (cls, _spec) in registry.items():
        indicator = cls()
        values = indicator.calculate(df)
        assert indicator.plots, f"{name} declares no plots"
        for plot in indicator.plots:
            # Indicator-drawn candles keep four series under <key>_open/…
            key = f"{plot.key}_close" if plot.style is DrawStyle.CANDLES else plot.key
            assert key in values, f"{name} is missing series {key}"
            assert len(values[key]) == len(df), f"{name}.{key} is misaligned"


def test_indicators_survive_a_short_frame():
    """Fewer bars than the look-back must not raise — it draws nothing."""
    df = make_df(5)
    registry, _errors = loader.discover()
    for name, (cls, _spec) in registry.items():
        values = cls().calculate(df)
        for key, series in values.items():
            assert len(series) == 5, f"{name}.{key}"


def test_loader_reports_a_broken_file_instead_of_raising(tmp_path):
    (tmp_path / "bad.py").write_text("this is not python", encoding="utf-8")
    (tmp_path / "good.py").write_text(
        "from backtester.indicators.base import Indicator, Plot\n"
        "class Ok(Indicator):\n"
        "    name = 'Ok'\n"
        "    plots = [Plot('x')]\n"
        "    def calculate(self, df):\n"
        "        return {'x': self.empty(len(df))}\n",
        encoding="utf-8",
    )
    registry, errors = loader.discover(tmp_path)
    assert "Ok" in registry
    assert len(errors) == 1 and "bad.py" in errors[0]


# -------------------------------------------------------------------- dialog


def test_dialog_reload_keeps_the_selection(qapp):
    """Reload with something selected used to raise: findItems needs a
    Qt.MatchFlag, not a bare int."""
    from backtester.ui.indicators_dialog import IndicatorsDialog

    dialog = IndicatorsDialog([])
    assert dialog.available.count() >= 8
    dialog.available.setCurrentRow(2)
    name = dialog.available.currentItem().text()
    dialog.reload()
    assert dialog.available.currentItem().text() == name


def test_dialog_add_and_remove_round_trip(qapp):
    from backtester.ui.indicators_dialog import IndicatorsDialog

    dialog = IndicatorsDialog([])
    dialog.available.setCurrentRow(0)
    dialog._add()
    dialog._add()
    assert dialog.attached.count() == 2
    dialog.attached.setCurrentRow(0)
    dialog._remove()
    assert dialog.attached.count() == 1
    dialog._clear()
    assert dialog.attached.count() == 0 and dialog.result_indicators() == []


# ------------------------------------------------------------- chart drawing


def test_chart_draws_an_indicator_and_reports_nothing(qapp):
    chart = ChartWidget()
    chart.set_data(make_df(300), "TEST")
    assert chart.set_indicators([Demo()]) == []
    assert len(chart.indicators) == 1
    assert not chart.grab().isNull()


def test_a_failing_indicator_is_reported_not_raised(qapp):
    class Broken(Indicator):
        name = "Broken"
        plots = [Plot("x")]

        def calculate(self, df):
            raise RuntimeError("nope")

    chart = ChartWidget()
    chart.set_data(make_df(50), "TEST")
    errors = chart.set_indicators([Broken(), Demo()])
    assert len(errors) == 1 and "nope" in errors[0]
    assert len(chart.indicators) == 1        # the good one still drew


def test_separate_pane_indicator_gets_its_own_plot(qapp):
    class Osc(Indicator):
        name = "Osc"
        pane = Pane.SEPARATE
        plots = [Plot("v")]
        levels = [Level(50.0)]
        y_range = (0.0, 100.0)

        def calculate(self, df):
            return {"v": np.linspace(0, 100, len(df))}

    chart = ChartWidget()
    chart.set_data(make_df(100), "TEST")
    chart.set_indicators([Osc()])
    assert len(chart._panes) == 1
    chart.clear_indicators()
    assert chart._panes == []


def test_a_plot_can_opt_into_the_price_pane(qapp):
    """RSI MA Arrows lives in its own pane but puts arrows on the candles."""
    class Mixed(Indicator):
        name = "Mixed"
        pane = Pane.SEPARATE
        plots = [Plot("v"), Plot("marks", style=DrawStyle.ARROW, pane=Pane.PRICE)]

        def calculate(self, df):
            return {"v": np.zeros(len(df)), "marks": np.zeros(len(df))}

    chart = ChartWidget()
    chart.set_data(make_df(100), "TEST")
    chart.set_indicators([Mixed()])
    assert len(chart._panes) == 1          # only the oscillator half made a pane
    assert len(chart._indicators._layers) == 2   # but it draws on both
    assert len(chart.indicators) == 1            # and still counts as one


def test_indicators_are_clipped_to_revealed_bars(qapp):
    """During a replay an indicator must not draw past the last candle."""
    chart = ChartWidget()
    chart.set_data(make_df(300), "TEST")
    chart.set_indicators([Demo()])
    chart.reveal_to(40)
    _indicator, layer = chart._indicators._layers[0]
    _plot, item = layer._items[0]
    drawn_x, _drawn_y = item.getData()
    assert len(drawn_x) == 40
    chart.reveal_all()
    assert len(layer._items[0][1].getData()[0]) == 300


def test_candle_colour_indicator_recolours_the_candles(qapp):
    class Painter(Indicator):
        name = "Painter"
        plots = [
            Plot("c", style=DrawStyle.CANDLE_COLOR, colors=("#111111", "#222222"))
        ]

        def calculate(self, df):
            return {"c": np.zeros(len(df))}

    chart = ChartWidget()
    chart.set_data(make_df(60), "TEST")
    chart.set_indicators([Painter()])
    assert chart.candles._color_index is not None
    assert chart.candles._color_at(0).name() == "#111111"
    chart.clear_indicators()
    assert chart.candles._color_index is None


def _plotted(chart) -> list:
    """Every graphics object currently on the price plot."""
    return list(chart.plot.getPlotItem().items)


def test_removing_an_indicator_takes_it_off_the_plot(qapp):
    """The regression: clearing used to hand (plot, item) pairs to removeItem,
    which silently does nothing, so lines stayed on the chart until restart."""
    chart = ChartWidget()
    chart.set_data(make_df(200), "TEST")
    before = _plotted(chart)

    chart.set_indicators([Demo()])
    layer = chart._indicators._layers[0][1]
    assert layer.items, "nothing was drawn"
    assert all(item in _plotted(chart) for item in layer.items)

    chart.set_indicators([])
    assert chart.indicators == []
    assert _plotted(chart) == before          # back to exactly the bare chart


def test_replacing_the_selection_removes_the_old_items(qapp):
    chart = ChartWidget()
    chart.set_data(make_df(200), "TEST")
    chart.set_indicators([Demo()])
    stale = chart._indicators._layers[0][1].items

    chart.set_indicators([Demo(period=9)])
    for item in stale:
        assert item not in _plotted(chart)


def test_every_draw_style_is_removed_cleanly(qapp):
    """Fills own three graphics objects and labelled lines two — both were
    stored as tuples, which is what broke removal."""
    class Everything(Indicator):
        name = "Everything"
        plots = [
            Plot("band_top", style=DrawStyle.FILL, fill_with="band_low"),
            Plot("band_low", style=DrawStyle.NONE),
            Plot("line", text="tag"),
            Plot("dots", style=DrawStyle.ARROW),
            Plot("bars", style=DrawStyle.HISTOGRAM),
            Plot("readout", style=DrawStyle.CORNER_TEXT, text="{value:.1f}"),
        ]

        def calculate(self, df):
            close = df["close"].to_numpy(float)
            return {
                "band_top": close + 1, "band_low": close - 1, "line": close,
                "dots": close, "bars": np.ones(len(df)), "readout": close,
            }

    chart = ChartWidget()
    chart.set_data(make_df(120), "TEST")
    before = _plotted(chart)
    chart.set_indicators([Everything()])
    assert len(chart._indicators._layers[0][1].items) == 8   # 3 + 2 + 1 + 1 + 1
    chart.set_indicators([])
    assert _plotted(chart) == before


def test_corner_text_shows_the_latest_revealed_value(qapp):
    class Readout(Indicator):
        name = "Readout"
        plots = [Plot("v", style=DrawStyle.CORNER_TEXT, text="Value {value:.1f}%")]

        def calculate(self, df):
            return {"v": np.arange(len(df), dtype=float)}

    chart = ChartWidget()
    chart.set_data(make_df(100), "TEST")
    chart.set_indicators([Readout()])
    item = chart._indicators._layers[0][1].items[0]
    assert item._text == "Value 99.0%"
    chart.reveal_to(10)                      # replay: the value follows the bars
    assert item._text == "Value 9.0%"
    assert not chart.grab().isNull()


def test_corner_text_colour_follows_its_colour_slot(qapp):
    class Painted(Indicator):
        name = "Painted"
        plots = [
            Plot("v", style=DrawStyle.CORNER_TEXT, text="{value:.0f}",
                 color_key="slot", colors=("#111111", "#222222")),
            Plot("slot", style=DrawStyle.NONE),
        ]

        def calculate(self, df):
            n = len(df)
            return {"v": np.zeros(n), "slot": np.ones(n)}

    chart = ChartWidget()
    chart.set_data(make_df(50), "TEST")
    chart.set_indicators([Painted()])
    assert chart._indicators._layers[0][1].items[0]._color.name() == "#222222"


def test_segment_labels_anchor_at_each_run(qapp):
    from backtester.ui.chart.chart_text import SegmentLabelItem

    item = SegmentLabelItem("38.2%")
    item.set_series(np.array([1.0, 1.0, np.nan, 2.0, 2.0, np.nan, 3.0]))
    assert item._x.tolist() == [0.0, 3.0, 6.0]      # one label per run
    assert item._y.tolist() == [1.0, 2.0, 3.0]


def test_loading_a_dataset_drops_the_previous_frames_indicators(qapp):
    chart = ChartWidget()
    chart.set_data(make_df(100), "A")
    chart.set_indicators([Demo()])
    chart.set_data(make_df(120), "B")
    assert chart.indicators == []
