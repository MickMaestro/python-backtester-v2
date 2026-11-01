"""marketprofile_ — converted from MQL5: MQL5 Indicators/MarketProfile/marketprofile_.mq5

Displays the Market Profile indicator for the daily trading sessions.
Should be attached to M5, M15 or M30 timeframes.
M30 is recommended.
Designed for standard currency pairs. May work incorrectly with very exotic pairs, CFDs or commodities.
Be careful: it will delete all rectangle objects on the chart upon deinitialization.
Copyright: EarnForex.com; Link: http://www.earnforex.com; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'EarnForex.com', 'link': 'http://www.earnforex.com', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Displays the Market Profile indicator for the daily trading sessions.', 'Should be attached to M5, M15 or M30 timeframes.', 'M30 is recommended.', '', 'Designed for standard currency pairs. May work incorrectly with very exotic pairs, CFDs or commodities.', 'Be careful: it will delete all rectangle objects on the chart upon deinitialization.'], 'name': 'marketprofile_', 'source': 'MQL5 Indicators/MarketProfile/marketprofile_.mq5', 'folder': 'MarketProfile', 'inputs': [{'mql': 'StartFromDate', 'py': 'StartFromDate', 'param': None, 'type': 'datetime', 'default': 1700000000, 'label': '', 'sinput': False}, {'mql': 'StartFromToday', 'py': 'StartFromToday', 'param': 'StartFromToday', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'DaysToCount', 'py': 'DaysToCount', 'param': 'DaysToCount', 'type': 'int', 'default': 2, 'label': 'Number of days for which to count the Market Profile', 'sinput': False}, {'mql': 'ColorScheme', 'py': 'ColorScheme', 'param': 'ColorScheme', 'type': 'int', 'default': 0, 'label': '0 - Blue to Red, 1 - Red to Green, 2 - Green to Blue', 'sinput': False}, {'mql': 'MedianColor', 'py': 'MedianColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'ValueAreaColor', 'py': 'ValueAreaColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

DarkBlue = 0x8B0000  # MQL4 colour name
DarkGreen = 0x006400  # MQL4 colour name
DarkRed = 0x00008B  # MQL4 colour name
White = 0xFFFFFF  # MQL4 colour name

# ---- inputs and global variables
StartFromDate = _input('StartFromDate', 1700000000)
StartFromToday = _input('StartFromToday', True)
DaysToCount = _input('DaysToCount', 2)  # Number of days for which to count the Market Profile
ColorScheme = _input('ColorScheme', 0)  # 0 - Blue to Red, 1 - Red to Green, 2 - Green to Blue
DigitsM = 0  # Amount of digits normalized for standard 4 and 2 digits after dot
StartDate = 0  # Will hold either StartFromDate or Time[0]
onetick = 0.0  # One normalized pip
SecondsInPeriod = 0  # Will hold calculated amount of seconds in the selected timeframe period
FirstRunDone = False  # If true - OnCalculate() was already executed once

def OnInit():
    global DigitsM, SecondsInPeriod, onetick
    IndicatorSetString(INDICATOR_SHORTNAME, 'MarketProfile')
    if Digits() == 5:
        DigitsM = 4
    elif Digits() == 3:
        DigitsM = 2
    else:
        DigitsM = Digits()
    if Period() == PERIOD_M30:
        SecondsInPeriod = 1800
    if Period() == PERIOD_M15:
        SecondsInPeriod = 900
    if Period() == PERIOD_M5:
        SecondsInPeriod = 300
    onetick = NormalizeDouble(_fdiv(1, MathPow(10, DigitsM)), DigitsM)

def OnDeinit(reason):
    ObjectsDeleteAll(0, 0, OBJ_RECTANGLE)

def OnCalculate(rates_total, prev_calculated, Time, open, High, Low, close, tick_volume, volume, spread):
    global FirstRunDone, StartDate
    if (Period() != PERIOD_M30 and Period() != PERIOD_M15) and Period() != PERIOD_M5:
        Print('TimeFrame should be set to M30, M15 or M5.')
        return -1
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Time, True)
    if StartFromToday:
        StartDate = Time[0]
    else:
        StartDate = StartFromDate
    if FirstRunDone and StartDate != Time[0]:
        return rates_total
    dayend = FindDayEndByDate(Time, StartDate, rates_total)
    daystart = FindDayStart(Time, dayend, rates_total)
    DayToStart = 0
    if FirstRunDone:
        DayToStart = DaysToCount - 1
    else:
        for i in range(1, DaysToCount):
            dayend = daystart + 1
            daystart = FindDayStart(Time, dayend, rates_total)
    for i in range(DayToStart, DaysToCount):
        DayMax = -1.0
        DayMin = 99999999999.0
        for bar in range(daystart, dayend - 1, -1):
            if High[bar] > DayMax:
                DayMax = High[bar]
            if Low[bar] < DayMin:
                DayMin = Low[bar]
        DayMax = NormalizeDouble(DayMax, DigitsM)
        DayMin = NormalizeDouble(DayMin, DigitsM)
        TPOperPrice = Arr(0, 0)
        max_ = _int(round(_fdiv(DayMax, onetick)) + 2)
        ArrayResize(TPOperPrice, max_)
        ArrayInitialize(TPOperPrice, 0)
        MaxRange = 0
        PriceOfMaxRange = 0.0
        DistanceToCenter = 99999999.0
        TotalTPO = 0
        price = DayMax
        while price >= DayMin:
            range_ = 0
            for bar in range(daystart, dayend - 1, -1):
                if price >= Low[bar] and price <= High[bar]:
                    if MaxRange < range_ or (MaxRange == range_ and MathAbs(price - (DayMin + ((DayMax - DayMin) / 2))) < DistanceToCenter):
                        MaxRange = range_
                        PriceOfMaxRange = price
                        DistanceToCenter = MathAbs(price - (DayMin + ((DayMax - DayMin) / 2)))
                    PutDot(price, Time[daystart], range_, bar - daystart)
                    TPOperPrice[_int(_fdiv(price, onetick))] += 1
                    range_ += 1
                    TotalTPO += 1
            price -= onetick
        ValueControlTPO = _int(float(TotalTPO) * 0.7)
        TPOcount = TPOperPrice[_int(_fdiv(PriceOfMaxRange, onetick))]
        up_offset = 1
        down_offset = 1
        while TPOcount < ValueControlTPO:
            abovePrice = PriceOfMaxRange + (up_offset * onetick)
            belowPrice = PriceOfMaxRange - (down_offset * onetick)
            if (TPOperPrice[_int(_fdiv(abovePrice, onetick))] >= TPOperPrice[_int(_fdiv(belowPrice, onetick))] or belowPrice < DayMin) and abovePrice <= DayMax:
                TPOcount += TPOperPrice[_int(_fdiv(abovePrice, onetick))]
                up_offset += 1
            else:
                TPOcount += TPOperPrice[_int(_fdiv(belowPrice, onetick))]
                down_offset += 1
        LastName = ' ' + TimeToString(Time[daystart], TIME_DATE)
        if ObjectFind(0, 'Median' + LastName) >= 0:
            ObjectDelete(0, 'Median ' + LastName)
        ObjectCreate(0, 'Median' + LastName, OBJ_RECTANGLE, 0, Time[daystart + 16], PriceOfMaxRange, Time[MathMax(daystart - MaxRange - 5, 0)], PriceOfMaxRange + onetick)
        ObjectSetInteger(0, 'Median' + LastName, OBJPROP_COLOR, MedianColor)
        ObjectSetInteger(0, 'Median' + LastName, OBJPROP_STYLE, STYLE_SOLID)
        if ObjectFind(0, 'Value Area' + LastName) >= 0:
            ObjectDelete(0, 'Value Area ' + LastName)
        ObjectCreate(0, 'Value Area' + LastName, OBJ_RECTANGLE, 0, Time[daystart], PriceOfMaxRange + (up_offset * onetick), Time[daystart] + ((MaxRange + 1) * SecondsInPeriod), PriceOfMaxRange - (down_offset * onetick))
        ObjectSetInteger(0, 'Value Area' + LastName, OBJPROP_COLOR, ValueAreaColor)
        ObjectSetInteger(0, 'Value Area' + LastName, OBJPROP_FILL, False)
        if (DaysToCount - i) > 1:
            daystart = dayend - 1
            dayend = FindDayEndByDate(Time, Time[daystart], rates_total)
    FirstRunDone = True
    return rates_total

def FindDayStart(Time, n, rates_total):
    dt1 = MqlDateTime()
    dt2 = MqlDateTime()
    x = n
    TimeToStruct(Time[n], dt1)
    TimeToStruct(Time[x], dt2)
    while dt1.day_of_year == dt2.day_of_year and x < rates_total:
        x += 1
        TimeToStruct(Time[x], dt2)
    return x - 1

def FindDayEndByDate(Time, date, rates_total):
    dt1 = MqlDateTime()
    dt2 = MqlDateTime()
    x = 0
    TimeToStruct(date, dt1)
    TimeToStruct(Time[x], dt2)
    while dt1.day_of_year < dt2.day_of_year and x < rates_total:
        x += 1
        TimeToStruct(Time[x], dt2)
    return x

def PutDot(price, time, range_, bar):
    LastName = ' ' + IntegerToString(time + (range_ * SecondsInPeriod)) + ' ' + DoubleToString(price)
    if ObjectFind(0, 'MP' + LastName) >= 0:
        return
    ObjectCreate(0, 'MP' + LastName, OBJ_RECTANGLE, 0, time + (range_ * SecondsInPeriod), price, time + ((range_ + 1) * SecondsInPeriod), price + onetick)
    colour = 0
    offset1 = 0
    offset2 = 0
    _sw1 = ColorScheme
    if _sw1 == 0:
        colour = _int(DarkBlue)
        offset1 = 0x020000
        offset2 = 0x000002
    elif _sw1 == 1:
        colour = _int(DarkRed)
        offset1 = 0x000002
        offset2 = 0x000200
    elif _sw1 == 2:
        colour = _int(DarkGreen)
        offset1 = 0x000200
        offset2 = 0x020000
    if Period() == PERIOD_M30:
        colour += bar * offset1
    elif Period() == PERIOD_M15:
        colour += bar * _idiv(offset1, 2)
    else:
        colour += _idiv(bar, 3) * _idiv(offset1, 2)
    if Period() == PERIOD_M30:
        colour -= bar * offset2
    elif Period() == PERIOD_M15:
        colour -= bar * _idiv(offset2, 2)
    else:
        colour -= _idiv(bar, 3) * _idiv(offset2, 2)
    ObjectSetInteger(0, 'MP' + LastName, OBJPROP_COLOR, colour)
    ObjectSetInteger(0, 'MP' + LastName, OBJPROP_FILL, True)

# ---- global variables initialised from expressions
MedianColor = _input('MedianColor', _uint(White))
ValueAreaColor = _input('ValueAreaColor', _uint(White))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Marketprofile(_MQL5Indicator):
    name = 'marketprofile_'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'StartFromToday': True,
        'DaysToCount': 2,  # Number of days for which to count the Market Profile
        'ColorScheme': 0,  # 0 - Blue to Red, 1 - Red to Green, 2 - Green to Blue
    }

