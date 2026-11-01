"""Kirshenbaum bands — converted from MQL5: MQL5 Indicators/Kirshenbaum bands/Kirshenbaum bands.mq5

Kirshenbaum Bands
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [7451452], 2: [11119017], 3: [17919]}, 'widths': {}, 'styles': {2: 2}, 'labels': {1: 'Band up', 2: 'Average', 3: 'Band down'}, 'levels': [], 'description': ['Kirshenbaum Bands'], 'name': 'Kirshenbaum bands', 'source': 'MQL5 Indicators/Kirshenbaum bands/Kirshenbaum bands.mq5', 'folder': 'Kirshenbaum bands', 'inputs': [{'mql': 'inpBandPeriod', 'py': 'inpBandPeriod', 'param': 'inpBandPeriod', 'type': 'int', 'default': 21, 'label': 'Bands period', 'sinput': False}, {'mql': 'inpBandPrice', 'py': 'inpBandPrice', 'param': 'inpBandPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpBandMethod', 'py': 'inpBandMethod', 'param': 'inpBandMethod', 'type': 'int', 'default': 1, 'label': 'Bands average method', 'sinput': False}, {'mql': 'inpBandDeviations', 'py': 'inpBandDeviations', 'param': 'inpBandDeviations', 'type': 'double', 'default': 2.0, 'label': 'Bands deviation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpBandPeriod = _input('inpBandPeriod', 21)  # Bands period
inpBandPrice = _input('inpBandPrice', PRICE_CLOSE)  # Price
inpBandMethod = _input('inpBandMethod', MODE_EMA)  # Bands average method
inpBandDeviations = _input('inpBandDeviations', 2.0)  # Bands deviation
valu = Arr(0, 0.0)
vald = Arr(0, 0.0)
vala = Arr(0, 0.0)
_maHandle = 0

def OnInit():
    global _maHandle
    SetIndexBuffer(0, valu, INDICATOR_DATA)
    SetIndexBuffer(1, vala, INDICATOR_DATA)
    SetIndexBuffer(2, vald, INDICATOR_DATA)
    _maHandle = iMA(Symbol(), 0, inpBandPeriod, 0, inpBandMethod, inpBandPrice)
    if _maHandle == INVALID_HANDLE:
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Kirshenbaum ' + StringSubstr(EnumToString(inpBandMethod, 'ENUM_MA_METHOD'), 5) + ' bands (' + _str(inpBandPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(_maHandle, 0, 0, _copyCount, vala) != _copyCount:
        return prev_calculated
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        price = getPrice(inpBandPrice, open, close, high, low, i)
        error = iStdError(price, inpBandPeriod, i, rates_total)
        if vala[i] == EMPTY_VALUE:
            vala[i] = price
        valu[i] = vala[i] + (inpBandDeviations * error)
        vald[i] = vala[i] - (inpBandDeviations * error)
        i += 1
    return i

def iStdError(price, period, i, bars):
    global _s_iStdError_m_arraySize
    if _s_iStdError_m_arraySize < bars:
        _s_iStdError_m_arraySize = ArrayResize(_s_iStdError_m_array, bars + 500)
        if _s_iStdError_m_arraySize < bars:
            return 0.0
    _s_iStdError_m_array[i] = price
    avgx = _fdiv(period * (period - 1) * 0.5, period)
    avgy = _s_iStdError_m_array[i]
    j = 1
    while j < period and (i - j) >= 0:
        avgy += _s_iStdError_m_array[i - j]
        j += 1
    avgy = _fdiv(avgy, j)
    sumdx = 0.0
    sumdy = 0.0
    sumdxdy = 0.0
    k = 0
    while k < period and i >= k:
        dx = k - avgx
        dy = _s_iStdError_m_array[i - k] - avgy
        sumdx += dx * dx
        sumdy += dy * dy
        sumdxdy += dx * dy
        k += 1
    err = (_fdiv(sumdy - _fdiv(sumdxdy * sumdxdy, sumdx), period - 2.0) if (sumdx != 0) else 0)
    if err > 0:
        return MathSqrt(err)
    else:
        return 0.0

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

# ---- static local variables
_s_iStdError_m_arraySize = -1
_s_iStdError_m_array = Arr(0, 0.0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KirshenbaumBands(_MQL5Indicator):
    name = 'Kirshenbaum bands'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpBandPeriod': 21,  # Bands period
        'inpBandPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpBandMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Bands average method
        'inpBandDeviations': 2.0,  # Bands deviation
    }

