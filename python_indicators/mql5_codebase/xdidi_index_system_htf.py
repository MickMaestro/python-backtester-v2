"""XDidi_Index_System_HTF — converted from MQL5: MQL5 Indicators/XDidi_Index_System_HTF/XDidi_Index_System_HTF.mq5

XDidi_Index с возможностью изменения таймфрейма во входных параметрах
Copyright: Copyright © 2016, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 5}, 'types': {1: 7, 2: 5, 3: 5, 4: 5, 5: 5}, 'colors': {1: [16748574, 16711935], 2: [65280], 3: [8388736], 4: [65280], 5: [8388736]}, 'widths': {2: 2, 3: 2, 4: 5, 5: 5}, 'styles': {}, 'labels': {1: 'XDidi_Index_HTF1', 2: 'XDidi_Index2 Up', 3: 'XDidi_Index2 Down', 4: 'Buy XDidi_Index2 signal', 5: 'Sell XDidi_Index2 signal'}, 'levels': [], 'description': ['XDidi_Index с возможностью изменения таймфрейма во входных параметрах'], 'name': 'XDidi_Index_System_HTF', 'source': 'MQL5 Indicators/XDidi_Index_System_HTF/XDidi_Index_System_HTF.mq5', 'folder': 'XDidi_Index_System_HTF', 'inputs': [{'mql': 'in1', 'py': 'in1', 'param': None, 'type': 'string', 'default': '<<<  Входные параметры индикатора 1  >>>', 'label': '', 'sinput': False}, {'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора (таймфрейм)', 'sinput': False}, {'mql': 'Curta_Method1', 'py': 'Curta_Method1', 'param': 'Curta_Method1', 'type': 'int', 'default': 0, 'label': 'Curta метод усреднения', 'sinput': False}, {'mql': 'Curta1', 'py': 'Curta1', 'param': 'Curta1', 'type': 'uint', 'default': 3, 'label': 'Curta глубина сглаживания', 'sinput': False}, {'mql': 'CPhase1', 'py': 'CPhase1', 'param': 'CPhase1', 'type': 'int', 'default': 15, 'label': 'Curta параметр сглаживания,', 'sinput': False}, {'mql': 'Media_Method1', 'py': 'Media_Method1', 'param': 'Media_Method1', 'type': 'int', 'default': 0, 'label': 'Media метод усреднения', 'sinput': False}, {'mql': 'Media1', 'py': 'Media1', 'param': 'Media1', 'type': 'uint', 'default': 8, 'label': 'Media глубина сглаживания', 'sinput': False}, {'mql': 'MPhase1', 'py': 'MPhase1', 'param': 'MPhase1', 'type': 'int', 'default': 15, 'label': 'Media параметр сглаживания,', 'sinput': False}, {'mql': 'Longa_Method1', 'py': 'Longa_Method1', 'param': 'Longa_Method1', 'type': 'int', 'default': 0, 'label': 'Longa метод усреднения', 'sinput': False}, {'mql': 'Longa1', 'py': 'Longa1', 'param': 'Longa1', 'type': 'uint', 'default': 20, 'label': 'Longa глубина сглаживания', 'sinput': False}, {'mql': 'LPhase1', 'py': 'LPhase1', 'param': 'LPhase1', 'type': 'int', 'default': 15, 'label': 'Longa параметр сглаживания,', 'sinput': False}, {'mql': 'IPC1', 'py': 'IPC1', 'param': 'IPC1', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Revers1', 'py': 'Revers1', 'param': 'Revers1', 'type': 'bool', 'default': False, 'label': 'переворот графика относительно оси времени', 'sinput': False}, {'mql': 'Shift1', 'py': 'Shift1', 'param': 'Shift1', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'in2', 'py': 'in2', 'param': None, 'type': 'string', 'default': '<<<  Входные параметры индикатора 2  >>>', 'label': '', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 16385, 'label': 'Период графика индикатора (таймфрейм)', 'sinput': False}, {'mql': 'Curta_Method2', 'py': 'Curta_Method2', 'param': 'Curta_Method2', 'type': 'int', 'default': 0, 'label': 'Curta метод усреднения', 'sinput': False}, {'mql': 'Curta2', 'py': 'Curta2', 'param': 'Curta2', 'type': 'uint', 'default': 3, 'label': 'Curta глубина сглаживания', 'sinput': False}, {'mql': 'CPhase2', 'py': 'CPhase2', 'param': 'CPhase2', 'type': 'int', 'default': 15, 'label': 'Curta параметр сглаживания,', 'sinput': False}, {'mql': 'Media_Method2', 'py': 'Media_Method2', 'param': 'Media_Method2', 'type': 'int', 'default': 0, 'label': 'Media метод усреднения', 'sinput': False}, {'mql': 'Media2', 'py': 'Media2', 'param': 'Media2', 'type': 'uint', 'default': 8, 'label': 'Media глубина сглаживания', 'sinput': False}, {'mql': 'MPhase2', 'py': 'MPhase2', 'param': 'MPhase2', 'type': 'int', 'default': 15, 'label': 'Media параметр сглаживания,', 'sinput': False}, {'mql': 'Longa_Method2', 'py': 'Longa_Method2', 'param': 'Longa_Method2', 'type': 'int', 'default': 0, 'label': 'Longa метод усреднения', 'sinput': False}, {'mql': 'Longa2', 'py': 'Longa2', 'param': 'Longa2', 'type': 'uint', 'default': 20, 'label': 'Longa глубина сглаживания', 'sinput': False}, {'mql': 'LPhase2', 'py': 'LPhase2', 'param': 'LPhase2', 'type': 'int', 'default': 15, 'label': 'Longa параметр сглаживания,', 'sinput': False}, {'mql': 'IPC2', 'py': 'IPC2', 'param': 'IPC2', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Revers2', 'py': 'Revers2', 'param': 'Revers2', 'type': 'bool', 'default': False, 'label': 'переворот графика относительно оси времени', 'sinput': False}, {'mql': 'Shift2', 'py': 'Shift2', 'param': 'Shift2', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# ---- inputs and global variables
in1 = _input('in1', '<<<  Входные параметры индикатора 1  >>>')
TimeFrame1 = _input('TimeFrame1', PERIOD_H4)  # Период графика индикатора (таймфрейм)
Curta_Method1 = _input('Curta_Method1', MODE_SMA_)  # Curta метод усреднения
Curta1 = _input('Curta1', 3)  # Curta глубина сглаживания
CPhase1 = _input('CPhase1', 15)  # Curta параметр сглаживания,
Media_Method1 = _input('Media_Method1', MODE_SMA_)  # Media метод усреднения
Media1 = _input('Media1', 8)  # Media глубина сглаживания
MPhase1 = _input('MPhase1', 15)  # Media параметр сглаживания,
Longa_Method1 = _input('Longa_Method1', MODE_SMA_)  # Longa метод усреднения
Longa1 = _input('Longa1', 20)  # Longa глубина сглаживания
LPhase1 = _input('LPhase1', 15)  # Longa параметр сглаживания,
IPC1 = _input('IPC1', PRICE_CLOSE_)  # ценовая константа
Revers1 = _input('Revers1', False)  # переворот графика относительно оси времени
Shift1 = _input('Shift1', 0)  # Сдвиг индикатора по горизонтали в барах
in2 = _input('in2', '<<<  Входные параметры индикатора 2  >>>')
TimeFrame2 = _input('TimeFrame2', PERIOD_H1)  # Период графика индикатора (таймфрейм)
Curta_Method2 = _input('Curta_Method2', MODE_SMA_)  # Curta метод усреднения
Curta2 = _input('Curta2', 3)  # Curta глубина сглаживания
CPhase2 = _input('CPhase2', 15)  # Curta параметр сглаживания,
Media_Method2 = _input('Media_Method2', MODE_SMA_)  # Media метод усреднения
Media2 = _input('Media2', 8)  # Media глубина сглаживания
MPhase2 = _input('MPhase2', 15)  # Media параметр сглаживания,
Longa_Method2 = _input('Longa_Method2', MODE_SMA_)  # Longa метод усреднения
Longa2 = _input('Longa2', 20)  # Longa глубина сглаживания
LPhase2 = _input('LPhase2', 15)  # Longa параметр сглаживания,
IPC2 = _input('IPC2', PRICE_CLOSE_)  # ценовая константа
Revers2 = _input('Revers2', False)  # переворот графика относительно оси времени
Shift2 = _input('Shift2', 0)  # Сдвиг индикатора по горизонтали в барах
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
TrendUp = Arr(0, 0.0)
TrendDown = Arr(0, 0.0)
SignUp = Arr(0, 0.0)
SignDown = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle1 = 0
Ind_Handle2 = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle1, Ind_Handle2, min_rates_total
    if not TimeFramesCheck('XDidi_Index_System', TimeFrame1):
        return INIT_FAILED
    if not TimeFramesCheck('XDidi_Index_System', TimeFrame2):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle1 = iCustom(Symbol(), TimeFrame1, 'XDidi_Index', Curta_Method1, Curta1, CPhase1, Media_Method1, Media1, MPhase1, Longa_Method1, Longa1, LPhase1, IPC1, Revers1)
    if Ind_Handle1 == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора XDidi_Index 1')
        return INIT_FAILED
    Ind_Handle2 = iCustom(Symbol(), TimeFrame2, 'XDidi_Index', Curta_Method2, Curta2, CPhase2, Media_Method2, Media2, MPhase2, Longa_Method2, Longa2, LPhase2, IPC2, Revers2)
    if Ind_Handle2 == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора XDidi_Index 2')
        return INIT_FAILED
    IndInit(0, UpIndBuffer, INDICATOR_DATA)
    IndInit(1, DnIndBuffer, INDICATOR_DATA)
    IndInit(2, TrendUp, INDICATOR_DATA)
    IndInit(3, TrendDown, INDICATOR_DATA)
    IndInit(4, SignUp, INDICATOR_DATA)
    IndInit(5, SignDown, INDICATOR_DATA)
    PlotInit(0, EMPTY_VALUE, 0, Shift1)
    PlotInit(1, EMPTY_VALUE, 0, Shift2)
    PlotInit(2, EMPTY_VALUE, 0, Shift2)
    PlotInit(3, EMPTY_VALUE, 0, Shift2)
    PlotInit(4, EMPTY_VALUE, 0, Shift2)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    PlotIndexSetInteger(3, PLOT_ARROW, 124)
    PlotIndexSetInteger(4, PLOT_ARROW, 124)
    shortname = Box("")
    StringConcatenate(shortname, 'XDidi_Index_System', '(', GetStringTimeframe(TimeFrame1), ',', GetStringTimeframe(TimeFrame2), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 4)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle1) < Bars(Symbol(), TimeFrame1):
        return prev_calculated
    if BarsCalculated(Ind_Handle2) < Bars(Symbol(), TimeFrame2):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator1(0, "", TimeFrame1, Ind_Handle1, 0, UpIndBuffer, 1, DnIndBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator2("", TimeFrame2, Ind_Handle2, TrendUp, TrendDown, SignUp, SignDown, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    PlotIndexSetInteger(Number, PLOT_SHOW_DATA, False)

def CountIndicator1(Numb, Symb, TFrame, IndHandle, UpBuffNumb, UpIndBuf, DnBuffNumb, DnIndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator1_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator1_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        if CopyTime(Symbol(), TFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountIndicator1_LastCountBar[Numb] = bar
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

def CountIndicator2(Symb, TFrame, IndHandle, UpIndBuf, DnIndBuf, BuyIndBuf, SellIndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    global _s_CountIndicator2_LastCountBar
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator2_LastCountBar = limit
    else:
        limit = _s_CountIndicator2_LastCountBar + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        if CopyTime(Symbol(), TFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountIndicator2_LastCountBar = bar
            UpArr = Arr(2, 0.0, dyn=False)
            DnArr = Arr(2, 0.0, dyn=False)
            if CopyBuffer(IndHandle, 0, _DT(iTime_[bar]), 2, UpArr) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, 1, _DT(iTime_[bar]), 2, DnArr) <= 0:
                return (0 != 0)
            DnIndBuf[bar] = EMPTY_VALUE
            UpIndBuf[bar] = DnIndBuf[bar]
            SellIndBuf[bar] = EMPTY_VALUE
            BuyIndBuf[bar] = SellIndBuf[bar]
            if UpArr[1] >= DnArr[1]:
                UpIndBuf[bar] = 1.0
                if UpArr[0] < DnArr[0]:
                    BuyIndBuf[bar] = 1.0
            else:
                DnIndBuf[bar] = 1.0
                if UpArr[0] >= DnArr[0]:
                    SellIndBuf[bar] = 1.0
        else:
            DnIndBuf[bar] = EMPTY_VALUE
            UpIndBuf[bar] = DnIndBuf[bar]
            SellIndBuf[bar] = EMPTY_VALUE
            BuyIndBuf[bar] = SellIndBuf[bar]
    return True

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика!')
        Print('Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountIndicator1_LastCountBar = Arr(1, 0, dyn=False)
_s_CountIndicator2_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XDidiIndexSystemHTF(_MQL5Indicator):
    name = 'XDidi_Index_System_HTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора (таймфрейм)
        'Curta_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Curta метод усреднения
        'Curta1': 3,  # Curta глубина сглаживания
        'CPhase1': 15,  # Curta параметр сглаживания,
        'Media_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Media метод усреднения
        'Media1': 8,  # Media глубина сглаживания
        'MPhase1': 15,  # Media параметр сглаживания,
        'Longa_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Longa метод усреднения
        'Longa1': 20,  # Longa глубина сглаживания
        'LPhase1': 15,  # Longa параметр сглаживания,
        'IPC1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Revers1': False,  # переворот графика относительно оси времени
        'Shift1': 0,  # Сдвиг индикатора по горизонтали в барах
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # Период графика индикатора (таймфрейм)
        'Curta_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Curta метод усреднения
        'Curta2': 3,  # Curta глубина сглаживания
        'CPhase2': 15,  # Curta параметр сглаживания,
        'Media_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Media метод усреднения
        'Media2': 8,  # Media глубина сглаживания
        'MPhase2': 15,  # Media параметр сглаживания,
        'Longa_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Longa метод усреднения
        'Longa2': 20,  # Longa глубина сглаживания
        'LPhase2': 15,  # Longa параметр сглаживания,
        'IPC2': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Revers2': False,  # переворот графика относительно оси времени
        'Shift2': 0,  # Сдвиг индикатора по горизонтали в барах
    }

