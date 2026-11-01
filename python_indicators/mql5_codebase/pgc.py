"""PGC — converted from MQL5: MQL5 Indicators/PGC/PGC.mq5

Price Gouging Cycle oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 13, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'PG Cycle'}, 'levels': [], 'description': ['Price Gouging Cycle oscillator'], 'name': 'PGC', 'source': 'MQL5 Indicators/PGC/PGC.mq5', 'folder': 'PGC', 'inputs': [{'mql': 'InpPeriod1', 'py': 'InpPeriod1', 'param': 'InpPeriod1', 'type': 'uint', 'default': 9, 'label': 'First MA period', 'sinput': False}, {'mql': 'InpPeriod2', 'py': 'InpPeriod2', 'param': 'InpPeriod2', 'type': 'uint', 'default': 19, 'label': 'Second MA period', 'sinput': False}, {'mql': 'InpPeriod3', 'py': 'InpPeriod3', 'param': 'InpPeriod3', 'type': 'uint', 'default': 6, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'InpPeriodRSI', 'py': 'InpPeriodRSI', 'param': 'InpPeriodRSI', 'type': 'uint', 'default': 8, 'label': 'RSI period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 70.0, 'label': 'Overbought level', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 30.0, 'label': 'Oversold level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod1 = _input('InpPeriod1', 9)  # First MA period
InpPeriod2 = _input('InpPeriod2', 19)  # Second MA period
InpPeriod3 = _input('InpPeriod3', 6)  # Smoothing period
InpPeriodRSI = _input('InpPeriodRSI', 8)  # RSI period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpOverbought = _input('InpOverbought', 70.0)  # Overbought level
InpOversold = _input('InpOversold', 30.0)  # Oversold level
BufferPGC = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMA2 = Arr(0, 0.0)
BufferAvgMA1 = Arr(0, 0.0)
BufferAvgMA2 = Arr(0, 0.0)
BufferE = Arr(0, 0.0)
BufferAvgMA3 = Arr(0, 0.0)
BufferAvg2MA3 = Arr(0, 0.0)
BufferZ3 = Arr(0, 0.0)
BufferInc = Arr(0, 0.0)
BufferDec = Arr(0, 0.0)
BufferAvgInc = Arr(0, 0.0)
BufferAvgDec = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_ma1 = 0
period_ma2 = 0
period_ma3 = 0
period_rsi = 0
weight_sum = 0
handle_ma1 = 0
handle_ma2 = 0

def OnInit():
    global handle_ma1, handle_ma2, overbought, oversold, period_ma1, period_ma2, period_ma3, period_rsi
    period_ma1 = (1 if (InpPeriod1 < 1) else InpPeriod1)
    period_ma2 = (1 if (InpPeriod2 < 1) else InpPeriod2)
    period_ma3 = (2 if (InpPeriod3 < 2) else InpPeriod3)
    period_rsi = (2 if (InpPeriodRSI < 2) else InpPeriodRSI)
    oversold = (0 if (InpOversold < 0) else 99.9 if (InpOversold > 99.9) else InpOversold)
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    if overbought <= oversold:
        overbought = oversold + 0.1
    if oversold >= overbought:
        oversold = overbought - 0.1
    SetIndexBuffer(0, BufferPGC, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferAvgMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferAvgMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferE, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferAvgMA3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferAvg2MA3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferZ3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferInc, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, BufferDec, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, BufferAvgInc, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, BufferAvgDec, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'PG Cycle (' + _str(period_ma1) + ',' + _str(period_ma2) + ',' + _str(period_ma3) + ',' + _str(period_rsi) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, oversold)
    ArraySetAsSeries(BufferPGC, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMA2, True)
    ArraySetAsSeries(BufferAvgMA1, True)
    ArraySetAsSeries(BufferAvgMA2, True)
    ArraySetAsSeries(BufferE, True)
    ArraySetAsSeries(BufferAvgMA3, True)
    ArraySetAsSeries(BufferAvg2MA3, True)
    ArraySetAsSeries(BufferZ3, True)
    ArraySetAsSeries(BufferInc, True)
    ArraySetAsSeries(BufferDec, True)
    ArraySetAsSeries(BufferAvgInc, True)
    ArraySetAsSeries(BufferAvgDec, True)
    ResetLastError()
    handle_ma1 = iMA(None, PERIOD_CURRENT, period_ma1, 0, MODE_EMA, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma1), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma2 = iMA(None, PERIOD_CURRENT, period_ma2, 0, MODE_EMA, InpAppliedPrice)
    if handle_ma2 == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma2), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferPGC, EMPTY_VALUE)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferMA2, 0)
        ArrayInitialize(BufferAvgMA1, 0)
        ArrayInitialize(BufferAvgMA2, 0)
        ArrayInitialize(BufferE, 0)
        ArrayInitialize(BufferAvgMA3, 0)
        ArrayInitialize(BufferAvg2MA3, 0)
        ArrayInitialize(BufferZ3, 0)
        ArrayInitialize(BufferInc, 0)
        ArrayInitialize(BufferDec, 0)
        ArrayInitialize(BufferAvgInc, 0)
        ArrayInitialize(BufferAvgDec, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma2, 0, 0, count, BufferMA2)
    if copied != count:
        return 0
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ma1, BufferMA1, BufferAvgMA1)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ma1, BufferMA2, BufferAvgMA2)
    for i in range(limit, 0 - 1, -1):
        z1 = (2.0 * BufferMA1[i]) - BufferAvgMA1[i]
        z2 = (2.0 * BufferMA2[i]) - BufferAvgMA2[i]
        BufferE[i] = z1 - z2
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ma3, BufferE, BufferAvgMA3)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ma3, BufferAvgMA3, BufferAvg2MA3)
    for i in range(limit, 0 - 1, -1):
        BufferZ3[i] = (2.0 * BufferAvgMA3[i]) - BufferAvg2MA3[i]
        if BufferZ3[i] > BufferZ3[i + 1]:
            BufferInc[i] = BufferZ3[i] - BufferZ3[i + 1]
            BufferDec[i] = 0.0
        else:
            if BufferZ3[i] < BufferZ3[i + 1]:
                BufferInc[i] = 0.0
                BufferDec[i] = BufferZ3[i + 1] - BufferZ3[i]
            else:
                BufferInc[i] = 0.0
                BufferDec[i] = 0.0
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_rsi, BufferInc, BufferAvgInc)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_rsi, BufferDec, BufferAvgDec)
    for i in range(limit, 0 - 1, -1):
        RS = (_fdiv(BufferAvgInc[i], BufferAvgDec[i]) if (BufferAvgDec[i] != 0) else 0)
        BufferPGC[i] = 100.0 - _fdiv(100.0, 1.0 + RS)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PGC(_MQL5Indicator):
    name = 'PGC'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod1': 9,  # First MA period
        'InpPeriod2': 19,  # Second MA period
        'InpPeriod3': 6,  # Smoothing period
        'InpPeriodRSI': 8,  # RSI period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpOverbought': 70.0,  # Overbought level
        'InpOversold': 30.0,  # Oversold level
    }

