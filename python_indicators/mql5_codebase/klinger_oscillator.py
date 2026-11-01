"""Klinger_Oscillator — converted from MQL5: MQL5 Indicators/Klinger_Oscillator/Klinger_Oscillator.mq5

Klinger Oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Klinger', 2: 'Signal'}, 'levels': [], 'description': ['Klinger Oscillator'], 'name': 'Klinger_Oscillator', 'source': 'MQL5 Indicators/Klinger_Oscillator/Klinger_Oscillator.mq5', 'folder': 'Klinger_Oscillator', 'inputs': [{'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 34, 'label': 'Fast period', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 55, 'label': 'Slow period', 'sinput': False}, {'mql': 'InpPeriodSig', 'py': 'InpPeriodSig', 'param': 'InpPeriodSig', 'type': 'uint', 'default': 13, 'label': 'Signal period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodFast = _input('InpPeriodFast', 34)  # Fast period
InpPeriodSlow = _input('InpPeriodSlow', 55)  # Slow period
InpPeriodSig = _input('InpPeriodSig', 13)  # Signal period
BufferKlinger = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferDM = Arr(0, 0.0)
BufferCM = Arr(0, 0.0)
BufferTR = Arr(0, 0.0)
BufferVF = Arr(0, 0.0)
BufferAvgFVF = Arr(0, 0.0)
BufferAvgSVF = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period_fast = 0
period_slow = 0
period_max = 0
period_sig = 0
handle_ma = 0

def OnInit():
    global handle_ma, period_fast, period_max, period_sig, period_slow
    period_fast = (2 if (InpPeriodFast < 2) else InpPeriodFast)
    period_slow = (2 if (InpPeriodSlow < 2) else InpPeriodSlow)
    period_sig = (2 if (InpPeriodSig < 2) else InpPeriodSig)
    period_max = fmax(period_fast, fmax(period_slow, period_sig))
    SetIndexBuffer(0, BufferKlinger, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(2, BufferDM, INDICATOR_DATA)
    SetIndexBuffer(3, BufferCM, INDICATOR_DATA)
    SetIndexBuffer(4, BufferTR, INDICATOR_DATA)
    SetIndexBuffer(5, BufferVF, INDICATOR_DATA)
    SetIndexBuffer(6, BufferAvgFVF, INDICATOR_DATA)
    SetIndexBuffer(7, BufferAvgSVF, INDICATOR_DATA)
    SetIndexBuffer(8, BufferMA, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Klinger Oscillator (' + _str(period_fast) + ',' + _str(period_slow) + ',' + _str(period_sig) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetString(0, PLOT_LABEL, 'Klinger(' + _str(period_fast) + ',' + _str(period_slow) + ')')
    PlotIndexSetString(1, PLOT_LABEL, 'Signal(' + _str(period_sig) + ')')
    ArraySetAsSeries(BufferKlinger, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferDM, True)
    ArraySetAsSeries(BufferCM, True)
    ArraySetAsSeries(BufferTR, True)
    ArraySetAsSeries(BufferVF, True)
    ArraySetAsSeries(BufferAvgFVF, True)
    ArraySetAsSeries(BufferAvgSVF, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, PRICE_TYPICAL)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) by PRICE_TYPICAL object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferKlinger, 0)
        ArrayInitialize(BufferSignal, 0)
        ArrayInitialize(BufferDM, 0)
        ArrayInitialize(BufferCM, 0)
        ArrayInitialize(BufferTR, 0)
        ArrayInitialize(BufferVF, 0)
        ArrayInitialize(BufferAvgFVF, 0)
        ArrayInitialize(BufferAvgSVF, 0)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferTR[i] = 0.0
        BufferCM[i] = 0.0
        BufferDM[i] = high[i] - low[i]
        BufferTR[i] = (1 if (BufferMA[i] > BufferMA[i + 1]) else -1 if (BufferMA[i] < BufferMA[i + 1]) else BufferTR[i + 1])
        BufferCM[i] = ((BufferCM[i] + BufferDM[i]) if (BufferTR[i] == BufferTR[i + 1]) else (BufferDM[i + 1] + BufferDM[i]))
        BufferVF[i] = (0 if (BufferCM[i] == 0) else (tick_volume[i] * fabs(_fdiv(2.0 * BufferDM[i], BufferCM[i]) + 1) * BufferTR[i] * 100.0))
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_fast, BufferVF, BufferAvgFVF) == 0:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_slow, BufferVF, BufferAvgSVF) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferKlinger[i] = BufferAvgFVF[i] - BufferAvgSVF[i]
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sig, BufferKlinger, BufferSignal) == 0:
        return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KlingerOscillator(_MQL5Indicator):
    name = 'Klinger_Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFast': 34,  # Fast period
        'InpPeriodSlow': 55,  # Slow period
        'InpPeriodSig': 13,  # Signal period
    }

