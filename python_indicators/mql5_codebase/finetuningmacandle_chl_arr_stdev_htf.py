"""FineTuningMACandle_Chl_Arr_StDev_HTF — converted from MQL5: MQL5 Indicators/FineTuningMACandle_Chl_Arr_StDev_HTF/FineTuningMACandle_Chl_Arr_StDev_HTF.mq5

FineTuningMACandle_Chl_Arr_StDev с фиксированным во входных параметрах таймфреймом
Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.70

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.70', 'window': 'chart', 'indicator_buffers': 10, 'indicator_plots': 7}, 'types': {1: 7, 2: 7, 3: 8, 4: 5, 5: 5, 6: 5, 7: 5}, 'colors': {1: [14942122], 2: [12320767], 3: [9639167, 8421504, 15570276], 4: [255], 5: [10156544], 6: [255], 7: [10156544]}, 'widths': {3: 2, 4: 2, 5: 2, 6: 5, 7: 5}, 'styles': {3: 0}, 'labels': {1: 'Upper Signal Cloud', 2: 'Lower Signal Cloud', 3: 'FineTuningMACandle Signal line', 4: 'Dn_Signal 1', 5: 'Up_Signal 1', 6: 'Dn_Signal 2', 7: 'Up_Signal 2'}, 'levels': [], 'description': ['FineTuningMACandle_Chl_Arr_StDev с фиксированным во входных параметрах таймфреймом'], 'name': 'FineTuningMACandle_Chl_Arr_StDev_HTF', 'source': 'MQL5 Indicators/FineTuningMACandle_Chl_Arr_StDev_HTF/FineTuningMACandle_Chl_Arr_StDev_HTF.mq5', 'folder': 'FineTuningMACandle_Chl_Arr_StDev_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора', 'sinput': False}, {'mql': 'FTMA', 'py': 'FTMA', 'param': 'FTMA', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'rank1', 'py': 'rank1', 'param': 'rank1', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'rank2', 'py': 'rank2', 'param': 'rank2', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'rank3', 'py': 'rank3', 'param': 'rank3', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'Shift1', 'py': 'Shift1', 'param': 'Shift1', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'Shift2', 'py': 'Shift2', 'param': 'Shift2', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'Shift3', 'py': 'Shift3', 'param': 'Shift3', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора по вертикали в пунктах', 'sinput': False}, {'mql': 'Gap', 'py': 'Gap', 'param': 'Gap', 'type': 'uint', 'default': 10, 'label': 'размер неучитываемого гэпа в пунктах', 'sinput': False}, {'mql': 'BBLength', 'py': 'BBLength', 'param': 'BBLength', 'type': 'uint', 'default': 10, 'label': 'период Боллинджера', 'sinput': False}, {'mql': 'BandsDeviation', 'py': 'BandsDeviation', 'param': 'BandsDeviation', 'type': 'double', 'default': 1.0, 'label': 'девиация', 'sinput': False}, {'mql': 'dK1', 'py': 'dK1', 'param': 'dK1', 'type': 'double', 'default': 1.5, 'label': 'коэффициент 1 для квадратичного фильтра', 'sinput': False}, {'mql': 'dK2', 'py': 'dK2', 'param': 'dK2', 'type': 'double', 'default': 2.5, 'label': 'коэффициент 2 для квадратичного фильтра', 'sinput': False}, {'mql': 'std_period', 'py': 'std_period', 'param': 'std_period', 'type': 'uint', 'default': 9, 'label': 'период квадратичного фильтра', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора
FTMA = _input('FTMA', 10)
rank1 = _input('rank1', 2.0)
rank2 = _input('rank2', 2.0)
rank3 = _input('rank3', 2.0)
Shift1 = _input('Shift1', 1.0)
Shift2 = _input('Shift2', 1.0)
Shift3 = _input('Shift3', 1.0)
PriceShift = _input('PriceShift', 0)  # cдвиг индикатора по вертикали в пунктах
Gap = _input('Gap', 10)  # размер неучитываемого гэпа в пунктах
BBLength = _input('BBLength', 10)  # период Боллинджера
BandsDeviation = _input('BandsDeviation', 1.0)  # девиация
dK1 = _input('dK1', 1.5)  # коэффициент 1 для квадратичного фильтра
dK2 = _input('dK2', 2.5)  # коэффициент 2 для квадратичного фильтра
std_period = _input('std_period', 9)  # период квадратичного фильтра
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
UpUpBuffer = Arr(0, 0.0)
UpDnBuffer = Arr(0, 0.0)
DnUpBuffer = Arr(0, 0.0)
DnDnBuffer = Arr(0, 0.0)
ExtBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
BearsBuffer1 = Arr(0, 0.0)
BullsBuffer1 = Arr(0, 0.0)
BearsBuffer2 = Arr(0, 0.0)
BullsBuffer2 = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'FineTuningMACandle_Chl_Arr_StDev', FTMA, rank1, rank2, rank3, Shift1, Shift2, Shift3, PriceShift, Gap, BBLength, BandsDeviation, dK1, dK2, std_period, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора FineTuningMACandle_Chl_Arr_StDev')
        return INIT_FAILED
    IndInit_1(0, UpUpBuffer, INDICATOR_DATA)
    IndInit_1(1, UpDnBuffer, INDICATOR_DATA)
    PlotInit(0, 0.0, min_rates_total, Shift)
    IndInit_1(2, DnUpBuffer, INDICATOR_DATA)
    IndInit_1(3, DnDnBuffer, INDICATOR_DATA)
    PlotInit(1, 0.0, min_rates_total, Shift)
    IndInit_1(4, ExtBuffer, INDICATOR_DATA)
    IndInit_1(5, ExtColorBuffer, INDICATOR_DATA)
    PlotInit(2, 0.0, min_rates_total, Shift)
    IndInit_1(6, BearsBuffer1, INDICATOR_DATA)
    IndInit_1(7, BullsBuffer1, INDICATOR_DATA)
    IndInit_1(8, BearsBuffer2, INDICATOR_DATA)
    IndInit_1(9, BullsBuffer2, INDICATOR_DATA)
    PlotInit(3, 0.0, min_rates_total, Shift)
    PlotInit(4, 0.0, min_rates_total, Shift)
    PlotInit(5, 0.0, min_rates_total, Shift)
    PlotInit(6, 0.0, min_rates_total, Shift)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    PlotIndexSetInteger(4, PLOT_ARROW, 159)
    PlotIndexSetInteger(5, PLOT_ARROW, 159)
    PlotIndexSetInteger(6, PLOT_ARROW, 159)
    shortname = Box("")
    StringConcatenate(shortname, 'FineTuningMACandle_Chl_Arr_StDev', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def IndInit_1(Number, Buffer, BufferType):
    SetIndexBuffer(Number, Buffer, BufferType)
    ArraySetAsSeries(Buffer, True)

def IndInit_2(Number, Buffer, Empty_Value, Draw_Begin, nShift):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if not TimeFramesCheck('FineTuningMACandle_Chl_Arr_StDev', TimeFrame):
        return 0
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, UpUpBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(1, "", TimeFrame, Ind_Handle, 1, UpDnBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(2, "", TimeFrame, Ind_Handle, 2, DnUpBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(3, "", TimeFrame, Ind_Handle, 3, DnDnBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(4, "", TimeFrame, Ind_Handle, 4, ExtBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(5, "", TimeFrame, Ind_Handle, 5, ExtColorBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(6, "", TimeFrame, Ind_Handle, 6, BearsBuffer1, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(7, "", TimeFrame, Ind_Handle, 7, BullsBuffer1, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(8, "", TimeFrame, Ind_Handle, 8, BearsBuffer2, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(9, "", TimeFrame, Ind_Handle, 9, BullsBuffer2, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb, IndBuf, Time, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        if CopyTime(Symbol(), TFrame, _DT(Time[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if Time[bar] >= IndTime[0] and Time[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            Arr_ = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb, _DT(Time[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf[bar] = Arr_[0]
        else:
            IndBuf[bar] = IndBuf[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Comment('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика! \n Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(10, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FineTuningMACandleChlArrStDevHTF(_MQL5Indicator):
    name = 'FineTuningMACandle_Chl_Arr_StDev_HTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора
        'FTMA': 10,
        'rank1': 2.0,
        'rank2': 2.0,
        'rank3': 2.0,
        'Shift1': 1.0,
        'Shift2': 1.0,
        'Shift3': 1.0,
        'PriceShift': 0,  # cдвиг индикатора по вертикали в пунктах
        'Gap': 10,  # размер неучитываемого гэпа в пунктах
        'BBLength': 10,  # период Боллинджера
        'BandsDeviation': 1.0,  # девиация
        'dK1': 1.5,  # коэффициент 1 для квадратичного фильтра
        'dK2': 2.5,  # коэффициент 2 для квадратичного фильтра
        'std_period': 9,  # период квадратичного фильтра
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

