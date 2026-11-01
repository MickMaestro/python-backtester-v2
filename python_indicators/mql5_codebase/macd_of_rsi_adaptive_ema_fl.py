"""MACD of RSI adaptive EMA (fl) — converted from MQL5: MQL5 Indicators/MACD of RSI adaptive EMA - with floating levels/MACD of RSI adaptive EMA (fl).mq5

MACD of RSI adaptive EMA - floating levels
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 8, 5: 1}, 'colors': {1: [8421504], 2: [8421504], 3: [8421504], 4: [11119017, 7451452, 17919], 5: [255]}, 'widths': {4: 2}, 'styles': {1: 2, 2: 2, 3: 2, 5: 2}, 'labels': {1: 'Upper level', 2: 'Middle level', 3: 'Lower level', 4: 'MACD', 5: 'MACD signal line'}, 'levels': [], 'description': ['MACD of RSI adaptive EMA - floating levels'], 'name': 'MACD of RSI adaptive EMA (fl)', 'source': 'MQL5 Indicators/MACD of RSI adaptive EMA - with floating levels/MACD of RSI adaptive EMA (fl).mq5', 'folder': 'MACD of RSI adaptive EMA - with floating levels', 'inputs': [{'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 12, 'label': 'MACD fast period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 26, 'label': 'MACD slow period', 'sinput': False}, {'mql': 'inpSignalPeriod', 'py': 'inpSignalPeriod', 'param': 'inpSignalPeriod', 'type': 'int', 'default': 9, 'label': 'MACD signal period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpFlPeriod', 'py': 'inpFlPeriod', 'param': 'inpFlPeriod', 'type': 'int', 'default': 25, 'label': 'Floating levels period', 'sinput': False}, {'mql': 'inpFlLevelUp', 'py': 'inpFlLevelUp', 'param': 'inpFlLevelUp', 'type': 'double', 'default': 90.0, 'label': 'Floating levels up %', 'sinput': False}, {'mql': 'inpFlLevelDn', 'py': 'inpFlLevelDn', 'param': 'inpFlLevelDn', 'type': 'double', 'default': 10.0, 'label': 'Floating levels down %', 'sinput': False}, {'mql': 'inpColorChange', 'py': 'inpColorChange', 'param': 'inpColorChange', 'type': 'int', 'default': 2, 'label': 'Color changing mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorChangeOn
cchange_onSlope = 0
cchange_onSignal = 1
cchange_onLevels = 2
cchange_onZero = 3
_enum('enColorChangeOn', {0: 'cchange_onSlope', 1: 'cchange_onSignal', 2: 'cchange_onLevels', 3: 'cchange_onZero'})

# ---- inputs and global variables
inpFastPeriod = _input('inpFastPeriod', 12)  # MACD fast period
inpSlowPeriod = _input('inpSlowPeriod', 26)  # MACD slow period
inpSignalPeriod = _input('inpSignalPeriod', 9)  # MACD signal period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpFlPeriod = _input('inpFlPeriod', 25)  # Floating levels period
inpFlLevelUp = _input('inpFlLevelUp', 90.0)  # Floating levels up %
inpFlLevelDn = _input('inpFlLevelDn', 10.0)  # Floating levels down %
inpColorChange = _input('inpColorChange', cchange_onLevels)  # Color changing mode
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levu = Arr(0, 0.0)
levd = Arr(0, 0.0)
levm = Arr(0, 0.0)
signal = Arr(0, 0.0)
emaf = Arr(0, 0.0)
emas = Arr(0, 0.0)

class sRsiStruct(MqlObject):
    _q_fields = ('price', 'change', 'changa')
    def __init__(self, *args):
        self.price = 0.0
        self.change = 0.0
        self.changa = 0.0

def OnInit():
    global _ub0__alphaSignal
    SetIndexBuffer(0, levu, INDICATOR_DATA)
    SetIndexBuffer(1, levm, INDICATOR_DATA)
    SetIndexBuffer(2, levd, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, signal, INDICATOR_DATA)
    SetIndexBuffer(6, emaf, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, emas, INDICATOR_CALCULATIONS)
    _ub0__alphaSignal = _fdiv(2.0, 1.0 + inpSignalPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MACD of RSI adaptive EMA (' + _str(inpFastPeriod) + ',' + _str(inpSlowPeriod) + ',' + _str(inpSignalPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_i, _s_OnCalculate_prev_max, _s_OnCalculate_prev_min
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _price = getPrice(inpPrice, open, close, high, low, i)
        _alphaf = ((iRsi(_price, inpFastPeriod, i, rates_total, 0) / 100.0) - 0.5) * 2.0
        if _alphaf < 0:
            _alphaf *= -1.0
        _alphas = ((iRsi(_price, inpSlowPeriod, i, rates_total, 1) / 100.0) - 0.5) * 2.0
        if _alphas < 0:
            _alphas *= -1.0
        if i > 0:
            emaf[i] = emaf[i - 1] + (_alphaf * (_price - emaf[i - 1]))
            emas[i] = emas[i - 1] + (_alphas * (_price - emas[i - 1]))
            val[i] = emaf[i] - emas[i]
            signal[i] = signal[i - 1] + (_ub0__alphaSignal * (val[i] - signal[i - 1]))
            if _s_OnCalculate_prev_i != i:
                _s_OnCalculate_prev_i = i
                start = i - inpFlPeriod + 1
                if start < 0:
                    start = 0
                _s_OnCalculate_prev_max = val[ArrayMaximum(val, start, inpFlPeriod - 1)]
                _s_OnCalculate_prev_min = val[ArrayMinimum(val, start, inpFlPeriod - 1)]
            min_ = (val[i] if (val[i] < _s_OnCalculate_prev_min) else _s_OnCalculate_prev_min)
            max_ = (val[i] if (val[i] > _s_OnCalculate_prev_max) else _s_OnCalculate_prev_max)
            range_ = (max_ - min_) / 100.0
            levu[i] = min_ + (inpFlLevelUp * range_)
            levd[i] = min_ + (inpFlLevelDn * range_)
            levm[i] = min_ + (50.0 * range_)
            _sw1 = inpColorChange
            if _sw1 == cchange_onLevels:
                valc[i] = (1 if (val[i] > levu[i]) else 2 if (val[i] < levd[i]) else 0)
            elif _sw1 == cchange_onSignal:
                valc[i] = (1 if (val[i] > signal[i]) else 2 if (val[i] < signal[i]) else 0)
            elif _sw1 == cchange_onSlope:
                valc[i] = (1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1])
            elif _sw1 == cchange_onZero:
                valc[i] = (1 if (val[i] > levm[i]) else 2 if (val[i] < levm[i]) else 0)
        else:
            emas[i] = _price
            emaf[i] = emas[i]
            signal[i] = 0.0
            valc[i] = signal[i]
            val[i] = valc[i]
        i += 1
    return i

def iRsi(price, period, i, bars, _instanceNo=0):
    global _s_iRsi_m_arraySize
    if _s_iRsi_m_arraySize < bars:
        _s_iRsi_m_arraySize = ArrayResize(_s_iRsi_m_array, bars + 500)
        if _s_iRsi_m_arraySize < bars:
            return 0.0
    alpha = _fdiv(1.0, period)
    _s_iRsi_m_array[i][_instanceNo].price = price
    if i < period:
        k = 0
        sum_ = 0.0
        k = 0
        while k < period and i > k:
            sum_ += MathAbs(_s_iRsi_m_array[i - k][_instanceNo].price - _s_iRsi_m_array[i - k - 1][_instanceNo].price)
            k += 1
        _s_iRsi_m_array[i][_instanceNo].change = _fdiv(_s_iRsi_m_array[i][_instanceNo].price - _s_iRsi_m_array[0][_instanceNo].price, MathMax(k, 1))
        _s_iRsi_m_array[i][_instanceNo].changa = _fdiv(sum_, MathMax(k, 1))
    else:
        change = _s_iRsi_m_array[i][_instanceNo].price - _s_iRsi_m_array[i - 1][_instanceNo].price
        _s_iRsi_m_array[i][_instanceNo].change = _s_iRsi_m_array[i - 1][_instanceNo].change + (alpha * (change - _s_iRsi_m_array[i - 1][_instanceNo].change))
        if change > 0:
            _s_iRsi_m_array[i][_instanceNo].changa = _s_iRsi_m_array[i - 1][_instanceNo].changa + (alpha * (change - _s_iRsi_m_array[i - 1][_instanceNo].changa))
        else:
            _s_iRsi_m_array[i][_instanceNo].changa = _s_iRsi_m_array[i - 1][_instanceNo].changa + (alpha * ((-change) - _s_iRsi_m_array[i - 1][_instanceNo].changa))
    if _s_iRsi_m_array[i][_instanceNo].changa != 0:
        return 50.0 * (_fdiv(_s_iRsi_m_array[i][_instanceNo].change, _s_iRsi_m_array[i][_instanceNo].changa) + 1.0)
    else:
        return 0.0

def getPrice(tprice, open, close, high, low, i):
    _sw2 = tprice
    if _sw2 == PRICE_CLOSE:
        return close[i]
    elif _sw2 == PRICE_OPEN:
        return open[i]
    elif _sw2 == PRICE_HIGH:
        return high[i]
    elif _sw2 == PRICE_LOW:
        return low[i]
    elif _sw2 == PRICE_MEDIAN:
        return (high[i] + low[i]) / 2.0
    elif _sw2 == PRICE_TYPICAL:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw2 == PRICE_WEIGHTED:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    return 0.0

# ---- global variables initialised from expressions
_ub0__alphaSignal = _fdiv(2.0, 1.0 + inpSignalPeriod)

# ---- static local variables
_s_OnCalculate_prev_i = -1
_s_OnCalculate_prev_max = 0.0
_s_OnCalculate_prev_min = 0.0
_s_iRsi_m_array = Arr(0, 0, factory=sRsiStruct, dims=(2,))
_s_iRsi_m_arraySize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MACDOfRSIAdaptiveEMAFl(_MQL5Indicator):
    name = 'MACD of RSI adaptive EMA (fl)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFastPeriod': 12,  # MACD fast period
        'inpSlowPeriod': 26,  # MACD slow period
        'inpSignalPeriod': 9,  # MACD signal period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpFlPeriod': 25,  # Floating levels period
        'inpFlLevelUp': 90.0,  # Floating levels up %
        'inpFlLevelDn': 10.0,  # Floating levels down %
        'inpColorChange': _Choice({0: 'Change color on slope change', 1: 'Change color on signal cross', 2: 'Change color on outer levels cross', 3: 'Change color on middle level cross'}, default=2),  # Color changing mode
    }

