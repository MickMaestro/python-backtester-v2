"""Volumes spread mod — converted from MQL5: MQL5 Indicators/Volumes Spread mod/Volumes spread mod.mq5

Copyright: 2009-2020, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009-2020, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1, 'indicator_minimum': 0.0}, 'types': {1: 3}, 'colors': {1: [16776960]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Volumes spread mod', 'source': 'MQL5 Indicators/Volumes Spread mod/Volumes spread mod.mq5', 'folder': 'Volumes Spread mod', 'inputs': [{'mql': 'InpVolumeType', 'py': 'InpVolumeType', 'param': 'InpVolumeType', 'type': 'int', 'default': 0, 'label': 'Volumes', 'sinput': False}, {'mql': 'spreadchoice', 'py': 'spreadchoice', 'param': 'spreadchoice', 'type': 'bool', 'default': True, 'label': 'Use Spread?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpVolumeType = _input('InpVolumeType', VOLUME_TICK)  # Volumes
spreadchoice = _input('spreadchoice', True)  # Use Spread?
ExtVolumesBuffer = Arr(0, 0.0)
ExtColorsBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtVolumesBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtVolumesBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volumes')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if InpVolumeType == VOLUME_TICK:
        ArraySetAsSeries(tick_volume, True)
    else:
        ArraySetAsSeries(volume, True)
    ArraySetAsSeries(spread, True)
    if rates_total < 2:
        return 0
    pos = prev_calculated - 1
    if pos < 1:
        ExtVolumesBuffer[0] = 0.0
        pos = 1
    if InpVolumeType == VOLUME_TICK:
        CalculateVolume(pos, rates_total, tick_volume, spread)
    else:
        CalculateVolume(pos, rates_total, volume, spread)
    return rates_total

def CalculateVolume(pos, rates_total, volume, spread):
    ExtVolumesBuffer[0] = float(volume[0])
    for i in range(pos, rates_total):
        curr_volume = 0.0
        curr_spread = spread[i]
        if spread[i] == 0:
            curr_spread = 1
        if spreadchoice == True:
            curr_volume = _fdiv(float(volume[i]), curr_spread)
        else:
            curr_volume = float(volume[i])
        ExtVolumesBuffer[i] = curr_volume


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolumesSpreadMod(_MQL5Indicator):
    name = 'Volumes spread mod'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpVolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volumes
        'spreadchoice': True,  # Use Spread?
    }

