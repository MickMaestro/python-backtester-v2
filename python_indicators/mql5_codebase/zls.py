"""ZLS — converted from MQL5: MQL5 Indicators/ZLS/ZLS.mq5

Zero Lag Stochastic indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'K', 2: 'D'}, 'levels': [], 'description': ['Zero Lag Stochastic indicator'], 'name': 'ZLS', 'source': 'MQL5 Indicators/ZLS/ZLS.mq5', 'folder': 'ZLS', 'inputs': [{'mql': 'InpSmoothing', 'py': 'InpSmoothing', 'param': 'InpSmoothing', 'type': 'uint', 'default': 15, 'label': 'Smoothing', 'sinput': False}, {'mql': 'InpPeriodK1', 'py': 'InpPeriodK1', 'param': 'InpPeriodK1', 'type': 'uint', 'default': 18, 'label': 'Stoch 1 %K period', 'sinput': False}, {'mql': 'InpPeriodD1', 'py': 'InpPeriodD1', 'param': 'InpPeriodD1', 'type': 'uint', 'default': 3, 'label': 'Stoch 1 %D period', 'sinput': False}, {'mql': 'InpSlowing1', 'py': 'InpSlowing1', 'param': 'InpSlowing1', 'type': 'uint', 'default': 3, 'label': 'Stoch 1 Slowing', 'sinput': False}, {'mql': 'InpMethod1', 'py': 'InpMethod1', 'param': 'InpMethod1', 'type': 'int', 'default': 0, 'label': 'Stoch 1 Method', 'sinput': False}, {'mql': 'InpPriceField1', 'py': 'InpPriceField1', 'param': 'InpPriceField1', 'type': 'int', 'default': 0, 'label': 'Stoch 1 Price field', 'sinput': False}, {'mql': 'InpWeight1', 'py': 'InpWeight1', 'param': 'InpWeight1', 'type': 'double', 'default': 0.05, 'label': 'Stoch 1 Weight', 'sinput': False}, {'mql': 'InpPeriodK2', 'py': 'InpPeriodK2', 'param': 'InpPeriodK2', 'type': 'uint', 'default': 21, 'label': 'Stoch 2 %K period', 'sinput': False}, {'mql': 'InpPeriodD2', 'py': 'InpPeriodD2', 'param': 'InpPeriodD2', 'type': 'uint', 'default': 3, 'label': 'Stoch 2 %D period', 'sinput': False}, {'mql': 'InpSlowing2', 'py': 'InpSlowing2', 'param': 'InpSlowing2', 'type': 'uint', 'default': 5, 'label': 'Stoch 2 Slowing', 'sinput': False}, {'mql': 'InpMethod2', 'py': 'InpMethod2', 'param': 'InpMethod2', 'type': 'int', 'default': 0, 'label': 'Stoch 2 Method', 'sinput': False}, {'mql': 'InpPriceField2', 'py': 'InpPriceField2', 'param': 'InpPriceField2', 'type': 'int', 'default': 0, 'label': 'Stoch 2 Price field', 'sinput': False}, {'mql': 'InpWeight2', 'py': 'InpWeight2', 'param': 'InpWeight2', 'type': 'double', 'default': 0.1, 'label': 'Stoch 2 Weight', 'sinput': False}, {'mql': 'InpPeriodK3', 'py': 'InpPeriodK3', 'param': 'InpPeriodK3', 'type': 'uint', 'default': 34, 'label': 'Stoch 3 %K period', 'sinput': False}, {'mql': 'InpPeriodD3', 'py': 'InpPeriodD3', 'param': 'InpPeriodD3', 'type': 'uint', 'default': 3, 'label': 'Stoch 3 %D period', 'sinput': False}, {'mql': 'InpSlowing3', 'py': 'InpSlowing3', 'param': 'InpSlowing3', 'type': 'uint', 'default': 8, 'label': 'Stoch 3 Slowing', 'sinput': False}, {'mql': 'InpMethod3', 'py': 'InpMethod3', 'param': 'InpMethod3', 'type': 'int', 'default': 0, 'label': 'Stoch 3 Method', 'sinput': False}, {'mql': 'InpPriceField3', 'py': 'InpPriceField3', 'param': 'InpPriceField3', 'type': 'int', 'default': 0, 'label': 'Stoch 3 Price field', 'sinput': False}, {'mql': 'InpWeight3', 'py': 'InpWeight3', 'param': 'InpWeight3', 'type': 'double', 'default': 0.16, 'label': 'Stoch 3 Weight', 'sinput': False}, {'mql': 'InpPeriodK4', 'py': 'InpPeriodK4', 'param': 'InpPeriodK4', 'type': 'uint', 'default': 55, 'label': 'Stoch 4 %K period', 'sinput': False}, {'mql': 'InpPeriodD4', 'py': 'InpPeriodD4', 'param': 'InpPeriodD4', 'type': 'uint', 'default': 3, 'label': 'Stoch 4 %D period', 'sinput': False}, {'mql': 'InpSlowing4', 'py': 'InpSlowing4', 'param': 'InpSlowing4', 'type': 'uint', 'default': 13, 'label': 'Stoch 4 Slowing', 'sinput': False}, {'mql': 'InpMethod4', 'py': 'InpMethod4', 'param': 'InpMethod4', 'type': 'int', 'default': 0, 'label': 'Stoch 4 Method', 'sinput': False}, {'mql': 'InpPriceField4', 'py': 'InpPriceField4', 'param': 'InpPriceField4', 'type': 'int', 'default': 0, 'label': 'Stoch 4 Price field', 'sinput': False}, {'mql': 'InpWeight4', 'py': 'InpWeight4', 'param': 'InpWeight4', 'type': 'double', 'default': 0.26, 'label': 'Stoch 4 Weight', 'sinput': False}, {'mql': 'InpPeriodK5', 'py': 'InpPeriodK5', 'param': 'InpPeriodK5', 'type': 'uint', 'default': 89, 'label': 'Stoch 5 %K period', 'sinput': False}, {'mql': 'InpPeriodD5', 'py': 'InpPeriodD5', 'param': 'InpPeriodD5', 'type': 'uint', 'default': 3, 'label': 'Stoch 5 %D period', 'sinput': False}, {'mql': 'InpSlowing5', 'py': 'InpSlowing5', 'param': 'InpSlowing5', 'type': 'uint', 'default': 21, 'label': 'Stoch 5 Slowing', 'sinput': False}, {'mql': 'InpMethod5', 'py': 'InpMethod5', 'param': 'InpMethod5', 'type': 'int', 'default': 0, 'label': 'Stoch 5 Method', 'sinput': False}, {'mql': 'InpPriceField5', 'py': 'InpPriceField5', 'param': 'InpPriceField5', 'type': 'int', 'default': 0, 'label': 'Stoch 5 Price field', 'sinput': False}, {'mql': 'InpWeight5', 'py': 'InpWeight5', 'param': 'InpWeight5', 'type': 'double', 'default': 0.43, 'label': 'Stoch 5 Weight', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpSmoothing = _input('InpSmoothing', 15)  # Smoothing
InpPeriodK1 = _input('InpPeriodK1', 18)  # Stoch 1 %K period
InpPeriodD1 = _input('InpPeriodD1', 3)  # Stoch 1 %D period
InpSlowing1 = _input('InpSlowing1', 3)  # Stoch 1 Slowing
InpMethod1 = _input('InpMethod1', MODE_SMA)  # Stoch 1 Method
InpPriceField1 = _input('InpPriceField1', STO_LOWHIGH)  # Stoch 1 Price field
InpWeight1 = _input('InpWeight1', 0.05)  # Stoch 1 Weight
InpPeriodK2 = _input('InpPeriodK2', 21)  # Stoch 2 %K period
InpPeriodD2 = _input('InpPeriodD2', 3)  # Stoch 2 %D period
InpSlowing2 = _input('InpSlowing2', 5)  # Stoch 2 Slowing
InpMethod2 = _input('InpMethod2', MODE_SMA)  # Stoch 2 Method
InpPriceField2 = _input('InpPriceField2', STO_LOWHIGH)  # Stoch 2 Price field
InpWeight2 = _input('InpWeight2', 0.1)  # Stoch 2 Weight
InpPeriodK3 = _input('InpPeriodK3', 34)  # Stoch 3 %K period
InpPeriodD3 = _input('InpPeriodD3', 3)  # Stoch 3 %D period
InpSlowing3 = _input('InpSlowing3', 8)  # Stoch 3 Slowing
InpMethod3 = _input('InpMethod3', MODE_SMA)  # Stoch 3 Method
InpPriceField3 = _input('InpPriceField3', STO_LOWHIGH)  # Stoch 3 Price field
InpWeight3 = _input('InpWeight3', 0.16)  # Stoch 3 Weight
InpPeriodK4 = _input('InpPeriodK4', 55)  # Stoch 4 %K period
InpPeriodD4 = _input('InpPeriodD4', 3)  # Stoch 4 %D period
InpSlowing4 = _input('InpSlowing4', 13)  # Stoch 4 Slowing
InpMethod4 = _input('InpMethod4', MODE_SMA)  # Stoch 4 Method
InpPriceField4 = _input('InpPriceField4', STO_LOWHIGH)  # Stoch 4 Price field
InpWeight4 = _input('InpWeight4', 0.26)  # Stoch 4 Weight
InpPeriodK5 = _input('InpPeriodK5', 89)  # Stoch 5 %K period
InpPeriodD5 = _input('InpPeriodD5', 3)  # Stoch 5 %D period
InpSlowing5 = _input('InpSlowing5', 21)  # Stoch 5 Slowing
InpMethod5 = _input('InpMethod5', MODE_SMA)  # Stoch 5 Method
InpPriceField5 = _input('InpPriceField5', STO_LOWHIGH)  # Stoch 5 Price field
InpWeight5 = _input('InpWeight5', 0.43)  # Stoch 5 Weight
BufferK = Arr(0, 0.0)
BufferD = Arr(0, 0.0)
BufferST1 = Arr(0, 0.0)
BufferST2 = Arr(0, 0.0)
BufferST3 = Arr(0, 0.0)
BufferST4 = Arr(0, 0.0)
BufferST5 = Arr(0, 0.0)
period_sm = 0
period_k1 = 0
period_d1 = 0
period_s1 = 0
period_k2 = 0
period_d2 = 0
period_s2 = 0
period_k3 = 0
period_d3 = 0
period_s3 = 0
period_k4 = 0
period_d4 = 0
period_s4 = 0
period_k5 = 0
period_d5 = 0
period_s5 = 0
max_k = 0
max_d = 0
max_s = 0
period_max = 0
handle_st1 = 0
handle_st2 = 0
handle_st3 = 0
handle_st4 = 0
handle_st5 = 0
smooth_const = 0.0
sum_weight = 0.0

def OnInit():
    global handle_st1, handle_st2, handle_st3, handle_st4, handle_st5, max_d, max_k, max_s, period_d1, period_d2, period_d3, period_d4, period_d5, period_k1, period_k2, period_k3, period_k4, period_k5, period_max, period_s1, period_s2, period_s3, period_s4, period_s5, period_sm, smooth_const, sum_weight
    period_sm = (1 if (InpSmoothing < 1) else InpSmoothing)
    period_k1 = (1 if (InpPeriodK1 < 1) else InpPeriodK1)
    period_d1 = (1 if (InpPeriodD1 < 1) else InpPeriodD1)
    period_s1 = (1 if (InpSlowing1 < 1) else InpSlowing1)
    period_k2 = (1 if (InpPeriodK2 < 1) else InpPeriodK2)
    period_d2 = (1 if (InpPeriodD2 < 1) else InpPeriodD2)
    period_s2 = (1 if (InpSlowing2 < 1) else InpSlowing2)
    period_k3 = (1 if (InpPeriodK3 < 1) else InpPeriodK3)
    period_d3 = (1 if (InpPeriodD3 < 1) else InpPeriodD3)
    period_s3 = (1 if (InpSlowing3 < 1) else InpSlowing3)
    period_k4 = (1 if (InpPeriodK4 < 1) else InpPeriodK4)
    period_d4 = (1 if (InpPeriodD4 < 1) else InpPeriodD4)
    period_s4 = (1 if (InpSlowing4 < 1) else InpSlowing4)
    period_k5 = (1 if (InpPeriodK5 < 1) else InpPeriodK5)
    period_d5 = (1 if (InpPeriodD5 < 1) else InpPeriodD5)
    period_s5 = (1 if (InpSlowing5 < 1) else InpSlowing5)
    max_k = fmax(period_k1, fmax(period_k2, fmax(period_k3, fmax(period_k4, period_k5))))
    max_d = fmax(period_d1, fmax(period_d2, fmax(period_d3, fmax(period_d4, period_d5))))
    max_s = fmax(period_s1, fmax(period_s2, fmax(period_s3, fmax(period_s4, period_s5))))
    period_max = fmax(period_sm, max_k + max_d + max_s)
    smooth_const = _fdiv(period_sm - 1.0, period_sm)
    sum_weight = InpWeight1 + InpWeight2 + InpWeight3 + InpWeight4 + InpWeight5
    if sum_weight == 0:
        sum_weight = 1.0
    SetIndexBuffer(0, BufferK, INDICATOR_DATA)
    SetIndexBuffer(1, BufferD, INDICATOR_DATA)
    SetIndexBuffer(2, BufferST1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferST2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferST3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferST4, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferST5, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Zero Lag Stochastic')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(BufferK, True)
    ArraySetAsSeries(BufferD, True)
    ArraySetAsSeries(BufferST1, True)
    ArraySetAsSeries(BufferST2, True)
    ArraySetAsSeries(BufferST3, True)
    ArraySetAsSeries(BufferST4, True)
    ArraySetAsSeries(BufferST5, True)
    ResetLastError()
    handle_st1 = iStochastic(None, PERIOD_CURRENT, period_k1, period_d1, period_s1, InpMethod1, InpPriceField1)
    if handle_st1 == INVALID_HANDLE:
        Print('The iStochastic(', _str(period_k1), ',', _str(period_d1), ',', _str(period_s1), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_st2 = iStochastic(None, PERIOD_CURRENT, period_k2, period_d2, period_s2, InpMethod2, InpPriceField2)
    if handle_st2 == INVALID_HANDLE:
        Print('The iStochastic(', _str(period_k2), ',', _str(period_d2), ',', _str(period_s2), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_st3 = iStochastic(None, PERIOD_CURRENT, period_k3, period_d3, period_s3, InpMethod3, InpPriceField3)
    if handle_st3 == INVALID_HANDLE:
        Print('The iStochastic(', _str(period_k3), ',', _str(period_d3), ',', _str(period_s3), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_st4 = iStochastic(None, PERIOD_CURRENT, period_k4, period_d4, period_s4, InpMethod4, InpPriceField4)
    if handle_st4 == INVALID_HANDLE:
        Print('The iStochastic(', _str(period_k4), ',', _str(period_d4), ',', _str(period_s4), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_st5 = iStochastic(None, PERIOD_CURRENT, period_k5, period_d5, period_s5, InpMethod5, InpPriceField5)
    if handle_st5 == INVALID_HANDLE:
        Print('The iStochastic(', _str(period_k5), ',', _str(period_d5), ',', _str(period_s5), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 2
        ArrayInitialize(BufferK, EMPTY_VALUE)
        ArrayInitialize(BufferD, 0)
        ArrayInitialize(BufferST1, 0)
        ArrayInitialize(BufferST2, 0)
        ArrayInitialize(BufferST3, 0)
        ArrayInitialize(BufferST4, 0)
        ArrayInitialize(BufferST5, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_st1, MAIN_LINE, 0, count, BufferST1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_st2, MAIN_LINE, 0, count, BufferST2)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_st3, MAIN_LINE, 0, count, BufferST3)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_st4, MAIN_LINE, 0, count, BufferST4)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_st5, MAIN_LINE, 0, count, BufferST5)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferK[i] = _fdiv(BufferST1[i] + BufferST2[i] + BufferST3[i] + BufferST4[i] + BufferST5[i], sum_weight)
        BufferD[i] = _fdiv(BufferK[i], period_sm) + (BufferD[i + 1] * smooth_const)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ZLS(_MQL5Indicator):
    name = 'ZLS'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpSmoothing': 15,  # Smoothing
        'InpPeriodK1': 18,  # Stoch 1 %K period
        'InpPeriodD1': 3,  # Stoch 1 %D period
        'InpSlowing1': 3,  # Stoch 1 Slowing
        'InpMethod1': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Stoch 1 Method
        'InpPriceField1': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stoch 1 Price field
        'InpWeight1': 0.05,  # Stoch 1 Weight
        'InpPeriodK2': 21,  # Stoch 2 %K period
        'InpPeriodD2': 3,  # Stoch 2 %D period
        'InpSlowing2': 5,  # Stoch 2 Slowing
        'InpMethod2': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Stoch 2 Method
        'InpPriceField2': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stoch 2 Price field
        'InpWeight2': 0.1,  # Stoch 2 Weight
        'InpPeriodK3': 34,  # Stoch 3 %K period
        'InpPeriodD3': 3,  # Stoch 3 %D period
        'InpSlowing3': 8,  # Stoch 3 Slowing
        'InpMethod3': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Stoch 3 Method
        'InpPriceField3': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stoch 3 Price field
        'InpWeight3': 0.16,  # Stoch 3 Weight
        'InpPeriodK4': 55,  # Stoch 4 %K period
        'InpPeriodD4': 3,  # Stoch 4 %D period
        'InpSlowing4': 13,  # Stoch 4 Slowing
        'InpMethod4': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Stoch 4 Method
        'InpPriceField4': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stoch 4 Price field
        'InpWeight4': 0.26,  # Stoch 4 Weight
        'InpPeriodK5': 89,  # Stoch 5 %K period
        'InpPeriodD5': 3,  # Stoch 5 %D period
        'InpSlowing5': 21,  # Stoch 5 Slowing
        'InpMethod5': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Stoch 5 Method
        'InpPriceField5': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stoch 5 Price field
        'InpWeight5': 0.43,  # Stoch 5 Weight
    }

