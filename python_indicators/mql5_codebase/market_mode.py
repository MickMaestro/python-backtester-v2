"""Market mode — converted from MQL5: MQL5 Indicators/Market mode/Market mode.mq5

Market mode
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 8}, 'colors': {1: [11119017], 2: [11119017], 3: [12632256, 7451452, 17919]}, 'widths': {3: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Market mode'], 'name': 'Market mode', 'source': 'MQL5 Indicators/Market mode/Market mode.mq5', 'folder': 'Market mode', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'inpDelta', 'py': 'inpDelta', 'param': 'inpDelta', 'type': 'double', 'default': 0.5, 'label': 'Delta', 'sinput': False}, {'mql': 'inpFraction', 'py': 'inpFraction', 'param': 'inpFraction', 'type': 'double', 'default': 0.1, 'label': 'Fraction', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 5, 'label': 'Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 20)  # Period
inpDelta = _input('inpDelta', 0.5)  # Delta
inpFraction = _input('inpFraction', 0.1)  # Fraction
inpPrice = _input('inpPrice', PRICE_MEDIAN)  # Price
mode = Arr(0, 0.0)
modec = Arr(0, 0.0)
fractionUp = Arr(0, 0.0)
fractionDn = Arr(0, 0.0)
g_alpha = 0.0
g_alphal = 0.0
g_beta = 0.0
g_dPeriod = 0

class sMarketModeStruct(MqlObject):
    _q_fields = ('price', 'bandpass', 'peak', 'valey', 'sumbp', 'sumpeak', 'sumvaley')
    def __init__(self, *args):
        self.price = 0.0
        self.bandpass = 0.0
        self.peak = 0.0
        self.valey = 0.0
        self.sumbp = 0.0
        self.sumpeak = 0.0
        self.sumvaley = 0.0

def OnInit():
    global g_alpha, g_beta, g_dPeriod
    SetIndexBuffer(0, fractionUp)
    SetIndexBuffer(1, fractionDn)
    SetIndexBuffer(2, mode)
    SetIndexBuffer(3, modec, INDICATOR_COLOR_INDEX)
    gamma = _fdiv(1.0, MathCos((4.0 * M_PI * inpDelta) / inpPeriod))
    g_beta = MathCos((2.0 * M_PI) / inpPeriod)
    g_alpha = gamma - MathSqrt((gamma * gamma) - 1.0)
    g_dPeriod = 2 * inpPeriod
    IndicatorSetString(INDICATOR_SHORTNAME, 'Market mode ' + _str(inpPeriod) + ',' + _str(inpDelta) + ',' + _str(inpFraction) + ')')
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
        if i > 1:
            m_array[i].bandpass = (0.5 * (1.0 - g_alpha) * (m_array[i].price - m_array[i - 2].price)) + (g_beta * (1.0 + g_alpha) * m_array[i - 1].bandpass) - (g_alpha * m_array[i - 2].bandpass)
            m_array[i].peak = m_array[i - 1].peak
            m_array[i].valey = m_array[i - 1].valey
            if m_array[i - 1].bandpass > m_array[i].bandpass and m_array[i - 1].bandpass > m_array[i - 2].bandpass:
                m_array[i].peak = m_array[i - 1].bandpass
            if m_array[i - 1].bandpass < m_array[i].bandpass and m_array[i - 1].bandpass < m_array[i - 2].bandpass:
                m_array[i].valey = m_array[i - 1].bandpass
        else:
            m_array[i].bandpass = m_array[i].price
            m_array[i].valey = m_array[i].bandpass
            m_array[i].peak = m_array[i].valey
        if i > g_dPeriod:
            m_array[i].sumbp = m_array[i - 1].sumbp + m_array[i].bandpass - m_array[i - g_dPeriod].bandpass
        else:
            m_array[i].sumbp = m_array[i].bandpass
            k = 1
            while k < g_dPeriod and (i - k) >= 0:
                m_array[i].sumbp += m_array[i - k].bandpass
                k += 1
        if i > 50:
            m_array[i].sumpeak = m_array[i - 1].sumpeak + m_array[i].peak - m_array[i - 50].peak
            m_array[i].sumvaley = m_array[i - 1].sumvaley + m_array[i].valey - m_array[i - 50].valey
        else:
            m_array[i].sumpeak = m_array[i].peak
            m_array[i].sumvaley = m_array[i].valey
            k = 1
            while k < 50 and (i - k) >= 0:
                m_array[i].sumpeak += m_array[i - k].peak
                m_array[i].sumvaley += m_array[i - k].valey
                k += 1
        fractionUp[i] = (inpFraction * m_array[i].sumpeak) / 50.0
        fractionDn[i] = (inpFraction * m_array[i].sumvaley) / 50.0
        mode[i] = _fdiv(m_array[i].sumbp, float(g_dPeriod))
        modec[i] = (1 if (mode[i] > fractionUp[i]) else 2 if (mode[i] < fractionDn[i]) else 0)
        i += 1
    return i

# ---- global variables initialised from expressions
m_array = Arr(0, 0, factory=sMarketModeStruct)

# ---- static local variables
_s_OnCalculate_m_arraySize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MarketMode(_MQL5Indicator):
    name = 'Market mode'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 20,  # Period
        'inpDelta': 0.5,  # Delta
        'inpFraction': 0.1,  # Fraction
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Price
    }

