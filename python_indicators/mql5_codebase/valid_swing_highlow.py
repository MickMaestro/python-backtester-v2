"""Valid_Swing_HighLow — converted from MQL5: MQL5 Indicators/Valid_Swing_HighLow/Valid_Swing_HighLow.mq5

Valid Swing HighLow indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [32768]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Fractal Up', 2: 'Fractal Down'}, 'levels': [], 'description': ['Valid Swing HighLow indicator'], 'name': 'Valid_Swing_HighLow', 'source': 'MQL5 Indicators/Valid_Swing_HighLow/Valid_Swing_HighLow.mq5', 'folder': 'Valid_Swing_HighLow', 'inputs': [{'mql': 'InpDrawBar', 'py': 'InpDrawBar', 'param': 'InpDrawBar', 'type': 'int', 'default': 0, 'label': 'Bar of drawing', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_DRAW_BAR
BAR_SIGNAL = 0
BAR_FRACTAL = 1
_enum('ENUM_DRAW_BAR', {0: 'BAR_SIGNAL', 1: 'BAR_FRACTAL'})

# ---- inputs and global variables
InpDrawBar = _input('InpDrawBar', BAR_SIGNAL)  # Bar of drawing
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferLast = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferLast, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 119)
    PlotIndexSetInteger(1, PLOT_ARROW, 119)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Valid Swing HighLow')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferLast, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < 5:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 5
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferLast, 0)
    for i in range(limit, 0 - 1, -1):
        curr = i + 2
        bar = (i if (InpDrawBar == BAR_SIGNAL) else curr)
        BufferLast[curr] = 0.0
        BufferDN[i] = EMPTY_VALUE
        BufferUP[i] = BufferDN[i]
        if ((high[curr] > high[curr - 1] and high[curr] > high[curr - 2]) and high[curr] > high[curr + 1]) and high[curr] > high[curr + 2]:
            BufferUP[bar] = (open[i] if (InpDrawBar == BAR_SIGNAL) else high[bar])
            BufferLast[curr] = 1.0
            Previous(rates_total, i, 1, high, low)
        if ((low[curr] < low[curr - 1] and low[curr] < low[curr - 2]) and low[curr] < low[curr + 1]) and low[curr] < low[curr + 2]:
            BufferDN[bar] = (open[i] if (InpDrawBar == BAR_SIGNAL) else low[bar])
            BufferLast[curr] = -1.0
            Previous(rates_total, i, -1, high, low)
    return rates_total

def Previous(rates_total, index, flag, high, low):
    limit = rates_total - 2
    for i in range(index + 1, limit + 1):
        if BufferLast[i] == flag:
            if flag == 1 and high[i] < high[index]:
                BufferLast[i] = 0.0
                break
            elif flag == -1 and low[i] > low[index]:
                BufferLast[i] = 0.0
                break


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ValidSwingHighLow(_MQL5Indicator):
    name = 'Valid_Swing_HighLow'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpDrawBar': _Choice({0: 'Signal bar', 1: 'Fractal bar'}, default=0),  # Bar of drawing
    }

