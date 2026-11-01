"""Bollinger Squeeze Basic — converted from MQL5: MQL5 Indicators/Bollinger Squeeze Basic MT5/Bollinger Squeeze Basic.mq5

Bollinger Squeeze Basic shows the change of momentum histogram and BB / Keltner channel dots.
Red dots are shown when Bollinger bands are outside of the Keltner channel.
Blue dots are shown when Bollinger bands are inside the Keltner channel.
Copyright: www.Wolfforex.com, 2025; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.Wolfforex.com, 2025', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 10, 2: 12}, 'colors': {1: [3329330, 6053069, 9498256, 12695295], 2: [16711680, 255]}, 'widths': {1: 2, 2: 1}, 'styles': {}, 'labels': {1: 'Momentum Histo', 2: 'BB/Keltner'}, 'levels': [], 'description': ['Bollinger Squeeze Basic shows the change of momentum histogram and BB / Keltner channel dots.', 'Red dots are shown when Bollinger bands are outside of the Keltner channel.', 'Blue dots are shown when Bollinger bands are inside the Keltner channel.'], 'name': 'Bollinger Squeeze Basic', 'source': 'MQL5 Indicators/Bollinger Squeeze Basic MT5/Bollinger Squeeze Basic.mq5', 'folder': 'Bollinger Squeeze Basic MT5', 'inputs': [{'mql': 'MaxBars', 'py': 'MaxBars', 'param': 'MaxBars', 'type': 'int', 'default': 300, 'label': '', 'sinput': False}, {'mql': 'BB_Period', 'py': 'BB_Period', 'param': 'BB_Period', 'type': 'int', 'default': 20, 'label': 'BB Period', 'sinput': False}, {'mql': 'BB_Deviation', 'py': 'BB_Deviation', 'param': 'BB_Deviation', 'type': 'double', 'default': 2.0, 'label': 'BB Deviation', 'sinput': False}, {'mql': 'Keltner_Period', 'py': 'Keltner_Period', 'param': 'Keltner_Period', 'type': 'int', 'default': 20, 'label': 'Keltner Period', 'sinput': False}, {'mql': 'Keltner_Factor', 'py': 'Keltner_Factor', 'param': 'Keltner_Factor', 'type': 'double', 'default': 1.5, 'label': 'Keltner Factor', 'sinput': False}, {'mql': 'Momentum_Period', 'py': 'Momentum_Period', 'param': 'Momentum_Period', 'type': 'int', 'default': 12, 'label': 'Momentum Period', 'sinput': False}, {'mql': 'EnableNativeAlerts', 'py': 'EnableNativeAlerts', 'param': 'EnableNativeAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnableEmailAlerts', 'py': 'EnableEmailAlerts', 'param': 'EnableEmailAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnablePushAlerts', 'py': 'EnablePushAlerts', 'param': 'EnablePushAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'TriggerCandle', 'py': 'TriggerCandle', 'param': 'TriggerCandle', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enum_candle_to_check
Current = 0
Previous = 1
_enum('enum_candle_to_check', {0: 'Current', 1: 'Previous'})

# ---- inputs and global variables
MaxBars = _input('MaxBars', 300)
BB_Period = _input('BB_Period', 20)  # BB Period
BB_Deviation = _input('BB_Deviation', 2.0)  # BB Deviation
Keltner_Period = _input('Keltner_Period', 20)  # Keltner Period
Keltner_Factor = _input('Keltner_Factor', 1.5)  # Keltner Factor
Momentum_Period = _input('Momentum_Period', 12)  # Momentum Period
EnableNativeAlerts = _input('EnableNativeAlerts', False)
EnableEmailAlerts = _input('EnableEmailAlerts', False)
EnablePushAlerts = _input('EnablePushAlerts', False)
TriggerCandle = _input('TriggerCandle', Previous)
Histogram = Arr(0, 0.0)
Histogram_Color = Arr(0, 0.0)
Arrows = Arr(0, 0.0)
Arrows_Color = Arr(0, 0.0)
Momentum_Buffer = Arr(0, 0.0)
ATR_Buffer = Arr(0, 0.0)
StdDev_Buffer = Arr(0, 0.0)
Momentum_Handle = 0
ATR_Handle = 0
StdDev_Handle = 0
LastAlertTime = 0
LastAlertDirection = 0

def OnInit():
    global ATR_Handle, Momentum_Handle, StdDev_Handle
    SetIndexBuffer(0, Histogram, INDICATOR_DATA)
    SetIndexBuffer(1, Histogram_Color, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, Arrows, INDICATOR_DATA)
    SetIndexBuffer(3, Arrows_Color, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_ARROW, 167)
    ArraySetAsSeries(Histogram, True)
    ArraySetAsSeries(Histogram_Color, True)
    ArraySetAsSeries(Arrows, True)
    ArraySetAsSeries(Arrows_Color, True)
    Momentum_Handle = iMomentum(Symbol(), Period(), Momentum_Period, PRICE_CLOSE)
    ATR_Handle = iATR(Symbol(), Period(), Keltner_Period)
    StdDev_Handle = iStdDev(Symbol(), Period(), BB_Period, MODE_SMA, 0, PRICE_CLOSE)
    ArraySetAsSeries(Momentum_Buffer, True)
    ArraySetAsSeries(ATR_Buffer, True)
    ArraySetAsSeries(StdDev_Buffer, True)

def OnCalculate(rates_total, prev_calculated, Time, open, high, low, close, tick_volume, volume, spread):
    global LastAlertDirection, LastAlertTime
    ArraySetAsSeries(Time, True)
    limit = MaxBars
    if limit > rates_total:
        limit = rates_total
    d = 0.0
    prev_d = 0.0
    if CopyBuffer(Momentum_Handle, 0, 0, limit, Momentum_Buffer) != limit:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, limit, ATR_Buffer) != limit:
        return 0
    if CopyBuffer(StdDev_Handle, 0, 0, limit, StdDev_Buffer) != limit:
        return 0
    for shift in range(limit - 1, 0 - 1, -1):
        d = Momentum_Buffer[shift] - 100
        if d > 0:
            if d >= prev_d:
                Histogram_Color[shift] = 0.0
            else:
                Histogram_Color[shift] = 2.0
            Histogram[shift] = d
        elif d < 0:
            if d <= prev_d:
                Histogram_Color[shift] = 1.0
            else:
                Histogram_Color[shift] = 3.0
            Histogram[shift] = d
        else:
            Histogram[shift] = 0.0
            Histogram_Color[shift] = 0.0
        prev_d = d
        diff = ATR_Buffer[shift] * Keltner_Factor
        std = StdDev_Buffer[shift]
        bbs = _fdiv(BB_Deviation * std, diff)
        Arrows[shift] = 0.0
        if bbs < 1:
            Arrows_Color[shift] = 0.0
        else:
            Arrows_Color[shift] = 1.0
    if (TriggerCandle > 0 and Time[0] > LastAlertTime) or TriggerCandle == 0:
        Text = ""
        if Arrows_Color[TriggerCandle] == 1 and LastAlertDirection != 1:
            if LastAlertDirection != 0:
                Text = 'BB Squeeze: ' + Symbol() + ' - ' + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7) + ' - BB Outside Keltner.'
                if EnableNativeAlerts:
                    Alert(Text)
                if EnableEmailAlerts:
                    SendMail('BB Squeeze Alert', Text)
                if EnablePushAlerts:
                    SendNotification(Text)
            LastAlertTime = Time[0]
            LastAlertDirection = 1
        if Arrows_Color[TriggerCandle] == 0 and LastAlertDirection != -1:
            if LastAlertDirection != 0:
                Text = 'BB Squeeze: ' + Symbol() + ' - ' + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7) + ' - BB Inside Keltner.'
                if EnableNativeAlerts:
                    Alert(Text)
                if EnableEmailAlerts:
                    SendMail('BB Squeeze Alert', Text)
                if EnablePushAlerts:
                    SendNotification(Text)
            LastAlertTime = Time[0]
            LastAlertDirection = -1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BollingerSqueezeBasic(_MQL5Indicator):
    name = 'Bollinger Squeeze Basic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'MaxBars': 300,
        'BB_Period': 20,  # BB Period
        'BB_Deviation': 2.0,  # BB Deviation
        'Keltner_Period': 20,  # Keltner Period
        'Keltner_Factor': 1.5,  # Keltner Factor
        'Momentum_Period': 12,  # Momentum Period
        'EnableNativeAlerts': False,
        'EnableEmailAlerts': False,
        'EnablePushAlerts': False,
        'TriggerCandle': _Choice({0: 'Current', 1: 'Previous'}, default=1),
    }

