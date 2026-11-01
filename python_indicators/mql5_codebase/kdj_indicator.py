"""KDJ Indicator — converted from MQL5: MQL5 Indicators/KDJ Indicator/KDJ Indicator.mq5

Copyright: senlin ge 20080219; Version: 1.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'senlin ge 20080219', 'version': '1.000', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 3}, 'colors': {1: [15624315]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'KDC'}, 'levels': [], 'description': [], 'name': 'KDJ Indicator', 'source': 'MQL5 Indicators/KDJ Indicator/KDJ Indicator.mq5', 'folder': 'KDJ Indicator', 'inputs': [{'mql': 'M1', 'py': 'M1', 'param': 'M1', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'M2', 'py': 'M2', 'param': 'M2', 'type': 'int', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'KdjPeriod', 'py': 'KdjPeriod', 'param': 'KdjPeriod', 'type': 'int', 'default': 30, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
KDCBuffer = Arr(0, 0.0)
RSVBuffer = Arr(0, 0.0)
KBuffer = Arr(0, 0.0)
DBuffer = Arr(0, 0.0)
M1 = _input('M1', 3)
M2 = _input('M2', 6)
KdjPeriod = _input('KdjPeriod', 30)

def OnInit():
    if M2 >= KdjPeriod:
        Print('The parameter "M2" can not be greater than or equal to "KdjPeriod"')
        return INIT_PARAMETERS_INCORRECT
    if M1 >= M2:
        Print('The parameter "M1" can not be greater than or equal to "M2"')
        return INIT_PARAMETERS_INCORRECT
    if (M1 <= 0 or M2 <= 0) or KdjPeriod <= 0:
        Print('The parameter can not be less than or equal to zero')
        return INIT_PARAMETERS_INCORRECT
    SetIndexBuffer(0, KDCBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, RSVBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, KBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, DBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'KDJ(' + _str(M1) + ',' + _str(M2) + ',' + _str(KdjPeriod) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = prev_calculated - 1
    if prev_calculated == 0:
        limit = 0
    for i in range(limit, rates_total):
        if i < KdjPeriod:
            RSVBuffer[i] = 50.0
            KBuffer[i] = 50.0
            DBuffer[i] = 50.0
            KDCBuffer[i] = 50.0
        else:
            MaxHigh = high[ArrayMaximum(high, i - KdjPeriod, KdjPeriod)]
            MinLow = low[ArrayMinimum(low, i - KdjPeriod, KdjPeriod)]
            if (MaxHigh - MinLow) != 0.0:
                RSVBuffer[i] = _fdiv(close[i] - MinLow, MaxHigh - MinLow) * 100.0
            else:
                RSVBuffer[i] = 1.0
            sumK = 0.0
            for j in range(i - M1, i):
                sumK += RSVBuffer[j]
            KBuffer[i] = sumK / M1
            sumD = 0.0
            for j in range(i - M2, i):
                sumD += KBuffer[j]
            DBuffer[i] = sumD / M2
            KDCBuffer[i] = KBuffer[i] - DBuffer[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KDJIndicator(_MQL5Indicator):
    name = 'KDJ Indicator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'M1': 3,
        'M2': 6,
        'KdjPeriod': 30,
    }

