"""BB_MACD — converted from MQL5: MQL5 Indicators/BB MACD indicator MT5/BB_MACD.mq5

An advanced version of MACD indicator for trend change detection.
Copyright: www.Wolfforex.com, 2025; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.Wolfforex.com, 2025', 'version': '1.02', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 3}, 'types': {1: 12, 2: 1, 3: 1}, 'colors': {1: [65280, 16711935], 2: [16711680], 3: [255]}, 'widths': {1: 0, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'bbMACD', 2: 'Upper band', 3: 'Lower band'}, 'levels': [], 'description': ['An advanced version of MACD indicator for trend change detection.'], 'name': 'BB_MACD', 'source': 'MQL5 Indicators/BB MACD indicator MT5/BB_MACD.mq5', 'folder': 'BB MACD indicator MT5', 'inputs': [{'mql': 'FastLen', 'py': 'FastLen', 'param': 'FastLen', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'SlowLen', 'py': 'SlowLen', 'param': 'SlowLen', 'type': 'int', 'default': 26, 'label': '', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'barsCount', 'py': 'barsCount', 'param': 'barsCount', 'type': 'int', 'default': 400, 'label': '', 'sinput': False}, {'mql': 'StDv', 'py': 'StDv', 'param': 'StDv', 'type': 'double', 'default': 2.5, 'label': '', 'sinput': False}, {'mql': 'EnableNativeAlerts', 'py': 'EnableNativeAlerts', 'param': 'EnableNativeAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnableSoundAlerts', 'py': 'EnableSoundAlerts', 'param': 'EnableSoundAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnableEmailAlerts', 'py': 'EnableEmailAlerts', 'param': 'EnableEmailAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnablePushAlerts', 'py': 'EnablePushAlerts', 'param': 'EnablePushAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'SoundFileName', 'py': 'SoundFileName', 'param': None, 'type': 'string', 'default': 'alert.wav', 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FastLen = _input('FastLen', 12)
SlowLen = _input('SlowLen', 26)
Length = _input('Length', 10)
barsCount = _input('barsCount', 400)
StDv = _input('StDv', 2.5)
EnableNativeAlerts = _input('EnableNativeAlerts', False)
EnableSoundAlerts = _input('EnableSoundAlerts', False)
EnableEmailAlerts = _input('EnableEmailAlerts', False)
EnablePushAlerts = _input('EnablePushAlerts', False)
SoundFileName = _input('SoundFileName', 'alert.wav')
ExtMapBuffer1 = Arr(0, 0.0)  # bbMACD
ExtMapBuffer2 = Arr(0, 0.0)  # bbMACD color
ExtMapBuffer3 = Arr(0, 0.0)  # Upper band
ExtMapBuffer4 = Arr(0, 0.0)  # Lower band
ExtMapBuffer5 = Arr(0, 0.0)  # Data for "iMAOnArray()"
MABuff1 = Arr(0, 0.0)
MABuff2 = Arr(0, 0.0)
bbMACD = Arr(0, 0.0)
Oldest_bbMACD = 0  # To avoid calculating EMA using bbMACD older than this.
LastAlertTime = 0

def OnInit():
    global LastAlertTime, Oldest_bbMACD
    IndicatorSetString(INDICATOR_SHORTNAME, 'BB MACD(' + IntegerToString(FastLen) + ',' + IntegerToString(SlowLen) + ',' + IntegerToString(Length) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    SetIndexBuffer(0, ExtMapBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ExtMapBuffer2, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ExtMapBuffer3, INDICATOR_DATA)
    SetIndexBuffer(3, ExtMapBuffer4, INDICATOR_DATA)
    SetIndexBuffer(4, ExtMapBuffer5, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, MABuff1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, MABuff2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, bbMACD, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(ExtMapBuffer1, True)
    ArraySetAsSeries(ExtMapBuffer2, True)
    ArraySetAsSeries(ExtMapBuffer3, True)
    ArraySetAsSeries(ExtMapBuffer4, True)
    ArraySetAsSeries(ExtMapBuffer5, True)
    ArraySetAsSeries(MABuff1, True)
    ArraySetAsSeries(MABuff2, True)
    ArraySetAsSeries(bbMACD, True)
    PlotIndexSetInteger(0, PLOT_ARROW, 108)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    if barsCount == 0:
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Length)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, Length)
        PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, Length)
    Oldest_bbMACD = 0
    LastAlertTime = 0

def OnCalculate(rates_total, prev_calculated, Time, open, high, low, close, tick_volume, volume, spread):
    global LastAlertTime, Oldest_bbMACD
    limit = 0
    if rates_total < Length:
        Print('Not enough bars!')
        return -1
    counted_bars = prev_calculated
    if counted_bars < 0:
        return -1
    if counted_bars > 0:
        counted_bars -= 1
    ArraySetAsSeries(Time, True)
    if barsCount > 0:
        limit = MathMin(rates_total - counted_bars, barsCount)
    else:
        limit = rates_total - counted_bars
    if barsCount > 0:
        draw_begin = rates_total - barsCount + Length
        if draw_begin < Length:
            draw_begin = Length
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, draw_begin)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, draw_begin)
        PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, draw_begin)
    myMA = iMA(None, 0, FastLen, 0, MODE_EMA, PRICE_CLOSE)
    if CopyBuffer(myMA, 0, 0, rates_total, MABuff1) != rates_total:
        return 0
    myMA = iMA(None, 0, SlowLen, 0, MODE_EMA, PRICE_CLOSE)
    if CopyBuffer(myMA, 0, 0, rates_total, MABuff2) != rates_total:
        return 0
    for i in range(0, limit):
        bbMACD[i] = MABuff1[i] - MABuff2[i]
    if (limit - 1) > Oldest_bbMACD:
        Oldest_bbMACD = limit - 1
    CalculateEMA(limit, Length, bbMACD)
    if barsCount > 0:
        if limit > (barsCount - Length):
            limit = barsCount - Length
    if limit > (rates_total - Length):
        limit = rates_total - Length
    for i in range(0, limit):
        avg = ExtMapBuffer5[i]
        sDev = StdDevFunc(i, Length, bbMACD)
        ExtMapBuffer1[i] = bbMACD[i]
        if bbMACD[i] > bbMACD[i + 1]:
            ExtMapBuffer2[i] = 0.0
        elif bbMACD[i] < bbMACD[i + 1]:
            ExtMapBuffer2[i] = 1.0
        ExtMapBuffer3[i] = avg + (StDv * sDev)
        ExtMapBuffer4[i] = avg - (StDv * sDev)
        if (i == 1 and LastAlertTime != Time[1]) and ExtMapBuffer1[i + 1] == bbMACD[i + 1]:
            if ExtMapBuffer2[i] == 0 and ExtMapBuffer2[i + 1] == 1:
                Text = Symbol() + ' - ' + EnumToString(Period(), 'ENUM_TIMEFRAMES') + ' - BB_MACD: from DOWN to UP @ ' + TimeToString(Time[i]) + '.'
                if EnableNativeAlerts:
                    Alert(Text)
                if EnableEmailAlerts:
                    SendMail(Text, Text)
                if EnableSoundAlerts:
                    PlaySound(SoundFileName)
                if EnablePushAlerts:
                    SendNotification(Text)
                LastAlertTime = Time[i]
            elif ExtMapBuffer2[i] == 1 and ExtMapBuffer2[i + 1] == 0:
                Text = Symbol() + ' - ' + EnumToString(Period(), 'ENUM_TIMEFRAMES') + ' - BB_MACD: from UP to DOWN @ ' + TimeToString(Time[i]) + '.'
                if EnableNativeAlerts:
                    Alert(Text)
                if EnableEmailAlerts:
                    SendMail(Text, Text)
                if EnableSoundAlerts:
                    PlaySound(SoundFileName)
                if EnablePushAlerts:
                    SendNotification(Text)
                LastAlertTime = Time[i]
    return rates_total

def CalculateEMA(begin, period, price):
    SmoothFactor = _fdiv(2.0, 1.0 + period)
    start = 0
    if begin == (Oldest_bbMACD + 1):
        ExtMapBuffer5[Oldest_bbMACD] = price[Oldest_bbMACD]
        start = Oldest_bbMACD - 1
    else:
        start = begin
    for i in range(start, 0 - 1, -1):
        ExtMapBuffer5[i] = (price[i] * SmoothFactor) + (ExtMapBuffer5[i + 1] * (1.0 - SmoothFactor))

def StdDevFunc(position, period, price):
    dTmp = 0.0
    for i in range(0, period):
        dTmp += MathPow(price[position + i] - ExtMapBuffer5[position], 2)
    dTmp = MathSqrt(_fdiv(dTmp, period))
    return dTmp


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BBMACD(_MQL5Indicator):
    name = 'BB_MACD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'FastLen': 12,
        'SlowLen': 26,
        'Length': 10,
        'barsCount': 400,
        'StDv': 2.5,
        'EnableNativeAlerts': False,
        'EnableSoundAlerts': False,
        'EnableEmailAlerts': False,
        'EnablePushAlerts': False,
    }

