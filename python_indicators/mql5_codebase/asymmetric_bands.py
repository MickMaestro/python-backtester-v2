"""Asymmetric bands — converted from MQL5: MQL5 Indicators/Asymmetric bands/Asymmetric bands.mq5

Asymmetric bands
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [3329330], 2: [11119017], 3: [17919]}, 'widths': {}, 'styles': {2: 2}, 'labels': {1: 'Band up', 2: 'Average', 3: 'Band down'}, 'levels': [], 'description': ['Asymmetric bands'], 'name': 'Asymmetric bands', 'source': 'MQL5 Indicators/Asymmetric bands/Asymmetric bands.mq5', 'folder': 'Asymmetric bands', 'inputs': [{'mql': 'inpBandPeriod', 'py': 'inpBandPeriod', 'param': 'inpBandPeriod', 'type': 'int', 'default': 14, 'label': 'Bands period', 'sinput': False}, {'mql': 'inpBandPrice', 'py': 'inpBandPrice', 'param': 'inpBandPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpBandMethod', 'py': 'inpBandMethod', 'param': 'inpBandMethod', 'type': 'int', 'default': 0, 'label': 'Bands average method', 'sinput': False}, {'mql': 'inpBandDeviations', 'py': 'inpBandDeviations', 'param': 'inpBandDeviations', 'type': 'double', 'default': 2.0, 'label': 'Bands deviation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpBandPeriod = _input('inpBandPeriod', 14)  # Bands period
inpBandPrice = _input('inpBandPrice', PRICE_CLOSE)  # Price
inpBandMethod = _input('inpBandMethod', MODE_SMA)  # Bands average method
inpBandDeviations = _input('inpBandDeviations', 2.0)  # Bands deviation
valu = Arr(0, 0.0)
vald = Arr(0, 0.0)
vala = Arr(0, 0.0)
wu = Arr(0, 0.0)
wd = Arr(0, 0.0)
_maHandle = 0
_avgVal = Arr(1, 0.0, dyn=False)

def OnInit():
    global _maHandle
    SetIndexBuffer(0, valu, INDICATOR_DATA)
    SetIndexBuffer(1, vala, INDICATOR_DATA)
    SetIndexBuffer(2, vald, INDICATOR_DATA)
    SetIndexBuffer(3, wu, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, wd, INDICATOR_CALCULATIONS)
    _maHandle = iMA(Symbol(), 0, inpBandPeriod, 0, inpBandMethod, inpBandPrice)
    if _maHandle == INVALID_HANDLE:
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Asymmetric bands (' + _str(inpBandPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if BarsCalculated(_maHandle) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        price = getPrice(inpBandPrice, open, close, high, low, i, rates_total)
        _avgCopied = CopyBuffer(_maHandle, 0, _DT(time[i]), 1, _avgVal)
        vala[i] = (_avgVal[0] if (_avgCopied == 1) else 0)
        diff = price - vala[i]
        if diff > 0:
            wu[i] = ((((wu[i - 1] * (inpBandPeriod - 1)) + (diff * diff)) / inpBandPeriod) if (i > inpBandPeriod) else 0)
            wd[i] = (((wd[i - 1] * (inpBandPeriod - 1)) / inpBandPeriod) if (i > inpBandPeriod) else 0)
        else:
            wd[i] = ((((wd[i - 1] * (inpBandPeriod - 1)) + (diff * diff)) / inpBandPeriod) if (i > inpBandPeriod) else 0)
            wu[i] = (((wu[i - 1] * (inpBandPeriod - 1)) / inpBandPeriod) if (i > inpBandPeriod) else 0)
        valu[i] = vala[i] + (inpBandDeviations * MathSqrt(wu[i]))
        vald[i] = vala[i] - (inpBandDeviations * MathSqrt(wd[i]))
        i += 1
    return i

def getPrice(tprice, open, close, high, low, i, _bars):
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


class AsymmetricBands(_MQL5Indicator):
    name = 'Asymmetric bands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpBandPeriod': 14,  # Bands period
        'inpBandPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpBandMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Bands average method
        'inpBandDeviations': 2.0,  # Bands deviation
    }

