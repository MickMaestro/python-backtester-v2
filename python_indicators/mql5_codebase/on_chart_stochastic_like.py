"""On chart stochastic (like) — converted from MQL5: MQL5 Indicators/On chart stochastic (like)/On chart stochastic (like).mq5

Copyright: © mladen, 2021; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2021', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 7, 2: 7, 3: 8}, 'colors': {1: [13628367], 2: [12052223], 3: [11119017, 3329330, 17919]}, 'widths': {3: 2}, 'styles': {}, 'labels': {1: 'Upper zone', 2: 'Lower zone', 3: 'Stoch (like)'}, 'levels': [], 'description': [], 'name': 'On chart stochastic (like)', 'source': 'MQL5 Indicators/On chart stochastic (like)/On chart stochastic (like).mq5', 'folder': 'On chart stochastic (like)', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 32, 'label': 'Period', 'sinput': False}, {'mql': 'inpSlowing', 'py': 'inpSlowing', 'param': 'inpSlowing', 'type': 'int', 'default': 3, 'label': 'Slowing', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 0, 'label': 'Price', 'sinput': False}, {'mql': 'inpLevelUp', 'py': 'inpLevelUp', 'param': 'inpLevelUp', 'type': 'double', 'default': 80.0, 'label': 'Upper level', 'sinput': False}, {'mql': 'inpLevelDn', 'py': 'inpLevelDn', 'param': 'inpLevelDn', 'type': 'double', 'default': 20.0, 'label': 'Lower level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enPrices
pr_close = 0
pr_open = 1
pr_high = 2
pr_low = 3
pr_median = 4
pr_typical = 5
pr_weighted = 6
pr_average = 7
pr_medianb = 8
pr_tbiased = 9
pr_tbiased2 = 10
pr_closeclose = 11
pr_highlow = 12
pr_haclose = 13
pr_haopen = 14
pr_hahigh = 15
pr_halow = 16
pr_hamedian = 17
pr_hatypical = 18
pr_haweighted = 19
pr_haaverage = 20
pr_hamedianb = 21
pr_hatbiased = 22
pr_hatbiased2 = 23
pr_habclose = 24
pr_habopen = 25
pr_habhigh = 26
pr_hablow = 27
pr_habmedian = 28
pr_habtypical = 29
pr_habweighted = 30
pr_habaverage = 31
pr_habmedianb = 32
pr_habtbiased = 33
pr_habtbiased2 = 34
_enum('enPrices', {0: 'pr_close', 1: 'pr_open', 2: 'pr_high', 3: 'pr_low', 4: 'pr_median', 5: 'pr_typical', 6: 'pr_weighted', 7: 'pr_average', 8: 'pr_medianb', 9: 'pr_tbiased', 10: 'pr_tbiased2', 11: 'pr_closeclose', 12: 'pr_highlow', 13: 'pr_haclose', 14: 'pr_haopen', 15: 'pr_hahigh', 16: 'pr_halow', 17: 'pr_hamedian', 18: 'pr_hatypical', 19: 'pr_haweighted', 20: 'pr_haaverage', 21: 'pr_hamedianb', 22: 'pr_hatbiased', 23: 'pr_hatbiased2', 24: 'pr_habclose', 25: 'pr_habopen', 26: 'pr_habhigh', 27: 'pr_hablow', 28: 'pr_habmedian', 29: 'pr_habtypical', 30: 'pr_habweighted', 31: 'pr_habaverage', 32: 'pr_habmedianb', 33: 'pr_habtbiased', 34: 'pr_habtbiased2'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32)  # Period
inpSlowing = _input('inpSlowing', 3)  # Slowing
inpPrice = _input('inpPrice', pr_close)  # Price
inpLevelUp = _input('inpLevelUp', 80.0)  # Upper level
inpLevelDn = _input('inpLevelDn', 20.0)  # Lower level
fupu = Arr(0, 0.0)
fupd = Arr(0, 0.0)
fdnd = Arr(0, 0.0)
fdnu = Arr(0, 0.0)
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

class sGlobalStruct(MqlObject):
    _q_fields = ('period', 'slowing', 'levelUp', 'levelDn')
    def __init__(self, *args):
        self.period = 0
        self.slowing = 0
        self.levelUp = 0.0
        self.levelDn = 0.0

class sWorkStruct(MqlObject):
    _q_fields = ('sto', 'stoSum', 'prevBar', 'prevMin', 'prevMax')
    def __init__(self):
        self.sto = 0.0
        self.stoSum = 0.0
        self.prevBar = 0
        self.prevMin = 0.0
        self.prevMax = 0.0
        self.prevBar = -1

class sHaStruct(MqlObject):
    _q_fields = ('open', 'high', 'low', 'close')
    def __init__(self, *args):
        self.open = 0.0
        self.high = 0.0
        self.low = 0.0
        self.close = 0.0

def OnInit():
    SetIndexBuffer(0, fupu, INDICATOR_DATA)
    SetIndexBuffer(1, fupd, INDICATOR_DATA)
    SetIndexBuffer(2, fdnu, INDICATOR_DATA)
    SetIndexBuffer(3, fdnd, INDICATOR_DATA)
    SetIndexBuffer(4, val, INDICATOR_DATA)
    SetIndexBuffer(5, valc, INDICATOR_COLOR_INDEX)
    global_.period = MathMax(inpPeriod, 1)
    global_.slowing = MathMax(inpSlowing, 1)
    global_.levelUp = MathMin(MathMax(inpLevelUp, inpLevelDn), 100)
    global_.levelDn = MathMax(MathMin(inpLevelUp, inpLevelDn), 0)
    if inpSlowing < 1:
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_workSize
    limit = prev_calculated - 1
    if limit < 0:
        limit = 0
    if _s_OnCalculate_m_workSize <= rates_total:
        _s_OnCalculate_m_workSize = ArrayResize(_s_OnCalculate_m_work, rates_total + 500, 2000)
    for i in range(limit, rates_total):
        if _s_OnCalculate_m_work[i].prevBar != i or _s_OnCalculate_m_work[i + 1].prevBar >= i:
            _s_OnCalculate_m_work[i].prevBar = i
            _s_OnCalculate_m_work[i + 1].prevBar = -1
            if i > 0 and global_.period > 1:
                _minMaxPeriod = global_.period - 1
                _start = i - global_.period + 1
                if _start < 0:
                    _start = 0
                    _minMaxPeriod = i
                _s_OnCalculate_m_work[i].prevMax = high[ArrayMaximum(high, _start, _minMaxPeriod)]
                _s_OnCalculate_m_work[i].prevMin = low[ArrayMinimum(low, _start, _minMaxPeriod)]
            else:
                _s_OnCalculate_m_work[i].prevMin = low[i]
                _s_OnCalculate_m_work[i].prevMax = high[i]
        _min = (_s_OnCalculate_m_work[i].prevMin if (_s_OnCalculate_m_work[i].prevMin < low[i]) else low[i])
        _max = (_s_OnCalculate_m_work[i].prevMax if (_s_OnCalculate_m_work[i].prevMax > high[i]) else high[i])
        _rng = _max - _min
        _prc = iGetPrice(inpPrice, open, high, low, close, i, rates_total)
        fdnd[i] = _min
        fdnu[i] = _min + ((_rng * global_.levelDn) / 100.0)
        fupu[i] = _max
        fupd[i] = _min + ((_rng * global_.levelUp) / 100.0)
        _s_OnCalculate_m_work[i].sto = (_fdiv(_prc - _min, _max - _min) if (_max != _min) else 0)
        if i >= global_.slowing:
            _s_OnCalculate_m_work[i].stoSum = _s_OnCalculate_m_work[i - 1].stoSum + _s_OnCalculate_m_work[i].sto - _s_OnCalculate_m_work[i - global_.slowing].sto
        else:
            _s_OnCalculate_m_work[i].stoSum = _s_OnCalculate_m_work[i].sto
            k = 1
            while k < global_.slowing and i >= k:
                _s_OnCalculate_m_work[i].stoSum += _s_OnCalculate_m_work[i - k].sto
                k += 1
        val[i] = _min + _fdiv(_rng * _s_OnCalculate_m_work[i].stoSum, float(global_.slowing))
        valc[i] = (1 if (val[i] >= fupd[i]) else 2 if (val[i] <= fdnu[i]) else 0)
    return rates_total

def iGetPrice(tprice, open, high, low, close, i, bars):
    global _s_iGetPrice_m_arraySize
    if tprice >= pr_haclose:
        if _s_iGetPrice_m_arraySize < bars:
            _s_iGetPrice_m_arraySize = ArrayResize(_s_iGetPrice_m_array, bars + 500)
        r = i
        haOpen = (((_s_iGetPrice_m_array[r - 1].open + _s_iGetPrice_m_array[r - 1].close) / 2.0) if (r > 0) else ((open[i] + close[i]) / 2))
        haClose = (open[i] + high[i] + low[i] + close[i]) / 4.0
        if tprice >= pr_habclose and tprice <= pr_habtbiased2:
            if high[i] != low[i]:
                haClose = ((open[i] + close[i]) / 2.0) + (_fdiv(close[i] - open[i], high[i] - low[i]) * MathAbs((close[i] - open[i]) / 2.0))
            else:
                haClose = (open[i] + close[i]) / 2.0
        haHigh = fmax(high[i], fmax(haOpen, haClose))
        haLow = fmin(low[i], fmin(haOpen, haClose))
        if haOpen < haClose:
            _s_iGetPrice_m_array[r].high = haLow
            _s_iGetPrice_m_array[r].low = haHigh
        else:
            _s_iGetPrice_m_array[r].high = haHigh
            _s_iGetPrice_m_array[r].low = haLow
        _s_iGetPrice_m_array[r].open = haOpen
        _s_iGetPrice_m_array[r].close = haClose
        _sw1 = tprice
        if _sw1 in (pr_haclose, pr_habclose):
            return haClose
        elif _sw1 in (pr_haopen, pr_habopen):
            return haOpen
        elif _sw1 in (pr_hahigh, pr_habhigh):
            return haHigh
        elif _sw1 in (pr_halow, pr_hablow):
            return haLow
        elif _sw1 in (pr_hamedian, pr_habmedian):
            return (haHigh + haLow) / 2.0
        elif _sw1 in (pr_hamedianb, pr_habmedianb):
            return (haOpen + haClose) / 2.0
        elif _sw1 in (pr_hatypical, pr_habtypical):
            return (haHigh + haLow + haClose) / 3.0
        elif _sw1 in (pr_haweighted, pr_habweighted):
            return (haHigh + haLow + haClose + haClose) / 4.0
        elif _sw1 in (pr_haaverage, pr_habaverage):
            return (haHigh + haLow + haClose + haOpen) / 4.0
        elif _sw1 in (pr_hatbiased, pr_habtbiased):
            if haClose > haOpen:
                return (haHigh + haClose) / 2.0
            else:
                return (haLow + haClose) / 2.0
        elif _sw1 in (pr_hatbiased2, pr_habtbiased2):
            if haClose > haOpen:
                return haHigh
            if haClose < haOpen:
                return haLow
            return haClose
    _sw2 = tprice
    if _sw2 == pr_close:
        return close[i]
    elif _sw2 == pr_open:
        return open[i]
    elif _sw2 == pr_high:
        return high[i]
    elif _sw2 == pr_low:
        return low[i]
    elif _sw2 == pr_median:
        return (high[i] + low[i]) / 2.0
    elif _sw2 == pr_medianb:
        return (open[i] + close[i]) / 2.0
    elif _sw2 == pr_typical:
        return (high[i] + low[i] + close[i]) / 3.0
    elif _sw2 == pr_weighted:
        return (high[i] + low[i] + close[i] + close[i]) / 4.0
    elif _sw2 == pr_average:
        return (high[i] + low[i] + close[i] + open[i]) / 4.0
    elif _sw2 == pr_tbiased:
        if close[i] > open[i]:
            return (high[i] + close[i]) / 2.0
        else:
            return (low[i] + close[i]) / 2.0
    elif _sw2 == pr_tbiased2:
        if close[i] > open[i]:
            return high[i]
        if close[i] < open[i]:
            return low[i]
        return close[i]
    return 0.0

# ---- global variables initialised from expressions
global_ = _alloc(sGlobalStruct)
global_.__init__()

# ---- static local variables
_s_OnCalculate_m_work = Arr(0, 0, factory=sWorkStruct)
_s_OnCalculate_m_workSize = -1
_s_iGetPrice_m_array = Arr(0, 0, factory=sHaStruct)
_s_iGetPrice_m_arraySize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class OnChartStochasticLike(_MQL5Indicator):
    name = 'On chart stochastic (like)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 32,  # Period
        'inpSlowing': 3,  # Slowing
        'inpPrice': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted', 7: 'Average (high+low+open+close)/4', 8: 'Average median body (open+close)/2', 9: 'Trend biased price', 10: 'Trend biased (extreme) price', 11: 'Close/close', 12: 'High/Low', 13: 'Heiken ashi close', 14: 'Heiken ashi open', 15: 'Heiken ashi high', 16: 'Heiken ashi low', 17: 'Heiken ashi median', 18: 'Heiken ashi typical', 19: 'Heiken ashi weighted', 20: 'Heiken ashi average', 21: 'Heiken ashi median body', 22: 'Heiken ashi trend biased price', 23: 'Heiken ashi trend biased (extreme) price', 24: 'Heiken ashi (better formula) close', 25: 'Heiken ashi (better formula) open', 26: 'Heiken ashi (better formula) high', 27: 'Heiken ashi (better formula) low', 28: 'Heiken ashi (better formula) median', 29: 'Heiken ashi (better formula) typical', 30: 'Heiken ashi (better formula) weighted', 31: 'Heiken ashi (better formula) average', 32: 'Heiken ashi (better formula) median body', 33: 'Heiken ashi (better formula) trend biased price', 34: 'Heiken ashi (better formula) trend biased (extreme) price'}, default=0),  # Price
        'inpLevelUp': 80.0,  # Upper level
        'inpLevelDn': 20.0,  # Lower level
    }

