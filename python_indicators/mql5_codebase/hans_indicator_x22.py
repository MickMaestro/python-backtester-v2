"""Hans_Indicator_x22 — converted from MQL5: MQL5 Indicators/Hans_Indicator_x22/Hans_Indicator_x22.mq5

Индикатор расширяющихся коридоров временных зон с одиннадцатью коридорами.
Сформированный коридор равен четырём часам, расширения коридора - шестнадцать часов.
Copyright: Copyright © 2014, Shimodax; Link: http://www.strategybuilderfx.com/forums/showthread.php?t=15439; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, Shimodax', 'link': 'http://www.strategybuilderfx.com/forums/showthread.php?t=15439', 'version': '1.02', 'window': 'chart', 'indicator_buffers': 24, 'indicator_plots': 24}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1}, 'colors': {1: [16711680], 2: [16711935], 3: [65280], 4: [255], 5: [32768], 6: [8519755], 7: [32768], 8: [8519755], 9: [32768], 10: [8519755], 11: [32768], 12: [8519755], 13: [65280], 14: [255], 15: [32768], 16: [8519755], 17: [32768], 18: [8519755], 19: [32768], 20: [8519755], 21: [32768], 22: [8519755], 23: [65280], 24: [255]}, 'widths': {1: 1, 2: 1, 3: 3, 4: 3, 5: 3, 6: 3, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 3, 14: 3, 15: 3, 16: 3, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 3, 24: 3}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 1, 8: 1, 9: 4, 10: 4, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 1, 18: 1, 19: 4, 20: 4, 21: 0, 22: 0, 23: 0, 24: 0}, 'labels': {1: 'Upper Hans_Indicator 1', 2: 'Lower Hans_Indicator 1', 3: 'Upper Hans_Indicator 2', 4: 'Lower Hans_Indicator 2', 5: 'Upper Hans_Indicator 3', 6: 'Lower Hans_Indicator 3', 7: 'Upper Hans_Indicator 4', 8: 'Lower Hans_Indicator 4', 9: 'Upper Hans_Indicator 5', 10: 'Lower Hans_Indicator 5', 11: 'Upper Hans_Indicator 6', 12: 'Lower Hans_Indicator 6', 13: 'Upper Hans_Indicator 7', 14: 'Lower Hans_Indicator 7', 15: 'Upper Hans_Indicator 8', 16: 'Lower Hans_Indicator 8', 17: 'Upper Hans_Indicator 8', 18: 'Lower Hans_Indicator 8', 19: 'Upper Hans_Indicator 10', 20: 'Lower Hans_Indicator 10', 21: 'Upper Hans_Indicator 11', 22: 'Lower Hans_Indicator 11', 23: 'Upper Hans_Indicator 12', 24: 'Lower Hans_Indicator 12'}, 'levels': [], 'description': ['Индикатор расширяющихся коридоров временных зон с одиннадцатью коридорами.', 'Сформированный коридор равен четырём часам, расширения коридора - шестнадцать часов.'], 'name': 'Hans_Indicator_x22', 'source': 'MQL5 Indicators/Hans_Indicator_x22/Hans_Indicator_x22.mq5', 'folder': 'Hans_Indicator_x22', 'inputs': [{'mql': 'LocalTimeZone', 'py': 'LocalTimeZone', 'param': 'LocalTimeZone', 'type': 'uint', 'default': 0, 'label': 'час начала отсчёта исходного коридора', 'sinput': False}, {'mql': 'DestTimeZone', 'py': 'DestTimeZone', 'param': 'DestTimeZone', 'type': 'uint', 'default': 4, 'label': 'сдвиг коридора влево в барах', 'sinput': False}, {'mql': 'PipsForEntryStep', 'py': 'PipsForEntryStep', 'param': 'PipsForEntryStep', 'type': 'uint', 'default': 50, 'label': 'шаг расширения границ каждого сформированного коридора в пунктах', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
LocalTimeZone = _input('LocalTimeZone', 0)  # час начала отсчёта исходного коридора
DestTimeZone = _input('DestTimeZone', 4)  # сдвиг коридора влево в барах
PipsForEntryStep = _input('PipsForEntryStep', 50)  # шаг расширения границ каждого сформированного коридора в пунктах
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
min_rates_total = 0
Zone1Upper = Arr(0, 0.0)
Zone2Upper = Arr(0, 0.0)
Zone3Upper = Arr(0, 0.0)
Zone4Upper = Arr(0, 0.0)
Zone5Upper = Arr(0, 0.0)
Zone6Upper = Arr(0, 0.0)
Zone1Lower = Arr(0, 0.0)
Zone2Lower = Arr(0, 0.0)
Zone3Lower = Arr(0, 0.0)
Zone4Lower = Arr(0, 0.0)
Zone5Lower = Arr(0, 0.0)
Zone6Lower = Arr(0, 0.0)
Zone7Upper = Arr(0, 0.0)
Zone8Upper = Arr(0, 0.0)
Zone9Upper = Arr(0, 0.0)
Zone10Upper = Arr(0, 0.0)
Zone11Upper = Arr(0, 0.0)
Zone12Upper = Arr(0, 0.0)
Zone7Lower = Arr(0, 0.0)
Zone8Lower = Arr(0, 0.0)
Zone9Lower = Arr(0, 0.0)
Zone10Lower = Arr(0, 0.0)
Zone11Lower = Arr(0, 0.0)
Zone12Lower = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = 100
    IndBufferInit(0, Zone1Upper)
    IndBufferInit(1, Zone1Lower)
    IndBufferInit(2, Zone2Upper)
    IndBufferInit(3, Zone2Lower)
    IndBufferInit(4, Zone3Upper)
    IndBufferInit(5, Zone3Lower)
    IndBufferInit(6, Zone4Upper)
    IndBufferInit(7, Zone4Lower)
    IndBufferInit(8, Zone5Upper)
    IndBufferInit(9, Zone5Lower)
    IndBufferInit(10, Zone6Upper)
    IndBufferInit(11, Zone6Lower)
    IndBufferInit(12, Zone7Upper)
    IndBufferInit(13, Zone7Lower)
    IndBufferInit(14, Zone8Upper)
    IndBufferInit(15, Zone8Lower)
    IndBufferInit(16, Zone9Upper)
    IndBufferInit(17, Zone9Lower)
    IndBufferInit(18, Zone10Upper)
    IndBufferInit(19, Zone10Lower)
    IndBufferInit(20, Zone11Upper)
    IndBufferInit(21, Zone11Lower)
    IndBufferInit(22, Zone12Upper)
    IndBufferInit(23, Zone12Lower)
    for count in range(0, 24):
        IndInit(count, 0.0, min_rates_total, Shift)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Hans_Indicator_x22(' + _str(LocalTimeZone) + ',' + _str(DestTimeZone) + ',' + _str(PipsForEntryStep) + ',' + _str(Shift) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def IndBufferInit(BuffNumber, Buffer):
    SetIndexBuffer(BuffNumber, Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Buffer, True)

def IndInit(PlotNumber, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(PlotNumber, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(PlotNumber, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(PlotNumber, PLOT_SHIFT, nShift)
    PlotIndexSetInteger(PlotNumber, PLOT_SHOW_DATA, False)

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
            Zone1Upper[i] = thigh[0] + (1 * PipsForEntryStep * Point())
            Zone1Lower[i] = tlow[0] - (1 * PipsForEntryStep * Point())
            Zone2Upper[i] = thigh[0] + (1 * PipsForEntryStep * Point())
            Zone2Lower[i] = tlow[0] - (1 * PipsForEntryStep * Point())
            Zone3Upper[i] = thigh[0] + (2 * PipsForEntryStep * Point())
            Zone3Lower[i] = tlow[0] - (2 * PipsForEntryStep * Point())
            Zone4Upper[i] = thigh[0] + (3 * PipsForEntryStep * Point())
            Zone4Lower[i] = tlow[0] - (3 * PipsForEntryStep * Point())
            Zone5Upper[i] = thigh[0] + (4 * PipsForEntryStep * Point())
            Zone5Lower[i] = tlow[0] - (4 * PipsForEntryStep * Point())
            Zone6Upper[i] = thigh[0] + (5 * PipsForEntryStep * Point())
            Zone6Lower[i] = tlow[0] - (5 * PipsForEntryStep * Point())
            Zone7Upper[i] = thigh[0] + (6 * PipsForEntryStep * Point())
            Zone7Lower[i] = tlow[0] - (6 * PipsForEntryStep * Point())
            Zone8Upper[i] = thigh[0] + (7 * PipsForEntryStep * Point())
            Zone8Lower[i] = tlow[0] - (7 * PipsForEntryStep * Point())
            Zone9Upper[i] = thigh[0] + (8 * PipsForEntryStep * Point())
            Zone9Lower[i] = tlow[0] - (8 * PipsForEntryStep * Point())
            Zone10Upper[i] = thigh[0] + (9 * PipsForEntryStep * Point())
            Zone10Lower[i] = tlow[0] - (9 * PipsForEntryStep * Point())
            Zone11Upper[i] = thigh[0] + (10 * PipsForEntryStep * Point())
            Zone11Lower[i] = tlow[0] - (10 * PipsForEntryStep * Point())
            Zone12Upper[i] = thigh[0] + (11 * PipsForEntryStep * Point())
            Zone12Lower[i] = tlow[0] - (11 * PipsForEntryStep * Point())
        else:
            Zone5Lower[i] = 0.0
            Zone5Upper[i] = Zone5Lower[i]
            Zone4Lower[i] = Zone5Upper[i]
            Zone4Upper[i] = Zone4Lower[i]
            Zone3Lower[i] = Zone4Upper[i]
            Zone3Upper[i] = Zone3Lower[i]
            Zone2Lower[i] = Zone3Upper[i]
            Zone2Upper[i] = Zone2Lower[i]
            Zone1Lower[i] = Zone2Upper[i]
            Zone1Upper[i] = Zone1Lower[i]
            Zone10Lower[i] = 0.0
            Zone10Upper[i] = Zone10Lower[i]
            Zone9Lower[i] = Zone10Upper[i]
            Zone9Upper[i] = Zone9Lower[i]
            Zone8Lower[i] = Zone9Upper[i]
            Zone8Upper[i] = Zone8Lower[i]
            Zone7Lower[i] = Zone8Upper[i]
            Zone7Upper[i] = Zone7Lower[i]
            Zone6Lower[i] = Zone7Upper[i]
            Zone6Upper[i] = Zone6Lower[i]
            Zone12Lower[i] = 0.0
            Zone12Upper[i] = Zone12Lower[i]
            Zone11Lower[i] = Zone12Upper[i]
            Zone11Upper[i] = Zone11Lower[i]
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


class HansIndicatorX22(_MQL5Indicator):
    name = 'Hans_Indicator_x22'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'LocalTimeZone': 0,  # час начала отсчёта исходного коридора
        'DestTimeZone': 4,  # сдвиг коридора влево в барах
        'PipsForEntryStep': 50,  # шаг расширения границ каждого сформированного коридора в пунктах
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

