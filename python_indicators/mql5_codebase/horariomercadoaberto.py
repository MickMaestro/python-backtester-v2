"""horariomercadoaberto — converted from MQL5: MQL5 Indicators/Mercado Aberto/horariomercadoaberto.mq5

Copyright: Copyright 2013, MEH Soluзхes em Informбtica; Link: http://www.meh.com.br; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2013, MEH Soluзхes em Informбtica', 'link': 'http://www.meh.com.br', 'version': '1.00', 'window': 'separate', 'indicator_minimum': 0.0, 'indicator_maximum': 2.0, 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 5}, 'colors': {1: [65280]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'HorarioMercado'}, 'levels': [], 'description': [], 'name': 'horariomercadoaberto', 'source': 'MQL5 Indicators/Mercado Aberto/horariomercadoaberto.mq5', 'folder': 'Mercado Aberto', 'inputs': [{'mql': 'StartHour', 'py': 'StartHour', 'param': 'StartHour', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'StartMinute', 'py': 'StartMinute', 'param': 'StartMinute', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'StopHour', 'py': 'StopHour', 'param': 'StopHour', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'StopMinute', 'py': 'StopMinute', 'param': 'StopMinute', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
StartHour = _input('StartHour', 10)
StartMinute = _input('StartMinute', 0)
StopHour = _input('StopHour', 14)
StopMinute = _input('StopMinute', 0)
SessionBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, SessionBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    start = 0
    if prev_calculated == 0:
        start = 0
    else:
        start = prev_calculated - 1
    for i in range(start, rates_total):
        if TimeSession(StartHour, StartMinute, StopHour, StopMinute, time[i]):
            SessionBuffer[i] = 1.0
        else:
            SessionBuffer[i] = EMPTY_VALUE
    return rates_total

def TimeSession(aStartHour, aStartMinute, aStopHour, aStopMinute, aTimeCur):
    StartTime = (3600 * aStartHour) + (60 * aStartMinute)
    StopTime = (3600 * aStopHour) + (60 * aStopMinute)
    aTimeCur = _imod(aTimeCur, 86400)
    if StopTime < StartTime:
        if aTimeCur >= StartTime or aTimeCur < StopTime:
            return True
    else:
        if aTimeCur >= StartTime and aTimeCur < StopTime:
            return True
    return False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Horariomercadoaberto(_MQL5Indicator):
    name = 'horariomercadoaberto'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'StartHour': 10,
        'StartMinute': 0,
        'StopHour': 14,
        'StopMinute': 0,
    }
    y_range = (0.0, 2.0)

