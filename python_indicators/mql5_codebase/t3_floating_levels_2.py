"""T3 floating levels (2) — converted from MQL5: MQL5 Indicators/T3 floating levels (2)/T3 floating levels (2).mq5

This T3 uses two methods for calculating T3
 
    1 - The original Tim Tillson way
    2 - The modified Bob Fulks / Alex Matulich way
 
Modified version is a bit 'faster' in response to price changes
Copyright: ©mladen, 2021; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '©mladen, 2021', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 8}, 'colors': {1: [14474460], 2: [8421504], 3: [11119017, 3329330, 36095]}, 'widths': {3: 3}, 'styles': {2: 2}, 'labels': {1: 'T3 zone', 2: 'T3 middle', 3: 'T3'}, 'levels': [], 'description': ['This T3 uses two methods for calculating T3', ' ', '    1 - The original Tim Tillson way', '    2 - The modified Bob Fulks / Alex Matulich way', ' ', "Modified version is a bit 'faster' in response to price changes"], 'name': 'T3 floating levels (2)', 'source': 'MQL5 Indicators/T3 floating levels (2)/T3 floating levels (2).mq5', 'folder': 'T3 floating levels (2)', 'inputs': [{'mql': 'T3Period', 'py': 'T3Period', 'param': 'T3Period', 'type': 'double', 'default': 25.0, 'label': 'T3 period', 'sinput': False}, {'mql': 'T3Hot', 'py': 'T3Hot', 'param': 'T3Hot', 'type': 'double', 'default': 0.7, 'label': 'T3 volume factor', 'sinput': False}, {'mql': 'T3Original', 'py': 'T3Original', 'param': 'T3Original', 'type': 'int', 'default': 0, 'label': 'T3 calculation mode', 'sinput': False}, {'mql': 'T3Price', 'py': 'T3Price', 'param': 'T3Price', 'type': 'int', 'default': 1, 'label': 'Average price', 'sinput': False}, {'mql': 'ColorOn', 'py': 'ColorOn', 'param': 'ColorOn', 'type': 'int', 'default': 1, 'label': 'Color change on :', 'sinput': False}, {'mql': 'FlPeriod', 'py': 'FlPeriod', 'param': 'FlPeriod', 'type': 'int', 'default': 25, 'label': 'Period for finding floating levels', 'sinput': False}, {'mql': 'FlUp', 'py': 'FlUp', 'param': 'FlUp', 'type': 'double', 'default': 90.0, 'label': 'Upper level %', 'sinput': False}, {'mql': 'FlDown', 'py': 'FlDown', 'param': 'FlDown', 'type': 'double', 'default': 10.0, 'label': 'Lower level %', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enT3Type
t3_tillson = 1
t3_fulksmat = 0
_enum('enT3Type', {1: 't3_tillson', 0: 't3_fulksmat'})

# enum chgColor
chg_onSlope = 0
chg_onLevel = 1
chg_onMiddle = 2
_enum('chgColor', {0: 'chg_onSlope', 1: 'chg_onLevel', 2: 'chg_onMiddle'})

# ---- inputs and global variables
T3Period = _input('T3Period', 25.0)  # T3 period
T3Hot = _input('T3Hot', 0.7)  # T3 volume factor
T3Original = _input('T3Original', t3_fulksmat)  # T3 calculation mode
T3Price = _input('T3Price', PRICE_CLOSE)  # Average price
ColorOn = _input('ColorOn', chg_onLevel)  # Color change on :
FlPeriod = _input('FlPeriod', 25)  # Period for finding floating levels
FlUp = _input('FlUp', 90.0)  # Upper level %
FlDown = _input('FlDown', 10.0)  # Lower level %
t3 = Arr(0, 0.0)
t3c = Arr(0, 0.0)
mid = Arr(0, 0.0)
fup = Arr(0, 0.0)
fdn = Arr(0, 0.0)

class sCoeffStruct(MqlObject):
    _q_fields = ('volumeFactor', 'volumePlus', 'period', 'alpha', 'result', 'original')
    def __init__(self):
        self.volumeFactor = 0.0
        self.volumePlus = 0.0
        self.period = 0.0
        self.alpha = 0.0
        self.result = 0.0
        self.original = False
        self.period = EMPTY_VALUE

class sDataStruct(MqlObject):
    _q_fields = ('val',)
    def __init__(self, *args):
        self.val = Arr(7, 0.0, dyn=False)

class sWorkStruct(MqlObject):
    _q_fields = ('data',)
    def __init__(self, *args):
        self.data = Arr(1, 0, dyn=False, factory=sDataStruct)

def OnInit():
    SetIndexBuffer(0, fup, INDICATOR_DATA)
    SetIndexBuffer(1, fdn, INDICATOR_DATA)
    SetIndexBuffer(2, mid, INDICATOR_DATA)
    SetIndexBuffer(3, t3, INDICATOR_DATA)
    SetIndexBuffer(4, t3c, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'T3 floating levels (' + _str(T3Period) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    for i in range(limit, rates_total):
        price = 0.0
        _sw1 = T3Price
        if _sw1 == PRICE_CLOSE:
            price = close[i]
        elif _sw1 == PRICE_OPEN:
            price = open[i]
        elif _sw1 == PRICE_HIGH:
            price = high[i]
        elif _sw1 == PRICE_LOW:
            price = low[i]
        elif _sw1 == PRICE_MEDIAN:
            price = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            price = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            price = 0.0
        t3[i] = iT3(price, T3Period, T3Hot, (T3Original != 0), i, rates_total)
        _start = i - FlPeriod + 1
        if _start < 0:
            _start = 0
        hi = t3[ArrayMaximum(t3, _start, FlPeriod)]
        lo = t3[ArrayMinimum(t3, _start, FlPeriod)]
        rn = hi - lo
        fup[i] = lo + ((rn * FlUp) / 100.0)
        fdn[i] = lo + ((rn * FlDown) / 100.0)
        mid[i] = (fup[i] + fdn[i]) / 2
        _sw2 = ColorOn
        if _sw2 == chg_onLevel:
            t3c[i] = (1 if (t3[i] > fup[i]) else 2 if (t3[i] < fdn[i]) else 0)
        elif _sw2 == chg_onMiddle:
            t3c[i] = (1 if (t3[i] > mid[i]) else 2 if (t3[i] < mid[i]) else 0)
        else:
            t3c[i] = ((1 if (t3[i] > t3[i - 1]) else 2 if (t3[i] < t3[i - 1]) else 0) if (i > 0) else 0)
    return rates_total

def iT3(value, period, volumeFactor, original, r, bars, instanceNo=0):
    global _s_iT3_m_arraySize
    if _s_iT3_m_arraySize <= bars:
        _s_iT3_m_arraySize = ArrayResize(_s_iT3_m_array, bars + 500, 2000)
    if _s_iT3_m_coeffs[instanceNo].period != period or _s_iT3_m_coeffs[instanceNo].volumeFactor != volumeFactor:
        _s_iT3_m_coeffs[instanceNo].period = (period if (period > 1) else 1)
        _s_iT3_m_coeffs[instanceNo].alpha = (_fdiv(2.0, 1.0 + _s_iT3_m_coeffs[instanceNo].period) if original else _fdiv(2.0, 2.0 + ((_s_iT3_m_coeffs[instanceNo].period - 1.0) / 2.0)))
        _s_iT3_m_coeffs[instanceNo].volumeFactor = ((1 if (volumeFactor > 1) else volumeFactor) if (volumeFactor > 0) else DBL_MIN)
        _s_iT3_m_coeffs[instanceNo].volumePlus = volumeFactor + 1
    if r > 0:
        _s_iT3_m_array[r].data[instanceNo].val[0] = _s_iT3_m_array[r - 1].data[instanceNo].val[0] + (_s_iT3_m_coeffs[instanceNo].alpha * (value - _s_iT3_m_array[r - 1].data[instanceNo].val[0]))
        _s_iT3_m_array[r].data[instanceNo].val[1] = _s_iT3_m_array[r - 1].data[instanceNo].val[1] + (_s_iT3_m_coeffs[instanceNo].alpha * (_s_iT3_m_array[r].data[instanceNo].val[0] - _s_iT3_m_array[r - 1].data[instanceNo].val[1]))
        _s_iT3_m_array[r].data[instanceNo].val[2] = _s_iT3_m_array[r - 1].data[instanceNo].val[2] + (_s_iT3_m_coeffs[instanceNo].alpha * ((_s_iT3_m_array[r].data[instanceNo].val[0] * _s_iT3_m_coeffs[instanceNo].volumePlus) - (_s_iT3_m_array[r].data[instanceNo].val[1] * _s_iT3_m_coeffs[instanceNo].volumeFactor) - _s_iT3_m_array[r - 1].data[instanceNo].val[2]))
        _s_iT3_m_array[r].data[instanceNo].val[3] = _s_iT3_m_array[r - 1].data[instanceNo].val[3] + (_s_iT3_m_coeffs[instanceNo].alpha * (_s_iT3_m_array[r].data[instanceNo].val[2] - _s_iT3_m_array[r - 1].data[instanceNo].val[3]))
        _s_iT3_m_array[r].data[instanceNo].val[4] = _s_iT3_m_array[r - 1].data[instanceNo].val[4] + (_s_iT3_m_coeffs[instanceNo].alpha * ((_s_iT3_m_array[r].data[instanceNo].val[2] * _s_iT3_m_coeffs[instanceNo].volumePlus) - (_s_iT3_m_array[r].data[instanceNo].val[3] * _s_iT3_m_coeffs[instanceNo].volumeFactor) - _s_iT3_m_array[r - 1].data[instanceNo].val[4]))
        _s_iT3_m_array[r].data[instanceNo].val[5] = _s_iT3_m_array[r - 1].data[instanceNo].val[5] + (_s_iT3_m_coeffs[instanceNo].alpha * (_s_iT3_m_array[r].data[instanceNo].val[4] - _s_iT3_m_array[r - 1].data[instanceNo].val[5]))
        _s_iT3_m_array[r].data[instanceNo].val[6] = (_s_iT3_m_array[r].data[instanceNo].val[4] * _s_iT3_m_coeffs[instanceNo].volumePlus) - (_s_iT3_m_array[r].data[instanceNo].val[5] * _s_iT3_m_coeffs[instanceNo].volumeFactor)
    else:
        ArrayInitialize(_s_iT3_m_array[r].data[instanceNo].val, value)
    return _s_iT3_m_array[r].data[instanceNo].val[6]

# ---- static local variables
_s_iT3_m_coeffs = Arr(1, 0, dyn=False, factory=sCoeffStruct)
_s_iT3_m_array = Arr(0, 0, factory=sWorkStruct)
_s_iT3_m_arraySize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class T3FloatingLevels2(_MQL5Indicator):
    name = 'T3 floating levels (2)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'T3Period': 25.0,  # T3 period
        'T3Hot': 0.7,  # T3 volume factor
        'T3Original': _Choice({1: 'Tim Tillson way of calculation', 0: 'Fulks/Matulich way of calculation'}, default=0),  # T3 calculation mode
        'T3Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Average price
        'ColorOn': _Choice({0: 'change color on slope change', 1: 'Change color on outer levels cross', 2: 'Change color on middle level cross'}, default=1),  # Color change on :
        'FlPeriod': 25,  # Period for finding floating levels
        'FlUp': 90.0,  # Upper level %
        'FlDown': 10.0,  # Lower level %
    }

