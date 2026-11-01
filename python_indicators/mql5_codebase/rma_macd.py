"""Rma MACD — converted from MQL5: MQL5 Indicators/Rma MACD/Rma MACD.mq5

Rma MACD
Copyright: © mladen, 2019; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 8, 2: 8}, 'colors': {1: [16748574, 6333684], 2: [16748574, 6333684]}, 'widths': {1: 2}, 'styles': {2: 2}, 'labels': {1: 'Rma MACD', 2: 'Rma MACD signal line'}, 'levels': [], 'description': ['Rma MACD'], 'name': 'Rma MACD', 'source': 'MQL5 Indicators/Rma MACD/Rma MACD.mq5', 'folder': 'Rma MACD', 'inputs': [{'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 12, 'label': 'MACD fast period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 26, 'label': 'MACD slow period', 'sinput': False}, {'mql': 'inpSignalPeriod', 'py': 'inpSignalPeriod', 'param': 'inpSignalPeriod', 'type': 'int', 'default': 9, 'label': 'Signal period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpFastPeriod = _input('inpFastPeriod', 12)  # MACD fast period
inpSlowPeriod = _input('inpSlowPeriod', 26)  # MACD slow period
inpSignalPeriod = _input('inpSignalPeriod', 9)  # Signal period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
sig = Arr(0, 0.0)
sigc = Arr(0, 0.0)

class CRma(MqlObject):
    _q_fields = ('m_period1', 'm_period2', 'm_period3', 'm_array', 'm_arraySize')
    def __init__(self):
        self.m_period1 = 0
        self.m_period2 = 0
        self.m_period3 = 0
        self.m_array = Arr(0, 0, factory=sRmaStruct)
        self.m_arraySize = 0
        self.m_arraySize = -1
        self.m_period1 = 1
        self.m_period2 = 1
        self.m_period3 = 1
    def _q_dtor(self):
        pass
    def init(self, _period):
        self.m_period1 = (_period if (_period > 1) else 1)
        self.m_period2 = 2 * self.m_period1
        self.m_period3 = 3 * self.m_period1
    def calculate(self, value, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
        self.m_array[i].price = value
        if i > self.m_period1:
            self.m_array[i].summ1 = self.m_array[i - 1].summ1 + self.m_array[i].price - self.m_array[i - self.m_period1].price
        else:
            self.m_array[i].summ1 = self.m_array[i].price
            k = 1
            while k < self.m_period1 and i >= k:
                self.m_array[i].summ1 += self.m_array[i - k].price
                k += 1
        if i > self.m_period2:
            self.m_array[i].summ2 = self.m_array[i - 1].summ2 + self.m_array[i].price - self.m_array[i - self.m_period2].price
        else:
            self.m_array[i].summ2 = self.m_array[i].price
            k = 1
            while k < self.m_period2 and i >= k:
                self.m_array[i].summ2 += self.m_array[i - k].price
                k += 1
        if i > self.m_period3:
            self.m_array[i].summ3 = self.m_array[i - 1].summ3 + self.m_array[i].price - self.m_array[i - self.m_period3].price
        else:
            self.m_array[i].summ3 = self.m_array[i].price
            k = 1
            while k < self.m_period3 and i >= k:
                self.m_array[i].summ3 += self.m_array[i - k].price
                k += 1
        return _fdiv(self.m_array[i].summ3, float(self.m_period3)) - _fdiv(self.m_array[i].summ2, float(self.m_period2)) + _fdiv(self.m_array[i].summ1, float(self.m_period1))

class sRmaStruct(MqlObject):
    _q_fields = ('price', 'summ1', 'summ2', 'summ3')
    def __init__(self, *args):
        self.price = 0.0
        self.summ1 = 0.0
        self.summ2 = 0.0
        self.summ3 = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, sig, INDICATOR_DATA)
    SetIndexBuffer(3, sigc, INDICATOR_COLOR_INDEX)
    iRmaFast.init(inpFastPeriod)
    iRmaSlow.init(inpSlowPeriod)
    iRmaSignal.init(inpSignalPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('Rma MACD (%i,%i,%i)', inpFastPeriod, inpSlowPeriod, inpSignalPeriod))
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
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
        val[i] = iRmaFast.calculate(_price, i, rates_total) - iRmaSlow.calculate(_price, i, rates_total)
        sig[i] = iRmaSignal.calculate(val[i], i, rates_total)
        valc[i] = ((0 if (val[i] > val[i - 1]) else 1) if (i > 0) else 0)
        sigc[i] = (0 if (val[i] > sig[i]) else 1)
        i += 1
    return rates_total

# ---- global variables initialised from expressions
iRmaFast = _alloc(CRma)
iRmaFast.__init__()
iRmaSlow = _alloc(CRma)
iRmaSlow.__init__()
iRmaSignal = _alloc(CRma)
iRmaSignal.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RmaMACD(_MQL5Indicator):
    name = 'Rma MACD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFastPeriod': 12,  # MACD fast period
        'inpSlowPeriod': 26,  # MACD slow period
        'inpSignalPeriod': 9,  # Signal period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

