"""Cutler_RSI — converted from MQL5: MQL5 Indicators/Cutler_RSI/Cutler_RSI.mq5

Cutler RSI indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [2263842]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'CRSI'}, 'levels': [], 'description': ['Cutler RSI indicator'], 'name': 'Cutler_RSI', 'source': 'MQL5 Indicators/Cutler_RSI/Cutler_RSI.mq5', 'folder': 'Cutler_RSI', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 80.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 20.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpOverbought = _input('InpOverbought', 80.0)  # Overbought
InpOversold = _input('InpOversold', 20.0)  # Oversold
BufferCRSI = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferPos = Arr(0, 0.0)
BufferNeg = Arr(0, 0.0)
BufferPosAvg = Arr(0, 0.0)
BufferNegAvg = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_ind = 0
weight_sum = 0
handle_ma = 0

def OnInit():
    global handle_ma, overbought, oversold, period_ind
    period_ind = (1 if (InpPeriod < 1) else InpPeriod)
    oversold = (0 if (InpOversold < 0) else 99.9 if (InpOversold > 99.9) else InpOversold)
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    if overbought <= oversold:
        overbought = oversold + 0.1
    if oversold >= overbought:
        oversold = overbought - 0.1
    SetIndexBuffer(0, BufferCRSI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferPos, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferNeg, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferPosAvg, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferNegAvg, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Cutler RSI (' + _str(period_ind) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, oversold)
    ArraySetAsSeries(BufferCRSI, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferPos, True)
    ArraySetAsSeries(BufferNeg, True)
    ArraySetAsSeries(BufferPosAvg, True)
    ArraySetAsSeries(BufferNegAvg, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferCRSI, EMPTY_VALUE)
        ArrayInitialize(BufferMA, EMPTY_VALUE)
        ArrayInitialize(BufferPos, 0)
        ArrayInitialize(BufferNeg, 0)
        ArrayInitialize(BufferPosAvg, 0)
        ArrayInitialize(BufferNegAvg, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        diff = BufferMA[i] - BufferMA[i + 1]
        if diff > 0:
            BufferPos[i] = diff
            BufferNeg[i] = 0.0
        else:
            BufferPos[i] = 0.0
            BufferNeg[i] = -diff
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferPos, BufferPosAvg)
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferNeg, BufferNegAvg)
    elif _sw1 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferPos, BufferPosAvg)
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferNeg, BufferNegAvg)
    elif _sw1 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_ind, BufferPos, BufferPosAvg, _GlobRef(globals(), 'weight_sum'))
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_ind, BufferNeg, BufferNegAvg, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferPos, BufferPosAvg)
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferNeg, BufferNegAvg)
    for i in range(limit, 0 - 1, -1):
        N = BufferNegAvg[i]
        BufferCRSI[i] = ((100.0 - _fdiv(100.0, 1.0 + _fdiv(BufferPosAvg[i], N))) if (N != 0) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CutlerRSI(_MQL5Indicator):
    name = 'Cutler_RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpOverbought': 80.0,  # Overbought
        'InpOversold': 20.0,  # Oversold
    }

