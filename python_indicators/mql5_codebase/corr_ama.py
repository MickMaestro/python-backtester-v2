"""Corr AMA — converted from MQL5: MQL5 Indicators/Corrected AMA/Corr AMA.mq5

Corrected AMA
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 8, 2: 8}, 'colors': {1: [12632256, 7451452, 17919], 2: [12632256, 7451452, 17919]}, 'widths': {2: 3}, 'styles': {}, 'labels': {1: 'Corrected AMA original', 2: 'Corrected AMA'}, 'levels': [], 'description': ['Corrected AMA'], 'name': 'Corr AMA', 'source': 'MQL5 Indicators/Corrected AMA/Corr AMA.mq5', 'folder': 'Corrected AMA', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Average period', 'sinput': False}, {'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 2, 'label': 'Fast end period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 30, 'label': 'Slow end period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpCorrectionPeriod', 'py': 'inpCorrectionPeriod', 'param': 'inpCorrectionPeriod', 'type': 'int', 'default': 0, 'label': '"Correction" period (<0 no correction,0 to 1 same as average)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Average period
inpFastPeriod = _input('inpFastPeriod', 2)  # Fast end period
inpSlowPeriod = _input('inpSlowPeriod', 30)  # Slow end period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpCorrectionPeriod = _input('inpCorrectionPeriod', 0)  # "Correction" period (<0 no correction,0 to 1 same as average)
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
avg = Arr(0, 0.0)
avgc = Arr(0, 0.0)
avgw = Arr(0, 0.0)
prices = Arr(0, 0.0)

class CCorrMa(MqlObject):
    _q_fields = ('m_period', 'm_array', 'm_arraySize')
    def __init__(self):
        self.m_period = 0
        self.m_array = Arr(0, 0, factory=sCorrMaStruct)
        self.m_arraySize = 0
        self.m_period = 1
        self.m_arraySize = -1
    def _q_dtor(self):
        pass
    def init(self, period):
        self.m_period = (period if (period > 1) else 1)
        return True
    def calculate(self, price, average, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize <= bars:
                return 0.0
        self.m_array[i].price = price
        self.m_array[i].price2 = price * price
        if i > self.m_period:
            self.m_array[i].summ = self.m_array[i - 1].summ + price - self.m_array[i - self.m_period].price
            self.m_array[i].summ2 = self.m_array[i - 1].summ2 + self.m_array[i].price2 - self.m_array[i - self.m_period].price2
        else:
            self.m_array[i].summ = self.m_array[i].price
            self.m_array[i].summ2 = self.m_array[i].price2
            k = 1
            while k < self.m_period and i >= k:
                self.m_array[i].summ += self.m_array[i - k].price
                self.m_array[i].summ2 += self.m_array[i - k].price2
                k += 1
        if i > 0:
            v1 = _fdiv(self.m_array[i].summ2 - _fdiv(self.m_array[i].summ * self.m_array[i].summ, float(self.m_period)), float(self.m_period))
            v2 = (self.m_array[i - 1].corrected - average) * (self.m_array[i - 1].corrected - average)
            c = (0 if (v2 < v1 or v2 == 0) else (1.0 - _fdiv(v1, v2)))
            self.m_array[i].corrected = self.m_array[i - 1].corrected + (c * (average - self.m_array[i - 1].corrected))
        else:
            self.m_array[i].corrected = average
        return self.m_array[i].corrected

class sCorrMaStruct(MqlObject):
    _q_fields = ('corrected', 'price', 'price2', 'summ', 'summ2')
    def __init__(self, *args):
        self.corrected = 0.0
        self.price = 0.0
        self.price2 = 0.0
        self.summ = 0.0
        self.summ2 = 0.0

class CAma(MqlObject):
    _q_fields = ('m_period', 'm_prev_i', 'm_fastEnd', 'm_slowEnd', 'm_prev_max', 'm_prev_min')
    def __init__(self):
        self.m_period = 0
        self.m_prev_i = 0
        self.m_fastEnd = 0.0
        self.m_slowEnd = 0.0
        self.m_prev_max = 0.0
        self.m_prev_min = 0.0
        self.m_period = 1
        self.m_fastEnd = 2.0 / 3.0
        self.m_slowEnd = 2.0 / 31.0
        return
    def _q_dtor(self):
        return
    def init(self, period, fastEnd, slowEnd):
        self.m_period = ((period + 1) if (period > 1) else 2)
        self.m_fastEnd = _fdiv(2.0, fastEnd + 1.0)
        self.m_slowEnd = _fdiv(2.0, slowEnd + 1.0)
        return True
    def calculate(self, value, target, arrayMax, arrayMin, i):
        if self.m_prev_i != i:
            self.m_prev_i = i
            start = i - self.m_period + 1
            if start < 0:
                start = 0
            self.m_prev_max = arrayMax[ArrayMaximum(arrayMax, start, self.m_period - 1)]
            self.m_prev_min = arrayMin[ArrayMinimum(arrayMin, start, self.m_period - 1)]
        max_ = (arrayMax[i] if (arrayMax[i] > self.m_prev_max) else self.m_prev_max)
        min_ = (arrayMin[i] if (arrayMin[i] < self.m_prev_min) else self.m_prev_min)
        mltp = (_fdiv(value - min_ - (max_ - value), max_ - min_) if (max_ != min_) else 1)
        if mltp < 0:
            mltp *= -1
        ssc = (mltp * (self.m_fastEnd - self.m_slowEnd)) + self.m_slowEnd
        _assign(target[i], ((target[i - 1] + (ssc * ssc * (value - target[i - 1]))) if (i > 0) else value))

def OnInit():
    SetIndexBuffer(0, avg, INDICATOR_DATA)
    SetIndexBuffer(1, avgc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, val, INDICATOR_DATA)
    SetIndexBuffer(3, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, avgw, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, prices, INDICATOR_CALCULATIONS)
    iAma.init(inpPeriod, inpFastPeriod, inpSlowPeriod)
    iCorrMa.init((inpCorrectionPeriod if (inpCorrectionPeriod > 0) else 0 if (inpCorrectionPeriod < 0) else inpPeriod))
    IndicatorSetString(INDICATOR_SHORTNAME, '"Corrected" AMA (' + _str(inpPeriod) + ',' + _str(inpCorrectionPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        prices[i] = getPrice(inpPrice, open, high, low, close, i)
        iAma.calculate(prices[i], avg, prices, prices, i)
        val[i] = iCorrMa.calculate(prices[i], avg[i], i, rates_total)
        valc[i] = (1 if (avg[i] > val[i]) else 2 if (avg[i] < val[i]) else 0)
        avgc[i] = valc[i]
        i += 1
    return i

def getPrice(tprice, open, high, low, close, i):
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

# ---- global variables initialised from expressions
iCorrMa = _alloc(CCorrMa)
iCorrMa.__init__()
iAma = _alloc(CAma)
iAma.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CorrAMA(_MQL5Indicator):
    name = 'Corr AMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Average period
        'inpFastPeriod': 2,  # Fast end period
        'inpSlowPeriod': 30,  # Slow end period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpCorrectionPeriod': 0,  # "Correction" period (<0 no correction,0 to 1 same as average)
    }

