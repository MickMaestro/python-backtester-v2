"""Smoothed_RSI — converted from MQL5: MQL5 Indicators/Smoothed_RSI/Smoothed_RSI.mq5

Smoothed RSI indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [2330219]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Smoothed RSI'}, 'levels': [], 'description': ['Smoothed RSI indicator'], 'name': 'Smoothed_RSI', 'source': 'MQL5 Indicators/Smoothed_RSI/Smoothed_RSI.mq5', 'folder': 'Smoothed_RSI', 'inputs': [{'mql': 'InpPeriodSRC', 'py': 'InpPeriodSRC', 'param': 'InpPeriodSRC', 'type': 'uint', 'default': 10, 'label': 'Source period', 'sinput': False}, {'mql': 'InpMethodSRC', 'py': 'InpMethodSRC', 'param': 'InpMethodSRC', 'type': 'int', 'default': 0, 'label': 'Source method', 'sinput': False}, {'mql': 'InpAppliedPriceSRC', 'py': 'InpAppliedPriceSRC', 'param': 'InpAppliedPriceSRC', 'type': 'int', 'default': 1, 'label': 'Source applied price', 'sinput': False}, {'mql': 'InpPeriodRSI', 'py': 'InpPeriodRSI', 'param': 'InpPeriodRSI', 'type': 'uint', 'default': 10, 'label': 'Smoothed RSI period', 'sinput': False}, {'mql': 'InpMethodRSI', 'py': 'InpMethodRSI', 'param': 'InpMethodRSI', 'type': 'int', 'default': 0, 'label': 'Smoothed RSI method', 'sinput': False}, {'mql': 'InpLevTop', 'py': 'InpLevTop', 'param': 'InpLevTop', 'type': 'double', 'default': 70.0, 'label': 'Top level', 'sinput': False}, {'mql': 'InpLevBottom', 'py': 'InpLevBottom', 'param': 'InpLevBottom', 'type': 'double', 'default': 30.0, 'label': 'Bottom level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodSRC = _input('InpPeriodSRC', 10)  # Source period
InpMethodSRC = _input('InpMethodSRC', MODE_SMA)  # Source method
InpAppliedPriceSRC = _input('InpAppliedPriceSRC', PRICE_CLOSE)  # Source applied price
InpPeriodRSI = _input('InpPeriodRSI', 10)  # Smoothed RSI period
InpMethodRSI = _input('InpMethodRSI', MODE_SMA)  # Smoothed RSI method
InpLevTop = _input('InpLevTop', 70.0)  # Top level
InpLevBottom = _input('InpLevBottom', 30.0)  # Bottom level
BufferRSI = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferPositive = Arr(0, 0.0)
BufferNegative = Arr(0, 0.0)
BufferAvgPositive = Arr(0, 0.0)
BufferAvgNegative = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_src = 0
period_rsi = 0
handle_ma = 0
weight_sumP = 0
weight_sumN = 0

def OnInit():
    global handle_ma, overbought, oversold, period_rsi, period_src
    period_src = (2 if (InpPeriodSRC < 2) else InpPeriodSRC)
    period_rsi = (2 if (InpPeriodRSI < 2) else InpPeriodRSI)
    overbought = (100 if (InpLevTop > 100) else 0.1 if (InpLevTop < 0.1) else InpLevTop)
    oversold = (0 if (InpLevBottom < 0) else (overbought - 0.1) if (InpLevBottom >= overbought) else InpLevBottom)
    SetIndexBuffer(0, BufferRSI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferPositive, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferNegative, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferAvgPositive, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferAvgNegative, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Smoothed RSI (' + _str(period_src) + ',' + _str(period_rsi) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Top')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Bottom')
    ArraySetAsSeries(BufferRSI, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferPositive, True)
    ArraySetAsSeries(BufferNegative, True)
    ArraySetAsSeries(BufferAvgPositive, True)
    ArraySetAsSeries(BufferAvgNegative, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period_src, 0, InpMethodSRC, InpAppliedPriceSRC)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_src), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_rsi, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferRSI, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferPositive, 0)
        ArrayInitialize(BufferNegative, 0)
        ArrayInitialize(BufferAvgPositive, 0)
        ArrayInitialize(BufferAvgNegative, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        diff = BufferMA[i] - close[i]
        if diff > 0:
            BufferPositive[i] = diff
            BufferNegative[i] = 0.0
        else:
            BufferNegative[i] = -diff
            BufferPositive[i] = 0.0
    _sw1 = InpMethodRSI
    if _sw1 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_src, period_rsi, BufferPositive, BufferAvgPositive) == 0:
            return 0
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_src, period_rsi, BufferNegative, BufferAvgNegative) == 0:
            return 0
    elif _sw1 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_src, period_rsi, BufferPositive, BufferAvgPositive) == 0:
            return 0
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_src, period_rsi, BufferNegative, BufferAvgNegative) == 0:
            return 0
    elif _sw1 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_src, period_rsi, BufferPositive, BufferAvgPositive, _GlobRef(globals(), 'weight_sumP')) == 0:
            return 0
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_src, period_rsi, BufferNegative, BufferAvgNegative, _GlobRef(globals(), 'weight_sumN')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_src, period_rsi, BufferPositive, BufferAvgPositive) == 0:
            return 0
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_src, period_rsi, BufferNegative, BufferAvgNegative) == 0:
            return 0
    for i in range(limit, 0 - 1, -1):
        BufferRSI[i] = ((100.0 - _fdiv(100.0, 1.0 + _fdiv(BufferAvgPositive[i], BufferAvgNegative[i]))) if (BufferAvgNegative[i] != 0) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SmoothedRSI(_MQL5Indicator):
    name = 'Smoothed_RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodSRC': 10,  # Source period
        'InpMethodSRC': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Source method
        'InpAppliedPriceSRC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Source applied price
        'InpPeriodRSI': 10,  # Smoothed RSI period
        'InpMethodRSI': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Smoothed RSI method
        'InpLevTop': 70.0,  # Top level
        'InpLevBottom': 30.0,  # Bottom level
    }

