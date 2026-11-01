"""sensetive — converted from MQL5: MQL5 Indicators/SeNSetiVe/sensetive.mq5

SeNSetiVe
Copyright: Copyright © 2006, QuantifiEd; Link: E-mail: MySpons@rambler.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, QuantifiEd', 'link': 'E-mail: MySpons@rambler.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16711680, 16711935]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'SeNSetiVe'}, 'levels': [], 'description': ['SeNSetiVe'], 'name': 'sensetive', 'source': 'MQL5 Indicators/SeNSetiVe/sensetive.mq5', 'folder': 'SeNSetiVe', 'inputs': [{'mql': 'SPerioD', 'py': 'SPerioD', 'param': 'SPerioD', 'type': 'uint', 'default': 150, 'label': 'Indicator period', 'sinput': False}, {'mql': 'SFactoR', 'py': 'SFactoR', 'param': 'SFactoR', 'type': 'uint', 'default': 7, 'label': 'Indicator sensitivity', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'Volume', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SPerioD = _input('SPerioD', 150)  # Indicator period
SFactoR = _input('SFactoR', 7)  # Indicator sensitivity
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
VolumeType = _input('VolumeType', VOLUME_TICK)  # Volume
Line1Buffer = Arr(0, 0.0)
Line2Buffer = Arr(0, 0.0)
min_rates_total = 0
MAO_Handle = 0
MAC_Handle = 0
MAH_Handle = 0
MAL_Handle = 0

def OnInit():
    global MAC_Handle, MAH_Handle, MAL_Handle, MAO_Handle, min_rates_total
    min_rates_total = _int(SFactoR + SPerioD)
    MAO_Handle = iMA(None, 0, SPerioD, 0, MODE_SMA, PRICE_OPEN)
    if MAO_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
    MAC_Handle = iMA(None, 0, SPerioD, 0, MODE_SMA, PRICE_CLOSE)
    if MAC_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
    MAH_Handle = iMA(None, 0, SPerioD, 0, MODE_SMA, PRICE_HIGH)
    if MAH_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
    MAL_Handle = iMA(None, 0, SPerioD, 0, MODE_SMA, PRICE_LOW)
    if MAL_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
    SetIndexBuffer(0, Line1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Line1Buffer, True)
    SetIndexBuffer(1, Line2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Line2Buffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'SeNSetiVe(', SPerioD, ', ', SFactoR, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (((BarsCalculated(MAO_Handle) < rates_total or BarsCalculated(MAC_Handle) < rates_total) or BarsCalculated(MAH_Handle) < rates_total) or BarsCalculated(MAL_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    sOpen = Arr(0, 0.0)
    sClose = Arr(0, 0.0)
    sLow = Arr(0, 0.0)
    sHigh = Arr(0, 0.0)
    max_ = 0.0
    min_ = 0.0
    volume_ = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(MAO_Handle, 0, 0, to_copy, sOpen) <= 0:
        return 0
    if CopyBuffer(MAC_Handle, 0, 0, to_copy, sClose) <= 0:
        return 0
    if CopyBuffer(MAH_Handle, 0, 0, to_copy, sLow) <= 0:
        return 0
    if CopyBuffer(MAL_Handle, 0, 0, to_copy, sHigh) <= 0:
        return 0
    ArraySetAsSeries(sOpen, True)
    ArraySetAsSeries(sClose, True)
    ArraySetAsSeries(sLow, True)
    ArraySetAsSeries(sHigh, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if VolumeType == VOLUME_TICK:
        ArraySetAsSeries(tick_volume, True)
    else:
        ArraySetAsSeries(volume, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        max_ = high[ArrayMaximum(high, bar, SFactoR)]
        min_ = low[ArrayMinimum(low, bar, SFactoR)]
        if VolumeType == VOLUME_TICK:
            volume_ = tick_volume[bar]
        else:
            volume_ = volume[bar]
        Line1Buffer[bar] = ((5 * sClose[bar]) - (5 * sOpen[bar]) + max_ + min_ - sHigh[bar] - sLow[bar]) * volume_
        Line2Buffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Sensetive(_MQL5Indicator):
    name = 'sensetive'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SPerioD': 150,  # Indicator period
        'SFactoR': 7,  # Indicator sensitivity
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volume
    }

