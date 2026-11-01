"""ticker_satl — converted from MQL5: MQL5 Indicators/Ticker_SATL/ticker_satl.mq5

Copyright: Copyright © 2007, mandorr@gmail.com; Link: mandorr@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, mandorr@gmail.com', 'link': 'mandorr@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16748574, 8036607]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Ticker_SATL'}, 'levels': [], 'description': [], 'name': 'ticker_satl', 'source': 'MQL5 Indicators/Ticker_SATL/ticker_satl.mq5', 'folder': 'Ticker_SATL', 'inputs': [], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
min_rates_total = 0
SATLPeriod = 0
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
SATLTable = Arr.of([0.0982862174, 0.0975682269, 0.0961401078, 0.0940230544, 0.091243709, 0.0878391006, 0.0838544303, 0.079340635, 0.0743569346, 0.0689666682, 0.0632381578, 0.0572428925, 0.0510534242, 0.0447468229, 0.038395995, 0.0320735368, 0.0258537721, 0.0198005183, 0.0139807863, 0.0084512448, 0.0032639979, -0.0015350359, -0.0059060082, -0.0098190256, -0.0132507215, -0.0161875265, -0.0186164872, -0.0205446727, -0.0219739146, -0.0229204861, -0.0234080863, -0.0234566315, -0.0231017777, -0.02237969, -0.0213300463, -0.0199924534, -0.0184126992, -0.0166377699, -0.0147139428, -0.0126796776, -0.0105938331, -0.008473677, -0.006384185, -0.0043466731, -0.0023956944, -0.000553518, 0.0011421469, 0.0026845693, 0.0040471369, 0.0052380201, 0.0062194591, 0.0070340085, 0.0076266453, 0.0080376628, 0.0083037666, 0.0083694798, 0.0082901022, 0.0080741359, 0.007754382, 0.0073260526, 0.0068163569, 0.0062325477, 0.0056078229, 0.0049516078, 0.0161380976], fill=0.0)

def OnInit():
    global SATLPeriod, min_rates_total
    SATLPeriod = ArraySize(SATLTable)
    min_rates_total = SATLPeriod
    SetIndexBuffer(0, ExtABuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtBBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Ticker_SATL')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (SATLPeriod - 1 + begin):
        return 0
    first = 0
    bar = 0
    iii = 0
    SATL = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = SATLPeriod - 1 + begin
        if begin > 0:
            PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, begin + SATLPeriod)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        ExtABuffer[bar] = price[bar]
        SATL = 0.0
        iii = 0
        for iii in range(iii, SATLPeriod):
            SATL += SATLTable[iii] * price[bar - iii]
        else:
            iii = _range_end(iii, SATLPeriod, 1)
        ExtBBuffer[bar] = SATL
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TickerSatl(_MQL5Indicator):
    name = 'ticker_satl'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

