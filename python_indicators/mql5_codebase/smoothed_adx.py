"""Smoothed_ADX — converted from MQL5: MQL5 Indicators/Smoothed_ADX/Smoothed_ADX.mq5

Smoothed ADX by John Ehlers indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16711680], 2: [32768], 3: [255]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'SADX', 2: '+SDI', 3: '- SDI'}, 'levels': [], 'description': ['Smoothed ADX by John Ehlers indicator'], 'name': 'Smoothed_ADX', 'source': 'MQL5 Indicators/Smoothed_ADX/Smoothed_ADX.mq5', 'folder': 'Smoothed_ADX', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpAlpha1', 'py': 'InpAlpha1', 'param': 'InpAlpha1', 'type': 'double', 'default': 0.25, 'label': 'Primary smoothing factor', 'sinput': False}, {'mql': 'InpAlpha2', 'py': 'InpAlpha2', 'param': 'InpAlpha2', 'type': 'double', 'default': 0.33, 'label': 'Secondary smoothing factor', 'sinput': False}, {'mql': 'InpLevStrong', 'py': 'InpLevStrong', 'param': 'InpLevStrong', 'type': 'double', 'default': 40.0, 'label': 'Strong trend level', 'sinput': False}, {'mql': 'InpLevWeak', 'py': 'InpLevWeak', 'param': 'InpLevWeak', 'type': 'double', 'default': 20.0, 'label': 'Weak trend level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpAlpha1 = _input('InpAlpha1', 0.25)  # Primary smoothing factor
InpAlpha2 = _input('InpAlpha2', 0.33)  # Secondary smoothing factor
InpLevStrong = _input('InpLevStrong', 40.0)  # Strong trend level
InpLevWeak = _input('InpLevWeak', 20.0)  # Weak trend level
BufferSDIP = Arr(0, 0.0)
BufferSDIM = Arr(0, 0.0)
BufferSADX = Arr(0, 0.0)
BufferDIPtmp = Arr(0, 0.0)
BufferDIMtmp = Arr(0, 0.0)
BufferADXtmp = Arr(0, 0.0)
BufferDIP = Arr(0, 0.0)
BufferDIM = Arr(0, 0.0)
BufferADX = Arr(0, 0.0)
alpha1 = 0.0
alpha2 = 0.0
strong = 0.0
weak = 0.0
period = 0
handle_adx = 0

def OnInit():
    global alpha1, alpha2, handle_adx, period, strong, weak
    period = (1 if (InpPeriod < 1) else InpPeriod)
    alpha1 = (0 if (InpAlpha1 < 0) else InpAlpha1)
    alpha2 = (0.109 if (InpAlpha2 < 0.109) else InpAlpha2)
    strong = (100.0 if (InpLevStrong > 100.0) else 0.1 if (InpLevStrong < 0.1) else InpLevStrong)
    weak = ((strong - 0.1) if (InpLevWeak >= strong) else 0 if (InpLevWeak < 0) else InpLevWeak)
    SetIndexBuffer(0, BufferSADX, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSDIP, INDICATOR_DATA)
    SetIndexBuffer(2, BufferSDIM, INDICATOR_DATA)
    SetIndexBuffer(3, BufferDIPtmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferDIMtmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferADXtmp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferDIP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferDIM, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferADX, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Smoothed ADX (' + _str(period) + ',' + DoubleToString(alpha1, 2) + ',' + DoubleToString(alpha2, 2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, strong)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, weak)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    PlotIndexSetString(0, PLOT_LABEL, 'SADX(' + _str(period) + ')')
    ArraySetAsSeries(BufferSDIP, True)
    ArraySetAsSeries(BufferSDIM, True)
    ArraySetAsSeries(BufferSADX, True)
    ArraySetAsSeries(BufferDIPtmp, True)
    ArraySetAsSeries(BufferDIMtmp, True)
    ArraySetAsSeries(BufferADXtmp, True)
    ArraySetAsSeries(BufferDIP, True)
    ArraySetAsSeries(BufferDIM, True)
    ArraySetAsSeries(BufferADX, True)
    ResetLastError()
    handle_adx = iADX(None, PERIOD_CURRENT, period)
    if handle_adx == INVALID_HANDLE:
        Print('The iADX (', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferSDIP, EMPTY_VALUE)
        ArrayInitialize(BufferSDIM, EMPTY_VALUE)
        ArrayInitialize(BufferSADX, EMPTY_VALUE)
        ArrayInitialize(BufferDIPtmp, 0)
        ArrayInitialize(BufferDIMtmp, 0)
        ArrayInitialize(BufferADXtmp, 0)
        ArrayInitialize(BufferDIP, 0)
        ArrayInitialize(BufferDIM, 0)
        ArrayInitialize(BufferADX, 0)
    count = (rates_total if (limit > 0) else 1)
    copied = 0
    copied = CopyBuffer(handle_adx, MAIN_LINE, 0, count, BufferADX)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_adx, PLUSDI_LINE, 0, count, BufferDIP)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_adx, MINUSDI_LINE, 0, count, BufferDIM)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferDIPtmp[i] = (2.0 * BufferDIP[i]) + ((alpha1 - 2.0) * BufferDIP[i + 1]) + ((1.0 - alpha1) * BufferDIPtmp[i + 1])
        BufferDIMtmp[i] = (2.0 * BufferDIM[i]) + ((alpha1 - 2.0) * BufferDIM[i + 1]) + ((1.0 - alpha1) * BufferDIMtmp[i + 1])
        BufferADXtmp[i] = (2.0 * BufferADX[i]) + ((alpha1 - 2.0) * BufferADX[i + 1]) + ((1.0 - alpha1) * BufferADXtmp[i + 1])
        BufferSDIP[i] = (alpha2 * BufferDIPtmp[i]) + ((1.0 - alpha2) * BufferSDIP[i + 1])
        BufferSDIM[i] = (alpha2 * BufferDIMtmp[i]) + ((1.0 - alpha2) * BufferSDIM[i + 1])
        BufferSADX[i] = (alpha2 * BufferADXtmp[i]) + ((1.0 - alpha2) * BufferSADX[i + 1])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SmoothedADX(_MQL5Indicator):
    name = 'Smoothed_ADX'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpAlpha1': 0.25,  # Primary smoothing factor
        'InpAlpha2': 0.33,  # Secondary smoothing factor
        'InpLevStrong': 40.0,  # Strong trend level
        'InpLevWeak': 20.0,  # Weak trend level
    }

