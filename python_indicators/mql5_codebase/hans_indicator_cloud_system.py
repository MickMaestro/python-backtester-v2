"""Hans_Indicator_Cloud_System — converted from MQL5: MQL5 Indicators/Hans_Indicator_Cloud_System/Hans_Indicator_Cloud_System.mq5

Индикатор расширяющихся коридоров временных зон с фоновым цветовым заполнением и средней линией коридора.
Сформированный коридор равен четырём часам, расширение коридора - шестнадцать часов.
Copyright: Copyright © 2014, Shimodax; Link: http://www.strategybuilderfx.com/forums/showthread.php?t=15439; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, Shimodax', 'link': 'http://www.strategybuilderfx.com/forums/showthread.php?t=15439', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 14, 'indicator_plots': 8}, 'types': {1: 7, 2: 7, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 17}, 'colors': {1: [16252904], 2: [16773375], 3: [16711680], 4: [16711935], 5: [3329330], 6: [255], 7: [9470064], 8: [16760576, 16711680, 8421504, 8388736, 16711935]}, 'widths': {3: 1, 4: 1, 5: 3, 6: 3, 7: 2}, 'styles': {3: 0, 4: 0, 5: 0, 6: 0, 7: 0}, 'labels': {1: 'Upper Hans_Indicator cloud', 2: 'Lower Hans_Indicator cloud', 3: 'Upper Hans_Indicator 1', 4: 'Lower Hans_Indicator 1', 5: 'Upper Hans_Indicator 2', 6: 'Lower Hans_Indicator 2', 7: 'Middle Hans_Indicator', 8: 'Hans_Indicator Open;Hans_Indicator High;Hans_Indicator Low;Hans_Indicator Close'}, 'levels': [], 'description': ['Индикатор расширяющихся коридоров временных зон с фоновым цветовым заполнением и средней линией коридора.', 'Сформированный коридор равен четырём часам, расширение коридора - шестнадцать часов.'], 'name': 'Hans_Indicator_Cloud_System', 'source': 'MQL5 Indicators/Hans_Indicator_Cloud_System/Hans_Indicator_Cloud_System.mq5', 'folder': 'Hans_Indicator_Cloud_System', 'inputs': [{'mql': 'LocalTimeZone', 'py': 'LocalTimeZone', 'param': 'LocalTimeZone', 'type': 'uint', 'default': 0, 'label': 'час начала отсчёта исходного коридора', 'sinput': False}, {'mql': 'DestTimeZone', 'py': 'DestTimeZone', 'param': 'DestTimeZone', 'type': 'uint', 'default': 4, 'label': 'сдвиг коридора влево в барах', 'sinput': False}, {'mql': 'PipsForEntry', 'py': 'PipsForEntry', 'param': 'PipsForEntry', 'type': 'uint', 'default': 100, 'label': 'расширение границ сформированного коридора в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
LocalTimeZone = _input('LocalTimeZone', 0)  # час начала отсчёта исходного коридора
DestTimeZone = _input('DestTimeZone', 4)  # сдвиг коридора влево в барах
PipsForEntry = _input('PipsForEntry', 100)  # расширение границ сформированного коридора в пунктах
min_rates_total = 0
UpUp2Buffer = Arr(0, 0.0)
UpDn2Buffer = Arr(0, 0.0)
DnUp2Buffer = Arr(0, 0.0)
DnDn2Buffer = Arr(0, 0.0)
Zone1Upper = Arr(0, 0.0)
Zone2Upper = Arr(0, 0.0)
Zone1Lower = Arr(0, 0.0)
Zone2Lower = Arr(0, 0.0)
MiddleBuffer = Arr(0, 0.0)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = 100
    SetIndexBuffer(0, UpUp2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(UpUp2Buffer, True)
    SetIndexBuffer(1, UpDn2Buffer, INDICATOR_DATA)
    ArraySetAsSeries(UpDn2Buffer, True)
    SetIndexBuffer(2, DnUp2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(DnUp2Buffer, True)
    SetIndexBuffer(3, DnDn2Buffer, INDICATOR_DATA)
    ArraySetAsSeries(DnDn2Buffer, True)
    SetIndexBuffer(4, Zone1Upper, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(Zone1Upper, True)
    SetIndexBuffer(5, Zone1Lower, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(3, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(Zone1Lower, True)
    SetIndexBuffer(6, Zone2Upper, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(4, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(Zone2Upper, True)
    SetIndexBuffer(7, Zone2Lower, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(5, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(Zone2Lower, True)
    SetIndexBuffer(8, MiddleBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(6, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(MiddleBuffer, True)
    SetIndexBuffer(9, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(10, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(11, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(12, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(13, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    PlotIndexSetInteger(7, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(7, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(7, PLOT_SHOW_DATA, False)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Hans_Indicator_Cloud_System(' + _str(LocalTimeZone) + ',' + _str(DestTimeZone) + ',' + _str(PipsForEntry) + ')')
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
    ArraySetAsSeries(Open, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Close, True)
    BreakoutRanges(0, limit, LocalTimeZone, DestTimeZone, rates_total, Time, Open, High, Low, Close)
    return rates_total

def BreakoutRanges(offset, lastk, tzlocal, tzdest, rates_total_, Time_, Open_, High_, Low_, Close_):
    i = 0
    j = 0
    k = 0
    tzdiff = tzlocal - tzdest
    tzdiffsec = tzdiff * 3600
    tidxstart = Arr.of([0, 0], fill=0, dyn=False, size=2)
    tidxend = Arr.of([0, 0], fill=0, dyn=False, size=2)
    thigh = Arr.of([0.0], fill=0.0, dyn=False, size=2)
    tlow = Arr.of([DBL_MAX], fill=0.0, dyn=False, size=2)
    tfrom = Arr.of(['04:00', '08:00', '12:00'], fill="", dyn=False, size=3)
    tto = Arr.of(['08:00', '12:00', '24:00'], fill="", dyn=False, size=3)
    tday = ""
    inperiod = (-1 != 0)
    timet = 0
    tday = TimeToString(Time_[lastk.v] - tzdiffsec, TIME_DATE)
    while lastk.v < (rates_total_ - 1):
        if TimeToString(Time_[lastk.v] - tzdiffsec, TIME_DATE) != tday:
            lastk.v -= 1
            break
        lastk.v += 1
    tday = 'XXX'
    i = lastk.v
    for i in range(i, offset - 1, -1):
        ExtCloseBuffer[i] = 0.0
        ExtLowBuffer[i] = ExtCloseBuffer[i]
        ExtHighBuffer[i] = ExtLowBuffer[i]
        ExtOpenBuffer[i] = ExtHighBuffer[i]
        ExtColorBuffer[i] = 2.0
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
                                UpUp2Buffer[k] = thigh[j - 1]
                                Zone1Upper[k] = UpUp2Buffer[k]
                                DnDn2Buffer[k] = tlow[j - 1]
                                Zone1Lower[k] = DnDn2Buffer[k]
                                DnUp2Buffer[k] = (Zone1Upper[k] + Zone1Lower[k]) / 2
                                UpDn2Buffer[k] = DnUp2Buffer[k]
                                MiddleBuffer[k] = UpDn2Buffer[k]
                                if Close_[k] > UpUp2Buffer[k]:
                                    ExtOpenBuffer[k] = Open_[k]
                                    ExtHighBuffer[k] = High_[k]
                                    ExtLowBuffer[k] = Low_[k]
                                    ExtCloseBuffer[k] = Close_[k]
                                    if Close_[k] >= Open_[k]:
                                        ExtColorBuffer[k] = 0.0
                                    else:
                                        ExtColorBuffer[k] = 1.0
                                if Close_[k] < DnDn2Buffer[k]:
                                    ExtOpenBuffer[k] = Open_[k]
                                    ExtHighBuffer[k] = High_[k]
                                    ExtLowBuffer[k] = Low_[k]
                                    ExtCloseBuffer[k] = Close_[k]
                                    if Close_[k] <= Open_[k]:
                                        ExtColorBuffer[k] = 4.0
                                    else:
                                        ExtColorBuffer[k] = 3.0
                            if (j - 1) == 1:
                                UpUp2Buffer[k] = thigh[j - 1]
                                Zone2Upper[k] = UpUp2Buffer[k]
                                DnDn2Buffer[k] = tlow[j - 1]
                                Zone2Lower[k] = DnDn2Buffer[k]
                                DnUp2Buffer[k] = (Zone1Upper[k] + Zone1Lower[k]) / 2
                                UpDn2Buffer[k] = DnUp2Buffer[k]
                                MiddleBuffer[k] = UpDn2Buffer[k]
                                if Close_[k] > UpUp2Buffer[k]:
                                    ExtOpenBuffer[k] = Open_[k]
                                    ExtHighBuffer[k] = High_[k]
                                    ExtLowBuffer[k] = Low_[k]
                                    ExtCloseBuffer[k] = Close_[k]
                                    if Close_[k] >= Open_[k]:
                                        ExtColorBuffer[k] = 0.0
                                    else:
                                        ExtColorBuffer[k] = 1.0
                                if Close_[k] < DnDn2Buffer[k]:
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
        ExtCloseBuffer[i] = 0.0
        ExtLowBuffer[i] = ExtCloseBuffer[i]
        ExtHighBuffer[i] = ExtLowBuffer[i]
        ExtOpenBuffer[i] = ExtHighBuffer[i]
        ExtColorBuffer[i] = 2.0
        if inperiod >= 1 and tday == thisday:
            UpUp2Buffer[i] = thigh[0] + (PipsForEntry * Point())
            Zone1Upper[i] = UpUp2Buffer[i]
            DnDn2Buffer[i] = tlow[0] - (PipsForEntry * Point())
            Zone1Lower[i] = DnDn2Buffer[i]
            DnUp2Buffer[i] = (Zone1Upper[i] + Zone1Lower[i]) / 2
            UpDn2Buffer[i] = DnUp2Buffer[i]
            MiddleBuffer[i] = UpDn2Buffer[i]
            Zone2Upper[i] = thigh[0] + (PipsForEntry * Point())
            Zone2Lower[i] = tlow[0] - (PipsForEntry * Point())
            if Close_[i] > UpUp2Buffer[i]:
                ExtOpenBuffer[i] = Open_[i]
                ExtHighBuffer[i] = High_[i]
                ExtLowBuffer[i] = Low_[i]
                ExtCloseBuffer[i] = Close_[i]
                if Close_[i] >= Open_[i]:
                    ExtColorBuffer[i] = 0.0
                else:
                    ExtColorBuffer[i] = 1.0
            if Close_[i] < DnDn2Buffer[i]:
                ExtOpenBuffer[i] = Open_[i]
                ExtHighBuffer[i] = High_[i]
                ExtLowBuffer[i] = Low_[i]
                ExtCloseBuffer[i] = Close_[i]
                if Close_[i] <= Open_[i]:
                    ExtColorBuffer[i] = 4.0
                else:
                    ExtColorBuffer[i] = 3.0
            if inperiod >= 2:
                UpUp2Buffer[i] = thigh[1] + (PipsForEntry * Point())
                Zone2Upper[i] = UpUp2Buffer[i]
                DnDn2Buffer[i] = tlow[1] - (PipsForEntry * Point())
                Zone2Lower[i] = DnDn2Buffer[i]
                DnUp2Buffer[i] = (Zone1Upper[i] + Zone1Lower[i]) / 2
                UpDn2Buffer[i] = DnUp2Buffer[i]
                MiddleBuffer[i] = UpDn2Buffer[i]
                if Close_[i] > UpUp2Buffer[i]:
                    ExtOpenBuffer[i] = Open_[i]
                    ExtHighBuffer[i] = High_[i]
                    ExtLowBuffer[i] = Low_[i]
                    ExtCloseBuffer[i] = Close_[i]
                    if Close_[i] >= Open_[i]:
                        ExtColorBuffer[i] = 0.0
                    else:
                        ExtColorBuffer[i] = 1.0
                if Close_[i] < DnDn2Buffer[i]:
                    ExtOpenBuffer[i] = Open_[i]
                    ExtHighBuffer[i] = High_[i]
                    ExtLowBuffer[i] = Low_[i]
                    ExtCloseBuffer[i] = Close_[i]
                    if Close_[i] <= Open_[i]:
                        ExtColorBuffer[i] = 4.0
                    else:
                        ExtColorBuffer[i] = 3.0
        else:
            DnDn2Buffer[i] = 0.0
            UpUp2Buffer[i] = DnDn2Buffer[i]
            DnUp2Buffer[i] = UpUp2Buffer[i]
            UpDn2Buffer[i] = DnUp2Buffer[i]
            MiddleBuffer[i] = UpDn2Buffer[i]
            Zone2Lower[i] = MiddleBuffer[i]
            Zone2Upper[i] = Zone2Lower[i]
            Zone1Lower[i] = Zone2Upper[i]
            Zone1Upper[i] = Zone1Lower[i]
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
                tlow[j] = DBL_MAX
            else:
                j = _range_end(j, 2, 1)
    else:
        i = _range_end(i, offset - 1, -1)
    return 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HansIndicatorCloudSystem(_MQL5Indicator):
    name = 'Hans_Indicator_Cloud_System'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'LocalTimeZone': 0,  # час начала отсчёта исходного коридора
        'DestTimeZone': 4,  # сдвиг коридора влево в барах
        'PipsForEntry': 100,  # расширение границ сформированного коридора в пунктах
    }

