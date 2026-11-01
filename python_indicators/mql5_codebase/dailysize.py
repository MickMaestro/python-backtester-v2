"""DailySize — converted from MQL5: MQL5 Indicators/DailySize/DailySize.mq5

Copyright: Tapochun; Link: https://login.mql5.com/ru/users/tapochun; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Tapochun', 'link': 'https://login.mql5.com/ru/users/tapochun', 'version': '1.00', 'window': 'separate', 'indicator_minimum': 0.0, 'indicator_plots': 1, 'indicator_buffers': 1}, 'types': {1: 3}, 'colors': {1: [255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'DailySize'}, 'levels': [], 'description': [], 'name': 'DailySize', 'source': 'MQL5 Indicators/DailySize/DailySize.mq5', 'folder': 'DailySize', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
bufRange = Arr(0, 0.0)

def OnInit():
    answer = CheckTimeframe()
    if not answer:
        return INIT_PARAMETERS_INCORRECT
    SetIndexBuffer(0, bufRange)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total <= 0:
        return 0
    if prev_calculated != 0:
        Calculation(rates_total - 1, _GlobRef(globals(), '_s_OnCalculate_dNum'), _GlobRef(globals(), '_s_OnCalculate_dHigh'), _GlobRef(globals(), '_s_OnCalculate_dLow'), rates_total, time, high, low)
    else:
        ArrayInitialize(bufRange, 0.0)
        firstBar = GetFirstBar(time, rates_total, _GlobRef(globals(), '_s_OnCalculate_dNum'))
        if firstBar == 0:
            return 0
        Calculation(firstBar, _GlobRef(globals(), '_s_OnCalculate_dNum'), _GlobRef(globals(), '_s_OnCalculate_dHigh'), _GlobRef(globals(), '_s_OnCalculate_dLow'), rates_total, time, high, low)
    return rates_total

def CheckTimeframe():
    if Period() > PERIOD_D1:
        Print('CheckTimeframe', ': Индикатор предназначен для запуска на ТФ до D1. Уменьшите ТФ!')
        return False
    else:
        return True

def GetFirstBar(time, rates_total, dayNum):
    prev = GetDayNumber(time[0])
    curr = 0
    for i in range(1, rates_total):
        curr = GetDayNumber(time[i])
        if curr == prev:
            continue
        else:
            dayNum.v = curr
            return i
    Print('GetFirstBar', ': Ожидаем больше данных..')
    return 0

def GetDayNumber(time):
    tStr = MqlDateTime()
    TimeToStruct(time, tStr)
    return tStr.day

def Calculation(firstBar, dNum, dHigh, dLow, rates_total, time, high, low):
    iNum = 0
    for i in range(firstBar, rates_total):
        iNum = GetDayNumber(time[i])
        if dNum.v != iNum:
            dNum.v = iNum
            dHigh.v = high[i]
            dLow.v = low[i]
        else:
            if high[i] > dHigh.v:
                dHigh.v = high[i]
            if low[i] < dLow.v:
                dLow.v = low[i]
        bufRange[i] = MathRound(_fdiv(dHigh.v - dLow.v, Point()))

# ---- static local variables
_s_OnCalculate_dNum = 0
_s_OnCalculate_dHigh = 0.0
_s_OnCalculate_dLow = DBL_MAX


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DailySize(_MQL5Indicator):
    name = 'DailySize'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

