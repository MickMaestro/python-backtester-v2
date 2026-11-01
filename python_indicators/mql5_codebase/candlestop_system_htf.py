"""CandleStop_System_HTF — converted from MQL5: MQL5 Indicators/CandleStop_System_HTF/CandleStop_System_HTF.mq5

Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 1, 4: 17}, 'colors': {1: [16443110], 2: [3329330], 3: [42495], 4: [9639167, 8388736, 16711680, 16748574]}, 'widths': {2: 3, 3: 3}, 'styles': {2: 0, 3: 0}, 'labels': {1: 'CandleStop Channel', 2: 'CandleStop Up Line', 3: 'CandleStop Down Line', 4: 'CandleStop_Open;CandleStop_High;CandleStop_Low;CandleStop_Close'}, 'levels': [], 'description': [], 'name': 'CandleStop_System_HTF', 'source': 'MQL5 Indicators/CandleStop_System_HTF/CandleStop_System_HTF.mq5', 'folder': 'CandleStop_System_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'UpTrailPeriods', 'py': 'UpTrailPeriods', 'param': 'UpTrailPeriods', 'type': 'uint', 'default': 5, 'label': 'Период поиска для хая', 'sinput': False}, {'mql': 'UpTrailShift', 'py': 'UpTrailShift', 'param': 'UpTrailShift', 'type': 'uint', 'default': 5, 'label': 'Период сдвига для хая', 'sinput': False}, {'mql': 'DnTrailPeriods', 'py': 'DnTrailPeriods', 'param': 'DnTrailPeriods', 'type': 'uint', 'default': 5, 'label': 'Период поиска для лоу', 'sinput': False}, {'mql': 'DnTrailShift', 'py': 'DnTrailShift', 'param': 'DnTrailShift', 'type': 'uint', 'default': 5, 'label': 'Период сдвига для хая', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
UpTrailPeriods = _input('UpTrailPeriods', 5)  # Период поиска для хая
UpTrailShift = _input('UpTrailShift', 5)  # Период сдвига для хая
DnTrailPeriods = _input('DnTrailPeriods', 5)  # Период поиска для лоу
DnTrailShift = _input('DnTrailShift', 5)  # Период сдвига для хая
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
ExtLineBuffer4 = Arr(0, 0.0)
ExtLineBuffer5 = Arr(0, 0.0)
ExtLineBuffer6 = Arr(0, 0.0)
ExtLineBuffer7 = Arr(0, 0.0)
ExtLineBuffer8 = Arr(0, 0.0)
ExtLineBuffer9 = Arr(0, 0.0)
Symbol_ = ""
Word = ""
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора CandleStop_System не может быть меньше периода текущего графика')
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'CandleStop_System', UpTrailPeriods, UpTrailShift, DnTrailPeriods, DnTrailShift)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора CandleStop_System')
        return INIT_FAILED
    SetIndexBuffer(0, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ExtLineBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLineBuffer3, INDICATOR_DATA)
    SetIndexBuffer(3, ExtLineBuffer4, INDICATOR_DATA)
    SetIndexBuffer(4, ExtLineBuffer5, INDICATOR_DATA)
    SetIndexBuffer(5, ExtLineBuffer6, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLineBuffer7, INDICATOR_DATA)
    SetIndexBuffer(7, ExtLineBuffer8, INDICATOR_DATA)
    SetIndexBuffer(8, ExtLineBuffer9, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(ExtLineBuffer1, True)
    ArraySetAsSeries(ExtLineBuffer2, True)
    ArraySetAsSeries(ExtLineBuffer3, True)
    ArraySetAsSeries(ExtLineBuffer4, True)
    ArraySetAsSeries(ExtLineBuffer5, True)
    ArraySetAsSeries(ExtLineBuffer6, True)
    ArraySetAsSeries(ExtLineBuffer7, True)
    ArraySetAsSeries(ExtLineBuffer8, True)
    ArraySetAsSeries(ExtLineBuffer9, True)
    shortname = Box("")
    StringConcatenate(shortname, 'CandleStop_System(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, ExtLineBuffer1, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(1, "", TimeFrame, Ind_Handle, 1, ExtLineBuffer2, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(2, "", TimeFrame, Ind_Handle, 2, ExtLineBuffer3, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(3, "", TimeFrame, Ind_Handle, 3, ExtLineBuffer4, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(4, "", TimeFrame, Ind_Handle, 8, ExtLineBuffer9, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicatorBar("", TimeFrame, Ind_Handle, 4, ExtLineBuffer5, 5, ExtLineBuffer6, 6, ExtLineBuffer7, 7, ExtLineBuffer8, time, open, high, low, close, rates_total, prev_calculated, min_rates_total):
        return 0
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

def CountIndicatorBar(Symb, TFrame, IndHandle, OHBuffNumb, OIndBuf, HBuffNumb, HIndBuf, LBuffNumb, LIndBuf, CBuffNumb, CIndBuf, Time, Open, High, Low, Close, Rates_Total, Prev_Calculated, Min_Rates_Total):
    global _s_CountIndicatorBar_LastCountBar
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicatorBar_LastCountBar = limit
    else:
        limit = _s_CountIndicatorBar_LastCountBar + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        CIndBuf[bar] = 0.0
        LIndBuf[bar] = CIndBuf[bar]
        HIndBuf[bar] = LIndBuf[bar]
        OIndBuf[bar] = HIndBuf[bar]
        if CopyTime(Symbol_, TimeFrame, _DT(Time[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if Time[bar] >= IndTime[0] and Time[bar + 1] < IndTime[0]:
            _s_CountIndicatorBar_LastCountBar = bar
            HArr = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, HBuffNumb, _DT(Time[bar]), 1, HArr) <= 0:
                return (0 != 0)
            if HArr[0]:
                OIndBuf[bar] = Open[bar]
                LIndBuf[bar] = Low[bar]
                HIndBuf[bar] = High[bar]
                CIndBuf[bar] = Close[bar]
        elif OIndBuf[bar + 1]:
            OIndBuf[bar] = Open[bar]
            LIndBuf[bar] = Low[bar]
            HIndBuf[bar] = High[bar]
            CIndBuf[bar] = Close[bar]
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(5, 0, dyn=False)
_s_CountIndicatorBar_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleStopSystemHTF(_MQL5Indicator):
    name = 'CandleStop_System_HTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'UpTrailPeriods': 5,  # Период поиска для хая
        'UpTrailShift': 5,  # Период сдвига для хая
        'DnTrailPeriods': 5,  # Период поиска для лоу
        'DnTrailShift': 5,  # Период сдвига для хая
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

