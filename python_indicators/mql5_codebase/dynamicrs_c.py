"""dynamicrs_c — converted from MQL5: MQL5 Indicators/DynamicRS_C/dynamicrs_c.mq5

Copyright: Copyright © 2007, Nick A. Zhilin; Link: rebus58@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Nick A. Zhilin', 'link': 'rebus58@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16711935, 65535, 14822282]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'DynamicRS_C'}, 'levels': [], 'description': [], 'name': 'dynamicrs_c', 'source': 'MQL5 Indicators/DynamicRS_C/dynamicrs_c.mq5', 'folder': 'DynamicRS_C', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 5, 'label': 'Depth of the first smoothing', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Vertical shift of the indicator in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 5)  # Depth of the first smoothing
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # Vertical shift of the indicator in points
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0

def OnInit():
    global dPriceShift, min_rates_total
    min_rates_total = _int(Length + 1)
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    shortname = Box("")
    StringConcatenate(shortname, 'DynamicRS_C(', Length, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total - 1
        IndBuffer[first - 1] = close[first - 1]
        ColorIndBuffer[first - 1] = 1.0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        ColorIndBuffer[bar] = 1.0
        if (high[bar] < high[bar - 1] and high[bar] < high[bar - Length]) and high[bar] < IndBuffer[bar - 1]:
            IndBuffer[bar] = high[bar] + PriceShift
            if ColorIndBuffer[bar - 1] == 2:
                ColorIndBuffer[bar] = 1.0
            else:
                ColorIndBuffer[bar] = 0.0
        elif (low[bar] > low[bar - 1] and low[bar] > low[bar - Length]) and low[bar] > IndBuffer[bar - 1]:
            IndBuffer[bar] = low[bar] + PriceShift
            if ColorIndBuffer[bar - 1] == 0:
                ColorIndBuffer[bar] = 1.0
            else:
                ColorIndBuffer[bar] = 2.0
        else:
            IndBuffer[bar] = IndBuffer[bar - 1]
            ColorIndBuffer[bar] = ColorIndBuffer[bar - 1]
            if ColorIndBuffer[bar] == 1:
                if ColorIndBuffer[bar - 2] == 0:
                    ColorIndBuffer[bar] = 2.0
                if ColorIndBuffer[bar - 2] == 2:
                    ColorIndBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DynamicrsC(_MQL5Indicator):
    name = 'dynamicrs_c'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Length': 5,  # Depth of the first smoothing
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'PriceShift': 0,  # Vertical shift of the indicator in points
    }

