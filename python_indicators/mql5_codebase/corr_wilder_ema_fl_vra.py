"""Corr Wilder EMA (fl)(vra) — converted from MQL5: MQL5 Indicators/Corrected volatility ratio adaptive double smoothed Wilders EMA with floating levels/Corr Wilder EMA (fl)(vra).mq5

Corrected double smoothed Wilder's EMA
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 8, 4: 8}, 'colors': {1: [15132390], 2: [8421504], 3: [12632256, 7451452, 17919], 4: [12632256, 7451452, 17919]}, 'widths': {4: 3}, 'styles': {2: 2}, 'labels': {1: 'Corrected average zone', 2: 'Corrected average middle', 3: 'Corrected average original', 4: 'Corrected average '}, 'levels': [], 'description': ["Corrected double smoothed Wilder's EMA"], 'name': 'Corr Wilder EMA (fl)(vra)', 'source': 'MQL5 Indicators/Corrected volatility ratio adaptive double smoothed Wilders EMA with floating levels/Corr Wilder EMA (fl)(vra).mq5', 'folder': 'Corrected volatility ratio adaptive double smoothed Wilders EMA with floating levels', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Average period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpCorrectionPeriod', 'py': 'inpCorrectionPeriod', 'param': 'inpCorrectionPeriod', 'type': 'int', 'default': 0, 'label': '"Correction" period (<0 no correction,0 to 1 same as average)', 'sinput': False}, {'mql': 'inpColorOn', 'py': 'inpColorOn', 'param': 'inpColorOn', 'type': 'int', 'default': 1, 'label': 'Color change on :', 'sinput': False}, {'mql': 'inpFlPeriod', 'py': 'inpFlPeriod', 'param': 'inpFlPeriod', 'type': 'int', 'default': 25, 'label': 'Period for finding floating levels', 'sinput': False}, {'mql': 'inpFlUp', 'py': 'inpFlUp', 'param': 'inpFlUp', 'type': 'double', 'default': 90.0, 'label': 'Upper level %', 'sinput': False}, {'mql': 'inpFlDown', 'py': 'inpFlDown', 'param': 'inpFlDown', 'type': 'double', 'default': 10.0, 'label': 'Lower level %', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum chgColor
chg_onSlope = 0
chg_onLevel = 1
chg_onMiddle = 2
chg_onOrig = 3
_enum('chgColor', {0: 'chg_onSlope', 1: 'chg_onLevel', 2: 'chg_onMiddle', 3: 'chg_onOrig'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Average period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpCorrectionPeriod = _input('inpCorrectionPeriod', 0)  # "Correction" period (<0 no correction,0 to 1 same as average)
inpColorOn = _input('inpColorOn', chg_onLevel)  # Color change on :
inpFlPeriod = _input('inpFlPeriod', 25)  # Period for finding floating levels
inpFlUp = _input('inpFlUp', 90.0)  # Upper level %
inpFlDown = _input('inpFlDown', 10.0)  # Lower level %
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
mid = Arr(0, 0.0)
fup = Arr(0, 0.0)
fdn = Arr(0, 0.0)
avg = Arr(0, 0.0)
avgw = Arr(0, 0.0)
avgc = Arr(0, 0.0)
ª_maPeriod = 0
ª_corrPeriod = 0
ª_colorOn = 0
_alpha = 0.0

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
        deviationAverage = _fdiv(self.m_array[i].sumd, float(self.m_period))
        return (_fdiv(self.m_array[i].deviation, deviationAverage) if (deviationAverage != 0) else 1)

class sStdDevVolatilityRatioStruct(MqlObject):
    _q_fields = ('price', 'price2', 'sum', 'sum2', 'sumd', 'deviation')
    def __init__(self, *args):
        self.price = 0.0
        self.price2 = 0.0
        self.sum = 0.0
        self.sum2 = 0.0
        self.sumd = 0.0
        self.deviation = 0.0

class sCorrMaStruct(MqlObject):
    _q_fields = ('corrected', 'price', 'price2', 'summ', 'summ2')
    def __init__(self, *args):
        self.corrected = 0.0
        self.price = 0.0
        self.price2 = 0.0
        self.summ = 0.0
        self.summ2 = 0.0

def OnInit():
    global ª_colorOn, ª_corrPeriod, ª_maPeriod
    SetIndexBuffer(0, fup, INDICATOR_DATA)
    SetIndexBuffer(1, fdn, INDICATOR_DATA)
    SetIndexBuffer(2, mid, INDICATOR_DATA)
    SetIndexBuffer(3, avg, INDICATOR_DATA)
    SetIndexBuffer(4, avgc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, val, INDICATOR_DATA)
    SetIndexBuffer(6, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, avgw, INDICATOR_CALCULATIONS)
    ª_corrPeriod = (inpCorrectionPeriod if (inpCorrectionPeriod > 0) else 0 if (inpCorrectionPeriod < 0) else inpPeriod)
    ª_colorOn = (inpColorOn if (inpFlPeriod > 1 and ª_corrPeriod > 1) else inpColorOn if (inpColorOn != chg_onOrig) else chg_onSlope)
    ª_maPeriod = (inpPeriod if (inpPeriod > 1) else 1)
    iVolatilityRatio.init(inpPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, '"Corrected" Wilder\'s EMA (' + _str(inpPeriod) + ',' + _str(inpCorrectionPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _alpha, _s_OnCalculate_prev_i, _s_OnCalculate_prev_max, _s_OnCalculate_prev_min
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
        _ratio = iVolatilityRatio.calculate(_price, i, rates_total)
        _alpha = _fdiv(1.0, MathSqrt(_fdiv(ª_maPeriod, _ratio)))
        if i > 0:
            avgw[i] = avgw[i - 1] + (_alpha * (_price - avgw[i - 1]))
            avg[i] = avg[i - 1] + (_alpha * (avgw[i] - avg[i - 1]))
        else:
            avgw[i] = _price
            avg[i] = avgw[i]
        val[i] = iCorrMa(_price, avg[i], ª_corrPeriod, i, rates_total)
        if _s_OnCalculate_prev_i != i:
            _s_OnCalculate_prev_i = i
            start = i - inpFlPeriod + 1
            if start < 0:
                start = 0
            _s_OnCalculate_prev_max = val[ArrayMaximum(val, start, inpFlPeriod - 1)]
            _s_OnCalculate_prev_min = val[ArrayMinimum(val, start, inpFlPeriod - 1)]
        max_ = (val[i] if (val[i] > _s_OnCalculate_prev_max) else _s_OnCalculate_prev_max)
        min_ = (val[i] if (val[i] < _s_OnCalculate_prev_min) else _s_OnCalculate_prev_min)
        range_ = (max_ - min_) / 100.0
        fup[i] = min_ + (inpFlUp * range_)
        fdn[i] = min_ + (inpFlDown * range_)
        mid[i] = min_ + (50.0 * range_)
        avgc[i] = (1 if (avg[i] > val[i]) else 2 if (avg[i] < val[i]) else 0)
        _sw2 = ª_colorOn
        if _sw2 == chg_onOrig:
            valc[i] = avgc[i]
        elif _sw2 == chg_onLevel:
            valc[i] = (1 if (val[i] > fup[i]) else 2 if (val[i] < fdn[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        elif _sw2 == chg_onMiddle:
            valc[i] = (1 if (val[i] > mid[i]) else 2 if (val[i] < mid[i]) else (valc[i - 1] if (val[i] == val[i - 1]) else 0) if (i > 0) else 0)
        else:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iCorrMa(price, average, period, i, bars, instance=0):
    global _s_iCorrMa_m_arraySize
    if _s_iCorrMa_m_arraySize < bars:
        _s_iCorrMa_m_arraySize = ArrayResize(_s_iCorrMa_m_array, bars + 500)
        if _s_iCorrMa_m_arraySize <= bars:
            return 0.0
    _s_iCorrMa_m_array[i][instance].price = price
    _s_iCorrMa_m_array[i][instance].price2 = price * price
    if i > period:
        _s_iCorrMa_m_array[i][instance].summ = _s_iCorrMa_m_array[i - 1][instance].summ + price - _s_iCorrMa_m_array[i - period][instance].price
        _s_iCorrMa_m_array[i][instance].summ2 = _s_iCorrMa_m_array[i - 1][instance].summ2 + _s_iCorrMa_m_array[i][instance].price2 - _s_iCorrMa_m_array[i - period][instance].price2
    else:
        _s_iCorrMa_m_array[i][instance].summ = _s_iCorrMa_m_array[i][instance].price
        _s_iCorrMa_m_array[i][instance].summ2 = _s_iCorrMa_m_array[i][instance].price2
        k = 1
        while k < period and i >= k:
            _s_iCorrMa_m_array[i][instance].summ += _s_iCorrMa_m_array[i - k][instance].price
            _s_iCorrMa_m_array[i][instance].summ2 += _s_iCorrMa_m_array[i - k][instance].price2
            k += 1
    if i > 0:
        v1 = _fdiv(_s_iCorrMa_m_array[i][instance].summ2 - _fdiv(_s_iCorrMa_m_array[i][instance].summ * _s_iCorrMa_m_array[i][instance].summ, float(period)), float(period))
        v2 = (_s_iCorrMa_m_array[i - 1][instance].corrected - average) * (_s_iCorrMa_m_array[i - 1][instance].corrected - average)
        c = (0 if (v2 < v1 or v2 == 0) else (1.0 - _fdiv(v1, v2)))
        _s_iCorrMa_m_array[i][instance].corrected = _s_iCorrMa_m_array[i - 1][instance].corrected + (c * (average - _s_iCorrMa_m_array[i - 1][instance].corrected))
    else:
        _s_iCorrMa_m_array[i][instance].corrected = average
    return _s_iCorrMa_m_array[i][instance].corrected

# ---- global variables initialised from expressions
iVolatilityRatio = _alloc(cStdDevVolatilityRatio)
iVolatilityRatio.__init__()

# ---- static local variables
_s_OnCalculate_prev_i = -1
_s_OnCalculate_prev_max = 0.0
_s_OnCalculate_prev_min = 0.0
_s_iCorrMa_m_array = Arr(0, 0, factory=sCorrMaStruct, dims=(1,))
_s_iCorrMa_m_arraySize = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CorrWilderEMAFlVra(_MQL5Indicator):
    name = 'Corr Wilder EMA (fl)(vra)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Average period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpCorrectionPeriod': 0,  # "Correction" period (<0 no correction,0 to 1 same as average)
        'inpColorOn': _Choice({0: 'change color on slope change', 1: 'Change color on outer levels cross', 2: 'Change color on middle level cross', 3: 'Change color on average value cross'}, default=1),  # Color change on :
        'inpFlPeriod': 25,  # Period for finding floating levels
        'inpFlUp': 90.0,  # Upper level %
        'inpFlDown': 10.0,  # Lower level %
    }

