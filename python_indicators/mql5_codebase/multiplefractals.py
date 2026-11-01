"""MultipleFractals — converted from MQL5: MQL5 Indicators/MultipleFractals/MultipleFractals.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 20, 'indicator_plots': 20}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5, 15: 5, 16: 5, 17: 5, 18: 5, 19: 5, 20: 5}, 'colors': {1: [255], 2: [16711680], 3: [255], 4: [16711680], 5: [255], 6: [16711680], 7: [255], 8: [16711680], 9: [255], 10: [16711680], 11: [255], 12: [16711680], 13: [255], 14: [16711680], 15: [255], 16: [16711680], 17: [255], 18: [16711680], 19: [255], 20: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0}, 'labels': {1: 'FractalUP1', 2: 'FractalDN1', 3: 'FractalUP2', 4: 'FractalDN2', 5: 'FractalUP3', 6: 'FractalDN3', 7: 'FractalUP4', 8: 'FractalDN4', 9: 'FractalUP5', 10: 'FractalDN5', 11: 'FractalUP6', 12: 'FractalDN6', 13: 'FractalUP7', 14: 'FractalDN7', 15: 'FractalUP8', 16: 'FractalDN8', 17: 'FractalUP9', 18: 'FractalDN9', 19: 'FractalUP10', 20: 'FractalDN10'}, 'levels': [], 'description': [], 'name': 'MultipleFractals', 'source': 'MQL5 Indicators/MultipleFractals/MultipleFractals.mq5', 'folder': 'MultipleFractals', 'inputs': [{'mql': 'InpMinFrame', 'py': 'InpMinFrame', 'param': 'InpMinFrame', 'type': 'uint', 'default': 2, 'label': 'Min dimension of a fractal', 'sinput': False}, {'mql': 'InpMaxFrame', 'py': 'InpMaxFrame', 'param': 'InpMaxFrame', 'type': 'uint', 'default': 10, 'label': 'Max dimension of a fractal', 'sinput': False}, {'mql': 'InpUseLastBar', 'py': 'InpUseLastBar', 'param': 'InpUseLastBar', 'type': 'int', 'default': 0, 'label': 'Use last bar', 'sinput': False}, {'mql': 'InpColorUP', 'py': 'InpColorUP', 'param': None, 'type': 'color', 'default': 255, 'label': 'Upper fractals color', 'sinput': False}, {'mql': 'InpColorDN', 'py': 'InpColorDN', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Lower fractals color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpMinFrame = _input('InpMinFrame', 2)  # Min dimension of a fractal
InpMaxFrame = _input('InpMaxFrame', 10)  # Max dimension of a fractal
InpUseLastBar = _input('InpUseLastBar', INPUT_NO)  # Use last bar
InpColorUP = _input('InpColorUP', clrRed)  # Upper fractals color
InpColorDN = _input('InpColorDN', clrBlue)  # Lower fractals color
min_frame = 0
max_frame = 0

class SDataBuffer(MqlObject):
    _q_fields = ('BufferUP', 'BufferDN')
    def __init__(self, *args):
        self.BufferUP = Arr(0, 0.0)
        self.BufferDN = Arr(0, 0.0)

def OnInit():
    global max_frame, min_frame
    min_frame = (1 if (InpMinFrame < 1) else 9 if (InpMinFrame > 9) else InpMinFrame)
    max_frame = (10 if (InpMaxFrame > 10) else (min_frame + 1) if (_int(InpMaxFrame) <= min_frame) else InpMaxFrame)
    for i in range(0, 10):
        buff1 = i * 2
        buff2 = buff1 + 1
        code = 140 + i
        SetIndexBuffer(buff1, Data[i].BufferUP, INDICATOR_DATA)
        SetIndexBuffer(buff2, Data[i].BufferDN, INDICATOR_DATA)
        PlotIndexSetInteger(buff1, PLOT_ARROW, code)
        PlotIndexSetInteger(buff2, PLOT_ARROW, code)
        PlotIndexSetInteger(buff1, PLOT_LINE_COLOR, InpColorUP)
        PlotIndexSetInteger(buff2, PLOT_LINE_COLOR, InpColorDN)
        PlotIndexSetString(buff1, PLOT_LABEL, _str(i + 1) + '-dimension up fractal')
        PlotIndexSetString(buff2, PLOT_LABEL, _str(i + 1) + '-dimension down fractal')
        ArraySetAsSeries(Data[i].BufferUP, True)
        ArraySetAsSeries(Data[i].BufferDN, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Multiple fractals')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < max_frame:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - max_frame - 1
        for i in range(0, 10):
            ArrayInitialize(Data[i].BufferUP, EMPTY_VALUE)
            ArrayInitialize(Data[i].BufferDN, EMPTY_VALUE)
    end = (0 if InpUseLastBar else 1)
    begin = fmax(limit, max_frame)
    for i in range(begin, end - 1, -1):
        for j in range(0, 10):
            Data[j].BufferUP[i] = EMPTY_VALUE
            Data[j].BufferDN[i] = EMPTY_VALUE
        count = fmin(i - end, max_frame)
        if count >= min_frame:
            UpFractalStatus = FindUP(i, count, high)
            if UpFractalStatus >= min_frame:
                Data[UpFractalStatus - 1].BufferUP[i] = high[i]
            DnFractalStatus = FindDN(i, count, low)
            if DnFractalStatus >= min_frame:
                Data[DnFractalStatus - 1].BufferDN[i] = low[i]
    return rates_total

def FindUP(index, count, high):
    for i in range(1, count + 1):
        if high[index + i] > high[index] or high[index - i] > high[index]:
            return i - 1
    return WRONG_VALUE

def FindDN(index, count, low):
    for i in range(1, count + 1):
        if low[index + i] < low[index] or low[index - i] < low[index]:
            return i - 1
    return WRONG_VALUE

# ---- global variables initialised from expressions
Data = Arr(10, 0, dyn=False, factory=SDataBuffer)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MultipleFractals(_MQL5Indicator):
    name = 'MultipleFractals'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMinFrame': 2,  # Min dimension of a fractal
        'InpMaxFrame': 10,  # Max dimension of a fractal
        'InpUseLastBar': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Use last bar
    }

