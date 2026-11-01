"""minpricechange — converted from MQL5: MQL5 Indicators/MinPriceChange/minpricechange.mq5

The signal is formed if the changes sum calculated on the last bar 
is less, than the smallest of sums calculated on the specified number of previous bars.
Copyright: Copyright 2013, Rone.; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2013, Rone.', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 5}, 'colors': {1: [16711680], 2: [255], 3: [65280]}, 'widths': {1: 2, 2: 2, 3: 3}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Current Change Sum', 2: 'Min Change Sum', 3: 'Signal'}, 'levels': [], 'description': ['The signal is formed if the changes sum calculated on the last bar ', 'is less, than the smallest of sums calculated on the specified number of previous bars.'], 'name': 'minpricechange', 'source': 'MQL5 Indicators/MinPriceChange/minpricechange.mq5', 'folder': 'MinPriceChange', 'inputs': [{'mql': 'InpChangesPeriod', 'py': 'InpChangesPeriod', 'param': 'InpChangesPeriod', 'type': 'int', 'default': 4, 'label': 'Changes Period', 'sinput': False}, {'mql': 'InpCheckPeriod', 'py': 'InpCheckPeriod', 'param': 'InpCheckPeriod', 'type': 'int', 'default': 10, 'label': 'Check Period', 'sinput': False}, {'mql': 'InpAbsChange', 'py': 'InpAbsChange', 'param': 'InpAbsChange', 'type': 'bool', 'default': False, 'label': 'Abs Change', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpChangesPeriod = _input('InpChangesPeriod', 4)  # Changes Period
InpCheckPeriod = _input('InpCheckPeriod', 10)  # Check Period
InpAbsChange = _input('InpAbsChange', False)  # Abs Change
CurrentSumBuffer = Arr(0, 0.0)
MinSumBuffer = Arr(0, 0.0)
SignalBuffer = Arr(0, 0.0)
changes_period = 0
check_period = 0
min_required_bars = 0

def OnInit():
    global changes_period, check_period, min_required_bars
    if InpChangesPeriod < 1 or InpCheckPeriod < 2:
        changes_period = 3
        check_period = 10
        printf('Incorrect input value InpChangesPeriod = %d or/and InpCheckPeriod =%d. Indicator will use values %d and %d respectively.', InpChangesPeriod, InpCheckPeriod, changes_period, check_period)
    else:
        changes_period = InpChangesPeriod
        check_period = InpCheckPeriod
    min_required_bars = changes_period + check_period + 1
    SetIndexBuffer(0, CurrentSumBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, MinSumBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, SignalBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    for plot in range(0, 3):
        PlotIndexSetInteger(plot, PLOT_DRAW_BEGIN, min_required_bars - 1)
        PlotIndexSetInteger(plot, PLOT_SHIFT, 0)
        PlotIndexSetDouble(plot, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Min Price Change (' + _str(changes_period) + ', ' + _str(check_period) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, begin, price):
    change_start_bar = 0
    check_start_bar = 0
    signal_start_bar = 0
    if rates_total < min_required_bars:
        Print('Not enough bars for calculations.')
        return 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        change_start_bar = changes_period
        check_start_bar = change_start_bar + check_period
        signal_start_bar = check_start_bar + 1
    else:
        change_start_bar = prev_calculated - 1
        check_start_bar = change_start_bar
        signal_start_bar = change_start_bar
    for bar in range(change_start_bar, rates_total):
        sum_ = 0.0
        for shift in range(bar - changes_period + 1, bar + 1):
            if InpAbsChange:
                sum_ += MathAbs(price[shift] - price[shift - 1])
            else:
                sum_ += price[shift] - price[shift - 1]
        CurrentSumBuffer[bar] = MathAbs(sum_)
    for bar in range(check_start_bar, rates_total):
        MinSumBuffer[bar] = CurrentSumBuffer[ArrayMinimum(CurrentSumBuffer, bar - check_period, check_period)]
    for bar in range(signal_start_bar, rates_total):
        SignalBuffer[bar] = EMPTY_VALUE
        if CurrentSumBuffer[bar] < MinSumBuffer[bar] and CurrentSumBuffer[bar - 1] >= MinSumBuffer[bar - 1]:
            SignalBuffer[bar] = MinSumBuffer[bar]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Minpricechange(_MQL5Indicator):
    name = 'minpricechange'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpChangesPeriod': 4,  # Changes Period
        'InpCheckPeriod': 10,  # Check Period
        'InpAbsChange': False,  # Abs Change
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

