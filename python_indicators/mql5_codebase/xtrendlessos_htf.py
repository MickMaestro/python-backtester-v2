"""XTrendlessOS_HTF — converted from MQL5: MQL5 Indicators/XTrendlessOS_HTF/XTrendlessOS_HTF.mq5

XTrendlessOS с возможностью изменения таймфрейма во входных параметрах
Copyright: Copyright © 2016, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16711680, 65280, 8421504, 32768, 8721863, 255, 16711935]}, 'widths': {1: 5}, 'styles': {1: 0}, 'labels': {1: 'XTrendlessOS'}, 'levels': [], 'description': ['XTrendlessOS с возможностью изменения таймфрейма во входных параметрах'], 'name': 'XTrendlessOS_HTF', 'source': 'MQL5 Indicators/XTrendlessOS_HTF/XTrendlessOS_HTF.mq5', 'folder': 'XTrendlessOS_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора (таймфрейм)', 'sinput': False}, {'mql': 'TMA_Method', 'py': 'TMA_Method', 'param': 'TMA_Method', 'type': 'int', 'default': 5, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'TLength', 'py': 'TLength', 'param': 'TLength', 'type': 'int', 'default': 7, 'label': 'глубина  усреднения', 'sinput': False}, {'mql': 'TPhase', 'py': 'TPhase', 'param': 'TPhase', 'type': 'int', 'default': 100, 'label': 'параметр усреднения,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'OBLevel', 'py': 'OBLevel', 'param': 'OBLevel', 'type': 'double', 'default': 0.00473, 'label': 'граница уровня перекупленности', 'sinput': False}, {'mql': 'OSLevel', 'py': 'OSLevel', 'param': 'OSLevel', 'type': 'double', 'default': -0.00473, 'label': 'граница уровня перепроданности', 'sinput': False}, {'mql': 'LevelsColor', 'py': 'LevelsColor', 'param': None, 'type': 'color', 'default': 255, 'label': 'цвет уровней', 'sinput': False}, {'mql': 'LevelsStyle', 'py': 'LevelsStyle', 'param': 'LevelsStyle', 'type': 'int', 'default': 4, 'label': 'стиль уровней', 'sinput': False}, {'mql': 'LevelsWidth', 'py': 'LevelsWidth', 'param': 'LevelsWidth', 'type': 'int', 'default': 1, 'label': 'толщина дневной линии', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

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

# enum ENUM_WIDTH
w_1 = 1
w_2 = 2
w_3 = 3
w_4 = 4
w_5 = 5
_enum('ENUM_WIDTH', {1: 'w_1', 2: 'w_2', 3: 'w_3', 4: 'w_4', 5: 'w_5'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора (таймфрейм)
TMA_Method = _input('TMA_Method', MODE_JurX)  # метод усреднения
TLength = _input('TLength', 7)  # глубина  усреднения
TPhase = _input('TPhase', 100)  # параметр усреднения,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
OBLevel = _input('OBLevel', 0.00473)  # граница уровня перекупленности
OSLevel = _input('OSLevel', -0.00473)  # граница уровня перепроданности
LevelsColor = _input('LevelsColor', clrRed)  # цвет уровней
LevelsStyle = _input('LevelsStyle', STYLE_DASHDOTDOT)  # стиль уровней
LevelsWidth = _input('LevelsWidth', w_1)  # толщина дневной линии
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('XTrendlessOS', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'XTrendlessOS', TMA_Method, TLength, TPhase, IPC, OBLevel, OSLevel, LevelsColor, LevelsStyle, LevelsWidth, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора XTrendlessOS')
        return INIT_FAILED
    IndInit(0, IndBuffer, INDICATOR_DATA)
    IndInit(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotInit(0, EMPTY_VALUE, 0, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'XTrendlessOS', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    OBLevel06 = 0.0
    OBLevel08 = 0.0
    OSLevel06 = 0.0
    OSLevel08 = 0.0
    OBLevel06 = 0.6 * OBLevel
    OBLevel08 = 0.8 * OBLevel
    OSLevel06 = 0.6 * OSLevel
    OSLevel08 = 0.8 * OSLevel
    IndicatorSetInteger(INDICATOR_LEVELS, 6)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, LevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, LevelsStyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 0, LevelsWidth)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, LevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, LevelsStyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 1, LevelsWidth)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, LevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, LevelsStyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 2, LevelsWidth)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 3, LevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 3, LevelsStyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 3, LevelsWidth)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 4, LevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 4, LevelsStyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 4, LevelsWidth)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 5, LevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 5, LevelsStyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 5, LevelsWidth)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, OBLevel06)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, OBLevel08)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, OSLevel06)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, OSLevel08)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 4, OSLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 5, OBLevel)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, IndBuffer, 1, ColorIndBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def CountIndicator(Numb, Symb, TFrame, IndHandle, UpBuffNumb, UpIndBuf, DnBuffNumb, DnIndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        if CopyTime(Symbol(), TFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            UpArr = Arr(1, 0.0, dyn=False)
            DnArr = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, UpBuffNumb, _DT(iTime_[bar]), 1, UpArr) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, DnBuffNumb, _DT(iTime_[bar]), 1, DnArr) <= 0:
                return (0 != 0)
            UpIndBuf[bar] = UpArr[0]
            DnIndBuf[bar] = DnArr[0]
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

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(1, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XTrendlessOSHTF(_MQL5Indicator):
    name = 'XTrendlessOS_HTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора (таймфрейм)
        'TMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=5),  # метод усреднения
        'TLength': 7,  # глубина  усреднения
        'TPhase': 100,  # параметр усреднения,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'OBLevel': 0.00473,  # граница уровня перекупленности
        'OSLevel': -0.00473,  # граница уровня перепроданности
        'LevelsStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=4),  # стиль уровней
        'LevelsWidth': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # толщина дневной линии
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

