"""fatl — converted from MQL5: MQL5 Indicators/FATL/fatl.mq5

Copyright: Copyright 2002, Finware.ru Ltd.; Link: http://www.finware.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2002, Finware.ru Ltd.', 'link': 'http://www.finware.ru/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'FATL'}, 'levels': [], 'description': [], 'name': 'fatl', 'source': 'MQL5 Indicators/FATL/fatl.mq5', 'folder': 'FATL', 'inputs': [{'mql': 'FATLShift', 'py': 'FATLShift', 'param': 'FATLShift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of moving average in bars', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FATLShift = _input('FATLShift', 0)  # Horizontal shift of moving average in bars
FATLPeriod = 39
ExtLineBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, FATLShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, FATLPeriod)
    shortname = Box("")
    StringConcatenate(shortname, 'FATL(', FATLShift, ')')
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (FATLPeriod - 1 + begin):
        return 0
    first = 0
    bar = 0
    FATL = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = FATLPeriod - 1 + begin
        if begin > 0:
            PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, begin + FATLPeriod)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        FATL = (0.436040945 * price[bar - 0]) + (0.3658689069 * price[bar - 1]) + (0.2460452079 * price[bar - 2]) + (0.1104506886 * price[bar - 3]) - (0.0054034585 * price[bar - 4]) - (0.0760367731 * price[bar - 5]) - (0.0933058722 * price[bar - 6]) - (0.0670110374 * price[bar - 7]) - (0.0190795053 * price[bar - 8]) + (0.0259609206 * price[bar - 9]) + (0.0502044896 * price[bar - 10]) + (0.0477818607 * price[bar - 11]) + (0.0249252327 * price[bar - 12]) - (0.0047706151 * price[bar - 13]) - (0.0272432537 * price[bar - 14]) - (0.0338917071 * price[bar - 15]) - (0.0244141482 * price[bar - 16]) - (0.0055774838 * price[bar - 17]) + (0.0128149838 * price[bar - 18]) + (0.0226522218 * price[bar - 19]) + (0.0208778257 * price[bar - 20]) + (0.0100299086 * price[bar - 21]) - (0.0036771622 * price[bar - 22]) - (0.013674485 * price[bar - 23]) - (0.0160483392 * price[bar - 24]) - (0.0108597376 * price[bar - 25]) - (0.0016060704 * price[bar - 26]) + (0.0069480557 * price[bar - 27]) + (0.0110573605 * price[bar - 28]) + (0.0095711419 * price[bar - 29]) + (0.0040444064 * price[bar - 30]) - (0.0023824623 * price[bar - 31]) - (0.0067093714 * price[bar - 32]) - (0.00720034 * price[bar - 33]) - (0.004771771 * price[bar - 34]) + (0.0005541115 * price[bar - 35]) + (0.000786016 * price[bar - 36]) + (0.0130129076 * price[bar - 37]) + (0.0040364019 * price[bar - 38])
        ExtLineBuffer[bar] = FATL
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Fatl(_MQL5Indicator):
    name = 'fatl'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FATLShift': 0,  # Horizontal shift of moving average in bars
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

