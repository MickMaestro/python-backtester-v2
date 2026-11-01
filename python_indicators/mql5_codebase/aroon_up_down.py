"""Aroon_Up_Down — converted from MQL5: MQL5 Indicators/Aroon Up, Down MT5/Aroon_Up_Down.mq5

Aroon Up Down - local top and bottom indicator.
Helps to buy from the bottom and sell from the top.
Copyright: www.Wolfforex.com, 2025; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.Wolfforex.com, 2025', 'version': '1.02', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2, 'indicator_minimum': 0.0}, 'types': {1: 1, 2: 1}, 'colors': {1: [16748574], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {}, 'levels': [], 'description': ['Aroon Up Down - local top and bottom indicator.', 'Helps to buy from the bottom and sell from the top.'], 'name': 'Aroon_Up_Down', 'source': 'MQL5 Indicators/Aroon Up, Down MT5/Aroon_Up_Down.mq5', 'folder': 'Aroon Up, Down MT5', 'inputs': [{'mql': 'AroonPeriod', 'py': 'AroonPeriod', 'param': 'AroonPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'MailAlert', 'py': 'MailAlert', 'param': 'MailAlert', 'type': 'bool', 'default': False, 'label': 'Alerts will be mailed to address set in MT5 options', 'sinput': False}, {'mql': 'SoundAlert', 'py': 'SoundAlert', 'param': 'SoundAlert', 'type': 'bool', 'default': False, 'label': 'Alerts will sound on indicator cross', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
AroonPeriod = _input('AroonPeriod', 14)
MailAlert = _input('MailAlert', False)  # Alerts will be mailed to address set in MT5 options
SoundAlert = _input('SoundAlert', False)  # Alerts will sound on indicator cross
AroonUpBuffer = Arr(0, 0.0)
AroonDnBuffer = Arr(0, 0.0)
LastBars = 0

def OnInit():
    IndicatorSetString(INDICATOR_SHORTNAME, 'Aroon Up Down' + IntegerToString(AroonPeriod))
    SetIndexBuffer(0, AroonUpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, AroonDnBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 200)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, 200)
    IndicatorSetInteger(INDICATOR_DIGITS, 1)

def OnCalculate(rates_total, prev_calculated, time, open, High, Low, close, tick_volume, volume, spread):
    global LastBars
    ArPer = 0
    limit = 0
    i = 0
    UpBarDif = 0
    DnBarDif = 0
    counted_bars = prev_calculated
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArPer = AroonPeriod
    if counted_bars < 0:
        return -1
    if ArPer < 1:
        return -1
    if counted_bars > 0:
        counted_bars -= 1
    limit = rates_total - counted_bars
    i = 0
    for i in range(i, limit):
        HH = ArrayMaximum(High, i, ArPer)
        LL = ArrayMinimum(Low, i, ArPer)
        UpBarDif = i - HH
        DnBarDif = i - LL
        AroonUpBuffer[rates_total - i - 1] = 100 + (_fdiv(100.0, ArPer) * UpBarDif)
        AroonDnBuffer[rates_total - i - 1] = 100 + (_fdiv(100.0, ArPer) * DnBarDif)
        if LastBars != rates_total:
            dt = MqlDateTime()
            TimeCurrent(dt)
            if AroonUpBuffer[0] > AroonDnBuffer[0] and AroonUpBuffer[1] <= AroonDnBuffer[1]:
                if MailAlert:
                    SendMail('Aroon Up & Down Indicator Alert', 'The indicator produced a cross (Blue ABOVE Red) on ' + IntegerToString(dt.year) + '-' + IntegerToString(dt.mon) + '-' + IntegerToString(dt.day) + ' ' + IntegerToString(dt.hour) + ':' + IntegerToString(dt.min))
                if SoundAlert:
                    Alert('Aroon Up & Down produced a cross (Blue ABOVE Red)')
            elif AroonUpBuffer[0] < AroonDnBuffer[0] and AroonUpBuffer[1] >= AroonDnBuffer[1]:
                if MailAlert:
                    SendMail('Aroon Up & Down Indicator Alert', 'The indicator produced a cross (Blue BELOW Red) on ' + IntegerToString(dt.year) + '-' + IntegerToString(dt.mon) + '-' + IntegerToString(dt.day) + ' ' + IntegerToString(dt.hour) + ':' + IntegerToString(dt.min))
                if SoundAlert:
                    Alert('Aroon Up & Down produced a cross (Blue BELOW Red)')
            LastBars = rates_total
    else:
        i = _range_end(i, limit, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AroonUpDown(_MQL5Indicator):
    name = 'Aroon_Up_Down'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'AroonPeriod': 14,
        'MailAlert': False,  # Alerts will be mailed to address set in MT5 options
        'SoundAlert': False,  # Alerts will sound on indicator cross
    }

