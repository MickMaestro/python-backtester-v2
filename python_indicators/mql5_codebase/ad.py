"""AD — converted from MQL5: MQL5 Indicators/AD/AD.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [32768]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'AD'}, 'levels': [], 'description': [], 'name': 'AD', 'source': 'MQL5 Indicators/AD/AD.mq5', 'folder': 'AD', 'inputs': [{'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'AD calculation method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_METHOD
METHOD_CLASSIC = 0
METHOD_INC = 1
METHOD_TS_INC = 2
_enum('ENUM_METHOD', {0: 'METHOD_CLASSIC', 1: 'METHOD_INC', 2: 'METHOD_TS_INC'})

# ---- inputs and global variables
InpMethod = _input('InpMethod', METHOD_CLASSIC)  # AD calculation method
BufferAD = Arr(0, 0.0)
BufferCurent = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BufferAD, INDICATOR_DATA)
    SetIndexBuffer(1, BufferCurent, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'AD')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferAD, True)
    ArraySetAsSeries(BufferCurent, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 1:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    limit = rates_total - prev_calculated
    limit2 = limit
    if limit > 1:
        limit = rates_total - 1
        limit2 = limit - 1
        ArrayInitialize(BufferAD, 0)
        ArrayInitialize(BufferCurent, 0)
    for i in range(limit, 0 - 1, -1):
        BufferCurent[i] = (((_fdiv(close[i] - open[i], high[i] - low[i]) * tick_volume[i]) if (InpMethod == METHOD_TS_INC) else (_fdiv(close[i] - low[i] - (high[i] - close[i]), high[i] - low[i]) * tick_volume[i])) if ((high[i] - low[i]) != 0) else 0)
    for i in range(limit2, 0 - 1, -1):
        BufferAD[i] = (BufferCurent[i] if (InpMethod == METHOD_CLASSIC) else (BufferAD[i + 1] + BufferCurent[i]))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AD(_MQL5Indicator):
    name = 'AD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMethod': _Choice({0: 'Classical', 1: 'Classical Incremental', 2: 'Trade Station Incremental'}, default=0),  # AD calculation method
    }

