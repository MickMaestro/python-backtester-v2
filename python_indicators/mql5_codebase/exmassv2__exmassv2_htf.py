"""ExMassV2 — converted from MQL5: MQL5 Indicators/ExMassV2_HTF/ExMassV2.mq5

Copyright: Copyright © 2006, Alex Sidd (Executer); Link: mailto:work_st@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Alex Sidd (Executer)', 'link': 'mailto:work_st@mail.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [14381203]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'ExMass'}, 'levels': [], 'description': [], 'name': 'ExMassV2', 'source': 'MQL5 Indicators/ExMassV2_HTF/ExMassV2.mq5', 'folder': 'ExMassV2_HTF', 'inputs': [{'mql': 'ExPeriod', 'py': 'ExPeriod', 'param': 'ExPeriod', 'type': 'uint', 'default': 8, 'label': 'период', 'sinput': False}, {'mql': 'Normalize', 'py': 'Normalize', 'param': 'Normalize', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExPeriod = _input('ExPeriod', 8)  # период
Normalize = _input('Normalize', 3)
ExtBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(ExPeriod + Normalize)
    SetIndexBuffer(0, ExtBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ExMassV2')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    poss = 0.0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        positive = high[ArrayMaximum(high, bar, ExPeriod)]
        negative = low[ArrayMinimum(low, bar, ExPeriod)]
        poss = 0.0
        for kkk in range(1, _int(Normalize)):
            poss += ExtBuffer[MathMin(bar + kkk, rates_total - 1)]
        ExtBuffer[bar] = (poss + _fdiv(positive - negative, Point())) / Normalize
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ExMassV2(_MQL5Indicator):
    name = 'ExMassV2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ExPeriod': 8,  # период
        'Normalize': 3,
    }

