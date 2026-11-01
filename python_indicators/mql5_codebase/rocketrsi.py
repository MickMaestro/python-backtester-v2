"""RocketRSI — converted from MQL5: MQL5 Indicators/Rocket RSI/RocketRSI.mq5

swilliamsforex@gmail.com
Copyright: Copyright 2018, Samuel Williams; Link: https://www.mql5.com/en/users/sambo3261; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, Samuel Williams', 'link': 'https://www.mql5.com/en/users/sambo3261', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1, 'indicator_maximum': 4.0, 'indicator_minimum': -4.0}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'RocketRSI'}, 'levels': [], 'description': ['swilliamsforex@gmail.com'], 'name': 'RocketRSI', 'source': 'MQL5 Indicators/Rocket RSI/RocketRSI.mq5', 'folder': 'Rocket RSI', 'inputs': [{'mql': 'RSILength', 'py': 'RSILength', 'param': 'RSILength', 'type': 'int', 'default': 10, 'label': 'Period of the RSI indicator - Needs to be half the dominant cycle', 'sinput': False}, {'mql': 'Smooth', 'py': 'Smooth', 'param': 'Smooth', 'type': 'int', 'default': 10, 'label': 'Smoothing of the indictor - not set above RSILength', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RSILength = _input('RSILength', 10)  # Period of the RSI indicator - Needs to be half the dominant cycle
Smooth = _input('Smooth', 10)  # Smoothing of the indictor - not set above RSILength
RSIBuffer = Arr(0, 0.0)
RocketRSIBuffer = Arr(0, 0.0)
RSITestBuffer = Arr(0, 0.0)
Filter = Arr(0, 0.0)
Mom = Arr(0, 0.0)
a1 = 0.0
b1 = 0.0
c1 = 0.0
c2 = 0.0
c3 = 0.0
rsiHandle = 0

def OnInit():
    global a1, b1, c1, c2, c3, rsiHandle
    SetIndexBuffer(0, RocketRSIBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, RSIBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, Filter, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, Mom, INDICATOR_CALCULATIONS)
    rsiHandle = iRSI(Symbol(), Period(), RSILength, PRICE_CLOSE)
    if rsiHandle == INVALID_HANDLE:
        PrintFormat('Failed to get handle of RSI indicator, code: %d', GetLastError())
    rad = M_PI / 180
    a1 = MathExp((-1.414 * M_PI) / Smooth)
    b1 = 2 * a1 * MathCos(((1.414 * 180) / Smooth) * rad)
    c2 = b1
    c3 = (-a1) * a1
    c1 = 1 - c2 - c3
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if CopyBuffer(rsiHandle, 0, 0, rates_total, RSIBuffer) < 0:
        PrintFormat('Error copying rsi data from handle, code: %d', GetLastError())
    i = MathMax(prev_calculated - 1, RSILength + 1)
    while i < rates_total:
        CU = 0.0
        CD = 0.0
        Mom[i] = close[i] - close[i - (RSILength + 1)]
        Filter[i] = (c1 * ((Mom[i] + Mom[i - 1]) / 2)) + (c2 * Filter[i - 1]) + (c3 * Filter[i - 2])
        j = i - (RSILength + 1)
        while j < i:
            if (Filter[j] - Filter[j + 1]) > 0:
                CU = CU + Filter[j] - Filter[j + 1]
            if (Filter[j] - Filter[j + 1]) < 0:
                CD = CD + Filter[j + 1] - Filter[j]
            j += 1
        MyRSI = 0.0
        denom = CU + CD
        if denom == 0:
            denom = -1.0
        if (CU + CD) != 0:
            MyRSI = _fdiv(CU - CD, denom)
        if denom == -1:
            MyRSI = 50.0
        if MyRSI > 0.999:
            MyRSI = 0.999
        if MyRSI < -0.999:
            MyRSI = -0.999
        RocketRSIBuffer[i] = 0.5 * MathLog(_fdiv(1 + MyRSI, 1 - MyRSI))
        i += 1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RocketRSI(_MQL5Indicator):
    name = 'RocketRSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSILength': 10,  # Period of the RSI indicator - Needs to be half the dominant cycle
        'Smooth': 10,  # Smoothing of the indictor - not set above RSILength
    }
    y_range = (-4.0, 4.0)

