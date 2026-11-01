"""ibbfill_htf — converted from MQL5: MQL5 Indicators/iBBFill_HTF/ibbfill_htf.mq5

iBBFill с возможностью изменения таймфрейма во входных параметрах
Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 10, 'indicator_plots': 6}, 'types': {1: 7, 2: 7, 3: 7, 4: 1, 5: 1, 6: 1}, 'colors': {1: [4590090], 2: [657990], 3: [3289650], 4: [65535], 5: [16748574], 6: [255]}, 'widths': {4: 2, 5: 2, 6: 2}, 'styles': {4: 0, 5: 0, 6: 0}, 'labels': {1: 'UpTrend', 2: 'DnTrend', 3: 'Flat', 4: 'BB MA', 5: 'BB Upper', 6: 'BB Lower'}, 'levels': [], 'description': ['iBBFill с возможностью изменения таймфрейма во входных параметрах'], 'name': 'ibbfill_htf', 'source': 'MQL5 Indicators/iBBFill_HTF/ibbfill_htf.mq5', 'folder': 'iBBFill_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора (таймфрейм)', 'sinput': False}, {'mql': 'BBPeriod', 'py': 'BBPeriod', 'param': 'BBPeriod', 'type': 'uint', 'default': 20, 'label': 'Период BB', 'sinput': False}, {'mql': 'BBDeviation', 'py': 'BBDeviation', 'param': 'BBDeviation', 'type': 'double', 'default': 2.0, 'label': 'Ширина BB', 'sinput': False}, {'mql': 'BBPrice', 'py': 'BBPrice', 'param': 'BBPrice', 'type': 'int', 'default': 1, 'label': 'Цена BB', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора (таймфрейм)
BBPeriod = _input('BBPeriod', 20)  # Период BB
BBDeviation = _input('BBDeviation', 2.0)  # Ширина BB
BBPrice = _input('BBPrice', PRICE_CLOSE)  # Цена BB
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
UpIndBuffer1 = Arr(0, 0.0)
DnIndBuffer1 = Arr(0, 0.0)
UpIndBuffer2 = Arr(0, 0.0)
DnIndBuffer2 = Arr(0, 0.0)
UpIndBuffer3 = Arr(0, 0.0)
DnIndBuffer3 = Arr(0, 0.0)
IndBuffer1 = Arr(0, 0.0)
IndBuffer2 = Arr(0, 0.0)
IndBuffer3 = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('iBBFill', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'iBBFill', BBPeriod, BBDeviation, BBPrice)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iBBFill')
        return INIT_FAILED
    IndInit(0, UpIndBuffer1, INDICATOR_DATA)
    IndInit(1, DnIndBuffer1, INDICATOR_DATA)
    IndInit(2, UpIndBuffer2, INDICATOR_DATA)
    IndInit(3, DnIndBuffer2, INDICATOR_DATA)
    IndInit(4, UpIndBuffer3, INDICATOR_DATA)
    IndInit(5, DnIndBuffer3, INDICATOR_DATA)
    IndInit(6, IndBuffer1, INDICATOR_DATA)
    IndInit(7, IndBuffer2, INDICATOR_DATA)
    IndInit(8, IndBuffer3, INDICATOR_DATA)
    for count in range(0, 6):
        PlotInit(count, 0, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'iBBFill', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountCloudIndicator(0, "", TimeFrame, Ind_Handle, 0, UpIndBuffer1, 1, DnIndBuffer1, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountCloudIndicator(1, "", TimeFrame, Ind_Handle, 2, UpIndBuffer2, 3, DnIndBuffer2, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountCloudIndicator(2, "", TimeFrame, Ind_Handle, 4, UpIndBuffer3, 5, DnIndBuffer3, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountLineIndicator(0, "", TimeFrame, Ind_Handle, 6, IndBuffer1, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountLineIndicator(1, "", TimeFrame, Ind_Handle, 7, IndBuffer2, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountLineIndicator(2, "", TimeFrame, Ind_Handle, 8, IndBuffer3, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def CountCloudIndicator(Numb, Symb, TFrame, IndHandle, UpBuffNumb, UpIndBuf, DnBuffNumb, DnIndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountCloudIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountCloudIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        if CopyTime(Symbol(), TFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountCloudIndicator_LastCountBar[Numb] = bar
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

def CountLineIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb, IndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountLineIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountLineIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        if CopyTime(Symbol(), TFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountLineIndicator_LastCountBar[Numb] = bar
            Arr_ = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf[bar] = Arr_[0]
        else:
            IndBuf[bar] = IndBuf[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика!')
        Print('Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountCloudIndicator_LastCountBar = Arr(3, 0, dyn=False)
_s_CountLineIndicator_LastCountBar = Arr(3, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IbbfillHtf(_MQL5Indicator):
    name = 'ibbfill_htf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора (таймфрейм)
        'BBPeriod': 20,  # Период BB
        'BBDeviation': 2.0,  # Ширина BB
        'BBPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Цена BB
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

