"""ATR adaptive smoothed Laguerre RSI 2 (no built in functions) — converted from MQL5: MQL5 Indicators/ATR adaptive smoothed Laguerre RSI (no built in functions)/ATR adaptive smoothed Laguerre RSI 2 (no built in functions).mq5

Copyright: © mladen 2021; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen 2021', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [8421504, 16748574, 4678655]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'ATR adaptive smoothed Laguerre RSI 2 (no built in functions)', 'source': 'MQL5 Indicators/ATR adaptive smoothed Laguerre RSI (no built in functions)/ATR adaptive smoothed Laguerre RSI 2 (no built in functions).mq5', 'folder': 'ATR adaptive smoothed Laguerre RSI (no built in functions)', 'inputs': [{'mql': 'inpAtrPeriod', 'py': 'inpAtrPeriod', 'param': 'inpAtrPeriod', 'type': 'int', 'default': 32, 'label': 'ATR period', 'sinput': False}, {'mql': 'inpRsiPrice', 'py': 'inpRsiPrice', 'param': 'inpRsiPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpRsiSmoothPeriod', 'py': 'inpRsiSmoothPeriod', 'param': 'inpRsiSmoothPeriod', 'type': 'double', 'default': 5.0, 'label': 'Price smoothing period', 'sinput': False}, {'mql': 'inpLevelUp', 'py': 'inpLevelUp', 'param': 'inpLevelUp', 'type': 'double', 'default': 0.85, 'label': 'Level up', 'sinput': False}, {'mql': 'inpLevelDown', 'py': 'inpLevelDown', 'param': 'inpLevelDown', 'type': 'double', 'default': 0.15, 'label': 'Level down', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpAtrPeriod = _input('inpAtrPeriod', 32)  # ATR period
inpRsiPrice = _input('inpRsiPrice', PRICE_CLOSE)  # Price
inpRsiSmoothPeriod = _input('inpRsiSmoothPeriod', 5.0)  # Price smoothing period
inpLevelUp = _input('inpLevelUp', 0.85)  # Level up
inpLevelDown = _input('inpLevelDown', 0.15)  # Level down
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

class sGlobalStruct(MqlObject):
    _q_fields = ('smoothPeriod',)
    def __init__(self, *args):
        self.smoothPeriod = 0.0

class sWorkStruct(MqlObject):
    _q_fields = ('tr', 'trSum', 'atr', 'prevMin', 'prevMax', 'saveBar')
    def __init__(self):
        self.tr = 0.0
        self.trSum = 0.0
        self.atr = 0.0
        self.prevMin = 0.0
        self.prevMax = 0.0
        self.saveBar = 0
        self.saveBar = -1

class sDataStruct(MqlObject):
    _q_fields = ('values', 'price')
    def __init__(self, *args):
        self.values = Arr(4, 0.0, dyn=False)
        self.price = 0.0

class sWorkStruct_iLaGuerreRsi(MqlObject):
    _q_fields = ('data',)
    def __init__(self, *args):
        self.data = Arr(1, 0, dyn=False, factory=sDataStruct)

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, inpLevelUp)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, inpLevelDown)
    global_.smoothPeriod = MathMax(inpRsiSmoothPeriod, 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ATR adaptive Laguerre RSI (' + _str(inpAtrPeriod) + ',' + _str(inpRsiSmoothPeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_workSize
    limit = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    if _s_OnCalculate_m_workSize <= rates_total:
        _s_OnCalculate_m_workSize = ArrayResize(_s_OnCalculate_m_work, rates_total + 500, 2000)
    for i in range(limit, rates_total):
        _s_OnCalculate_m_work[i].tr = (((high[i] if (high[i] > close[i - 1]) else close[i - 1]) - (low[i] if (low[i] < close[i - 1]) else close[i - 1])) if (i > 0) else (high[i] - low[i]))
        if i > inpAtrPeriod:
            _s_OnCalculate_m_work[i].trSum = _s_OnCalculate_m_work[i - 1].trSum + _s_OnCalculate_m_work[i].tr - _s_OnCalculate_m_work[i - inpAtrPeriod].tr
        else:
            _s_OnCalculate_m_work[i].trSum = _s_OnCalculate_m_work[i].tr
            k = 1
            while k < inpAtrPeriod and i >= k:
                _s_OnCalculate_m_work[i].trSum += _s_OnCalculate_m_work[i - k].tr
                k += 1
        _s_OnCalculate_m_work[i].atr = _s_OnCalculate_m_work[i].trSum / float(inpAtrPeriod)
        if _s_OnCalculate_m_work[i].saveBar != i or _s_OnCalculate_m_work[i + 1].saveBar >= i:
            _s_OnCalculate_m_work[i].saveBar = i
            _s_OnCalculate_m_work[i + 1].saveBar = -1
            if inpAtrPeriod > 1 and i > 0:
                _s_OnCalculate_m_work[i].prevMin = _s_OnCalculate_m_work[i - 1].atr
                _s_OnCalculate_m_work[i].prevMax = _s_OnCalculate_m_work[i].prevMin
                k = 2
                while k < inpAtrPeriod and i >= k:
                    if _s_OnCalculate_m_work[i - k].atr > _s_OnCalculate_m_work[i].prevMax:
                        _s_OnCalculate_m_work[i].prevMax = _s_OnCalculate_m_work[i - k].atr
                    if _s_OnCalculate_m_work[i - k].atr < _s_OnCalculate_m_work[i].prevMin:
                        _s_OnCalculate_m_work[i].prevMin = _s_OnCalculate_m_work[i - k].atr
                    k += 1
            else:
                _s_OnCalculate_m_work[i].prevMin = _s_OnCalculate_m_work[i].atr
                _s_OnCalculate_m_work[i].prevMax = _s_OnCalculate_m_work[i].prevMin
        _max = (_s_OnCalculate_m_work[i].prevMax if (_s_OnCalculate_m_work[i].prevMax > _s_OnCalculate_m_work[i].atr) else _s_OnCalculate_m_work[i].atr)
        _min = (_s_OnCalculate_m_work[i].prevMin if (_s_OnCalculate_m_work[i].prevMin < _s_OnCalculate_m_work[i].atr) else _s_OnCalculate_m_work[i].atr)
        _coeff = ((1.0 - _fdiv(_s_OnCalculate_m_work[i].atr - _min, _max - _min)) if (_min != _max) else 0.5)
        val[i] = iLaGuerreRsi(getPrice(inpRsiPrice, open, high, low, close, i), inpAtrPeriod * (_coeff + 0.75), global_.smoothPeriod, i, rates_total)
        valc[i] = (1 if (val[i] > inpLevelUp) else 2 if (val[i] < inpLevelDown) else 0)
    return rates_total

def iLaGuerreRsi(price, period, smoothPeriod, i, bars, instance=0):
    global _s_iLaGuerreRsi_m_workSize
    if _s_iLaGuerreRsi_m_workSize < bars:
        _s_iLaGuerreRsi_m_workSize = ArrayResize(_s_iLaGuerreRsi_m_work, bars + 500, 2000)
    CU = 0.0
    CD = 0.0
    if i > 0 and period > 1:
        _gamma = 1.0 - _fdiv(10.0, period + 9.0)
        _alpha = _fdiv(2.0, 1.0 + smoothPeriod)
        _s_iLaGuerreRsi_m_work[i].data[instance].price = _s_iLaGuerreRsi_m_work[i - 1].data[instance].price + (_alpha * (price - _s_iLaGuerreRsi_m_work[i - 1].data[instance].price))
        _s_iLaGuerreRsi_m_work[i].data[instance].values[0] = _s_iLaGuerreRsi_m_work[i].data[instance].price + (_gamma * (_s_iLaGuerreRsi_m_work[i - 1].data[instance].values[0] - _s_iLaGuerreRsi_m_work[i].data[instance].price))
        _s_iLaGuerreRsi_m_work[i].data[instance].values[1] = _s_iLaGuerreRsi_m_work[i - 1].data[instance].values[0] + (_gamma * (_s_iLaGuerreRsi_m_work[i - 1].data[instance].values[1] - _s_iLaGuerreRsi_m_work[i].data[instance].values[0]))
        _s_iLaGuerreRsi_m_work[i].data[instance].values[2] = _s_iLaGuerreRsi_m_work[i - 1].data[instance].values[1] + (_gamma * (_s_iLaGuerreRsi_m_work[i - 1].data[instance].values[2] - _s_iLaGuerreRsi_m_work[i].data[instance].values[1]))
        _s_iLaGuerreRsi_m_work[i].data[instance].values[3] = _s_iLaGuerreRsi_m_work[i - 1].data[instance].values[2] + (_gamma * (_s_iLaGuerreRsi_m_work[i - 1].data[instance].values[3] - _s_iLaGuerreRsi_m_work[i].data[instance].values[2]))
        if _s_iLaGuerreRsi_m_work[i].data[instance].values[0] >= _s_iLaGuerreRsi_m_work[i].data[instance].values[1]:
            CU = _s_iLaGuerreRsi_m_work[i].data[instance].values[0] - _s_iLaGuerreRsi_m_work[i].data[instance].values[1]
        else:
            CD = _s_iLaGuerreRsi_m_work[i].data[instance].values[1] - _s_iLaGuerreRsi_m_work[i].data[instance].values[0]
        if _s_iLaGuerreRsi_m_work[i].data[instance].values[1] >= _s_iLaGuerreRsi_m_work[i].data[instance].values[2]:
            CU += _s_iLaGuerreRsi_m_work[i].data[instance].values[1] - _s_iLaGuerreRsi_m_work[i].data[instance].values[2]
        else:
            CD += _s_iLaGuerreRsi_m_work[i].data[instance].values[2] - _s_iLaGuerreRsi_m_work[i].data[instance].values[1]
        if _s_iLaGuerreRsi_m_work[i].data[instance].values[2] >= _s_iLaGuerreRsi_m_work[i].data[instance].values[3]:
            CU += _s_iLaGuerreRsi_m_work[i].data[instance].values[2] - _s_iLaGuerreRsi_m_work[i].data[instance].values[3]
        else:
            CD += _s_iLaGuerreRsi_m_work[i].data[instance].values[3] - _s_iLaGuerreRsi_m_work[i].data[instance].values[2]
    else:
        for k in range(0, 4):
            _s_iLaGuerreRsi_m_work[i].data[instance].values[k] = price
        _s_iLaGuerreRsi_m_work[i].data[instance].price = price
    return (_fdiv(CU, CU + CD) if ((CU + CD) != 0) else 0)

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
global_ = _alloc(sGlobalStruct)
global_.__init__()

# ---- static local variables
_s_OnCalculate_m_work = Arr(0, 0, factory=sWorkStruct)
_s_OnCalculate_m_workSize = -1
_s_iLaGuerreRsi_m_work = Arr(0, 0, factory=sWorkStruct_iLaGuerreRsi)
_s_iLaGuerreRsi_m_workSize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ATRAdaptiveSmoothedLaguerreRSI2NoBuiltInFunctions(_MQL5Indicator):
    name = 'ATR adaptive smoothed Laguerre RSI 2 (no built in functions)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpAtrPeriod': 32,  # ATR period
        'inpRsiPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpRsiSmoothPeriod': 5.0,  # Price smoothing period
        'inpLevelUp': 0.85,  # Level up
        'inpLevelDown': 0.15,  # Level down
    }

