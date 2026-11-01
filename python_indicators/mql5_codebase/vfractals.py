"""vfractals — converted from MQL5: MQL5 Indicators/VFractals/vfractals.mq5

indicator marks the level of the fractal which formed on the bar with the volume,
which larger than the average volume of the last 3 bars before fractal.
Copyright: Copyright © 2010, sanyooooook; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, sanyooooook', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16711680]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'Down VFractals', 2: 'Up VFractals'}, 'levels': [], 'description': ['indicator marks the level of the fractal which formed on the bar with the volume,', 'which larger than the average volume of the last 3 bars before fractal.'], 'name': 'vfractals', 'source': 'MQL5 Indicators/VFractals/vfractals.mq5', 'folder': 'VFractals', 'inputs': [{'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'volume', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'Lable', 'py': 'Lable', 'param': 'Lable', 'type': 'uint', 'default': 158, 'label': 'Lable for icon', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
VolumeType = _input('VolumeType', VOLUME_TICK)  # volume
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
Lable = _input('Lable', 158)  # Lable for icon
DnBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
min_rates_total = 0
Fra_Handle = 0

def OnInit():
    global Fra_Handle, min_rates_total
    min_rates_total = 6
    Fra_Handle = iFractals(Symbol(), PERIOD_CURRENT)
    if Fra_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iFractals indicator')
    SetIndexBuffer(0, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, Lable)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    SetIndexBuffer(1, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, Lable)
    ArraySetAsSeries(UpBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'VFractals(' + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(Fra_Handle) < min_rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    to_copy = 0
    UpFractals = Arr(0, 0.0)
    DnFractals = Arr(0, 0.0)
    Vol2 = 0
    SVol = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        UpBuffer[limit] = EMPTY_VALUE
        DnBuffer[limit] = EMPTY_VALUE
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(volume, True)
    ArraySetAsSeries(tick_volume, True)
    ArraySetAsSeries(spread, True)
    ArraySetAsSeries(UpFractals, True)
    ArraySetAsSeries(DnFractals, True)
    if CopyBuffer(Fra_Handle, UPPER_LINE, 2, to_copy, UpFractals) <= 0:
        return 0
    if CopyBuffer(Fra_Handle, LOWER_LINE, 2, to_copy, DnFractals) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        UpBuffer[bar] = EMPTY_VALUE
        DnBuffer[bar] = EMPTY_VALUE
        if VolumeType == VOLUME_TICK:
            Vol2 = tick_volume[bar + 2]
            SVol = _idiv(tick_volume[bar + 3] + tick_volume[bar + 4] + tick_volume[bar + 5], 3)
        else:
            Vol2 = volume[bar + 2]
            SVol = _idiv(volume[bar + 3] + volume[bar + 4] + volume[bar + 5], 3)
        if Vol2 > SVol and UpFractals[bar] != EMPTY_VALUE:
            UpBuffer[bar] = UpFractals[bar] + Point() + (spread[bar] * Point())
        else:
            UpBuffer[bar] = UpBuffer[bar + 1]
        if Vol2 > SVol and DnFractals[bar] != EMPTY_VALUE:
            DnBuffer[bar] = DnFractals[bar] - Point()
        else:
            DnBuffer[bar] = DnBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Vfractals(_MQL5Indicator):
    name = 'vfractals'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # volume
        'Shift': 0,  # horizontal shift of the indicator in bars
        'Lable': 158,  # Lable for icon
    }

