"""T3Taotra_HTF — converted from MQL5: MQL5 Indicators/T3Taotra_HTF/T3Taotra_HTF.mq5

T3Taotra с возможностью изменения таймфрейма во входных параметрах
Copyright: Copyright © 2016, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [65535], 2: [255], 3: [16711935], 4: [16776960], 5: [3329330], 6: [16711680]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'T3Taotra1', 2: 'T3Taotra2', 3: 'T3Taotra3', 4: 'T3Taotra4', 5: 'T3Taotra5', 6: 'T3Taotra6'}, 'levels': [], 'description': ['T3Taotra с возможностью изменения таймфрейма во входных параметрах'], 'name': 'T3Taotra_HTF', 'source': 'MQL5 Indicators/T3Taotra_HTF/T3Taotra_HTF.mq5', 'folder': 'T3Taotra_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'период графика', 'sinput': False}, {'mql': 'T3_Period_1', 'py': 'T3_Period_1', 'param': 'T3_Period_1', 'type': 'int', 'default': 3, 'label': 'период индикатора 1', 'sinput': False}, {'mql': 'T3_Period_2', 'py': 'T3_Period_2', 'param': 'T3_Period_2', 'type': 'int', 'default': 5, 'label': 'период индикатора 2', 'sinput': False}, {'mql': 'T3_Period_3', 'py': 'T3_Period_3', 'param': 'T3_Period_3', 'type': 'int', 'default': 8, 'label': 'период индикатора 3', 'sinput': False}, {'mql': 'T3_Period_4', 'py': 'T3_Period_4', 'param': 'T3_Period_4', 'type': 'int', 'default': 12, 'label': 'период индикатора 4', 'sinput': False}, {'mql': 'T3_Period_5', 'py': 'T3_Period_5', 'param': 'T3_Period_5', 'type': 'int', 'default': 21, 'label': 'период индикатора 5', 'sinput': False}, {'mql': 'T3_Period_6', 'py': 'T3_Period_6', 'param': 'T3_Period_6', 'type': 'int', 'default': 34, 'label': 'период индикатора 6', 'sinput': False}, {'mql': 'Smooth_Curvature', 'py': 'Smooth_Curvature', 'param': 'Smooth_Curvature', 'type': 'int', 'default': 100, 'label': '', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift1', 'py': 'Shift1', 'param': 'Shift1', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора 1 вдоль оси времени', 'sinput': False}, {'mql': 'Shift2', 'py': 'Shift2', 'param': 'Shift2', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора 2 вдоль оси времени', 'sinput': False}, {'mql': 'Shift3', 'py': 'Shift3', 'param': 'Shift3', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора 3 вдоль оси времени', 'sinput': False}, {'mql': 'Shift4', 'py': 'Shift4', 'param': 'Shift4', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора 6 вдоль оси времени', 'sinput': False}, {'mql': 'Shift5', 'py': 'Shift5', 'param': 'Shift5', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора 5 вдоль оси времени', 'sinput': False}, {'mql': 'Shift6', 'py': 'Shift6', 'param': 'Shift6', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора 6 вдоль оси времени', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # период графика
T3_Period_1 = _input('T3_Period_1', 3)  # период индикатора 1
T3_Period_2 = _input('T3_Period_2', 5)  # период индикатора 2
T3_Period_3 = _input('T3_Period_3', 8)  # период индикатора 3
T3_Period_4 = _input('T3_Period_4', 12)  # период индикатора 4
T3_Period_5 = _input('T3_Period_5', 21)  # период индикатора 5
T3_Period_6 = _input('T3_Period_6', 34)  # период индикатора 6
Smooth_Curvature = _input('Smooth_Curvature', 100)
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift1 = _input('Shift1', 0)  # cдвиг индикатора 1 вдоль оси времени
Shift2 = _input('Shift2', 0)  # cдвиг индикатора 2 вдоль оси времени
Shift3 = _input('Shift3', 0)  # cдвиг индикатора 3 вдоль оси времени
Shift4 = _input('Shift4', 0)  # cдвиг индикатора 6 вдоль оси времени
Shift5 = _input('Shift5', 0)  # cдвиг индикатора 5 вдоль оси времени
Shift6 = _input('Shift6', 0)  # cдвиг индикатора 6 вдоль оси времени
IndBuffer1 = Arr(0, 0.0)
IndBuffer2 = Arr(0, 0.0)
IndBuffer3 = Arr(0, 0.0)
IndBuffer4 = Arr(0, 0.0)
IndBuffer5 = Arr(0, 0.0)
IndBuffer6 = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('T3Taotra', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'T3Taotra', T3_Period_1, T3_Period_2, T3_Period_3, T3_Period_4, T3_Period_5, T3_Period_6, Smooth_Curvature, IPC, 0, 0, 0, 0, 0, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора PChannel')
        return INIT_FAILED
    IndInit(0, IndBuffer1, INDICATOR_DATA)
    IndInit(1, IndBuffer2, INDICATOR_DATA)
    IndInit(2, IndBuffer3, INDICATOR_DATA)
    IndInit(3, IndBuffer4, INDICATOR_DATA)
    IndInit(4, IndBuffer5, INDICATOR_DATA)
    IndInit(5, IndBuffer6, INDICATOR_DATA)
    PlotInit(0, 0.0, 0, Shift1)
    PlotInit(1, 0.0, 0, Shift2)
    PlotInit(2, 0.0, 0, Shift3)
    PlotInit(3, 0.0, 0, Shift4)
    PlotInit(4, 0.0, 0, Shift5)
    PlotInit(5, 0.0, 0, Shift6)
    shortname = Box("")
    StringConcatenate(shortname, 'T3Taotra', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, IndBuffer1, 1, IndBuffer2, 2, IndBuffer3, 3, IndBuffer4, 4, IndBuffer5, 5, IndBuffer6, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb1, IndBuf1, BuffNumb2, IndBuf2, BuffNumb3, IndBuf3, BuffNumb4, IndBuf4, BuffNumb5, IndBuf5, BuffNumb6, IndBuf6, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
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
            Arr5 = Arr(1, 0.0, dyn=False)
            Arr6 = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb1, _DT(iTime_[bar]), 1, Arr1) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, BuffNumb2, _DT(iTime_[bar]), 1, Arr2) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, BuffNumb3, _DT(iTime_[bar]), 1, Arr3) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, BuffNumb4, _DT(iTime_[bar]), 1, Arr4) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, BuffNumb5, _DT(iTime_[bar]), 1, Arr5) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, BuffNumb6, _DT(iTime_[bar]), 1, Arr6) <= 0:
                return (0 != 0)
            IndBuf1[bar] = Arr1[0]
            IndBuf2[bar] = Arr2[0]
            IndBuf3[bar] = Arr3[0]
            IndBuf4[bar] = Arr4[0]
            IndBuf5[bar] = Arr5[0]
            IndBuf6[bar] = Arr6[0]
        else:
            IndBuf1[bar] = IndBuf1[bar + 1]
            IndBuf2[bar] = IndBuf2[bar + 1]
            IndBuf3[bar] = IndBuf3[bar + 1]
            IndBuf4[bar] = IndBuf4[bar + 1]
            IndBuf5[bar] = IndBuf5[bar + 1]
            IndBuf6[bar] = IndBuf6[bar + 1]
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


class T3TaotraHTF(_MQL5Indicator):
    name = 'T3Taotra_HTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # период графика
        'T3_Period_1': 3,  # период индикатора 1
        'T3_Period_2': 5,  # период индикатора 2
        'T3_Period_3': 8,  # период индикатора 3
        'T3_Period_4': 12,  # период индикатора 4
        'T3_Period_5': 21,  # период индикатора 5
        'T3_Period_6': 34,  # период индикатора 6
        'Smooth_Curvature': 100,
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL', 9: 'PRICE_QUARTER', 10: 'PRICE_TRENDFOLLOW0', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift1': 0,  # cдвиг индикатора 1 вдоль оси времени
        'Shift2': 0,  # cдвиг индикатора 2 вдоль оси времени
        'Shift3': 0,  # cдвиг индикатора 3 вдоль оси времени
        'Shift4': 0,  # cдвиг индикатора 6 вдоль оси времени
        'Shift5': 0,  # cдвиг индикатора 5 вдоль оси времени
        'Shift6': 0,  # cдвиг индикатора 6 вдоль оси времени
    }

