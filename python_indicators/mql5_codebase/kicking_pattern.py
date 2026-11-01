"""Kicking_Pattern — converted from MQL5: MQL5 Indicators/Kicking Pattern/Kicking_Pattern.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Bullish', 2: 'Bearish'}, 'levels': [], 'description': [], 'name': 'Kicking_Pattern', 'source': 'MQL5 Indicators/Kicking Pattern/Kicking_Pattern.mq5', 'folder': 'Kicking Pattern', 'inputs': [{'mql': 'InpShowBullish', 'py': 'InpShowBullish', 'param': 'InpShowBullish', 'type': 'int', 'default': 1, 'label': 'Show bullish patterns', 'sinput': False}, {'mql': 'InpShowBearish', 'py': 'InpShowBearish', 'param': 'InpShowBearish', 'type': 'int', 'default': 1, 'label': 'Show bearish patterns', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpShowBullish = _input('InpShowBullish', INPUT_YES)  # Show bullish patterns
InpShowBearish = _input('InpShowBearish', INPUT_YES)  # Show bearish patterns
BufferBullish = Arr(0, 0.0)
BufferBearish = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BufferBullish, INDICATOR_DATA)
    SetIndexBuffer(1, BufferBearish, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 119)
    PlotIndexSetInteger(1, PLOT_ARROW, 119)
    ArraySetAsSeries(BufferBullish, True)
    ArraySetAsSeries(BufferBearish, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Kicking pattern')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 4
        ArrayInitialize(BufferBullish, EMPTY_VALUE)
        ArrayInitialize(BufferBearish, EMPTY_VALUE)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    for i in range(limit, 0, -1):
        if InpShowBullish:
            if ((close[i] > open[i] and close[i + 1] < open[i + 1]) and close[i + 2] > open[i + 2]) and close[i + 3] < open[i + 3]:
                BufferBullish[i] = high[i]
            else:
                BufferBullish[i] = EMPTY_VALUE
        if InpShowBearish:
            if ((close[i] < open[i] and close[i + 1] > open[i + 1]) and close[i + 2] < open[i + 2]) and close[i + 3] > open[i + 3]:
                BufferBearish[i] = low[i]
            else:
                BufferBearish[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KickingPattern(_MQL5Indicator):
    name = 'Kicking_Pattern'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpShowBullish': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show bullish patterns
        'InpShowBearish': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show bearish patterns
    }

