"""squize_ma_htf — converted from MQL5: MQL5 Indicators/Squize_MA_HTF/squize_ma_htf.mq5

Squize_MA с возможностью изменения таймфрейма во входных параметрах
Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [1993170], 2: [8421376], 3: [255], 4: [14822282]}, 'widths': {1: 2, 2: 5, 3: 5, 4: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Squize_MA1', 2: '+Squize_MA Env', 3: '-Squize_MA Env', 4: 'Squize_MA2'}, 'levels': [], 'description': ['Squize_MA с возможностью изменения таймфрейма во входных параметрах'], 'name': 'squize_ma_htf', 'source': 'MQL5 Indicators/Squize_MA_HTF/squize_ma_htf.mq5', 'folder': 'Squize_MA_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора (таймфрейм)', 'sinput': False}, {'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 1, 'label': 'Метод первого усреднения', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'uint', 'default': 5, 'label': 'Глубина  первого сглаживания', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'Параметр первого среднения', 'sinput': False}, {'mql': 'IPC1', 'py': 'IPC1', 'param': 'IPC1', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 1, 'label': 'Метод второго усреднения', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'uint', 'default': 21, 'label': 'Глубина  второго усреднения', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 100, 'label': 'Параметр второго сглаживания', 'sinput': False}, {'mql': 'IPC2', 'py': 'IPC2', 'param': 'IPC2', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'MAsThreSHoldPips', 'py': 'MAsThreSHoldPips', 'param': 'MAsThreSHoldPips', 'type': 'uint', 'default': 15, 'label': '', 'sinput': False}, {'mql': 'ATRmode', 'py': 'ATRmode', 'param': 'ATRmode', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'ATRperiod', 'py': 'ATRperiod', 'param': 'ATRperiod', 'type': 'uint', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'ATRmultipl', 'py': 'ATRmultipl', 'param': 'ATRmultipl', 'type': 'double', 'default': 0.4, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

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
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора (таймфрейм)
MA_Method1 = _input('MA_Method1', MODE_EMA)  # Метод первого усреднения
Length1 = _input('Length1', 5)  # Глубина  первого сглаживания
Phase1 = _input('Phase1', 15)  # Параметр первого среднения
IPC1 = _input('IPC1', PRICE_CLOSE)  # Ценовая константа
MA_Method2 = _input('MA_Method2', MODE_EMA)  # Метод второго усреднения
Length2 = _input('Length2', 21)  # Глубина  второго усреднения
Phase2 = _input('Phase2', 100)  # Параметр второго сглаживания
IPC2 = _input('IPC2', PRICE_CLOSE)  # Ценовая константа
MAsThreSHoldPips = _input('MAsThreSHoldPips', 15)
ATRmode = _input('ATRmode', True)
ATRperiod = _input('ATRperiod', 50)
ATRmultipl = _input('ATRmultipl', 0.4)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer1 = Arr(0, 0.0)
IndBuffer2 = Arr(0, 0.0)
IndBuffer3 = Arr(0, 0.0)
IndBuffer4 = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('Squize_MA', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'Squize_MA', MA_Method1, Length1, Phase1, IPC1, MA_Method2, Length2, Phase2, IPC2, MAsThreSHoldPips, ATRmode, ATRperiod, ATRmultipl, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Squize_MA')
        return INIT_FAILED
    IndInit(0, IndBuffer1, INDICATOR_DATA)
    IndInit(1, IndBuffer2, INDICATOR_DATA)
    IndInit(2, IndBuffer3, INDICATOR_DATA)
    IndInit(3, IndBuffer4, INDICATOR_DATA)
    PlotInit(0, EMPTY_VALUE, 0, Shift)
    PlotInit(1, EMPTY_VALUE, 0, Shift)
    PlotInit(2, EMPTY_VALUE, 0, Shift)
    PlotInit(3, EMPTY_VALUE, 0, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'Squize_MA', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, IndBuffer1, 3, IndBuffer4, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(1, "", TimeFrame, Ind_Handle, 1, IndBuffer2, 2, IndBuffer3, time, rates_total, prev_calculated, min_rates_total):
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
_s_CountIndicator_LastCountBar = Arr(2, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SquizeMaHtf(_MQL5Indicator):
    name = 'squize_ma_htf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора (таймфрейм)
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Метод первого усреднения
        'Length1': 5,  # Глубина  первого сглаживания
        'Phase1': 15,  # Параметр первого среднения
        'IPC1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Ценовая константа
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Метод второго усреднения
        'Length2': 21,  # Глубина  второго усреднения
        'Phase2': 100,  # Параметр второго сглаживания
        'IPC2': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Ценовая константа
        'MAsThreSHoldPips': 15,
        'ATRmode': True,
        'ATRperiod': 50,
        'ATRmultipl': 0.4,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

