"""color_parabolic — converted from MQL5: MQL5 Indicators/Color Parabolic/color_parabolic.mq5

Parabolic Sar
Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [255], 2: [13434880], 3: [9639167], 4: [14822282]}, 'widths': {1: 1, 2: 1, 3: 4, 4: 4}, 'styles': {}, 'labels': {1: 'Lower Parabolic', 2: 'Upper Parabolic', 3: 'Parabolic Sell', 4: 'Parabolic Buy'}, 'levels': [], 'description': ['Parabolic Sar'], 'name': 'color_parabolic', 'source': 'MQL5 Indicators/Color Parabolic/color_parabolic.mq5', 'folder': 'Color Parabolic', 'inputs': [{'mql': 'Step', 'py': 'Step', 'param': 'Step', 'type': 'double', 'default': 0.02, 'label': 'Step', 'sinput': False}, {'mql': 'Maximum', 'py': 'Maximum', 'param': 'Maximum', 'type': 'double', 'default': 0.2, 'label': 'Maximum', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Step = _input('Step', 0.02)  # Step
Maximum = _input('Maximum', 0.2)  # Maximum
BuyBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
UpSarBuffer = Arr(0, 0.0)
DnSarBuffer = Arr(0, 0.0)
SAR_Handle = 0
min_rates_total = 0

def OnInit():
    global SAR_Handle, min_rates_total
    min_rates_total = 2
    SAR_Handle = iSAR(None, PERIOD_CURRENT, Step, Maximum)
    if SAR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iSAR indicator')
    SetIndexBuffer(0, UpSarBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 158)
    ArraySetAsSeries(UpSarBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, DnSarBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 158)
    ArraySetAsSeries(DnSarBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 174)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(3, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 174)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Parabolic Sar'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(SAR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    SAR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total + 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(SAR_Handle, 0, 0, to_copy, SAR) <= 0:
        return 0
    ArraySetAsSeries(SAR, True)
    ArraySetAsSeries(open, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        DnSarBuffer[bar] = 0.0
        UpSarBuffer[bar] = 0.0
        if open[bar] < SAR[bar]:
            UpSarBuffer[bar] = SAR[bar]
        else:
            DnSarBuffer[bar] = SAR[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if UpSarBuffer[bar + 1] > 0.0 and DnSarBuffer[bar] > 0.0:
            BuyBuffer[bar] = SAR[bar]
        if DnSarBuffer[bar + 1] > 0.0 and UpSarBuffer[bar] > 0.0:
            SellBuffer[bar] = SAR[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorParabolic(_MQL5Indicator):
    name = 'color_parabolic'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Step': 0.02,  # Step
        'Maximum': 0.2,  # Maximum
    }

