"""Bandpass filter — converted from MQL5: MQL5 Indicators/Bandpass filter/Bandpass filter.mq5

Bandpass filter
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [12632256, 7451452, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Bandpass filter'], 'name': 'Bandpass filter', 'source': 'MQL5 Indicators/Bandpass filter/Bandpass filter.mq5', 'folder': 'Bandpass filter', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 50, 'label': 'Period', 'sinput': False}, {'mql': 'inpDelta', 'py': 'inpDelta', 'param': 'inpDelta', 'type': 'double', 'default': 0.5, 'label': 'Delta', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 50)  # Period
inpDelta = _input('inpDelta', 0.5)  # Delta
inpPrice = _input('inpPrice', PRICE_MEDIAN)  # Price
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
g_alpha = 0.0
g_alphal = 0.0
g_beta = 0.0

class sBandPassStruct(MqlObject):
    _q_fields = ('price', 'bandpass')
    def __init__(self, *args):
        self.price = 0.0
        self.bandpass = 0.0

def OnInit():
    global g_alpha, g_beta
    SetIndexBuffer(0, val)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    gamma = _fdiv(1.0, MathCos((4.0 * M_PI * inpDelta) / inpPeriod))
    g_beta = MathCos((2.0 * M_PI) / inpPeriod)
    g_alpha = gamma - MathSqrt((gamma * gamma) - 1.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Bandpass filter (' + _str(inpPeriod) + ',' + _str(inpDelta) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_arraySize
    if _s_OnCalculate_m_arraySize < rates_total:
        _s_OnCalculate_m_arraySize = ArrayResize(m_array, rates_total + 500)
        if _s_OnCalculate_m_arraySize < rates_total:
            return 0
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            m_array[i].price = close[i]
        elif _sw1 == PRICE_OPEN:
            m_array[i].price = open[i]
        elif _sw1 == PRICE_HIGH:
            m_array[i].price = high[i]
        elif _sw1 == PRICE_LOW:
            m_array[i].price = low[i]
        elif _sw1 == PRICE_MEDIAN:
            m_array[i].price = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            m_array[i].price = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            m_array[i].price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            m_array[i].price = 0.0
        m_array[i].bandpass = (((0.5 * (1.0 - g_alpha) * (m_array[i].price - m_array[i - 2].price)) + (g_beta * (1.0 + g_alpha) * m_array[i - 1].bandpass) - (g_alpha * m_array[i - 2].bandpass)) if (i > 1) else m_array[i].price)
        val[i] = m_array[i].bandpass
        valc[i] = (1 if (val[i] > 0) else 2 if (val[i] < 0) else 0)
        i += 1
    return i

# ---- global variables initialised from expressions
m_array = Arr(0, 0, factory=sBandPassStruct)

# ---- static local variables
_s_OnCalculate_m_arraySize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BandpassFilter(_MQL5Indicator):
    name = 'Bandpass filter'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 50,  # Period
        'inpDelta': 0.5,  # Delta
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
    }

