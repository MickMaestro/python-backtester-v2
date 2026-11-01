"""marketprofile — converted from MQL5: MQL5 Indicators/MarketProfile/marketprofile.mq5

Copyright: Copyright © 2006, Viatcheslav Suvorov; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Viatcheslav Suvorov', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'marketprofile', 'source': 'MQL5 Indicators/MarketProfile/marketprofile.mq5', 'folder': 'MarketProfile', 'inputs': [{'mql': 'StartDate', 'py': 'StartDate', 'param': None, 'type': 'datetime', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'lastdayStart', 'py': 'lastdayStart', 'param': 'lastdayStart', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'CountProfile', 'py': 'CountProfile', 'param': 'CountProfile', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'AziaColor', 'py': 'AziaColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'EuropaColor', 'py': 'EuropaColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'AmericaColor', 'py': 'AmericaColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'MedianaColor', 'py': 'MedianaColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

DeepSkyBlue = 0xFFBF00  # MQL4 colour name
Gray = 0x808080  # MQL4 colour name
SpringGreen = 0x7FFF00  # MQL4 colour name
Violet = 0xEE82EE  # MQL4 colour name

# ---- inputs and global variables
StartDate = _input('StartDate', 0)
lastdayStart = _input('lastdayStart', True)
CountProfile = _input('CountProfile', 2)
CurPeriod_ = 0
StartDate_ = 0

def CreateRetangle(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_RECTANGLE, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetRetangle(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateRetangle(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)

def OnInit():
    global CurPeriod_, StartDate_
    StartDate_ = StartDate
    CurPeriod_ = _idiv(PeriodSeconds(PERIOD_CURRENT), 60)

def OnDeinit(reason):
    ObjectsDeleteAll(0, 0, OBJ_RECTANGLE)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global StartDate_
    x = CurPeriod_
    if x < 15 or x > 60:
        return 0
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    signal = False
    onetick = 0.0
    Mediana = 0.0
    LastHigh = 0.0
    LastLow = 0.0
    CurPos = 0.0
    i = 0
    j = 0
    MaxSize = 0
    MySize = 0
    MySizeEuropa = 0
    MySizeAzia = 0
    MySizeAmerica = 0
    BACK = 0
    TimeDay_ = 0
    TimeYear_ = 0
    sirname = ""
    if lastdayStart:
        StartDate_ = time[0]
    BACK = 0
    tm = MqlDateTime()
    TimeToStruct(StartDate_, tm)
    TimeDay_ = tm.day_of_year
    TimeYear_ = tm.year
    TimeToStruct(time[BACK], tm)
    while tm.day_of_year > TimeDay_ or (tm.year != TimeYear_ and BACK < rates_total):
        BACK += 1
        if BACK >= rates_total:
            return rates_total
        TimeToStruct(time[BACK], tm)
        TimeYear_ = tm.year
    onetick = _fdiv(1, MathPow(10, Digits()))
    i = BACK
    for cycles in range(CountProfile, 0, -1):
        signal = False
        LastHigh = high[i]
        LastLow = low[i]
        while not signal:
            if high[i + 1] > LastHigh:
                LastHigh = high[i + 1]
            if low[i + 1] < LastLow:
                LastLow = low[i + 1]
            MaxSize = 0
            MySize = 0
            TimeToStruct(time[i], tm)
            TimeDay_ = tm.day
            TimeToStruct(time[i + 1], tm)
            if TimeDay_ != tm.day:
                signal = True
                CurPos = LastLow
                while CurPos <= LastHigh:
                    MySizeAzia = 0
                    MySizeEuropa = 0
                    MySizeAmerica = 0
                    j = i
                    for j in range(j, BACK - 1, -1):
                        if high[j] >= CurPos and low[j] <= CurPos:
                            MySize += 1
                            TimeToStruct(time[j], tm)
                            if tm.hour >= 13:
                                MySizeAmerica += 1
                            elif tm.hour >= 8 and tm.hour < 13:
                                MySizeEuropa += 1
                            else:
                                MySizeAzia += 1
                    else:
                        j = _range_end(j, BACK - 1, -1)
                    if (MySizeAzia + MySizeEuropa + MySizeAmerica) > MaxSize:
                        MaxSize = MySizeAzia + MySizeEuropa + MySizeAmerica
                        Mediana = CurPos
                    sirname = TimeToString(time[i], TIME_DATE) + _str(CurPos)
                    if MySizeAzia != 0:
                        CreateRetangle(0, 'rec' + 'Azia' + sirname, 0, time[i], CurPos, time[i - MySizeAzia], CurPos + onetick, AziaColor, STYLE_SOLID, 1, 'rec' + 'Azia' + sirname)
                    if MySizeEuropa != 0:
                        CreateRetangle(0, 'rec' + 'Europa' + sirname, 0, time[i - MySizeAzia], CurPos, time[i - MySizeAzia - MySizeEuropa], CurPos + onetick, EuropaColor, STYLE_SOLID, 1, 'rec' + 'Europa' + sirname)
                    if MySizeAmerica != 0:
                        CreateRetangle(0, 'rec' + 'America' + sirname, 0, time[i - MySizeAzia - MySizeEuropa], CurPos, time[i - MySizeAzia - MySizeEuropa - MySizeAmerica], CurPos + onetick, AmericaColor, STYLE_SOLID, 1, 'rec' + 'America' + sirname)
                    CurPos = CurPos + onetick
                sirname = TimeToString(time[i], TIME_DATE)
                CreateRetangle(0, 'mediana' + sirname, 0, time[i], Mediana, time[i + 10], Mediana + onetick, _uint(Gray), STYLE_SOLID, 1, 'mediana' + sirname)
                BACK = i + 1
            i += 1
            if i >= rates_total:
                return rates_total
    ChartRedraw(0)
    return rates_total

# ---- global variables initialised from expressions
AziaColor = _input('AziaColor', _uint(SpringGreen))
EuropaColor = _input('EuropaColor', _uint(DeepSkyBlue))
AmericaColor = _input('AmericaColor', _uint(Violet))
MedianaColor = _input('MedianaColor', _uint(Gray))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Marketprofile(_MQL5Indicator):
    name = 'marketprofile'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'lastdayStart': True,
        'CountProfile': 2,
    }

