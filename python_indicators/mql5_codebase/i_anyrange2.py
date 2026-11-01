"""i-anyrange2 — converted from MQL5: MQL5 Indicators/i-AnyRange2/i-anyrange2.mq5

Indicator of two ranges of arbitrary time intervals.
Copyright: Copyright © 2006, Kim Igor V. aka KimIV; Link: http://www.kimiv.ru; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Kim Igor V. aka KimIV', 'link': 'http://www.kimiv.ru', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [16711680], 2: [255], 3: [65280], 4: [16711935]}, 'widths': {1: 3, 2: 3, 3: 3, 4: 3}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Upper Zone 1', 2: 'Lower Zone 1', 3: 'Upper Zone 2', 4: 'Lower Zone 2'}, 'levels': [], 'description': ['Indicator of two ranges of arbitrary time intervals.'], 'name': 'i-anyrange2', 'source': 'MQL5 Indicators/i-AnyRange2/i-anyrange2.mq5', 'folder': 'i-AnyRange2', 'inputs': [{'mql': 'Start1', 'py': 'Start1', 'param': None, 'type': 'string', 'default': '03:00', 'label': 'origin of 1', 'sinput': False}, {'mql': 'End1', 'py': 'End1', 'param': None, 'type': 'string', 'default': '08:00', 'label': 'end of 1', 'sinput': False}, {'mql': 'Start2', 'py': 'Start2', 'param': None, 'type': 'string', 'default': '12:00', 'label': 'origin of 2', 'sinput': False}, {'mql': 'End2', 'py': 'End2', 'param': None, 'type': 'string', 'default': '17:00', 'label': 'end of 2', 'sinput': False}, {'mql': 'nDays', 'py': 'nDays', 'param': 'nDays', 'type': 'uint', 'default': 2, 'label': 'number of counting days (0-all)', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Start1 = _input('Start1', '03:00')  # origin of 1
End1 = _input('End1', '08:00')  # end of 1
Start2 = _input('Start2', '12:00')  # origin of 2
End2 = _input('End2', '17:00')  # end of 2
nDays = _input('nDays', 2)  # number of counting days (0-all)
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
Up1Buffer = Arr(0, 0.0)
Dn1Buffer = Arr(0, 0.0)
Up2Buffer = Arr(0, 0.0)
Dn2Buffer = Arr(0, 0.0)
min_rates_total = 0
Max = 0

def OnInit():
    global Max, min_rates_total
    min_rates_total = _int(_idiv(24 * 60 * 60 * nDays, PeriodSeconds()) + 1)
    Max = _int(_idiv(nDays * 1440 * 60, PeriodSeconds()))
    SetIndexBuffer(0, Up1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Up1Buffer, True)
    SetIndexBuffer(1, Dn1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Dn1Buffer, True)
    SetIndexBuffer(2, Up2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Up2Buffer, True)
    SetIndexBuffer(3, Dn2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Dn2Buffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'i-AnyRange2(', Start1, ', ', End1, ', ', Start2, ', ', End2, ', ', nDays, ', ', Shift, ')')
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
    if Period() > PERIOD_H1:
        Comment('Indicator i-AnyRange is required timeframe under H2!')
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
    rates_10 = 0
    sdt = ""
    rates_10 = rates_total - 10
    if nDays == 0:
        limit = rates_10
    else:
        limit = Max
    limit = MathMin(rates_10, limit)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    kd = 0
    bar = 0
    for bar in range(bar, limit):
        tm = MqlDateTime()
        TimeToStruct(time[bar], tm)
        if nd != tm.day:
            nd = tm.day
            kd += 1
            if kd > _int(nDays) and nDays:
                break
            sdt = TimeToString(time[bar], TIME_DATE)
            nb1 = iBarShift_u("", 0, StringToTime(sdt + ' ' + Start1))
            nb2 = iBarShift_u("", 0, StringToTime(sdt + ' ' + End1))
            if nb1 > (nb2 + 1):
                up = high[ArrayMaximum(high, nb2 + 1, nb1 - nb2)]
                dn = low[ArrayMinimum(low, nb2 + 1, nb1 - nb2)]
            if nb2 > (nb1 + 1):
                up = high[ArrayMaximum(high, nb1 + 1, nb2 - nb1)]
                dn = low[ArrayMinimum(low, nb1 + 1, nb2 - nb1)]
        if (nb1 >= bar and bar > nb2) or (nb2 >= bar and bar > nb1):
            Up1Buffer[bar] = up
            Dn1Buffer[bar] = dn
        else:
            Up1Buffer[bar] = EMPTY_VALUE
            Dn1Buffer[bar] = EMPTY_VALUE
    else:
        bar = _range_end(bar, limit, 1)
    kd = 0
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
            nb1 = iBarShift_u("", 0, StringToTime(sdt + ' ' + Start2))
            nb2 = iBarShift_u("", 0, StringToTime(sdt + ' ' + End2))
            if nb1 > (nb2 + 1):
                up = high[ArrayMaximum(high, nb2 + 1, nb1 - nb2)]
                dn = low[ArrayMinimum(low, nb2 + 1, nb1 - nb2)]
            if nb2 > (nb1 + 1):
                up = high[ArrayMaximum(high, nb1 + 1, nb2 - nb1)]
                dn = low[ArrayMinimum(low, nb1 + 1, nb2 - nb1)]
        if (nb1 >= bar and bar > nb2) or (nb2 >= bar and bar > nb1):
            Up2Buffer[bar] = up
            Dn2Buffer[bar] = dn
        else:
            Up2Buffer[bar] = EMPTY_VALUE
            Dn2Buffer[bar] = EMPTY_VALUE
    else:
        bar = _range_end(bar, limit, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IAnyrange2(_MQL5Indicator):
    name = 'i-anyrange2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'nDays': 2,  # number of counting days (0-all)
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

