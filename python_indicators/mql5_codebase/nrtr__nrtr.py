"""nrtr — converted from MQL5: MQL5 Indicators/NRTR/nrtr.mq5

Copyright: MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [16748574], 2: [255], 3: [14772545], 4: [3937500]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Support', 2: 'Resistance', 3: 'UpTarget', 4: 'DnTarget'}, 'levels': [], 'description': [], 'name': 'nrtr', 'source': 'MQL5 Indicators/NRTR/nrtr.mq5', 'folder': 'NRTR', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 40, 'label': 'period', 'sinput': False}, {'mql': 'k', 'py': 'k', 'param': 'k', 'type': 'double', 'default': 2.0, 'label': 'k', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
period = _input('period', 40)  # period
k = _input('k', 2.0)  # k
SupportBuffer = Arr(0, 0.0)
ResistanceBuffer = Arr(0, 0.0)
UpTargetBuffer = Arr(0, 0.0)
DnTargetBuffer = Arr(0, 0.0)
Trend = Arr(0, 0.0)
ATRBuffer = Arr(0, 0.0)
Handle_v = 0

def OnInit():
    global Handle_v
    SetIndexBuffer(0, SupportBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    SetIndexBuffer(1, ResistanceBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    SetIndexBuffer(2, UpTargetBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_ARROW, 158)
    SetIndexBuffer(3, DnTargetBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_ARROW, 158)
    SetIndexBuffer(4, Trend, INDICATOR_DATA)
    SetIndexBuffer(5, ATRBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0)
    Handle_v = iATR(Symbol(), PERIOD_CURRENT, period)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_error
    start = 0
    if prev_calculated == 0:
        _s_OnCalculate_error = True
    if _s_OnCalculate_error:
        ArrayInitialize(Trend, 0)
        ArrayInitialize(UpTargetBuffer, 0)
        ArrayInitialize(DnTargetBuffer, 0)
        ArrayInitialize(SupportBuffer, 0)
        ArrayInitialize(ResistanceBuffer, 0)
        start = period
        _s_OnCalculate_error = False
    else:
        start = prev_calculated - 1
    if CopyBuffer(Handle_v, 0, 0, rates_total - start, ATRBuffer) == -1:
        _s_OnCalculate_error = True
        return 0
    for i in range(start, rates_total):
        Trend[i] = Trend[i - 1]
        UpTargetBuffer[i] = UpTargetBuffer[i - 1]
        DnTargetBuffer[i] = DnTargetBuffer[i - 1]
        SupportBuffer[i] = SupportBuffer[i - 1]
        ResistanceBuffer[i] = ResistanceBuffer[i - 1]
        _sw1 = _int(Trend[i])
        if _sw1 == 2:
            if low[i] > UpTargetBuffer[i]:
                UpTargetBuffer[i] = close[i]
                SupportBuffer[i] = close[i] - (k * ATRBuffer[i])
            if close[i] < SupportBuffer[i]:
                DnTargetBuffer[i] = close[i]
                ResistanceBuffer[i] = close[i] + (k * ATRBuffer[i])
                Trend[i] = 3.0
                UpTargetBuffer[i] = 0.0
                SupportBuffer[i] = 0.0
        elif _sw1 == 3:
            if high[i] < DnTargetBuffer[i]:
                DnTargetBuffer[i] = close[i]
                ResistanceBuffer[i] = close[i] + (k * ATRBuffer[i])
            if close[i] > ResistanceBuffer[i]:
                UpTargetBuffer[i] = close[i]
                SupportBuffer[i] = close[i] - (k * ATRBuffer[i])
                Trend[i] = 2.0
                DnTargetBuffer[i] = 0.0
                ResistanceBuffer[i] = 0.0
        elif _sw1 == 0:
            UpTargetBuffer[i] = close[i]
            DnTargetBuffer[i] = close[i]
            Trend[i] = 1.0
        elif _sw1 == 1:
            if low[i] > UpTargetBuffer[i]:
                UpTargetBuffer[i] = close[i]
                SupportBuffer[i] = close[i] - (k * ATRBuffer[i])
                Trend[i] = 2.0
                DnTargetBuffer[i] = 0.0
            if high[i] < DnTargetBuffer[i]:
                DnTargetBuffer[i] = close[i]
                ResistanceBuffer[i] = close[i] + (k * ATRBuffer[i])
                Trend[i] = 3.0
                UpTargetBuffer[i] = 0.0
    return rates_total

# ---- static local variables
_s_OnCalculate_error = True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Nrtr(_MQL5Indicator):
    name = 'nrtr'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 40,  # period
        'k': 2.0,  # k
    }

