"""satl — converted from MQL5: MQL5 Indicators/SATL/satl.mq5

Copyright: Copyright 2002, Finware.ru Ltd.; Link: http://www.finware.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2002, Finware.ru Ltd.', 'link': 'http://www.finware.ru/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'SATL'}, 'levels': [], 'description': [], 'name': 'satl', 'source': 'MQL5 Indicators/SATL/satl.mq5', 'folder': 'SATL', 'inputs': [{'mql': 'SATLShift', 'py': 'SATLShift', 'param': 'SATLShift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the average in bars', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SATLShift = _input('SATLShift', 0)  # Horizontal shift of the average in bars
SATLPeriod = 65
ExtLineBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, SATLShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, SATLPeriod)
    shortname = Box("")
    StringConcatenate(shortname, 'SATL(', SATLShift, ')')
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (SATLPeriod - 1 + begin):
        return 0
    first = 0
    bar = 0
    SATL = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = SATLPeriod - 1 + begin
        if begin > 0:
            PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, begin + SATLPeriod)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        SATL = (0.0982862174 * price[bar - 0]) + (0.0975682269 * price[bar - 1]) + (0.0961401078 * price[bar - 2]) + (0.0940230544 * price[bar - 3]) + (0.091243709 * price[bar - 4]) + (0.0878391006 * price[bar - 5]) + (0.0838544303 * price[bar - 6]) + (0.079340635 * price[bar - 7]) + (0.0743569346 * price[bar - 8]) + (0.0689666682 * price[bar - 9]) + (0.0632381578 * price[bar - 10]) + (0.0572428925 * price[bar - 11]) + (0.0510534242 * price[bar - 12]) + (0.0447468229 * price[bar - 13]) + (0.038395995 * price[bar - 14]) + (0.0320735368 * price[bar - 15]) + (0.0258537721 * price[bar - 16]) + (0.0198005183 * price[bar - 17]) + (0.0139807863 * price[bar - 18]) + (0.0084512448 * price[bar - 19]) + (0.0032639979 * price[bar - 20]) - (0.0015350359 * price[bar - 21]) - (0.0059060082 * price[bar - 22]) - (0.0098190256 * price[bar - 23]) - (0.0132507215 * price[bar - 24]) - (0.0161875265 * price[bar - 25]) - (0.0186164872 * price[bar - 26]) - (0.0205446727 * price[bar - 27]) - (0.0219739146 * price[bar - 28]) - (0.0229204861 * price[bar - 29]) - (0.0234080863 * price[bar - 30]) - (0.0234566315 * price[bar - 31]) - (0.0231017777 * price[bar - 32]) - (0.02237969 * price[bar - 33]) - (0.0213300463 * price[bar - 34]) - (0.0199924534 * price[bar - 35]) - (0.0184126992 * price[bar - 36]) - (0.0166377699 * price[bar - 37]) - (0.0147139428 * price[bar - 38]) - (0.0126796776 * price[bar - 39]) - (0.0105938331 * price[bar - 40]) - (0.008473677 * price[bar - 41]) - (0.006384185 * price[bar - 42]) - (0.0043466731 * price[bar - 43]) - (0.0023956944 * price[bar - 44]) - (0.000553518 * price[bar - 45]) + (0.0011421469 * price[bar - 46]) + (0.0026845693 * price[bar - 47]) + (0.0040471369 * price[bar - 48]) + (0.0052380201 * price[bar - 49]) + (0.0062194591 * price[bar - 50]) + (0.0070340085 * price[bar - 51]) + (0.0076266453 * price[bar - 52]) + (0.0080376628 * price[bar - 53]) + (0.0083037666 * price[bar - 54]) + (0.0083694798 * price[bar - 55]) + (0.0082901022 * price[bar - 56]) + (0.0080741359 * price[bar - 57]) + (0.007754382 * price[bar - 58]) + (0.0073260526 * price[bar - 59]) + (0.0068163569 * price[bar - 60]) + (0.0062325477 * price[bar - 61]) + (0.0056078229 * price[bar - 62]) + (0.0049516078 * price[bar - 63]) + (0.0161380976 * price[bar - 64])
        ExtLineBuffer[bar] = SATL
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Satl(_MQL5Indicator):
    name = 'satl'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SATLShift': 0,  # Horizontal shift of the average in bars
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

