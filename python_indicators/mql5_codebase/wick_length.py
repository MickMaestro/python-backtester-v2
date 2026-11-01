"""Wick_Length — converted from MQL5: MQL5 Indicators/Wick_Length/Wick_Length.mq5

Wick length indicator.
The indicator shows the candles lengths.
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Upper wick', 2: 'Lower wick'}, 'levels': [], 'description': ['Wick length indicator.', 'The indicator shows the candles lengths.'], 'name': 'Wick_Length', 'source': 'MQL5 Indicators/Wick_Length/Wick_Length.mq5', 'folder': 'Wick_Length', 'inputs': [{'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_MODE
MODE_SEP = 0
MODE_SEP_OPP = 1
MODE_CML = 2
MODE_DIFF = 3
_enum('ENUM_MODE', {0: 'MODE_SEP', 1: 'MODE_SEP_OPP', 2: 'MODE_CML', 3: 'MODE_DIFF'})

# ---- inputs and global variables
InpMethod = _input('InpMethod', MODE_SEP)  # Method
BufferWLup = Arr(0, 0.0)
BufferWLdn = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BufferWLup, INDICATOR_DATA)
    SetIndexBuffer(1, BufferWLdn, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Wick length (' + MethodToString() + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    if InpMethod == MODE_SEP:
        PlotIndexSetString(0, PLOT_LABEL, 'Upper wick')
        PlotIndexSetString(1, PLOT_LABEL, 'Lower wick')
        PlotIndexSetInteger(1, PLOT_SHOW_DATA, True)
    elif InpMethod == MODE_SEP_OPP:
        PlotIndexSetString(0, PLOT_LABEL, 'Upper wick')
        PlotIndexSetString(1, PLOT_LABEL, 'Lower wick')
        PlotIndexSetInteger(1, PLOT_SHOW_DATA, True)
    elif InpMethod == MODE_CML:
        PlotIndexSetString(0, PLOT_LABEL, 'Wick cumulative')
        PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    else:
        PlotIndexSetString(0, PLOT_LABEL, 'Wick difference')
        PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(BufferWLup, True)
    ArraySetAsSeries(BufferWLdn, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 4 or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferWLup, EMPTY_VALUE)
        ArrayInitialize(BufferWLdn, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        Up = _fdiv(high[i] - fmax(open[i], close[i]), Point())
        Down = _fdiv(-(fmin(open[i], close[i]) - low[i]), Point())
        if InpMethod == MODE_SEP_OPP:
            if close[i] > open[i]:
                Up = 0.0
            else:
                Down = 0.0
        if InpMethod == MODE_SEP or InpMethod == MODE_SEP_OPP:
            BufferWLup[i] = Up
            BufferWLdn[i] = Down
        else:
            BufferWLdn[i] = EMPTY_VALUE
            if InpMethod == MODE_DIFF:
                BufferWLup[i] = Up - fabs(Down)
            else:
                BufferWLup[i] = Up + fabs(Down)
    return rates_total

def MethodToString():
    return ('Separated' if (InpMethod == MODE_SEP) else 'Separated Opposite Only' if (InpMethod == MODE_SEP_OPP) else 'Cumulative' if (InpMethod == MODE_CML) else 'Difference')


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WickLength(_MQL5Indicator):
    name = 'Wick_Length'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMethod': _Choice({0: 'Separated', 1: 'Separated Opposite Only', 2: 'Cumulative', 3: 'Difference'}, default=0),  # Method
    }

