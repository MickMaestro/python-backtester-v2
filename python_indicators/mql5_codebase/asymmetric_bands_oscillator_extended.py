"""Asymmetric bands oscillator (extended) — converted from MQL5: MQL5 Indicators/Asymmetric bands oscillator - extended/Asymmetric bands oscillator (extended).mq5

Asymmetric bands oscillator
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 12, 'indicator_plots': 6}, 'types': {1: 7, 2: 7, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [15461375], 2: [15466475], 3: [7451452], 4: [11119017], 5: [17919], 6: [11119017]}, 'widths': {4: 2}, 'styles': {}, 'labels': {1: 'Bear fill', 2: 'Bull fill', 3: 'Band up', 4: 'Average', 5: 'Band down', 6: 'Price'}, 'levels': [], 'description': ['Asymmetric bands oscillator'], 'name': 'Asymmetric bands oscillator (extended)', 'source': 'MQL5 Indicators/Asymmetric bands oscillator - extended/Asymmetric bands oscillator (extended).mq5', 'folder': 'Asymmetric bands oscillator - extended', 'inputs': [{'mql': 'inpBandPeriod', 'py': 'inpBandPeriod', 'param': 'inpBandPeriod', 'type': 'int', 'default': 14, 'label': 'Bands period', 'sinput': False}, {'mql': 'inpBandPrice', 'py': 'inpBandPrice', 'param': 'inpBandPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpBandMethod', 'py': 'inpBandMethod', 'param': 'inpBandMethod', 'type': 'int', 'default': 0, 'label': 'Bands average method', 'sinput': False}, {'mql': 'inpSmooth', 'py': 'inpSmooth', 'param': 'inpSmooth', 'type': 'int', 'default': 3, 'label': 'Smooth period', 'sinput': False}, {'mql': 'inpBandDeviations', 'py': 'inpBandDeviations', 'param': 'inpBandDeviations', 'type': 'double', 'default': 2.0, 'label': 'Bands deviation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpBandPeriod = _input('inpBandPeriod', 14)  # Bands period
inpBandPrice = _input('inpBandPrice', PRICE_CLOSE)  # Price
inpBandMethod = _input('inpBandMethod', MODE_SMA)  # Bands average method
inpSmooth = _input('inpSmooth', 3)  # Smooth period
inpBandDeviations = _input('inpBandDeviations', 2.0)  # Bands deviation
price = Arr(0, 0.0)
valu = Arr(0, 0.0)
vald = Arr(0, 0.0)
vala = Arr(0, 0.0)
wu = Arr(0, 0.0)
wd = Arr(0, 0.0)
avg = Arr(0, 0.0)
filluu = Arr(0, 0.0)
fillud = Arr(0, 0.0)
filldu = Arr(0, 0.0)
filldd = Arr(0, 0.0)
ema = Arr(0, 0.0)
_alpha = 0.0
_maHandle = 0

def OnInit():
    global _alpha, _maHandle
    SetIndexBuffer(0, filluu, INDICATOR_DATA)
    SetIndexBuffer(1, fillud, INDICATOR_DATA)
    SetIndexBuffer(2, filldu, INDICATOR_DATA)
    SetIndexBuffer(3, filldd, INDICATOR_DATA)
    SetIndexBuffer(4, valu, INDICATOR_DATA)
    SetIndexBuffer(5, vala, INDICATOR_DATA)
    SetIndexBuffer(6, vald, INDICATOR_DATA)
    SetIndexBuffer(7, price, INDICATOR_DATA)
    SetIndexBuffer(8, wu, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, wd, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, avg, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, ema, INDICATOR_CALCULATIONS)
    _maHandle = iMA(Symbol(), 0, inpBandPeriod, 0, inpBandMethod, inpBandPrice)
    if _maHandle == INVALID_HANDLE:
        return INIT_FAILED
    _alpha = _fdiv(2.0, 1.0 + (inpSmooth if (inpSmooth > 1) else 1.0))
    IndicatorSetString(INDICATOR_SHORTNAME, 'Asymmetric ' + StringSubstr(EnumToString(inpBandMethod, 'ENUM_MA_METHOD'), 5) + ' bands (' + _str(inpBandPeriod) + ',' + _str(inpSmooth) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(_maHandle, 0, 0, _copyCount, avg) != _copyCount:
        return prev_calculated
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        _price = getPrice(inpBandPrice, open, close, high, low, i)
        if avg[i] == EMPTY_VALUE:
            avg[i] = _price
        diff = _price - avg[i]
        if i < 1:
            wd[i] = 0.0
            wu[i] = wd[i]
        elif diff > 0:
            wu[i] = ((wu[i - 1] * (inpBandPeriod - 1)) + (diff * diff)) / inpBandPeriod
            wd[i] = (wd[i - 1] * (inpBandPeriod - 1)) / inpBandPeriod
        else:
            wd[i] = ((wd[i - 1] * (inpBandPeriod - 1)) + (diff * diff)) / inpBandPeriod
            wu[i] = (wu[i - 1] * (inpBandPeriod - 1)) / inpBandPeriod
        highBand = avg[i] + (inpBandDeviations * MathSqrt(wu[i]))
        lowBand = avg[i] - (inpBandDeviations * MathSqrt(wd[i]))
        range_ = highBand - lowBand
        filldu[i] = ((1.0 - _fdiv(2.0 * (avg[i] - lowBand), range_)) if (range_ != 0) else 0)
        fillud[i] = filldu[i]
        vala[i] = fillud[i]
        filluu[i] = 1.0
        valu[i] = filluu[i]
        filldd[i] = -1.0
        vald[i] = filldd[i]
        ema[i] = ((ema[i - 1] + (_alpha * (_price - avg[i] - ema[i - 1]))) if (i > 0) else _price)
        price[i] = (_fdiv(ema[i], range_) if (range_ != 0) else 0)
        i += 1
    return i

def getPrice(tprice, open, close, high, low, i):
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


class AsymmetricBandsOscillatorExtended(_MQL5Indicator):
    name = 'Asymmetric bands oscillator (extended)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpBandPeriod': 14,  # Bands period
        'inpBandPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpBandMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Bands average method
        'inpSmooth': 3,  # Smooth period
        'inpBandDeviations': 2.0,  # Bands deviation
    }

