"""Minions.BetterVolume — converted from MQL5: MQL5 Indicators/Better volume/Minions.BetterVolume.mq5

Minions in the quest for explaining Volume in a better way.
 
(CC) Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License
Copyright: www.MinionsLabs.com; Link: http://www.MinionsLabs.com; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.MinionsLabs.com', 'link': 'http://www.MinionsLabs.com', 'version': '1.0', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [1315860, 65280, 255]}, 'widths': {1: 4}, 'styles': {1: 0}, 'labels': {1: 'Better Volume'}, 'levels': [], 'description': ['Minions in the quest for explaining Volume in a better way.', ' ', '(CC) Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License'], 'name': 'Minions.BetterVolume', 'source': 'MQL5 Indicators/Better volume/Minions.BetterVolume.mq5', 'folder': 'Better volume', 'inputs': [{'mql': 'inpAppliedVolume', 'py': 'inpAppliedVolume', 'param': 'inpAppliedVolume', 'type': 'int', 'default': 1, 'label': 'Volume Type', 'sinput': False}, {'mql': 'inpBarsToAnalyze', 'py': 'inpBarsToAnalyze', 'param': 'inpBarsToAnalyze', 'type': 'int', 'default': 20, 'label': 'N past bars to analyze', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpAppliedVolume = _input('inpAppliedVolume', VOLUME_REAL)  # Volume Type
inpBarsToAnalyze = _input('inpBarsToAnalyze', 20)  # N past bars to analyze
bufferVolume = Arr(0, 0.0)
bufferColors = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, bufferVolume, INDICATOR_DATA)
    SetIndexBuffer(1, bufferColors, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Minions.BetterVolume (' + EnumToString(inpAppliedVolume, 'ENUM_APPLIED_VOLUME') + ', Period:' + _str(paramBarsToAnalyze) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    start = prev_calculated - 1
    SMA = 0
    if rates_total < 2:
        return 0
    if start < 1:
        start = 1
    for i in range(start, rates_total):
        bufferVolume[i] = float((volume[i] if (paramAppliedVolume == VOLUME_REAL) else tick_volume[i]))
        if paramAppliedVolume == VOLUME_REAL:
            SMA = SMAOnArray(volume, paramBarsToAnalyze, i)
        else:
            SMA = SMAOnArray(tick_volume, paramBarsToAnalyze, i)
        if open[i] < close[i] and bufferVolume[i] > SMA:
            bufferColors[i] = 1.0
        elif open[i] > close[i] and bufferVolume[i] > SMA:
            bufferColors[i] = 2.0
        else:
            bufferColors[i] = 0.0
    return rates_total

def SMAOnArray(array, period, position):
    sum_ = 0
    if (position - period) <= 0:
        return False
    for i in range(position - period + 1, position + 1):
        sum_ += array[i]
    return _idiv(sum_, period)

# ---- global variables initialised from expressions
paramAppliedVolume = (VOLUME_REAL if (inpAppliedVolume == 0) else inpAppliedVolume)
paramBarsToAnalyze = (20 if (inpBarsToAnalyze == 0) else inpBarsToAnalyze)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MinionsBetterVolume(_MQL5Indicator):
    name = 'Minions.BetterVolume'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpAppliedVolume': _Choice({0: 'Tick', 1: 'Real'}, default=1),  # Volume Type
        'inpBarsToAnalyze': 20,  # N past bars to analyze
    }

