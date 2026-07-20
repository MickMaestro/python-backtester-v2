import numpy as np
import pandas as pd
import pytest

from backtester.strategy import indicators as ind
from backtester.strategy.indicators import AppliedPrice, IndicatorFactory, price_series


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


def _ohlc_df():
    return pd.DataFrame(
        {
            "open": [10.0, 11.0],
            "high": [12.0, 14.0],
            "low": [8.0, 10.0],
            "close": [11.0, 13.0],
        }
    )


def test_price_series_applied_prices():
    df = _ohlc_df()
    assert price_series(df, AppliedPrice.CLOSE).tolist() == [11.0, 13.0]
    assert price_series(df, AppliedPrice.OPEN).tolist() == [10.0, 11.0]
    # Median (H+L)/2, Typical (H+L+C)/3, Weighted (H+L+2C)/4
    assert price_series(df, AppliedPrice.MEDIAN).tolist() == [10.0, 12.0]
    assert price_series(df, AppliedPrice.TYPICAL)[0] == pytest.approx((12 + 8 + 11) / 3)
    assert price_series(df, AppliedPrice.WEIGHTED)[1] == pytest.approx((14 + 10 + 2 * 13) / 4)
    # string value accepted too
    assert price_series(df, "median").tolist() == [10.0, 12.0]


def test_factory_applied_price_changes_result():
    df = _ohlc_df()
    factory = IndicatorFactory(df)
    on_close = factory.sma(2, applied=AppliedPrice.CLOSE)
    on_typical = factory.sma(2, applied=AppliedPrice.TYPICAL)
    assert on_close[1] == pytest.approx((11 + 13) / 2)
    assert on_typical[1] != pytest.approx(on_close[1])
    # back-compat: a raw column name still works
    assert factory.sma(2, applied="close")[1] == pytest.approx(on_close[1])


def test_applied_price_labels_cover_enum():
    for applied in AppliedPrice:
        assert applied.label  # every member has a display label
        assert applied.short
