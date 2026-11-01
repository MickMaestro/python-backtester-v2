"""rvi_bars — converted from MQL5: MQL5 Indicators/RVI BARS/rvi_bars.mq5

Copyright: Copyright © 2005, Perky; Link: Perky_z@yahoo.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Perky', 'link': 'Perky_z@yahoo.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 11}, 'colors': {1: [255, 8388736, 8421504, 13434880, 16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'RVI_BARS'}, 'levels': [], 'description': [], 'name': 'rvi_bars', 'source': 'MQL5 Indicators/RVI BARS/rvi_bars.mq5', 'folder': 'RVI BARS', 'inputs': [{'mql': 'RVIPeriod', 'py': 'RVIPeriod', 'param': 'RVIPeriod', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RVIPeriod = _input('RVIPeriod', 14)
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
RVI_Handle = 0

def OnInit():
    global RVI_Handle, min_rates_total
    min_rates_total = _int(RVIPeriod)
    RVI_Handle = iRVI(None, 0, RVIPeriod)
    if RVI_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of the iRVI calculator')
        return INIT_FAILED
    SetIndexBuffer(0, UpIndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpIndBuffer, True)
    SetIndexBuffer(1, DnIndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnIndBuffer, True)
    SetIndexBuffer(2, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RVI_BARS')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if BarsCalculated(RVI_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    RVI = Arr(0, 0.0)
    SIG = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(Open, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Close, True)
    ArraySetAsSeries(RVI, True)
    ArraySetAsSeries(SIG, True)
    if CopyBuffer(RVI_Handle, MAIN_LINE, 0, to_copy, RVI) <= 0:
        return 0
    if CopyBuffer(RVI_Handle, SIGNAL_LINE, 0, to_copy, SIG) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        UpIndBuffer[bar] = High[bar]
        DnIndBuffer[bar] = Low[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        clr = 2
        if RVI[bar] > SIG[bar]:
            if Open[bar] < Close[bar]:
                clr = 4
            if Open[bar] > Close[bar]:
                clr = 3
        if RVI[bar] < SIG[bar]:
            if Open[bar] > Close[bar]:
                clr = 0
            if Open[bar] < Close[bar]:
                clr = 1
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RviBars(_MQL5Indicator):
    name = 'rvi_bars'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RVIPeriod': 14,
    }

