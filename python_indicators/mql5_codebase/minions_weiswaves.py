"""Minions.WeisWaves — converted from MQL5: MQL5 Indicators/Weis Waves/Minions.WeisWaves.mq5

Minions for building Weis Volume Waves
 
(CC) Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License
Copyright: www.MinionsLabs.com; Link: http://www.MinionsLabs.com; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.MinionsLabs.com', 'link': 'http://www.MinionsLabs.com', 'version': '1.0', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255]}, 'widths': {1: 4}, 'styles': {}, 'labels': {1: 'Weis Volume Waves'}, 'levels': [], 'description': ['Minions for building Weis Volume Waves', ' ', '(CC) Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License'], 'name': 'Minions.WeisWaves', 'source': 'MQL5 Indicators/Weis Waves/Minions.WeisWaves.mq5', 'folder': 'Weis Waves', 'inputs': [{'mql': 'inpVolumeType', 'py': 'inpVolumeType', 'param': 'inpVolumeType', 'type': 'int', 'default': 1, 'label': 'Volume Type to use on waves', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpVolumeType = _input('inpVolumeType', VOLUME_REAL)  # Volume Type to use on waves
bufferWW = Arr(0, 0.0)
bufferColors = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, bufferWW, INDICATOR_DATA)
    SetIndexBuffer(1, bufferColors, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Weis Volume Waves')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    barsToProcess = 0
    shouldStartIn = 2
    vol = 0.0
    if rates_total < shouldStartIn:
        return 0
    if prev_calculated == 0 or rates_total > (prev_calculated + 1):
        bufferWW[0] = (float(tick_volume[0]) if (inpVolumeType == VOLUME_TICK) else float(volume[0]))
        barsToProcess = rates_total
    else:
        barsToProcess = rates_total - prev_calculated + 1
    i = rates_total - MathMax(shouldStartIn, barsToProcess - shouldStartIn)
    for i in range(i, rates_total):
        vol = (float(tick_volume[i]) if (inpVolumeType == VOLUME_TICK) else float(volume[i]))
        if close[i] >= close[i - 1]:
            if close[i - 1] >= close[i - 2]:
                bufferWW[i] = bufferWW[i - 1] + vol
                bufferColors[i] = 0.0
            else:
                bufferWW[i] = vol
                bufferColors[i] = 0.0
        else:
            if close[i - 1] < close[i - 2]:
                bufferWW[i] = bufferWW[i - 1] + vol
                bufferColors[i] = 1.0
            else:
                bufferWW[i] = vol
                bufferColors[i] = 1.0
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MinionsWeisWaves(_MQL5Indicator):
    name = 'Minions.WeisWaves'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpVolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=1),  # Volume Type to use on waves
    }

