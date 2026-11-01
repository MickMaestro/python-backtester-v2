"""sintiks — converted from MQL5: MQL5 Indicators/SinTick/sintiks.mq5

Signals:
Mode 0 = MathSin(tick_volume[i])
Mode 1 = MathSin(tick_volume[i-1])
Copyright: LoopXor; Link: Skype: Loopxor for communication

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'LoopXor', 'link': 'Skype: Loopxor for communication', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 3, 2: 1}, 'colors': {1: [255], 2: [42495]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {}, 'levels': [], 'description': ['', 'Signals:', 'Mode 0 = MathSin(tick_volume[i])', 'Mode 1 = MathSin(tick_volume[i-1])'], 'name': 'sintiks', 'source': 'MQL5 Indicators/SinTick/sintiks.mq5', 'folder': 'SinTick', 'inputs': [{'mql': 'Min_Bars', 'py': 'Min_Bars', 'param': 'Min_Bars', 'type': 'int', 'default': 80, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
indName = '0'  # Indicator Name
ExtMapBuffer0 = Arr(0, 0.0)
ExtMapBuffer1 = Arr(0, 0.0)
Min_Bars = _input('Min_Bars', 80)

def OnInit():
    SetIndexBuffer(0, ExtMapBuffer0, INDICATOR_DATA)
    SetIndexBuffer(1, ExtMapBuffer1, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    Print('', indName, '')
    Print('', indName, ' starts running at: Server Time=', TimeToString(TimeCurrent(), TIME_DATE | TIME_SECONDS), ' Terminal Time=', TimeToString(TimeLocal(), TIME_DATE | TIME_SECONDS))
    Comment('THIS INDICATOR IS MADE: LoopXor ')
    return 0

def OnDeinit(reason):
    Print('M-', Symbol(), ' Custom Indicator deinit')
    Print('OnDeinit', '_Uninitalization reason code =', reason)
    Print('OnDeinit', '_UninitReason =', getUnitReasonText(0))
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < Min_Bars:
        Print('Indicator Warning: A minimum of ', Min_Bars, ' is required to show the Indicator.')
        return 0
    limit = 0
    limit = prev_calculated
    if prev_calculated < Min_Bars:
        limit = Min_Bars
    if prev_calculated == rates_total:
        limit = rates_total - 1
    sum_ = 0.0
    for i in range(limit, rates_total):
        ExtMapBuffer0[i] = MathSin(tick_volume[i])
        ExtMapBuffer1[i] = MathSin(tick_volume[i - 1])
    return rates_total

def getUnitReasonText(reasonCode):
    text = ''
    _sw1 = reasonCode
    if _sw1 == REASON_ACCOUNT:
        text = 'Account was changed'
    elif _sw1 == REASON_CHARTCHANGE:
        text = 'Symbol or timeframe was changed'
    elif _sw1 == REASON_CHARTCLOSE:
        text = 'Chart was closed'
    elif _sw1 == REASON_PARAMETERS:
        text = 'Input-parameter was changed'
    elif _sw1 == REASON_RECOMPILE:
        text = 'Program ' + 'sintiks.mq5' + ' was recompiled'
    elif _sw1 == REASON_REMOVE:
        text = 'Program ' + 'sintiks.mq5' + ' was removed from chart'
    elif _sw1 == REASON_TEMPLATE:
        text = 'New template was applied to chart'
    else:
        text = 'Unknow reason'
    return text


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Sintiks(_MQL5Indicator):
    name = 'sintiks'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Min_Bars': 80,
    }

