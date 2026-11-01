"""Float_Pivot_Smoothed_Digit_System_HTF — converted from MQL5: MQL5 Indicators/Float_Pivot_Smoothed_Digit_System_HTF/Float_Pivot_Smoothed_Digit_System_HTF.mq5

Float_Pivot_Smoothed_Digit_System с фиксированным во входных параметрах таймфреймом
Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.70

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.70', 'window': 'chart', 'indicator_buffers': 12, 'indicator_plots': 6}, 'types': {1: 7, 2: 1, 3: 1, 4: 1, 5: 7, 6: 17}, 'colors': {1: [15859441], 2: [16748574], 3: [13458026], 4: [9639167], 5: [16641789], 6: [9639167, 8388736, 8421504, 13434880, 16748574]}, 'widths': {2: 2, 3: 2, 4: 2, 6: 2}, 'styles': {2: 0, 3: 0, 4: 0, 6: 0}, 'labels': {1: 'Upper Cloud', 2: 'Upper FloatPivot', 3: 'Middle FloatPivot', 4: 'Lower FloatPivot', 5: 'Lower Cloud', 6: 'Float_Pivot_Smoothed_Digit Open;Float_Pivot_Smoothed_Digit High;Float_Pivot_Smoothed_Digit Low;Float_Pivot_Smoothed_Digit Close'}, 'levels': [], 'description': ['Float_Pivot_Smoothed_Digit_System с фиксированным во входных параметрах таймфреймом'], 'name': 'Float_Pivot_Smoothed_Digit_System_HTF', 'source': 'MQL5 Indicators/Float_Pivot_Smoothed_Digit_System_HTF/Float_Pivot_Smoothed_Digit_System_HTF.mq5', 'folder': 'Float_Pivot_Smoothed_Digit_System_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора', 'sinput': False}, {'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'Float_Pivot_Digit', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'IPeriod', 'py': 'IPeriod', 'param': 'IPeriod', 'type': 'int', 'default': 100, 'label': 'Период поиска экстремумов', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 5, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'HMA_Method', 'py': 'HMA_Method', 'param': 'HMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод сглаживания', 'sinput': False}, {'mql': 'HLength', 'py': 'HLength', 'param': 'HLength', 'type': 'uint', 'default': 12, 'label': 'Глубина  сглаживания', 'sinput': False}, {'mql': 'HPhase', 'py': 'HPhase', 'param': 'HPhase', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'uint', 'default': 3, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Digit', 'py': 'Digit', 'param': 'Digit', 'type': 'uint', 'default': 2, 'label': 'количество разрядов округления', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': 'показывать ценовые метки', 'sinput': False}, {'mql': 'Upper_color', 'py': 'Upper_color', 'param': None, 'type': 'color', 'default': 8421376, 'label': 'Цвет верхней ценовой метки', 'sinput': False}, {'mql': 'Middle_color', 'py': 'Middle_color', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Цвет средней ценовой метки', 'sinput': False}, {'mql': 'Lower_color', 'py': 'Lower_color', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'Цвет нижней ценовой метки', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum ENUM_APPLIED_PRICE_
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
_enum('ENUM_APPLIED_PRICE_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора
SirName = _input('SirName', 'Float_Pivot_Digit')  # Первая часть имени графических объектов
IPeriod = _input('IPeriod', 100)  # Период поиска экстремумов
IPC = _input('IPC', PRICE_MEDIAN_)  # ценовая константа
HMA_Method = _input('HMA_Method', MODE_SMA_)  # Метод сглаживания
HLength = _input('HLength', 12)  # Глубина  сглаживания
HPhase = _input('HPhase', 100)  # Параметр сглаживания,
Shift = _input('Shift', 3)  # сдвиг индикатора по горизонтали в барах
Digit = _input('Digit', 2)  # количество разрядов округления
ShowPrice = _input('ShowPrice', True)  # показывать ценовые метки
Upper_color = _input('Upper_color', clrTeal)  # Цвет верхней ценовой метки
Middle_color = _input('Middle_color', clrBlue)  # Цвет средней ценовой метки
Lower_color = _input('Lower_color', clrMagenta)  # Цвет нижней ценовой метки
ExtUp1Buffer = Arr(0, 0.0)
ExtUp2Buffer = Arr(0, 0.0)
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
ExtCBuffer = Arr(0, 0.0)
ExtDn1Buffer = Arr(0, 0.0)
ExtDn2Buffer = Arr(0, 0.0)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    min_rates_total = 100
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'Float_Pivot_Smoothed_Digit_System', SirName, IPeriod, IPC, HMA_Method, HLength, HPhase, Shift, Digit, ShowPrice, Upper_color, Middle_color, Lower_color)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Float_Pivot_Smoothed_Digit_System')
        return INIT_FAILED
    SetIndexBuffer(0, ExtUp1Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtUp2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, ExtABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, ExtBBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(4, ExtCBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(5, ExtDn1Buffer, INDICATOR_DATA)
    SetIndexBuffer(6, ExtDn2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(7, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(8, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(9, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(10, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(11, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtUp1Buffer, True)
    ArraySetAsSeries(ExtUp2Buffer, True)
    ArraySetAsSeries(ExtABuffer, True)
    ArraySetAsSeries(ExtBBuffer, True)
    ArraySetAsSeries(ExtCBuffer, True)
    ArraySetAsSeries(ExtDn1Buffer, True)
    ArraySetAsSeries(ExtDn2Buffer, True)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Float_Pivot_Smoothed_Digit_System', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if not TimeFramesCheck('Float_Pivot_Smoothed_Digit_System', TimeFrame):
        return 0
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, ExtUp1Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(1, "", TimeFrame, Ind_Handle, 1, ExtUp2Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(2, "", TimeFrame, Ind_Handle, 2, ExtABuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(3, "", TimeFrame, Ind_Handle, 3, ExtBBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(4, "", TimeFrame, Ind_Handle, 4, ExtCBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(5, "", TimeFrame, Ind_Handle, 5, ExtDn1Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(6, "", TimeFrame, Ind_Handle, 6, ExtDn2Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicatorBar("", TimeFrame, Ind_Handle, time, open, high, low, close, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Empty_Value, Draw_Begin, nShift):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    ArraySetAsSeries(Buffer, True)

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
            if CopyBuffer(IndHandle, BuffNumb, Time[bar] - (Shift * PeriodSeconds(TimeFrame)), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf[bar] = Arr_[0]
        else:
            IndBuf[bar] = IndBuf[bar + 1]
    return True

def CountIndicatorBar(Symb, TFrame, IndHandle, Time, Open, High, Low, Close, Rates_Total, Prev_Calculated, Min_Rates_Total):
    global _s_CountIndicatorBar_LastCountBar
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicatorBar_LastCountBar = limit
    else:
        limit = _s_CountIndicatorBar_LastCountBar + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        ExtLowBuffer[bar] = 0.0
        ExtHighBuffer[bar] = ExtLowBuffer[bar]
        ExtCloseBuffer[bar] = ExtHighBuffer[bar]
        ExtOpenBuffer[bar] = ExtCloseBuffer[bar]
        ExtColorBuffer[bar] = 2.0
        if CopyTime(Symbol(), TimeFrame, _DT(Time[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if Time[bar] >= IndTime[0] and Time[bar + 1] < IndTime[0]:
            _s_CountIndicatorBar_LastCountBar = bar
            Col = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, 11, _DT(Time[bar]), 1, Col) <= 0:
                return (0 != 0)
            ExtColorBuffer[bar] = 2.0
            if Col[0] > 2:
                if Open[bar] <= Close[bar]:
                    ExtColorBuffer[bar] = 4.0
                else:
                    ExtColorBuffer[bar] = 3.0
                ExtOpenBuffer[bar] = Open[bar]
                ExtLowBuffer[bar] = Low[bar]
                ExtHighBuffer[bar] = High[bar]
                ExtCloseBuffer[bar] = Close[bar]
            elif Col[0] < 2:
                if Open[bar] >= Close[bar]:
                    ExtColorBuffer[bar] = 0.0
                else:
                    ExtColorBuffer[bar] = 1.0
                ExtOpenBuffer[bar] = Open[bar]
                ExtLowBuffer[bar] = Low[bar]
                ExtHighBuffer[bar] = High[bar]
                ExtCloseBuffer[bar] = Close[bar]
        else:
            if ExtColorBuffer[bar + 1] > 2:
                if Open[bar] <= Close[bar]:
                    ExtColorBuffer[bar] = 4.0
                else:
                    ExtColorBuffer[bar] = 3.0
                ExtOpenBuffer[bar] = Open[bar]
                ExtLowBuffer[bar] = Low[bar]
                ExtHighBuffer[bar] = High[bar]
                ExtCloseBuffer[bar] = Close[bar]
            elif ExtColorBuffer[bar + 1] < 2:
                if Open[bar] >= Close[bar]:
                    ExtColorBuffer[bar] = 0.0
                else:
                    ExtColorBuffer[bar] = 1.0
                ExtOpenBuffer[bar] = Open[bar]
                ExtLowBuffer[bar] = Low[bar]
                ExtHighBuffer[bar] = High[bar]
                ExtCloseBuffer[bar] = Close[bar]
    return True

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Comment('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика! \n Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(12, 0, dyn=False)
_s_CountIndicatorBar_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FloatPivotSmoothedDigitSystemHTF(_MQL5Indicator):
    name = 'Float_Pivot_Smoothed_Digit_System_HTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора
        'IPeriod': 100,  # Период поиска экстремумов
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW0_2', 12: 'Demark Price'}, default=5),  # ценовая константа
        'HMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод сглаживания
        'HLength': 12,  # Глубина  сглаживания
        'HPhase': 100,  # Параметр сглаживания,
        'Shift': 3,  # сдвиг индикатора по горизонтали в барах
        'Digit': 2,  # количество разрядов округления
        'ShowPrice': True,  # показывать ценовые метки
    }

