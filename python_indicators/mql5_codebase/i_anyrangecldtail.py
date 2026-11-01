"""i-AnyRangeCldTail — converted from MQL5: MQL5 Indicators/i-AnyRangeCldTail/i-AnyRangeCldTail.mq5

Индикатор диапазонов произвольных временных интервалов
Copyright: Copyright © 2006, Ким Игорь В. aka KimIV; Link: http://www.kimiv.ru; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Ким Игорь В. aka KimIV', 'link': 'http://www.kimiv.ru', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 6}, 'types': {1: 7, 2: 1, 3: 1, 4: 7, 5: 1, 6: 1}, 'colors': {1: [16443110], 2: [16711680], 3: [255], 4: [16118015], 5: [16711680], 6: [255]}, 'widths': {2: 3, 3: 3, 5: 1, 6: 1}, 'styles': {1: 0, 3: 0, 5: 4, 6: 4}, 'labels': {1: 'i-AnyRange', 2: 'Upper Zone', 3: 'Lower Zone', 4: 'i-AnyRange tail', 5: 'Upper Zone  tail', 6: 'Lower Zone  tail'}, 'levels': [], 'description': ['Индикатор диапазонов произвольных временных интервалов'], 'name': 'i-AnyRangeCldTail', 'source': 'MQL5 Indicators/i-AnyRangeCldTail/i-AnyRangeCldTail.mq5', 'folder': 'i-AnyRangeCldTail', 'inputs': [{'mql': 'Time1', 'py': 'Time1', 'param': None, 'type': 'string', 'default': '02:00', 'label': 'Временная точка 1', 'sinput': False}, {'mql': 'Time2', 'py': 'Time2', 'param': None, 'type': 'string', 'default': '07:00', 'label': 'Временная точка 2', 'sinput': False}, {'mql': 'nDays', 'py': 'nDays', 'param': 'nDays', 'type': 'uint', 'default': 8, 'label': 'Количество дней обсчёта (0-все)', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Time1 = _input('Time1', '02:00')  # Временная точка 1
Time2 = _input('Time2', '07:00')  # Временная точка 2
nDays = _input('nDays', 8)  # Количество дней обсчёта (0-все)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
Up0Buffer = Arr(0, 0.0)
Dn0Buffer = Arr(0, 0.0)
Up1Buffer = Arr(0, 0.0)
Dn1Buffer = Arr(0, 0.0)
Up2Buffer = Arr(0, 0.0)
Dn2Buffer = Arr(0, 0.0)
Up3Buffer = Arr(0, 0.0)
Dn3Buffer = Arr(0, 0.0)
min_rates_total = 0
Max = 0

def OnInit():
    global Max, min_rates_total
    min_rates_total = _int(_idiv(24 * 60 * 60 * nDays, PeriodSeconds()) + 1)
    Max = _int(_idiv(nDays * 1440 * 60, PeriodSeconds()))
    SetIndexBuffer(0, Up0Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Up0Buffer, True)
    SetIndexBuffer(1, Dn0Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Dn0Buffer, True)
    SetIndexBuffer(2, Up1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Up1Buffer, True)
    SetIndexBuffer(3, Dn1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Dn1Buffer, True)
    SetIndexBuffer(4, Up2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Up2Buffer, True)
    SetIndexBuffer(5, Dn2Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Dn2Buffer, True)
    SetIndexBuffer(6, Up3Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Up3Buffer, True)
    SetIndexBuffer(7, Dn3Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Dn3Buffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'i-AnyRangeCldTail(', Time1, ', ', Time2, ', ', nDays, ')')
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
        Comment('Индикатору i-AnyRange нужен ТФ младше H4!')
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
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, rates_total - limit)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, rates_total - limit)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, rates_total - limit)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, rates_total - limit)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, rates_total - limit)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, rates_total - limit)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(time, True)
    bar = 0
    for bar in range(bar, limit):
        Up0Buffer[bar] = 0.0
        Dn0Buffer[bar] = 0.0
        Up1Buffer[bar] = EMPTY_VALUE
        Dn1Buffer[bar] = EMPTY_VALUE
    else:
        bar = _range_end(bar, limit, 1)
    bar = 0
    for bar in range(bar, limit):
        Up1Buffer[bar] = EMPTY_VALUE
        Dn1Buffer[bar] = EMPTY_VALUE
        tm = MqlDateTime()
        TimeToStruct(time[bar], tm)
        if nd != tm.day:
            nd = tm.day
            kd += 1
            if kd > _int(nDays) and nDays:
                break
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
            Up1Buffer[bar] = up
            Dn1Buffer[bar] = dn
            Up0Buffer[bar] = up
            Dn0Buffer[bar] = dn
        else:
            Up1Buffer[bar] = EMPTY_VALUE
            Dn1Buffer[bar] = EMPTY_VALUE
    else:
        bar = _range_end(bar, limit, 1)
    bar = 0
    for bar in range(bar, limit):
        if Up1Buffer[bar] == EMPTY_VALUE and Dn1Buffer[bar] == EMPTY_VALUE:
            Up0Buffer[bar] = 0.0
            Dn0Buffer[bar] = 0.0
    else:
        bar = _range_end(bar, limit, 1)
    dn = EMPTY_VALUE
    up = dn
    bar = limit - 1
    for bar in range(bar, 0 - 1, -1):
        Up2Buffer[bar] = 0.0
        Dn2Buffer[bar] = 0.0
        Up3Buffer[bar] = EMPTY_VALUE
        Dn3Buffer[bar] = EMPTY_VALUE
        if Up0Buffer[bar]:
            up = Up0Buffer[bar]
            dn = Dn0Buffer[bar]
        else:
            Up3Buffer[bar] = up
            Up2Buffer[bar] = Up3Buffer[bar]
            Dn3Buffer[bar] = dn
            Dn2Buffer[bar] = Dn3Buffer[bar]
            bar1 = bar + 1
            if Up0Buffer[bar1]:
                Up3Buffer[bar1] = up
                Up2Buffer[bar1] = Up3Buffer[bar1]
                Dn3Buffer[bar1] = dn
                Dn2Buffer[bar1] = Dn3Buffer[bar1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IAnyRangeCldTail(_MQL5Indicator):
    name = 'i-AnyRangeCldTail'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'nDays': 8,  # Количество дней обсчёта (0-все)
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

