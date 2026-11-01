"""volumes — converted from MQL5: MQL5 Indicators/Volumes/volumes.mq5

Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_minimum': 0.0}, 'types': {1: 10}, 'colors': {1: [32768, 255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': [], 'name': 'volumes', 'source': 'MQL5 Indicators/Volumes/volumes.mq5', 'folder': 'Volumes', 'inputs': [{'mql': 'InpVolumeType', 'py': 'InpVolumeType', 'param': 'InpVolumeType', 'type': 'int', 'default': 0, 'label': 'Volumes', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpVolumeType = _input('InpVolumeType', VOLUME_TICK)  # Volumes
ExtVolumesBuffer = Arr(0, 0.0)
ExtColorsBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtVolumesBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtColorsBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volumes')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    if rates_total < 2:
        return 0
    start = prev_calculated - 1
    if start < 1:
        start = 1
    if InpVolumeType == VOLUME_TICK:
        CalculateVolume(start, rates_total, TickVolume)
    else:
        CalculateVolume(start, rates_total, Volume)
    return rates_total

def CalculateVolume(nPosition, nRatesCount, SrcBuffer):
    ExtVolumesBuffer[0] = float(SrcBuffer[0])
    ExtColorsBuffer[0] = 0.0
    for i in range(nPosition, nRatesCount):
        dCurrVolume = float(SrcBuffer[i])
        dPrevVolume = float(SrcBuffer[i - 1])
        ExtVolumesBuffer[i] = dCurrVolume
        if dCurrVolume > dPrevVolume:
            ExtColorsBuffer[i] = 0.0
        else:
            ExtColorsBuffer[i] = 1.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Volumes(_MQL5Indicator):
    name = 'volumes'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpVolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volumes
    }

