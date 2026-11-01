"""lrma_channel_trajectory — converted from MQL5: MQL5 Indicators/LRMA_Channel_trajectory/lrma_channel_trajectory.mq5

Copyright: Copyright 2010, Urain; Link: https://login.mql5.com/ru/users/Urain; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2010, Urain', 'link': 'https://login.mql5.com/ru/users/Urain', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 5, 5: 5}, 'colors': {1: [255], 2: [16760576], 3: [16760576], 4: [255], 5: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'Transform', 2: 'LineUp', 3: 'LineDown', 4: 'LR_down', 5: 'LR_up'}, 'levels': [], 'description': [], 'name': 'lrma_channel_trajectory', 'source': 'MQL5 Indicators/LRMA_Channel_trajectory/lrma_channel_trajectory.mq5', 'folder': 'LRMA_Channel_trajectory', 'inputs': [{'mql': 'lr_per', 'py': 'lr_per', 'param': 'lr_per', 'type': 'int', 'default': 16, 'label': 'Linear regression period', 'sinput': False}, {'mql': 'stdev_koef', 'py': 'stdev_koef', 'param': 'stdev_koef', 'type': 'double', 'default': 2.0, 'label': 'Standard deviation ratio', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
lr_per = _input('lr_per', 16)  # Linear regression period
stdev_koef = _input('stdev_koef', 2.0)  # Standard deviation ratio
TransBuffer = Arr(0, 0.0)
Label1Buffer = Arr(0, 0.0)
Color1Buffer = Arr(0, 0.0)
Label2Buffer = Arr(0, 0.0)
Label3Buffer = Arr(0, 0.0)
Label4Buffer = Arr(0, 0.0)
sma2 = 0.0
lwma3 = 0.0

def OnInit():
    SetIndexBuffer(0, TransBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, Label3Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, Label4Buffer, INDICATOR_DATA)
    SetIndexBuffer(3, Label1Buffer, INDICATOR_DATA)
    SetIndexBuffer(4, Color1Buffer, INDICATOR_DATA)
    SetIndexBuffer(5, Label2Buffer, INDICATOR_CALCULATIONS)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0.0)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global lwma3, sma2
    prev = prev_calculated
    for i in range(prev, rates_total):
        TransBuffer[i] = close[i]
    for i in range(prev, rates_total):
        if i > lr_per:
            sma2 = 2.0 * SMA(TransBuffer, lr_per + 1, i)
            lwma3 = 3.0 * LWMA(TransBuffer, lr_per + 1, i)
            Label1Buffer[i] = lwma3 - sma2
            Label2Buffer[i] = (2.0 * sma2) - lwma3
    for i in range(prev, rates_total):
        if i > lr_per:
            temp = (Label1Buffer[i] - Label2Buffer[i]) / lr_per
            Kstdev = stdev_koef * StDev(TransBuffer, Label1Buffer[i], temp, lr_per, i)
            if temp > 0:
                Color1Buffer[i] = Label1Buffer[i]
            Label3Buffer[i] = Label1Buffer[i] + Kstdev
            Label4Buffer[i] = Label1Buffer[i] - Kstdev
    for i in range(prev, rates_total):
        if Color1Buffer[i] != 0:
            Label1Buffer[i] = 0.0
    return rates_total

def SMA(cot, per, shift):
    res = 0.0
    for i in range(0, per):
        res += cot[shift - i]
    return _fdiv(res, float(per))

def LWMA(cot, per, shift):
    res = 0.0
    sumk = 0
    for i in range(0, per):
        res += cot[shift - i] * float(per - i)
        sumk += per - i
    return _fdiv(res, float(sumk))

def StDev(cot, nl, lr, per, shift):
    res = 0.0
    for i in range(0, per):
        temp = cot[shift - i] - (nl - (lr * i))
        res += temp * temp
    return sqrt(_fdiv(res, float(per)))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LrmaChannelTrajectory(_MQL5Indicator):
    name = 'lrma_channel_trajectory'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'lr_per': 16,  # Linear regression period
        'stdev_koef': 2.0,  # Standard deviation ratio
    }

