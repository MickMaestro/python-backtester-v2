"""Average Volume — converted from MQL5: MQL5 Indicators/Simple Average Volumes/Average Volume.mq5

Copyright: Created by abfs.tech; Link: https://www.abfs.tech/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Created by abfs.tech', 'link': 'https://www.abfs.tech/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16755200], 2: [16449791]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Average Real Volume', 2: 'Average Tick Volume'}, 'levels': [], 'description': [''], 'name': 'Average Volume', 'source': 'MQL5 Indicators/Simple Average Volumes/Average Volume.mq5', 'folder': 'Simple Average Volumes', 'inputs': [{'mql': 'Period_Input', 'py': 'Period_Input', 'param': 'Period_Input', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Buffer1 = Arr(0, 0.0)
Buffer2 = Arr(0, 0.0)
Period_Input = _input('Period_Input', 14)
myPoint = 0.0  # initialized in OnInit
Volumes_handle = 0
Volumes = Arr(0, 0.0)
Volumes_handle2 = 0
Volumes2 = Arr(0, 0.0)
MA_handle = 0
MA = Arr(0, 0.0)
MA_handle2 = 0
MA2 = Arr(0, 0.0)

def myAlert(type_, message):
    if type_ == 'print':
        Print(message)
    elif type_ == 'error':
        Print(type_ + ' | Average Volume @ ' + Symbol() + ',' + IntegerToString(Period()) + ' | ' + message)
    elif type_ == 'order':
        pass
    elif type_ == 'modify':
        pass

def OnInit():
    global MA_handle, MA_handle2, Volumes_handle, Volumes_handle2, myPoint
    SetIndexBuffer(0, Buffer1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, Buffer2)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    myPoint = Point()
    if Digits() == 5 or Digits() == 3:
        myPoint *= 10
    Volumes_handle = iVolumes(None, PERIOD_CURRENT, VOLUME_REAL)
    if Volumes_handle < 0:
        Print('The creation of iVolumes has failed: Volumes_handle=', INVALID_HANDLE)
        Print('Runtime error = ', GetLastError())
        return INIT_FAILED
    Volumes_handle2 = iVolumes(None, PERIOD_CURRENT, VOLUME_TICK)
    if Volumes_handle2 < 0:
        Print('The creation of iVolumes has failed: Volumes_handle2=', INVALID_HANDLE)
        Print('Runtime error = ', GetLastError())
        return INIT_FAILED
    MA_handle = iMA(None, PERIOD_CURRENT, Period_Input, 0, MODE_SMA, Volumes_handle)
    if MA_handle < 0:
        Print('The creation of iMA has failed: MA_handle=', INVALID_HANDLE)
        Print('Runtime error = ', GetLastError())
        return INIT_FAILED
    MA_handle2 = iMA(None, PERIOD_CURRENT, Period_Input, 0, MODE_SMA, Volumes_handle2)
    if MA_handle2 < 0:
        Print('The creation of iMA has failed: MA_handle2=', INVALID_HANDLE)
        Print('Runtime error = ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = rates_total - prev_calculated
    ArraySetAsSeries(Buffer1, True)
    ArraySetAsSeries(Buffer2, True)
    if prev_calculated < 1:
        ArrayInitialize(Buffer1, EMPTY_VALUE)
        ArrayInitialize(Buffer2, EMPTY_VALUE)
    else:
        limit += 1
    if BarsCalculated(Volumes_handle) <= 0:
        return 0
    if CopyBuffer(Volumes_handle, 0, 0, rates_total, Volumes) <= 0:
        return rates_total
    ArraySetAsSeries(Volumes, True)
    if BarsCalculated(MA_handle) <= 0:
        return 0
    if CopyBuffer(MA_handle, 0, 0, rates_total, MA) <= 0:
        return rates_total
    ArraySetAsSeries(MA, True)
    if BarsCalculated(Volumes_handle2) <= 0:
        return 0
    if CopyBuffer(Volumes_handle2, 0, 0, rates_total, Volumes2) <= 0:
        return rates_total
    ArraySetAsSeries(Volumes2, True)
    if BarsCalculated(MA_handle2) <= 0:
        return 0
    if CopyBuffer(MA_handle2, 0, 0, rates_total, MA2) <= 0:
        return rates_total
    ArraySetAsSeries(MA2, True)
    for i in range(limit - 1, 0 - 1, -1):
        if i >= MathMin(5000 - 1, rates_total - 1 - 50):
            continue
        if Volumes[i] > 0:
            Buffer1[i] = MA[i]
        else:
            Buffer1[i] = EMPTY_VALUE
        if Volumes2[i] > 0:
            Buffer2[i] = MA2[i]
        else:
            Buffer2[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AverageVolume(_MQL5Indicator):
    name = 'Average Volume'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period_Input': 14,
    }

