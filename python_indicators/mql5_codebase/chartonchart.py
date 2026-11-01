"""ChartOnChart — converted from MQL5: MQL5 Indicators/Chart on Chart/ChartOnChart.mq5

Copyright: Copyright 2016 prostotrader; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2016 prostotrader', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 15}, 'colors': {1: [16777215, 32768, 255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: ''}, 'levels': [0.0], 'description': [], 'name': 'ChartOnChart', 'source': 'MQL5 Indicators/Chart on Chart/ChartOnChart.mq5', 'folder': 'Chart on Chart', 'inputs': [{'mql': 'SecSymb', 'py': 'SecSymb', 'param': None, 'type': 'string', 'default': 'RTS-12.16', 'label': 'Отображаемый символ', 'sinput': False}, {'mql': 'Match', 'py': 'Match', 'param': 'Match', 'type': 'bool', 'default': True, 'label': 'Точное совпадение свечей по времени', 'sinput': False}, {'mql': 'LineColor', 'py': 'LineColor', 'param': None, 'type': 'color', 'default': 16777215, 'label': 'Цвет линии', 'sinput': False}, {'mql': 'BullColor', 'py': 'BullColor', 'param': None, 'type': 'color', 'default': 32768, 'label': 'Цвет бычьей свечи', 'sinput': False}, {'mql': 'BearColor', 'py': 'BearColor', 'param': None, 'type': 'color', 'default': 255, 'label': 'Цвет медвежьей свечи', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SecSymb = _input('SecSymb', 'RTS-12.16')  # Отображаемый символ
Match = _input('Match', True)  # Точное совпадение свечей по времени
LineColor = _input('LineColor', clrWhite)  # Цвет линии
BullColor = _input('BullColor', clrGreen)  # Цвет бычьей свечи
BearColor = _input('BearColor', clrRed)  # Цвет медвежьей свечи
Buffer1 = Arr(0, 0.0)
Buffer2 = Arr(0, 0.0)
Buffer3 = Arr(0, 0.0)
Buffer4 = Arr(0, 0.0)
LastBuffer = Arr(0, 0.0)
att_cnt = 0.0

def OnInit():
    global att_cnt
    att_cnt = 1.0
    if not SymbolSelect(SecSymb, True):
        Alert('Не правильно выбран символ ' + SecSymb)
        return INIT_FAILED
    digits = _int(SymbolInfoInteger(SecSymb, SYMBOL_DIGITS))
    IndicatorSetInteger(INDICATOR_DIGITS, digits)
    IndicatorSetString(INDICATOR_SHORTNAME, SecSymb)
    SetIndexBuffer(0, Buffer1, INDICATOR_DATA)
    SetIndexBuffer(1, Buffer2, INDICATOR_DATA)
    SetIndexBuffer(2, Buffer3, INDICATOR_DATA)
    SetIndexBuffer(3, Buffer4, INDICATOR_DATA)
    SetIndexBuffer(4, LastBuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(Buffer1, True)
    ArraySetAsSeries(Buffer2, True)
    ArraySetAsSeries(Buffer3, True)
    ArraySetAsSeries(Buffer4, True)
    ArraySetAsSeries(LastBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, LineColor)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, BullColor)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 2, BearColor)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrYellow)
    PlotIndexSetString(0, PLOT_LABEL, ' Open;' + ' High;' + ' Low;' + ' Close')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global att_cnt
    ArraySetAsSeries(time, True)
    rates = Arr(0, 0, factory=MqlRates)
    if prev_calculated == 0:
        ArrayInitialize(Buffer1, EMPTY_VALUE)
        ArrayInitialize(Buffer2, EMPTY_VALUE)
        ArrayInitialize(Buffer3, EMPTY_VALUE)
        ArrayInitialize(Buffer4, EMPTY_VALUE)
        ArrayInitialize(LastBuffer, EMPTY_VALUE)
        attempts = 0
        result = 0
        a_cnt = 1000
        while attempts < a_cnt:
            result = CopyRates(SecSymb, Period(), 0, rates_total, rates)
            if result > 0:
                break
            for i in range(0, a_cnt):
                result = 1
                result = 0
            attempts += 1
        if result > 0:
            mem_pos = result
            ArraySetAsSeries(rates, True)
            if Match:
                for i in range(rates_total - 1, 0 - 1, -1):
                    is_done = False
                    for j in range(mem_pos - 1, 0 - 1, -1):
                        if time[i] == rates[j].time:
                            mem_pos = j
                            Buffer1[i] = rates[j].open
                            Buffer2[i] = rates[j].high
                            Buffer3[i] = rates[j].low
                            Buffer4[i] = rates[j].close
                            is_done = True
                            break
                    if not is_done:
                        Buffer1[i] = EMPTY_VALUE
                        Buffer2[i] = EMPTY_VALUE
                        Buffer3[i] = EMPTY_VALUE
                        Buffer4[i] = EMPTY_VALUE
            else:
                for i in range(result - 1, 0 - 1, -1):
                    Buffer1[i] = rates[i].open
                    Buffer2[i] = rates[i].high
                    Buffer3[i] = rates[i].low
                    Buffer4[i] = rates[i].close
        else:
            if att_cnt == 5:
                Alert('Данные по символу ' + SecSymb + ' не скопированы! Перегрузите индикатор.')
            else:
                att_cnt += 1
                return 0
    else:
        diff = rates_total - prev_calculated
        if diff > 0:
            i = diff - 1
            while i > 0:
                Buffer1[i] = Buffer1[i + 1]
                Buffer2[i] = Buffer2[i + 1]
                Buffer3[i] = Buffer3[i + 1]
                Buffer4[i] = Buffer4[i + 1]
                i += 1
            Buffer1[0] = EMPTY_VALUE
            Buffer2[0] = EMPTY_VALUE
            Buffer3[0] = EMPTY_VALUE
            Buffer4[0] = EMPTY_VALUE
    if CopyRates(SecSymb, Period(), 0, 1, rates) == 1:
        if time[0] == rates[0].time:
            Buffer1[0] = rates[0].open
            Buffer2[0] = rates[0].high
            Buffer3[0] = rates[0].low
            Buffer4[0] = rates[0].close
    else:
        attempts = 0
        a_cnt = 10
        result = 0
        while attempts < a_cnt:
            result = CopyRates(SecSymb, Period(), 0, 1, rates)
            if result > 0:
                break
            for i in range(0, 100):
                result = 1
                result = 0
            attempts += 1
        if result > 0:
            if time[0] == rates[0].time:
                Buffer1[0] = rates[0].open
                Buffer2[0] = rates[0].high
                Buffer3[0] = rates[0].low
                Buffer4[0] = rates[0].close
        else:
            Alert('Данные тика не скопированы!')
    s_last = SymbolInfoDouble(SecSymb, SYMBOL_LAST)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, s_last)
    LastBuffer[0] = s_last
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ChartOnChart(_MQL5Indicator):
    name = 'ChartOnChart'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Match': True,  # Точное совпадение свечей по времени
    }

