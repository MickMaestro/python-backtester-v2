"""UltraMFI_HTF — converted from MQL5: MQL5 Indicators/UltraMFI_HTF/UltraMFI_HTF.mq5

Индикатор UltraMFI с возможностью изменения таймфрейма во входных параметрах
Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 7}, 'colors': {1: [65280, 36095]}, 'widths': {}, 'styles': {}, 'labels': {1: 'INDICATOR_NAME " HTF"'}, 'levels': [], 'description': ['Индикатор UltraMFI с возможностью изменения таймфрейма во входных параметрах'], 'name': 'UltraMFI_HTF', 'source': 'MQL5 Indicators/UltraMFI_HTF/UltraMFI_HTF.mq5', 'folder': 'UltraMFI_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора', 'sinput': False}, {'mql': 'MFI_Period', 'py': 'MFI_Period', 'param': 'MFI_Period', 'type': 'int', 'default': 13, 'label': 'период индикатора MFI', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'объём индикатора MFI', 'sinput': False}, {'mql': 'W_Method', 'py': 'W_Method', 'param': 'W_Method', 'type': 'int', 'default': 4, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'StartLength', 'py': 'StartLength', 'param': 'StartLength', 'type': 'int', 'default': 3, 'label': 'стартовый период усреднения', 'sinput': False}, {'mql': 'WPhase', 'py': 'WPhase', 'param': 'WPhase', 'type': 'int', 'default': 100, 'label': 'параметр усреднения,', 'sinput': False}, {'mql': 'Step', 'py': 'Step', 'param': 'Step', 'type': 'uint', 'default': 5, 'label': 'шаг изменения периода', 'sinput': False}, {'mql': 'StepsTotal', 'py': 'StepsTotal', 'param': 'StepsTotal', 'type': 'uint', 'default': 10, 'label': 'количество изменений периода', 'sinput': False}, {'mql': 'SmoothMethod', 'py': 'SmoothMethod', 'param': 'SmoothMethod', 'type': 'int', 'default': 4, 'label': 'метод сглаживания', 'sinput': False}, {'mql': 'SmoothLength', 'py': 'SmoothLength', 'param': 'SmoothLength', 'type': 'int', 'default': 3, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'SmoothPhase', 'py': 'SmoothPhase', 'param': 'SmoothPhase', 'type': 'int', 'default': 100, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'UpLevel', 'py': 'UpLevel', 'param': 'UpLevel', 'type': 'uint', 'default': 80, 'label': 'уровень перезакупа в %%', 'sinput': False}, {'mql': 'DnLevel', 'py': 'DnLevel', 'param': 'DnLevel', 'type': 'uint', 'default': 20, 'label': 'уровень перепродажи в %%', 'sinput': False}, {'mql': 'UpLevelsColor', 'py': 'UpLevelsColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'цвет уровня перезакупа', 'sinput': False}, {'mql': 'DnLevelsColor', 'py': 'DnLevelsColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'цвет уровня перепродажи', 'sinput': False}, {'mql': 'Levelstyle', 'py': 'Levelstyle', 'param': 'Levelstyle', 'type': 'int', 'default': 1, 'label': 'стиль уровней', 'sinput': False}, {'mql': 'LevelsWidth', 'py': 'LevelsWidth', 'param': 'LevelsWidth', 'type': 'int', 'default': 1, 'label': 'толщина уровней', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Blue = 0xFF0000  # MQL4 colour name

# enum Smooth_Method
MODE_SMA_ = 0
MODE_EMA_ = 1
MODE_SMMA_ = 2
MODE_LWMA_ = 3
MODE_JJMA = 4
MODE_JurX = 5
MODE_ParMA = 6
MODE_T3 = 7
MODE_VIDYA = 8
MODE_AMA = 9
_enum('Smooth_Method', {0: 'MODE_SMA_', 1: 'MODE_EMA_', 2: 'MODE_SMMA_', 3: 'MODE_LWMA_', 4: 'MODE_JJMA', 5: 'MODE_JurX', 6: 'MODE_ParMA', 7: 'MODE_T3', 8: 'MODE_VIDYA', 9: 'MODE_AMA'})

# enum WIDTH
Width_1 = 1
Width_2 = 2
Width_3 = 3
Width_4 = 4
Width_5 = 5
_enum('WIDTH', {1: 'Width_1', 2: 'Width_2', 3: 'Width_3', 4: 'Width_4', 5: 'Width_5'})

# enum STYLE
SOLID_ = 0
DASH_ = 1
DOT_ = 2
DASHDOT_ = 3
DASHDOTDOT_ = 4
_enum('STYLE', {0: 'SOLID_', 1: 'DASH_', 2: 'DOT_', 3: 'DASHDOT_', 4: 'DASHDOTDOT_'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора
MFI_Period = _input('MFI_Period', 13)  # период индикатора MFI
VolumeType = _input('VolumeType', VOLUME_TICK)  # объём индикатора MFI
W_Method = _input('W_Method', MODE_JJMA)  # метод усреднения
StartLength = _input('StartLength', 3)  # стартовый период усреднения
WPhase = _input('WPhase', 100)  # параметр усреднения,
Step = _input('Step', 5)  # шаг изменения периода
StepsTotal = _input('StepsTotal', 10)  # количество изменений периода
SmoothMethod = _input('SmoothMethod', MODE_JJMA)  # метод сглаживания
SmoothLength = _input('SmoothLength', 3)  # глубина сглаживания
SmoothPhase = _input('SmoothPhase', 100)  # параметр сглаживания,
UpLevel = _input('UpLevel', 80)  # уровень перезакупа в %%
DnLevel = _input('DnLevel', 20)  # уровень перепродажи в %%
Levelstyle = _input('Levelstyle', DASH_)  # стиль уровней
LevelsWidth = _input('LevelsWidth', Width_1)  # толщина уровней
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
Ind1Buffer = Arr(0, 0.0)
Ind2Buffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('UltraMFI', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'UltraMFI', MFI_Period, VolumeType, W_Method, StartLength, WPhase, Step, StepsTotal, SmoothMethod, SmoothLength, SmoothPhase, 0, 0, clrRed, clrRed, 0, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора UltraMFI')
        return INIT_FAILED
    IndInit(0, Ind1Buffer)
    IndInit(1, Ind2Buffer)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'UltraMFI', '(', EnumToString(TimeFrame, 'ENUM_TIMEFRAMES'), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, _idiv(StepsTotal * UpLevel, 100))
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, UpLevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, Levelstyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 0, LevelsWidth)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, _idiv(StepsTotal * DnLevel, 100))
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, DnLevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, Levelstyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 1, LevelsWidth)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, Symbol(), TimeFrame, Ind_Handle, 0, Ind1Buffer, 1, Ind2Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Buffer, True)

def CountIndicator(Numb, Symb, TFrame, IndHandle, UpBuffNumb, UpIndBuf, DnBuffNumb, DnIndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        UpIndBuf[bar] = EMPTY_VALUE
        DnIndBuf[bar] = EMPTY_VALUE
        if CopyTime(Symbol(), TFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            Arr_ = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, UpBuffNumb, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            UpIndBuf[bar] = Arr_[0]
            if CopyBuffer(IndHandle, DnBuffNumb, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            DnIndBuf[bar] = Arr_[0]
        else:
            UpIndBuf[bar] = UpIndBuf[bar + 1]
            DnIndBuf[bar] = DnIndBuf[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика!')
        Print('Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- global variables initialised from expressions
UpLevelsColor = _input('UpLevelsColor', _uint(Blue))  # цвет уровня перезакупа
DnLevelsColor = _input('DnLevelsColor', _uint(Blue))  # цвет уровня перепродажи

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(1, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class UltraMFIHTF(_MQL5Indicator):
    name = 'UltraMFI_HTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора
        'MFI_Period': 13,  # период индикатора MFI
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём индикатора MFI
        'W_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения
        'StartLength': 3,  # стартовый период усреднения
        'WPhase': 100,  # параметр усреднения,
        'Step': 5,  # шаг изменения периода
        'StepsTotal': 10,  # количество изменений периода
        'SmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод сглаживания
        'SmoothLength': 3,  # глубина сглаживания
        'SmoothPhase': 100,  # параметр сглаживания,
        'UpLevel': 80,  # уровень перезакупа в %%
        'DnLevel': 20,  # уровень перепродажи в %%
        'Levelstyle': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=1),  # стиль уровней
        'LevelsWidth': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # толщина уровней
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

