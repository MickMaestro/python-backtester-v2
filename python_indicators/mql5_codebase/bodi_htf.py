"""BoDi_HTF — converted from MQL5: MQL5 Indicators/BoDi_HTF/BoDi_HTF.mq5

Copyright: Copyright © 2014, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [9639167, 8421504, 16748574]}, 'widths': {1: 5}, 'styles': {1: 0}, 'labels': {1: 'BoDi HTF'}, 'levels': [], 'description': [], 'name': 'BoDi_HTF', 'source': 'MQL5 Indicators/BoDi_HTF/BoDi_HTF.mq5', 'folder': 'BoDi_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'BBPeriod', 'py': 'BBPeriod', 'param': 'BBPeriod', 'type': 'uint', 'default': 20, 'label': 'Период для расчета средней линии', 'sinput': False}, {'mql': 'StdDeviation', 'py': 'StdDeviation', 'param': 'StdDeviation', 'type': 'double', 'default': 2.0, 'label': 'Кол-во отклонений', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 1, 'label': 'Тип цены', 'sinput': False}, {'mql': 'ReDraw', 'py': 'ReDraw', 'param': 'ReDraw', 'type': 'bool', 'default': True, 'label': 'Повтор отображения инфомации на пустых барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
BBPeriod = _input('BBPeriod', 20)  # Период для расчета средней линии
StdDeviation = _input('StdDeviation', 2.0)  # Кол-во отклонений
applied_price = _input('applied_price', PRICE_CLOSE)  # Тип цены
ReDraw = _input('ReDraw', True)  # Повтор отображения инфомации на пустых барах
min_rates_total = 0
BoDi_Handle = 0
BoDiBuffer = Arr(0, 0.0)
ColorBoDiBuffer = Arr(0, 0.0)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global BoDi_Handle, min_rates_total
    min_rates_total = 3
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора BoDi не может быть меньше периода текущего графика')
        return INIT_FAILED
    BoDi_Handle = iCustom(Symbol(), TimeFrame, 'BoDi', BBPeriod, StdDeviation, applied_price)
    if BoDi_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора BoDi')
        return INIT_FAILED
    SetIndexBuffer(0, BoDiBuffer, INDICATOR_DATA)
    ArraySetAsSeries(BoDiBuffer, True)
    SetIndexBuffer(1, ColorBoDiBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorBoDiBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'BoDi HTF( ', GetStringTimeframe(TimeFrame), ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(BoDi_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    limit = 0
    bar = 0
    BoDi = Arr(1, 0.0, dyn=False)
    Col = Arr(1, 0.0, dyn=False)
    BoDiTime = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BoDiBuffer[bar] = EMPTY_VALUE
        ColorBoDiBuffer[bar] = 1.0
        if CopyTime(Symbol(), TimeFrame, _DT(time[bar]), 1, BoDiTime) <= 0:
            return 0
        if time[bar] >= BoDiTime[0] and time[bar + 1] < BoDiTime[0]:
            _s_OnCalculate_LastCountBar = bar
            if CopyBuffer(BoDi_Handle, 0, _DT(time[bar]), 1, BoDi) <= 0:
                return 0
            if CopyBuffer(BoDi_Handle, 1, _DT(time[bar]), 1, Col) <= 0:
                return 0
            BoDiBuffer[bar] = BoDi[0]
            ColorBoDiBuffer[bar] = Col[0]
        if ReDraw:
            if BoDiBuffer[bar + 1] != EMPTY_VALUE and BoDiBuffer[bar] == EMPTY_VALUE:
                BoDiBuffer[bar] = BoDiBuffer[bar + 1]
                ColorBoDiBuffer[bar] = ColorBoDiBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BoDiHTF(_MQL5Indicator):
    name = 'BoDi_HTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'BBPeriod': 20,  # Период для расчета средней линии
        'StdDeviation': 2.0,  # Кол-во отклонений
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Тип цены
        'ReDraw': True,  # Повтор отображения инфомации на пустых барах
    }

