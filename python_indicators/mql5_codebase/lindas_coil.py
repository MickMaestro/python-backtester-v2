"""Lindas_Coil — converted from MQL5: MQL5 Indicators/Linda's Coil/Lindas_Coil.mq5

Linda's Coil indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 5}, 'colors': {1: [255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'LC'}, 'levels': [], 'description': ["Linda's Coil indicator"], 'name': 'Lindas_Coil', 'source': "MQL5 Indicators/Linda's Coil/Lindas_Coil.mq5", 'folder': "Linda's Coil", 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 3, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpType', 'py': 'InpType', 'param': 'InpType', 'type': 'int', 'default': 1, 'label': 'Type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_PATT_METHOD
METHOD_EN = 0
METHOD_EQ = 1
_enum('ENUM_PATT_METHOD', {0: 'METHOD_EN', 1: 'METHOD_EQ'})

# enum ENUM_PATT_TYPE
TYPE_PREV = 0
TYPE_FIRST = 1
_enum('ENUM_PATT_TYPE', {0: 'TYPE_PREV', 1: 'TYPE_FIRST'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 3)  # Period
InpMethod = _input('InpMethod', METHOD_EN)  # Method
InpType = _input('InpType', TYPE_FIRST)  # Type
BufferLC = Arr(0, 0.0)
period = 0

def OnInit():
    global period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferLC, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 118)
    IndicatorSetString(INDICATOR_SHORTNAME, "Linda's Coil (" + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferLC, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferLC, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        beg = i + period - 1
        flag = True
        for j in range(beg - 1, i - 1, -1):
            if InpType == TYPE_PREV:
                if ((high[j] >= high[j + 1] or low[j] <= low[j + 1]) and InpMethod == METHOD_EQ) or ((high[j] > high[j + 1] or low[j] < low[j + 1]) and InpMethod == METHOD_EN):
                    flag = False
            else:
                if ((high[j] >= high[beg] or low[j] <= low[beg]) and InpMethod == METHOD_EQ) or ((high[j] > high[beg] or low[j] < low[beg]) and InpMethod == METHOD_EN):
                    flag = False
        BufferLC[i] = (low[i] if flag else EMPTY_VALUE)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LindasCoil(_MQL5Indicator):
    name = 'Lindas_Coil'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 3,  # Period
        'InpMethod': _Choice({0: 'Engulfed', 1: 'Engulfed or Equal'}, default=0),  # Method
        'InpType': _Choice({0: 'Previous', 1: 'First'}, default=1),  # Type
    }

