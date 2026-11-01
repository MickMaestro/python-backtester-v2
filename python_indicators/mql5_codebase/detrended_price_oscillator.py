"""Detrended Price Oscillator — converted from MQL5: MQL5 Indicators/Detrended Price Oscillator MT5/Detrended Price Oscillator.mq5

Detrended Price Oscillator tries to capture the short-term trend changes.
Indicator's cross with the zero is the best indicator of such a change.
Optional alerts on zero cross available.
Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'version': '1.01', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [0.0], 'description': ['Detrended Price Oscillator tries to capture the short-term trend changes.', "Indicator's cross with the zero is the best indicator of such a change.", 'Optional alerts on zero cross available.'], 'name': 'Detrended Price Oscillator', 'source': 'MQL5 Indicators/Detrended Price Oscillator MT5/Detrended Price Oscillator.mq5', 'folder': 'Detrended Price Oscillator MT5', 'inputs': [{'mql': 'MA_Period', 'py': 'MA_Period', 'param': 'MA_Period', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'BarsToCount', 'py': 'BarsToCount', 'param': 'BarsToCount', 'type': 'int', 'default': 400, 'label': '', 'sinput': False}, {'mql': 'EnableNativeAlerts', 'py': 'EnableNativeAlerts', 'param': 'EnableNativeAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnableEmailAlerts', 'py': 'EnableEmailAlerts', 'param': 'EnableEmailAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'EnablePushAlerts', 'py': 'EnablePushAlerts', 'param': 'EnablePushAlerts', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'TriggerCandle', 'py': 'TriggerCandle', 'param': 'TriggerCandle', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enum_candle_to_check
Current = 0
Previous = 1
_enum('enum_candle_to_check', {0: 'Current', 1: 'Previous'})

# ---- inputs and global variables
MA_Period = _input('MA_Period', 14)
BarsToCount = _input('BarsToCount', 400)
EnableNativeAlerts = _input('EnableNativeAlerts', False)
EnableEmailAlerts = _input('EnableEmailAlerts', False)
EnablePushAlerts = _input('EnablePushAlerts', False)
TriggerCandle = _input('TriggerCandle', Previous)
Shift = 0
MA_handle = 0
LastAlertTime = 0
LastBars = 0
DPO = Arr(0, 0.0)

def OnInit():
    global LastBars, MA_handle, Shift
    IndicatorSetString(INDICATOR_SHORTNAME, 'DPO(' + IntegerToString(MA_Period) + ')')
    SetIndexBuffer(0, DPO, INDICATOR_DATA)
    MA_handle = iMA(Symbol(), Period(), MA_Period, 0, MODE_SMA, PRICE_CLOSE)
    Shift = _idiv(MA_Period, 2) + 1
    LastBars = 0

def OnCalculate(rates_total, prev_calculated, Time, open, high, low, Close, tick_volume, volume, spread):
    global LastAlertTime, LastBars
    if rates_total <= MA_Period:
        return 0
    limit = BarsToCount
    if BarsToCount >= rates_total:
        limit = rates_total
    MA = Arr(0, 0.0)
    if CopyBuffer(MA_handle, 0, 0, rates_total, MA) != rates_total:
        Print('Waiting for MA data...')
        return prev_calculated
    for i in range(rates_total - limit + MA_Period + 1, rates_total):
        DPO[i] = Close[i] - MA[i - Shift]
    if (TriggerCandle > 0 and Time[rates_total - 1] > LastAlertTime) or TriggerCandle == 0:
        if DPO[rates_total - 2 - TriggerCandle] <= 0 and DPO[rates_total - 1 - TriggerCandle] > 0:
            if LastBars != 0:
                NativeText = 'DPO Zero Cross: DPO above zero.'
                Text = 'DPO Zero Cross: ' + Symbol() + ' - ' + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7) + ' - DPO above zero.'
                if EnableNativeAlerts:
                    Alert(NativeText)
                if EnableEmailAlerts:
                    SendMail('DPO Zero Cross Alert - ' + Symbol() + ' - ' + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7), Text)
                if EnablePushAlerts:
                    SendNotification(Text)
            LastAlertTime = Time[rates_total - 1]
        if DPO[rates_total - 2 - TriggerCandle] >= 0 and DPO[rates_total - 1 - TriggerCandle] < 0:
            if LastBars != 0:
                NativeText = 'DPO Zero Cross: DPO below zero.'
                Text = 'DPO Zero Cross: ' + Symbol() + ' - ' + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7) + ' - DPO below zero.'
                if EnableNativeAlerts:
                    Alert(NativeText)
                if EnableEmailAlerts:
                    SendMail('DPO Zero Cross Alert - ' + Symbol() + ' - ' + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7), Text)
                if EnablePushAlerts:
                    SendNotification(Text)
            LastAlertTime = Time[rates_total - 1]
    LastBars = rates_total
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DetrendedPriceOscillator(_MQL5Indicator):
    name = 'Detrended Price Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'MA_Period': 14,
        'BarsToCount': 400,
        'EnableNativeAlerts': False,
        'EnableEmailAlerts': False,
        'EnablePushAlerts': False,
        'TriggerCandle': _Choice({0: 'Current', 1: 'Previous'}, default=1),
    }

