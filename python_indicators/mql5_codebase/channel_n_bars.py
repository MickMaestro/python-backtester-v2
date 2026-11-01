"""Channel N Bars — converted from MQL5: MQL5 Indicators/Channel N Bars/Channel N Bars.mq5

Copyright: Copyright © 2022, Vladimir Karputov; Link: https://www.mql5.com/en/users/barabashkakvn; Version: 1.003

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2022, Vladimir Karputov', 'link': 'https://www.mql5.com/en/users/barabashkakvn', 'version': '1.003', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [3329434], 2: [3329434]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 2, 2: 2}, 'labels': {1: 'Lowest', 2: 'Highest'}, 'levels': [], 'description': [], 'name': 'Channel N Bars', 'source': 'MQL5 Indicators/Channel N Bars/Channel N Bars.mq5', 'folder': 'Channel N Bars', 'inputs': [{'mql': 'InputNBars', 'py': 'InputNBars', 'param': 'InputNBars', 'type': 'int', 'default': 9, 'label': 'N Bars', 'sinput': False}, {'mql': 'InpPrice', 'py': 'InpPrice', 'param': 'InpPrice', 'type': 'int', 'default': 1, 'label': 'Cannel price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_PRICE
hl = 0
oc = 1
_enum('ENUM_PRICE', {0: 'hl', 1: 'oc'})

# ---- inputs and global variables
InputNBars = _input('InputNBars', 9)  # N Bars
InpPrice = _input('InpPrice', oc)  # Cannel price
LowestBuffer = Arr(0, 0.0)
HighestBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, LowestBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, HighestBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < InputNBars:
        return 0
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = InputNBars
    for i in range(limit, rates_total):
        if InpPrice == hl:
            LowestBuffer[i] = low[ArrayMinimum(low, i - InputNBars + 1, InputNBars)]
            HighestBuffer[i] = high[ArrayMaximum(high, i - InputNBars + 1, InputNBars)]
        else:
            LowestBuffer[i] = close[ArrayMinimum(close, i - InputNBars + 1, InputNBars)]
            HighestBuffer[i] = open[ArrayMaximum(open, i - InputNBars + 1, InputNBars)]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ChannelNBars(_MQL5Indicator):
    name = 'Channel N Bars'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InputNBars': 9,  # N Bars
        'InpPrice': _Choice({0: 'high low', 1: 'open close'}, default=1),  # Cannel price
    }

