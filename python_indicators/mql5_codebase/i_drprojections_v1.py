"""i-drprojections_v1 — converted from MQL5: MQL5 Indicators/i-DRProjections_v1/i-drprojections_v1.mq5

Copyright: KimIV; Link: http://www.kimiv.ru

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'KimIV', 'link': 'http://www.kimiv.ru', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [15453831], 2: [4678655]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Line Hi', 2: 'Line Lo'}, 'levels': [], 'description': [], 'name': 'i-drprojections_v1', 'source': 'MQL5 Indicators/i-DRProjections_v1/i-drprojections_v1.mq5', 'folder': 'i-DRProjections_v1', 'inputs': [{'mql': 'NumberOfDays', 'py': 'NumberOfDays', 'param': 'NumberOfDays', 'type': 'int', 'default': 1, 'label': 'Number of days', 'sinput': False}, {'mql': 'ShowTomorrow', 'py': 'ShowTomorrow', 'param': 'ShowTomorrow', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'UniqueID', 'py': 'UniqueID', 'param': None, 'type': 'string', 'default': 'DRProj', 'label': '', 'sinput': False}, {'mql': 'LineHiColor', 'py': 'LineHiColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'LineLoColor', 'py': 'LineLoColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'LineStyle', 'py': 'LineStyle', 'param': 'LineStyle', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'LineWidth', 'py': 'LineWidth', 'param': 'LineWidth', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

SkyBlue = 0xEBCE87  # MQL4 colour name
Tomato = 0x4763FF  # MQL4 colour name

# ---- inputs and global variables
NumberOfDays = _input('NumberOfDays', 1)  # Number of days
ShowTomorrow = _input('ShowTomorrow', True)
UniqueID = _input('UniqueID', 'DRProj')
LineStyle = _input('LineStyle', STYLE_DOT)
LineWidth = _input('LineWidth', 1)
MaxDay = Arr(0, 0.0)
MinDay = Arr(0, 0.0)
TimeFrame = PERIOD_D1

def OnInit():
    SetIndexBuffer(0, MaxDay, INDICATOR_DATA)
    SetIndexBuffer(1, MinDay, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'i-DRProjections_v1[' + timeframeToString(TimeFrame) + '](' + _str(NumberOfDays) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    objCreate(UniqueID + 'linehi', OBJ_TREND, LineStyle, 1, LineWidth, LineHiColor)
    objCreate(UniqueID + 'linelo', OBJ_TREND, LineStyle, 1, LineWidth, LineLoColor)

def OnDeinit(reason):
    deleteObj(UniqueID)
    Comment('')
    return

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    j = 0
    copied = 0
    currDay = 0
    open = 0.0
    high = 0.0
    low = 0.0
    close = 0.0
    price = 0.0
    if Period() > PERIOD_H12:
        Comment('i-DRProjections does not support TimeFrame longer H12 !')
        return 0
    if prev_calculated == 0:
        ArrayInitialize(MaxDay, EMPTY_VALUE)
        ArrayInitialize(MinDay, EMPTY_VALUE)
    mtfRates = Arr(0, 0, factory=MqlRates)
    ArraySetAsSeries(mtfRates, True)
    ArraySetAsSeries(Time, True)
    ArraySetAsSeries(MaxDay, True)
    ArraySetAsSeries(MinDay, True)
    copied = CopyRates(None, TimeFrame, 0, NumberOfDays + 2, mtfRates)
    if copied < 0:
        Print('not all Rates copied. Will try on next tick Error =', GetLastError(), ', copied =', copied)
        return 0
    while i <= NumberOfDays:
        if currDay != TimeDay_u(Time[j]):
            open = mtfRates[i + 1].open
            high = mtfRates[i + 1].high
            low = mtfRates[i + 1].low
            close = mtfRates[i + 1].close
            if close < open:
                price = (high + low + close + low) / 2
            if close > open:
                price = (high + low + close + high) / 2
            if close == open:
                price = (high + low + close + close) / 2
            i += 1
        currDay = TimeDay_u(Time[j])
        MaxDay[j] = price - low
        MinDay[j] = price - high
        j += 1
    if ShowTomorrow:
        open = mtfRates[0].open
        high = mtfRates[0].high
        low = mtfRates[0].low
        close = mtfRates[0].close
        if close < open:
            price = (high + low + close + low) / 2
        if close > open:
            price = (high + low + close + high) / 2
        if close == open:
            price = (high + low + close + close) / 2
        ObjectMove(0, UniqueID + 'linehi', 0, Time[1], price - low)
        ObjectMove(0, UniqueID + 'linelo', 0, Time[1], price - high)
        ObjectSetInteger(0, UniqueID + 'linehi', OBJPROP_TIME, 0, Time[1])
        ObjectSetDouble(0, UniqueID + 'linehi', OBJPROP_PRICE, 0, price - low)
        ObjectSetInteger(0, UniqueID + 'linehi', OBJPROP_TIME, 1, TimeCurrent())
        ObjectSetDouble(0, UniqueID + 'linehi', OBJPROP_PRICE, 1, price - low)
        ObjectSetInteger(0, UniqueID + 'linelo', OBJPROP_TIME, 0, Time[1])
        ObjectSetDouble(0, UniqueID + 'linelo', OBJPROP_PRICE, 0, price - high)
        ObjectSetInteger(0, UniqueID + 'linelo', OBJPROP_TIME, 1, TimeCurrent())
        ObjectSetDouble(0, UniqueID + 'linelo', OBJPROP_PRICE, 1, price - high)
    return rates_total

def timeframeToString(TF):
    _sw1 = TF
    if _sw1 == PERIOD_CURRENT:
        return 'Current'
    elif _sw1 == PERIOD_M1:
        return 'M1'
    elif _sw1 == PERIOD_M2:
        return 'M2'
    elif _sw1 == PERIOD_M3:
        return 'M3'
    elif _sw1 == PERIOD_M4:
        return 'M4'
    elif _sw1 == PERIOD_M5:
        return 'M5'
    elif _sw1 == PERIOD_M6:
        return 'M6'
    elif _sw1 == PERIOD_M10:
        return 'M10'
    elif _sw1 == PERIOD_M12:
        return 'M12'
    elif _sw1 == PERIOD_M15:
        return 'M15'
    elif _sw1 == PERIOD_M20:
        return 'M20'
    elif _sw1 == PERIOD_M30:
        return 'M30'
    elif _sw1 == PERIOD_H1:
        return 'H1'
    elif _sw1 == PERIOD_H2:
        return 'H2'
    elif _sw1 == PERIOD_H3:
        return 'H3'
    elif _sw1 == PERIOD_H4:
        return 'H4'
    elif _sw1 == PERIOD_H6:
        return 'H6'
    elif _sw1 == PERIOD_H8:
        return 'H8'
    elif _sw1 == PERIOD_H12:
        return 'H12'
    elif _sw1 == PERIOD_D1:
        return 'D1'
    elif _sw1 == PERIOD_W1:
        return 'W1'
    elif _sw1 == PERIOD_MN1:
        return 'MN1'
    else:
        return 'Current'

def TimeDay_u(date):
    tm = MqlDateTime()
    TimeToStruct(date, tm)
    return tm.day

def objCreate(name, type_, style, ray, width, clr):
    if not ObjectCreate(0, name, type_, 0, 0, 0, 0, 0, 0, 0):
        return -1
    if not ObjectSetInteger(0, name, OBJPROP_STYLE, style):
        return -1
    if not ObjectSetInteger(0, name, OBJPROP_WIDTH, width):
        return -1
    if not ObjectSetInteger(0, name, OBJPROP_COLOR, clr):
        return -1
    if ray > 0:
        if not ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, ray):
            return -1
    return 1

def deleteObj(prefix):
    name = ''
    total = ObjectsTotal(0) - 1
    for i in range(total, 0 - 1, -1):
        name = ObjectName(0, i)
        if StringFind(name, prefix) >= 0:
            ObjectDelete(0, name)

# ---- global variables initialised from expressions
LineHiColor = _input('LineHiColor', _uint(SkyBlue))
LineLoColor = _input('LineLoColor', _uint(Tomato))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IDrprojectionsV1(_MQL5Indicator):
    name = 'i-drprojections_v1'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'NumberOfDays': 1,  # Number of days
        'ShowTomorrow': True,
        'LineStyle': 2,
        'LineWidth': 1,
    }

