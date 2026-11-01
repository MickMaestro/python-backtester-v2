"""ColorParabolic_HTF — converted from MQL5: MQL5 Indicators/ColorParabolic_HTF/ColorParabolic_HTF.mq5

PChannel с возможностью изменения таймфрейма во входных параметрах
Copyright: Copyright © 2017, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [16711935], 2: [16748574], 3: [16711935], 4: [16748574]}, 'widths': {1: 4, 2: 4, 3: 4, 4: 4}, 'styles': {}, 'labels': {1: 'Lower Parabolic', 2: 'Upper Parabolic', 3: 'Parabolic Sell', 4: 'Parabolic Buy'}, 'levels': [], 'description': ['PChannel с возможностью изменения таймфрейма во входных параметрах'], 'name': 'ColorParabolic_HTF', 'source': 'MQL5 Indicators/ColorParabolic_HTF/ColorParabolic_HTF.mq5', 'folder': 'ColorParabolic_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора (таймфрейм)', 'sinput': False}, {'mql': 'StepH_', 'py': 'StepH_', 'param': 'StepH_', 'type': 'double', 'default': 0.02, 'label': 'Шаг для верхних точек', 'sinput': False}, {'mql': 'MaximumH', 'py': 'MaximumH', 'param': 'MaximumH', 'type': 'double', 'default': 0.5, 'label': 'Максимум для верхних точек', 'sinput': False}, {'mql': 'StepL_', 'py': 'StepL_', 'param': 'StepL_', 'type': 'double', 'default': 0.02, 'label': 'Шаг для нижних точек', 'sinput': False}, {'mql': 'MaximumL', 'py': 'MaximumL', 'param': 'MaximumL', 'type': 'double', 'default': 0.5, 'label': 'Максимум для нижних точек', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора (таймфрейм)
StepH_ = _input('StepH_', 0.02)  # Шаг для верхних точек
MaximumH = _input('MaximumH', 0.5)  # Максимум для верхних точек
StepL_ = _input('StepL_', 0.02)  # Шаг для нижних точек
MaximumL = _input('MaximumL', 0.5)  # Максимум для нижних точек
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
    if not TimeFramesCheck('ColorParabolic', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'ColorParabolic', StepH_, MaximumH, StepL_, MaximumL)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора PChannel')
        return INIT_FAILED
    IndInit(0, IndBuffer1, INDICATOR_DATA)
    IndInit(1, IndBuffer2, INDICATOR_DATA)
    IndInit(2, IndBuffer3, INDICATOR_DATA)
    IndInit(3, IndBuffer4, INDICATOR_DATA)
    PlotInit(0, EMPTY_VALUE, 0, Shift)
    PlotInit(1, EMPTY_VALUE, 0, Shift)
    PlotInit(2, EMPTY_VALUE, 0, Shift)
    PlotInit(3, EMPTY_VALUE, 0, Shift)
    PlotIndexSetInteger(0, PLOT_ARROW, 158)
    PlotIndexSetInteger(1, PLOT_ARROW, 158)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    shortname = Box("")
    StringConcatenate(shortname, 'ColorParabolic', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, IndBuffer1, 1, IndBuffer2, 2, IndBuffer3, 3, IndBuffer4, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb1, IndBuf1, BuffNumb2, IndBuf2, BuffNumb3, IndBuf3, BuffNumb4, IndBuf4, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
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
            Arr1 = Arr(1, 0.0, dyn=False)
            Arr2 = Arr(1, 0.0, dyn=False)
            Arr3 = Arr(1, 0.0, dyn=False)
            Arr4 = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb1, _DT(iTime_[bar]), 1, Arr1) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, BuffNumb2, _DT(iTime_[bar]), 1, Arr2) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, BuffNumb3, _DT(iTime_[bar]), 1, Arr3) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, BuffNumb4, _DT(iTime_[bar]), 1, Arr4) <= 0:
                return (0 != 0)
            IndBuf1[bar] = Arr1[0]
            IndBuf2[bar] = Arr2[0]
            IndBuf3[bar] = Arr3[0]
            IndBuf4[bar] = Arr4[0]
        else:
            IndBuf1[bar] = IndBuf1[bar + 1]
            IndBuf2[bar] = IndBuf2[bar + 1]
            IndBuf3[bar] = IndBuf3[bar + 1]
            IndBuf4[bar] = IndBuf4[bar + 1]
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


class ColorParabolicHTF(_MQL5Indicator):
    name = 'ColorParabolic_HTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора (таймфрейм)
        'StepH_': 0.02,  # Шаг для верхних точек
        'MaximumH': 0.5,  # Максимум для верхних точек
        'StepL_': 0.02,  # Шаг для нижних точек
        'MaximumL': 0.5,  # Максимум для нижних точек
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

