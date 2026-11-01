"""chanellonparabolic — converted from MQL5: MQL5 Indicators/ChanellOnParabolic/chanellonparabolic.mq5

The channel built on parabolic
Copyright: Copyright © 2009, Svinozavr; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Svinozavr', 'link': '', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 5, 2: 1, 3: 1}, 'colors': {1: [16748574], 2: [255], 3: [7451452]}, 'widths': {1: 1, 2: 2, 3: 2}, 'styles': {2: 0, 3: 0}, 'labels': {1: ' Parabolic Sar', 2: 'Chanell On Parabolic Upper', 3: 'Chanell On Parabolic Lower'}, 'levels': [], 'description': ['The channel built on parabolic'], 'name': 'chanellonparabolic', 'source': 'MQL5 Indicators/ChanellOnParabolic/chanellonparabolic.mq5', 'folder': 'ChanellOnParabolic', 'inputs': [{'mql': 'Step', 'py': 'Step', 'param': 'Step', 'type': 'double', 'default': 0.02, 'label': 'SAR step', 'sinput': False}, {'mql': 'Maximum', 'py': 'Maximum', 'param': 'Maximum', 'type': 'double', 'default': 0.2, 'label': 'SAR maximum', 'sinput': False}, {'mql': 'Wide', 'py': 'Wide', 'param': 'Wide', 'type': 'int', 'default': 0, 'label': 'minimal allowable channel width in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Step = _input('Step', 0.02)  # SAR step
Maximum = _input('Maximum', 0.2)  # SAR maximum
Wide = _input('Wide', 0)  # minimal allowable channel width in points
LowestBuffer = Arr(0, 0.0)
HighestBuffer = Arr(0, 0.0)
SarBuffer = Arr(0, 0.0)
wide = 0.0
min_rates_total = 0
SAR_Handle = 0

def OnInit():
    global SAR_Handle, min_rates_total, wide
    min_rates_total = 1
    wide = Wide * Point()
    SAR_Handle = iSAR(None, 0, Step, Maximum)
    if SAR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the SAR indicator')
    SetIndexBuffer(0, SarBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, LowestBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, HighestBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(LowestBuffer, True)
    ArraySetAsSeries(HighestBuffer, True)
    ArraySetAsSeries(SarBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    shortname = Box("")
    StringConcatenate(shortname, 'Chanell On Parabolic Sar(', DoubleToString(Step, 2), ', ', DoubleToString(Maximum, 2), ', ', Wide, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_bot, _s_OnCalculate_prev_top
    if BarsCalculated(SAR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    middleprice0 = 0.0
    middleprice1 = 0.0
    top = 0.0
    bot = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
        to_copy = limit + 2
    else:
        limit = rates_total - prev_calculated
        to_copy = limit + 1
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    top = _s_OnCalculate_prev_top
    bot = _s_OnCalculate_prev_bot
    if CopyBuffer(SAR_Handle, 0, 0, to_copy, SarBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        middleprice0 = (high[bar] + low[bar]) / 2
        middleprice1 = (high[bar + 1] + low[bar + 1]) / 2
        if SarBuffer[bar + 1] >= middleprice1 and SarBuffer[bar] < middleprice0:
            if (top - SarBuffer[bar]) > wide:
                bot = SarBuffer[bar]
        if SarBuffer[bar + 1] <= middleprice1 and SarBuffer[bar] > middleprice0:
            if (SarBuffer[bar] - bot) > wide:
                top = SarBuffer[bar]
        HighestBuffer[bar] = top
        LowestBuffer[bar] = bot
        if bar:
            _s_OnCalculate_prev_top = top
            _s_OnCalculate_prev_bot = bot
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_prev_top = 0.0
_s_OnCalculate_prev_bot = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Chanellonparabolic(_MQL5Indicator):
    name = 'chanellonparabolic'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Step': 0.02,  # SAR step
        'Maximum': 0.2,  # SAR maximum
        'Wide': 0,  # minimal allowable channel width in points
    }

