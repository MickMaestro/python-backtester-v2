"""candle_timer — converted from MQL5: MQL5 Indicators/Candle Timer/candle_timer.mq5

Copyright: www.forex-tsd.com; Link: www.forex-tsd.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.forex-tsd.com', 'link': 'www.forex-tsd.com', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'candle_timer', 'source': 'MQL5 Indicators/Candle Timer/candle_timer.mq5', 'folder': 'Candle Timer', 'inputs': [{'mql': 'ValuesPositiveColor', 'py': 'ValuesPositiveColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Color for positive timer values', 'sinput': False}, {'mql': 'ValuesNegativeColor', 'py': 'ValuesNegativeColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Color for negative timer values', 'sinput': False}, {'mql': 'TimeFontSize', 'py': 'TimeFontSize', 'param': 'TimeFontSize', 'type': 'int', 'default': 10, 'label': 'Font size for timer', 'sinput': False}, {'mql': 'TimerShift', 'py': 'TimerShift', 'param': 'TimerShift', 'type': 'int', 'default': 7, 'label': 'Timer shift', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MediumSeaGreen = 0x71B33C  # MQL4 colour name
PaleVioletRed = 0x9370DB  # MQL4 colour name

# ---- inputs and global variables
TimeFontSize = _input('TimeFontSize', 10)  # Font size for timer
TimerShift = _input('TimerShift', 7)  # Timer shift
atrHandle = 0

def OnInit():
    global atrHandle
    atrHandle = iATR(None, 0, 30)
    EventSetTimer(1)
    return 0

def OnDeinit(reason):
    EventKillTimer()

def OnTimer():
    refreshClock()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    refreshClock()
    return rates_total

def refreshClock():
    global _s_refreshClock_inRefresh
    if _s_refreshClock_inRefresh:
        return
    _s_refreshClock_inRefresh = True
    ShowClock()
    ChartRedraw()
    _s_refreshClock_inRefresh = False

def ShowClock():
    periodMinutes = periodToMinutes(Period())
    shift = periodMinutes * TimerShift * 60
    currentTime = _int(TimeCurrent())
    localTime = _int(TimeLocal())
    barTime = _int(iTime_u())
    diff = _int(MathMax(round((currentTime - localTime) / 3600.0) * 3600, -24 * 3600))
    theColor = Box(0)
    time = getTime(barTime + (periodMinutes * 60) - localTime - diff, theColor)
    time = (time if TerminalInfoInteger(TERMINAL_CONNECTED) else (time + ' x'))
    if ObjectFind(0, 'CandleTimer') < 0:
        ObjectCreate(0, 'CandleTimer', OBJ_TEXT, 0, barTime + shift, 0)
    ObjectSetString(0, 'CandleTimer', OBJPROP_TEXT, time)
    ObjectSetString(0, 'CandleTimer', OBJPROP_FONT, 'Arial')
    ObjectSetInteger(0, 'CandleTimer', OBJPROP_FONTSIZE, TimeFontSize)
    ObjectSetInteger(0, 'CandleTimer', OBJPROP_COLOR, theColor.v)
    if ChartGetInteger(0, CHART_SHIFT, 0) == 0 and shift >= 0:
        ObjectSetInteger(0, 'CandleTimer', OBJPROP_TIME, barTime - (shift * 3))
    else:
        ObjectSetInteger(0, 'CandleTimer', OBJPROP_TIME, barTime + shift)
    price = Arr(0, 0.0)
    if CopyClose(Symbol(), 0, 0, 1, price) <= 0:
        return
    atr = Arr(0, 0.0)
    if CopyBuffer(atrHandle, 0, 0, 1, atr) <= 0:
        return
    price[0] += (3.0 * atr[0]) / 4.0
    visible = (ChartGetInteger(0, CHART_VISIBLE_BARS, 0) - ChartGetInteger(0, CHART_FIRST_VISIBLE_BAR, 0)) > 0
    if visible and price[0] >= ChartGetDouble(0, CHART_PRICE_MAX, 0):
        ObjectSetDouble(0, 'CandleTimer', OBJPROP_PRICE, price[0] - (1.5 * atr[0]))
    else:
        ObjectSetDouble(0, 'CandleTimer', OBJPROP_PRICE, price[0])

def getTime(times, theColor):
    stime = ''
    seconds = 0
    minutes = 0
    hours = 0
    if times < 0:
        theColor.v = ValuesNegativeColor
        times = fabs(times)
    else:
        theColor.v = ValuesPositiveColor
    seconds = _imod(times, 60)
    hours = _idiv(times - _imod(times, 3600), 3600)
    minutes = _idiv(times - seconds, 60) - (hours * 60)
    if hours > 0:
        if minutes < 10:
            stime = stime + _str(hours) + ':0'
        else:
            stime = stime + _str(hours) + ':'
    stime = stime + _str(minutes)
    if seconds < 10:
        stime = stime + ':0' + _str(seconds)
    else:
        stime = stime + ':' + _str(seconds)
    return stime

def iTime_u(forPeriod=PERIOD_CURRENT):
    times = Arr(0, 0)
    if CopyTime(Symbol(), forPeriod, 0, 1, times) <= 0:
        return TimeLocal()
    return times[0]

def periodToMinutes(period):
    i = 0
    if period == PERIOD_CURRENT:
        period = Period()
    i = 0
    for i in range(i, 20):
        if period == _s_periodToMinutes__per[i]:
            break
    else:
        i = _range_end(i, 20, 1)
    return _s_periodToMinutes__min[i]

# ---- global variables initialised from expressions
ValuesPositiveColor = _input('ValuesPositiveColor', _uint(MediumSeaGreen))  # Color for positive timer values
ValuesNegativeColor = _input('ValuesNegativeColor', _uint(PaleVioletRed))  # Color for negative timer values

# ---- static local variables
_s_refreshClock_inRefresh = False
_s_periodToMinutes__per = Arr.of([1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 0x4001, 0x4002, 0x4003, 0x4004, 0x4006, 0x4008, 0x400c, 0x4018, 0x8001, 0xc001], fill=0)
_s_periodToMinutes__min = Arr.of([1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60, 120, 180, 240, 360, 480, 720, 1440, 10080, 43200], fill=0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleTimer(_MQL5Indicator):
    name = 'candle_timer'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFontSize': 10,  # Font size for timer
        'TimerShift': 7,  # Timer shift
    }

