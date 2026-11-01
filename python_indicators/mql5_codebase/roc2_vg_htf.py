"""ROC2_VG_HTF — converted from MQL5: MQL5 Indicators/ROC2_VG_HTF/ROC2_VG_HTF.mq5

ROC2_VG с возможностью изменения таймфрейма во входных параметрах
Copyright: Copyright © 2016, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [2263842, 17919]}, 'widths': {}, 'styles': {}, 'labels': {1: 'ROC2_VG HTF'}, 'levels': [], 'description': ['ROC2_VG с возможностью изменения таймфрейма во входных параметрах'], 'name': 'ROC2_VG_HTF', 'source': 'MQL5 Indicators/ROC2_VG_HTF/ROC2_VG_HTF.mq5', 'folder': 'ROC2_VG_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора (таймфрейм)', 'sinput': False}, {'mql': 'ROCPeriod1', 'py': 'ROCPeriod1', 'param': 'ROCPeriod1', 'type': 'uint', 'default': 8, 'label': '', 'sinput': False}, {'mql': 'ROCType1', 'py': 'ROCType1', 'param': 'ROCType1', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'ROCPeriod2', 'py': 'ROCPeriod2', 'param': 'ROCPeriod2', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'ROCType2', 'py': 'ROCType2', 'param': 'ROCType2', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Livel1', 'py': 'Livel1', 'param': 'Livel1', 'type': 'double', 'default': 0.005, 'label': '', 'sinput': False}, {'mql': 'Livel2', 'py': 'Livel2', 'param': 'Livel2', 'type': 'double', 'default': 0.002, 'label': '', 'sinput': False}, {'mql': 'Livel3', 'py': 'Livel3', 'param': 'Livel3', 'type': 'double', 'default': 0.0, 'label': '', 'sinput': False}, {'mql': 'Livel4', 'py': 'Livel4', 'param': 'Livel4', 'type': 'double', 'default': -0.002, 'label': '', 'sinput': False}, {'mql': 'Livel5', 'py': 'Livel5', 'param': 'Livel5', 'type': 'double', 'default': -0.005, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_TYPE
MOM = 1
ROC = 2
ROCP = 3
ROCR = 4
ROCR100 = 5
_enum('ENUM_TYPE', {1: 'MOM', 2: 'ROC', 3: 'ROCP', 4: 'ROCR', 5: 'ROCR100'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора (таймфрейм)
ROCPeriod1 = _input('ROCPeriod1', 8)
ROCType1 = _input('ROCType1', MOM)
ROCPeriod2 = _input('ROCPeriod2', 14)
ROCType2 = _input('ROCType2', MOM)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
Livel1 = _input('Livel1', 0.005)
Livel2 = _input('Livel2', 0.002)
Livel3 = _input('Livel3', 0.0)
Livel4 = _input('Livel4', -0.002)
Livel5 = _input('Livel5', -0.005)
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('ROC2_VG', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'ROC2_VG', ROCPeriod1, ROCType1, ROCPeriod2, ROCType2, 0, 0, 0, 0, 0, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ROC2_VG')
        return INIT_FAILED
    IndInit(0, UpIndBuffer, INDICATOR_DATA)
    IndInit(1, DnIndBuffer, INDICATOR_DATA)
    PlotInit(0, EMPTY_VALUE, 0, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'ROC2_VG', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 5)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, Livel1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, Livel2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, Livel3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, Livel4)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 4, Livel5)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrDodgerBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 3, clrRed)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 4, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASH)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 3, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 4, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, UpIndBuffer, 1, DnIndBuffer, time, rates_total, prev_calculated, min_rates_total):
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
_s_CountIndicator_LastCountBar = Arr(1, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ROC2VGHTF(_MQL5Indicator):
    name = 'ROC2_VG_HTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора (таймфрейм)
        'ROCPeriod1': 8,
        'ROCType1': _Choice({1: 'MOM', 2: 'ROC', 3: 'ROCP', 4: 'ROC', 5: 'ROCR100'}, default=1),
        'ROCPeriod2': 14,
        'ROCType2': _Choice({1: 'MOM', 2: 'ROC', 3: 'ROCP', 4: 'ROC', 5: 'ROCR100'}, default=1),
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'Livel1': 0.005,
        'Livel2': 0.002,
        'Livel3': 0.0,
        'Livel4': -0.002,
        'Livel5': -0.005,
    }

