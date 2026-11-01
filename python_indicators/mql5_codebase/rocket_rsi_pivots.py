"""Rocket RSI (pivots) — converted from MQL5: MQL5 Indicators/Rocket RSI pivots/Rocket RSI (pivots).mq5

Copyright: © mladen, 2019; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 8}, 'types': {8: 8}, 'colors': {8: [12632256, 7451452, 17919]}, 'widths': {8: 2}, 'styles': {}, 'labels': {8: 'Rocket RSI'}, 'levels': [], 'description': [], 'name': 'Rocket RSI (pivots)', 'source': 'MQL5 Indicators/Rocket RSI pivots/Rocket RSI (pivots).mq5', 'folder': 'Rocket RSI pivots', 'inputs': [{'mql': 'inpTimeFrame', 'py': 'inpTimeFrame', 'param': 'inpTimeFrame', 'type': 'int', 'default': 16388, 'label': 'Time frame', 'sinput': False}, {'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpSmooth', 'py': 'inpSmooth', 'param': 'inpSmooth', 'type': 'int', 'default': 50, 'label': 'Smoothing', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpCalcMode', 'py': 'inpCalcMode', 'param': 'inpCalcMode', 'type': 'int', 'default': 0, 'label': 'Calculating mode', 'sinput': False}, {'mql': 'inpColorSup', 'py': 'inpColorSup', 'param': None, 'type': 'color', 'default': 17919, 'label': 'Support color', 'sinput': False}, {'mql': 'inpColorRes', 'py': 'inpColorRes', 'param': None, 'type': 'color', 'default': 7451452, 'label': 'Resistance color', 'sinput': False}, {'mql': 'inpColorPiv', 'py': 'inpColorPiv', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'Resistance color', 'sinput': False}, {'mql': 'inpDisplayType', 'py': 'inpDisplayType', 'param': 'inpDisplayType', 'type': 'int', 'default': 1, 'label': 'Display type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enTimeFrames
tf_cu = 0
tf_m1 = 1
tf_m2 = 2
tf_m3 = 3
tf_m4 = 4
tf_m5 = 5
tf_m6 = 6
tf_m10 = 10
tf_m12 = 12
tf_m15 = 15
tf_m20 = 20
tf_m30 = 30
tf_h1 = 16385
tf_h2 = 16386
tf_h3 = 16387
tf_h4 = 16388
tf_h6 = 16390
tf_h8 = 16392
tf_h12 = 16396
tf_d1 = 16408
tf_w1 = 32769
tf_mn = 49153
tf_cp1 = -1
tf_cp2 = -2
tf_cp3 = -3
_enum('enTimeFrames', {0: 'tf_cu', 1: 'tf_m1', 2: 'tf_m2', 3: 'tf_m3', 4: 'tf_m4', 5: 'tf_m5', 6: 'tf_m6', 10: 'tf_m10', 12: 'tf_m12', 15: 'tf_m15', 20: 'tf_m20', 30: 'tf_m30', 16385: 'tf_h1', 16386: 'tf_h2', 16387: 'tf_h3', 16388: 'tf_h4', 16390: 'tf_h6', 16392: 'tf_h8', 16396: 'tf_h12', 16408: 'tf_d1', 32769: 'tf_w1', 49153: 'tf_mn', -1: 'tf_cp1', -2: 'tf_cp2', -3: 'tf_cp3'})

# enum enCalcMode
calc_fisher = 0
calc_regular = 1
_enum('enCalcMode', {0: 'calc_fisher', 1: 'calc_regular'})

# enum enDisplayType
type_1 = 0
type_2 = 1
type_3 = 2
type_4 = 3
_enum('enDisplayType', {0: 'type_1', 1: 'type_2', 2: 'type_3', 3: 'type_4'})

# ---- inputs and global variables
inpTimeFrame = _input('inpTimeFrame', tf_h4)  # Time frame
inpPeriod = _input('inpPeriod', 14)  # Period
inpSmooth = _input('inpSmooth', 50)  # Smoothing
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpCalcMode = _input('inpCalcMode', calc_fisher)  # Calculating mode
inpColorSup = _input('inpColorSup', clrOrangeRed)  # Support color
inpColorRes = _input('inpColorRes', clrMediumSeaGreen)  # Resistance color
inpColorPiv = _input('inpColorPiv', clrGray)  # Resistance color
inpDisplayType = _input('inpDisplayType', type_2)  # Display type
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
sup1 = Arr(0, 0.0)
sup2 = Arr(0, 0.0)
sup3 = Arr(0, 0.0)
res1 = Arr(0, 0.0)
res2 = Arr(0, 0.0)
res3 = Arr(0, 0.0)
piv = Arr(0, 0.0)
_pivotsTimeFrame = 0
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

class CRocketRsi(MqlObject):
    _q_fields = ('m_mode', 'm_period', 'm_coeff1', 'm_coeff2', 'm_coeff3', 'm_arraySize', 'm_array')
    def __init__(self):
        self.m_mode = 0
        self.m_period = 0
        self.m_coeff1 = 0.0
        self.m_coeff2 = 0.0
        self.m_coeff3 = 0.0
        self.m_arraySize = 0
        self.m_array = Arr(0, 0, factory=sRocketRsiArrayStruct)
        self.m_arraySize = -1
    def _q_dtor(self):
        ArrayFree(self.m_array)
    def init(self, period, smooth, mode):
        self.m_period = (period if (period > 1) else 1)
        self.m_mode = mode
        _smooth = (smooth if (smooth > 1) else 1)
        a = MathExp(_fdiv(-1.414 * M_PI, _smooth))
        self.m_coeff2 = 2 * a * MathCos(_fdiv(1.414 * M_PI, _smooth))
        self.m_coeff3 = (-a) * a
        self.m_coeff1 = 1 - self.m_coeff2 - self.m_coeff3
        return True
    def caculate(self, value, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        self.m_array[i].value = value
        if i > self.m_period:
            self.m_array[i].momentum = self.m_array[i].value - self.m_array[_imod(i - self.m_period + 1, self.m_arraySize)].value
            self.m_array[i].filter = (self.m_coeff1 * ((self.m_array[i].momentum + self.m_array[i - 1].momentum) / 2.0)) + (self.m_coeff2 * self.m_array[i - 1].filter) + (self.m_coeff3 * self.m_array[_imod(i - 2, self.m_arraySize)].filter)
            if self.m_array[i].filter > self.m_array[i - 1].filter:
                self.m_array[i].diffp = self.m_array[i].filter - self.m_array[i - 1].filter
                self.m_array[i].diffn = 0.0
            else:
                self.m_array[i].diffn = self.m_array[i - 1].filter - self.m_array[i].filter
                self.m_array[i].diffp = 0.0
            self.m_array[i].sump = self.m_array[i - 1].sump + self.m_array[i].diffp - self.m_array[i - self.m_period].diffp
            self.m_array[i].sumn = self.m_array[i - 1].sumn + self.m_array[i].diffn - self.m_array[i - self.m_period].diffn
        else:
            self.m_array[i].momentum = self.m_array[i].value - self.m_array[0].value
            self.m_array[i].filter = (((self.m_coeff1 * ((self.m_array[i].momentum + self.m_array[i - 1].momentum) / 2)) + (self.m_coeff2 * self.m_array[i - 1].filter) + (self.m_coeff3 * self.m_array[_imod(i - 2, self.m_arraySize)].filter)) if (i > 1) else self.m_array[i].momentum)
            self.m_array[i].diffp = (((self.m_array[i].filter - self.m_array[i - 1].filter) if (self.m_array[i].filter > self.m_array[i - 1].filter) else 0) if (i > 0) else 0)
            self.m_array[i].diffn = (((self.m_array[i - 1].filter - self.m_array[i].filter) if (self.m_array[i].filter < self.m_array[i - 1].filter) else 0) if (i > 0) else 0)
            self.m_array[i].sump = self.m_array[i].diffp
            self.m_array[i].sumn = self.m_array[i].diffn
            k = 1
            while k < self.m_period and i >= k:
                self.m_array[i].sump += self.m_array[i - k].diffp
                self.m_array[i].sumn += self.m_array[i - k].diffn
                k += 1
        denom = self.m_array[i].sump + self.m_array[i].sumn
        rsi = (_fdiv(self.m_array[i].sump - self.m_array[i].sumn, denom) if (denom != 0) else 0)
        if self.m_mode == 0:
            if rsi > 0.999:
                rsi = 0.999
            if rsi < -0.999:
                rsi = -0.999
            return 0.5 * MathLog(_fdiv(1.0 + rsi, 1.0 - rsi))
        else:
            return rsi

class sRocketRsiArrayStruct(MqlObject):
    _q_fields = ('value', 'momentum', 'filter', 'diffp', 'diffn', 'sump', 'sumn')
    def __init__(self, *args):
        self.value = 0.0
        self.momentum = 0.0
        self.filter = 0.0
        self.diffp = 0.0
        self.diffn = 0.0
        self.sump = 0.0
        self.sumn = 0.0

def OnInit():
    global _pivotsTimeFrame
    SetIndexBuffer(0, sup3, INDICATOR_DATA)
    SetIndexBuffer(1, sup2, INDICATOR_DATA)
    SetIndexBuffer(2, sup1, INDICATOR_DATA)
    SetIndexBuffer(3, piv, INDICATOR_DATA)
    SetIndexBuffer(4, res1, INDICATOR_DATA)
    SetIndexBuffer(5, res2, INDICATOR_DATA)
    SetIndexBuffer(6, res3, INDICATOR_DATA)
    SetIndexBuffer(7, val, INDICATOR_DATA)
    SetIndexBuffer(8, valc, INDICATOR_COLOR_INDEX)
    for i in range(0, 7):
        _sw1 = i
        if _sw1 in (0, 1, 2):
            PlotIndexSetInteger(i, PLOT_LINE_COLOR, inpColorSup)
        elif _sw1 == 3:
            PlotIndexSetInteger(i, PLOT_LINE_COLOR, inpColorPiv)
        elif _sw1 in (4, 5, 6):
            PlotIndexSetInteger(i, PLOT_LINE_COLOR, inpColorRes)
        PlotIndexSetInteger(i, PLOT_DRAW_TYPE, DRAW_LINE)
        PlotIndexSetInteger(i, PLOT_LINE_STYLE, STYLE_DOT)
        PlotIndexSetInteger(i, PLOT_SHOW_DATA, False)
    iRocketRsi.init(inpPeriod, inpSmooth, inpCalcMode)
    _pivotsTimeFrame = MathMax(Period(), timeFrameGet(inpTimeFrame))
    IndicatorSetString(INDICATOR_SHORTNAME, timeFrameToString(_pivotsTimeFrame) + ' Rocket RSI (' + _str(inpPeriod) + ',' + _str(inpSmooth) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_close, _s_OnCalculate_prev_i, _s_OnCalculate_prev_max, _s_OnCalculate_prev_min
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _price = 0.0
        _sw2 = inpPrice
        if _sw2 == PRICE_CLOSE:
            _price = close[i]
        elif _sw2 == PRICE_OPEN:
            _price = open[i]
        elif _sw2 == PRICE_HIGH:
            _price = high[i]
        elif _sw2 == PRICE_LOW:
            _price = low[i]
        elif _sw2 == PRICE_MEDIAN:
            _price = (high[i] + low[i]) / 2.0
        elif _sw2 == PRICE_TYPICAL:
            _price = (high[i] + low[i] + close[i]) / 3.0
        elif _sw2 == PRICE_WEIGHTED:
            _price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            _price = 0.0
        val[i] = iRocketRsi.caculate(_price, i, rates_total)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        res3[i] = EMPTY_VALUE
        res2[i] = res3[i]
        res1[i] = res2[i]
        sup3[i] = res1[i]
        sup2[i] = sup3[i]
        sup1[i] = sup2[i]
        if _s_OnCalculate_prev_i != i:
            _s_OnCalculate_prev_i = i
            _startTime = iTime(Symbol(), _pivotsTimeFrame, iBarShift(Symbol(), _pivotsTimeFrame, time[i]) + 1)
            _endTime = iTime(Symbol(), _pivotsTimeFrame, iBarShift(Symbol(), _pivotsTimeFrame, time[i]))
            _startBar = iBarShift(Symbol(), Period(), _startTime)
            _endBar = iBarShift(Symbol(), Period(), _endTime)
            if _endBar < _startBar:
                _period = _startBar - _endBar
                _s_OnCalculate_prev_max = val[ArrayMaximum(val, rates_total - _startBar - 1, _period)]
                _s_OnCalculate_prev_min = val[ArrayMinimum(val, rates_total - _startBar - 1, _period)]
            _s_OnCalculate_prev_close = (val[rates_total - _endBar - 1] if (_endBar > 0) else val[i])
        range_ = _s_OnCalculate_prev_max - _s_OnCalculate_prev_min
        pivot = (_s_OnCalculate_prev_max + _s_OnCalculate_prev_min + _s_OnCalculate_prev_close) / 3.0
        _sw3 = inpDisplayType
        _k4 = 0 if _sw3 == 3 else 1 if _sw3 == 2 else 2 if _sw3 == 1 else 3 if _sw3 == 0 else 4
        try:
            if _k4 <= 0:
                res3[i] = (pivot * 2.0) + _s_OnCalculate_prev_max - (_s_OnCalculate_prev_min * 2.0)
                sup3[i] = (pivot * 2.0) + _s_OnCalculate_prev_min - (_s_OnCalculate_prev_max * 2.0)
            if _k4 <= 1:
                res2[i] = pivot + range_
                sup2[i] = pivot - range_
            if _k4 <= 2:
                res1[i] = (pivot * 2.0) - _s_OnCalculate_prev_min
                sup1[i] = (pivot * 2.0) - _s_OnCalculate_prev_max
            if _k4 <= 3:
                piv[i] = pivot
        except _SwitchBreak:
            pass
        i += 1
    return i

def timeFrameToString(period):
    if period == PERIOD_CURRENT:
        period = Period()
    i = 0
    i = 0
    for i in range(i, ArraySize(_tfsPer)):
        if period == _tfsPer[i]:
            break
    else:
        i = _range_end(i, ArraySize(_tfsPer), 1)
    return _tfsStr[i]

def timeFrameGet(period):
    _shift = (MathAbs(period) if (period < 0) else 0)
    if period <= 0:
        period = Period()
    i = 0
    i = 0
    for i in range(i, ArraySize(_tfsPer)):
        if period == _tfsPer[i]:
            break
    else:
        i = _range_end(i, ArraySize(_tfsPer), 1)
    return _tfsPer[MathMin(i + _shift, ArraySize(_tfsPer) - 1)]

# ---- global variables initialised from expressions
iRocketRsi = _alloc(CRocketRsi)
iRocketRsi.__init__()

# ---- static local variables
_s_OnCalculate_prev_i = -1
_s_OnCalculate_prev_max = 0.0
_s_OnCalculate_prev_min = 0.0
_s_OnCalculate_prev_close = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RocketRSIPivots(_MQL5Indicator):
    name = 'Rocket RSI (pivots)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpTimeFrame': _Choice({0: 'Current time frame', 1: '1 minute', 2: '2 minutes', 3: '3 minutes', 4: '4 minutes', 5: '5 minutes', 6: '6 minutes', 10: '10 minutes', 12: '12 minutes', 15: '15 minutes', 20: '20 minutes', 30: '30 minutes', 16385: '1 hour', 16386: '2 hours', 16387: '3 hours', 16388: '4 hours', 16390: '6 hours', 16392: '8 hours', 16396: '12 hours', 16408: 'daily', 32769: 'weekly', 49153: 'monthly', -1: 'Next higher time frame', -2: 'Second higher time frame', -3: 'Third higher time frame'}, default=16388),  # Time frame
        'inpPeriod': 14,  # Period
        'inpSmooth': 50,  # Smoothing
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpCalcMode': _Choice({0: 'Calculate fisher transform of "rocket" rsi', 1: 'Calculate "rocket" rsi only'}, default=0),  # Calculating mode
        'inpDisplayType': _Choice({0: 'Display pivot only', 1: 'Display pivot + SR 1', 2: 'Display pivot + SR 1,2', 3: 'Display pivot + SR 1,2,3'}, default=1),  # Display type
    }

