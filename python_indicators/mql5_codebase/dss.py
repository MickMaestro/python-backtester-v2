"""DSS — converted from MQL5: MQL5 Indicators/DSS/DSS.mq5

Double Smoothed Stochastic
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [32768]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'DSS', 2: 'Signal'}, 'levels': [], 'description': ['Double Smoothed Stochastic'], 'name': 'DSS', 'source': 'MQL5 Indicators/DSS/DSS.mq5', 'folder': 'DSS', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 13, 'label': 'Period', 'sinput': False}, {'mql': 'InpPeriodEMA', 'py': 'InpPeriodEMA', 'param': 'InpPeriodEMA', 'type': 'uint', 'default': 8, 'label': 'EMA period', 'sinput': False}, {'mql': 'InpPeriodSig', 'py': 'InpPeriodSig', 'param': 'InpPeriodSig', 'type': 'uint', 'default': 8, 'label': 'Signal period', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 80.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 20.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 13)  # Period
InpPeriodEMA = _input('InpPeriodEMA', 8)  # EMA period
InpPeriodSig = _input('InpPeriodSig', 8)  # Signal period
InpOverbought = _input('InpOverbought', 80.0)  # Overbought
InpOversold = _input('InpOversold', 20.0)  # Oversold
BufferDSS = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferRAW = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
coeff = 0.0
period_raw = 0
period_ema = 0
period_sig = 0
weight_sum = 0

def OnInit():
    global coeff, overbought, oversold, period_ema, period_raw, period_sig
    period_raw = (2 if (InpPeriod < 2) else InpPeriod)
    period_ema = (2 if (InpPeriodEMA < 2) else InpPeriodEMA)
    period_sig = (2 if (InpPeriodSig < 2) else InpPeriodSig)
    coeff = _fdiv(2.0, 1.0 + period_ema)
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else (overbought - 0.1) if (InpOversold >= overbought) else InpOversold)
    SetIndexBuffer(0, BufferDSS, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(2, BufferRAW, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'DSS (' + _str(period_raw) + ',' + _str(period_ema) + ',' + _str(period_sig) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 100)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Oversold')
    ArraySetAsSeries(BufferDSS, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferRAW, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_raw, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_raw - 2
        ArrayInitialize(BufferDSS, 0)
        ArrayInitialize(BufferSignal, EMPTY_VALUE)
        ArrayInitialize(BufferRAW, 0)
    for i in range(limit, 0 - 1, -1):
        bh = ArrayMaximum(high, i, period_raw)
        bl = ArrayMinimum(low, i, period_raw)
        if bh == WRONG_VALUE or bl == WRONG_VALUE:
            continue
        max_ = high[bh]
        min_ = low[bl]
        delta = close[i] - min_
        mit = (_fdiv(delta * 100.0, max_ - min_) if ((max_ - min_) != 0) else 0)
        BufferRAW[i] = (coeff * mit) + ((1.0 - coeff) * BufferRAW[i + 1])
        bh = ArrayMaximum(BufferRAW, i, period_raw)
        bl = ArrayMinimum(BufferRAW, i, period_raw)
        if bh == WRONG_VALUE or bl == WRONG_VALUE:
            continue
        max_ = BufferRAW[bh]
        min_ = BufferRAW[bl]
        delta = BufferRAW[i] - min_
        mit = (_fdiv(delta * 100.0, max_ - min_) if ((max_ - min_) != 0) else 0)
        BufferDSS[i] = (coeff * mit) + ((1.0 - coeff) * BufferDSS[i + 1])
    return ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sig, BufferDSS, BufferSignal)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DSS(_MQL5Indicator):
    name = 'DSS'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 13,  # Period
        'InpPeriodEMA': 8,  # EMA period
        'InpPeriodSig': 8,  # Signal period
        'InpOverbought': 80.0,  # Overbought
        'InpOversold': 20.0,  # Oversold
    }

