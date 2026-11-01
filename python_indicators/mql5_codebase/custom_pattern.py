"""Custom_Pattern — converted from MQL5: MQL5 Indicators/Custom_Pattern/Custom_Pattern.mq5

The indicator provides the user to
specify a custom format pattern candle
and draws patterns on the chart
------------------------------------
U - UP candle (Close>Open)
D - DOWN candle (Close<Open)
N - Nothing (UP or DOWN)
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'DIR', 2: 'REV'}, 'levels': [], 'description': ['The indicator provides the user to', 'specify a custom format pattern candle', 'and draws patterns on the chart', '------------------------------------', 'U - UP candle (Close>Open)', 'D - DOWN candle (Close<Open)', 'N - Nothing (UP or DOWN)'], 'name': 'Custom_Pattern', 'source': 'MQL5 Indicators/Custom_Pattern/Custom_Pattern.mq5', 'folder': 'Custom_Pattern', 'inputs': [{'mql': 'InpPattern', 'py': 'InpPattern', 'param': None, 'type': 'string', 'default': 'UND', 'label': 'Pattern (U - up, N - nothing, D - down)', 'sinput': False}, {'mql': 'InpShowReverce', 'py': 'InpShowReverce', 'param': 'InpShowReverce', 'type': 'int', 'default': 0, 'label': 'Show reverse pattern', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPattern = _input('InpPattern', 'UND')  # Pattern (U - up, N - nothing, D - down)
InpShowReverce = _input('InpShowReverce', INPUT_NO)  # Show reverse pattern
BufferDIR = Arr(0, 0.0)
BufferREV = Arr(0, 0.0)
array = Arr(0, 0)
length = 0
pattern = ""

def OnInit():
    global length, pattern
    pattern = InpPattern
    StringTrimLeft(_GlobRef(globals(), 'pattern'))
    StringTrimRight(_GlobRef(globals(), 'pattern'))
    if not StringToLower(_GlobRef(globals(), 'pattern')):
        Print("Failed to convert characters of string '", pattern, "' to lowercase. Error: ", GetLastError())
        return INIT_FAILED
    length = StringLen(pattern)
    ResetLastError()
    if ArrayResize(array, length) == length:
        StringToCharArray(pattern, array)
    else:
        Print('Error filling the array of characters: ', GetLastError())
        return INIT_FAILED
    SetIndexBuffer(0, BufferDIR, INDICATOR_DATA)
    SetIndexBuffer(1, BufferREV, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 119)
    PlotIndexSetInteger(1, PLOT_ARROW, 119)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Custom pattern')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferDIR, True)
    ArraySetAsSeries(BufferREV, True)
    ArraySetAsSeries(array, False)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (length + 1):
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - length - 1
        ArrayInitialize(BufferDIR, EMPTY_VALUE)
        ArrayInitialize(BufferREV, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        if DirectPattern(i, open, close):
            BufferDIR[i] = high[i]
        if InpShowReverce and ReversePattern(i, open, close):
            BufferREV[i] = low[i]
    return rates_total

def DirectPattern(shift, open, close):
    s = ''
    f = True
    for i in range(1, length + 1):
        s = CharToString(array[length - i])
        if s == 'u' and close[shift + i - 1] <= open[shift + i - 1]:
            f = False
        if s == 'd' and close[shift + i - 1] >= open[shift + i - 1]:
            f = False
    return f

def ReversePattern(shift, open, close):
    s = ''
    f = True
    for i in range(1, length + 1):
        s = CharToString(array[length - i])
        if s == 'u' and close[shift + i - 1] >= open[shift + i - 1]:
            f = False
        if s == 'd' and close[shift + i - 1] <= open[shift + i - 1]:
            f = False
    return f


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CustomPattern(_MQL5Indicator):
    name = 'Custom_Pattern'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpShowReverce': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Show reverse pattern
    }

