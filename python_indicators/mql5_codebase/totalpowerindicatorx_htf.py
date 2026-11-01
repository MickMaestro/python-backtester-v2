"""TotalPowerIndicatorX_HTF — converted from MQL5: MQL5 Indicators/TotalPowerIndicatorX_HTF/TotalPowerIndicatorX_HTF.mq5

TotalPowerIndicatorX с фиксированным во входных параметрах таймфреймом
Copyright: Copyright © 2017, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2, 'indicator_minimum': -5.0, 'indicator_maximum': 105.0}, 'types': {1: 7, 2: 1}, 'colors': {1: [16748574, 16711935], 2: [13382297]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'BullsBears Cloud', 2: 'Power'}, 'levels': [100.0, 50.0, 0.0], 'description': ['TotalPowerIndicatorX с фиксированным во входных параметрах таймфреймом'], 'name': 'TotalPowerIndicatorX_HTF', 'source': 'MQL5 Indicators/TotalPowerIndicatorX_HTF/TotalPowerIndicatorX_HTF.mq5', 'folder': 'TotalPowerIndicatorX_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора', 'sinput': False}, {'mql': 'PowerPeriod', 'py': 'PowerPeriod', 'param': 'PowerPeriod', 'type': 'int', 'default': 10, 'label': 'период индикатора', 'sinput': False}, {'mql': 'LookbackPeriod', 'py': 'LookbackPeriod', 'param': 'LookbackPeriod', 'type': 'int', 'default': 45, 'label': 'период сглаживания', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора
PowerPeriod = _input('PowerPeriod', 10)  # период индикатора
LookbackPeriod = _input('LookbackPeriod', 45)  # период сглаживания
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
Ind1Buffer = Arr(0, 0.0)
Ind2Buffer = Arr(0, 0.0)
Ind3Buffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('TotalPowerIndicatorX', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'TotalPowerIndicatorX', PowerPeriod, LookbackPeriod, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора TotalPowerIndicatorX')
        return INIT_FAILED
    IndInit(0, Ind1Buffer, INDICATOR_DATA)
    IndInit(1, Ind2Buffer, INDICATOR_DATA)
    IndInit(2, Ind3Buffer, INDICATOR_DATA)
    PlotInit(0, EMPTY_VALUE, 0, Shift)
    PlotInit(1, EMPTY_VALUE, 0, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'TotalPowerIndicatorX', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, Ind1Buffer, 1, Ind2Buffer, 2, Ind3Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb1, IndBuf1, BuffNumb2, IndBuf2, BuffNumb3, IndBuf3, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
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
        else:
            IndBuf1[bar] = IndBuf1[bar + 1]
            IndBuf2[bar] = IndBuf2[bar + 1]
            IndBuf3[bar] = IndBuf3[bar + 1]
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


class TotalPowerIndicatorXHTF(_MQL5Indicator):
    name = 'TotalPowerIndicatorX_HTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора
        'PowerPeriod': 10,  # период индикатора
        'LookbackPeriod': 45,  # период сглаживания
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }
    y_range = (-5.0, 105.0)

