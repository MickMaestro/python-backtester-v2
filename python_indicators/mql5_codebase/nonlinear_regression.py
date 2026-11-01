"""Nonlinear regression — converted from MQL5: MQL5 Indicators/Nonlinear regression/Nonlinear regression.mq5

Nonlinear regression
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 9639167, 3329330]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Nonlinear regression'}, 'levels': [], 'description': ['Nonlinear regression'], 'name': 'Nonlinear regression', 'source': 'MQL5 Indicators/Nonlinear regression/Nonlinear regression.mq5', 'folder': 'Nonlinear regression', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 50, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 50)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
workNlr = Arr(0, 0.0, dims=(1,))
nlrYValue = Arr(0, 0.0)
nlrXValue = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Nonlinear regression (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        val[i] = iNlr(getPrice(inpPrice, open, close, high, low, i, rates_total), inpPeriod, i, 0, rates_total)
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
    return rates_total

def iNlr(price, Length, shift, desiredBar, bars, instanceNo=0):
    if ArrayRange(workNlr, 0) != bars:
        ArrayResize(workNlr, bars)
    if ArraySize(nlrYValue) != Length:
        ArrayResize(nlrYValue, Length)
    if ArraySize(nlrXValue) != Length:
        ArrayResize(nlrXValue, Length)
    AvgX = 0.0
    AvgY = 0.0
    r = shift
    workNlr[r][instanceNo] = price
    ArrayInitialize(nlrXValue, 0)
    ArrayInitialize(nlrYValue, 0)
    i = 0
    while i < Length and (r - i) >= 0:
        nlrXValue[i] = i
        nlrYValue[i] = workNlr[r - i][instanceNo]
        AvgX += nlrXValue[i]
        AvgY += nlrYValue[i]
        i += 1
    AvgX = _fdiv(AvgX, Length)
    AvgY = _fdiv(AvgY, Length)
    SXX = 0.0
    SXY = 0.0
    SYY = 0.0
    SXX2 = 0.0
    SX2X2 = 0.0
    SYX2 = 0.0
    for i in range(0, Length):
        XM = nlrXValue[i] - AvgX
        YM = nlrYValue[i] - AvgY
        XM2 = (nlrXValue[i] * nlrXValue[i]) - (AvgX * AvgX)
        SXX += XM * XM
        SXY += XM * YM
        SYY += YM * YM
        SXX2 += XM * XM2
        SX2X2 += XM2 * XM2
        SYX2 += YM * XM2
    tmp = 0.0
    ACoeff = 0.0
    BCoeff = 0.0
    CCoeff = 0.0
    tmp = (SXX * SX2X2) - (SXX2 * SXX2)
    if tmp != 0:
        BCoeff = _fdiv((SXY * SX2X2) - (SYX2 * SXX2), tmp)
        CCoeff = _fdiv((SXX * SYX2) - (SXX2 * SXY), tmp)
    ACoeff = AvgY - (BCoeff * AvgX) - (CCoeff * AvgX * AvgX)
    tmp = ACoeff + (BCoeff * desiredBar) + (CCoeff * desiredBar * desiredBar)
    return tmp

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


class NonlinearRegression(_MQL5Indicator):
    name = 'Nonlinear regression'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 50,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

