"""dayextremumzones — converted from MQL5: MQL5 Indicators/DayExtremumZones/dayextremumzones.mq5

Индикатор отображает зоны максимумов и минимумов дня в процентах от дневного движения.
Использует индикатор DailySize https://www.mql5.com/ru/code/13323
Copyright: Tapochun; Link: https://login.mql5.com/ru/users/tapochun; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Tapochun', 'link': 'https://login.mql5.com/ru/users/tapochun', 'version': '1.01', 'window': 'chart', 'indicator_plots': 2, 'indicator_buffers': 4}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Индикатор отображает зоны максимумов и минимумов дня в процентах от дневного движения.', 'Использует индикатор DailySize https://www.mql5.com/ru/code/13323'], 'name': 'dayextremumzones', 'source': 'MQL5 Indicators/DayExtremumZones/dayextremumzones.mq5', 'folder': 'DayExtremumZones', 'inputs': [{'mql': 'inpUpZonePct', 'py': 'inpUpZonePct', 'param': 'inpUpZonePct', 'type': 'int', 'default': 15, 'label': 'Размер зоны максимумов, % от дневного движения [0..50]', 'sinput': False}, {'mql': 'inpDnZonePct', 'py': 'inpDnZonePct', 'param': 'inpDnZonePct', 'type': 'int', 'default': 15, 'label': 'Размер зоны минимумов, % от дневного движения [0..50]', 'sinput': False}, {'mql': 'inpDrawType', 'py': 'inpDrawType', 'param': 'inpDrawType', 'type': 'int', 'default': 3, 'label': 'Тип отрисовки', 'sinput': False}, {'mql': 'inpDrawInternalZone', 'py': 'inpDrawInternalZone', 'param': 'inpDrawInternalZone', 'type': 'bool', 'default': True, 'label': 'Отображать внутреннюю зону (для типов "Линия"/"Стрелки"/"Не отрисовывается")', 'sinput': False}, {'mql': 'inpShowData', 'py': 'inpShowData', 'param': 'inpShowData', 'type': 'bool', 'default': False, 'label': 'Отображать значения индикатора в окне данных', 'sinput': False}, {'mql': 'd1', 'py': 'd1', 'param': None, 'type': 'string', 'default': '', 'label': 'Общие настройки отрисовки', 'sinput': True}, {'mql': 'inpUpWidth', 'py': 'inpUpWidth', 'param': 'inpUpWidth', 'type': 'int', 'default': 1, 'label': 'Толщина отрисовки зоны максимумов', 'sinput': False}, {'mql': 'inpDnWidth', 'py': 'inpDnWidth', 'param': 'inpDnWidth', 'type': 'int', 'default': 1, 'label': 'Толщина отрисовки зоны минимумов', 'sinput': False}, {'mql': 'inpUpColor', 'py': 'inpUpColor', 'param': None, 'type': 'color', 'default': 15128749, 'label': 'Цвет отрисовки зоны максимумов', 'sinput': False}, {'mql': 'inpDnColor', 'py': 'inpDnColor', 'param': None, 'type': 'color', 'default': 8388352, 'label': 'Цвет отрисовки зоны минимумов', 'sinput': False}, {'mql': 'd2', 'py': 'd2', 'param': None, 'type': 'string', 'default': '', 'label': 'Настройки отрисовки типа "Линия"/"Гистограмма"', 'sinput': True}, {'mql': 'inpUpStyle', 'py': 'inpUpStyle', 'param': 'inpUpStyle', 'type': 'int', 'default': 2, 'label': 'Стиль линии/зоны максимумов', 'sinput': False}, {'mql': 'inpDnStyle', 'py': 'inpDnStyle', 'param': 'inpDnStyle', 'type': 'int', 'default': 2, 'label': 'Стиль линии/зоны минимумов', 'sinput': False}, {'mql': 'd3', 'py': 'd3', 'param': None, 'type': 'string', 'default': '', 'label': 'Настройки отрисовки типа "Стрелки"', 'sinput': True}, {'mql': 'inpUpArrowCode', 'py': 'inpUpArrowCode', 'param': 'inpUpArrowCode', 'type': 'int', 'default': 158, 'label': 'Код стрелок зоны максимумов (для типа "Стрелки")', 'sinput': False}, {'mql': 'inpDnArrowCode', 'py': 'inpDnArrowCode', 'param': 'inpDnArrowCode', 'type': 'int', 'default': 158, 'label': 'Код стрелок зоны минимумов (для типа "Стрелки")', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_DW_TYPE
FILLING = 0
HISTOGRAM2 = 1
LINE = 2
ARROW = 3
NONE = 4
_enum('ENUM_DW_TYPE', {0: 'FILLING', 1: 'HISTOGRAM2', 2: 'LINE', 3: 'ARROW', 4: 'NONE'})

# ---- inputs and global variables
bufW = Arr(0, 0.0)  # Значения максимумов дневного диапазона
bufX = Arr(0, 0.0)  # Граница зоны максимумов/значения минимумов дневного диапазона
bufY = Arr(0, 0.0)  # Значения минимумов дневного диапазона
bufZ = Arr(0, 0.0)  # Граница зоны минимумов
globHandle = 0  # Хэндл индикатора дневных диапазонов (DailySize)
inpUpZonePct = _input('inpUpZonePct', 15)  # Размер зоны максимумов, % от дневного движения [0..50]
inpDnZonePct = _input('inpDnZonePct', 15)  # Размер зоны минимумов, % от дневного движения [0..50]
inpDrawType = _input('inpDrawType', ARROW)  # Тип отрисовки
inpDrawInternalZone = _input('inpDrawInternalZone', True)  # Отображать внутреннюю зону (для типов "Линия"/"Стрелки"/"Не отрисовывается")
inpShowData = _input('inpShowData', False)  # Отображать значения индикатора в окне данных
d1 = _input('d1', '')  # Общие настройки отрисовки
inpUpWidth = _input('inpUpWidth', 1)  # Толщина отрисовки зоны максимумов
inpDnWidth = _input('inpDnWidth', 1)  # Толщина отрисовки зоны минимумов
inpUpColor = _input('inpUpColor', clrLightBlue)  # Цвет отрисовки зоны максимумов
inpDnColor = _input('inpDnColor', clrSpringGreen)  # Цвет отрисовки зоны минимумов
d2 = _input('d2', '')  # Настройки отрисовки типа "Линия"/"Гистограмма"
inpUpStyle = _input('inpUpStyle', STYLE_DOT)  # Стиль линии/зоны максимумов
inpDnStyle = _input('inpDnStyle', STYLE_DOT)  # Стиль линии/зоны минимумов
d3 = _input('d3', '')  # Настройки отрисовки типа "Стрелки"
inpUpArrowCode = _input('inpUpArrowCode', 158)  # Код стрелок зоны максимумов (для типа "Стрелки")
inpDnArrowCode = _input('inpDnArrowCode', 158)  # Код стрелок зоны минимумов (для типа "Стрелки")

def OnInit():
    if ((inpUpZonePct < 0 or inpUpZonePct > 50) or inpDnZonePct < 0) or inpDnZonePct > 50:
        Print('dayextremumzones.mq5', ': ОШИБКА! Размер зон должен находиться в диапазоне от 0 до 50%. Проверьте входные параметры!')
        return INIT_PARAMETERS_INCORRECT
    if Period() > PERIOD_H2:
        Print('dayextremumzones.mq5', ': ОШИБКА! Индикатор предназначен для работы на ТФ не выше H2!')
        return INIT_PARAMETERS_INCORRECT
    if (inpDrawType == FILLING or inpDrawType == HISTOGRAM2) and (inpUpZonePct == 0 or inpDnZonePct == 0):
        Print('dayextremumzones.mq5', ": ОШИБКА! Отрисовка стилем 'Заливка' или 'Гистограмма' доступна только при размерах зон > 0. Проверьте входные параметры!")
        return INIT_PARAMETERS_INCORRECT
    SetIndexBuffer(0, bufW, INDICATOR_DATA)
    SetIndexBuffer(1, bufX, INDICATOR_DATA)
    SetIndexBuffer(2, bufY, INDICATOR_DATA)
    SetIndexBuffer(3, bufZ, INDICATOR_DATA)
    _sw1 = inpDrawType
    if _sw1 == FILLING:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_FILLING)
        PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_FILLING)
        PlotIndexSetString(0, PLOT_LABEL, 'dez: up;dez: upZone')
        PlotIndexSetString(1, PLOT_LABEL, 'dez: dn;dez: dnZone')
        PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 2)
        PlotIndexSetInteger(1, PLOT_COLOR_INDEXES, 2)
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, inpUpColor)
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, inpUpColor)
        PlotIndexSetInteger(1, PLOT_LINE_COLOR, 0, inpDnColor)
        PlotIndexSetInteger(1, PLOT_LINE_COLOR, 1, inpDnColor)
    elif _sw1 == HISTOGRAM2:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_HISTOGRAM2)
        PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_HISTOGRAM2)
        PlotIndexSetString(0, PLOT_LABEL, 'dez: up;dez: upZone')
        PlotIndexSetString(1, PLOT_LABEL, 'dez: dn;dez: dnZone')
        PlotIndexSetInteger(0, PLOT_LINE_STYLE, inpUpStyle)
        PlotIndexSetInteger(1, PLOT_LINE_STYLE, inpDnStyle)
    elif _sw1 == LINE:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_LINE)
        PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_LINE)
        PlotIndexSetInteger(0, PLOT_LINE_STYLE, inpUpStyle)
        PlotIndexSetInteger(1, PLOT_LINE_STYLE, inpDnStyle)
        PlotIndexSetString(0, PLOT_LABEL, 'dez: up')
        PlotIndexSetString(1, PLOT_LABEL, 'dez: dn')
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, inpUpColor)
        PlotIndexSetInteger(1, PLOT_LINE_COLOR, inpDnColor)
    elif _sw1 == ARROW:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_ARROW)
        PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_ARROW)
        PlotIndexSetInteger(0, PLOT_ARROW, inpUpArrowCode)
        PlotIndexSetInteger(1, PLOT_ARROW, inpDnArrowCode)
        PlotIndexSetString(0, PLOT_LABEL, 'dez: up')
        PlotIndexSetString(1, PLOT_LABEL, 'dez: dn')
        PlotIndexSetInteger(0, PLOT_LINE_COLOR, inpUpColor)
        PlotIndexSetInteger(1, PLOT_LINE_COLOR, inpDnColor)
    elif _sw1 == NONE:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetString(0, PLOT_LABEL, 'dez: up')
        PlotIndexSetString(1, PLOT_LABEL, 'dez: dn')
    else:
        Print('OnInit', ': ОШИБКА! Неизвестный тип отрисовки: ' + EnumToString(inpDrawType, 'ENUM_DW_TYPE'))
        return INIT_FAILED
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, inpUpWidth)
    PlotIndexSetInteger(1, PLOT_LINE_WIDTH, inpDnWidth)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, inpShowData)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, inpShowData)
    answer = InitializeIndicatorHandle(_GlobRef(globals(), 'globHandle'))
    if not answer:
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_dHigh, _s_OnCalculate_dLow, _s_OnCalculate_dNum
    if rates_total <= 0:
        return 0
    answer = False
    firstBar = rates_total - 2
    firstInd = 0
    sizes = Arr(0, 0.0)
    if prev_calculated != 0:
        if rates_total > prev_calculated:
            n = rates_total - 1
            bufW[n] = EMPTY_VALUE
            bufX[n] = EMPTY_VALUE
            bufY[n] = EMPTY_VALUE
            bufZ[n] = EMPTY_VALUE
            answer = GetIndicatorData(globHandle, 0, 1, 1, sizes, 'DailySize')
            if not answer:
                return prev_calculated
        else:
            return prev_calculated
    else:
        ArrayInitialize(bufW, EMPTY_VALUE)
        ArrayInitialize(bufX, EMPTY_VALUE)
        ArrayInitialize(bufY, EMPTY_VALUE)
        ArrayInitialize(bufZ, EMPTY_VALUE)
        firstBar = GetFirstBar(time, rates_total, _GlobRef(globals(), '_s_OnCalculate_dNum'))
        if firstBar == 0:
            return prev_calculated
        firstInd = firstBar
        answer = GetIndicatorData(globHandle, 0, 0, rates_total, sizes, 'DailySize')
        if not answer:
            return prev_calculated
    iNum = 0
    i = firstBar
    j = firstInd
    while i < (rates_total - 1):
        iNum = GetDayNumber(time[i])
        if _s_OnCalculate_dNum != iNum:
            _s_OnCalculate_dNum = iNum
            _s_OnCalculate_dHigh = high[i]
            _s_OnCalculate_dLow = low[i]
        else:
            if high[i] > _s_OnCalculate_dHigh:
                _s_OnCalculate_dHigh = high[i]
            if low[i] < _s_OnCalculate_dLow:
                _s_OnCalculate_dLow = low[i]
        _sw2 = inpDrawType
        if _sw2 in (FILLING, HISTOGRAM2):
            bufW[i] = _s_OnCalculate_dHigh
            bufX[i] = bufW[i] - (((sizes[j] * inpUpZonePct) / 100) * Point())
            bufY[i] = _s_OnCalculate_dLow
            bufZ[i] = bufY[i] + (((sizes[j] * inpDnZonePct) / 100) * Point())
        elif _sw2 in (LINE, ARROW, NONE):
            if inpDrawInternalZone:
                bufW[i] = _s_OnCalculate_dHigh - (((sizes[j] * inpUpZonePct) / 100) * Point())
                bufX[i] = _s_OnCalculate_dLow + (((sizes[j] * inpDnZonePct) / 100) * Point())
            else:
                bufW[i] = _s_OnCalculate_dHigh
                bufX[i] = _s_OnCalculate_dLow
        else:
            Print('OnCalculate', ': ОШИБКА! Неизвестный тип отрисовки: ' + EnumToString(inpDrawType, 'ENUM_DW_TYPE'))
            return rates_total
        i += 1
        j += 1
    return rates_total

def GetIndicatorData(handle, bufferNum, startPos, count, array, strIndName=''):
    num = CopyBuffer(handle, bufferNum, startPos, count, array)
    if num == -1:
        Print('GetIndicatorData', ': ОШИБКА #', GetLastError(), '. Данные индикатора ' + strIndName + ' не получены. Скопировано элементов: ', num)
        return False
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

def InitializeIndicatorHandle(handle):
    handle.v = iCustom(Symbol(), Period(), 'DailySize')
    if handle.v == INVALID_HANDLE:
        Print('InitializeIndicatorHandle', ': ОШИБКА #', GetLastError(), '. Хэндл индикатора DailySize не получен!')
        return False
    else:
        return True

# ---- static local variables
_s_OnCalculate_dNum = 0
_s_OnCalculate_dHigh = 0.0
_s_OnCalculate_dLow = DBL_MAX


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dayextremumzones(_MQL5Indicator):
    name = 'dayextremumzones'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpUpZonePct': 15,  # Размер зоны максимумов, % от дневного движения [0..50]
        'inpDnZonePct': 15,  # Размер зоны минимумов, % от дневного движения [0..50]
        'inpDrawType': _Choice({0: 'Заливка', 1: 'Гистограмма', 2: 'Линии', 3: 'Стрелки', 4: 'Не отрисовывается'}, default=3),  # Тип отрисовки
        'inpDrawInternalZone': True,  # Отображать внутреннюю зону (для типов "Линия"/"Стрелки"/"Не отрисовывается")
        'inpShowData': False,  # Отображать значения индикатора в окне данных
        'inpUpWidth': 1,  # Толщина отрисовки зоны максимумов
        'inpDnWidth': 1,  # Толщина отрисовки зоны минимумов
        'inpUpStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),  # Стиль линии/зоны максимумов
        'inpDnStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),  # Стиль линии/зоны минимумов
        'inpUpArrowCode': 158,  # Код стрелок зоны максимумов (для типа "Стрелки")
        'inpDnArrowCode': 158,  # Код стрелок зоны минимумов (для типа "Стрелки")
    }

