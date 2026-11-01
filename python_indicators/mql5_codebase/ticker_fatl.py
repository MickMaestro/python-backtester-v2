"""ticker_fatl — converted from MQL5: MQL5 Indicators/Ticker_FATL/ticker_fatl.mq5

Copyright: Copyright © 2007, mandorr@gmail.com; Link: mandorr@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, mandorr@gmail.com', 'link': 'mandorr@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16776960, 13850042]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Ticker_FATL'}, 'levels': [], 'description': [], 'name': 'ticker_fatl', 'source': 'MQL5 Indicators/Ticker_FATL/ticker_fatl.mq5', 'folder': 'Ticker_FATL', 'inputs': [], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
min_rates_total = 0
FATLPeriod = 0
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
FATLTable = Arr.of([0.436040945, 0.3658689069, 0.2460452079, 0.1104506886, -0.0054034585, -0.0760367731, -0.0933058722, -0.0670110374, -0.0190795053, 0.0259609206, 0.0502044896, 0.0477818607, 0.0249252327, -0.0047706151, -0.0272432537, -0.0338917071, -0.0244141482, -0.0055774838, 0.0128149838, 0.0226522218, 0.0208778257, 0.0100299086, -0.0036771622, -0.013674485, -0.0160483392, -0.0108597376, -0.0016060704, 0.0069480557, 0.0110573605, 0.0095711419, 0.0040444064, -0.0023824623, -0.0067093714, -0.00720034, -0.004771771, 0.0005541115, 0.000786016, 0.0130129076, 0.0040364019], fill=0.0)

def OnInit():
    global FATLPeriod, min_rates_total
    FATLPeriod = ArraySize(FATLTable)
    min_rates_total = FATLPeriod
    SetIndexBuffer(0, ExtABuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtBBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Ticker_FATL')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

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
        ExtABuffer[bar] = price[bar]
        FATL = 0.0
        iii = 0
        for iii in range(iii, FATLPeriod):
            FATL += FATLTable[iii] * price[bar - iii]
        else:
            iii = _range_end(iii, FATLPeriod, 1)
        ExtBBuffer[bar] = FATL
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TickerFatl(_MQL5Indicator):
    name = 'ticker_fatl'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

