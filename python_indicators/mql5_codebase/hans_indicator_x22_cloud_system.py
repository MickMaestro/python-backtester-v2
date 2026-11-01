"""Hans_Indicator_x22_Cloud_System — converted from MQL5: MQL5 Indicators/Hans_Indicator_x22_Cloud_System/Hans_Indicator_x22_Cloud_System.mq5

Индикатор расширяющихся коридоров временных зон с одиннадцатью коридорами,  с фоновым цветовым заполнением, средней линией коридора,
с окрашиванием свечек при выходе из сформированного четырёхчасового коридора.
Сформированный коридор равен четырём часам, расширения коридора - шестнадцать часов.
Copyright: Copyright © 2014, Shimodax; Link: http://www.strategybuilderfx.com/forums/showthread.php?t=15439; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, Shimodax', 'link': 'http://www.strategybuilderfx.com/forums/showthread.php?t=15439', 'version': '1.02', 'window': 'chart', 'indicator_buffers': 34, 'indicator_plots': 28}, 'types': {1: 7, 2: 7, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 17}, 'colors': {1: [16252904], 2: [16773375], 3: [16711680], 4: [16711935], 5: [65280], 6: [255], 7: [32768], 8: [8519755], 9: [32768], 10: [8519755], 11: [32768], 12: [8519755], 13: [32768], 14: [8519755], 15: [65280], 16: [255], 17: [32768], 18: [8519755], 19: [32768], 20: [8519755], 21: [32768], 22: [8519755], 23: [32768], 24: [8519755], 25: [65280], 26: [255], 27: [9470064], 28: [16760576, 16711680, 8421504, 8388736, 16711935]}, 'widths': {3: 1, 4: 1, 5: 3, 6: 3, 7: 3, 8: 3, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 3, 16: 3, 17: 3, 18: 3, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 25: 3, 26: 3, 27: 2}, 'styles': {3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 1, 10: 1, 11: 4, 12: 4, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 1, 20: 1, 21: 4, 22: 4, 23: 0, 24: 0, 25: 0, 26: 0, 27: 0}, 'labels': {1: 'Upper Hans_Indicator_x22 cloud', 2: 'Lower Hans_Indicator_x22 cloud', 3: 'Upper Hans_Indicator 1', 4: 'Lower Hans_Indicator 1', 5: 'Upper Hans_Indicator 2', 6: 'Lower Hans_Indicator 2', 7: 'Upper Hans_Indicator 3', 8: 'Lower Hans_Indicator 3', 9: 'Upper Hans_Indicator 4', 10: 'Lower Hans_Indicator 4', 11: 'Upper Hans_Indicator 5', 12: 'Lower Hans_Indicator 5', 13: 'Upper Hans_Indicator 6', 14: 'Lower Hans_Indicator 6', 15: 'Upper Hans_Indicator 7', 16: 'Lower Hans_Indicator 7', 17: 'Upper Hans_Indicator 8', 18: 'Lower Hans_Indicator 8', 19: 'Upper Hans_Indicator 8', 20: 'Lower Hans_Indicator 8', 21: 'Upper Hans_Indicator 10', 22: 'Lower Hans_Indicator 10', 23: 'Upper Hans_Indicator 11', 24: 'Lower Hans_Indicator 11', 25: 'Upper Hans_Indicator 12', 26: 'Lower Hans_Indicator 12', 27: 'Middle Hans_Indicator', 28: 'Hans_Indicator Open;Hans_Indicator High;Hans_Indicator Low;Hans_Indicator Close'}, 'levels': [], 'description': ['Индикатор расширяющихся коридоров временных зон с одиннадцатью коридорами,  с фоновым цветовым заполнением, средней линией коридора,', 'с окрашиванием свечек при выходе из сформированного четырёхчасового коридора.', 'Сформированный коридор равен четырём часам, расширения коридора - шестнадцать часов.'], 'name': 'Hans_Indicator_x22_Cloud_System', 'source': 'MQL5 Indicators/Hans_Indicator_x22_Cloud_System/Hans_Indicator_x22_Cloud_System.mq5', 'folder': 'Hans_Indicator_x22_Cloud_System', 'inputs': [{'mql': 'LocalTimeZone', 'py': 'LocalTimeZone', 'param': 'LocalTimeZone', 'type': 'uint', 'default': 0, 'label': 'час начала отсчёта исходного коридора', 'sinput': False}, {'mql': 'DestTimeZone', 'py': 'DestTimeZone', 'param': 'DestTimeZone', 'type': 'uint', 'default': 4, 'label': 'сдвиг коридора влево в барах', 'sinput': False}, {'mql': 'PipsForEntryStep', 'py': 'PipsForEntryStep', 'param': 'PipsForEntryStep', 'type': 'uint', 'default': 50, 'label': 'шаг расширения границ каждого сформированного коридора в пунктах', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
LocalTimeZone = _input('LocalTimeZone', 0)  # час начала отсчёта исходного коридора
DestTimeZone = _input('DestTimeZone', 4)  # сдвиг коридора влево в барах
PipsForEntryStep = _input('PipsForEntryStep', 50)  # шаг расширения границ каждого сформированного коридора в пунктах
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
min_rates_total = 0
UpUpBuffer = Arr(0, 0.0)
UpDnBuffer = Arr(0, 0.0)
DnUpBuffer = Arr(0, 0.0)
DnDnBuffer = Arr(0, 0.0)
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
MiddleBuffer = Arr(0, 0.0)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = 100
    IndBufferInit(0, UpUpBuffer)
    IndBufferInit(1, UpDnBuffer)
    IndBufferInit(2, DnUpBuffer)
    IndBufferInit(3, DnDnBuffer)
    IndBufferInit(4, Zone1Upper)
    IndBufferInit(5, Zone1Lower)
    IndBufferInit(6, Zone2Upper)
    IndBufferInit(7, Zone2Lower)
    IndBufferInit(8, Zone3Upper)
    IndBufferInit(9, Zone3Lower)
    IndBufferInit(10, Zone4Upper)
    IndBufferInit(11, Zone4Lower)
    IndBufferInit(12, Zone5Upper)
    IndBufferInit(13, Zone5Lower)
    IndBufferInit(14, Zone6Upper)
    IndBufferInit(15, Zone6Lower)
    IndBufferInit(16, Zone7Upper)
    IndBufferInit(17, Zone7Lower)
    IndBufferInit(18, Zone8Upper)
    IndBufferInit(19, Zone8Lower)
    IndBufferInit(20, Zone9Upper)
    IndBufferInit(21, Zone9Lower)
    IndBufferInit(22, Zone10Upper)
    IndBufferInit(23, Zone10Lower)
    IndBufferInit(24, Zone11Upper)
    IndBufferInit(25, Zone11Lower)
    IndBufferInit(26, Zone12Upper)
    IndBufferInit(27, Zone12Lower)
    IndBufferInit(28, MiddleBuffer)
    IndBufferInit(29, ExtOpenBuffer)
    IndBufferInit(30, ExtHighBuffer)
    IndBufferInit(31, ExtLowBuffer)
    IndBufferInit(32, ExtCloseBuffer)
    IndBufferInit(33, ExtColorBuffer)
    for count in range(0, 2):
        IndInit(count, EMPTY_VALUE, min_rates_total, Shift)
    for count in range(2, 28):
        IndInit(count, 0.0, min_rates_total, Shift)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Hans_Indicator_x22_Cloud_System(' + _str(LocalTimeZone) + ',' + _str(DestTimeZone) + ',' + _str(PipsForEntryStep) + ',' + _str(Shift) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def IndBufferInit(BuffNumber, Buffer):
    SetIndexBuffer(BuffNumber, Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Buffer, True)

def IndCldInit(PlotNumber, Draw_Begin, nShift):
    PlotIndexSetInteger(PlotNumber, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetInteger(PlotNumber, PLOT_SHIFT, nShift)
    PlotIndexSetInteger(PlotNumber, PLOT_SHOW_DATA, False)

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
    ArraySetAsSeries(Open, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Close, True)
    BreakoutRanges(0, limit, LocalTimeZone, DestTimeZone, rates_total, Time, Open, High, Low, Close)
    return rates_total

def BreakoutRanges(offset, lastbar, tzlocal, tzdest, rates_total_, Time_, Open_, High_, Low_, Close_):
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
                            ExtCloseBuffer[k] = 0.0
                            ExtLowBuffer[k] = ExtCloseBuffer[k]
                            ExtHighBuffer[k] = ExtLowBuffer[k]
                            ExtOpenBuffer[k] = ExtHighBuffer[k]
                            ExtColorBuffer[k] = 2.0
                            if (j - 1) == 0:
                                Zone1Upper[k] = thigh[j - 1]
                                Zone1Lower[k] = tlow[j - 1]
                                MiddleBuffer[k] = (Zone1Upper[k] + Zone1Lower[k]) / 2
                                if Close_[k] > Zone1Upper[k]:
                                    ExtOpenBuffer[k] = Open_[k]
                                    ExtHighBuffer[k] = High_[k]
                                    ExtLowBuffer[k] = Low_[k]
                                    ExtCloseBuffer[k] = Close_[k]
                                    if Close_[k] >= Open_[k]:
                                        ExtColorBuffer[k] = 0.0
                                    else:
                                        ExtColorBuffer[k] = 1.0
                                if Close_[k] < Zone1Lower[k]:
                                    ExtOpenBuffer[k] = Open_[k]
                                    ExtHighBuffer[k] = High_[k]
                                    ExtLowBuffer[k] = Low_[k]
                                    ExtCloseBuffer[k] = Close_[k]
                                    if Close_[k] <= Open_[k]:
                                        ExtColorBuffer[k] = 4.0
                                    else:
                                        ExtColorBuffer[k] = 3.0
                            if (j - 1) == 1:
                                Zone2Upper[k] = thigh[j - 1]
                                Zone2Lower[k] = tlow[j - 1]
                                MiddleBuffer[k] = (Zone1Upper[k] + Zone1Lower[k]) / 2
                                if Close_[k] > Zone2Upper[k]:
                                    ExtOpenBuffer[k] = Open_[k]
                                    ExtHighBuffer[k] = High_[k]
                                    ExtLowBuffer[k] = Low_[k]
                                    ExtCloseBuffer[k] = Close_[k]
                                    if Close_[k] >= Open_[k]:
                                        ExtColorBuffer[k] = 0.0
                                    else:
                                        ExtColorBuffer[k] = 1.0
                                if Close_[k] < Zone2Lower[k]:
                                    ExtOpenBuffer[k] = Open_[k]
                                    ExtHighBuffer[k] = High_[k]
                                    ExtLowBuffer[k] = Low_[k]
                                    ExtCloseBuffer[k] = Close_[k]
                                    if Close_[k] <= Open_[k]:
                                        ExtColorBuffer[k] = 4.0
                                    else:
                                        ExtColorBuffer[k] = 3.0
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
            DnUpBuffer[i] = (Zone1Upper[i] + Zone1Lower[i]) / 2
            UpDnBuffer[i] = DnUpBuffer[i]
            MiddleBuffer[i] = UpDnBuffer[i]
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
            UpUpBuffer[i] = thigh[0] + (11 * PipsForEntryStep * Point())
            Zone12Upper[i] = UpUpBuffer[i]
            DnDnBuffer[i] = tlow[0] - (11 * PipsForEntryStep * Point())
            Zone12Lower[i] = DnDnBuffer[i]
            ExtCloseBuffer[i] = 0.0
            ExtLowBuffer[i] = ExtCloseBuffer[i]
            ExtHighBuffer[i] = ExtLowBuffer[i]
            ExtOpenBuffer[i] = ExtHighBuffer[i]
            ExtColorBuffer[i] = 2.0
            if Close_[i] > Zone1Upper[i]:
                ExtOpenBuffer[i] = Open_[i]
                ExtHighBuffer[i] = High_[i]
                ExtLowBuffer[i] = Low_[i]
                ExtCloseBuffer[i] = Close_[i]
                if Close_[i] >= Open_[i]:
                    ExtColorBuffer[i] = 0.0
                else:
                    ExtColorBuffer[i] = 1.0
            if Close_[i] < Zone1Lower[i]:
                ExtOpenBuffer[i] = Open_[i]
                ExtHighBuffer[i] = High_[i]
                ExtLowBuffer[i] = Low_[i]
                ExtCloseBuffer[i] = Close_[i]
                if Close_[i] <= Open_[i]:
                    ExtColorBuffer[i] = 4.0
                else:
                    ExtColorBuffer[i] = 3.0
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
            DnDnBuffer[i] = 0.0
            UpUpBuffer[i] = DnDnBuffer[i]
            DnUpBuffer[i] = UpUpBuffer[i]
            UpDnBuffer[i] = DnUpBuffer[i]
            MiddleBuffer[i] = UpDnBuffer[i]
            ExtCloseBuffer[i] = 0.0
            ExtLowBuffer[i] = ExtCloseBuffer[i]
            ExtHighBuffer[i] = ExtLowBuffer[i]
            ExtOpenBuffer[i] = ExtHighBuffer[i]
            ExtColorBuffer[i] = 2.0
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


class HansIndicatorX22CloudSystem(_MQL5Indicator):
    name = 'Hans_Indicator_x22_Cloud_System'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'LocalTimeZone': 0,  # час начала отсчёта исходного коридора
        'DestTimeZone': 4,  # сдвиг коридора влево в барах
        'PipsForEntryStep': 50,  # шаг расширения границ каждого сформированного коридора в пунктах
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

