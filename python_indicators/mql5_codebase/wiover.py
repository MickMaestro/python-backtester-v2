"""wiover — converted from MQL5: MQL5 Indicators/WiOver/wiover.mq5

Copyright: Copyright © 2010, Murad Ismayilov; Link: http://www.wmlab.org/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Murad Ismayilov', 'link': 'http://www.wmlab.org/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {}, 'levels': [], 'description': [], 'name': 'wiover', 'source': 'MQL5 Indicators/WiOver/wiover.mq5', 'folder': 'WiOver', 'inputs': [{'mql': 'WiOverPeriod', 'py': 'WiOverPeriod', 'param': 'WiOverPeriod', 'type': 'int', 'default': 9, 'label': 'Indicator period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
WiOverPeriod = _input('WiOverPeriod', 9)  # Indicator period
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
BullsBuffer = Arr(0, 0.0)
BearsBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = WiOverPeriod
    SetIndexBuffer(0, BullsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(0, PLOT_LABEL, 'WiOver(' + _str(WiOverPeriod) + ') ' + 'SellLimit')
    SetIndexBuffer(1, BearsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(1, PLOT_LABEL, 'WiOver(' + _str(WiOverPeriod) + ') ' + 'BuyLimit')
    shortname = Box("")
    StringConcatenate(shortname, 'WiOver(', WiOverPeriod, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    k = 0
    k1 = 0
    sum_ = 0.0
    abs_ = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        sum_ = 0.0
        k = bar - WiOverPeriod + 1
        while k <= bar:
            k1 = k - 1
            if high[k1] > low[k] and low[k] > low[k1]:
                sum_ += high[k1] - low[k1] - _fdiv(low[k], high[k1])
            if low[k1] < high[k] and high[k] < high[k1]:
                sum_ += high[k1] - low[k1] - _fdiv(high[k], low[k1])
            k += 1
        abs_ = (sum_ * (high[bar] - low[bar])) / WiOverPeriod
        BullsBuffer[bar] = low[bar] - abs_
        BearsBuffer[bar] = high[bar] + abs_
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Wiover(_MQL5Indicator):
    name = 'wiover'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'WiOverPeriod': 9,  # Indicator period
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

