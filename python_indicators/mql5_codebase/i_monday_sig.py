"""i-monday_sig — converted from MQL5: MQL5 Indicators/i-Monday_Sig/i-monday_sig.mq5

Entries and exits signals on the system Monday
Copyright: Copyright © 2005, Kim Igor V. aka KimIV; Link: http://www.kimiv.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Kim Igor V. aka KimIV', 'link': 'http://www.kimiv.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 3, 2: 3}, 'styles': {}, 'labels': {1: 'Up i-Monday_Sig', 2: 'Down i-Monday_Sig'}, 'levels': [], 'description': ['Entries and exits signals on the system Monday'], 'name': 'i-monday_sig', 'source': 'MQL5 Indicators/i-Monday_Sig/i-monday_sig.mq5', 'folder': 'i-Monday_Sig', 'inputs': [{'mql': 'HourOpenPos', 'py': 'HourOpenPos', 'param': 'HourOpenPos', 'type': 'int', 'default': 11, 'label': 'Time of opening of deal', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum HourOpen
H0 = 0
H1 = 1
H2 = 2
H3 = 3
H4 = 4
H5 = 5
H6 = 6
H7 = 7
H8 = 8
H9 = 9
H10 = 10
H11 = 11
H12 = 12
H13 = 13
H14 = 14
H15 = 15
H16 = 16
H17 = 17
H18 = 18
H19 = 19
H20 = 20
H21 = 21
H22 = 22
H23 = 23
_enum('HourOpen', {0: 'H0', 1: 'H1', 2: 'H2', 3: 'H3', 4: 'H4', 5: 'H5', 6: 'H6', 7: 'H7', 8: 'H8', 9: 'H9', 10: 'H10', 11: 'H11', 12: 'H12', 13: 'H13', 14: 'H14', 15: 'H15', 16: 'H16', 17: 'H17', 18: 'H18', 19: 'H19', 20: 'H20', 21: 'H21', 22: 'H22', 23: 'H23'})

# ---- inputs and global variables
HourOpenPos = _input('HourOpenPos', H11)  # Time of opening of deal
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _idiv(24 * 60 * 60 * 5, PeriodSeconds()) + 1
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_ARROW, 233)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_ARROW, 234)
    ArraySetAsSeries(DnBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'i-Monday_Sig(', HourOpenPos, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Period() > PERIOD_H1:
        Comment('The i-Monday_Sig indicator needs timeframe under H2!')
        return 0
    else:
        Comment('')
    if rates_total < min_rates_total:
        return 0
    iOpen_ = Arr(2, 0.0, dyn=False)
    bar = 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    bar = 0
    for bar in range(bar, limit):
        UpBuffer[bar] = EMPTY_VALUE
        DnBuffer[bar] = EMPTY_VALUE
        tm = MqlDateTime()
        TimeToStruct(time[bar], tm)
        if (tm.day == MONDAY and tm.hour == HourOpenPos) and tm.min == 0:
            AvgRange = 0.0
            for count in range(bar, bar + 9 + 1):
                AvgRange += MathAbs(high[count] - low[count])
            Range = AvgRange / 20
            if CopyOpen(Symbol(), PERIOD_D1, _DT(time[bar]), 2, iOpen_) <= 0:
                return 0
            if iOpen_[0] > close[bar]:
                UpBuffer[bar] = low[bar] - Range
            if iOpen_[0] < close[bar]:
                DnBuffer[bar] = high[bar] + Range
    else:
        bar = _range_end(bar, limit, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IMondaySig(_MQL5Indicator):
    name = 'i-monday_sig'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'HourOpenPos': _Choice({0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: '11', 12: '12', 13: '13', 14: '14', 15: '15', 16: '16', 17: '17', 18: '18', 19: '19', 20: '20', 21: '21', 22: '22', 23: '23'}, default=11),  # Time of opening of deal
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

