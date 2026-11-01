"""Instantaneous Trend Line bands (general) — converted from MQL5: MQL5 Indicators/Instantaneous Trend Line bands (generalized)/Instantaneous Trend Line bands (general).mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [9639167, 3329330], 2: [11119017], 3: [11119017]}, 'widths': {2: 2, 3: 1}, 'styles': {}, 'labels': {1: 'Filling', 2: 'Instantaneous trend line', 3: 'Signal line'}, 'levels': [], 'description': [], 'name': 'Instantaneous Trend Line bands (general)', 'source': 'MQL5 Indicators/Instantaneous Trend Line bands (generalized)/Instantaneous Trend Line bands (general).mq5', 'folder': 'Instantaneous Trend Line bands (generalized)', 'inputs': [{'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}, {'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'double', 'default': 27.0, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPrice = _input('inpPrice', PRICE_MEDIAN)  # Price
inpPeriod = _input('inpPeriod', 27.0)  # Period
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
itrend = Arr(0, 0.0)
signal = Arr(0, 0.0)
prices = Arr(0, 0.0)
smooth = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, itrend, INDICATOR_DATA)
    SetIndexBuffer(3, signal, INDICATOR_DATA)
    SetIndexBuffer(4, prices, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, smooth, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Instantaneous trend line bands(' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    alpha = 2 / (1 + inpPeriod)
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        prices[i] = getPrice(inpPrice, open, close, high, low, i, rates_total)
        smooth[i] = (((prices[i] + (2 * prices[i - 1]) + (2 * prices[i - 2]) + prices[i - 3]) / 6) if (i > 2) else prices[i])
        itrend[i] = ((((alpha - ((alpha * alpha) / 4)) * smooth[i]) + (0.5 * alpha * alpha * smooth[i - 1]) - ((alpha - (0.75 * alpha * alpha)) * smooth[i - 2]) + (2 * (1 - alpha) * itrend[i - 1]) - ((1 - alpha) * (1 - alpha) * itrend[i - 2])) if (i > 1) else itrend[i])
        signal[i] = (((2 * itrend[i]) - itrend[i - 2]) if (i > 1) else itrend[i])
        fillu[i] = itrend[i]
        filld[i] = signal[i]
    return rates_total

def getPrice(tprice, open, close, high, low, i, _bars):
    if i >= 0:
        _sw1 = tprice
        if _sw1 == PRICE_CLOSE:
            return close[i]
        elif _sw1 == PRICE_OPEN:
            return open[i]
        elif _sw1 == PRICE_HIGH:
            return high[i]
        elif _sw1 == PRICE_LOW:
            return low[i]
        elif _sw1 == PRICE_MEDIAN:
            return (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            return (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class InstantaneousTrendLineBandsGeneral(_MQL5Indicator):
    name = 'Instantaneous Trend Line bands (general)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
        'inpPeriod': 27.0,  # Period
    }

