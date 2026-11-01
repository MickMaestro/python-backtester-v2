"""Hans_Indicator_x4 — converted from MQL5: MQL5 Indicators/Hans_Indicator_x4/Hans_Indicator_x4.mq5

Индикатор расширяющихся коридоров временных зон с двумя коридорами. Сформированный коридор равен четырём часам, расширения коридора - шестнадцать часов.
Copyright: Copyright © 2014, Shimodax; Link: http://www.strategybuilderfx.com/forums/showthread.php?t=15439; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, Shimodax', 'link': 'http://www.strategybuilderfx.com/forums/showthread.php?t=15439', 'version': '1.02', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [16711680], 2: [16711935], 3: [65280], 4: [255], 5: [32768], 6: [8519755]}, 'widths': {1: 1, 2: 1, 3: 3, 4: 3, 5: 3, 6: 3}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'Upper Hans_Indicator 1', 2: 'Lower Hans_Indicator 1', 3: 'Upper Hans_Indicator 2', 4: 'Lower Hans_Indicator 2', 5: 'Upper Hans_Indicator 3', 6: 'Lower Hans_Indicator 3'}, 'levels': [], 'description': ['Индикатор расширяющихся коридоров временных зон с двумя коридорами. Сформированный коридор равен четырём часам, расширения коридора - шестнадцать часов.'], 'name': 'Hans_Indicator_x4', 'source': 'MQL5 Indicators/Hans_Indicator_x4/Hans_Indicator_x4.mq5', 'folder': 'Hans_Indicator_x4', 'inputs': [{'mql': 'LocalTimeZone', 'py': 'LocalTimeZone', 'param': 'LocalTimeZone', 'type': 'uint', 'default': 0, 'label': 'час начала отсчёта исходного коридора', 'sinput': False}, {'mql': 'DestTimeZone', 'py': 'DestTimeZone', 'param': 'DestTimeZone', 'type': 'uint', 'default': 4, 'label': 'сдвиг коридора влево в барах', 'sinput': False}, {'mql': 'PipsForEntry1', 'py': 'PipsForEntry1', 'param': 'PipsForEntry1', 'type': 'uint', 'default': 100, 'label': 'расширение границ первого сформированного коридора в пунктах', 'sinput': False}, {'mql': 'PipsForEntry2', 'py': 'PipsForEntry2', 'param': 'PipsForEntry2', 'type': 'uint', 'default': 200, 'label': 'расширение границ второго сформированного коридора в пунктах', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
LocalTimeZone = _input('LocalTimeZone', 0)  # час начала отсчёта исходного коридора
DestTimeZone = _input('DestTimeZone', 4)  # сдвиг коридора влево в барах
PipsForEntry1 = _input('PipsForEntry1', 100)  # расширение границ первого сформированного коридора в пунктах
PipsForEntry2 = _input('PipsForEntry2', 200)  # расширение границ второго сформированного коридора в пунктах
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
min_rates_total = 0
Zone1Upper = Arr(0, 0.0)
Zone2Upper = Arr(0, 0.0)
Zone3Upper = Arr(0, 0.0)
Zone1Lower = Arr(0, 0.0)
Zone2Lower = Arr(0, 0.0)
Zone3Lower = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = 100
    SetIndexBuffer(0, Zone1Upper, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(Zone1Upper, True)
    SetIndexBuffer(1, Zone1Lower, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(Zone1Lower, True)
    SetIndexBuffer(2, Zone2Upper, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(Zone2Upper, True)
    SetIndexBuffer(3, Zone2Lower, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(Zone2Lower, True)
    SetIndexBuffer(4, Zone3Upper, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(Zone3Upper, True)
    SetIndexBuffer(5, Zone3Lower, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(5, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(5, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(Zone3Lower, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Hans_Indicator_x4(' + _str(LocalTimeZone) + ',' + _str(DestTimeZone) + ',' + _str(PipsForEntry1) + ',' + _str(PipsForEntry2) + ',' + _str(Shift) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if rates_total < min_rates_total:
        return 0
    limit = Box(0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit.v = rates_total - min_rates_total - 1
    else:
        limit.v = rates_total - prev_calculated
    ArraySetAsSeries(Time, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    BreakoutRanges(0, limit, LocalTimeZone, DestTimeZone, rates_total, Time, High, Low)
    return rates_total

def BreakoutRanges(offset, lastbar, tzlocal, tzdest, rates_total_, Time_, High_, Low_):
    i = 0
    j = 0
    k = 0
    tzdiff = tzlocal - tzdest
    tzdiffsec = tzdiff * 3600
    tidxstart = Arr.of([0, 0], fill=0, dyn=False, size=2)
    tidxend = Arr.of([0, 0], fill=0, dyn=False, size=2)
    thigh = Arr.of([0.0, 0.0], fill=0.0, dyn=False, size=2)
    tlow = Arr.of([DBL_MAX], fill=0.0, dyn=False, size=2)
    tfrom = Arr.of(['04:00', '08:00', '12:00'], fill="", dyn=False, size=3)
    tto = Arr.of(['08:00', '12:00', '24:00'], fill="", dyn=False, size=3)
    tday = ""
    inperiod = (-1 != 0)
    timet = 0
    tday = TimeToString(Time_[lastbar.v] - tzdiffsec, TIME_DATE)
    while lastbar.v < (rates_total_ - 1):
        if TimeToString(Time_[lastbar.v] - tzdiffsec, TIME_DATE) != tday:
            lastbar.v -= 1
            break
        lastbar.v += 1
    tday = 'XXX'
    i = lastbar.v
    for i in range(i, offset - 1, -1):
        timet = Time_[i] - tzdiffsec
        timestr = TimeToString(timet, TIME_MINUTES)
        thisday = TimeToString(timet, TIME_DATE)
        j = 0
        for j in range(j, 2):
            if tfrom[j] <= timestr and timestr < tto[j]:
                if inperiod != j:
                    if j > 0:
                        k = tidxstart[j - 1]
                        while k >= tidxend[j - 1]:
                            if (j - 1) == 0:
                                Zone1Upper[k] = thigh[j - 1]
                                Zone1Lower[k] = tlow[j - 1]
                            if (j - 1) == 1:
                                Zone2Upper[k] = thigh[j - 1]
                                Zone2Lower[k] = tlow[j - 1]
                            k -= 1
                    inperiod = (j != 0)
                if inperiod == 2:
                    break
                if tidxstart[j] == 0:
                    tidxstart[j] = i
                    tday = thisday
                tidxend[j] = i
                thigh[j] = MathMax(thigh[j], High_[i])
                tlow[j] = MathMin(tlow[j], Low_[i])
        else:
            j = _range_end(j, 2, 1)
        if inperiod >= 1 and tday == thisday:
            Zone1Upper[i] = thigh[0] + (PipsForEntry1 * Point())
            Zone1Lower[i] = tlow[0] - (PipsForEntry1 * Point())
            Zone2Upper[i] = thigh[0] + (PipsForEntry1 * Point())
            Zone2Lower[i] = tlow[0] - (PipsForEntry1 * Point())
            Zone3Upper[i] = thigh[0] + (PipsForEntry2 * Point())
            Zone3Lower[i] = tlow[0] - (PipsForEntry2 * Point())
        else:
            Zone3Lower[i] = 0.0
            Zone3Upper[i] = Zone3Lower[i]
            Zone2Lower[i] = Zone3Upper[i]
            Zone2Upper[i] = Zone2Lower[i]
            Zone1Lower[i] = Zone2Upper[i]
            Zone1Upper[i] = Zone1Lower[i]
        if tday != 'XXX' and tday != thisday:
            tday = 'XXX'
            inperiod = (-1 != 0)
            j = 0
            for j in range(j, 2):
                tidxstart[j] = 0
                tidxend[j] = 0
                thigh[j] = 0.0
                tlow[j] = 99999.0
            else:
                j = _range_end(j, 2, 1)
    else:
        i = _range_end(i, offset - 1, -1)
    return 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HansIndicatorX4(_MQL5Indicator):
    name = 'Hans_Indicator_x4'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'LocalTimeZone': 0,  # час начала отсчёта исходного коридора
        'DestTimeZone': 4,  # сдвиг коридора влево в барах
        'PipsForEntry1': 100,  # расширение границ первого сформированного коридора в пунктах
        'PipsForEntry2': 200,  # расширение границ второго сформированного коридора в пунктах
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

