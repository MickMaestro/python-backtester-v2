"""fatl_ — converted from MQL5: MQL5 Indicators/FATL/fatl_.mq5

Copyright: Copyright 2002, Finware.ru Ltd.; Link: http://www.finware.ru/; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2002, Finware.ru Ltd.', 'link': 'http://www.finware.ru/', 'version': '2.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'FATL'}, 'levels': [], 'description': [], 'name': 'fatl_', 'source': 'MQL5 Indicators/FATL/fatl_.mq5', 'folder': 'FATL', 'inputs': [{'mql': 'FATLShift', 'py': 'FATLShift', 'param': 'FATLShift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of moving average in bars', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FATLShift = _input('FATLShift', 0)  # Horizontal shift of moving average in bars
FATLPeriod = 0
ExtLineBuffer = Arr(0, 0.0)
FATLTable = Arr.of([0.436040945, 0.3658689069, 0.2460452079, 0.1104506886, -0.0054034585, -0.0760367731, -0.0933058722, -0.0670110374, -0.0190795053, 0.0259609206, 0.0502044896, 0.0477818607, 0.0249252327, -0.0047706151, -0.0272432537, -0.0338917071, -0.0244141482, -0.0055774838, 0.0128149838, 0.0226522218, 0.0208778257, 0.0100299086, -0.0036771622, -0.013674485, -0.0160483392, -0.0108597376, -0.0016060704, 0.0069480557, 0.0110573605, 0.0095711419, 0.0040444064, -0.0023824623, -0.0067093714, -0.00720034, -0.004771771, 0.0005541115, 0.000786016, 0.0130129076, 0.0040364019], fill=0.0)

def OnInit():
    global FATLPeriod
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, FATLShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, FATLPeriod)
    shortname = Box("")
    StringConcatenate(shortname, 'FATL(', FATLShift, ')')
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    FATLPeriod = ArraySize(FATLTable)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, FATLPeriod)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (FATLPeriod - 1 + begin):
        return 0
    first = 0
    bar = 0
    iii = 0
    FATL = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = FATLPeriod - 1 + begin
        if begin > 0:
            PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, begin + FATLPeriod)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        FATL = 0.0
        iii = 0
        for iii in range(iii, FATLPeriod):
            FATL += FATLTable[iii] * price[bar - iii]
        else:
            iii = _range_end(iii, FATLPeriod, 1)
        ExtLineBuffer[bar] = FATL
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Fatl(_MQL5Indicator):
    name = 'fatl_'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FATLShift': 0,  # Horizontal shift of moving average in bars
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

