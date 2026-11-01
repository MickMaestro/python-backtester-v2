"""OnChart_Stochastic — converted from MQL5: MQL5 Indicators/OnChart_Stochastic/OnChart_Stochastic.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'colors': {1: [3329330], 2: [255], 3: [9419919], 4: [9419919], 5: [8421504]}, 'widths': {1: 2, 2: 2, 3: 1, 4: 1, 5: 1}, 'styles': {1: 0, 2: 0, 3: 2, 4: 2, 5: 2}, 'labels': {1: 'Main line', 2: 'Signal line', 3: 'Overbought', 4: 'Oversold', 5: 'Middle'}, 'levels': [], 'description': [], 'name': 'OnChart_Stochastic', 'source': 'MQL5 Indicators/OnChart_Stochastic/OnChart_Stochastic.mq5', 'folder': 'OnChart_Stochastic', 'inputs': [{'mql': 'InpPeriodK', 'py': 'InpPeriodK', 'param': 'InpPeriodK', 'type': 'uint', 'default': 5, 'label': '%K period', 'sinput': False}, {'mql': 'InpPeriodD', 'py': 'InpPeriodD', 'param': 'InpPeriodD', 'type': 'uint', 'default': 3, 'label': '%D period', 'sinput': False}, {'mql': 'InpSlowing', 'py': 'InpSlowing', 'param': 'InpSlowing', 'type': 'uint', 'default': 3, 'label': 'Slowing', 'sinput': False}, {'mql': 'InpMethodSmoothK', 'py': 'InpMethodSmoothK', 'param': 'InpMethodSmoothK', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'InpPriceField', 'py': 'InpPriceField', 'param': 'InpPriceField', 'type': 'int', 'default': 0, 'label': 'Price field', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 80.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 20.0, 'label': 'Oversold', 'sinput': False}, {'mql': 'InpPeriodATR', 'py': 'InpPeriodATR', 'param': 'InpPeriodATR', 'type': 'uint', 'default': 14, 'label': 'ATR period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodK = _input('InpPeriodK', 5)  # %K period
InpPeriodD = _input('InpPeriodD', 3)  # %D period
InpSlowing = _input('InpSlowing', 3)  # Slowing
InpMethodSmoothK = _input('InpMethodSmoothK', MODE_SMA)  # Smoothing method
InpPriceField = _input('InpPriceField', STO_LOWHIGH)  # Price field
InpOverbought = _input('InpOverbought', 80.0)  # Overbought
InpOversold = _input('InpOversold', 20.0)  # Oversold
InpPeriodATR = _input('InpPeriodATR', 14)  # ATR period
BufferK = Arr(0, 0.0)
BufferD = Arr(0, 0.0)
BufferOB = Arr(0, 0.0)
BufferOS = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferKTMP = Arr(0, 0.0)
BufferDTMP = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_k = 0
period_s = 0
period_d = 0
period_atr = 0
handle_sto = 0
handle_ma = 0
handle_atr = 0

def OnInit():
    global handle_atr, handle_ma, handle_sto, overbought, oversold, period_atr, period_d, period_k, period_s
    period_k = (1 if (InpPeriodK < 1) else InpPeriodK)
    period_d = (1 if (InpPeriodD < 1) else InpPeriodD)
    period_s = (1 if (InpSlowing < 1) else InpSlowing)
    period_atr = (1 if (InpPeriodATR < 1) else InpPeriodATR)
    overbought = (100 if (InpOverbought > 100) else 0.2 if (InpOverbought < 0.2) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else 99.9 if (InpOversold > 99.9) else InpOversold)
    if overbought <= oversold:
        overbought = oversold + 0.1
    if oversold >= overbought:
        oversold = overbought - 0.1
    SetIndexBuffer(0, BufferK, INDICATOR_DATA)
    SetIndexBuffer(1, BufferD, INDICATOR_DATA)
    SetIndexBuffer(2, BufferOB, INDICATOR_DATA)
    SetIndexBuffer(3, BufferOS, INDICATOR_DATA)
    SetIndexBuffer(4, BufferMA, INDICATOR_DATA)
    SetIndexBuffer(5, BufferDTMP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferKTMP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferATR, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'OnChart stochastic(' + _str(period_k) + ',' + _str(period_d) + ',' + _str(period_s) + ')')
    ArraySetAsSeries(BufferK, True)
    ArraySetAsSeries(BufferD, True)
    ArraySetAsSeries(BufferOB, True)
    ArraySetAsSeries(BufferOS, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferDTMP, True)
    ArraySetAsSeries(BufferKTMP, True)
    ArraySetAsSeries(BufferATR, True)
    ResetLastError()
    handle_sto = iStochastic(None, PERIOD_CURRENT, period_k, period_d, period_s, InpMethodSmoothK, InpPriceField)
    if handle_sto == INVALID_HANDLE:
        Print('The Fast iStochastic(', _str(period_k), ',', _str(period_d), ',', _str(period_s), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period_atr, 0, InpMethodSmoothK, PRICE_CLOSE)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_atr), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_atr = iATR(None, PERIOD_CURRENT, period_atr)
    if handle_atr == INVALID_HANDLE:
        Print('The iATR(', _str(period_atr), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferK, EMPTY_VALUE)
        ArrayInitialize(BufferD, EMPTY_VALUE)
        ArrayInitialize(BufferOB, EMPTY_VALUE)
        ArrayInitialize(BufferOS, EMPTY_VALUE)
        ArrayInitialize(BufferMA, EMPTY_VALUE)
        ArrayInitialize(BufferDTMP, EMPTY_VALUE)
        ArrayInitialize(BufferKTMP, EMPTY_VALUE)
        ArrayInitialize(BufferATR, EMPTY_VALUE)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_sto, MAIN_LINE, 0, count, BufferKTMP)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sto, SIGNAL_LINE, 0, count, BufferDTMP)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_atr, 0, 0, count, BufferATR)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferOB[i] = BufferMA[i] + ((BufferATR[i] * (overbought - 50)) / 100)
        BufferOS[i] = BufferMA[i] - ((BufferATR[i] * (50 - oversold)) / 100)
        BufferK[i] = BufferMA[i] + (((BufferKTMP[i] - 50) * BufferATR[i]) / 100)
        BufferD[i] = BufferMA[i] + (((BufferDTMP[i] - 50) * BufferATR[i]) / 100)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class OnChartStochastic(_MQL5Indicator):
    name = 'OnChart_Stochastic'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodK': 5,  # %K period
        'InpPeriodD': 3,  # %D period
        'InpSlowing': 3,  # Slowing
        'InpMethodSmoothK': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Smoothing method
        'InpPriceField': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Price field
        'InpOverbought': 80.0,  # Overbought
        'InpOversold': 20.0,  # Oversold
        'InpPeriodATR': 14,  # ATR period
    }

