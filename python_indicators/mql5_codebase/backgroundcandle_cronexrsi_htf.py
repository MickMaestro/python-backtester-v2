"""backgroundcandle_cronexrsi_htf — converted from MQL5: MQL5 Indicators/BackgroundCandle_CronexRSI_HTF/backgroundcandle_cronexrsi_htf.mq5

Индикатор свечек с окраской от CronexRSI с возможностью изменения таймфрейма во входных параметрах
Copyright: Copyright © 2014, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.61

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.61', 'window': 'chart', 'indicator_buffers': 12, 'indicator_plots': 6}, 'types': {1: 7, 2: 7, 3: 7, 4: 7, 5: 7, 6: 7}, 'colors': {1: [10025880, 15631086], 2: [11829830, 13382297], 3: [10025880, 15631086], 4: [10025880, 15631086], 5: [11829830, 13382297], 6: [10025880, 15631086]}, 'widths': {}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'Upper Shade', 2: 'Body', 3: 'Lower Shade', 4: 'Upper Shade', 5: 'Body', 6: 'Lower Shade'}, 'levels': [], 'description': ['Индикатор свечек с окраской от CronexRSI с возможностью изменения таймфрейма во входных параметрах'], 'name': 'backgroundcandle_cronexrsi_htf', 'source': 'MQL5 Indicators/BackgroundCandle_CronexRSI_HTF/backgroundcandle_cronexrsi_htf.mq5', 'folder': 'BackgroundCandle_CronexRSI_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора', 'sinput': False}, {'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'uint', 'default': 25, 'label': 'Период индикатора RSI', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': 'Цена индикатора RSI', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'FastPeriod', 'py': 'FastPeriod', 'param': 'FastPeriod', 'type': 'uint', 'default': 14, 'label': 'Период быстрого усреднения', 'sinput': False}, {'mql': 'SlowPeriod', 'py': 'SlowPeriod', 'param': 'SlowPeriod', 'type': 'uint', 'default': 25, 'label': 'Метод медленного усреднения', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
RSIPeriod = _input('RSIPeriod', 25)  # Период индикатора RSI
RSIPrice = _input('RSIPrice', PRICE_CLOSE)  # Цена индикатора RSI
XMA_Method = _input('XMA_Method', MODE_SMA)  # Метод усреднения
FastPeriod = _input('FastPeriod', 14)  # Период быстрого усреднения
SlowPeriod = _input('SlowPeriod', 25)  # Метод медленного усреднения
XPhase = _input('XPhase', 15)  # Параметр сглаживания
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

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('BackgroundCandle_CronexRSI', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'CronexRSI', RSIPeriod, RSIPrice, XMA_Method, FastPeriod, SlowPeriod, XPhase)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора CronexRSI')
        return INIT_FAILED
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
    StringConcatenate(shortname, 'BackgroundCandle_CronexRSI', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
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
    global _s_CountIndicator_LastTime, _s_CountIndicator_Sign, _s_CountIndicator_Trend
    iOpen_ = Arr(1, 0.0, dyn=False)
    iLow_ = Arr(1, 0.0, dyn=False)
    iHigh_ = Arr(1, 0.0, dyn=False)
    iClose_ = Arr(1, 0.0, dyn=False)
    iUp = Arr(1, 0.0, dyn=False)
    iDn = Arr(1, 0.0, dyn=False)
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
            if CopyBuffer(IndHandle, 0, _DT(Time[bar]), 1, iUp) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, 1, _DT(Time[bar]), 1, iDn) <= 0:
                return (0 != 0)
            if CopyOpen(Symbol(), TFrame, _DT(Time[bar]), 1, iOpen_) <= 0:
                return (0 != 0)
            if CopyLow(Symbol(), TFrame, _DT(Time[bar]), 1, iLow_) <= 0:
                return (0 != 0)
            if CopyHigh(Symbol(), TFrame, _DT(Time[bar]), 1, iHigh_) <= 0:
                return (0 != 0)
            if CopyClose(Symbol(), TFrame, _DT(Time[bar]), 1, iClose_) <= 0:
                return (0 != 0)
            mathmax = MathMax(iOpen_[0], iClose_[0])
            mathmin = MathMin(iOpen_[0], iClose_[0])
            if _s_CountIndicator_Sign > 0:
                if iUp[0] > iDn[0]:
                    ExtA1Buff[bar] = iHigh_[0]
                    ExtB1Buff[bar] = mathmax
                    ExtA2Buff[bar] = mathmax
                    ExtB2Buff[bar] = mathmin
                    ExtA3Buff[bar] = mathmin
                    ExtB3Buff[bar] = iLow_[0]
                    _s_CountIndicator_Trend = 1
                if iUp[0] < iDn[0]:
                    ExtB1Buff[bar] = iHigh_[0]
                    ExtA1Buff[bar] = mathmax
                    ExtB2Buff[bar] = mathmax
                    ExtA2Buff[bar] = mathmin
                    ExtB3Buff[bar] = mathmin
                    ExtA3Buff[bar] = iLow_[0]
                    _s_CountIndicator_Trend = -1
                if iUp[0] == iDn[0]:
                    if _s_CountIndicator_Trend > 0:
                        ExtA1Buff[bar] = iHigh_[0]
                        ExtB1Buff[bar] = mathmax
                        ExtA2Buff[bar] = mathmax
                        ExtB2Buff[bar] = mathmin
                        ExtA3Buff[bar] = mathmin
                        ExtB3Buff[bar] = iLow_[0]
                    if _s_CountIndicator_Trend < 0:
                        ExtB1Buff[bar] = iHigh_[0]
                        ExtA1Buff[bar] = mathmax
                        ExtB2Buff[bar] = mathmax
                        ExtA2Buff[bar] = mathmin
                        ExtB3Buff[bar] = mathmin
                        ExtA3Buff[bar] = iLow_[0]
                ExtA4Buff[bar] = 0.0
                ExtB4Buff[bar] = 0.0
                ExtA5Buff[bar] = 0.0
                ExtB5Buff[bar] = 0.0
                ExtA6Buff[bar] = 0.0
                ExtB6Buff[bar] = 0.0
            else:
                if iUp[0] > iDn[0]:
                    ExtA4Buff[bar] = iHigh_[0]
                    ExtB4Buff[bar] = mathmax
                    ExtA5Buff[bar] = mathmax
                    ExtB5Buff[bar] = mathmin
                    ExtA6Buff[bar] = mathmin
                    ExtB6Buff[bar] = iLow_[0]
                    _s_CountIndicator_Trend = 1
                if iUp[0] < iDn[0]:
                    ExtB4Buff[bar] = iHigh_[0]
                    ExtA4Buff[bar] = mathmax
                    ExtB5Buff[bar] = mathmax
                    ExtA5Buff[bar] = mathmin
                    ExtB6Buff[bar] = mathmin
                    ExtA6Buff[bar] = iLow_[0]
                    _s_CountIndicator_Trend = -1
                if iUp[0] == iDn[0]:
                    if _s_CountIndicator_Trend > 0:
                        ExtA4Buff[bar] = iHigh_[0]
                        ExtB4Buff[bar] = mathmax
                        ExtA5Buff[bar] = mathmax
                        ExtB5Buff[bar] = mathmin
                        ExtA6Buff[bar] = mathmin
                        ExtB6Buff[bar] = iLow_[0]
                    if _s_CountIndicator_Trend < 0:
                        ExtB4Buff[bar] = iHigh_[0]
                        ExtA4Buff[bar] = mathmax
                        ExtB5Buff[bar] = mathmax
                        ExtA5Buff[bar] = mathmin
                        ExtB6Buff[bar] = mathmin
                        ExtA6Buff[bar] = iLow_[0]
                ExtA1Buff[bar] = 0.0
                ExtB1Buff[bar] = 0.0
                ExtA2Buff[bar] = 0.0
                ExtB2Buff[bar] = 0.0
                ExtA3Buff[bar] = 0.0
                ExtB3Buff[bar] = 0.0
        else:
            bar1 = bar + 1
            ExtA1Buff[bar] = ExtA1Buff[bar1]
            ExtB1Buff[bar] = ExtB1Buff[bar1]
            ExtA2Buff[bar] = ExtA2Buff[bar1]
            ExtB2Buff[bar] = ExtB2Buff[bar1]
            ExtA3Buff[bar] = ExtA3Buff[bar1]
            ExtB3Buff[bar] = ExtB3Buff[bar1]
            ExtA4Buff[bar] = ExtA4Buff[bar1]
            ExtB4Buff[bar] = ExtB4Buff[bar1]
            ExtA5Buff[bar] = ExtA5Buff[bar1]
            ExtB5Buff[bar] = ExtB5Buff[bar1]
            ExtA6Buff[bar] = ExtA6Buff[bar1]
            ExtB6Buff[bar] = ExtB6Buff[bar1]
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
_s_CountIndicator_Trend = 0
_s_CountIndicator_LastTime = 0
_s_CountIndicator_LastCountBar = Arr(1, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BackgroundcandleCronexrsiHtf(_MQL5Indicator):
    name = 'backgroundcandle_cronexrsi_htf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора
        'RSIPeriod': 25,  # Период индикатора RSI
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Цена индикатора RSI
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения
        'FastPeriod': 14,  # Период быстрого усреднения
        'SlowPeriod': 25,  # Метод медленного усреднения
        'XPhase': 15,  # Параметр сглаживания
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

