"""Range weighted average MACD — converted from MQL5: MQL5 Indicators/Range weighted average MACD/Range weighted average MACD.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 7, 2: 8, 3: 8}, 'colors': {1: [14811105, 14803455], 2: [11119017, 17919, 7451452], 3: [11119017, 17919, 7451452]}, 'widths': {2: 2}, 'styles': {3: 2}, 'labels': {1: 'Fill zone', 2: 'Range weighted average MACD', 3: 'Range weighted average MACD signal'}, 'levels': [], 'description': [], 'name': 'Range weighted average MACD', 'source': 'MQL5 Indicators/Range weighted average MACD/Range weighted average MACD.mq5', 'folder': 'Range weighted average MACD', 'inputs': [{'mql': 'inpFastPeriod', 'py': 'inpFastPeriod', 'param': 'inpFastPeriod', 'type': 'int', 'default': 12, 'label': 'Fast period', 'sinput': False}, {'mql': 'inpSlowPeriod', 'py': 'inpSlowPeriod', 'param': 'inpSlowPeriod', 'type': 'int', 'default': 26, 'label': 'Slow period', 'sinput': False}, {'mql': 'inpSignPeriod', 'py': 'inpSignPeriod', 'param': 'inpSignPeriod', 'type': 'int', 'default': 9, 'label': 'Signal period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpFastPeriod = _input('inpFastPeriod', 12)  # Fast period
inpSlowPeriod = _input('inpSlowPeriod', 26)  # Slow period
inpSignPeriod = _input('inpSignPeriod', 9)  # Signal period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
valm = Arr(0, 0.0)
valmc = Arr(0, 0.0)
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
vals = Arr(0, 0.0)
valsc = Arr(0, 0.0)

class sRwAverage(MqlObject):
    _q_fields = ('weight', 'price', 'macd', 'sumw1', 'sump1', 'sumw2', 'sump2', 'sumw3', 'sump3')
    def __init__(self, *args):
        self.weight = 0.0
        self.price = 0.0
        self.macd = 0.0
        self.sumw1 = 0.0
        self.sump1 = 0.0
        self.sumw2 = 0.0
        self.sump2 = 0.0
        self.sumw3 = 0.0
        self.sump3 = 0.0

def OnInit():
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, valm, INDICATOR_DATA)
    SetIndexBuffer(3, valmc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, vals, INDICATOR_DATA)
    SetIndexBuffer(5, valsc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Range weighted average MACD (' + _str(inpFastPeriod) + ',' + _str(inpSlowPeriod) + _str(inpSignPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_arraySize
    if _s_OnCalculate_m_arraySize < rates_total:
        _res = ArrayResize(_s_OnCalculate_m_array, rates_total + 500)
        if _res <= rates_total:
            return prev_calculated
        _s_OnCalculate_m_arraySize = _res
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
        _weight = high[i] - low[i]
        if _weight == 0:
            _weight = Point()
        _s_OnCalculate_m_array[i].weight = _weight
        _s_OnCalculate_m_array[i].price = _weight * _price
        if i > inpFastPeriod:
            _s_OnCalculate_m_array[i].sump1 = _s_OnCalculate_m_array[i - 1].sump1 + _s_OnCalculate_m_array[i].price - _s_OnCalculate_m_array[i - inpFastPeriod].price
            _s_OnCalculate_m_array[i].sumw1 = _s_OnCalculate_m_array[i - 1].sumw1 + _s_OnCalculate_m_array[i].weight - _s_OnCalculate_m_array[i - inpFastPeriod].weight
        else:
            _s_OnCalculate_m_array[i].sump1 = _s_OnCalculate_m_array[i].price
            _s_OnCalculate_m_array[i].sumw1 = _s_OnCalculate_m_array[i].weight
            k = 1
            while k < inpFastPeriod and i >= k:
                _s_OnCalculate_m_array[i].sump1 += _s_OnCalculate_m_array[i - k].price
                _s_OnCalculate_m_array[i].sumw1 += _s_OnCalculate_m_array[i - k].weight
                k += 1
        if i > inpSlowPeriod:
            _s_OnCalculate_m_array[i].sump2 = _s_OnCalculate_m_array[i - 1].sump2 + _s_OnCalculate_m_array[i].price - _s_OnCalculate_m_array[i - inpSlowPeriod].price
            _s_OnCalculate_m_array[i].sumw2 = _s_OnCalculate_m_array[i - 1].sumw2 + _s_OnCalculate_m_array[i].weight - _s_OnCalculate_m_array[i - inpSlowPeriod].weight
        else:
            _s_OnCalculate_m_array[i].sump2 = _s_OnCalculate_m_array[i].price
            _s_OnCalculate_m_array[i].sumw2 = _s_OnCalculate_m_array[i].weight
            k = 1
            while k < inpSlowPeriod and i >= k:
                _s_OnCalculate_m_array[i].sump2 += _s_OnCalculate_m_array[i - k].price
                _s_OnCalculate_m_array[i].sumw2 += _s_OnCalculate_m_array[i - k].weight
                k += 1
        _s_OnCalculate_m_array[i].macd = _weight * (_fdiv(_s_OnCalculate_m_array[i].sump1, _s_OnCalculate_m_array[i].sumw1) - _fdiv(_s_OnCalculate_m_array[i].sump2, _s_OnCalculate_m_array[i].sumw2))
        if i > inpSignPeriod:
            _s_OnCalculate_m_array[i].sump3 = _s_OnCalculate_m_array[i - 1].sump3 + _s_OnCalculate_m_array[i].macd - _s_OnCalculate_m_array[i - inpSignPeriod].macd
            _s_OnCalculate_m_array[i].sumw3 = _s_OnCalculate_m_array[i - 1].sumw3 + _s_OnCalculate_m_array[i].weight - _s_OnCalculate_m_array[i - inpSignPeriod].weight
        else:
            _s_OnCalculate_m_array[i].sump3 = _s_OnCalculate_m_array[i].macd
            _s_OnCalculate_m_array[i].sumw3 = _s_OnCalculate_m_array[i].weight
            k = 1
            while k < inpSignPeriod and i >= k:
                _s_OnCalculate_m_array[i].sump3 += _s_OnCalculate_m_array[i - k].macd
                _s_OnCalculate_m_array[i].sumw3 += _s_OnCalculate_m_array[i - k].weight
                k += 1
        valm[i] = _fdiv(_s_OnCalculate_m_array[i].sump1, _s_OnCalculate_m_array[i].sumw1) - _fdiv(_s_OnCalculate_m_array[i].sump2, _s_OnCalculate_m_array[i].sumw2)
        vals[i] = _fdiv(_s_OnCalculate_m_array[i].sump3, _s_OnCalculate_m_array[i].sumw3)
        valsc[i] = (2 if (valm[i] > vals[i]) else 1 if (valm[i] < vals[i]) else 0)
        valmc[i] = valsc[i]
        filld[i] = 0.0
        fillu[i] = valm[i] - vals[i]
        i += 1
    return i

# ---- static local variables
_s_OnCalculate_m_array = Arr(0, 0, factory=sRwAverage)
_s_OnCalculate_m_arraySize = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RangeWeightedAverageMACD(_MQL5Indicator):
    name = 'Range weighted average MACD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFastPeriod': 12,  # Fast period
        'inpSlowPeriod': 26,  # Slow period
        'inpSignPeriod': 9,  # Signal period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

