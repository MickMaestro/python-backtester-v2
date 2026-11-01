"""PriceSpeed — converted from MQL5: MQL5 Indicators/PriceSpeed/PriceSpeed.mq5

Calculates average and peak (efficient) speed of price in true and false directions, shows standard deviation for specified period. All values are in points per minute.\\n
Inspired by Average Speed indicator (https://www.mql5.com/en/code/1544) by Totom Sukopratomo, but thoroughly reworked and improved.
Copyright: Copyright (c) 2019, Marketeer; Link: https://www.mql5.com/en/users/marketeer; Version: 3.1

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright (c) 2019, Marketeer', 'link': 'https://www.mql5.com/en/users/marketeer', 'version': '3.1', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 5}, 'types': {1: 3, 2: 3, 3: 3, 4: 1, 5: 1}, 'colors': {1: [32768], 2: [42495], 3: [255], 4: [8421504], 5: [8421504]}, 'widths': {1: 3, 2: 1, 3: 1, 4: 1, 5: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 2, 5: 2}, 'labels': {1: 'Average Speed', 2: 'Peak True Speed', 3: 'Peak False Speed', 4: 'Peak Deviation Up', 5: 'Peak Deviation Dn'}, 'levels': [], 'description': ['Calculates average and peak (efficient) speed of price in true and false directions, shows standard deviation for specified period. All values are in points per minute.\\n', 'Inspired by Average Speed indicator (https://www.mql5.com/en/code/1544) by Totom Sukopratomo, but thoroughly reworked and improved.'], 'name': 'PriceSpeed', 'source': 'MQL5 Indicators/PriceSpeed/PriceSpeed.mq5', 'folder': 'PriceSpeed', 'inputs': [{'mql': 'n', 'py': 'n', 'param': 'n', 'type': 'int', 'default': 3, 'label': 'Averaging Bars', 'sinput': False}, {'mql': 'price', 'py': 'price', 'param': 'price', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'm', 'py': 'm', 'param': 'm', 'type': 'int', 'default': 5, 'label': 'Peak Deviation Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
n = _input('n', 3)  # Averaging Bars
price = _input('price', PRICE_CLOSE)  # Price
m = _input('m', 5)  # Peak Deviation Period
OutputBuffer1 = Arr(0, 0.0)
OutputBuffer2 = Arr(0, 0.0)
OutputBuffer3 = Arr(0, 0.0)
SmoothBuffer = Arr(0, 0.0)
SmoothMirror = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, OutputBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, OutputBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, OutputBuffer3, INDICATOR_DATA)
    SetIndexBuffer(3, SmoothBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, SmoothMirror, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'PriceSpeed(' + _str(n) + ',' + _str(m) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = 0
    if prev_calculated == 0:
        limit = n
    else:
        limit = prev_calculated - 1
    for i in range(limit, rates_total):
        v = 0.0
        d = 0.0
        f = 0.0
        t = GetMinute()
        sumv = 0.0
        sumw = 0.0
        sumf = 0.0
        j = i - n + 1
        while j <= i and j < rates_total:
            d = _fdiv(close[j] - close[j - 1], Point())
            if d > 0:
                d = _fdiv(high[j] - low[j], Point())
                f = _fdiv(MathMin(low[j] - open[j], close[j] - high[j]), Point())
            else:
                d = _fdiv(low[j] - high[j], Point())
                f = _fdiv(MathMax(high[j] - open[j], close[j] - low[j]), Point())
            sumw += _fdiv(d, t)
            sumf += _fdiv(f, t)
            _sw1 = price
            if _sw1 == PRICE_CLOSE:
                d = _fdiv(close[j] - close[j - 1], Point())
            elif _sw1 == PRICE_HIGH:
                d = _fdiv(high[j] - high[j - 1], Point())
            elif _sw1 == PRICE_LOW:
                d = _fdiv(low[j] - low[j - 1], Point())
            elif _sw1 == PRICE_MEDIAN:
                d = _fdiv(((high[j] + low[j]) / 2) - ((high[j - 1] + low[j - 1]) / 2), Point())
            elif _sw1 == PRICE_OPEN:
                d = _fdiv(open[j] - open[j - 1], Point())
            elif _sw1 == PRICE_TYPICAL:
                d = _fdiv(((high[j] + low[j] + close[j]) / 3) - ((high[j - 1] + low[j - 1] + close[j - 1]) / 3), Point())
            elif _sw1 == PRICE_WEIGHTED:
                d = _fdiv(((high[j] + low[j] + close[j] + close[j]) / 4) - ((high[j - 1] + low[j - 1] + close[j - 1] + close[j - 1]) / 4), Point())
            v = _fdiv(d, t)
            sumv += v
            j += 1
        OutputBuffer1[i] = sumv / n
        OutputBuffer2[i] = sumw / n
        OutputBuffer3[i] = sumf / n
    N = MathMax(1, m - 1)
    for i in range(limit, rates_total):
        SmoothBuffer[i] = 0.0
        j = i - m + 1
        while (j >= 0 and j <= i) and j < rates_total:
            SmoothBuffer[i] += OutputBuffer2[j] * OutputBuffer2[j]
            j += 1
        SmoothBuffer[i] = sqrt(_fdiv(SmoothBuffer[i], N))
        SmoothMirror[i] = -SmoothBuffer[i]
    return rates_total

def GetMinute():
    return _idiv(PeriodSeconds(Period()), 60)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PriceSpeed(_MQL5Indicator):
    name = 'PriceSpeed'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'n': 3,  # Averaging Bars
        'price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'm': 5,  # Peak Deviation Period
    }

