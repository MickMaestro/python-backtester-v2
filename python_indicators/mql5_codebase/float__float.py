"""float — converted from MQL5: MQL5 Indicators/Float/float.mq5

Float - Trend strength, volume, Fibonacci and DiNapoli levels.
Copyright: Copyright © 2010  Andriy Moraru; Link: http://www.earnforex.com/

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010  Andriy Moraru', 'link': 'http://www.earnforex.com/', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 3, 2: 1}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {}, 'levels': [], 'description': ['Float - Trend strength, volume, Fibonacci and DiNapoli levels.'], 'name': 'float', 'source': 'MQL5 Indicators/Float/float.mq5', 'folder': 'Float', 'inputs': [{'mql': 'Float', 'py': 'Float', 'param': 'Float', 'type': 'int', 'default': 200, 'label': 'amount of bars for the trends analysis. The lower the number, the newer the data,', 'sinput': False}, {'mql': 'use_fibos', 'py': 'use_fibos', 'param': 'use_fibos', 'type': 'bool', 'default': True, 'label': 'permission Fibonacci levels', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'volume', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Float = _input('Float', 200)  # amount of bars for the trends analysis. The lower the number, the newer the data,
use_fibos = _input('use_fibos', True)  # permission Fibonacci levels
VolumeType = _input('VolumeType', VOLUME_TICK)  # volume
high_bar = 0.0
low_bar = 0.0
cumulativeV = 0.0
FLOATV = 0.0
swing = 0.0
prevbars = 0.0
fib23 = 0.0
fib38 = 0.0
fib50 = 0.0
fib62 = 0.0
fib76 = 0.0
dinap0 = 0.0
dinap1 = 0.0
dinap2 = 0.0
dinap3 = 0.0
dinap4 = 0.0
dinap5 = 0.0
Buffer1 = Arr(0, 0.0)
Buffer2 = Arr(0, 0.0)
first = True
bar = 0
swing_time = 0
loopbegin1 = 0
cvstart = 0
cvend = 0
bars_high = 0
bars_low = 0

def OnInit():
    SetIndexBuffer(0, Buffer1, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(Buffer1, True)
    SetIndexBuffer(1, Buffer2, INDICATOR_DATA)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(Buffer2, True)
    short_name = 'Float'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    PlotIndexSetString(0, PLOT_LABEL, short_name)

def OnDeinit(reason):
    ObjectDelete(0, 'swingtop')
    ObjectDelete(0, 'swingbottom')
    ObjectDelete(0, 'fib23')
    ObjectDelete(0, 'fib38')
    ObjectDelete(0, 'fib50')
    ObjectDelete(0, 'fib62')
    ObjectDelete(0, 'fib76')
    ObjectDelete(0, 'fib23t')
    ObjectDelete(0, 'fib38t')
    ObjectDelete(0, 'fib50t')
    ObjectDelete(0, 'fib62t')
    ObjectDelete(0, 'fib76t')
    ObjectDelete(0, 'dinap0')
    ObjectDelete(0, 'dinap1')
    ObjectDelete(0, 'dinap2')
    ObjectDelete(0, 'dinap3')
    ObjectDelete(0, 'dinap4')
    ObjectDelete(0, 'dinap5')
    ObjectDelete(0, 'CVSTART')
    ObjectDelete(0, 'CVEND')
    ObjectDelete(0, 'swingend1')
    ObjectDelete(0, 'swingend2')
    ObjectDelete(0, 'swingend3')
    ObjectDelete(0, 'swingend4')
    ObjectDelete(0, 'swingend5')
    ObjectDelete(0, 'swingend6')
    ObjectDelete(0, 'swingend7')
    ObjectDelete(0, 'swingend8')
    ObjectDelete(0, 'swingend9')
    Comment('')

def OnCalculate(rates_total, prev_calculated, Time, open, High, Low, close, tick_volume, volume, spread):
    global FLOATV, bar, bars_high, bars_low, cumulativeV, cvend, cvstart, dinap0, dinap1, dinap2, dinap3, dinap4, dinap5, fib23, fib38, fib50, fib62, fib76, first, high_bar, loopbegin1, low_bar, prevbars, swing, swing_time
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(tick_volume, True)
    ArraySetAsSeries(volume, True)
    ArraySetAsSeries(Time, True)
    counted_bars = prev_calculated
    if counted_bars < 0:
        return -1
    cumulativeV = 0.0
    if rates_total < prevbars or (rates_total - prevbars) > 1:
        first = True
        prevbars = rates_total
        FLOATV = 0.0
        loopbegin1 = rates_total - Float
        bar = loopbegin1
        while bar >= 0:
            bars_high = ArrayMaximum(High, 1, Float)
            bars_low = ArrayMinimum(Low, 1, Float)
            high_bar = High[bars_high]
            low_bar = Low[bars_low]
            if bars_high < bars_low:
                cvstart = bars_low
                cvend = bars_high
            else:
                cvstart = bars_high
                cvend = bars_low
            if first and (not FLOATV):
                bar = cvstart
                while bar >= cvend:
                    if VolumeType == VOLUME_TICK:
                        FLOATV += float(tick_volume[bar])
                    else:
                        FLOATV += float(volume[bar])
                    first = False
                    bar -= 1
            bar -= 1
        swing = high_bar - low_bar
        swing_time = MathAbs(bars_low - bars_high)
        start = rates_total - cvstart
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, start)
        bar = cvstart
        while bar >= 0:
            if VolumeType == VOLUME_TICK:
                cumulativeV += float(tick_volume[bar])
            else:
                cumulativeV += float(volume[bar])
            if cumulativeV >= FLOATV:
                cumulativeV = 0.0
            Buffer1[bar] = cumulativeV * 0.001
            Buffer2[bar] = FLOATV * 0.001
            Comment('\n', 'high was   ', bars_high, '  bars ago', '\n', 'Low was    ', bars_low, ' bars ago', '\n', '\n', 'Float time was  =      ', swing_time, ' bars', '\n', 'Float Vol. left    =     ', FLOATV - cumulativeV, '\n', 'Float Volume    =     ', FLOATV)
            bar -= 1
        SetTline(0, 'swingtop', 0, Time[cvstart], high_bar, Time[1], high_bar, clrBlue, STYLE_SOLID, 1, 'swingtop')
        SetTline(0, 'swingbottom', 0, Time[cvstart], low_bar, Time[1], low_bar, clrBlue, STYLE_SOLID, 1, 'swingbottom')
        if use_fibos:
            fib23 = (swing * 0.236) + low_bar
            fib38 = (swing * 0.382) + low_bar
            fib50 = (swing * 0.5) + low_bar
            fib62 = (swing * 0.618) + low_bar
            fib76 = (swing * 0.764) + low_bar
            dinap0 = (low_bar + fib23) / 2
            dinap1 = (fib23 + fib38) / 2
            dinap2 = (fib38 + fib50) / 2
            dinap3 = (fib50 + fib62) / 2
            dinap4 = (fib62 + fib76) / 2
            dinap5 = (high_bar + fib76) / 2
            SetTline(0, 'fib23', 0, Time[cvstart], fib23, Time[1], fib23, clrGreen, STYLE_DASH, 1, 'fib23')
            SetTextObj(0, 'fib23t', 0, Time[1], fib23, clrGreen, 8, 'Arial', '23.6')
            SetTline(0, 'fib38', 0, Time[cvstart], fib38, Time[1], fib38, clrGreen, STYLE_DASH, 1, 'fib38')
            SetTextObj(0, 'fib38t', 0, Time[1], fib38, clrGreen, 8, 'Arial', '38.2')
            SetTline(0, 'fib50', 0, Time[cvstart], fib50, Time[1], fib50, clrRed, STYLE_SOLID, 2, 'fib50')
            SetTextObj(0, 'fib50t', 0, Time[1], fib50, clrGreen, 8, 'Arial', '50.0')
            SetTline(0, 'fib62', 0, Time[cvstart], fib62, Time[1], fib62, clrGreen, STYLE_DASH, 1, 'fib62')
            SetTextObj(0, 'fib62t', 0, Time[1], fib62, clrGreen, 8, 'Arial', '61.8')
            SetTline(0, 'fib76', 0, Time[cvstart], fib76, Time[1], fib76, clrGreen, STYLE_DASH, 1, 'fib76')
            SetTextObj(0, 'fib76t', 0, Time[1], fib76, clrGreen, 8, 'Arial', '76.4')
            SetTline(0, 'dinap0', 0, Time[cvstart], dinap0, Time[1], dinap0, clrRed, STYLE_DOT, 1, 'dinap0')
            SetTline(0, 'dinap1', 0, Time[cvstart], dinap1, Time[1], dinap1, clrRed, STYLE_DOT, 1, 'dinap1')
            SetTline(0, 'dinap2', 0, Time[cvstart], dinap2, Time[1], dinap2, clrRed, STYLE_DOT, 1, 'dinap2')
            SetTline(0, 'dinap3', 0, Time[cvstart], dinap3, Time[1], dinap3, clrRed, STYLE_DOT, 1, 'dinap3')
            SetTline(0, 'dinap4', 0, Time[cvstart], dinap4, Time[1], dinap4, clrRed, STYLE_DOT, 1, 'dinap4')
            SetTline(0, 'dinap5', 0, Time[cvstart], dinap5, Time[1], dinap5, clrRed, STYLE_DOT, 1, 'dinap5')
        SetTline(0, 'CVSTART', 0, Time[cvstart], high_bar, Time[cvstart], low_bar * Point(), clrBlue, STYLE_SOLID, 1, 'CVSTART')
        SetTline(0, 'CVEND', 0, Time[cvend], high_bar, Time[cvend], low_bar * Point(), clrBlue, STYLE_SOLID, 1, 'CVEND')
        for number in range(1, 10):
            barX = cvend - (swing_time * number)
            name = 'swingend' + _str(number)
            if barX > 0:
                SetTline(0, name, 0, Time[barX + 5], high_bar, Time[barX + 5], low_bar, clrRed, STYLE_DOT, 1, name)
            else:
                ObjectDelete(0, name)
    return rates_total

def CreateTextObj(chart_id, name, nwin, time, price, Color, size, font, text):
    ObjectCreate(chart_id, name, OBJ_TEXT, nwin, time, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_FONTSIZE, size)
    ObjectSetString(chart_id, name, OBJPROP_FONT, font)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, False)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, True)

def SetTextObj(chart_id, name, nwin, time, price, Color, size, font, text):
    if ObjectFind(chart_id, name) == -1:
        CreateTextObj(chart_id, name, nwin, time, price, Color, size, font, text)
    else:
        ObjectCreate(chart_id, name, OBJ_TEXT, nwin, time, price)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)

def CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_TREND, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, False)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY_LEFT, False)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(chart_id, name, OBJPROP_ZORDER, True)

def SetTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FloatIndicator(_MQL5Indicator):
    name = 'float'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Float': 200,  # amount of bars for the trends analysis. The lower the number, the newer the data,
        'use_fibos': True,  # permission Fibonacci levels
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # volume
    }

