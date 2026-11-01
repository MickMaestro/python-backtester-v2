"""Open_Oscillator — converted from MQL5: MQL5 Indicators/Open_Oscillator/Open_Oscillator.mq5

Open oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [17919], 2: [7451452], 3: [255], 4: [32768]}, 'widths': {1: 1, 2: 1, 3: 2, 4: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Low', 2: 'High', 3: 'Signal Low', 4: 'Signal High'}, 'levels': [], 'description': ['Open oscillator'], 'name': 'Open_Oscillator', 'source': 'MQL5 Indicators/Open_Oscillator/Open_Oscillator.mq5', 'folder': 'Open_Oscillator', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpPeriodSig', 'py': 'InpPeriodSig', 'param': 'InpPeriodSig', 'type': 'uint', 'default': 10, 'label': 'Signal period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpPeriodSig = _input('InpPeriodSig', 10)  # Signal period
BufferLO = Arr(0, 0.0)
BufferHI = Arr(0, 0.0)
BufferSigLO = Arr(0, 0.0)
BufferSigHI = Arr(0, 0.0)
period_hl = 0
period_sig = 0

def OnInit():
    global period_hl, period_sig
    period_hl = (1 if (InpPeriod < 1) else InpPeriod)
    period_sig = (1 if (InpPeriodSig < 1) else InpPeriodSig)
    SetIndexBuffer(0, BufferLO, INDICATOR_DATA)
    SetIndexBuffer(1, BufferHI, INDICATOR_DATA)
    SetIndexBuffer(2, BufferSigLO, INDICATOR_DATA)
    SetIndexBuffer(3, BufferSigHI, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Open oscillator (' + _str(period_hl) + ',' + _str(period_sig) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferLO, True)
    ArraySetAsSeries(BufferHI, True)
    ArraySetAsSeries(BufferSigLO, True)
    ArraySetAsSeries(BufferSigHI, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    if rates_total < fmax(period_hl, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_hl - 1
        ArrayInitialize(BufferLO, EMPTY_VALUE)
        ArrayInitialize(BufferHI, EMPTY_VALUE)
        ArrayInitialize(BufferSigLO, 0)
        ArrayInitialize(BufferSigHI, 0)
    for i in range(limit, 0 - 1, -1):
        bl = Lowest(period_hl, i)
        bh = Highest(period_hl, i)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        BufferLO[i] = open[bl] - open[i]
        BufferHI[i] = open[i] - open[bh]
    if ExponentialMAOnBuffer(rates_total, prev_calculated, period_hl, period_sig, BufferLO, BufferSigLO) == 0:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, period_hl, period_sig, BufferHI, BufferSigHI) == 0:
        return 0
    return rates_total

def Highest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return ((ArrayMaximum(array) + start) if (CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)

def Lowest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    return ((ArrayMinimum(array) + start) if (CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count) else WRONG_VALUE)
    return WRONG_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class OpenOscillator(_MQL5Indicator):
    name = 'Open_Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpPeriodSig': 10,  # Signal period
    }

