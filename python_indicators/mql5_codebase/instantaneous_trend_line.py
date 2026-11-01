"""Instantaneous Trend Line — converted from MQL5: MQL5 Indicators/Instantaneous Trend Line/Instantaneous Trend Line.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [9639167, 3329330]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Instantaneous trend line'}, 'levels': [], 'description': [], 'name': 'Instantaneous Trend Line', 'source': 'MQL5 Indicators/Instantaneous Trend Line/Instantaneous Trend Line.mq5', 'folder': 'Instantaneous Trend Line', 'inputs': [{'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}, {'mql': 'inpAlpha', 'py': 'inpAlpha', 'param': 'inpAlpha', 'type': 'double', 'default': 0.07, 'label': 'Alpha', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPrice = _input('inpPrice', PRICE_MEDIAN)  # Price
inpAlpha = _input('inpAlpha', 0.07)  # Alpha
itrend = Arr(0, 0.0)
itrendc = Arr(0, 0.0)
prices = Arr(0, 0.0)
smooth = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, itrend, INDICATOR_DATA)
    SetIndexBuffer(1, itrendc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, prices, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, smooth, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Instantaneous trend line (' + _str(inpAlpha) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        prices[i] = getPrice(inpPrice, open, close, high, low, i, rates_total)
        smooth[i] = (((prices[i] + (2 * prices[i - 1]) + (2 * prices[i - 2]) + prices[i - 3]) / 6) if (i > 2) else prices[i])
        itrend[i] = ((((inpAlpha - ((inpAlpha * inpAlpha) / 4)) * smooth[i]) + (0.5 * inpAlpha * inpAlpha * smooth[i - 1]) - ((inpAlpha - (0.75 * inpAlpha * inpAlpha)) * smooth[i - 2]) + (2 * (1 - inpAlpha) * itrend[i - 1]) - ((1 - inpAlpha) * (1 - inpAlpha) * itrend[i - 2])) if (i > 1) else itrend[i])
        itrendc[i] = ((1 if (itrend[i] > itrend[i - 1]) else 0) if (i > 1) else 0)
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


class InstantaneousTrendLine(_MQL5Indicator):
    name = 'Instantaneous Trend Line'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
        'inpAlpha': 0.07,  # Alpha
    }

