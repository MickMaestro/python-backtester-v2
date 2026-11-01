"""leading — converted from MQL5: MQL5 Indicators/Leading/leading.mq5

Copyright: Coded by Witold Wozniak; Link: www.mqlsoft.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Coded by Witold Wozniak', 'link': 'www.mqlsoft.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Lead', 2: 'EMA'}, 'levels': [], 'description': [], 'name': 'leading', 'source': 'MQL5 Indicators/Leading/leading.mq5', 'folder': 'Leading', 'inputs': [{'mql': 'Alpha1', 'py': 'Alpha1', 'param': 'Alpha1', 'type': 'double', 'default': 0.25, 'label': 'Alpha1 indicator ratio', 'sinput': False}, {'mql': 'Alpha2', 'py': 'Alpha2', 'param': 'Alpha2', 'type': 'double', 'default': 0.33, 'label': 'Alpha2 indicator ratio', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Alpha1 = _input('Alpha1', 0.25)  # Alpha1 indicator ratio
Alpha2 = _input('Alpha2', 0.33)  # Alpha2 indicator ratio
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
min_rates_total = 0
NetLeadBuffer = Arr(0, 0.0)
EMABuffer = Arr(0, 0.0)

def Get_Price(High, Low, bar):
    return (High[bar] + Low[bar]) / 2

def OnInit():
    global min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, NetLeadBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, EMABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'Leading(', DoubleToString(Alpha1, 4), ', ', DoubleToString(Alpha2, 4), ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Lead_
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    Lead = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    Lead = _s_OnCalculate_Lead_
    bar = first
    for bar in range(bar, rates_total):
        if rates_total != prev_calculated and bar == (rates_total - 1):
            _s_OnCalculate_Lead_ = Lead
        if bar > min_rates_total:
            Lead = (2.0 * Get_Price(high, low, bar)) + ((Alpha1 - 2.0) * Get_Price(high, low, bar - 1)) + ((1.0 - Alpha1) * Lead)
            NetLeadBuffer[bar] = (Alpha2 * Lead) + ((1 - Alpha2) * NetLeadBuffer[bar - 1])
            EMABuffer[bar] = (0.5 * Get_Price(high, low, bar)) + (0.5 * EMABuffer[bar - 1])
        else:
            Lead = Get_Price(high, low, bar)
            NetLeadBuffer[bar] = Lead
            EMABuffer[bar] = Lead
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_Lead_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Leading(_MQL5Indicator):
    name = 'leading'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Alpha1': 0.25,  # Alpha1 indicator ratio
        'Alpha2': 0.33,  # Alpha2 indicator ratio
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

