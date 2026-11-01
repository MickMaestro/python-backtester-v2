"""AdaptiveRVICloud_System_HTF — converted from MQL5: MQL5 Indicators/AdaptiveRVICloud_System_HTF/AdaptiveRVICloud_System_HTF.mq5

AdaptiveRVICloud с возможностью изменения таймфрейма во входных параметрах
Copyright: Copyright © 2017, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 5}, 'types': {1: 7, 2: 5, 3: 5, 4: 5, 5: 5}, 'colors': {1: [13959039, 13353215], 2: [8421376], 3: [16711935], 4: [8421376], 5: [16711935]}, 'widths': {2: 2, 3: 2, 4: 5, 5: 5}, 'styles': {}, 'labels': {1: 'AdaptiveRVICloud_HTF1', 2: 'AdaptiveRVICloud2 Up', 3: 'AdaptiveRVICloud2 Down', 4: 'Buy AdaptiveRVICloud2 signal', 5: 'Sell AdaptiveRVICloud2 signal'}, 'levels': [], 'description': ['AdaptiveRVICloud с возможностью изменения таймфрейма во входных параметрах'], 'name': 'AdaptiveRVICloud_System_HTF', 'source': 'MQL5 Indicators/AdaptiveRVICloud_System_HTF/AdaptiveRVICloud_System_HTF.mq5', 'folder': 'AdaptiveRVICloud_System_HTF', 'inputs': [{'mql': 'in1', 'py': 'in1', 'param': None, 'type': 'string', 'default': '<<<  Входные параметры индикатора 1  >>>', 'label': '', 'sinput': False}, {'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора (таймфрейм)', 'sinput': False}, {'mql': 'Alpha1', 'py': 'Alpha1', 'param': 'Alpha1', 'type': 'double', 'default': 0.07, 'label': 'Коэффициент усреднения индикатора', 'sinput': False}, {'mql': 'Shift1', 'py': 'Shift1', 'param': 'Shift1', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'in2', 'py': 'in2', 'param': None, 'type': 'string', 'default': '<<<  Входные параметры индикатора 2  >>>', 'label': '', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 16385, 'label': 'Период графика индикатора (таймфрейм)', 'sinput': False}, {'mql': 'Alpha2', 'py': 'Alpha2', 'param': 'Alpha2', 'type': 'double', 'default': 0.07, 'label': 'Коэффициент усреднения индикатора', 'sinput': False}, {'mql': 'Shift2', 'py': 'Shift2', 'param': 'Shift2', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
in1 = _input('in1', '<<<  Входные параметры индикатора 1  >>>')
TimeFrame1 = _input('TimeFrame1', PERIOD_H4)  # Период графика индикатора (таймфрейм)
Alpha1 = _input('Alpha1', 0.07)  # Коэффициент усреднения индикатора
Shift1 = _input('Shift1', 0)  # Сдвиг индикатора по горизонтали в барах
in2 = _input('in2', '<<<  Входные параметры индикатора 2  >>>')
TimeFrame2 = _input('TimeFrame2', PERIOD_H1)  # Период графика индикатора (таймфрейм)
Alpha2 = _input('Alpha2', 0.07)  # Коэффициент усреднения индикатора
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
    if not TimeFramesCheck('AdaptiveRVICloud_System', TimeFrame1):
        return INIT_FAILED
    if not TimeFramesCheck('AdaptiveRVICloud_System', TimeFrame2):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle1 = iCustom(Symbol(), TimeFrame1, 'AdaptiveRVICloud', Alpha1, 0)
    if Ind_Handle1 == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора AdaptiveRVICloud 1')
        return INIT_FAILED
    Ind_Handle2 = iCustom(Symbol(), TimeFrame2, 'AdaptiveRVICloud', Alpha2, 0)
    if Ind_Handle2 == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора AdaptiveRVICloud 2')
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
    PlotIndexSetInteger(3, PLOT_ARROW, 174)
    PlotIndexSetInteger(4, PLOT_ARROW, 174)
    shortname = Box("")
    StringConcatenate(shortname, 'AdaptiveRVICloud_System', '(', GetStringTimeframe(TimeFrame1), ',', GetStringTimeframe(TimeFrame2), ')')
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
    if not CountIndicator2("", TimeFrame2, Ind_Handle2, TrendUp, TrendDown, SignUp, SignDown, time, rates_total, prev_calculated, min_rates_total, UpIndBuffer, DnIndBuffer):
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

def CountIndicator2(Symb, TFrame, IndHandle, UpIndBuf, DnIndBuf, BuyIndBuf, SellIndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total, UpVal, DnVal):
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
            val = (UpVal[bar] + DnVal[bar]) / 2.0
            if UpArr[1] >= DnArr[1]:
                UpIndBuf[bar] = val
                if UpArr[0] < DnArr[0]:
                    BuyIndBuf[bar] = val
            else:
                DnIndBuf[bar] = val
                if UpArr[0] >= DnArr[0]:
                    SellIndBuf[bar] = val
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


class AdaptiveRVICloudSystemHTF(_MQL5Indicator):
    name = 'AdaptiveRVICloud_System_HTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора (таймфрейм)
        'Alpha1': 0.07,  # Коэффициент усреднения индикатора
        'Shift1': 0,  # Сдвиг индикатора по горизонтали в барах
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # Период графика индикатора (таймфрейм)
        'Alpha2': 0.07,  # Коэффициент усреднения индикатора
        'Shift2': 0,  # Сдвиг индикатора по горизонтали в барах
    }

