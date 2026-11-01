"""i-anyrange — converted from MQL5: MQL5 Indicators/i-AnyRange/i-anyrange.mq5

Indicator of ranges of arbitrary time intervals.
Copyright: Copyright © 2006, Kim Igor V. aka KimIV; Link: http://www.kimiv.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Kim Igor V. aka KimIV', 'link': 'http://www.kimiv.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 3, 2: 3}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Up i-AnyRange', 2: 'Down i-AnyRange'}, 'levels': [], 'description': ['Indicator of ranges of arbitrary time intervals.'], 'name': 'i-anyrange', 'source': 'MQL5 Indicators/i-AnyRange/i-anyrange.mq5', 'folder': 'i-AnyRange', 'inputs': [{'mql': 'Time1', 'py': 'Time1', 'param': None, 'type': 'string', 'default': '02:00', 'label': 'Temporary point 1', 'sinput': False}, {'mql': 'Time2', 'py': 'Time2', 'param': None, 'type': 'string', 'default': '07:00', 'label': 'Temporary point 2', 'sinput': False}, {'mql': 'nDays', 'py': 'nDays', 'param': 'nDays', 'type': 'uint', 'default': 2, 'label': 'Number of days for calculation (0-all)', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Time1 = _input('Time1', '02:00')  # Temporary point 1
Time2 = _input('Time2', '07:00')  # Temporary point 2
nDays = _input('nDays', 2)  # Number of days for calculation (0-all)
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(_idiv(24 * 60 * 60 * nDays, PeriodSeconds()) + 1)
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(DnBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'i-AnyRange(', Time1, ', ', Time2, ', ', nDays, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnDeinit(reason):
    Comment('')

def iBarShift_u(symbol, timeframe, time):
    if time < 0:
        return -1
    Arr_ = Arr(0, 0)
    time1 = 0
    time1 = SeriesInfoInteger(symbol, timeframe, SERIES_LASTBAR_DATE)
    if time >= time1:
        return 0
    if CopyTime(symbol, timeframe, _DT(time), _DT(time1), Arr_) > 0:
        size = ArraySize(Arr_)
        return size - 1
    else:
        return -1

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_RecountPoint
    if Period() > PERIOD_H1:
        Comment('Indicator i-AnyRange is required timeframe under H4!')
        return 0
    else:
        Comment('')
    if rates_total < min_rates_total:
        return 0
    up = 0.0
    dn = 0.0
    bar = 0
    limit = 0
    kd = 0
    nb1 = 0
    nb2 = 0
    nd = 0
    sdt = ""
    if nDays == 0:
        limit = rates_total - 10
    else:
        limit = _int(_idiv(nDays * 1440 * 60, PeriodSeconds()))
    limit = MathMin(rates_total - 10, limit)
    if prev_calculated > rates_total or prev_calculated <= 0:
        _s_OnCalculate_RecountPoint = 0
    limit = _int(MathMin(_s_OnCalculate_RecountPoint + rates_total - prev_calculated, limit))
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    bar = 0
    for bar in range(bar, limit):
        tm = MqlDateTime()
        TimeToStruct(time[bar], tm)
        if nd != tm.day:
            nd = tm.day
            kd += 1
            if kd > _int(nDays) and nDays:
                return rates_total
            sdt = TimeToString(time[bar], TIME_DATE)
            nb1 = iBarShift_u("", 0, StringToTime(sdt + ' ' + Time1))
            nb2 = iBarShift_u("", 0, StringToTime(sdt + ' ' + Time2))
            if nb1 > (nb2 + 1):
                up = high[ArrayMaximum(high, nb2 + 1, nb1 - nb2)]
                dn = low[ArrayMinimum(low, nb2 + 1, nb1 - nb2)]
            if nb2 > (nb1 + 1):
                up = high[ArrayMaximum(high, nb1 + 1, nb2 - nb1)]
                dn = low[ArrayMinimum(low, nb1 + 1, nb2 - nb1)]
        if (nb1 >= bar and bar > nb2) or (nb2 >= bar and bar > nb1):
            UpBuffer[bar] = up
            DnBuffer[bar] = dn
        else:
            UpBuffer[bar] = EMPTY_VALUE
            DnBuffer[bar] = EMPTY_VALUE
        if UpBuffer[bar + 1] == EMPTY_VALUE and UpBuffer[bar] != EMPTY_VALUE:
            _s_OnCalculate_RecountPoint = bar
    else:
        bar = _range_end(bar, limit, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_RecountPoint = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IAnyrange(_MQL5Indicator):
    name = 'i-anyrange'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'nDays': 2,  # Number of days for calculation (0-all)
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

