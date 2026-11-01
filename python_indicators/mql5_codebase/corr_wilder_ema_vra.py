"""Corr Wilder EMA (vra) — converted from MQL5: MQL5 Indicators/Corrected volatility ratio adaptive double smoothed Wilders eEMA/Corr Wilder EMA (vra).mq5

Corrected double smoothed Wilder's EMA volatility ratio adaptive
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 8, 2: 8}, 'colors': {1: [12632256, 7451452, 17919], 2: [12632256, 7451452, 17919]}, 'widths': {2: 3}, 'styles': {}, 'labels': {1: 'Corrected average original', 2: 'Corrected average '}, 'levels': [], 'description': ["Corrected double smoothed Wilder's EMA volatility ratio adaptive"], 'name': 'Corr Wilder EMA (vra)', 'source': 'MQL5 Indicators/Corrected volatility ratio adaptive double smoothed Wilders eEMA/Corr Wilder EMA (vra).mq5', 'folder': 'Corrected volatility ratio adaptive double smoothed Wilders eEMA', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Average period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpCorrectionPeriod', 'py': 'inpCorrectionPeriod', 'param': 'inpCorrectionPeriod', 'type': 'int', 'default': 0, 'label': '"Correction" period (<0 no correction,0 to 1 same as average)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Average period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpCorrectionPeriod = _input('inpCorrectionPeriod', 0)  # "Correction" period (<0 no correction,0 to 1 same as average)
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
avg = Arr(0, 0.0)
avgc = Arr(0, 0.0)
avgw = Arr(0, 0.0)
ª_maPeriod = 0
ª_corrPeriod = 0
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
    global ª_corrPeriod, ª_maPeriod
    SetIndexBuffer(0, avg, INDICATOR_DATA)
    SetIndexBuffer(1, avgc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, avgw, INDICATOR_CALCULATIONS)
    ª_corrPeriod = (inpCorrectionPeriod if (inpCorrectionPeriod > 0) else 0 if (inpCorrectionPeriod < 0) else inpPeriod)
    ª_maPeriod = (inpPeriod if (inpPeriod > 1) else 1)
    iVolatilityRatio.init(inpPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, '"Corrected" Wilder\'s EMA (vra)(' + _str(inpPeriod) + ',' + _str(inpCorrectionPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _alpha
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
        valc[i] = (1 if (avg[i] > val[i]) else 2 if (avg[i] < val[i]) else 0)
        avgc[i] = valc[i]
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
_s_iCorrMa_m_array = Arr(0, 0, factory=sCorrMaStruct, dims=(1,))
_s_iCorrMa_m_arraySize = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CorrWilderEMAVra(_MQL5Indicator):
    name = 'Corr Wilder EMA (vra)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Average period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpCorrectionPeriod': 0,  # "Correction" period (<0 no correction,0 to 1 same as average)
    }

