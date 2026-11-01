"""The MQL5 include ports (``backtester/indicators/mql5_include``): each
module imports, the numeric libraries match independent references, and the
two indicators that ship inside the ``MQL5 Include`` folder compute without
leaking the future."""

import importlib
import pkgutil
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from backtester.indicators import loader, smoothing
from backtester.indicators.mql5_include import (
    dt_fft,
    inc_on_ring_buffer as rb,
    moving_averages as ma,
    smooth_algorithms as sa,
    bpnn,
)
from backtester.indicators.mql5_include.mql_runtime import EMPTY_VALUE, fdiv, idiv, imod

import backtester.indicators.mql5_include as pkg

ROOT = Path(__file__).resolve().parents[1]
RNG = np.random.default_rng(7)
PRICE = 100 + RNG.standard_normal(600).cumsum()


def forex_df(n: int = 800, seed: int = 3) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    close = 1.10 + rng.normal(0, 0.0006, n).cumsum() + 0.004 * np.sin(np.arange(n) / 40)
    open_ = np.r_[close[0], close[:-1]]
    high = np.maximum(open_, close) + rng.uniform(0, 0.0008, n)
    low = np.minimum(open_, close) - rng.uniform(0, 0.0008, n)
    return pd.DataFrame({
        "time": pd.date_range("2024-01-01", periods=n, freq="15min"),
        "open": open_.round(5), "high": high.round(5), "low": low.round(5),
        "close": close.round(5), "tick_volume": rng.integers(50, 500, n),
        "spread": 10, "real_volume": 0,
    })


# ------------------------------------------------------------ every module

OPTIONAL = {"swisseph": "swisseph"}       # module -> third-party package it wraps


@pytest.mark.parametrize("name", sorted(m.name for m in pkgutil.iter_modules(pkg.__path__)))
def test_module_imports(name):
    if name in OPTIONAL:
        pytest.importorskip(OPTIONAL[name])
    importlib.import_module(f"{pkg.__name__}.{name}")


# ------------------------------------------------------------ MQL semantics

def test_c_integer_division_and_float_division():
    assert idiv(-7, 2) == -3 and imod(-7, 2) == -1        # C truncation, not floor
    assert fdiv(1, 0) == np.inf and np.isnan(fdiv(0, 0))
    assert EMPTY_VALUE == np.finfo(float).max


# ------------------------------------------------------------ MovingAverages.mqh

def test_moving_averages_on_buffer_match_pandas():
    n, per, beg = len(PRICE), 14, 3
    s = pd.Series(PRICE)
    w = np.arange(1, per + 1)
    lwma = s.rolling(per).apply(lambda x: (x * w).sum() / w.sum(), raw=True).to_numpy()
    first = beg + per - 1

    b = np.zeros(n)
    assert ma.SimpleMAOnBuffer(n, 0, beg, per, PRICE, b) == n
    np.testing.assert_allclose(b[first:], s.rolling(per).mean().to_numpy()[first:], atol=1e-9)
    assert (b[:first] == 0).all()                         # warm-up is 0.0, as in MT5

    b = np.zeros(n)
    ma.ExponentialMAOnBuffer(n, 0, beg, per, PRICE, b)
    np.testing.assert_allclose(b[beg:], s.iloc[beg:].ewm(span=per, adjust=False).mean(), atol=1e-9)

    b = np.zeros(n)
    ma.LinearWeightedMAOnBuffer(n, 0, beg, per, PRICE, b)
    np.testing.assert_allclose(b[first:], lwma[first:], atol=1e-9)

    b = np.zeros(n)
    rt, wsum = ma.LinearWeightedMAOnBuffer(n, 0, beg, per, PRICE, b, 0)
    assert rt == n and wsum == per * (per + 1) // 2
    np.testing.assert_allclose(b[first:], lwma[first:], atol=1e-9)

    b = np.zeros(n)
    ma.SmoothedMAOnBuffer(n, 0, 0, per, PRICE, b)
    assert b[per - 1] == pytest.approx(PRICE[:per].mean())
    assert b[per] == pytest.approx((b[per - 1] * (per - 1) + PRICE[per]) / per)

    assert ma.SimpleMAOnBuffer(n, 0, 0, 1, PRICE, np.zeros(n)) == 0     # period 1 → 0


def test_moving_averages_incremental_equals_full():
    n, per = len(PRICE), 10
    full = np.zeros(n)
    ma.SmoothedMAOnBuffer(n, 0, 0, per, PRICE, full)
    part = np.zeros(n)
    ma.SmoothedMAOnBuffer(n - 5, 0, 0, per, PRICE[:n - 5], part[:n - 5])
    ma.SmoothedMAOnBuffer(n, n - 5, 0, per, PRICE, part)
    np.testing.assert_array_equal(part, full)


def test_moving_averages_point_functions():
    assert ma.SimpleMA(13, 14, PRICE) == pytest.approx(PRICE[:14].mean())
    assert ma.SimpleMA(12, 14, PRICE) == 0.0
    w = np.arange(1, 15)
    assert ma.LinearWeightedMA(30, 14, PRICE) == pytest.approx((PRICE[17:31] * w).sum() / w.sum())


# ------------------------------------------------------------ SmoothAlgorithms.mqh

@pytest.mark.parametrize("method,name,length,phase", [
    (sa.MODE_SMA_, "sma", 12, 0), (sa.MODE_EMA_, "ema", 12, 0), (sa.MODE_SMMA_, "smma", 12, 0),
    (sa.MODE_LWMA_, "lwma", 12, 0), (sa.MODE_JJMA, "jjma", 7, 30), (sa.MODE_JurX, "jurx", 9, 0),
    (sa.MODE_ParMA, "parma", 9, 0), (sa.MODE_T3, "t3", 6, 70), (sa.MODE_VIDYA, "vidya", 9, 12),
    (sa.MODE_AMA, "ama", 9, 30),
])
def test_smooth_algorithms_match_vectorised_smoothing(method, name, length, phase):
    got = sa.xma_series(PRICE, method, length, phase)
    ref = smoothing.xma(PRICE, name, length, phase)
    both = ~np.isnan(got) & ~np.isnan(ref)
    assert both.sum() > len(PRICE) - 120
    np.testing.assert_allclose(got[both], ref[both], rtol=1e-9, atol=1e-8)


# ------------------------------------------------------------ IncOnRingBuffer

def test_ring_buffer_sma_matches_pandas():
    m = rb.CMAOnRingBuffer()
    m.Init(14, rb.MODE_SMA, 64)
    vals = [m.MainOnValue(len(PRICE), 0, 0, v, i) for i, v in enumerate(PRICE)]
    ref = pd.Series(PRICE).rolling(14).mean().to_numpy()
    got = np.where(np.array(vals) == EMPTY_VALUE, np.nan, vals)
    ok = ~np.isnan(ref) & ~np.isnan(got)
    assert ok.sum() > 500
    np.testing.assert_allclose(got[ok], ref[ok], atol=1e-9)


# ------------------------------------------------------------ dt_fft.mqh

def test_real_fft_matches_numpy():
    n = 64
    x = RNG.standard_normal(n)
    a = x.tolist()
    dt_fft.realfastfouriertransform(a, n, False)
    f = np.fft.rfft(x)
    # ALGLIB packing: a[0]=Re0, a[1]=Re(n/2), then (Re, Im) pairs with Im sign as ALGLIB's e^{+i}
    assert a[0] == pytest.approx(f[0].real)
    assert a[1] == pytest.approx(f[n // 2].real)
    np.testing.assert_allclose(a[2::2], f[1:n // 2].real, atol=1e-9)
    np.testing.assert_allclose(np.abs(a[3::2]), np.abs(f[1:n // 2].imag), atol=1e-9)
    dt_fft.realfastfouriertransform(a, n, True)
    np.testing.assert_allclose(a, x, atol=1e-9)


# ------------------------------------------------------------ BPNN

def test_bpnn_learns_xor():
    inp = [0, 0, 0, 1, 1, 0, 1, 1]
    tgt = [0, 1, 1, 0]
    out, wt = [], []
    bpnn.Train(inp, tgt, out, 4, 0, [], wt, 3, [2, 4, 1], 0, 1, 5000, 0.001, seed=1)
    assert [round(v) for v in out[:4]] == tgt


# ------------------------------------------------------------ the two .mq5 in Include

INCLUDE_INDICATORS = ["x2ma_osc.py", "hl_cross_sig_for_wpr.py"]


@pytest.mark.parametrize("filename", INCLUDE_INDICATORS)
def test_include_indicator_is_causal(filename):
    classes = loader.load_indicators_from_file(ROOT / "python_indicators" / filename)
    assert len(classes) == 1
    (cls,) = classes.values()
    df = forex_df()
    full = cls().calculate(df)
    for plot in cls.plots:
        assert len(full[plot.key]) == len(df)
    assert any(np.isfinite(v).any() for v in full.values())
    k = 600
    part = cls().calculate(df.iloc[:k].reset_index(drop=True))
    for key, arr in part.items():
        np.testing.assert_allclose(arr, full[key][:k], equal_nan=True, err_msg=key)
