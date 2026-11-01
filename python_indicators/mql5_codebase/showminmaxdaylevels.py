"""showminmaxdaylevels — converted from MQL5: MQL5 Indicators/ShowMinMaxDayLevels/showminmaxdaylevels.mq5

Copyright: Copyright © 2012, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 3, 2: 3}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'MaxDayLevel', 2: 'MinDayLevel'}, 'levels': [], 'description': [], 'name': 'showminmaxdaylevels', 'source': 'MQL5 Indicators/ShowMinMaxDayLevels/showminmaxdaylevels.mq5', 'folder': 'ShowMinMaxDayLevels', 'inputs': [{'mql': 'DayShift', 'py': 'DayShift', 'param': 'DayShift', 'type': 'uint', 'default': 0, 'label': 'shift of counting start in days', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
DayShift = _input('DayShift', 0)  # shift of counting start in days
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
MaxBuffer = Arr(0, 0.0)
MinBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(3 + _idiv(DayShift * PeriodSeconds(PERIOD_D1), PeriodSeconds()))
    SetIndexBuffer(0, MaxBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(MaxBuffer, True)
    SetIndexBuffer(1, MinBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(MinBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'ShowMinMaxDayLevels( Shift = ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total or Period() > PERIOD_H12:
        return 0
    limit = 0
    bar = 0
    DHigh = Arr(1, 0.0, dyn=False)
    DLow = Arr(1, 0.0, dyn=False)
    DTime = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        _s_OnCalculate_LastCountBar = bar
        MaxBuffer[bar] = EMPTY_VALUE
        MinBuffer[bar] = EMPTY_VALUE
        if CopyTime(Symbol(), PERIOD_D1, _DT(time[bar]), 1, DTime) <= 0:
            return 0
        if time[bar] >= DTime[0] and time[bar + 1] < DTime[0]:
            if CopyHigh(Symbol(), PERIOD_D1, _DT(time[bar + DayShift]), 1, DHigh) <= 0:
                return 0
            if CopyLow(Symbol(), PERIOD_D1, _DT(time[bar + DayShift]), 1, DLow) <= 0:
                return 0
            MaxBuffer[bar] = DHigh[0]
            MinBuffer[bar] = DLow[0]
        if MaxBuffer[bar + 1] != EMPTY_VALUE and MaxBuffer[bar] == EMPTY_VALUE:
            MaxBuffer[bar] = MaxBuffer[bar + 1]
            MinBuffer[bar] = MinBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Showminmaxdaylevels(_MQL5Indicator):
    name = 'showminmaxdaylevels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'DayShift': 0,  # shift of counting start in days
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

