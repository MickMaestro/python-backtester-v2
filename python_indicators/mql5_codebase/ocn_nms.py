"""ocn - nms — converted from MQL5: MQL5 Indicators/Ocean theory - natural market slope/ocn - nms.mq5

Copyright: © mladen, 2020; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2020', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [7451452, 5275647]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Ocean natural market slope'}, 'levels': [], 'description': [], 'name': 'ocn - nms', 'source': 'MQL5 Indicators/Ocean theory - natural market slope/ocn - nms.mq5', 'folder': 'Ocean theory - natural market slope', 'inputs': [{'mql': 'inpNmsPeriod', 'py': 'inpNmsPeriod', 'param': 'inpNmsPeriod', 'type': 'int', 'default': 40, 'label': 'Natural market slope period', 'sinput': False}, {'mql': 'inpNmsPrice', 'py': 'inpNmsPrice', 'param': 'inpNmsPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpTemaPeriod', 'py': 'inpTemaPeriod', 'param': 'inpTemaPeriod', 'type': 'int', 'default': 10, 'label': 'Triple EMA pre-smoothing period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpNmsPeriod = _input('inpNmsPeriod', 40)  # Natural market slope period
inpNmsPrice = _input('inpNmsPrice', PRICE_CLOSE)  # Price
inpTemaPeriod = _input('inpTemaPeriod', 10)  # Triple EMA pre-smoothing period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
alpha = 0.0
iNmsPeriod = 0

class sCoeffStruct(MqlObject):
    _q_fields = ('sumx', 'sumx2', 'bot', 'root')
    def __init__(self, *args):
        self.sumx = 0.0
        self.sumx2 = 0.0
        self.bot = 0.0
        self.root = 0.0

class sWorkStruct(MqlObject):
    _q_fields = ('price', 'tema0', 'tema1', 'tema2')
    def __init__(self, *args):
        self.price = 0.0
        self.tema0 = 0.0
        self.tema1 = 0.0
        self.tema2 = 0.0

def OnInit():
    global alpha, iNmsPeriod
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    iNmsPeriod = (inpNmsPeriod if (inpNmsPeriod > 1) else 1)
    alpha = _fdiv(2.0, 1.0 + MathMax(inpTemaPeriod, 1))
    ArrayResize(coeff, iNmsPeriod + 1)
    for period in range(1, iNmsPeriod + 1):
        coeff[period].sumx = (period * (period + 1.0)) / 2.0
        coeff[period].sumx2 = (period * (period + 1.0) * ((2 * period) + 1.0)) / 6.0
        coeff[period].bot = (period * coeff[period].sumx2) - (coeff[period].sumx * coeff[period].sumx)
        if coeff[period].bot == 0:
            coeff[period].bot = 1.0
        coeff[period].root = MathSqrt(period)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Ocean nms (' + _str(iNmsPeriod) + ',' + _str(inpTemaPeriod) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_workSize
    limit = prev_calculated - 1
    if limit < 0:
        limit = 0
    if _s_OnCalculate_m_workSize < rates_total:
        _s_OnCalculate_m_workSize = ArrayResize(_s_OnCalculate_m_work, rates_total + 500, 2000)
    for i in range(limit, rates_total):
        _price = MathLog(getPrice(inpNmsPrice, _ElemRef(open, i), _ElemRef(high, i), _ElemRef(low, i), _ElemRef(close, i)))
        if i == 0:
            _s_OnCalculate_m_work[i].tema2 = _price
            _s_OnCalculate_m_work[i].tema1 = _s_OnCalculate_m_work[i].tema2
            _s_OnCalculate_m_work[i].tema0 = _s_OnCalculate_m_work[i].tema1
        else:
            _s_OnCalculate_m_work[i].tema0 = _s_OnCalculate_m_work[i - 1].tema0 + (alpha * (_price - _s_OnCalculate_m_work[i - 1].tema0))
            _s_OnCalculate_m_work[i].tema1 = _s_OnCalculate_m_work[i - 1].tema1 + (alpha * (_s_OnCalculate_m_work[i].tema0 - _s_OnCalculate_m_work[i - 1].tema1))
            _s_OnCalculate_m_work[i].tema2 = _s_OnCalculate_m_work[i - 1].tema2 + (alpha * (_s_OnCalculate_m_work[i].tema1 - _s_OnCalculate_m_work[i - 1].tema2))
        _s_OnCalculate_m_work[i].price = (3.0 * _s_OnCalculate_m_work[i].tema0) - (3.0 * _s_OnCalculate_m_work[i].tema1) + _s_OnCalculate_m_work[i].tema2
        sumxy = 0.0
        sumy = 0.0
        sum_ = 0.0
        period = 1
        while period <= iNmsPeriod and i >= period:
            sumxy += sumy + _s_OnCalculate_m_work[i - (period - 1)].price
            sumy += _s_OnCalculate_m_work[i - (period - 1)].price
            sum_ += _fdiv((period * sumxy) - (coeff[period].sumx * sumy), coeff[period].bot) * coeff[period].root
            period += 1
        val[i] = sum_ * 100.0
        valc[i] = ((0 if (val[i] > val[i - 1]) else 1) if (i > 0) else 0)
    return rates_total

def getPrice(price, open, high, low, close):
    _sw1 = price
    if _sw1 == PRICE_CLOSE:
        return close.v
    elif _sw1 == PRICE_HIGH:
        return high.v
    elif _sw1 == PRICE_LOW:
        return low.v
    elif _sw1 == PRICE_OPEN:
        return open.v
    elif _sw1 == PRICE_MEDIAN:
        return (high.v + low.v) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (high.v + low.v + close.v) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return (high.v + low.v + close.v + close.v) / 4.0
    return 0.0

# ---- global variables initialised from expressions
coeff = Arr(0, 0, factory=sCoeffStruct)

# ---- static local variables
_s_OnCalculate_m_work = Arr(0, 0, factory=sWorkStruct)
_s_OnCalculate_m_workSize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class OcnNms(_MQL5Indicator):
    name = 'ocn - nms'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpNmsPeriod': 40,  # Natural market slope period
        'inpNmsPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpTemaPeriod': 10,  # Triple EMA pre-smoothing period
    }

