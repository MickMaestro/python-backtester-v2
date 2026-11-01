"""instantaneoustrendline — converted from MQL5: MQL5 Indicators/Instantaneous Trendline/instantaneoustrendline.mq5

Copyright: Coded by Witold Wozniak; Link: www.mqlsoft.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Coded by Witold Wozniak', 'link': 'www.mqlsoft.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Instantaneous Trendline', 2: 'Trigger'}, 'levels': [0.0], 'description': [], 'name': 'instantaneoustrendline', 'source': 'MQL5 Indicators/Instantaneous Trendline/instantaneoustrendline.mq5', 'folder': 'Instantaneous Trendline', 'inputs': [{'mql': 'Alpha', 'py': 'Alpha', 'param': 'Alpha', 'type': 'double', 'default': 0.07, 'label': 'Indicator ratio', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Alpha = _input('Alpha', 0.07)  # Indicator ratio
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
ITrendBuffer = Arr(0, 0.0)
TriggerBuffer = Arr(0, 0.0)
min_rates_total = 0
K0 = 0.0
K1 = 0.0
K2 = 0.0
K3 = 0.0
K4 = 0.0

def OnInit():
    global K0, K1, K2, K3, K4, min_rates_total
    min_rates_total = 8 + 3
    A2 = Alpha * Alpha
    K0 = Alpha - (A2 / 4.0)
    K1 = 0.5 * A2
    K2 = Alpha - (0.75 * A2)
    K3 = 2.0 * (1.0 - Alpha)
    K4 = MathPow(1.0 - Alpha, 2)
    SetIndexBuffer(0, ITrendBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 3)
    SetIndexBuffer(1, TriggerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, 3)
    shortname = Box("")
    StringConcatenate(shortname, 'Instantaneous Trendline(', Alpha, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    price0 = 0.0
    price1 = 0.0
    price2 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 3
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price0 = (high[bar] + low[bar]) / 2.0
        price1 = (high[bar - 1] + low[bar - 1]) / 2.0
        price2 = (high[bar - 2] + low[bar - 2]) / 2.0
        if bar < min_rates_total:
            ITrendBuffer[bar] = (price0 + (2.0 * price1) + price2) / 4.0
        else:
            ITrendBuffer[bar] = (K0 * price0) + (K1 * price1) - (K2 * price2) + (K3 * ITrendBuffer[bar - 1]) - (K4 * ITrendBuffer[bar - 2])
        TriggerBuffer[bar] = (2.0 * ITrendBuffer[bar]) - ITrendBuffer[bar - 2]
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Instantaneoustrendline(_MQL5Indicator):
    name = 'instantaneoustrendline'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Alpha': 0.07,  # Indicator ratio
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

