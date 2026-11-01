"""Swings — converted from MQL5: MQL5 Indicators/Swing Highs and Lows/Swings.mq5

Copyright: Rajesh Nait, Copyright 2023; Link: https://www.mql5.com/en/users/rajeshnait/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Rajesh Nait, Copyright 2023', 'link': 'https://www.mql5.com/en/users/rajeshnait/seller', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16448255], 2: [16448255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: '+S', 2: '-S'}, 'levels': [], 'description': [], 'name': 'Swings', 'source': 'MQL5 Indicators/Swing Highs and Lows/Swings.mq5', 'folder': 'Swing Highs and Lows', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpSwingLowCode = 110  # Swing Low: code for style DRAW_ARROW (font Wingdings)
InpSwingLowShift = 10  # Swing Low: vertical shift of arrows in pixels
InpSwingHighCode = 110  # SwingHigh: code for style DRAW_ARROW (font Wingdings)
InpSwingHighShift = 10  # SwingHigh: vertical shift of arrows in pixels
SwingLowBuffer = Arr(0, 0.0)
SwingHighBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, SwingLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SwingHighBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_ARROW, InpSwingLowCode)
    PlotIndexSetInteger(1, PLOT_ARROW, InpSwingHighCode)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, InpSwingLowShift)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, -InpSwingHighShift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 3:
        return 0
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 2
    for i in range(limit, rates_total - 2):
        SwingLowBuffer[i] = 0.0
        SwingHighBuffer[i] = 0.0
        if i > 0:
            SwingHighBuffer[0] = EMPTY_VALUE
            if high[i + 2] < high[i + 1] and high[i + 1] < high[i]:
                if high[i] > high[i - 1] and high[i - 1] > high[i - 2]:
                    SwingHighBuffer[i] = high[i]
            SwingLowBuffer[0] = EMPTY_VALUE
            if low[i + 2] > low[i + 1] and low[i + 1] > low[i]:
                if low[i] < low[i - 1] and low[i - 1] < low[i - 2]:
                    SwingLowBuffer[i] = low[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Swings(_MQL5Indicator):
    name = 'Swings'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

