"""BB_ATR_Oscillator — converted from MQL5: MQL5 Indicators/BB_ATR_Oscillator/BB_ATR_Oscillator.mq5

BB ATR oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'BBands ATR'}, 'levels': [], 'description': ['BB ATR oscillator'], 'name': 'BB_ATR_Oscillator', 'source': 'MQL5 Indicators/BB_ATR_Oscillator/BB_ATR_Oscillator.mq5', 'folder': 'BB_ATR_Oscillator', 'inputs': [{'mql': 'InpPeriodATR', 'py': 'InpPeriodATR', 'param': 'InpPeriodATR', 'type': 'uint', 'default': 14, 'label': 'ATR period', 'sinput': False}, {'mql': 'InpMultiplier', 'py': 'InpMultiplier', 'param': 'InpMultiplier', 'type': 'double', 'default': 2.0, 'label': 'ATR multiplier', 'sinput': False}, {'mql': 'InpPeriodBB', 'py': 'InpPeriodBB', 'param': 'InpPeriodBB', 'type': 'uint', 'default': 20, 'label': 'BB period', 'sinput': False}, {'mql': 'InpDeviationBB', 'py': 'InpDeviationBB', 'param': 'InpDeviationBB', 'type': 'double', 'default': 2.0, 'label': 'BB deviation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodATR = _input('InpPeriodATR', 14)  # ATR period
InpMultiplier = _input('InpMultiplier', 2.0)  # ATR multiplier
InpPeriodBB = _input('InpPeriodBB', 20)  # BB period
InpDeviationBB = _input('InpDeviationBB', 2.0)  # BB deviation
BufferBBATR = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
BufferBBUP = Arr(0, 0.0)
BufferBBDN = Arr(0, 0.0)
deviation = 0.0
multiplier = 0.0
period_atr = 0
period_bb = 0
period_max = 0
handle_atr = 0
handle_bb = 0

def OnInit():
    global deviation, handle_atr, handle_bb, multiplier, period_atr, period_bb, period_max
    period_atr = (1 if (InpPeriodATR < 1) else InpPeriodATR)
    period_bb = (1 if (InpPeriodBB < 1) else InpPeriodBB)
    period_max = fmax(period_atr, period_bb)
    deviation = InpDeviationBB
    multiplier = InpMultiplier
    SetIndexBuffer(0, BufferBBATR, INDICATOR_DATA)
    SetIndexBuffer(1, BufferATR, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferBBUP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferBBDN, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BB ATR Osc (' + _str(period_atr) + ',' + _str(multiplier) + ',' + _str(period_bb) + ',' + _str(deviation) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferBBATR, True)
    ArraySetAsSeries(BufferATR, True)
    ArraySetAsSeries(BufferBBUP, True)
    ArraySetAsSeries(BufferBBDN, True)
    ResetLastError()
    handle_atr = iATR(None, PERIOD_CURRENT, period_atr)
    if handle_atr == INVALID_HANDLE:
        Print('The iATR(', _str(period_atr), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_bb = iBands(None, PERIOD_CURRENT, period_bb, 0, deviation, PRICE_CLOSE)
    if handle_bb == INVALID_HANDLE:
        Print('The iATR(', _str(period_bb), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferBBATR, EMPTY_VALUE)
        ArrayInitialize(BufferATR, 0)
        ArrayInitialize(BufferBBUP, 0)
        ArrayInitialize(BufferBBDN, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_atr, 0, 0, count, BufferATR)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_bb, UPPER_BAND, 0, count, BufferBBUP)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_bb, LOWER_BAND, 0, count, BufferBBDN)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferBBATR[i] = BufferBBUP[i] - BufferBBDN[i] - (BufferATR[i] * multiplier)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BBATROscillator(_MQL5Indicator):
    name = 'BB_ATR_Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodATR': 14,  # ATR period
        'InpMultiplier': 2.0,  # ATR multiplier
        'InpPeriodBB': 20,  # BB period
        'InpDeviationBB': 2.0,  # BB deviation
    }

