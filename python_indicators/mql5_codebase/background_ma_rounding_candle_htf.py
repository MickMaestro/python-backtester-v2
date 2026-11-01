"""background_ma_rounding_candle_htf — converted from MQL5: MQL5 Indicators/Background_MA_Rounding_Candle_HTF/background_ma_rounding_candle_htf.mq5

Индикатор MA_Rounding свечек с возможностью изменения таймфрейма во входных параметрах.
Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 12, 'indicator_plots': 6}, 'types': {1: 7, 2: 7, 3: 7, 4: 7, 5: 7, 6: 7}, 'colors': {1: [15453831, 14524637], 2: [16760576, 14053594], 3: [15453831, 14524637], 4: [15453831, 14524637], 5: [16760576, 14053594], 6: [15453831, 14524637]}, 'widths': {}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'Upper Shade', 2: 'Body', 3: 'Lower Shade', 4: 'Upper Shade', 5: 'Body', 6: 'Lower Shade'}, 'levels': [], 'description': ['Индикатор MA_Rounding свечек с возможностью изменения таймфрейма во входных параметрах.'], 'name': 'background_ma_rounding_candle_htf', 'source': 'MQL5 Indicators/Background_MA_Rounding_Candle_HTF/background_ma_rounding_candle_htf.mq5', 'folder': 'Background_MA_Rounding_Candle_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'int', 'default': 12, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'MaRound', 'py': 'MaRound', 'param': 'MaRound', 'type': 'uint', 'default': 50, 'label': 'Коэффициент округления', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора
XMA_Method = _input('XMA_Method', MODE_SMA)  # Метод усреднения
XLength = _input('XLength', 12)  # Глубина сглаживания
XPhase = _input('XPhase', 15)  # Параметр сглаживания
MaRound = _input('MaRound', 50)  # Коэффициент округления
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtA1Buffer = Arr(0, 0.0)
ExtB1Buffer = Arr(0, 0.0)
ExtA2Buffer = Arr(0, 0.0)
ExtB2Buffer = Arr(0, 0.0)
ExtA3Buffer = Arr(0, 0.0)
ExtB3Buffer = Arr(0, 0.0)
ExtA4Buffer = Arr(0, 0.0)
ExtB4Buffer = Arr(0, 0.0)
ExtA5Buffer = Arr(0, 0.0)
ExtB5Buffer = Arr(0, 0.0)
ExtA6Buffer = Arr(0, 0.0)
ExtB6Buffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('Background_MA_Rounding_Candle', TimeFrame):
        return INIT_FAILED
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'MA_Rounding_Candle', XMA_Method, XLength, XPhase, MaRound)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора MA_Rounding_Candle')
        return INIT_FAILED
    min_rates_total = 2
    ArrayInit(0, ExtA1Buffer)
    ArrayInit(1, ExtB1Buffer)
    ArrayInit(2, ExtA2Buffer)
    ArrayInit(3, ExtB2Buffer)
    ArrayInit(4, ExtA3Buffer)
    ArrayInit(5, ExtB3Buffer)
    ArrayInit(6, ExtA4Buffer)
    ArrayInit(7, ExtB4Buffer)
    ArrayInit(8, ExtA5Buffer)
    ArrayInit(9, ExtB5Buffer)
    ArrayInit(10, ExtA6Buffer)
    ArrayInit(11, ExtB6Buffer)
    PlotInit(0, 2, Shift)
    PlotInit(1, 2, Shift)
    PlotInit(2, 2, Shift)
    PlotInit(3, 2, Shift)
    PlotInit(4, 2, Shift)
    PlotInit(5, 2, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'Background_MA_Rounding_Candle', '(', EnumToString(TimeFrame, 'ENUM_TIMEFRAMES'), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, Symbol(), TimeFrame, Ind_Handle, ExtA1Buffer, ExtB1Buffer, ExtA2Buffer, ExtB2Buffer, ExtA3Buffer, ExtB3Buffer, ExtA4Buffer, ExtB4Buffer, ExtA5Buffer, ExtB5Buffer, ExtA6Buffer, ExtB6Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def CountIndicator(Numb, Symb, TFrame, IndHandle, ExtA1Buff, ExtB1Buff, ExtA2Buff, ExtB2Buff, ExtA3Buff, ExtB3Buff, ExtA4Buff, ExtB4Buff, ExtA5Buff, ExtB5Buff, ExtA6Buff, ExtB6Buff, Time, Rates_Total, Prev_Calculated, Min_Rates_Total):
    global _s_CountIndicator_LastTime, _s_CountIndicator_Sign
    iOpen_ = Arr(1, 0.0, dyn=False)
    iLow_ = Arr(1, 0.0, dyn=False)
    iHigh_ = Arr(1, 0.0, dyn=False)
    iClose_ = Arr(1, 0.0, dyn=False)
    iTime_ = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
        _s_CountIndicator_LastTime = 0
        _s_CountIndicator_Sign = 1
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        if CopyTime(Symbol(), TFrame, _DT(Time[bar]), 1, iTime_) <= 0:
            return (0 != 0)
        if Time[bar] >= iTime_[0] and Time[bar + 1] < iTime_[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            if iTime_[0] != _s_CountIndicator_LastTime:
                _s_CountIndicator_LastTime = iTime_[0]
                _s_CountIndicator_Sign *= -1
            if CopyBuffer(IndHandle, 0, _DT(Time[bar]), 1, iOpen_) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, 1, _DT(Time[bar]), 1, iHigh_) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, 2, _DT(Time[bar]), 1, iLow_) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, 3, _DT(Time[bar]), 1, iClose_) <= 0:
                return (0 != 0)
            if _s_CountIndicator_Sign > 0:
                if iClose_[0] >= iOpen_[0]:
                    ExtA1Buff[bar] = iHigh_[0]
                    ExtB1Buff[bar] = iClose_[0]
                    ExtA2Buff[bar] = iClose_[0]
                    ExtB2Buff[bar] = iOpen_[0]
                    ExtA3Buff[bar] = iOpen_[0]
                    ExtB3Buff[bar] = iLow_[0]
                else:
                    ExtB1Buff[bar] = iHigh_[0]
                    ExtA1Buff[bar] = iClose_[0]
                    ExtA2Buff[bar] = iClose_[0]
                    ExtB2Buff[bar] = iOpen_[0]
                    ExtB3Buff[bar] = iOpen_[0]
                    ExtA3Buff[bar] = iLow_[0]
                ExtA4Buff[bar] = 0.0
                ExtB4Buff[bar] = 0.0
                ExtA5Buff[bar] = 0.0
                ExtB5Buff[bar] = 0.0
                ExtA6Buff[bar] = 0.0
                ExtB6Buff[bar] = 0.0
            else:
                if iClose_[0] >= iOpen_[0]:
                    ExtA4Buff[bar] = iHigh_[0]
                    ExtB4Buff[bar] = iClose_[0]
                    ExtA5Buff[bar] = iClose_[0]
                    ExtB5Buff[bar] = iOpen_[0]
                    ExtA6Buff[bar] = iOpen_[0]
                    ExtB6Buff[bar] = iLow_[0]
                else:
                    ExtB4Buff[bar] = iHigh_[0]
                    ExtA4Buff[bar] = iClose_[0]
                    ExtA5Buff[bar] = iClose_[0]
                    ExtB5Buff[bar] = iOpen_[0]
                    ExtB6Buff[bar] = iOpen_[0]
                    ExtA6Buff[bar] = iLow_[0]
                ExtA1Buff[bar] = 0.0
                ExtB1Buff[bar] = 0.0
                ExtA2Buff[bar] = 0.0
                ExtB2Buff[bar] = 0.0
                ExtA3Buff[bar] = 0.0
                ExtB3Buff[bar] = 0.0
        else:
            ExtA1Buff[bar] = ExtA1Buff[bar + 1]
            ExtB1Buff[bar] = ExtB1Buff[bar + 1]
            ExtA2Buff[bar] = ExtA2Buff[bar + 1]
            ExtB2Buff[bar] = ExtB2Buff[bar + 1]
            ExtA3Buff[bar] = ExtA3Buff[bar + 1]
            ExtB3Buff[bar] = ExtB3Buff[bar + 1]
            ExtA4Buff[bar] = ExtA4Buff[bar + 1]
            ExtB4Buff[bar] = ExtB4Buff[bar + 1]
            ExtA5Buff[bar] = ExtA5Buff[bar + 1]
            ExtB5Buff[bar] = ExtB5Buff[bar + 1]
            ExtA6Buff[bar] = ExtA6Buff[bar + 1]
            ExtB6Buff[bar] = ExtB6Buff[bar + 1]
    return True

def PlotInit(PlotNumber, DrawBegin, PlotShift):
    PlotIndexSetInteger(PlotNumber, PLOT_DRAW_BEGIN, DrawBegin)
    PlotIndexSetInteger(PlotNumber, PLOT_SHIFT, PlotShift)

def ArrayInit(ArrNumber, Array):
    SetIndexBuffer(ArrNumber, Array, INDICATOR_DATA)
    ArraySetAsSeries(Array, True)

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика!')
        Print('Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountIndicator_Sign = 0
_s_CountIndicator_LastTime = 0
_s_CountIndicator_LastCountBar = Arr(1, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BackgroundMaRoundingCandleHtf(_MQL5Indicator):
    name = 'background_ma_rounding_candle_htf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения
        'XLength': 12,  # Глубина сглаживания
        'XPhase': 15,  # Параметр сглаживания
        'MaRound': 50,  # Коэффициент округления
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

