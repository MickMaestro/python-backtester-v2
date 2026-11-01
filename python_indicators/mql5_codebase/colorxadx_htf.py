"""colorxadx_htf — converted from MQL5: MQL5 Indicators/ColorXADX_HTF/colorxadx_htf.mq5

ColorXADX с фиксированным во входных параметрах таймфреймом
Copyright: Copyright © 2016, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 12}, 'colors': {1: [65280, 255], 2: [8421504], 3: [8421504, 16711680, 16711935, 255]}, 'widths': {2: 1, 3: 3}, 'styles': {2: 0, 3: 0}, 'labels': {1: 'XDi', 2: 'XADX Line', 3: 'XADX'}, 'levels': [], 'description': ['ColorXADX с фиксированным во входных параметрах таймфреймом'], 'name': 'colorxadx_htf', 'source': 'MQL5 Indicators/ColorXADX_HTF/colorxadx_htf.mq5', 'folder': 'ColorXADX_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 7, 'label': 'Метод усреднения гистограммы', 'sinput': False}, {'mql': 'ADX_Period', 'py': 'ADX_Period', 'param': 'ADX_Period', 'type': 'uint', 'default': 14, 'label': 'Период XMA усреднения', 'sinput': False}, {'mql': 'ADX_Phase', 'py': 'ADX_Phase', 'param': 'ADX_Phase', 'type': 'int', 'default': 100, 'label': 'Параметр XMA усреднения', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'ExtraHighLevel', 'py': 'ExtraHighLevel', 'param': 'ExtraHighLevel', 'type': 'uint', 'default': 60, 'label': 'Уровень максимального тренда', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'uint', 'default': 40, 'label': 'Уровень сильного тренда', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'uint', 'default': 20, 'label': 'Уровень слабого тренда', 'sinput': False}, {'mql': 'LevelStyle', 'py': 'LevelStyle', 'param': 'LevelStyle', 'type': 'int', 'default': 4, 'label': 'Стиль линий уровней', 'sinput': False}, {'mql': 'LevelColor', 'py': 'LevelColor', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Цвет уровней', 'sinput': False}, {'mql': 'LevelWidth', 'py': 'LevelWidth', 'param': 'LevelWidth', 'type': 'int', 'default': 0, 'label': 'Толщина уровней', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
w_1 = 0
w_2 = 1
w_3 = 2
w_4 = 3
w_5 = 4
_enum('ENUM_WIDTH', {0: 'w_1', 1: 'w_2', 2: 'w_3', 3: 'w_4', 4: 'w_5'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора
XMA_Method = _input('XMA_Method', MODE_T3)  # Метод усреднения гистограммы
ADX_Period = _input('ADX_Period', 14)  # Период XMA усреднения
ADX_Phase = _input('ADX_Phase', 100)  # Параметр XMA усреднения
IPC = _input('IPC', PRICE_CLOSE_)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtraHighLevel = _input('ExtraHighLevel', 60)  # Уровень максимального тренда
HighLevel = _input('HighLevel', 40)  # Уровень сильного тренда
LowLevel = _input('LowLevel', 20)  # Уровень слабого тренда
LevelStyle = _input('LevelStyle', STYLE_DASHDOTDOT)  # Стиль линий уровней
LevelColor = _input('LevelColor', clrBlue)  # Цвет уровней
LevelWidth = _input('LevelWidth', w_1)  # Толщина уровней
Ind1Buffer = Arr(0, 0.0)
Ind2Buffer = Arr(0, 0.0)
Ind3Buffer = Arr(0, 0.0)
Ind4Buffer = Arr(0, 0.0)
Ind5Buffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('ColorXADX_HTF', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'ColorXADX', XMA_Method, ADX_Period, ADX_Phase, IPC, 0, ExtraHighLevel, HighLevel, LowLevel, LevelStyle, LevelColor, LevelWidth)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ColorXADX')
        return INIT_FAILED
    SetIndexBuffer(0, Ind1Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, Ind2Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, Ind3Buffer, INDICATOR_DATA)
    SetIndexBuffer(3, Ind4Buffer, INDICATOR_DATA)
    SetIndexBuffer(4, Ind5Buffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(Ind1Buffer, True)
    ArraySetAsSeries(Ind2Buffer, True)
    ArraySetAsSeries(Ind3Buffer, True)
    ArraySetAsSeries(Ind4Buffer, True)
    ArraySetAsSeries(Ind5Buffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'ColorXADX_HTF', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0.0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, ExtraHighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, LevelColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, LevelStyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 0, LevelWidth)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, LevelColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, LevelStyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 1, LevelWidth)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, LevelColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, LevelStyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 2, LevelWidth)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, Ind1Buffer, 1, Ind2Buffer, 2, Ind3Buffer, 3, Ind4Buffer, 4, Ind5Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb1, IndBuf1, BuffNumb2, IndBuf2, BuffNumb3, IndBuf3, BuffNumb4, IndBuf4, BuffNumb5, IndBuf5, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
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
            Arr_ = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb1, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf1[bar] = Arr_[0]
            if CopyBuffer(IndHandle, BuffNumb2, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf2[bar] = Arr_[0]
            if CopyBuffer(IndHandle, BuffNumb3, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf3[bar] = Arr_[0]
            if CopyBuffer(IndHandle, BuffNumb4, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf4[bar] = Arr_[0]
            if CopyBuffer(IndHandle, BuffNumb5, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf5[bar] = Arr_[0]
        else:
            IndBuf1[bar] = IndBuf1[bar + 1]
            IndBuf2[bar] = IndBuf2[bar + 1]
            IndBuf3[bar] = IndBuf3[bar + 1]
            IndBuf4[bar] = IndBuf4[bar + 1]
            IndBuf5[bar] = IndBuf5[bar + 1]
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


class ColorxadxHtf(_MQL5Indicator):
    name = 'colorxadx_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # Метод усреднения гистограммы
        'ADX_Period': 14,  # Период XMA усреднения
        'ADX_Phase': 100,  # Параметр XMA усреднения
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'ExtraHighLevel': 60,  # Уровень максимального тренда
        'HighLevel': 40,  # Уровень сильного тренда
        'LowLevel': 20,  # Уровень слабого тренда
        'LevelStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=4),  # Стиль линий уровней
        'LevelWidth': _Choice({0: '1', 1: '2', 2: '3', 3: '4', 4: '5'}, default=0),  # Толщина уровней
    }

