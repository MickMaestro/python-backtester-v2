"""reversalbar — converted from MQL5: MQL5 Indicators/Reversal Bar/reversalbar.mq5

Copyright: zfs; Link: vasbsm@mail.ru

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'zfs', 'link': 'vasbsm@mail.ru', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'ReversalBar'}, 'levels': [], 'description': [], 'name': 'reversalbar', 'source': 'MQL5 Indicators/Reversal Bar/reversalbar.mq5', 'folder': 'Reversal Bar', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Blue = 0xFF0000  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

# ---- inputs and global variables
ExtBuffer = Arr(0, 0.0)
OpenBuffer = Arr(0, 0.0)
HighBuffer = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)
CloseBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, OpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, HighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, LowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, CloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 3)
    for i in range(1, 3):
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, i, ColorOf[i])
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    if prev_calculated == 0:
        i = 0
    else:
        i = prev_calculated - 1
    while i < rates_total:
        OpenBuffer[i] = Open[i]
        HighBuffer[i] = High[i]
        LowBuffer[i] = Low[i]
        CloseBuffer[i] = Close[i]
        ExtBuffer[i] = 0.0
        if ((i > 2 and High[i - 1] >= High[i - 2]) and Close[i - 1] < ((High[i - 1] + Low[i - 1]) / 2)) and Low[i] < Low[i - 1]:
            ExtBuffer[i] = 1.0
        if ((i > 2 and Low[i - 1] <= Low[i - 2]) and Close[i - 1] > ((High[i - 1] + Low[i - 1]) / 2)) and High[i] > High[i - 1]:
            ExtBuffer[i] = 2.0
        i += 1
    return rates_total

# ---- global variables initialised from expressions
ColorOf = Arr.of([CLR_NONE, _uint(Red), _uint(Blue)], fill=0, dyn=False, size=3)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Reversalbar(_MQL5Indicator):
    name = 'reversalbar'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

