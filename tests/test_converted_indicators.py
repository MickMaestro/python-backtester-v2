"""The MQL5 Codebase conversions: every plugin computes, nothing leaks the
future onto the replay, and the shared maths matches MetaTrader's formulas."""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import numpy as np
import pandas as pd
import pytest
from PySide6.QtWidgets import QApplication

from backtester.data.store import DataStore
from backtester.indicators import loader, mql5, onarray, smoothing
from backtester.indicators.base import DrawStyle, Indicator, Pane, Plot
from backtester.ui.chart.indicator_layer import (
    IndicatorLayer,
    RepaintSource,
    zigzag_points,
)

REGISTRY, LOAD_ERRORS = loader.discover()


@pytest.fixture(scope="module")
def qapp():
    return QApplication.instance() or QApplication([])


def forex_df(n: int = 1500, freq: str = "15min", seed: int = 3) -> pd.DataFrame:
    """EURUSD-like bars quoted to 5 digits, so ``_Point`` resolves to 1e-5."""
    rng = np.random.default_rng(seed)
    close = 1.10 + rng.normal(0, 0.0006, n).cumsum() + 0.004 * np.sin(np.arange(n) / 40)
    open_ = np.r_[close[0], close[:-1]]
    high = np.maximum(open_, close) + rng.uniform(0, 0.0008, n)
    low = np.minimum(open_, close) - rng.uniform(0, 0.0008, n)
    return pd.DataFrame({
        "time": pd.date_range("2024-01-01", periods=n, freq=freq),
        "open": open_.round(5), "high": high.round(5), "low": low.round(5),
        "close": close.round(5), "tick_volume": rng.integers(50, 500, n),
        "spread": 10, "real_volume": 0,
    })


DF = forex_df()


def plot_keys(plot: Plot) -> list[str]:
    if plot.style is DrawStyle.CANDLES:
        return [f"{plot.key}_{part}" for part in ("open", "high", "low", "close")]
    return [plot.key] + ([plot.fill_with] if plot.fill_with else [])


# ------------------------------------------------------------ the plugins


def test_every_plugin_file_loads():
    assert LOAD_ERRORS == []
    assert len(REGISTRY) >= 98       # 8 earlier conversions + 90 from the Codebase


@pytest.mark.parametrize("name", sorted(REGISTRY))
def test_plugin_computes_every_declared_series(name):
    cls, _spec = REGISTRY[name]
    indicator = cls()
    out = indicator.calculate(DF)
    for plot in indicator.plots:
        for key in plot_keys(plot) + [k for k in (plot.known_at, plot.expires_at) if k]:
            assert key in out, f"{name}: missing {key}"
            assert len(out[key]) == len(DF), f"{name}: {key} has the wrong length"


@pytest.mark.parametrize("name", sorted(REGISTRY))
def test_replay_shows_only_what_was_known(name):
    """At every replay position k, what the chart draws (the full result —
    or for repainting indicators the RepaintSource splice — clipped to k and
    honouring ``known_at``) must equal a computation on the first k bars."""
    cls, _spec = REGISTRY[name]
    indicator = cls()
    full = indicator.calculate(DF)
    source = RepaintSource(indicator, DF, full) if indicator.repaint_window else None
    for k in (300, 900):
        shown = source.values_at(k) if source else full
        prefix = cls().calculate(DF.iloc[:k].reset_index(drop=True))
        for plot in indicator.plots:
            if plot.expires_at:       # replaced over time by design
                continue
            for key in plot_keys(plot):
                a = np.asarray(shown[key], dtype=float)[:k].copy()
                b = np.asarray(prefix[key], dtype=float)[:k].copy()
                if plot.known_at:
                    a[~(np.asarray(shown[plot.known_at])[:k] < k)] = np.nan
                    b[~(np.asarray(prefix[plot.known_at])[:k] < k)] = np.nan
                if plot.style in (DrawStyle.LINE, DrawStyle.FILL):
                    # A colour run's joining bar at the very edge (see
                    # mql5.segments) is decided by the next bar; ignore it.
                    a[k - 1] = b[k - 1] = np.nan
                assert np.array_equal(np.isfinite(a), np.isfinite(b)), \
                    f"{name}: {key} differs in which bars it draws at k={k}"
                both = np.isfinite(a)
                np.testing.assert_allclose(a[both], b[both], rtol=1e-7, atol=1e-9,
                                           err_msg=f"{name}: {key} at k={k}")


# --------------------------------------------------------------- MT5 maths


def test_atr_is_a_simple_average_of_true_range():
    h = DF["high"].to_numpy()
    l = DF["low"].to_numpy()
    c = DF["close"].to_numpy()
    atr = mql5.atr(h, l, c, 14)
    tr = mql5.true_range(h, l, c)
    assert np.isnan(atr[13])
    assert atr[14] == pytest.approx(tr[1:15].mean())
    assert atr[200] == pytest.approx(tr[187:201].mean())


def test_wpr_and_cci_match_their_definitions():
    h = DF["high"].to_numpy()
    l = DF["low"].to_numpy()
    c = DF["close"].to_numpy()
    wpr = mql5.wpr(h, l, c, 10)
    i = 50
    hh, ll = h[i - 9: i + 1].max(), l[i - 9: i + 1].min()
    assert wpr[i] == pytest.approx(-(hh - c[i]) * 100 / (hh - ll))

    tp = mql5.applied_price(DF, "typical")
    cci = mql5.cci(tp, 14)
    window = tp[i - 13: i + 1]
    mean = window.mean()
    assert cci[i] == pytest.approx((tp[i] - mean) / (np.abs(window - mean).mean() * 0.015))


def test_rsi_is_wilder_smoothed():
    rising = np.arange(1.0, 40.0)
    assert mql5.rsi(rising, 14)[-1] == pytest.approx(100.0)
    flat_then_mixed = np.r_[np.full(15, 5.0), 5.5, 5.0]
    out = mql5.rsi(flat_then_mixed, 14)
    assert out[15] == pytest.approx(100.0)      # only a gain so far
    assert 0.0 < out[16] < 100.0


def test_sar_trails_below_an_uptrend():
    n = 60
    low = np.linspace(1.0, 2.0, n)
    high = low + 0.05
    sar = mql5.sar(high, low)
    assert np.all(sar[10:] < low[10:])


def test_zigzag_alternates_peaks_and_troughs():
    peaks, troughs = mql5.zigzag(DF["high"].to_numpy(), DF["low"].to_numpy(), 12, 5e-5, 3)
    kinds = [1 if np.isfinite(p) else -1
             for p, t in zip(peaks, troughs) if np.isfinite(p) or np.isfinite(t)]
    assert len(kinds) > 10
    assert all(a != b for a, b in zip(kinds, kinds[1:]))


def test_pivot_line_knows_each_leg_when_it_ends():
    pivots = np.full(10, np.nan)
    pivots[[1, 4, 8]] = [1.0, 4.0, 0.0]
    line, known = mql5.pivot_line(pivots)
    assert line[2] == pytest.approx(2.0)
    assert known[1] == 1 and known[2] == 4 and known[6] == 8
    assert np.isinf(known[9]) and np.isnan(line[9])


def test_point_comes_from_the_store_or_the_prices(tmp_path):
    assert mql5.digits(DF) == 5 and mql5.point(DF) == pytest.approx(1e-5)
    store = DataStore(tmp_path)
    store.save_bars("XAUUSD", "H1", DF, spec={"point": 0.01, "digits": 2})
    loaded = store.load_bars("XAUUSD", "H1")
    assert mql5.point(loaded) == pytest.approx(0.01) and mql5.digits(loaded) == 2


# ------------------------------------------------------ library smoothing


def test_onarray_ema_is_seeded_with_the_first_value():
    values = np.r_[np.nan, np.nan, 2.0, 4.0, 4.0]
    out = onarray.ma(values, 3, "ema")
    assert np.isnan(out[1]) and out[2] == 2.0
    assert out[3] == pytest.approx(2.0 + 0.5 * (4.0 - 2.0))


@pytest.mark.parametrize("method", smoothing.METHODS)
def test_every_xma_method_holds_a_constant_series(method):
    values = np.full(300, 1.2345)
    out = smoothing.xma(values, method, 12, 50)
    finite = out[np.isfinite(out)]
    assert len(finite) > 200
    np.testing.assert_allclose(finite, 1.2345, rtol=1e-9)


def test_xma_start_offsets_match_the_library():
    values = np.arange(100.0)
    assert np.isnan(smoothing.lwma(values, 10)[9]) and np.isfinite(smoothing.lwma(values, 10)[10])
    assert np.isfinite(smoothing.jjma(values, 5, 0)[30]) and np.isnan(smoothing.jjma(values, 5, 0)[29])


def test_parma_fits_a_parabola_exactly():
    x = np.arange(50.0)
    values = 0.5 * x * x - 3 * x + 7
    np.testing.assert_allclose(smoothing.parma(values, 9)[8:], values[8:], rtol=1e-9)


def test_jjma_tracks_a_trend():
    values = np.linspace(1.0, 2.0, 400)
    out = smoothing.jjma(values, 7, 0)
    assert abs(out[-1] - values[-1]) < 0.01


# ------------------------------------------------------- chart mechanics


class Timed(Indicator):
    name = "Timed"
    pane = Pane.PRICE
    plots = [Plot("v", known_at="known", expires_at="expires", style=DrawStyle.ARROW)]

    def calculate(self, df):
        n = len(df)
        v = np.full(n, 1.0)
        known = np.arange(n) + 2.0          # known two bars late
        expires = np.arange(n) + 5.0        # current for five bars
        return {"v": v, "known": known, "expires": expires}


def test_known_at_and_expires_at_window_each_value(qapp):
    import pyqtgraph as pg

    plot_item = pg.PlotItem()
    layer = IndicatorLayer(plot_item)
    indicator = Timed()
    layer.set_plots(indicator.plots, indicator.calculate(DF.iloc[:20]))
    layer.set_visible_length(10)                 # bars 0..9 revealed
    _x, y = layer._clipped("v", "known", "expires")
    shown = np.nonzero(np.isfinite(y))[0]
    # known (j+2) < 10 → j ≤ 7; current (j+5 ≥ 9) → j ≥ 4
    assert shown.tolist() == [4, 5, 6, 7]


def test_zigzag_points_order_a_bar_with_both_extremes():
    highs = np.array([np.nan, 2.0, np.nan, 3.0])
    lows = np.array([1.0, np.nan, np.nan, 0.5])
    x, y = zigzag_points(highs, lows)
    # after the high at bar 1, bar 3 goes to its low first, then its high
    assert x.tolist() == [0, 1, 3, 3]
    assert y.tolist() == [1.0, 2.0, 0.5, 3.0]


def test_indicator_candles_tolerate_a_warm_up(qapp):
    from backtester.ui.chart.chart_widget import ChartWidget

    chart = ChartWidget()
    chart.set_data(DF.iloc[:300])
    cls, _spec = REGISTRY["Heiken Ashi Smoothed"]
    assert chart.set_indicators([cls()]) == []
    chart.reveal_to(100)
    chart.reveal_all()
