"""ichimoku_htf — converted from MQL5: MQL5 Indicators/Ichimoku_HTF/ichimoku_htf.mq5

Copyright: Copyright © 2016, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 7, 4: 1, 5: 11}, 'colors': {1: [255], 2: [16711680], 3: [15658671, 16118015], 4: [65280], 5: [255, 16711680]}, 'widths': {1: 1, 2: 1, 4: 2, 5: 1}, 'styles': {1: 0, 2: 0, 4: 0, 5: 4}, 'labels': {1: 'Tenkan-sen', 2: 'Kijun-sen', 3: 'Senkou Span A;Senkou Span B', 4: 'Chinkou Span', 5: 'Tenkan-sen; Kijun-sen'}, 'levels': [], 'description': [], 'name': 'ichimoku_htf', 'source': 'MQL5 Indicators/Ichimoku_HTF/ichimoku_htf.mq5', 'folder': 'Ichimoku_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'InpTenkan', 'py': 'InpTenkan', 'param': 'InpTenkan', 'type': 'int', 'default': 9, 'label': 'Tenkan-sen', 'sinput': False}, {'mql': 'InpKijun', 'py': 'InpKijun', 'param': 'InpKijun', 'type': 'int', 'default': 26, 'label': 'Kijun-sen', 'sinput': False}, {'mql': 'InpSenkou', 'py': 'InpSenkou', 'param': 'InpSenkou', 'type': 'int', 'default': 52, 'label': 'Senkou Span B', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
InpTenkan = _input('InpTenkan', 9)  # Tenkan-sen
InpKijun = _input('InpKijun', 26)  # Kijun-sen
InpSenkou = _input('InpSenkou', 52)  # Senkou Span B
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
ExtLineBuffer4 = Arr(0, 0.0)
ExtLineBuffer5 = Arr(0, 0.0)
ExtLineBuffer6 = Arr(0, 0.0)
ExtLineBuffer7 = Arr(0, 0.0)
ExtLineBuffer8 = Arr(0, 0.0)
Symbol_ = ""
Word = ""
min_rates_total = 0
Shift = 0
Ind_Handle = 0

def GetStringTimeframe(Timeframe):
    return StringSubstr(EnumToString(Timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, Shift, Symbol_, Word, min_rates_total
    if InpTenkan > 0:
        if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
            Print('Период графика для индикатора Ichimoku не может быть меньше периода текущего графика')
            return INIT_FAILED
    min_rates_total = 2
    if InpTenkan > 0:
        Shift = _idiv((InpKijun - 2) * PeriodSeconds(TimeFrame), PeriodSeconds(PERIOD_CURRENT))
    Symbol_ = Symbol()
    Word = 'Ichimoku' + ' индикатор: ' + Symbol_ + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1)
    if InpTenkan > 0:
        Ind_Handle = iCustom(Symbol_, TimeFrame, MQLInfoString(MQL_PROGRAM_NAME), PERIOD_CURRENT, -InpTenkan, InpKijun, InpSenkou)
        if Ind_Handle == INVALID_HANDLE:
            Print(' Не удалось получить хендл индикатора ' + MQLInfoString(MQL_PROGRAM_NAME))
            return INIT_FAILED
    SetIndexBuffer(0, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ExtLineBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLineBuffer3, INDICATOR_DATA)
    SetIndexBuffer(3, ExtLineBuffer4, INDICATOR_DATA)
    SetIndexBuffer(4, ExtLineBuffer5, INDICATOR_DATA)
    SetIndexBuffer(5, ExtLineBuffer6, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLineBuffer7, INDICATOR_DATA)
    SetIndexBuffer(7, ExtLineBuffer8, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer1, True)
    ArraySetAsSeries(ExtLineBuffer2, True)
    ArraySetAsSeries(ExtLineBuffer3, True)
    ArraySetAsSeries(ExtLineBuffer4, True)
    ArraySetAsSeries(ExtLineBuffer5, True)
    ArraySetAsSeries(ExtLineBuffer6, True)
    ArraySetAsSeries(ExtLineBuffer7, True)
    ArraySetAsSeries(ExtLineBuffer8, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Ichimoku(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    if rates_total < min_rates_total:
        return 0
    if InpTenkan > 0:
        ArraySetAsSeries(Time, True)
        time1 = Arr(1, 0, dyn=False)
        timex = Arr(0, 0)
        if CopyTime(Symbol(), TimeFrame, 1, 1, time1) <= 0:
            return 0
        if CopyTime(Symbol(), None, _DT(Time[0]), _DT(time1[0]), timex) <= 0:
            return 0
        shiftx = Shift + ArraySize(timex)
        PlotIndexSetInteger(2, PLOT_SHIFT, shiftx)
        PlotIndexSetInteger(3, PLOT_SHIFT, -shiftx)
        if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, ExtLineBuffer1, Time, rates_total, prev_calculated, min_rates_total):
            return 0
        if not CountIndicator(1, "", TimeFrame, Ind_Handle, 1, ExtLineBuffer2, Time, rates_total, prev_calculated, min_rates_total):
            return 0
        if not CountIndicator(2, "", TimeFrame, Ind_Handle, 2, ExtLineBuffer3, Time, rates_total, prev_calculated, min_rates_total):
            return 0
        if not CountIndicator(3, "", TimeFrame, Ind_Handle, 3, ExtLineBuffer4, Time, rates_total, prev_calculated, min_rates_total):
            return 0
        if not CountIndicator(4, "", TimeFrame, Ind_Handle, 4, ExtLineBuffer5, Time, rates_total, prev_calculated, min_rates_total):
            return 0
        if not CountIndicator(5, "", TimeFrame, Ind_Handle, 5, ExtLineBuffer6, Time, rates_total, prev_calculated, min_rates_total):
            return 0
        if not CountIndicator(6, "", TimeFrame, Ind_Handle, 6, ExtLineBuffer7, Time, rates_total, prev_calculated, min_rates_total):
            return 0
        if not CountIndicator(7, "", TimeFrame, Ind_Handle, 7, ExtLineBuffer8, Time, rates_total, prev_calculated, min_rates_total):
            return 0
    else:
        limit = 0
        ArraySetAsSeries(High, True)
        ArraySetAsSeries(Low, True)
        ArraySetAsSeries(Close, True)
        if prev_calculated == 0:
            limit = 0
        else:
            limit = prev_calculated - 1
        for i in range(limit, rates_total):
            ExtLineBuffer5[i] = Close[i]
            high = High[ArrayMaximum(High, i, MathAbs(InpTenkan))]
            low = Low[ArrayMinimum(Low, i, MathAbs(InpTenkan))]
            ExtLineBuffer6[i] = (high + low) / 2.0
            ExtLineBuffer1[i] = ExtLineBuffer6[i]
            high = High[ArrayMaximum(High, i, InpKijun)]
            low = Low[ArrayMinimum(Low, i, InpKijun)]
            ExtLineBuffer7[i] = (high + low) / 2.0
            ExtLineBuffer2[i] = ExtLineBuffer7[i]
            ExtLineBuffer3[i] = (ExtLineBuffer1[i] + ExtLineBuffer2[i]) / 2.0
            high = High[ArrayMaximum(High, i, InpSenkou)]
            low = Low[ArrayMinimum(Low, i, InpSenkou)]
            ExtLineBuffer4[i] = (high + low) / 2.0
            if ExtLineBuffer2[i] < ExtLineBuffer1[i]:
                ExtLineBuffer8[i] = 1.0
            else:
                ExtLineBuffer8[i] = 0.0
    return rates_total

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
        if CopyTime(Symbol_, TimeFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
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

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(8, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IchimokuHtf(_MQL5Indicator):
    name = 'ichimoku_htf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'InpTenkan': 9,  # Tenkan-sen
        'InpKijun': 26,  # Kijun-sen
        'InpSenkou': 52,  # Senkou Span B
    }

