"""Chandes dmi (dsl)(vra) — converted from MQL5: MQL5 Indicators/Chande's DMI - volatility ratio adaptive/Chandes dmi (dsl)(vra).mq5

Chande\\'s DMI with discontinued signal lines
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 8}, 'colors': {1: [8421504], 2: [8421504], 3: [8421504], 4: [11119017, 7451452, 17919]}, 'widths': {4: 2}, 'styles': {1: 2, 2: 2, 3: 2}, 'labels': {1: 'Upper level', 2: 'Middle level', 3: 'Lower level', 4: 'Chande DMI'}, 'levels': [], 'description': ["Chande\\'s DMI with discontinued signal lines"], 'name': 'Chandes dmi (dsl)(vra)', 'source': "MQL5 Indicators/Chande's DMI - volatility ratio adaptive/Chandes dmi (dsl)(vra).mq5", 'folder': "Chande's DMI - volatility ratio adaptive", 'inputs': [{'mql': 'inpDMIPeriod', 'py': 'inpDMIPeriod', 'param': 'inpDMIPeriod', 'type': 'int', 'default': 15, 'label': 'DMI period', 'sinput': False}, {'mql': 'inpDmiLowerLimit', 'py': 'inpDmiLowerLimit', 'param': 'inpDmiLowerLimit', 'type': 'int', 'default': 10, 'label': 'DMI lower bound', 'sinput': False}, {'mql': 'inpDmiUpperLimit', 'py': 'inpDmiUpperLimit', 'param': 'inpDmiUpperLimit', 'type': 'int', 'default': 50, 'label': 'DMI upper bound', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpDevPeriod', 'py': 'inpDevPeriod', 'param': 'inpDevPeriod', 'type': 'int', 'default': 10, 'label': 'Period of smoothing', 'sinput': False}, {'mql': 'inpDslPeriod', 'py': 'inpDslPeriod', 'param': 'inpDslPeriod', 'type': 'int', 'default': 10, 'label': 'DSL period', 'sinput': False}, {'mql': 'inpColorChange', 'py': 'inpColorChange', 'param': 'inpColorChange', 'type': 'int', 'default': 1, 'label': 'Color changing mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorChangeOn
cchange_onSlope = 0
cchange_onLevels = 1
cchange_onZero = 2
_enum('enColorChangeOn', {0: 'cchange_onSlope', 1: 'cchange_onLevels', 2: 'cchange_onZero'})

# ---- inputs and global variables
inpDMIPeriod = _input('inpDMIPeriod', 15)  # DMI period
inpDmiLowerLimit = _input('inpDmiLowerLimit', 10)  # DMI lower bound
inpDmiUpperLimit = _input('inpDmiUpperLimit', 50)  # DMI upper bound
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpDevPeriod = _input('inpDevPeriod', 10)  # Period of smoothing
inpDslPeriod = _input('inpDslPeriod', 10)  # DSL period
inpColorChange = _input('inpColorChange', cchange_onLevels)  # Color changing mode
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
levu = Arr(0, 0.0)
levd = Arr(0, 0.0)
levm = Arr(0, 0.0)
m_array = Arr(0, 0.0, dims=(13,))
_dslPeriod = 0.0

class cStdDevVolatilityRatio(MqlObject):
    _q_fields = ('m_period', 'm_arraySize', 'm_array')
    def __init__(self):
        self.m_period = 0
        self.m_arraySize = 0
        self.m_array = Arr(0, 0, factory=sStdDevVolatilityRatioStruct)
        self.m_arraySize = -1
    def _q_dtor(self):
        ArrayFree(self.m_array)
    def init(self, period):
        self.m_period = (period if (period > 1) else 1)
    def calculate(self, price, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        self.m_array[i].price = price
        self.m_array[i].price2 = price * price
        if i > self.m_period:
            self.m_array[i].sum = self.m_array[i - 1].sum + self.m_array[i].price - self.m_array[i - self.m_period].price
            self.m_array[i].sum2 = self.m_array[i - 1].sum2 + self.m_array[i].price2 - self.m_array[i - self.m_period].price2
        else:
            self.m_array[i].sum = self.m_array[i].price
            self.m_array[i].sum2 = self.m_array[i].price2
            k = 1
            while k < self.m_period and i >= k:
                self.m_array[i].sum += self.m_array[i - k].price
                self.m_array[i].sum2 += self.m_array[i - k].price2
                k += 1
        self.m_array[i].deviation = MathSqrt(_fdiv(self.m_array[i].sum2 - _fdiv(self.m_array[i].sum * self.m_array[i].sum, float(self.m_period)), float(self.m_period)))
        if i > self.m_period:
            self.m_array[i].sumd = self.m_array[i - 1].sumd + self.m_array[i].deviation - self.m_array[i - self.m_period].deviation
        else:
            self.m_array[i].sumd = self.m_array[i].deviation
            k = 1
            while k < self.m_period and i >= k:
                self.m_array[i].sumd += self.m_array[i - k].deviation
                k += 1
        return (_fdiv(float(self.m_period) * self.m_array[i].deviation, self.m_array[i].sumd) if (self.m_array[i].sumd > 0) else 1)

class sStdDevVolatilityRatioStruct(MqlObject):
    _q_fields = ('price', 'price2', 'sum', 'sum2', 'sumd', 'deviation')
    def __init__(self, *args):
        self.price = 0.0
        self.price2 = 0.0
        self.sum = 0.0
        self.sum2 = 0.0
        self.sumd = 0.0
        self.deviation = 0.0

def OnInit():
    global _dslPeriod
    SetIndexBuffer(0, levu, INDICATOR_DATA)
    SetIndexBuffer(1, levm, INDICATOR_DATA)
    SetIndexBuffer(2, levd, INDICATOR_DATA)
    SetIndexBuffer(3, val, INDICATOR_DATA)
    SetIndexBuffer(4, valc, INDICATOR_COLOR_INDEX)
    iVolatilityRatio.init(inpDevPeriod)
    _dslPeriod = (inpDslPeriod if (inpDslPeriod > 1) else 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Chandes DMI (' + _str(inpDMIPeriod) + ',' + _str(inpDslPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_arraySize
    if _s_OnCalculate_m_arraySize < rates_total:
        _s_OnCalculate_m_arraySize = ArrayResize(m_array, rates_total + 500)
        if _s_OnCalculate_m_arraySize < rates_total:
            return 0
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _price = 0.0
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            _price = close[i]
        elif _sw1 == PRICE_OPEN:
            _price = open[i]
        elif _sw1 == PRICE_HIGH:
            _price = high[i]
        elif _sw1 == PRICE_LOW:
            _price = low[i]
        elif _sw1 == PRICE_MEDIAN:
            _price = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            _price = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            _price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            _price = 0.0
        vr = iVolatilityRatio.calculate(_price, i, rates_total)
        td = _fdiv(inpDMIPeriod, vr)
        if td > inpDmiUpperLimit:
            td = inpDmiUpperLimit
        if td < inpDmiLowerLimit:
            td = inpDmiLowerLimit
        kg = _fdiv(3.0, 2.0 + td)
        hg = 1.0 - kg
        m_array[i][12] = _price
        if i > 0:
            mom = m_array[i][12] - m_array[i - 1][12]
            moa = (mom if (mom > 0) else (-mom))
            m_array[i][0] = (kg * mom) + (hg * m_array[i - 1][0])
            m_array[i][1] = (kg * m_array[i][0]) + (hg * m_array[i - 1][1])
            m_array[i][2] = (kg * ((1.5 * m_array[i][0]) - (0.5 * m_array[i][1]))) + (hg * m_array[i - 1][2])
            m_array[i][3] = (kg * m_array[i][2]) + (hg * m_array[i - 1][3])
            m_array[i][4] = (kg * ((1.5 * m_array[i][2]) - (0.5 * m_array[i][3]))) + (hg * m_array[i - 1][4])
            m_array[i][5] = (kg * m_array[i][4]) + (hg * m_array[i - 1][5])
            m_array[i][6] = (kg * moa) + (hg * m_array[i - 1][6])
            m_array[i][7] = (kg * m_array[i][6]) + (hg * m_array[i - 1][7])
            m_array[i][8] = (kg * ((1.5 * m_array[i][6]) - (0.5 * m_array[i][7]))) + (hg * m_array[i - 1][8])
            m_array[i][9] = (kg * m_array[i][8]) + (hg * m_array[i - 1][9])
            m_array[i][10] = (kg * ((1.5 * m_array[i][8]) - (0.5 * m_array[i][9]))) + (hg * m_array[i - 1][10])
            m_array[i][11] = (kg * m_array[i][10]) + (hg * m_array[i - 1][11])
            mom = (1.5 * m_array[i][4]) - (0.5 * m_array[i][5])
            moa = (1.5 * m_array[i][10]) - (0.5 * m_array[i][11])
            val[i] = (_fdiv(mom, (moa if (moa > DBL_MIN) else DBL_MIN)) + 1.0) * 50.0
            _alpha = _fdiv(2.0, 1.0 + _fdiv(_dslPeriod, vr))
            levu[i] = ((levu[i - 1] + (_alpha * (val[i] - levu[i - 1]))) if (val[i] > 50) else levu[i - 1])
            levd[i] = ((levd[i - 1] + (_alpha * (val[i] - levd[i - 1]))) if (val[i] < 50) else levd[i - 1])
            levm[i] = (levu[i] + levd[i]) / 2.0
        else:
            for k in range(0, 12):
                m_array[i][k] = 0.0
            val[i] = 0.0
            levd[i] = val[i]
            levu[i] = levd[i]
            levm[i] = levu[i]
        _sw2 = inpColorChange
        if _sw2 == cchange_onLevels:
            valc[i] = (1 if (val[i] > levu[i]) else 2 if (val[i] < levd[i]) else 0)
        elif _sw2 == cchange_onSlope:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        elif _sw2 == cchange_onZero:
            valc[i] = (1 if (val[i] > levm[i]) else 2 if (val[i] < levm[i]) else 0)
        i += 1
    return i

# ---- global variables initialised from expressions
iVolatilityRatio = _alloc(cStdDevVolatilityRatio)
iVolatilityRatio.__init__()

# ---- static local variables
_s_OnCalculate_m_arraySize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ChandesDmiDslVra(_MQL5Indicator):
    name = 'Chandes dmi (dsl)(vra)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpDMIPeriod': 15,  # DMI period
        'inpDmiLowerLimit': 10,  # DMI lower bound
        'inpDmiUpperLimit': 50,  # DMI upper bound
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpDevPeriod': 10,  # Period of smoothing
        'inpDslPeriod': 10,  # DSL period
        'inpColorChange': _Choice({0: 'Change color on slope change', 1: 'Change color on outer levels cross', 2: 'Change color on middle level cross'}, default=1),  # Color changing mode
    }

