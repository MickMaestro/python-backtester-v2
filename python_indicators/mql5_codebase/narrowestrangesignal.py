"""narrowestrangesignal — converted from MQL5: MQL5 Indicators/Narrowest Range Signal/narrowestrangesignal.mq5

The signal occurs if the channel range calculated on the last bar is less 
than the smallest range, which calculated on the specified number of previous bars.
Copyright: Copyright 2013, Rone.; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2013, Rone.', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 5}, 'colors': {1: [16711680], 2: [255], 3: [65280]}, 'widths': {1: 2, 2: 2, 3: 3}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'CurrentRange', 2: 'MinRange', 3: 'Signal'}, 'levels': [], 'description': ['The signal occurs if the channel range calculated on the last bar is less ', 'than the smallest range, which calculated on the specified number of previous bars.'], 'name': 'narrowestrangesignal', 'source': 'MQL5 Indicators/Narrowest Range Signal/narrowestrangesignal.mq5', 'folder': 'Narrowest Range Signal', 'inputs': [{'mql': 'InpBarsInRange', 'py': 'InpBarsInRange', 'param': 'InpBarsInRange', 'type': 'int', 'default': 3, 'label': 'Bars in Range', 'sinput': False}, {'mql': 'InpCheckPeriod', 'py': 'InpCheckPeriod', 'param': 'InpCheckPeriod', 'type': 'int', 'default': 10, 'label': 'Check Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpBarsInRange = _input('InpBarsInRange', 3)  # Bars in Range
InpCheckPeriod = _input('InpCheckPeriod', 10)  # Check Period
CurrentRangeBuffer = Arr(0, 0.0)
MinRangeBuffer = Arr(0, 0.0)
SignalBuffer = Arr(0, 0.0)
bars_in_range = 0
check_period = 0
min_required_bars = 0

def OnInit():
    global bars_in_range, check_period, min_required_bars
    if InpCheckPeriod <= 2 or InpBarsInRange < 1:
        bars_in_range = 3
        check_period = 10
        printf('Incorrect input value InpBarsInChannel = %d or/and InpCheckPeriod = %d. Indicator will use value %d and %d respectively.', InpBarsInRange, InpCheckPeriod, bars_in_range, check_period)
    else:
        bars_in_range = InpBarsInRange
        check_period = InpCheckPeriod
    min_required_bars = bars_in_range + check_period
    SetIndexBuffer(0, CurrentRangeBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, MinRangeBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, SignalBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    for plot in range(0, 3):
        PlotIndexSetInteger(plot, PLOT_DRAW_BEGIN, min_required_bars - 1)
        PlotIndexSetInteger(plot, PLOT_SHIFT, 0)
        PlotIndexSetDouble(plot, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Narrowest Channel Signal (' + _str(bars_in_range) + ', ' + _str(check_period) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    channel_start_bar = 0
    check_start_bar = 0
    signal_start_bar = 0
    if rates_total < min_required_bars:
        Print('Not enough bars for calculations.')
        return 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        channel_start_bar = bars_in_range - 1
        check_start_bar = channel_start_bar + check_period
        signal_start_bar = check_start_bar + 1
    else:
        channel_start_bar = prev_calculated - 1
        check_start_bar = channel_start_bar
        signal_start_bar = channel_start_bar
    for bar in range(channel_start_bar, rates_total):
        max_high = high[ArrayMaximum(high, bar - bars_in_range + 1, bars_in_range)]
        min_low = low[ArrayMinimum(low, bar - bars_in_range + 1, bars_in_range)]
        CurrentRangeBuffer[bar] = max_high - min_low
    for bar in range(check_start_bar, rates_total):
        MinRangeBuffer[bar] = CurrentRangeBuffer[ArrayMinimum(CurrentRangeBuffer, bar - check_period, check_period)]
    for bar in range(signal_start_bar, rates_total):
        SignalBuffer[bar] = EMPTY_VALUE
        if CurrentRangeBuffer[bar] < MinRangeBuffer[bar] and CurrentRangeBuffer[bar - 1] >= MinRangeBuffer[bar - 1]:
            SignalBuffer[bar] = MinRangeBuffer[bar]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Narrowestrangesignal(_MQL5Indicator):
    name = 'narrowestrangesignal'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpBarsInRange': 3,  # Bars in Range
        'InpCheckPeriod': 10,  # Check Period
    }

