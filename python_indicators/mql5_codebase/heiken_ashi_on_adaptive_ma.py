"""heiken_ashi_on_adaptive_ma — converted from MQL5: MQL5 Indicators/Heiken Ashi On Adaptive Moving Average/heiken_ashi_on_adaptive_ma.mq5

Copyright: extern.fx; Link: extern.fx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'extern.fx', 'link': 'extern.fx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16711680, 255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Heiken Ashi Open;Heiken Ashi High;Heiken Ashi Low;Heiken Ashi Close'}, 'levels': [], 'description': [], 'name': 'heiken_ashi_on_adaptive_ma', 'source': 'MQL5 Indicators/Heiken Ashi On Adaptive Moving Average/heiken_ashi_on_adaptive_ma.mq5', 'folder': 'Heiken Ashi On Adaptive Moving Average', 'inputs': [{'mql': 'AMAPeriod', 'py': 'AMAPeriod', 'param': 'AMAPeriod', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'FastEMA', 'py': 'FastEMA', 'param': 'FastEMA', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'SlowEMA', 'py': 'SlowEMA', 'param': 'SlowEMA', 'type': 'int', 'default': 30, 'label': '', 'sinput': False}, {'mql': 'AMAShift', 'py': 'AMAShift', 'param': 'AMAShift', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
AMAPeriod = _input('AMAPeriod', 9)
FastEMA = _input('FastEMA', 2)
SlowEMA = _input('SlowEMA', 30)
AMAShift = _input('AMAShift', 0)
extOpen = Arr(0, 0.0)
extClose = Arr(0, 0.0)
extHigh = Arr(0, 0.0)
extLow = Arr(0, 0.0)
extColor = Arr(0, 0.0)
AMAOpen = Arr(0, 0.0)
AMAClose = Arr(0, 0.0)
AMAHigh = Arr(0, 0.0)
AMALow = Arr(0, 0.0)
AMAOpenHandle = 0
AMACloseHandle = 0
AMAHighHandle = 0
AMALowHandle = 0

def OnInit():
    global AMACloseHandle, AMAHighHandle, AMALowHandle, AMAOpenHandle
    SetIndexBuffer(0, extOpen, INDICATOR_DATA)
    SetIndexBuffer(3, extClose, INDICATOR_DATA)
    SetIndexBuffer(1, extHigh, INDICATOR_DATA)
    SetIndexBuffer(2, extLow, INDICATOR_DATA)
    SetIndexBuffer(4, extColor, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, AMAOpen, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, AMAClose, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, AMAHigh, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, AMALow, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Heiken Ashi')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    AMAOpenHandle = iAMA(Symbol(), Period(), AMAPeriod, FastEMA, SlowEMA, AMAShift, PRICE_OPEN)
    AMACloseHandle = iAMA(Symbol(), Period(), AMAPeriod, FastEMA, SlowEMA, AMAShift, PRICE_CLOSE)
    AMAHighHandle = iAMA(Symbol(), Period(), AMAPeriod, FastEMA, SlowEMA, AMAShift, PRICE_HIGH)
    AMALowHandle = iAMA(Symbol(), Period(), AMAPeriod, FastEMA, SlowEMA, AMAShift, PRICE_LOW)
    ArraySetAsSeries(extOpen, True)
    ArraySetAsSeries(extClose, True)
    ArraySetAsSeries(extHigh, True)
    ArraySetAsSeries(extLow, True)
    ArraySetAsSeries(AMAOpen, True)
    ArraySetAsSeries(AMAClose, True)
    ArraySetAsSeries(AMAHigh, True)
    ArraySetAsSeries(AMALow, True)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    copy_count = 0
    if prev_calculated == 0:
        copy_count = rates_total - SlowEMA
    else:
        copy_count = rates_total - prev_calculated + 1
    if CopyBuffer(AMAOpenHandle, 0, 0, copy_count, AMAOpen) < 0:
        Print('HeikenAshiOnAMA: ошибка копирования буфера индикатора...')
        return 1
    if CopyBuffer(AMACloseHandle, 0, 0, copy_count, AMAClose) < 0:
        Print('HeikenAshiOnAMA: ошибка копирования буфера индикатора...')
        return 1
    if CopyBuffer(AMAHighHandle, 0, 0, copy_count, AMAHigh) < 0:
        Print('HeikenAshiOnAMA: ошибка копирования буфера индикатора...')
        return 1
    if CopyBuffer(AMALowHandle, 0, 0, copy_count, AMALow) < 0:
        Print('HeikenAshiOnAMA: ошибка копирования буфера индикатора...')
        return 1
    total = rates_total - SlowEMA
    if prev_calculated == 0:
        extOpen[total] = AMAOpen[total]
        extClose[total] = AMAClose[total]
        extHigh[total] = AMAHigh[total]
        extLow[total] = AMALow[total]
        total += 1
    else:
        total = rates_total - prev_calculated + 1
    for i in range(total, 0 - 1, -1):
        haOpen = (extOpen[i + 1] + extClose[i + 1]) / 2
        haClose = (AMAOpen[i] + AMAClose[i] + AMAHigh[i] + AMAClose[i]) / 4
        haHigh = MathMax(AMAHigh[i], MathMax(haOpen, haClose))
        haLow = MathMin(AMALow[i], MathMin(haOpen, haClose))
        extOpen[i] = haOpen
        extClose[i] = haClose
        extHigh[i] = haHigh
        extLow[i] = haLow
        if haOpen < haClose:
            extColor[i] = 0.0
        else:
            extColor[i] = 1.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HeikenAshiOnAdaptiveMa(_MQL5Indicator):
    name = 'heiken_ashi_on_adaptive_ma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'AMAPeriod': 9,
        'FastEMA': 2,
        'SlowEMA': 30,
        'AMAShift': 0,
    }

