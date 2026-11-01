"""Zigzag on macross — converted from MQL5: MQL5 Indicators/Trend Zigzag (on ma cross)/Zigzag on macross.mq5


Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 13, 2: 1, 3: 1}, 'colors': {1: [3329330, 255, 13882323], 2: [32768], 3: [255]}, 'widths': {1: 2, 2: 1, 3: 1}, 'styles': {2: 2, 3: 2}, 'labels': {1: 'ZigZag'}, 'levels': [], 'description': [], 'name': 'Zigzag on macross', 'source': 'MQL5 Indicators/Trend Zigzag (on ma cross)/Zigzag on macross.mq5', 'folder': 'Trend Zigzag (on ma cross)', 'inputs': [{'mql': 'MA1Period', 'py': 'MA1Period', 'param': 'MA1Period', 'type': 'int', 'default': 5, 'label': 'Fast period (green)', 'sinput': False}, {'mql': 'MA2Period', 'py': 'MA2Period', 'param': 'MA2Period', 'type': 'int', 'default': 8, 'label': 'Slow period (red)', 'sinput': False}, {'mql': 'Backstep', 'py': 'Backstep', 'param': 'Backstep', 'type': 'int', 'default': 3, 'label': 'Backstep', 'sinput': False}, {'mql': 'alerts', 'py': 'alerts', 'param': 'alerts', 'type': 'bool', 'default': False, 'label': 'Alert on leg change', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ZigZagState
NONE = 0
LL_FOUND = 1
HL_FOUND = 2
LH_FOUND = 3
HH_FOUND = 4
_enum('ZigZagState', {0: 'NONE', 1: 'LL_FOUND', 2: 'HL_FOUND', 3: 'LH_FOUND', 4: 'HH_FOUND'})

# ---- inputs and global variables
MA1Buffer = Arr(0, 0.0)
MA2Buffer = Arr(0, 0.0)
ZigZagBuffer1 = Arr(0, 0.0)
ZigZagBuffer2 = Arr(0, 0.0)
zag_color = Arr(0, 0.0)
MA1Period = _input('MA1Period', 5)  # Fast period (green)
MA2Period = _input('MA2Period', 8)  # Slow period (red)
Backstep = _input('Backstep', 3)  # Backstep
alerts = _input('alerts', False)  # Alert on leg change
LL = 0.0
HL = 0.0
LH = 0.0
HH = 0.0
currentState = NONE

def CalculateSMA(price, period, index):
    sum_ = 0.0
    for j in range(0, period):
        sum_ += price[index - j]
    return _fdiv(sum_, period)

def OnInit():
    SetIndexBuffer(0, ZigZagBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ZigZagBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, zag_color, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, MA1Buffer, INDICATOR_DATA)
    SetIndexBuffer(4, MA2Buffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global HH, HL, LH, LL, currentState, lastAlertTime
    start = (MathMax(MA1Period, MA2Period) if (prev_calculated == 0) else prev_calculated)
    for i in range(start, rates_total):
        res = 0
        ZigZagBuffer1[i] = EMPTY_VALUE
        ZigZagBuffer2[i] = EMPTY_VALUE
        MA1Buffer[i] = CalculateSMA(close, MA1Period, i)
        MA2Buffer[i] = CalculateSMA(close, MA2Period, i)
        bullishCrossover = MA1Buffer[i - 1] < MA2Buffer[i] and MA1Buffer[i] > MA2Buffer[i - 1]
        bearishCrossover = MA1Buffer[i - 1] > MA2Buffer[i] and MA1Buffer[i] < MA2Buffer[i - 1]
        barOpenTime = time[i]
        High = high[i]
        Low = low[i]
        for j in range(1, Backstep + 1):
            if high[i - j] > High:
                High = high[i - j]
            if low[i - j] < Low:
                Low = low[i - j]
        if currentState == NONE and bearishCrossover:
            LL = High
            ZigZagBuffer1[i] = LL
            currentState = LL_FOUND
            zag_color[i] = 0.0
            res = 1
        elif currentState == LL_FOUND and bullishCrossover:
            HL = Low
            ZigZagBuffer2[i] = HL
            currentState = HL_FOUND
            zag_color[i] = 1.0
            res = 2
        elif currentState == HL_FOUND and bearishCrossover:
            LH = High
            ZigZagBuffer1[i] = LH
            currentState = LH_FOUND
            zag_color[i] = 0.0
            res = 3
        elif currentState == LH_FOUND and bullishCrossover:
            HH = Low
            ZigZagBuffer2[i] = HH
            currentState = HH_FOUND
            zag_color[i] = 1.0
            res = 4
        elif currentState == HH_FOUND:
            currentState = NONE
        if currentState == LL_FOUND and LL < HL:
            zag_color[i] = 2.0
        if currentState == HH_FOUND and HH > LH:
            zag_color[i] = 2.0
        if alerts:
            if ((res == 1 or res == 2) or res == 3) or res == 4:
                if lastAlertTime < barOpenTime:
                    Alert('Zigzag leg completed')
                    lastAlertTime = time[i]
    return rates_total

# ---- global variables initialised from expressions
lastAlertTime = TimeCurrent()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ZigzagOnMacross(_MQL5Indicator):
    name = 'Zigzag on macross'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA1Period': 5,  # Fast period (green)
        'MA2Period': 8,  # Slow period (red)
        'Backstep': 3,  # Backstep
        'alerts': False,  # Alert on leg change
    }

