"""Basing Candlesticks — converted from MQL5: MQL5 Indicators/Basing Candlesticks MT5/Basing Candlesticks.mq5

Marks candlesticks with body < 50% of overall length (high-low range).
Copyright: www.Wolfforex.com, 2025; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.Wolfforex.com, 2025', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 15}, 'colors': {1: [16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': ['Marks candlesticks with body < 50% of overall length (high-low range).'], 'name': 'Basing Candlesticks', 'source': 'MQL5 Indicators/Basing Candlesticks MT5/Basing Candlesticks.mq5', 'folder': 'Basing Candlesticks MT5', 'inputs': [{'mql': 'Percentage', 'py': 'Percentage', 'param': 'Percentage', 'type': 'int', 'default': 50, 'label': 'Percentage for Basing Candle calculation.', 'sinput': False}, {'mql': 'TriggerCandle', 'py': 'TriggerCandle', 'param': 'TriggerCandle', 'type': 'int', 'default': 1, 'label': 'TriggerCandle: Number of candle to check for alerts.', 'sinput': False}, {'mql': 'EnableNativeAlerts', 'py': 'EnableNativeAlerts', 'param': 'EnableNativeAlerts', 'type': 'bool', 'default': False, 'label': 'EnableNativeAlerts: Alert popup inside platform.', 'sinput': False}, {'mql': 'EnableSoundAlerts', 'py': 'EnableSoundAlerts', 'param': 'EnableSoundAlerts', 'type': 'bool', 'default': False, 'label': 'EnableSoundAlerts: Play a sound on alert.', 'sinput': False}, {'mql': 'EnableEmailAlerts', 'py': 'EnableEmailAlerts', 'param': 'EnableEmailAlerts', 'type': 'bool', 'default': False, 'label': 'EnableEmailAlerts: Send an email on alert.', 'sinput': False}, {'mql': 'EnablePushAlerts', 'py': 'EnablePushAlerts', 'param': 'EnablePushAlerts', 'type': 'bool', 'default': False, 'label': 'EnablePushAlerts: Send a push notification on alert.', 'sinput': False}, {'mql': 'AlertEmailSubject', 'py': 'AlertEmailSubject', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'AlertText', 'py': 'AlertText', 'param': None, 'type': 'string', 'default': '', 'label': '', 'sinput': False}, {'mql': 'SoundFileName', 'py': 'SoundFileName', 'param': None, 'type': 'string', 'default': 'alert.wav', 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Percentage = _input('Percentage', 50)  # Percentage for Basing Candle calculation.
TriggerCandle = _input('TriggerCandle', 1)  # TriggerCandle: Number of candle to check for alerts.
EnableNativeAlerts = _input('EnableNativeAlerts', False)  # EnableNativeAlerts: Alert popup inside platform.
EnableSoundAlerts = _input('EnableSoundAlerts', False)  # EnableSoundAlerts: Play a sound on alert.
EnableEmailAlerts = _input('EnableEmailAlerts', False)  # EnableEmailAlerts: Send an email on alert.
EnablePushAlerts = _input('EnablePushAlerts', False)  # EnablePushAlerts: Send a push notification on alert.
AlertEmailSubject = _input('AlertEmailSubject', '')
AlertText = _input('AlertText', '')
SoundFileName = _input('SoundFileName', 'alert.wav')
H = Arr(0, 0.0)
L = Arr(0, 0.0)
O = Arr(0, 0.0)
C = Arr(0, 0.0)
LastAlertTime = 0

def OnInit():
    global LastAlertTime
    SetIndexBuffer(0, O, INDICATOR_DATA)
    SetIndexBuffer(1, H, INDICATOR_DATA)
    SetIndexBuffer(2, L, INDICATOR_DATA)
    SetIndexBuffer(3, C, INDICATOR_DATA)
    ArraySetAsSeries(O, True)
    ArraySetAsSeries(H, True)
    ArraySetAsSeries(L, True)
    ArraySetAsSeries(C, True)
    LastAlertTime = iTime(Symbol(), Period(), 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, tick_volume, volume, spread):
    global LastAlertTime
    ArraySetAsSeries(Open, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Close, True)
    ArraySetAsSeries(Time, True)
    counted_bars = prev_calculated
    if counted_bars < 0:
        return -1
    if counted_bars > 0:
        counted_bars -= 1
    i = rates_total - counted_bars - 1
    if i == 0:
        i += 1
    while i >= 0:
        length = High[i] - Low[i]
        body = MathAbs(Open[i] - Close[i])
        percentage = float(Percentage) / 100.0
        if length != 0 and _fdiv(body, length) < percentage:
            H[i] = High[i]
            L[i] = Low[i]
            O[i] = Open[i]
            C[i] = Close[i]
        else:
            H[i] = EMPTY_VALUE
            L[i] = EMPTY_VALUE
            O[i] = EMPTY_VALUE
            C[i] = EMPTY_VALUE
        i -= 1
    if Time[0] > LastAlertTime:
        Text = ""
        if H[TriggerCandle] != EMPTY_VALUE:
            Text = AlertText + 'Basing Candle Alert: ' + Symbol() + ' - ' + TF2Str(Period()) + '.'
            if EnableNativeAlerts:
                Alert(Text)
            if EnableEmailAlerts:
                SendMail(AlertEmailSubject + 'Basing Candle Alert', Text)
            if EnableSoundAlerts:
                PlaySound(SoundFileName)
            if EnablePushAlerts:
                SendNotification(Text)
            LastAlertTime = Time[0]
    return rates_total

def TF2Str(period):
    _sw1 = period
    if _sw1 == PERIOD_M1:
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
        return 'MN'
    else:
        return 'Unknown'
    return EnumToString(Period(), 'ENUM_TIMEFRAMES')


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BasingCandlesticks(_MQL5Indicator):
    name = 'Basing Candlesticks'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Percentage': 50,  # Percentage for Basing Candle calculation.
        'TriggerCandle': 1,  # TriggerCandle: Number of candle to check for alerts.
        'EnableNativeAlerts': False,  # EnableNativeAlerts: Alert popup inside platform.
        'EnableSoundAlerts': False,  # EnableSoundAlerts: Play a sound on alert.
        'EnableEmailAlerts': False,  # EnableEmailAlerts: Send an email on alert.
        'EnablePushAlerts': False,  # EnablePushAlerts: Send a push notification on alert.
    }

