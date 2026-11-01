"""i-dayofweek — converted from MQL5: MQL5 Indicators/i-DayOfWeek/i-dayofweek.mq5

Copyright: Copyright © 2007, Kim Igor V. aka KimIV; Link: http://www.kimiv.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Kim Igor V. aka KimIV', 'link': 'http://www.kimiv.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16436871]}, 'widths': {}, 'styles': {}, 'labels': {1: 'i-DayOfWeek'}, 'levels': [], 'description': [], 'name': 'i-dayofweek', 'source': 'MQL5 Indicators/i-DayOfWeek/i-dayofweek.mq5', 'folder': 'i-DayOfWeek', 'inputs': [{'mql': 'NumberDayOfWeek', 'py': 'NumberDayOfWeek', 'param': 'NumberDayOfWeek', 'type': 'int', 'default': 5, 'label': 'Number for the day of the week', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum dayOfWeek
Sunday = 0
Monday = 1
Tuesday = 2
Wednesday = 3
Thursday = 4
Friday = 5
Saturday = 6
_enum('dayOfWeek', {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'})

# ---- inputs and global variables
NumberDayOfWeek = _input('NumberDayOfWeek', Friday)  # Number for the day of the week
min_rates_total = 0
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = 10
    SetIndexBuffer(0, ExtABuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtABuffer, True)
    SetIndexBuffer(1, ExtBBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtBBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetString(INDICATOR_SHORTNAME, 'i-DayOfWeek(' + EnumToString(NumberDayOfWeek, 'dayOfWeek') + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total:
        return 0
    limit = 0
    iHigh_ = Arr(1, 0.0, dyn=False)
    iLow_ = Arr(1, 0.0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = _s_OnCalculate_LastCountBar + rates_total - prev_calculated
    ArraySetAsSeries(Time, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    for bar in range(limit, 0 - 1, -1):
        tm0 = MqlDateTime()
        tm1 = MqlDateTime()
        TimeToStruct(Time[bar], tm0)
        TimeToStruct(Time[bar + 1], tm1)
        if tm0.day_of_week == NumberDayOfWeek:
            if CopyLow(Symbol(), PERIOD_D1, _DT(Time[bar]), 1, iLow_) <= 0:
                return 0
            if CopyHigh(Symbol(), PERIOD_D1, _DT(Time[bar]), 1, iHigh_) <= 0:
                return 0
            if tm1.day_of_week != NumberDayOfWeek:
                _s_OnCalculate_LastCountBar = bar
            ExtABuffer[bar] = iHigh_[0]
            ExtBBuffer[bar] = iLow_[0]
        else:
            ExtABuffer[bar] = 0.0
            ExtBBuffer[bar] = 0.0
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IDayofweek(_MQL5Indicator):
    name = 'i-dayofweek'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'NumberDayOfWeek': _Choice({0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}, default=5),  # Number for the day of the week
    }

