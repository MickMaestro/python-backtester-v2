"""Bulls and bears — converted from MQL5: MQL5 Indicators/Bulls and Bears/Bulls and bears.mq5

Bulls and bears
Copyright: mladen; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 7, 2: 7, 3: 1, 4: 1}, 'colors': {1: [9498256], 2: [9498256, 11788021], 3: [3329330], 4: [6333684]}, 'widths': {3: 2, 4: 2}, 'styles': {}, 'labels': {1: 'Bulls zone', 2: 'Bears zone', 3: 'Bulls value', 4: 'Bears line'}, 'levels': [], 'description': ['Bulls and bears'], 'name': 'Bulls and bears', 'source': 'MQL5 Indicators/Bulls and Bears/Bulls and bears.mq5', 'folder': 'Bulls and Bears', 'inputs': [{'mql': 'inpBullBearPeriod', 'py': 'inpBullBearPeriod', 'param': 'inpBullBearPeriod', 'type': 'int', 'default': 14, 'label': 'Bulls and bears period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpBullBearPeriod = _input('inpBullBearPeriod', 14)  # Bulls and bears period
bullsh = Arr(0, 0.0)
bullsz = Arr(0, 0.0)
bullsl = Arr(0, 0.0)
bearsh = Arr(0, 0.0)
bearsl = Arr(0, 0.0)
bearsz = Arr(0, 0.0)
_bullsHandle = 0
_bearsHandle = 0

def OnInit():
    global _bearsHandle, _bullsHandle
    SetIndexBuffer(0, bullsh, INDICATOR_DATA)
    SetIndexBuffer(1, bullsz, INDICATOR_DATA)
    SetIndexBuffer(2, bearsh, INDICATOR_DATA)
    SetIndexBuffer(3, bearsz, INDICATOR_DATA)
    SetIndexBuffer(4, bullsl, INDICATOR_DATA)
    SetIndexBuffer(5, bearsl, INDICATOR_DATA)
    _bullsHandle = iBullsPower(Symbol(), 0, inpBullBearPeriod)
    if _bullsHandle == INVALID_HANDLE:
        return INIT_FAILED
    _bearsHandle = iBearsPower(Symbol(), 0, inpBullBearPeriod)
    if _bullsHandle == INVALID_HANDLE:
        IndicatorRelease(_bullsHandle)
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Bulls and bears (' + _str(inpBullBearPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if BarsCalculated(_bullsHandle) < rates_total:
        return prev_calculated
    if BarsCalculated(_bullsHandle) < rates_total:
        return prev_calculated
    _bullVal = Arr(1, 0.0, dyn=False)
    _bearVal = Arr(1, 0.0, dyn=False)
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        _bullCopied = CopyBuffer(_bullsHandle, 0, _DT(time[i]), 1, _bullVal)
        _bearCopied = CopyBuffer(_bearsHandle, 0, _DT(time[i]), 1, _bearVal)
        bullsl[i] = (_bullVal[0] if (_bullCopied == 1) else EMPTY_VALUE)
        bearsl[i] = (_bearVal[0] if (_bearCopied == 1) else EMPTY_VALUE)
        bullsh[i] = MathMax(bullsl[i], 0)
        bullsz[i] = 0.0
        bearsh[i] = MathMin(bearsl[i], 0)
        bearsz[i] = 0.0
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BullsAndBears(_MQL5Indicator):
    name = 'Bulls and bears'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpBullBearPeriod': 14,  # Bulls and bears period
    }

