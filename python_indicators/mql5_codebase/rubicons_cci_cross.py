"""Rubicons_CCI_Cross — converted from MQL5: MQL5 Indicators/Rubicons_CCI_Cross/Rubicons_CCI_Cross.mq5

Rubicons CCI Cross signal oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [16748574], 2: [36095], 3: [32768], 4: [255]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'CCI', 2: 'EMA', 3: 'Up Signal', 4: 'Down Signal'}, 'levels': [], 'description': ['Rubicons CCI Cross signal oscillator'], 'name': 'Rubicons_CCI_Cross', 'source': 'MQL5 Indicators/Rubicons_CCI_Cross/Rubicons_CCI_Cross.mq5', 'folder': 'Rubicons_CCI_Cross', 'inputs': [{'mql': 'InpPeriodCCI', 'py': 'InpPeriodCCI', 'param': 'InpPeriodCCI', 'type': 'uint', 'default': 10, 'label': 'CCI period', 'sinput': False}, {'mql': 'InpPeriodEMA', 'py': 'InpPeriodEMA', 'param': 'InpPeriodEMA', 'type': 'uint', 'default': 3, 'label': 'EMA period', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 100.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': -100.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodCCI = _input('InpPeriodCCI', 10)  # CCI period
InpPeriodEMA = _input('InpPeriodEMA', 3)  # EMA period
InpOverbought = _input('InpOverbought', 100.0)  # Overbought
InpOversold = _input('InpOversold', -100.0)  # Oversold
BufferCCI = Arr(0, 0.0)
BufferEMA = Arr(0, 0.0)
BufferSigUP = Arr(0, 0.0)
BufferSigDN = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_cci = 0
period_ema = 0
period_max = 0
handle_cci = 0

def OnInit():
    global handle_cci, overbought, oversold, period_cci, period_ema, period_max
    period_cci = (1 if (InpPeriodCCI < 1) else InpPeriodCCI)
    period_ema = (1 if (InpPeriodEMA < 1) else InpPeriodEMA)
    period_max = fmax(period_cci, period_ema)
    overbought = (0.1 if (fabs(InpOverbought) < 0.1) else 100.0 if (InpOverbought > 100.0) else fabs(InpOverbought))
    oversold = (-0.1 if ((-fabs(InpOversold)) > -0.1) else -100.0 if ((-fabs(InpOversold)) < -100.0) else (-fabs(InpOversold)))
    SetIndexBuffer(0, BufferCCI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferEMA, INDICATOR_DATA)
    SetIndexBuffer(2, BufferSigUP, INDICATOR_DATA)
    SetIndexBuffer(3, BufferSigDN, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_ARROW, 241)
    PlotIndexSetInteger(3, PLOT_ARROW, 242)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Rubicons CCI Cross (' + _str(period_cci) + ',' + _str(period_ema) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Oversold')
    ArraySetAsSeries(BufferCCI, True)
    ArraySetAsSeries(BufferEMA, True)
    ArraySetAsSeries(BufferSigUP, True)
    ArraySetAsSeries(BufferSigDN, True)
    ResetLastError()
    handle_cci = iCCI(None, PERIOD_CURRENT, period_cci, PRICE_TYPICAL)
    if handle_cci == INVALID_HANDLE:
        Print('The iCCI(', _str(period_cci), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 2
        ArrayInitialize(BufferCCI, 0)
        ArrayInitialize(BufferSigUP, EMPTY_VALUE)
        ArrayInitialize(BufferSigDN, EMPTY_VALUE)
        ArrayInitialize(BufferEMA, 0)
    count = (rates_total if (limit > 1) else 1)
    ResetLastError()
    copied = CopyBuffer(handle_cci, 0, 0, count, BufferCCI)
    if copied != count:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, period_cci, period_ema, BufferCCI, BufferEMA) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferSigDN[i] = EMPTY_VALUE
        BufferSigUP[i] = BufferSigDN[i]
        if (BufferCCI[i + 1] < oversold and BufferCCI[i] > oversold) and BufferEMA[i] < BufferCCI[i]:
            BufferSigUP[i] = oversold - 40.0
        if (BufferCCI[i + 1] > overbought and BufferCCI[i] < overbought) and BufferEMA[i] > BufferCCI[i]:
            BufferSigDN[i] = overbought + 40.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RubiconsCCICross(_MQL5Indicator):
    name = 'Rubicons_CCI_Cross'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodCCI': 10,  # CCI period
        'InpPeriodEMA': 3,  # EMA period
        'InpOverbought': 100.0,  # Overbought
        'InpOversold': -100.0,  # Oversold
    }

