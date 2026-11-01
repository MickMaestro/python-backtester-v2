"""Psychology_Index — converted from MQL5: MQL5 Indicators/Psychology_Index/Psychology_Index.mq5

Psychology Index
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [14772545]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Psy Index'}, 'levels': [], 'description': ['Psychology Index'], 'name': 'Psychology_Index', 'source': 'MQL5 Indicators/Psychology_Index/Psychology_Index.mq5', 'folder': 'Psychology_Index', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 12, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 12)  # Period
BufferPI = Arr(0, 0.0)
BufferUpD = Arr(0, 0.0)
period_ind = 0

def OnInit():
    global period_ind
    period_ind = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferPI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferUpD, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'PsyIndex(' + _str(period_ind) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferPI, True)
    ArraySetAsSeries(BufferUpD, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_ind:
        return 0
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferPI, EMPTY_VALUE)
        ArrayInitialize(BufferUpD, 0)
    for i in range(limit, 0 - 1, -1):
        BufferUpD[i] = (1 if (close[i] > close[i + 1]) else 0)
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferUpD, BufferPI)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PsychologyIndex(_MQL5Indicator):
    name = 'Psychology_Index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 12,  # Period
    }

