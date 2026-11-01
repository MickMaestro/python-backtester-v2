"""BB stops 2 - MACD — converted from MQL5: MQL5 Indicators/BB stops 2 - MACD/BB stops 2 - MACD.mq5

Bollinger bands stops - MACD based with multiple stops
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 8}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'colors': {1: [16748574], 2: [6333684], 3: [16748574], 4: [6333684], 5: [16748574], 6: [6333684], 7: [17919], 8: [6908265]}, 'widths': {1: 3, 2: 3}, 'styles': {7: 2, 8: 2}, 'labels': {1: 'Bollinger bands stops up stop line', 2: 'Bollinger bands stops down stop line', 3: 'Bollinger bands stops up first stop line', 4: 'Bollinger bands stops down first stop line', 5: 'Bollinger bands stops up second stop line', 6: 'Bollinger bands stops down second stop line', 7: 'MACD', 8: 'Macd signal'}, 'levels': [], 'description': ['Bollinger bands stops - MACD based with multiple stops'], 'name': 'BB stops 2 - MACD', 'source': 'MQL5 Indicators/BB stops 2 - MACD/BB stops 2 - MACD.mq5', 'folder': 'BB stops 2 - MACD', 'inputs': [{'mql': 'inpMacdFastPeriod', 'py': 'inpMacdFastPeriod', 'param': 'inpMacdFastPeriod', 'type': 'int', 'default': 12, 'label': 'Fast MACD period', 'sinput': False}, {'mql': 'inpMacdSlowPeriod', 'py': 'inpMacdSlowPeriod', 'param': 'inpMacdSlowPeriod', 'type': 'int', 'default': 26, 'label': 'Slow MACD period', 'sinput': False}, {'mql': 'inpMacdSignPeriod', 'py': 'inpMacdSignPeriod', 'param': 'inpMacdSignPeriod', 'type': 'int', 'default': 9, 'label': 'Signal MACD period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'MACD Price', 'sinput': False}, {'mql': 'inpDevPeriod', 'py': 'inpDevPeriod', 'param': 'inpDevPeriod', 'type': 'int', 'default': 0, 'label': 'Deviation period (<=1 for same as fast MACD period)', 'sinput': False}, {'mql': 'inpDeviation', 'py': 'inpDeviation', 'param': 'inpDeviation', 'type': 'double', 'default': 2.0, 'label': 'Deviation multiplier', 'sinput': False}, {'mql': '__º__01_00', 'py': '__º__01_00', 'param': None, 'type': 'string', 'default': '', 'label': '.', 'sinput': False}, {'mql': '__º__01_01', 'py': '__º__01_01', 'param': None, 'type': 'string', 'default': '', 'label': 'Risk settings', 'sinput': False}, {'mql': '__º__01_02', 'py': '__º__01_02', 'param': None, 'type': 'string', 'default': '', 'label': '.', 'sinput': False}, {'mql': 'inpRisk', 'py': 'inpRisk', 'param': 'inpRisk', 'type': 'double', 'default': 0.75, 'label': 'Risk multiplier', 'sinput': False}, {'mql': 'inpRisk2', 'py': 'inpRisk2', 'param': 'inpRisk2', 'type': 'double', 'default': 1.5, 'label': 'Risk 2 multiplier', 'sinput': False}, {'mql': 'inpRisk3', 'py': 'inpRisk3', 'param': 'inpRisk3', 'type': 'double', 'default': 2.5, 'label': 'Risk 3 multiplier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpMacdFastPeriod = _input('inpMacdFastPeriod', 12)  # Fast MACD period
inpMacdSlowPeriod = _input('inpMacdSlowPeriod', 26)  # Slow MACD period
inpMacdSignPeriod = _input('inpMacdSignPeriod', 9)  # Signal MACD period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # MACD Price
inpDevPeriod = _input('inpDevPeriod', 0)  # Deviation period (<=1 for same as fast MACD period)
inpDeviation = _input('inpDeviation', 2.0)  # Deviation multiplier
__º__01_00 = _input('__º__01_00', '')  # .
__º__01_01 = _input('__º__01_01', '')  # Risk settings
__º__01_02 = _input('__º__01_02', '')  # .
inpRisk = _input('inpRisk', 0.75)  # Risk multiplier
inpRisk2 = _input('inpRisk2', 1.5)  # Risk 2 multiplier
inpRisk3 = _input('inpRisk3', 2.5)  # Risk 3 multiplier
lineup = Arr(0, 0.0)
linedn = Arr(0, 0.0)
lineup2 = Arr(0, 0.0)
linedn2 = Arr(0, 0.0)
lineup3 = Arr(0, 0.0)
linedn3 = Arr(0, 0.0)
macd = Arr(0, 0.0)
signal = Arr(0, 0.0)

class CEma(MqlObject):
    _q_fields = ('m_period', 'm_alpha', 'm_array', 'm_arraySize')
    def __init__(self):
        self.m_period = 0.0
        self.m_alpha = 0.0
        self.m_array = Arr(0, 0.0)
        self.m_arraySize = 0
        self.m_period = 1.0
        self.m_alpha = 1.0
        self.m_arraySize = -1
        return
    def _q_dtor(self):
        return
    def init(self, period):
        self.m_period = (period if (period > 1) else 1)
        self.m_alpha = _fdiv(2.0, 1.0 + self.m_period)
    def calculate(self, value, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        self.m_array[i] = value
        if i > 0:
            self.m_array[i] = self.m_array[i - 1] + (self.m_alpha * (value - self.m_array[i - 1]))
        else:
            self.m_array[i] = value
        return self.m_array[i]

class CEmaDeviation(MqlObject):
    _q_fields = ('m_period', 'm_divisor', 'm_alpha', 'm_workSize', 'm_work')
    def __init__(self):
        self.m_period = 0.0
        self.m_divisor = 0.0
        self.m_alpha = 0.0
        self.m_workSize = 0
        self.m_work = Arr(32, 0, dyn=False, factory=sEmaDeviationStruct)
        self.init(1.0)
    def _q_dtor(self):
        pass
    def init(self, period):
        self.m_period = (period if (period > 1) else 1)
        self.m_divisor = ((self.m_period - 1) if (self.m_period > 2) else 1)
        self.m_alpha = _fdiv(2.0, 2.0 + ((period - 1.0) / 2.0))
        return True
    def calculate(self, price, i):
        _indC = _imod(i, 32)
        if i > 0:
            _indP = _imod(i - 1, 32)
            self.m_work[_indC].ema0 = self.m_work[_indP].ema0 + (self.m_alpha * (price - self.m_work[_indP].ema0))
            self.m_work[_indC].ema1 = self.m_work[_indP].ema1 + (self.m_alpha * ((price * price) - self.m_work[_indP].ema1))
        else:
            self.m_work[_indC].ema1 = price
            self.m_work[_indC].ema0 = self.m_work[_indC].ema1
        return MathSqrt(_fdiv(self.m_period * (self.m_work[_indC].ema1 - (self.m_work[_indC].ema0 * self.m_work[_indC].ema0)), self.m_divisor))

class sEmaDeviationStruct(MqlObject):
    _q_fields = ('ema0', 'ema1')
    def __init__(self, *args):
        self.ema0 = 0.0
        self.ema1 = 0.0

class CBbStops(MqlObject):
    _q_fields = ('m_devPeriod', 'm_devMultiplier', 'm_risk1', 'm_risk2', 'm_risk3', 'm_emaDeviation', 'm_work')
    _q_ptrs = ('m_emaDeviation',)
    def __init__(self):
        self.m_devPeriod = 0
        self.m_devMultiplier = 0.0
        self.m_risk1 = 0.0
        self.m_risk2 = 0.0
        self.m_risk3 = 0.0
        self.m_emaDeviation = None
        self.m_work = Arr(32, 0, dyn=False, factory=sBbStopsStruct)
        self.init(1, 1.0, 1.0, 1.0, 1.0)
    def _q_dtor(self):
        if CheckPointer(self.m_emaDeviation) == POINTER_DYNAMIC:
            _delete(self.m_emaDeviation)
    def init(self, devPeriod, devMultiplier, risk1, risk2, risk3):
        if CheckPointer(self.m_emaDeviation) != POINTER_DYNAMIC:
            self.m_emaDeviation = CEmaDeviation()
        if CheckPointer(self.m_emaDeviation) != POINTER_DYNAMIC:
            return False
        self.m_devPeriod = (devPeriod if (devPeriod > 1) else 1)
        self.m_devMultiplier = (devMultiplier if (devMultiplier > 0) else 0)
        self.m_emaDeviation.init(self.m_devPeriod)
        self.m_risk1 = risk1
        self.m_risk2 = risk2
        self.m_risk3 = risk3
        return True
    def calculate(self, value, average, i, result):
        _indC = _imod(i, 32)
        _indP = _imod(i - 1, 32)
        deviation = self.m_emaDeviation.calculate(value, i)
        self.m_work[_indC].amax = average + (self.m_devMultiplier * deviation)
        self.m_work[_indC].amin = average - (self.m_devMultiplier * deviation)
        self.m_work[_indC].bmax = average + (self.m_risk1 * deviation)
        self.m_work[_indC].bmin = average - (self.m_risk1 * deviation)
        self.m_work[_indC].cmax = average + (self.m_risk2 * deviation)
        self.m_work[_indC].cmin = average - (self.m_risk2 * deviation)
        self.m_work[_indC].dmax = average + (self.m_risk3 * deviation)
        self.m_work[_indC].dmin = average - (self.m_risk3 * deviation)
        if i > 0:
            self.m_work[_indC].trend = (1 if (value > self.m_work[_indP].amax) else -1 if (value < self.m_work[_indP].amin) else self.m_work[_indP].trend)
            if self.m_work[_indC].trend == -1:
                if self.m_work[_indC].amax > self.m_work[_indP].amax:
                    self.m_work[_indC].amax = self.m_work[_indP].amax
                if self.m_work[_indC].bmax > self.m_work[_indP].bmax:
                    self.m_work[_indC].bmax = self.m_work[_indP].bmax
                if self.m_work[_indC].cmax > self.m_work[_indP].cmax:
                    self.m_work[_indC].cmax = self.m_work[_indP].cmax
                if self.m_work[_indC].dmax > self.m_work[_indP].dmax:
                    self.m_work[_indC].dmax = self.m_work[_indP].dmax
                result[4] = EMPTY_VALUE
                result[2] = result[4]
                result[0] = result[2]
                result[1] = self.m_work[_indC].bmax
                result[3] = self.m_work[_indC].cmax
                result[5] = self.m_work[_indC].dmax
            if self.m_work[_indC].trend == 1:
                if self.m_work[_indC].amin < self.m_work[_indP].amin:
                    self.m_work[_indC].amin = self.m_work[_indP].amin
                if self.m_work[_indC].bmin < self.m_work[_indP].bmin:
                    self.m_work[_indC].bmin = self.m_work[_indP].bmin
                if self.m_work[_indC].cmin < self.m_work[_indP].cmin:
                    self.m_work[_indC].cmin = self.m_work[_indP].cmin
                if self.m_work[_indC].dmin < self.m_work[_indP].dmin:
                    self.m_work[_indC].dmin = self.m_work[_indP].dmin
                result[5] = EMPTY_VALUE
                result[3] = result[5]
                result[1] = result[3]
                result[0] = self.m_work[_indC].bmin
                result[2] = self.m_work[_indC].cmin
                result[4] = self.m_work[_indC].dmin
            result[6] = self.m_work[_indC].trend != self.m_work[_indP].trend
        else:
            result[6] = 0.0
            self.m_work[_indC].trend = result[6]
        result[7] = self.m_work[_indC].trend

class sBbStopsStruct(MqlObject):
    _q_fields = ('amax', 'amin', 'bmax', 'bmin', 'cmax', 'cmin', 'dmax', 'dmin', 'trend')
    def __init__(self, *args):
        self.amax = 0.0
        self.amin = 0.0
        self.bmax = 0.0
        self.bmin = 0.0
        self.cmax = 0.0
        self.cmin = 0.0
        self.dmax = 0.0
        self.dmin = 0.0
        self.trend = 0.0

def OnInit():
    SetIndexBuffer(0, lineup, INDICATOR_DATA)
    SetIndexBuffer(1, linedn, INDICATOR_DATA)
    SetIndexBuffer(2, lineup2, INDICATOR_DATA)
    SetIndexBuffer(3, linedn2, INDICATOR_DATA)
    SetIndexBuffer(4, lineup3, INDICATOR_DATA)
    SetIndexBuffer(5, linedn3, INDICATOR_DATA)
    SetIndexBuffer(6, macd, INDICATOR_DATA)
    SetIndexBuffer(7, signal, INDICATOR_DATA)
    _risks = Arr(3, 0.0, dyn=False)
    _risks[0] = inpRisk
    _risks[1] = inpRisk2
    _risks[2] = inpRisk3
    ArraySort(_risks)
    _devPeriod = (inpDevPeriod if (inpDevPeriod > 1) else inpMacdFastPeriod)
    iEmaFast.init(inpMacdFastPeriod)
    iEmaSlow.init(inpMacdSlowPeriod)
    iEmaSignal.init(inpMacdSignPeriod)
    iBbStops.init(_devPeriod, inpDeviation, _risks[0], _risks[1], _risks[2])
    IndicatorSetString(INDICATOR_SHORTNAME, 'BB stops 1 MACD (' + _str(inpMacdFastPeriod) + ',' + _str(inpMacdSlowPeriod) + ',' + _str(inpMacdSignPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _price = getPrice(inpPrice, open, high, low, close, i)
        macd[i] = iEmaFast.calculate(_price, i, rates_total) - iEmaSlow.calculate(_price, i, rates_total)
        signal[i] = iEmaSignal.calculate(macd[i], i, rates_total)
        iBbStops.calculate(macd[i], signal[i], i, _s_OnCalculate__results)
        lineup[i] = _s_OnCalculate__results[4]
        linedn[i] = _s_OnCalculate__results[5]
        lineup2[i] = _s_OnCalculate__results[0]
        linedn2[i] = _s_OnCalculate__results[1]
        lineup3[i] = _s_OnCalculate__results[2]
        linedn3[i] = _s_OnCalculate__results[3]
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
iEmaFast = _alloc(CEma)
iEmaFast.__init__()
iEmaSlow = _alloc(CEma)
iEmaSlow.__init__()
iEmaSignal = _alloc(CEma)
iEmaSignal.__init__()
iBbStops = _alloc(CBbStops)
iBbStops.__init__()

# ---- static local variables
_s_OnCalculate__results = Arr.of([EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE, EMPTY_VALUE], fill=0.0, dyn=False, size=8)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BBStops2MACD(_MQL5Indicator):
    name = 'BB stops 2 - MACD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpMacdFastPeriod': 12,  # Fast MACD period
        'inpMacdSlowPeriod': 26,  # Slow MACD period
        'inpMacdSignPeriod': 9,  # Signal MACD period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MACD Price
        'inpDevPeriod': 0,  # Deviation period (<=1 for same as fast MACD period)
        'inpDeviation': 2.0,  # Deviation multiplier
        'inpRisk': 0.75,  # Risk multiplier
        'inpRisk2': 1.5,  # Risk 2 multiplier
        'inpRisk3': 2.5,  # Risk 3 multiplier
    }

