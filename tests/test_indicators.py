import numpy as np
import pytest

from backtester.strategy import indicators as ind


def test_sma_values_and_warmup():
    values = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    out = ind.sma(values, 3)
    assert np.isnan(out[:2]).all()
    assert out[2] == pytest.approx(2.0)
    assert out[4] == pytest.approx(4.0)


def test_ema_constant_series_is_constant():
    out = ind.ema(np.full(50, 5.0), 10)
    assert np.isnan(out[:9]).all()
    assert out[9:] == pytest.approx(5.0)


def test_rsi_extremes():
    rising = np.arange(1, 40, dtype=float)
    falling = rising[::-1].copy()
    assert ind.rsi(rising, 14)[-1] == pytest.approx(100.0)
    assert ind.rsi(falling, 14)[-1] == pytest.approx(0.0)
    assert np.isnan(ind.rsi(rising, 14)[:14]).all()


def test_atr_constant_range():
    n = 60
    close = np.full(n, 1.1000)
    high = np.full(n, 1.1010)
    low = np.full(n, 1.0990)
    out = ind.atr(high, low, close, 14)
    assert out[-1] == pytest.approx(0.0020, abs=1e-6)


def test_highest_lowest():
    values = np.array([1.0, 3.0, 2.0, 5.0, 4.0])
    assert ind.highest(values, 3)[3] == pytest.approx(5.0)
    assert ind.lowest(values, 3)[4] == pytest.approx(2.0)
