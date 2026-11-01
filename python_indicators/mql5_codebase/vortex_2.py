"""Vortex 2 — converted from MQL5: MQL5 Indicators/Vortex 2/Vortex 2.mq5

Vortex
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 7, 2: 8, 3: 8}, 'colors': {1: [16770276, 15000831], 2: [11119017, 16748574, 3937500], 3: [11119017, 16748574, 3937500]}, 'widths': {2: 2, 3: 1}, 'styles': {}, 'labels': {1: 'Filling', 2: 'Vortex +', 3: 'Vortex -'}, 'levels': [], 'description': ['Vortex'], 'name': 'Vortex 2', 'source': 'MQL5 Indicators/Vortex 2/Vortex 2.mq5', 'folder': 'Vortex 2', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 32, 'label': 'Vortex period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 32)  # Vortex period
fillu = Arr(0, 0.0)
filld = Arr(0, 0.0)
valp = Arr(0, 0.0)
valpc = Arr(0, 0.0)
valm = Arr(0, 0.0)
valmc = Arr(0, 0.0)

class sVortex(MqlObject):
    _q_fields = ('rng', 'mp', 'mm', 'sumrng', 'summp', 'summm')
    def __init__(self, *args):
        self.rng = 0.0
        self.mp = 0.0
        self.mm = 0.0
        self.sumrng = 0.0
        self.summp = 0.0
        self.summm = 0.0

def OnInit():
    SetIndexBuffer(0, fillu, INDICATOR_DATA)
    SetIndexBuffer(1, filld, INDICATOR_DATA)
    SetIndexBuffer(2, valp, INDICATOR_DATA)
    SetIndexBuffer(3, valpc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, valm, INDICATOR_DATA)
    SetIndexBuffer(5, valmc, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Vortex (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_arraySize
    if _s_OnCalculate_m_arraySize < rates_total:
        _s_OnCalculate_m_arraySize = ArrayResize(m_array, rates_total + 500)
        if _s_OnCalculate_m_arraySize < rates_total:
            return prev_calculated
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        if i > 0:
            m_array[i].rng = (high[i] if (high[i] > close[i - 1]) else close[i - 1]) - (low[i] if (low[i] < close[i - 1]) else close[i - 1])
            m_array[i].mp = ((high[i] - low[i - 1]) if (high[i] > low[i - 1]) else (low[i - 1] - high[i]))
            m_array[i].mm = ((low[i] - high[i - 1]) if (low[i] > high[i - 1]) else (high[i - 1] - low[i]))
            if i > inpPeriod:
                m_array[i].sumrng = m_array[i - 1].sumrng + m_array[i].rng - m_array[i - inpPeriod].rng
                m_array[i].summp = m_array[i - 1].summp + m_array[i].mp - m_array[i - inpPeriod].mp
                m_array[i].summm = m_array[i - 1].summm + m_array[i].mm - m_array[i - inpPeriod].mm
            else:
                m_array[i].sumrng = 0.0
                m_array[i].summm = m_array[i].sumrng
                m_array[i].summp = m_array[i].summm
                k = 0
                while k < inpPeriod and i >= k:
                    m_array[i].sumrng += m_array[i - k].rng
                    m_array[i].summp += m_array[i - k].mp
                    m_array[i].summm += m_array[i - k].mm
                    k += 1
        else:
            m_array[i].rng = high[i] - low[i]
            m_array[i].summm = high[i] - low[i]
            m_array[i].summp = m_array[i].summm
            m_array[i].mm = m_array[i].summp
            m_array[i].mp = m_array[i].mm
        if m_array[i].sumrng != 0:
            valp[i] = _fdiv(m_array[i].summp, m_array[i].sumrng)
            valm[i] = _fdiv(m_array[i].summm, m_array[i].sumrng)
        else:
            valm[i] = 0.0
            valp[i] = valm[i]
        valpc[i] = (1 if (valp[i] > valm[i]) else 2)
        valmc[i] = (1 if (valp[i] > valm[i]) else 2)
        fillu[i] = valp[i]
        filld[i] = valm[i]
        i += 1
    return i

# ---- global variables initialised from expressions
m_array = Arr(0, 0, factory=sVortex)

# ---- static local variables
_s_OnCalculate_m_arraySize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Vortex2(_MQL5Indicator):
    name = 'Vortex 2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 32,  # Vortex period
    }

