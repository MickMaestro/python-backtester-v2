"""JBrainTrend1_HTF — converted from MQL5: MQL5 Indicators/JBrainTrend1_HTF/JBrainTrend1_HTF.mq5

Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [4294967295, 14662143, 16763799]}, 'widths': {}, 'styles': {}, 'labels': {1: 'JBrainTrend1_Open;JBrainTrend1_High;JBrainTrend1_Low;JBrainTrend1_Close'}, 'levels': [], 'description': [], 'name': 'JBrainTrend1_HTF', 'source': 'MQL5 Indicators/JBrainTrend1_HTF/JBrainTrend1_HTF.mq5', 'folder': 'JBrainTrend1_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'ATR_Period', 'py': 'ATR_Period', 'param': 'ATR_Period', 'type': 'uint', 'default': 7, 'label': 'период ATR', 'sinput': False}, {'mql': 'STO_Period', 'py': 'STO_Period', 'param': 'STO_Period', 'type': 'uint', 'default': 9, 'label': 'период стохастика', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 0, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'STO_Price', 'py': 'STO_Price', 'param': 'STO_Price', 'type': 'int', 'default': 0, 'label': 'метод расчёта цен', 'sinput': False}, {'mql': 'Length_', 'py': 'Length_', 'param': 'Length_', 'type': 'int', 'default': 7, 'label': 'глубина JMA сглаживания', 'sinput': False}, {'mql': 'Phase_', 'py': 'Phase_', 'param': 'Phase_', 'type': 'int', 'default': 100, 'label': 'параметр JMA сглаживания,', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
ATR_Period = _input('ATR_Period', 7)  # период ATR
STO_Period = _input('STO_Period', 9)  # период стохастика
MA_Method = _input('MA_Method', MODE_SMA)  # метод усреднения
STO_Price = _input('STO_Price', STO_LOWHIGH)  # метод расчёта цен
Length_ = _input('Length_', 7)  # глубина JMA сглаживания
Phase_ = _input('Phase_', 100)  # параметр JMA сглаживания,
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    min_rates_total = 2
    short_name = 'JBrainTrend1' + ' ' + Symbol() + '(' + GetStringTimeframe(Period()) + ')'
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'JBrainTrend1', ATR_Period, STO_Period, MA_Method, STO_Price, Length_, Phase_)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора JBrainTrend1')
        return INIT_FAILED
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicatorBar("", TimeFrame, Ind_Handle, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def CountIndicatorBar(Symb, TFrame, IndHandle, Time, Rates_Total, Prev_Calculated, Min_Rates_Total):
    global _s_CountIndicatorBar_LastCountBar
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicatorBar_LastCountBar = limit
    else:
        limit = _s_CountIndicatorBar_LastCountBar + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        if CopyTime(Symbol(), TimeFrame, _DT(Time[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if Time[bar] >= IndTime[0] and Time[bar + 1] < IndTime[0]:
            _s_CountIndicatorBar_LastCountBar = bar
            Col = Arr(1, 0.0, dyn=False)
            O = Arr(1, 0.0, dyn=False)
            H = Arr(1, 0.0, dyn=False)
            L = Arr(1, 0.0, dyn=False)
            C = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, 4, _DT(Time[bar]), 1, Col) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, 0, _DT(Time[bar]), 1, O) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, 1, _DT(Time[bar]), 1, H) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, 2, _DT(Time[bar]), 1, L) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, 3, _DT(Time[bar]), 1, C) <= 0:
                return (0 != 0)
            ExtColorBuffer[bar] = Col[0]
            ExtOpenBuffer[bar] = O[0]
            ExtLowBuffer[bar] = L[0]
            ExtHighBuffer[bar] = H[0]
            ExtCloseBuffer[bar] = C[0]
        else:
            ExtColorBuffer[bar] = ExtColorBuffer[bar + 1]
            ExtOpenBuffer[bar] = ExtOpenBuffer[bar + 1]
            ExtLowBuffer[bar] = ExtLowBuffer[bar + 1]
            ExtHighBuffer[bar] = ExtHighBuffer[bar + 1]
            ExtCloseBuffer[bar] = ExtCloseBuffer[bar + 1]
    return True

# ---- static local variables
_s_CountIndicatorBar_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class JBrainTrend1HTF(_MQL5Indicator):
    name = 'JBrainTrend1_HTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'ATR_Period': 7,  # период ATR
        'STO_Period': 9,  # период стохастика
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # метод усреднения
        'STO_Price': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # метод расчёта цен
        'Length_': 7,  # глубина JMA сглаживания
        'Phase_': 100,  # параметр JMA сглаживания,
    }

