"""Gann high low activator (simple) — converted from MQL5: MQL5 Indicators/Gann high_low activator (simple)/Gann high low activator (simple).mq5

Gann high/low activator
Copyright: © mladen, 2020; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2020', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [3329330, 17919]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Gann activator'}, 'levels': [], 'description': ['Gann high/low activator'], 'name': 'Gann high low activator (simple)', 'source': 'MQL5 Indicators/Gann high_low activator (simple)/Gann high low activator (simple).mq5', 'folder': 'Gann high_low activator (simple)', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 10, 'label': 'Activator period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 10)  # Activator period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

class sWorkStruct(MqlObject):
    _q_fields = ('sumHigh', 'sumLow', 'state')
    def __init__(self, *args):
        self.sumHigh = 0.0
        self.sumLow = 0.0
        self.state = 0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Gann high/low activator (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_workSize
    limit = ((prev_calculated - 1) if prev_calculated else 0)
    if _s_OnCalculate_m_workSize < rates_total:
        _s_OnCalculate_m_workSize = ArrayResize(_s_OnCalculate_m_work, rates_total + 500, 2000)
    for i in range(limit, rates_total):
        if i > inpPeriod:
            _s_OnCalculate_m_work[i].sumHigh = _s_OnCalculate_m_work[i - 1].sumHigh + high[i] - high[i - inpPeriod]
            _s_OnCalculate_m_work[i].sumLow = _s_OnCalculate_m_work[i - 1].sumLow + low[i] - low[i - inpPeriod]
        else:
            _s_OnCalculate_m_work[i].sumHigh = high[i]
            _s_OnCalculate_m_work[i].sumLow = low[i]
            k = 1
            while k < inpPeriod and i >= k:
                _s_OnCalculate_m_work[i].sumHigh += high[i - k]
                _s_OnCalculate_m_work[i].sumLow += low[i - k]
                k += 1
        avgHigh = ((_s_OnCalculate_m_work[i - 1].sumHigh / float(inpPeriod)) if (i > 0) else high[i])
        avgLow = ((_s_OnCalculate_m_work[i - 1].sumLow / float(inpPeriod)) if (i > 0) else low[i])
        _s_OnCalculate_m_work[i].state = (1 if (close[i] > avgHigh) else -1 if (close[i] < avgLow) else _s_OnCalculate_m_work[i - 1].state if (i > 0) else 0)
        val[i] = (avgLow if (_s_OnCalculate_m_work[i].state == 1) else avgHigh if (_s_OnCalculate_m_work[i].state == -1) else close[i])
        valc[i] = (0 if (_s_OnCalculate_m_work[i].state == 1) else 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_m_work = Arr(0, 0, factory=sWorkStruct)
_s_OnCalculate_m_workSize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GannHighLowActivatorSimple(_MQL5Indicator):
    name = 'Gann high low activator (simple)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 10,  # Activator period
    }

