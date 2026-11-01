"""candlesizes — converted from MQL5: MQL5 Indicators/CandleSizes/candlesizes.mq5

Copyright: Tapochun; Link: https://login.mql5.com/ru/users/tapochun; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Tapochun', 'link': 'https://login.mql5.com/ru/users/tapochun', 'version': '1.00', 'window': 'separate', 'indicator_plots': 2, 'indicator_buffers': 3, 'indicator_minimum': 0.0}, 'types': {1: 10, 2: 1}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {1: 'CandleSize', 2: 'csAverage'}, 'levels': [], 'description': [], 'name': 'candlesizes', 'source': 'MQL5 Indicators/CandleSizes/candlesizes.mq5', 'folder': 'CandleSizes', 'inputs': [{'mql': 'inpType', 'py': 'inpType', 'param': 'inpType', 'type': 'int', 'default': 0, 'label': 'Тип построения индикатора', 'sinput': False}, {'mql': 'inpClr', 'py': 'inpClr', 'param': None, 'type': 'color', 'default': 65280, 'label': 'Цвет построения', 'sinput': False}, {'mql': 'inpNeutralClr', 'py': 'inpNeutralClr', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'Нейтральный цвет', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_CONSTRUCTION_TYPE
upper_shadows = 0
lower_shadows = 1
bodies = 2
_enum('ENUM_CONSTRUCTION_TYPE', {0: 'upper_shadows', 1: 'lower_shadows', 2: 'bodies'})

# ---- inputs and global variables
bufSize = Arr(0, 0.0)  # Буфер значений
bufSizeClr = Arr(0, 0.0)  # Буфер цвета
bufAverage = Arr(0, 0.0)  # Буфер средних значений
inpType = _input('inpType', upper_shadows)  # Тип построения индикатора
inpClr = _input('inpClr', clrLime)  # Цвет построения
inpNeutralClr = _input('inpNeutralClr', clrGray)  # Нейтральный цвет

def OnInit():
    if Period() > PERIOD_H2:
        Print('OnInit', ': ВНИМАНИЕ! Индикатор предназначен для работы на ТФ ниже Н2')
        return INIT_FAILED
    SetIndicatorParameters(inpType, inpClr, inpNeutralClr)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total <= 0:
        return 0
    if prev_calculated != 0:
        n = 0
        if rates_total > prev_calculated:
            bufSize[rates_total - 1] = 0.0
            bufAverage[rates_total - 1] = bufAverage[rates_total - 2]
            n = rates_total - 2
            Calculation_bar(inpType, n, _GlobRef(globals(), '_s_OnCalculate_dCount'), _GlobRef(globals(), '_s_OnCalculate_dSum'), time, high, low, open, close)
            CheckNewDay(time[n + 1], _GlobRef(globals(), '_s_OnCalculate_dNum'), _GlobRef(globals(), '_s_OnCalculate_dCount'), _GlobRef(globals(), '_s_OnCalculate_dSum'))
        else:
            n = rates_total - 1
            Calculation(inpType, n, _s_OnCalculate_dCount + 1, _s_OnCalculate_dSum, time[n], high[n], low[n], open[n], close[n])
    else:
        ArrayInitialize(bufSize, 0.0)
        ArrayInitialize(bufAverage, 0.0)
        first = GetFirstBar(time, rates_total, _GlobRef(globals(), '_s_OnCalculate_dNum'))
        if first == 0:
            return 0
        for i in range(first, rates_total - 1):
            Calculation_bar(inpType, i, _GlobRef(globals(), '_s_OnCalculate_dCount'), _GlobRef(globals(), '_s_OnCalculate_dSum'), time, high, low, open, close)
            CheckNewDay(time[i + 1], _GlobRef(globals(), '_s_OnCalculate_dNum'), _GlobRef(globals(), '_s_OnCalculate_dCount'), _GlobRef(globals(), '_s_OnCalculate_dSum'))
    return rates_total

def GetCandleType(open, close):
    if open > close:
        return 1
    else:
        return 0

def SetIndicatorParameters(type_, clr, neutralClr):
    SetIndexBuffer(0, bufSize)
    SetIndexBuffer(1, bufSizeClr, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, bufAverage)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 2)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, neutralClr)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, clr)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, 0, clr)
    name = 'CandleSizes (' + GetConstructionStringType(type_) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, name)
    return True

def GetConstructionStringType(type_):
    _sw1 = type_
    if _sw1 == upper_shadows:
        return 'upper'
    elif _sw1 == lower_shadows:
        return 'lower'
    elif _sw1 == bodies:
        return 'bodies'
    else:
        Print('GetConstructionStringType', ': ОШИБКА! Неизвестный тип построения ' + EnumToString(type_, 'ENUM_CONSTRUCTION_TYPE'))
        return ''

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

def Calculation(type_, num, dCount, dSum, time, high, low, open, close):
    cdlType = GetCandleType(open, close)
    size = GetElementSize(type_, cdlType, open, high, low, close)
    if size == 0:
        return
    bufSize[num] = size
    bufSizeClr[num] = 0.0
    bufAverage[num] = _int(MathRound(_idiv(dSum + size, dCount)))
    if bufSize[num] > bufAverage[num]:
        bufSizeClr[num] = 1.0

def Calculation_bar(type_, num, dCount, dSum, time, high, low, open, close):
    dCount.v += 1
    cdlType = GetCandleType(open[num], close[num])
    size = GetElementSize(type_, cdlType, open[num], high[num], low[num], close[num])
    if size == -1:
        return
    dSum.v += size
    bufSize[num] = size
    bufAverage[num] = _int(MathRound(_idiv(dSum.v, dCount.v)))
    if bufSize[num] > bufAverage[num]:
        bufSizeClr[num] = 1.0
    else:
        bufSizeClr[num] = 0.0

def GetElementSize(type_, cdlType, open, high, low, close):
    _sw2 = type_
    if _sw2 == upper_shadows:
        if cdlType == 0:
            return _int(_fdiv(NormalizeDouble(high - close, Digits()), Point()))
        else:
            return _int(_fdiv(NormalizeDouble(high - open, Digits()), Point()))
    elif _sw2 == lower_shadows:
        if cdlType == 0:
            return _int(_fdiv(NormalizeDouble(open - low, Digits()), Point()))
        else:
            return _int(_fdiv(NormalizeDouble(close - low, Digits()), Point()))
    elif _sw2 == bodies:
        if cdlType == 0:
            return _int(_fdiv(NormalizeDouble(close - open, Digits()), Point()))
        else:
            return _int(_fdiv(NormalizeDouble(open - close, Digits()), Point()))
    else:
        Print('GetElementSize', ': ОШИБКА! Неизвестный тип построения: ' + EnumToString(type_, 'ENUM_CONSTRUCTION_TYPE'))
        return -1

def CheckNewDay(time, dNum, dCount, dSum):
    currDayNum = GetDayNumber(time)
    if currDayNum != dNum.v:
        dNum.v = currDayNum
        dCount.v = 0
        dSum.v = 0

# ---- static local variables
_s_OnCalculate_dNum = 0
_s_OnCalculate_dCount = 0
_s_OnCalculate_dSum = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Candlesizes(_MQL5Indicator):
    name = 'candlesizes'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpType': _Choice({0: 'Верхние тени', 1: 'Нижние тени', 2: 'Тела'}, default=0),  # Тип построения индикатора
    }

