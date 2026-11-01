"""begin_trend_v02_htf — converted from MQL5: MQL5 Indicators/Begin_Trend_v02_HTF/begin_trend_v02_htf.mq5

Begin_Trend_v02 с возможностью изменения таймфрейма во входных параметрах
Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 3, 4: 3}, 'colors': {1: [3329330], 2: [255], 3: [65280], 4: [255]}, 'widths': {1: 2, 2: 2, 3: 4, 4: 4}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Begin_Trend_v01 Up', 2: 'Begin_Trend_v01 Down', 3: 'Begin_Trend_v01 Up', 4: 'Begin_Trend_v01 Down'}, 'levels': [100.0, 50.0, 0.0, -50.0, -100.0], 'description': ['Begin_Trend_v02 с возможностью изменения таймфрейма во входных параметрах'], 'name': 'begin_trend_v02_htf', 'source': 'MQL5 Indicators/Begin_Trend_v02_HTF/begin_trend_v02_htf.mq5', 'folder': 'Begin_Trend_v02_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора (таймфрейм)', 'sinput': False}, {'mql': 'Period_Channel', 'py': 'Period_Channel', 'param': 'Period_Channel', 'type': 'uint', 'default': 70, 'label': '', 'sinput': False}, {'mql': 'Period_Input', 'py': 'Period_Input', 'param': 'Period_Input', 'type': 'uint', 'default': 48, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора (таймфрейм)
Period_Channel = _input('Period_Channel', 70)
Period_Input = _input('Period_Input', 48)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
Up1IndBuffer = Arr(0, 0.0)
Dn1IndBuffer = Arr(0, 0.0)
Up2IndBuffer = Arr(0, 0.0)
Dn2IndBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('Begin_Trend_v02', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'Begin_Trend_v02', Period_Channel, Period_Input, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Begin_Trend_v02')
        return INIT_FAILED
    IndInit(0, Up1IndBuffer, INDICATOR_DATA)
    IndInit(1, Dn1IndBuffer, INDICATOR_DATA)
    IndInit(2, Up2IndBuffer, INDICATOR_DATA)
    IndInit(3, Dn2IndBuffer, INDICATOR_DATA)
    PlotInit(0, EMPTY_VALUE, 0, Shift)
    PlotInit(1, EMPTY_VALUE, 0, Shift)
    PlotInit(2, EMPTY_VALUE, 0, Shift)
    PlotInit(3, EMPTY_VALUE, 0, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'Begin_Trend_v02', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, Up1IndBuffer, 1, Dn1IndBuffer, 2, Up2IndBuffer, 3, Dn2IndBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def CountIndicator(Numb, Symb, TFrame, IndHandle, Up1BuffNumb, Up1IndBuf, Dn1BuffNumb, Dn1IndBuf, Up2BuffNumb, Up2IndBuf, Dn2BuffNumb, Dn2IndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
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
            Up1Arr = Arr(1, 0.0, dyn=False)
            Dn1Arr = Arr(1, 0.0, dyn=False)
            Up2Arr = Arr(1, 0.0, dyn=False)
            Dn2Arr = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, Up1BuffNumb, _DT(iTime_[bar]), 1, Up1Arr) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, Dn1BuffNumb, _DT(iTime_[bar]), 1, Dn1Arr) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, Up2BuffNumb, _DT(iTime_[bar]), 1, Up2Arr) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, Dn2BuffNumb, _DT(iTime_[bar]), 1, Dn2Arr) <= 0:
                return (0 != 0)
            Up1IndBuf[bar] = Up1Arr[0]
            Dn1IndBuf[bar] = Dn1Arr[0]
            Up2IndBuf[bar] = Up2Arr[0]
            Dn2IndBuf[bar] = Dn2Arr[0]
        else:
            Up1IndBuf[bar] = Up1IndBuf[bar + 1]
            Dn1IndBuf[bar] = Dn1IndBuf[bar + 1]
            Up2IndBuf[bar] = Up2IndBuf[bar + 1]
            Dn2IndBuf[bar] = Dn2IndBuf[bar + 1]
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


class BeginTrendV02Htf(_MQL5Indicator):
    name = 'begin_trend_v02_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора (таймфрейм)
        'Period_Channel': 70,
        'Period_Input': 48,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

