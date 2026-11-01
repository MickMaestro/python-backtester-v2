"""Volume Profile — converted from MQL5: MQL5 Indicators/Volume Profile/Volume Profile.mq5

Copyright: Mohammad E. Baset; Link: baset84@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Mohammad E. Baset', 'link': 'baset84@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Volume Profile', 'source': 'MQL5 Indicators/Volume Profile/Volume Profile.mq5', 'folder': 'Volume Profile', 'inputs': [{'mql': 'tf0', 'py': 'tf0', 'param': 'tf0', 'type': 'int', 'default': 0, 'label': 'calcualtion timeframe', 'sinput': False}, {'mql': 'precision', 'py': 'precision', 'param': 'precision', 'type': 'int', 'default': 100, 'label': 'number of VP bars', 'sinput': False}, {'mql': 'av', 'py': 'av', 'param': 'av', 'type': 'int', 'default': 1, 'label': 'applied volume', 'sinput': False}, {'mql': 'ratio', 'py': 'ratio', 'param': 'ratio', 'type': 'double', 'default': 0.25, 'label': 'ratio of maximum VP bar length to chart width', 'sinput': False}, {'mql': 'gc', 'py': 'gc', 'param': None, 'type': 'color', 'default': 9470064, 'label': 'bars color', 'sinput': False}, {'mql': 'pocc', 'py': 'pocc', 'param': None, 'type': 'color', 'default': 42495, 'label': 'POC color', 'sinput': False}, {'mql': 'svlc', 'py': 'svlc', 'param': None, 'type': 'color', 'default': 32768, 'label': 'start vline color', 'sinput': False}, {'mql': 'evlc', 'py': 'evlc', 'param': None, 'type': 'color', 'default': 32768, 'label': 'end vline color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
tf0 = _input('tf0', PERIOD_CURRENT)  # calcualtion timeframe
precision = _input('precision', 100)  # number of VP bars
av = _input('av', VOLUME_REAL)  # applied volume
ratio = _input('ratio', 0.25)  # ratio of maximum VP bar length to chart width
gc = _input('gc', clrSlateGray)  # bars color
pocc = _input('pocc', clrOrange)  # POC color
svlc = _input('svlc', clrGreen)  # start vline color
evlc = _input('evlc', clrGreen)  # end vline color
tf = tf0

def OnInit():
    global tf
    if precision <= 0:
        Alert("precision couldn't be zero or less than zero")
        return INIT_FAILED
    if PeriodSeconds(PERIOD_CURRENT) < PeriodSeconds(tf0):
        tf = PERIOD_CURRENT
    ChartRedraw(0)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    if reason == 1:
        ObjectsDeleteAll(0, 'VP', -1, -1)
    if reason != 1:
        ChartRedraw()

def OnChartEvent(id_, lparam, dparam, sparam):
    if ObjectFind(0, 'VP begin') < 0:
        VLineCreate('VP begin', TimeCurrent() - (61 * PeriodSeconds(PERIOD_CURRENT)), svlc)
    if ObjectFind(0, 'VP finish') < 0:
        VLineCreate('VP finish', TimeCurrent() - (1 * PeriodSeconds(PERIOD_CURRENT)), evlc)
    if id_ != CHARTEVENT_OBJECT_DRAG and id_ != CHARTEVENT_CHART_CHANGE:
        return
    if id_ == CHARTEVENT_OBJECT_DRAG and (sparam == 'VP begin' or sparam == 'VP finish'):
        ChartRedraw(0)
    time_begin = ObjectGetInteger(0, 'VP begin', OBJPROP_TIME)
    time_finish = ObjectGetInteger(0, 'VP finish', OBJPROP_TIME)
    bars = Bars(Symbol(), tf, time_begin, time_finish)
    if time_begin >= time_finish:
        return
    high_array = Arr(0, 0.0)
    low_array = Arr(0, 0.0)
    volume = Arr(0, 0)
    ArrayResize(high_array, bars)
    ArrayResize(low_array, bars)
    ArrayResize(volume, bars)
    if (CopyHigh(Symbol(), tf, _DT(time_begin), _DT(time_finish), high_array) == -1 or CopyLow(Symbol(), tf, _DT(time_begin), _DT(time_finish), low_array) == -1) or CopyRealVolume(Symbol(), tf, _DT(time_begin), _DT(time_finish), volume) == -1:
        return
    if av == VOLUME_TICK or volume[0] == 0:
        if CopyTickVolume(Symbol(), tf, _DT(time_begin), _DT(time_finish), volume) == -1:
            return
    max_ = high_array[ArrayMaximum(high_array, 0, WHOLE_ARRAY)]
    min_ = low_array[ArrayMinimum(low_array, 0, WHOLE_ARRAY)]
    range_ = (max_ - min_) / precision
    profile = Arr(0, 0.0)
    ArrayResize(profile, precision)
    for i in range(0, bars):
        Floor = _int(MathFloor(_fdiv(low_array[i] - min_, range_)))
        Ceil = _int(MathFloor(_fdiv(high_array[i] - min_, range_)))
        body = high_array[i] - low_array[i]
        tail = min_ + ((Floor + 1) * range_) - low_array[i]
        wick = high_array[i] - (min_ + (Ceil * range_))
        if i == 0:
            for n in range(0, precision):
                profile[n] = 0.0
        for n in range(0, precision):
            if n < Floor or n > Ceil:
                continue
            if (Ceil - Floor) == 0:
                profile[n] += float(volume[i])
            elif n == Floor:
                profile[n] += _fdiv(tail, body) * volume[i]
            elif n == Ceil:
                profile[n] += _fdiv(wick, body) * volume[i]
            else:
                profile[n] += _fdiv(range_, body) * volume[i]
    POC = profile[ArrayMaximum(profile, 0, WHOLE_ARRAY)]
    BL = _int(ratio * ChartGetInteger(0, CHART_WIDTH_IN_PIXELS))
    ch = _int((ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS) * _fdiv(max_ - min_, ChartGetDouble(0, CHART_PRICE_MAX) - ChartGetDouble(0, CHART_PRICE_MIN))) / precision)
    if POC == 0.0:
        return
    ObjectsDeleteAll(0, 'VP prfl ', -1, -1)
    for n in range(0, precision):
        xd = _int(_fdiv(profile[n], POC) * BL)
        x_start = Box(0)
        y_start = Box(0)
        ChartTimePriceToXY(0, 0, time_finish, min_ + ((n + 1) * range_), x_start, y_start)
        if (x_start.v + xd) >= ChartGetInteger(0, CHART_WIDTH_IN_PIXELS):
            xd = _int(ChartGetInteger(0, CHART_WIDTH_IN_PIXELS)) - x_start.v
        RectLabelCreate('VP prfl ' + IntegerToString(n), x_start.v, y_start.v, xd, ch, gc)
        if profile[n] == POC:
            ObjectSetInteger(0, 'VP prfl ' + IntegerToString(n), OBJPROP_COLOR, pocc)
            ObjectSetInteger(0, 'VP prfl ' + IntegerToString(n), OBJPROP_BGCOLOR, pocc)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def VLineCreate(name='VLine', time=0, clr=clrRed, style=STYLE_DOT, width=1, chart_ID=0, sub_window=0, back=True, selection=True, ray=True, hidden=False, z_order=0):
    if not time:
        time = TimeCurrent()
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_VLINE, sub_window, time, 0):
        Print('VLineCreate', ': failed to create a vertical line! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_RAY, ray)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True

def RectLabelCreate(name='RectLabel', x=0, y=0, width=50, height=1, clr=clrRed, back_clr=clrNONE, border=BORDER_FLAT, corner=CORNER_LEFT_UPPER, style=STYLE_SOLID, line_width=1, chart_ID=0, sub_window=0, back=True, selection=False, hidden=True, z_order=0):
    ResetLastError()
    if not ObjectCreate(chart_ID, name, OBJ_RECTANGLE_LABEL, sub_window, 0, 0):
        Print('RectLabelCreate', ': failed to create a rectangle label! Error code = ', GetLastError())
        return False
    ObjectSetInteger(chart_ID, name, OBJPROP_XDISTANCE, x)
    ObjectSetInteger(chart_ID, name, OBJPROP_YDISTANCE, y)
    ObjectSetInteger(chart_ID, name, OBJPROP_XSIZE, width)
    ObjectSetInteger(chart_ID, name, OBJPROP_YSIZE, height)
    ObjectSetInteger(chart_ID, name, OBJPROP_BGCOLOR, back_clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_BORDER_TYPE, border)
    ObjectSetInteger(chart_ID, name, OBJPROP_CORNER, corner)
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, line_width)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolumeProfile(_MQL5Indicator):
    name = 'Volume Profile'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'tf0': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # calcualtion timeframe
        'precision': 100,  # number of VP bars
        'av': _Choice({0: 'Tick', 1: 'Real'}, default=1),  # applied volume
        'ratio': 0.25,  # ratio of maximum VP bar length to chart width
    }

