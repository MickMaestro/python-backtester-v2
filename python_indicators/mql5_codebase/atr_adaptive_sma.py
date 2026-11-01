"""ATR adaptive SMA — converted from MQL5: MQL5 Indicators/ATR adaptive SMA/ATR adaptive SMA.mq5

ATR adaptive SMA
Copyright: © mladen, 2020; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2020', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 34, 'indicator_plots': 2}, 'types': {1: 1, 2: 8}, 'colors': {1: [11119017], 2: [11119017, 9639167, 3329330]}, 'widths': {1: 0, 2: 2}, 'styles': {}, 'labels': {1: 'SMA', 2: 'Adaptive SMA'}, 'levels': [], 'description': ['ATR adaptive SMA'], 'name': 'ATR adaptive SMA', 'source': 'MQL5 Indicators/ATR adaptive SMA/ATR adaptive SMA.mq5', 'folder': 'ATR adaptive SMA', 'inputs': [{'mql': 'inpMaPeriod', 'py': 'inpMaPeriod', 'param': 'inpMaPeriod', 'type': 'int', 'default': 25, 'label': 'SMA period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpColorMode', 'py': 'inpColorMode', 'param': 'inpColorMode', 'type': 'int', 'default': 1, 'label': 'Color change mode', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorMode
col_onSlope = 0
col_onCross = 1
_enum('enColorMode', {0: 'col_onSlope', 1: 'col_onCross'})

# ---- inputs and global variables
inpMaPeriod = _input('inpMaPeriod', 25)  # SMA period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpColorMode = _input('inpColorMode', col_onCross)  # Color change mode
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
sma = Arr(0, 0.0)
atr = Arr(0, 0.0)

class sWorkStruct(MqlObject):
    _q_fields = ('price', 'tr', 'sumtr', 'min', 'max', 'sum', 'sumSma', 'period', 'prevBar')
    def __init__(self):
        self.price = 0.0
        self.tr = 0.0
        self.sumtr = 0.0
        self.min = 0.0
        self.max = 0.0
        self.sum = 0.0
        self.sumSma = 0.0
        self.period = 0
        self.prevBar = 0
        self.prevBar = -1
        self.period = INT_MIN

def OnInit():
    SetIndexBuffer(0, sma, INDICATOR_DATA)
    SetIndexBuffer(1, val, INDICATOR_DATA)
    SetIndexBuffer(2, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, atr, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ATR adaptive SMA (' + _str(inpMaPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_workSize
    limit = prev_calculated - 1
    if limit < 0:
        limit = 0
    if _s_OnCalculate_m_workSize <= rates_total:
        _s_OnCalculate_m_workSize = ArrayResize(_s_OnCalculate_m_work, rates_total + 500, 2000)
    for i in range(limit, rates_total):
        _s_OnCalculate_m_work[i].price = getPrice(inpPrice, open, high, low, close, i)
        _s_OnCalculate_m_work[i].tr = (((high[i] if (high[i] > close[i - 1]) else close[i - 1]) - (low[i] if (low[i] < close[i - 1]) else close[i - 1])) if (i > 0) else (high[i] - low[i]))
        if i > inpMaPeriod:
            _s_OnCalculate_m_work[i].sumSma = _s_OnCalculate_m_work[i - 1].sumSma + _s_OnCalculate_m_work[i].price - _s_OnCalculate_m_work[i - inpMaPeriod].price
            _s_OnCalculate_m_work[i].sumtr = _s_OnCalculate_m_work[i - 1].sumtr + _s_OnCalculate_m_work[i].tr - _s_OnCalculate_m_work[i - inpMaPeriod].tr
        else:
            _s_OnCalculate_m_work[i].sumSma = _s_OnCalculate_m_work[i].price
            k = 1
            while k < inpMaPeriod and i >= k:
                _s_OnCalculate_m_work[i].sumSma += _s_OnCalculate_m_work[i - k].price
                k += 1
            _s_OnCalculate_m_work[i].sumtr = _s_OnCalculate_m_work[i].tr
            k = 1
            while k < inpMaPeriod and i >= k:
                _s_OnCalculate_m_work[i].sumtr += _s_OnCalculate_m_work[i - k].tr
                k += 1
        atr[i] = _s_OnCalculate_m_work[i].sumtr / float(inpMaPeriod)
        sma[i] = NormalizeDouble(_s_OnCalculate_m_work[i].sumSma / float(inpMaPeriod), Digits())
        if _s_OnCalculate_m_work[i].prevBar != i or _s_OnCalculate_m_work[i + 1].prevBar > i:
            if inpMaPeriod > 1:
                _start = MathMax(i - inpMaPeriod + 1, 0)
                _s_OnCalculate_m_work[i].max = atr[ArrayMaximum(atr, _start, inpMaPeriod - 1)]
                _s_OnCalculate_m_work[i].min = atr[ArrayMinimum(atr, _start, inpMaPeriod - 1)]
            else:
                _s_OnCalculate_m_work[i].max = -DBL_MAX
                _s_OnCalculate_m_work[i].min = DBL_MAX
        _max = (_s_OnCalculate_m_work[i].max if (_s_OnCalculate_m_work[i].max > atr[i]) else atr[i])
        _min = (_s_OnCalculate_m_work[i].min if (_s_OnCalculate_m_work[i].min < atr[i]) else atr[i])
        _coeff = ((1 - _fdiv(atr[i] - _min, _max - _min)) if (_min != _max) else 0.5)
        _period = _int((inpMaPeriod * (_coeff + 1.0)) / 2.0)
        if (_s_OnCalculate_m_work[i + 1].period != _period or _s_OnCalculate_m_work[i].prevBar != i) or _s_OnCalculate_m_work[i + 1].prevBar > i:
            _s_OnCalculate_m_work[i].prevBar = i
            _s_OnCalculate_m_work[i + 1].prevBar = -1
            _s_OnCalculate_m_work[i + 1].period = _period
            _s_OnCalculate_m_work[i].sum = 0.0
            k = 1
            while k < _period and i >= k:
                _s_OnCalculate_m_work[i].sum += _s_OnCalculate_m_work[i - k].price
                k += 1
        val[i] = (NormalizeDouble(_fdiv(_s_OnCalculate_m_work[i].sum + _s_OnCalculate_m_work[i].price, float(_period)), Digits()) if (_period > 0) else _s_OnCalculate_m_work[i].price)
        if inpColorMode == col_onSlope:
            valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        else:
            valc[i] = (2 if (val[i] > sma[i]) else 1 if (val[i] < sma[i]) else valc[i - 1] if (i > 0) else 0)
    return rates_total

def getPrice(priceType, open, high, low, close, i):
    _sw1 = priceType
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
_s_OnCalculate_m_work = Arr(0, 0, factory=sWorkStruct)
_s_OnCalculate_m_workSize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ATRAdaptiveSMA(_MQL5Indicator):
    name = 'ATR adaptive SMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpMaPeriod': 25,  # SMA period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpColorMode': _Choice({0: 'Change color on slope change', 1: 'Change color on two sma cross'}, default=1),  # Color change mode
    }

