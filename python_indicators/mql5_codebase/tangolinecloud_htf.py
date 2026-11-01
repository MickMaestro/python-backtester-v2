"""tangolinecloud_htf — converted from MQL5: MQL5 Indicators/TangoLineCloud_HTF/tangolinecloud_htf.mq5

TangoLineCloud с фиксированным во входных параметрах таймфреймом
Copyright: Copyright © 2016, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 5}, 'types': {1: 7, 2: 7, 3: 1, 4: 1, 5: 1}, 'colors': {1: [16436871], 2: [13353215], 3: [14822282], 4: [3329330], 5: [255]}, 'widths': {3: 5, 4: 2, 5: 2}, 'styles': {3: 0, 4: 0, 5: 0}, 'labels': {1: 'Upper TangoLineCloud Cloud', 2: 'Lower TangoLineCloud Cloud', 3: 'TangoLine', 4: 'Upper', 5: 'Lower'}, 'levels': [], 'description': ['TangoLineCloud с фиксированным во входных параметрах таймфреймом'], 'name': 'tangolinecloud_htf', 'source': 'MQL5 Indicators/TangoLineCloud_HTF/tangolinecloud_htf.mq5', 'folder': 'TangoLineCloud_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора', 'sinput': False}, {'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'MinSpread', 'py': 'MinSpread', 'param': 'MinSpread', 'type': 'double', 'default': 5.0, 'label': 'Min Spread', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора
InpPeriod = _input('InpPeriod', 20)  # Period
MinSpread = _input('MinSpread', 5.0)  # Min Spread
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
Ind1Buffer = Arr(0, 0.0)
Ind2Buffer = Arr(0, 0.0)
Ind3Buffer = Arr(0, 0.0)
Ind4Buffer = Arr(0, 0.0)
Ind5Buffer = Arr(0, 0.0)
Ind6Buffer = Arr(0, 0.0)
Ind7Buffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('TangoLineCloud_HTF', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'TangoLineCloud', InpPeriod, MinSpread, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора TangoLineCloud')
        return INIT_FAILED
    BuffInit(0, Ind1Buffer)
    BuffInit(1, Ind2Buffer)
    BuffInit(2, Ind3Buffer)
    BuffInit(3, Ind4Buffer)
    BuffInit(4, Ind5Buffer)
    BuffInit(5, Ind6Buffer)
    BuffInit(6, Ind7Buffer)
    IndInit(0, 0.0, min_rates_total, Shift)
    IndInit(1, 0.0, min_rates_total, Shift)
    IndInit(2, 0.0, min_rates_total, Shift)
    IndInit(3, 0.0, min_rates_total, Shift)
    IndInit(4, 0.0, min_rates_total, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'TangoLineCloud_HTF', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, Ind1Buffer, 1, Ind2Buffer, 2, Ind3Buffer, 3, Ind4Buffer, 4, Ind5Buffer, 5, Ind6Buffer, 6, Ind7Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def BuffInit(Number, Buffer):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Buffer, True)

def IndInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb1, IndBuf1, BuffNumb2, IndBuf2, BuffNumb3, IndBuf3, BuffNumb4, IndBuf4, BuffNumb5, IndBuf5, BuffNumb6, IndBuf6, BuffNumb7, IndBuf7, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
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
            if CopyBuffer(IndHandle, BuffNumb4, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf4[bar] = Arr_[0]
            if CopyBuffer(IndHandle, BuffNumb5, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf5[bar] = Arr_[0]
            if CopyBuffer(IndHandle, BuffNumb6, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf6[bar] = Arr_[0]
            if CopyBuffer(IndHandle, BuffNumb7, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf7[bar] = Arr_[0]
        else:
            IndBuf1[bar] = IndBuf1[bar + 1]
            IndBuf2[bar] = IndBuf2[bar + 1]
            IndBuf3[bar] = IndBuf3[bar + 1]
            IndBuf4[bar] = IndBuf4[bar + 1]
            IndBuf5[bar] = IndBuf5[bar + 1]
            IndBuf6[bar] = IndBuf6[bar + 1]
            IndBuf7[bar] = IndBuf7[bar + 1]
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


class TangolinecloudHtf(_MQL5Indicator):
    name = 'tangolinecloud_htf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора
        'InpPeriod': 20,  # Period
        'MinSpread': 5.0,  # Min Spread
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

