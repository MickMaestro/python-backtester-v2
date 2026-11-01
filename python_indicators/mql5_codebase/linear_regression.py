"""Linear regression — converted from MQL5: MQL5 Indicators/Liner regression/Linear regression.mq5

Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 9639167, 7451452]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Liner regression value'}, 'levels': [], 'description': [], 'name': 'Linear regression', 'source': 'MQL5 Indicators/Liner regression/Linear regression.mq5', 'folder': 'Liner regression', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 20)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

class sLinrArrayStruct(MqlObject):
    _q_fields = ('price', 'wsumm', 'psumm', 'weight')
    def __init__(self, *args):
        self.price = 0.0
        self.wsumm = 0.0
        self.psumm = 0.0
        self.weight = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Linear regression value (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

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
        val[i] = iLinr(_price, inpPeriod, i, rates_total)
        valc[i] = ((2 if (val[i] > val[i - 1]) else 1 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i

def iLinr(price, period, i, bars, instance=0):
    global _s_iLinr_m_arraySize
    if _s_iLinr_m_arraySize < bars:
        _res = ArrayResize(_s_iLinr_m_array, bars + 500)
        if _res <= bars:
            return 0.0
        _s_iLinr_m_arraySize = _res
    _s_iLinr_m_array[i][instance].price = price
    if i > period:
        _s_iLinr_m_array[i][instance].weight = _s_iLinr_m_array[i - 1][instance].weight
        _s_iLinr_m_array[i][instance].wsumm = _s_iLinr_m_array[i - 1][instance].wsumm + (price * period) - _s_iLinr_m_array[i - 1][instance].psumm
        _s_iLinr_m_array[i][instance].psumm = _s_iLinr_m_array[i - 1][instance].psumm + price - _s_iLinr_m_array[i - period][instance].price
    else:
        _s_iLinr_m_array[i][instance].wsumm = 0.0
        _s_iLinr_m_array[i][instance].psumm = 0.0
        _s_iLinr_m_array[i][instance].weight = 0.0
        k = 0
        w = period
        while k < period and i >= k:
            _s_iLinr_m_array[i][instance].wsumm += _s_iLinr_m_array[i - k][instance].price * w
            _s_iLinr_m_array[i][instance].psumm += _s_iLinr_m_array[i - k][instance].price
            _s_iLinr_m_array[i][instance].weight += w
            k += 1
            w -= 1
    return _fdiv(3.0 * _s_iLinr_m_array[i][instance].wsumm, _s_iLinr_m_array[i][instance].weight) - _fdiv(2.0 * _s_iLinr_m_array[i][instance].psumm, float(period))

# ---- static local variables
_s_iLinr_m_array = Arr(0, 0, factory=sLinrArrayStruct, dims=(1,))
_s_iLinr_m_arraySize = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LinearRegression(_MQL5Indicator):
    name = 'Linear regression'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 20,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
    }

