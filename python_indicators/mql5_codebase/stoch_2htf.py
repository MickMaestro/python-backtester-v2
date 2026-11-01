"""stoch_2htf — converted from MQL5: MQL5 Indicators/Stoch_2HTF/stoch_2htf.mq5

Цветное облако из осцилляторов Stoch с разных таймфреймов на одном графике.
Copyright: Copyright © 2006, lukas1; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, lukas1', 'link': '', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16776960, 13850042]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Stoch_2HTF'}, 'levels': [80.0, 50.0, 20.0], 'description': ['Цветное облако из осцилляторов Stoch с разных таймфреймов на одном графике.'], 'name': 'stoch_2htf', 'source': 'MQL5 Indicators/Stoch_2HTF/stoch_2htf.mq5', 'folder': 'Stoch_2HTF', 'inputs': [{'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 16386, 'label': 'Период графика индикатора 1 (младший таймфрейм)', 'sinput': False}, {'mql': 'KPeriod1', 'py': 'KPeriod1', 'param': 'KPeriod1', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'DPeriod1', 'py': 'DPeriod1', 'param': 'DPeriod1', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing1', 'py': 'Slowing1', 'param': 'Slowing1', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_field1', 'py': 'Price_field1', 'param': 'Price_field1', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Line_Type1', 'py': 'Line_Type1', 'param': 'Line_Type1', 'type': 'int', 'default': 1, 'label': 'Тип линии 1', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора 2 (старший таймфрейм)', 'sinput': False}, {'mql': 'KPeriod2', 'py': 'KPeriod2', 'param': 'KPeriod2', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'DPeriod2', 'py': 'DPeriod2', 'param': 'DPeriod2', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing2', 'py': 'Slowing2', 'param': 'Slowing2', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Price_field2', 'py': 'Price_field2', 'param': 'Price_field2', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Line_Type2', 'py': 'Line_Type2', 'param': 'Line_Type2', 'type': 'int', 'default': 1, 'label': 'Тип линии 2', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Line
MODE_MAIN = 0
MODE_SIGNAL = 1
_enum('Line', {0: 'MODE_MAIN', 1: 'MODE_SIGNAL'})

# ---- inputs and global variables
TimeFrame1 = _input('TimeFrame1', PERIOD_H2)  # Период графика индикатора 1 (младший таймфрейм)
KPeriod1 = _input('KPeriod1', 5)
DPeriod1 = _input('DPeriod1', 3)
Slowing1 = _input('Slowing1', 3)
MA_Method1 = _input('MA_Method1', MODE_SMA)
Price_field1 = _input('Price_field1', STO_LOWHIGH)
Line_Type1 = _input('Line_Type1', MODE_SIGNAL)  # Тип линии 1
TimeFrame2 = _input('TimeFrame2', PERIOD_H4)  # Период графика индикатора 2 (старший таймфрейм)
KPeriod2 = _input('KPeriod2', 5)
DPeriod2 = _input('DPeriod2', 3)
Slowing2 = _input('Slowing2', 3)
MA_Method2 = _input('MA_Method2', MODE_SMA)
Price_field2 = _input('Price_field2', STO_LOWHIGH)
Line_Type2 = _input('Line_Type2', MODE_SIGNAL)  # Тип линии 2
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
Ind1Buffer = Arr(0, 0.0)
Ind2Buffer = Arr(0, 0.0)
min_rates_total = 0
Ind1_Handle = 0
Ind2_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind1_Handle, Ind2_Handle, min_rates_total
    if not TimeFramesCheck('Stoch', TimeFrame1, TimeFrame2):
        return INIT_FAILED
    min_rates_total = 2
    Ind1_Handle = iStochastic(Symbol(), TimeFrame1, KPeriod1, DPeriod1, Slowing1, MA_Method1, Price_field1)
    if Ind1_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Stoch 1')
        return INIT_FAILED
    Ind2_Handle = iStochastic(Symbol(), TimeFrame2, KPeriod2, DPeriod2, Slowing2, MA_Method2, Price_field2)
    if Ind2_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Stoch 2')
        return INIT_FAILED
    IndInit(0, Ind1Buffer)
    IndInit(1, Ind2Buffer)
    PlotInit(0, 0.0, min_rates_total, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'Stoch', '(', GetStringTimeframe(TimeFrame1), ', ', GetStringTimeframe(TimeFrame2), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind1_Handle) < Bars(Symbol(), TimeFrame1):
        return prev_calculated
    if BarsCalculated(Ind2_Handle) < Bars(Symbol(), TimeFrame2):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame1, Ind1_Handle, Line_Type1, Ind1Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(1, "", TimeFrame2, Ind2_Handle, Line_Type2, Ind2Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb, IndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        IndBuf[bar] = 0.0
        if CopyTime(Symbol(), TFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            Arr_ = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf[bar] = Arr_[0]
        else:
            IndBuf[bar] = IndBuf[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame1, TFrame2):
    if TFrame1 < Period() and TFrame1 != PERIOD_CURRENT:
        Print('Период графика 1 для индикатора ' + IndName + ' не может быть меньше периода текущего графика!')
        Print('Следует изменить входные параметры индикатора!')
        return (0 != 0)
    if TFrame2 <= TFrame1:
        Print('Период графика 2 для индикатора ' + IndName + ' должен быть больше периода графика 1!')
        Print('Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(2, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Stoch2htf(_MQL5Indicator):
    name = 'stoch_2htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16386),  # Период графика индикатора 1 (младший таймфрейм)
        'KPeriod1': 5,
        'DPeriod1': 3,
        'Slowing1': 3,
        'MA_Method1': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_field1': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
        'Line_Type1': _Choice({0: 'основная линия', 1: 'сигнальная линия'}, default=1),  # Тип линии 1
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора 2 (старший таймфрейм)
        'KPeriod2': 5,
        'DPeriod2': 3,
        'Slowing2': 3,
        'MA_Method2': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Price_field2': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),
        'Line_Type2': _Choice({0: 'основная линия', 1: 'сигнальная линия'}, default=1),  # Тип линии 2
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

