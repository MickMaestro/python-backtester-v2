"""Support and Resistance — converted from MQL5: MQL5 Indicators/Support and Resistance MT5/Support and Resistance.mq5

Blue and red support and resistance levels displayed directly on the chart.
Alerts for close above resistance and close below support.
Copyright: https://t.me/ForexEaPremium; Version: 2.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'https://t.me/ForexEaPremium', 'version': '2.02', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Resistance', 2: 'Support'}, 'levels': [], 'description': ['Blue and red support and resistance levels displayed directly on the chart.', 'Alerts for close above resistance and close below support.'], 'name': 'Support and Resistance', 'source': 'MQL5 Indicators/Support and Resistance MT5/Support and Resistance.mq5', 'folder': 'Support and Resistance MT5', 'inputs': [{'mql': 'EnableNativeAlerts', 'py': 'EnableNativeAlerts', 'param': 'EnableNativeAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnableEmailAlerts', 'py': 'EnableEmailAlerts', 'param': 'EnableEmailAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnablePushAlerts', 'py': 'EnablePushAlerts', 'param': 'EnablePushAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'TriggerCandle', 'py': 'TriggerCandle', 'param': 'TriggerCandle', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enum_candle_to_check
Current = 0
Previous = 1
_enum('enum_candle_to_check', {0: 'Current', 1: 'Previous'})

# ---- inputs and global variables
EnableNativeAlerts = _input('EnableNativeAlerts', False)
EnableEmailAlerts = _input('EnableEmailAlerts', False)
EnablePushAlerts = _input('EnablePushAlerts', False)
TriggerCandle = _input('TriggerCandle', Previous)
Resistance = Arr(0, 0.0)
Support = Arr(0, 0.0)
myFractal = 0
LastAlertTime = 0

def OnInit():
    global myFractal
    PlotIndexSetInteger(0, PLOT_ARROW, 119)
    PlotIndexSetInteger(1, PLOT_ARROW, 119)
    SetIndexBuffer(0, Resistance)
    SetIndexBuffer(1, Support)
    ArraySetAsSeries(Resistance, True)
    ArraySetAsSeries(Support, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 5)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, 5)
    myFractal = iFractals(None, 0)

def OnCalculate(rates_total, prev_calculated, Time, open, High, Low, Close, tick_volume, volume, spread):
    global LastAlertTime
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Close, True)
    ArraySetAsSeries(Time, True)
    FractalUpperBuffer = Arr(0, 0.0)
    FractalLowerBuffer = Arr(0, 0.0)
    CopyBuffer(myFractal, 0, 0, rates_total, FractalUpperBuffer)
    CopyBuffer(myFractal, 1, 0, rates_total, FractalLowerBuffer)
    ArraySetAsSeries(FractalUpperBuffer, True)
    ArraySetAsSeries(FractalLowerBuffer, True)
    for i in range(rates_total - 2, 0 - 1, -1):
        if FractalUpperBuffer[i] != EMPTY_VALUE:
            Resistance[i] = High[i]
        else:
            Resistance[i] = Resistance[i + 1]
        if FractalLowerBuffer[i] != EMPTY_VALUE:
            Support[i] = Low[i]
        else:
            Support[i] = Support[i + 1]
    if (TriggerCandle > 0 and Time[0] > LastAlertTime) or TriggerCandle == 0:
        Text = ""
        TextNative = ""
        if Close[TriggerCandle] > Resistance[TriggerCandle] and Close[TriggerCandle + 1] <= Resistance[TriggerCandle]:
            Text = 'S&R: ' + Symbol() + ' - ' + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7) + ' - Closed above Resistance: ' + DoubleToString(Resistance[TriggerCandle], Digits()) + '.'
            TextNative = 'S&R: Closed above Resistance: ' + DoubleToString(Resistance[TriggerCandle], Digits()) + '.'
            if EnableNativeAlerts:
                Alert(TextNative)
            if EnableEmailAlerts:
                SendMail('S&R Alert', Text)
            if EnablePushAlerts:
                SendNotification(Text)
            LastAlertTime = Time[0]
        if Close[TriggerCandle] < Support[TriggerCandle] and Close[TriggerCandle + 1] >= Support[TriggerCandle]:
            Text = 'S&R: ' + Symbol() + ' - ' + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7) + ' - Closed below Support: ' + DoubleToString(Support[TriggerCandle], Digits()) + '.'
            TextNative = 'S&R: Closed below Support: ' + DoubleToString(Support[TriggerCandle], Digits()) + '.'
            if EnableNativeAlerts:
                Alert(TextNative)
            if EnableEmailAlerts:
                SendMail('S&R Alert', Text)
            if EnablePushAlerts:
                SendNotification(Text)
            LastAlertTime = Time[0]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SupportAndResistance(_MQL5Indicator):
    name = 'Support and Resistance'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'EnableNativeAlerts': False,
        'EnableEmailAlerts': False,
        'EnablePushAlerts': False,
        'TriggerCandle': _Choice({0: 'Current', 1: 'Previous'}, default=1),
    }

