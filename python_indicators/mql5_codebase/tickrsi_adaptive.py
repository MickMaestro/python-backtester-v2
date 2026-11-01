"""TickRSI_adaptive — converted from MQL5: MQL5 Indicators/Tick RSI Adaptive/TickRSI_adaptive.mq5

Copyright: Copyright © 2008, TrendLaboratory; Link: http://finance.groups.yahoo.com/group/TrendLaboratory

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, TrendLaboratory', 'link': 'http://finance.groups.yahoo.com/group/TrendLaboratory', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [65280], 2: [16748574], 3: [4678655]}, 'widths': {1: 2, 2: 2, 3: 1}, 'styles': {3: 2}, 'labels': {1: 'ARSI', 2: 'Fast', 3: 'Slow'}, 'levels': [], 'description': [], 'name': 'TickRSI_adaptive', 'source': 'MQL5 Indicators/Tick RSI Adaptive/TickRSI_adaptive.mq5', 'folder': 'Tick RSI Adaptive', 'inputs': [{'mql': 'ARSIPeriod', 'py': 'ARSIPeriod', 'param': 'ARSIPeriod', 'type': 'int', 'default': 14, 'label': 'Adaptive RSI Period', 'sinput': False}, {'mql': 'FastMA', 'py': 'FastMA', 'param': 'FastMA', 'type': 'int', 'default': 5, 'label': 'Fast MA Length(Period)', 'sinput': False}, {'mql': 'SlowMA', 'py': 'SlowMA', 'param': 'SlowMA', 'type': 'int', 'default': 14, 'label': 'Slow MA Length(Period)', 'sinput': False}, {'mql': 'MA_Mode', 'py': 'MA_Mode', 'param': 'MA_Mode', 'type': 'int', 'default': 0, 'label': 'MA Mode: 0-SMA,1-EMA,2-Wilder(SMMA),3-LWMA', 'sinput': False}, {'mql': 'UseDelimiter', 'py': 'UseDelimiter', 'param': 'UseDelimiter', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'DelimColor', 'py': 'DelimColor', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'Color of Bars Delimiter', 'sinput': False}, {'mql': 'MaxTicks', 'py': 'MaxTicks', 'param': 'MaxTicks', 'type': 'int', 'default': 200, 'label': 'Max Number of ticks', 'sinput': False}, {'mql': 'NumTicks', 'py': 'NumTicks', 'param': 'NumTicks', 'type': 'int', 'default': 0, 'label': 'TimeFrame in ticks (=0 if NumSecs  > 0)', 'sinput': False}, {'mql': 'RSI_ind', 'py': 'RSI_ind', 'param': None, 'type': 'string', 'default': 'Examples\\RSI', 'label': 'Load RSI indicator', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ARSIPeriod = _input('ARSIPeriod', 14)  # Adaptive RSI Period
FastMA = _input('FastMA', 5)  # Fast MA Length(Period)
SlowMA = _input('SlowMA', 14)  # Slow MA Length(Period)
MA_Mode = _input('MA_Mode', 0)  # MA Mode: 0-SMA,1-EMA,2-Wilder(SMMA),3-LWMA
UseDelimiter = _input('UseDelimiter', 1)
DelimColor = _input('DelimColor', clrGray)  # Color of Bars Delimiter
MaxTicks = _input('MaxTicks', 200)  # Max Number of ticks
NumTicks = _input('NumTicks', 0)  # TimeFrame in ticks (=0 if NumSecs  > 0)
RSI_ind = _input('RSI_ind', 'Examples\\RSI')  # Load RSI indicator
Ticks = Arr(0, 0.0)
Fast = Arr(0, 0.0)
Slow = Arr(0, 0.0)
ARSI = Arr(0, 0.0)
barCounter = 0
tickCounter = 0
delimeterCounter = 0
pTime = 0
short_name = ""
setup = ""
digits = 3
handle = INVALID_HANDLE

def OnInit():
    global handle, pTime, setup, short_name
    SetIndexBuffer(0, Ticks, INDICATOR_DATA)
    SetIndexBuffer(1, Fast, INDICATOR_DATA)
    SetIndexBuffer(2, Slow, INDICATOR_DATA)
    SetIndexBuffer(3, ARSI, INDICATOR_DATA)
    ArraySetAsSeries(Ticks, True)
    ArraySetAsSeries(Fast, True)
    ArraySetAsSeries(Slow, True)
    ArraySetAsSeries(ARSI, True)
    IndicatorSetInteger(INDICATOR_DIGITS, SymbolInfoInteger(Symbol(), SYMBOL_DIGITS, _GlobRef(globals(), 'digits')))
    short_name = 'TickAdaptiveRSI_v1(' + IntegerToString(ARSIPeriod) + ',' + IntegerToString(FastMA) + ',' + IntegerToString(SlowMA) + ',' + IntegerToString(MA_Mode) + ',' + IntegerToString(UseDelimiter) + ')'
    handle = iCustom(None, PERIOD_CURRENT, RSI_ind)
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    setup = short_name + ': '
    pTime = iTime(Symbol(), Period(), 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global tickCounter
    tickCounter += 1
    if tickCounter == 0:
        for i in range(rates_total - 1, 0 - 1, -1):
            Ticks[i] = 0.0
            Fast[i] = 0.0
            Slow[i] = 0.0
    if Ticks[tickCounter] == 0:
        Fast[tickCounter] = EMPTY_VALUE
        Slow[tickCounter] = EMPTY_VALUE
        ARSI[tickCounter] = EMPTY_VALUE
    if tickCounter >= MaxTicks:
        tickCounter = MaxTicks
        Ticks[tickCounter] = 0.0
        Fast[tickCounter] = 0.0
        Slow[tickCounter] = 0.0
    CopyBuffer(handle, 0, 0, MaxTicks, ARSI)
    if ARSI[1] < (2 * ARSI[0]):
        Ticks[0] = (ARSI[0] - ARSI[1]) * 10000
    if MA_Mode == 0:
        if tickCounter >= (FastMA + ARSIPeriod):
            Fast[0] = TickSMA(Ticks, FastMA)
        if tickCounter >= (SlowMA + ARSIPeriod):
            Slow[0] = TickSMA(Ticks, SlowMA)
    elif MA_Mode == 1:
        if tickCounter == FastMA:
            Fast[0] = TickSMA(Ticks, FastMA)
        elif tickCounter > FastMA:
            Fast[0] = TickEMA(Ticks, Fast, FastMA)
        if tickCounter == SlowMA:
            Slow[0] = TickSMA(Ticks, SlowMA)
        elif tickCounter > SlowMA:
            Slow[0] = TickEMA(Ticks, Slow, SlowMA)
    elif MA_Mode == 2:
        if tickCounter == ((2 * FastMA) - 1):
            Fast[0] = TickSMA(Ticks, (2 * FastMA) - 1)
        elif tickCounter > ((2 * FastMA) - 1):
            Fast[0] = TickEMA(Ticks, Fast, (2 * FastMA) - 1)
        if tickCounter == ((2 * SlowMA) - 1):
            Slow[0] = TickSMA(Ticks, (2 * SlowMA) - 1)
        elif tickCounter > ((2 * SlowMA) - 1):
            Slow[0] = TickEMA(Ticks, Slow, (2 * SlowMA) - 1)
    if MA_Mode == 3:
        if tickCounter >= (FastMA + ARSIPeriod):
            Fast[0] = TickLWMA(Ticks, FastMA)
        if tickCounter >= (SlowMA + ARSIPeriod):
            Slow[0] = TickLWMA(Ticks, SlowMA)
    return rates_total

def TickSMA(array, per):
    Sum = 0.0
    for i in range(0, per):
        Sum += array[i]
    return _fdiv(Sum, per)

def TickEMA(array1, array2, per):
    return array2[1] + (_fdiv(2.0, 1 + per) * (array1[0] - array2[1]))

def TickLWMA(array, per):
    Sum = 0.0
    Weight = 0.0
    for i in range(0, per):
        Weight += per - i
        Sum += array[i] * (per - i)
    if Weight > 0:
        return _fdiv(Sum, Weight)
    else:
        return 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TickRSIAdaptive(_MQL5Indicator):
    name = 'TickRSI_adaptive'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'ARSIPeriod': 14,  # Adaptive RSI Period
        'FastMA': 5,  # Fast MA Length(Period)
        'SlowMA': 14,  # Slow MA Length(Period)
        'MA_Mode': 0,  # MA Mode: 0-SMA,1-EMA,2-Wilder(SMMA),3-LWMA
        'UseDelimiter': 1,
        'MaxTicks': 200,  # Max Number of ticks
        'NumTicks': 0,  # TimeFrame in ticks (=0 if NumSecs  > 0)
    }

