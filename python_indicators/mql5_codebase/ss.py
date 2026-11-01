"""SS — converted from MQL5: MQL5 Indicators/SS/SS.mq5

Stochastic Stack indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 10, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255, 11119017]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'SStack'}, 'levels': [], 'description': ['Stochastic Stack indicator'], 'name': 'SS', 'source': 'MQL5 Indicators/SS/SS.mq5', 'folder': 'SS', 'inputs': [{'mql': 'InpPeriodK1', 'py': 'InpPeriodK1', 'param': 'InpPeriodK1', 'type': 'uint', 'default': 36, 'label': 'Stoch 1 %K period', 'sinput': False}, {'mql': 'InpPeriodD1', 'py': 'InpPeriodD1', 'param': 'InpPeriodD1', 'type': 'uint', 'default': 18, 'label': 'Stoch 1 %D period', 'sinput': False}, {'mql': 'InpSlowing1', 'py': 'InpSlowing1', 'param': 'InpSlowing1', 'type': 'uint', 'default': 9, 'label': 'Stoch 1 slowing', 'sinput': False}, {'mql': 'InpMethod1', 'py': 'InpMethod1', 'param': 'InpMethod1', 'type': 'int', 'default': 0, 'label': 'Stoch 1 Method', 'sinput': False}, {'mql': 'InpPriceField1', 'py': 'InpPriceField1', 'param': 'InpPriceField1', 'type': 'int', 'default': 0, 'label': 'Stoch 1 Price field', 'sinput': False}, {'mql': 'InpPeriodK2', 'py': 'InpPeriodK2', 'param': 'InpPeriodK2', 'type': 'uint', 'default': 40, 'label': 'Stoch 2 %K period', 'sinput': False}, {'mql': 'InpPeriodD2', 'py': 'InpPeriodD2', 'param': 'InpPeriodD2', 'type': 'uint', 'default': 20, 'label': 'Stoch 2 %D period', 'sinput': False}, {'mql': 'InpSlowing2', 'py': 'InpSlowing2', 'param': 'InpSlowing2', 'type': 'uint', 'default': 10, 'label': 'Stoch 2 slowing', 'sinput': False}, {'mql': 'InpMethod2', 'py': 'InpMethod2', 'param': 'InpMethod2', 'type': 'int', 'default': 0, 'label': 'Stoch 2 Method', 'sinput': False}, {'mql': 'InpPriceField2', 'py': 'InpPriceField2', 'param': 'InpPriceField2', 'type': 'int', 'default': 0, 'label': 'Stoch 2 Price field', 'sinput': False}, {'mql': 'InpPeriodK3', 'py': 'InpPeriodK3', 'param': 'InpPeriodK3', 'type': 'uint', 'default': 52, 'label': 'Stoch 3 %K period', 'sinput': False}, {'mql': 'InpPeriodD3', 'py': 'InpPeriodD3', 'param': 'InpPeriodD3', 'type': 'uint', 'default': 26, 'label': 'Stoch 3 %D period', 'sinput': False}, {'mql': 'InpSlowing3', 'py': 'InpSlowing3', 'param': 'InpSlowing3', 'type': 'uint', 'default': 13, 'label': 'Stoch 3 slowing', 'sinput': False}, {'mql': 'InpMethod3', 'py': 'InpMethod3', 'param': 'InpMethod3', 'type': 'int', 'default': 0, 'label': 'Stoch 3 Method', 'sinput': False}, {'mql': 'InpPriceField3', 'py': 'InpPriceField3', 'param': 'InpPriceField3', 'type': 'int', 'default': 0, 'label': 'Stoch 3 Price field', 'sinput': False}, {'mql': 'InpPeriodK4', 'py': 'InpPeriodK4', 'param': 'InpPeriodK4', 'type': 'uint', 'default': 60, 'label': 'Stoch 4 %K period', 'sinput': False}, {'mql': 'InpPeriodD4', 'py': 'InpPeriodD4', 'param': 'InpPeriodD4', 'type': 'uint', 'default': 30, 'label': 'Stoch 4 %D period', 'sinput': False}, {'mql': 'InpSlowing4', 'py': 'InpSlowing4', 'param': 'InpSlowing4', 'type': 'uint', 'default': 15, 'label': 'Stoch 4 slowing', 'sinput': False}, {'mql': 'InpMethod4', 'py': 'InpMethod4', 'param': 'InpMethod4', 'type': 'int', 'default': 0, 'label': 'Stoch 4 Method', 'sinput': False}, {'mql': 'InpPriceField4', 'py': 'InpPriceField4', 'param': 'InpPriceField4', 'type': 'int', 'default': 0, 'label': 'Stoch 4 Price field', 'sinput': False}, {'mql': 'InpPeriodK5', 'py': 'InpPeriodK5', 'param': 'InpPeriodK5', 'type': 'uint', 'default': 70, 'label': 'Stoch 5 %K period', 'sinput': False}, {'mql': 'InpPeriodD5', 'py': 'InpPeriodD5', 'param': 'InpPeriodD5', 'type': 'uint', 'default': 17, 'label': 'Stoch 5 %D period', 'sinput': False}, {'mql': 'InpSlowing5', 'py': 'InpSlowing5', 'param': 'InpSlowing5', 'type': 'uint', 'default': 8, 'label': 'Stoch 5 slowing', 'sinput': False}, {'mql': 'InpMethod5', 'py': 'InpMethod5', 'param': 'InpMethod5', 'type': 'int', 'default': 0, 'label': 'Stoch 5 Method', 'sinput': False}, {'mql': 'InpPriceField5', 'py': 'InpPriceField5', 'param': 'InpPriceField5', 'type': 'int', 'default': 0, 'label': 'Stoch 5 Price field', 'sinput': False}, {'mql': 'InpPeriodK6', 'py': 'InpPeriodK6', 'param': 'InpPeriodK6', 'type': 'uint', 'default': 84, 'label': 'Stoch 6 %K period', 'sinput': False}, {'mql': 'InpPeriodD6', 'py': 'InpPeriodD6', 'param': 'InpPeriodD6', 'type': 'uint', 'default': 42, 'label': 'Stoch 6 %D period', 'sinput': False}, {'mql': 'InpSlowing6', 'py': 'InpSlowing6', 'param': 'InpSlowing6', 'type': 'uint', 'default': 21, 'label': 'Stoch 6 slowing', 'sinput': False}, {'mql': 'InpMethod6', 'py': 'InpMethod6', 'param': 'InpMethod6', 'type': 'int', 'default': 0, 'label': 'Stoch 6 Method', 'sinput': False}, {'mql': 'InpPriceField6', 'py': 'InpPriceField6', 'param': 'InpPriceField6', 'type': 'int', 'default': 0, 'label': 'Stoch 6 Price field', 'sinput': False}, {'mql': 'InpPeriodK7', 'py': 'InpPeriodK7', 'param': 'InpPeriodK7', 'type': 'uint', 'default': 100, 'label': 'Stoch 7 %K period', 'sinput': False}, {'mql': 'InpPeriodD7', 'py': 'InpPeriodD7', 'param': 'InpPeriodD7', 'type': 'uint', 'default': 50, 'label': 'Stoch 7 %D period', 'sinput': False}, {'mql': 'InpSlowing7', 'py': 'InpSlowing7', 'param': 'InpSlowing7', 'type': 'uint', 'default': 25, 'label': 'Stoch 7 slowing', 'sinput': False}, {'mql': 'InpMethod7', 'py': 'InpMethod7', 'param': 'InpMethod7', 'type': 'int', 'default': 0, 'label': 'Stoch 7 Method', 'sinput': False}, {'mql': 'InpPriceField7', 'py': 'InpPriceField7', 'param': 'InpPriceField7', 'type': 'int', 'default': 0, 'label': 'Stoch 7 Price field', 'sinput': False}, {'mql': 'InpPeriodK8', 'py': 'InpPeriodK8', 'param': 'InpPeriodK8', 'type': 'uint', 'default': 120, 'label': 'Stoch 8 %K period', 'sinput': False}, {'mql': 'InpPeriodD8', 'py': 'InpPeriodD8', 'param': 'InpPeriodD8', 'type': 'uint', 'default': 60, 'label': 'Stoch 8 %D period', 'sinput': False}, {'mql': 'InpSlowing8', 'py': 'InpSlowing8', 'param': 'InpSlowing8', 'type': 'uint', 'default': 30, 'label': 'Stoch 8 slowing', 'sinput': False}, {'mql': 'InpMethod8', 'py': 'InpMethod8', 'param': 'InpMethod8', 'type': 'int', 'default': 0, 'label': 'Stoch 8 Method', 'sinput': False}, {'mql': 'InpPriceField8', 'py': 'InpPriceField8', 'param': 'InpPriceField8', 'type': 'int', 'default': 0, 'label': 'Stoch 8 Price field', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodK1 = _input('InpPeriodK1', 36)  # Stoch 1 %K period
InpPeriodD1 = _input('InpPeriodD1', 18)  # Stoch 1 %D period
InpSlowing1 = _input('InpSlowing1', 9)  # Stoch 1 slowing
InpMethod1 = _input('InpMethod1', MODE_SMA)  # Stoch 1 Method
InpPriceField1 = _input('InpPriceField1', STO_LOWHIGH)  # Stoch 1 Price field
InpPeriodK2 = _input('InpPeriodK2', 40)  # Stoch 2 %K period
InpPeriodD2 = _input('InpPeriodD2', 20)  # Stoch 2 %D period
InpSlowing2 = _input('InpSlowing2', 10)  # Stoch 2 slowing
InpMethod2 = _input('InpMethod2', MODE_SMA)  # Stoch 2 Method
InpPriceField2 = _input('InpPriceField2', STO_LOWHIGH)  # Stoch 2 Price field
InpPeriodK3 = _input('InpPeriodK3', 52)  # Stoch 3 %K period
InpPeriodD3 = _input('InpPeriodD3', 26)  # Stoch 3 %D period
InpSlowing3 = _input('InpSlowing3', 13)  # Stoch 3 slowing
InpMethod3 = _input('InpMethod3', MODE_SMA)  # Stoch 3 Method
InpPriceField3 = _input('InpPriceField3', STO_LOWHIGH)  # Stoch 3 Price field
InpPeriodK4 = _input('InpPeriodK4', 60)  # Stoch 4 %K period
InpPeriodD4 = _input('InpPeriodD4', 30)  # Stoch 4 %D period
InpSlowing4 = _input('InpSlowing4', 15)  # Stoch 4 slowing
InpMethod4 = _input('InpMethod4', MODE_SMA)  # Stoch 4 Method
InpPriceField4 = _input('InpPriceField4', STO_LOWHIGH)  # Stoch 4 Price field
InpPeriodK5 = _input('InpPeriodK5', 70)  # Stoch 5 %K period
InpPeriodD5 = _input('InpPeriodD5', 17)  # Stoch 5 %D period
InpSlowing5 = _input('InpSlowing5', 8)  # Stoch 5 slowing
InpMethod5 = _input('InpMethod5', MODE_SMA)  # Stoch 5 Method
InpPriceField5 = _input('InpPriceField5', STO_LOWHIGH)  # Stoch 5 Price field
InpPeriodK6 = _input('InpPeriodK6', 84)  # Stoch 6 %K period
InpPeriodD6 = _input('InpPeriodD6', 42)  # Stoch 6 %D period
InpSlowing6 = _input('InpSlowing6', 21)  # Stoch 6 slowing
InpMethod6 = _input('InpMethod6', MODE_SMA)  # Stoch 6 Method
InpPriceField6 = _input('InpPriceField6', STO_LOWHIGH)  # Stoch 6 Price field
InpPeriodK7 = _input('InpPeriodK7', 100)  # Stoch 7 %K period
InpPeriodD7 = _input('InpPeriodD7', 50)  # Stoch 7 %D period
InpSlowing7 = _input('InpSlowing7', 25)  # Stoch 7 slowing
InpMethod7 = _input('InpMethod7', MODE_SMA)  # Stoch 7 Method
InpPriceField7 = _input('InpPriceField7', STO_LOWHIGH)  # Stoch 7 Price field
InpPeriodK8 = _input('InpPeriodK8', 120)  # Stoch 8 %K period
InpPeriodD8 = _input('InpPeriodD8', 60)  # Stoch 8 %D period
InpSlowing8 = _input('InpSlowing8', 30)  # Stoch 8 slowing
InpMethod8 = _input('InpMethod8', MODE_SMA)  # Stoch 8 Method
InpPriceField8 = _input('InpPriceField8', STO_LOWHIGH)  # Stoch 8 Price field
BufferSS = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferSto1 = Arr(0, 0.0)
BufferSto2 = Arr(0, 0.0)
BufferSto3 = Arr(0, 0.0)
BufferSto4 = Arr(0, 0.0)
BufferSto5 = Arr(0, 0.0)
BufferSto6 = Arr(0, 0.0)
BufferSto7 = Arr(0, 0.0)
BufferSto8 = Arr(0, 0.0)
period_k1 = 0
period_d1 = 0
slowing1 = 0
period_k2 = 0
period_d2 = 0
slowing2 = 0
period_k3 = 0
period_d3 = 0
slowing3 = 0
period_k4 = 0
period_d4 = 0
slowing4 = 0
period_k5 = 0
period_d5 = 0
slowing5 = 0
period_k6 = 0
period_d6 = 0
slowing6 = 0
period_k7 = 0
period_d7 = 0
slowing7 = 0
period_k8 = 0
period_d8 = 0
slowing8 = 0
handle_sto1 = 0
handle_sto2 = 0
handle_sto3 = 0
handle_sto4 = 0
handle_sto5 = 0
handle_sto6 = 0
handle_sto7 = 0
handle_sto8 = 0

def OnInit():
    global handle_sto1, handle_sto2, handle_sto3, handle_sto4, handle_sto5, handle_sto6, handle_sto7, handle_sto8, period_d1, period_d2, period_d3, period_d4, period_d5, period_d6, period_d7, period_d8, period_k1, period_k2, period_k3, period_k4, period_k5, period_k6, period_k7, period_k8, slowing1, slowing2, slowing3, slowing4, slowing5, slowing6, slowing7, slowing8
    period_k1 = (1 if (InpPeriodK1 < 1) else InpPeriodK1)
    period_d1 = (1 if (InpPeriodD1 < 1) else InpPeriodD1)
    slowing1 = (1 if (InpSlowing1 < 1) else InpSlowing1)
    period_k2 = (1 if (InpPeriodK2 < 1) else InpPeriodK2)
    period_d2 = (1 if (InpPeriodD2 < 1) else InpPeriodD2)
    slowing2 = (1 if (InpSlowing2 < 1) else InpSlowing2)
    period_k3 = (1 if (InpPeriodK3 < 1) else InpPeriodK3)
    period_d3 = (1 if (InpPeriodD3 < 1) else InpPeriodD3)
    slowing3 = (1 if (InpSlowing3 < 1) else InpSlowing3)
    period_k4 = (1 if (InpPeriodK4 < 1) else InpPeriodK4)
    period_d4 = (1 if (InpPeriodD4 < 1) else InpPeriodD4)
    slowing4 = (1 if (InpSlowing4 < 1) else InpSlowing4)
    period_k5 = (1 if (InpPeriodK5 < 1) else InpPeriodK5)
    period_d5 = (1 if (InpPeriodD5 < 1) else InpPeriodD5)
    slowing5 = (1 if (InpSlowing5 < 1) else InpSlowing5)
    period_k6 = (1 if (InpPeriodK6 < 1) else InpPeriodK6)
    period_d6 = (1 if (InpPeriodD6 < 1) else InpPeriodD6)
    slowing6 = (1 if (InpSlowing6 < 1) else InpSlowing6)
    period_k7 = (1 if (InpPeriodK7 < 1) else InpPeriodK7)
    period_d7 = (1 if (InpPeriodD7 < 1) else InpPeriodD7)
    slowing7 = (1 if (InpSlowing7 < 1) else InpSlowing7)
    period_k8 = (1 if (InpPeriodK8 < 1) else InpPeriodK8)
    period_d8 = (1 if (InpPeriodD8 < 1) else InpPeriodD8)
    slowing8 = (1 if (InpSlowing8 < 1) else InpSlowing8)
    SetIndexBuffer(0, BufferSS, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferSto1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferSto2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferSto3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferSto4, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferSto5, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferSto6, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferSto7, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferSto8, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stochastic Stack')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferSS, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferSto1, True)
    ArraySetAsSeries(BufferSto2, True)
    ArraySetAsSeries(BufferSto3, True)
    ArraySetAsSeries(BufferSto4, True)
    ArraySetAsSeries(BufferSto5, True)
    ArraySetAsSeries(BufferSto6, True)
    ArraySetAsSeries(BufferSto7, True)
    ArraySetAsSeries(BufferSto8, True)
    ResetLastError()
    handle_sto1 = iStochastic(None, PERIOD_CURRENT, period_k1, period_d1, slowing1, InpMethod1, InpPriceField1)
    if handle_sto1 == INVALID_HANDLE:
        Print('The iStochastic(', _str(period_k1), ',', _str(period_d1), ',', _str(slowing1), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sto2 = iStochastic(None, PERIOD_CURRENT, period_k2, period_d2, slowing2, InpMethod2, InpPriceField2)
    if handle_sto2 == INVALID_HANDLE:
        Print('The iStochastic(', _str(period_k2), ',', _str(period_d2), ',', _str(slowing2), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sto3 = iStochastic(None, PERIOD_CURRENT, period_k3, period_d3, slowing3, InpMethod3, InpPriceField3)
    if handle_sto3 == INVALID_HANDLE:
        Print('The iStochastic(', _str(period_k3), ',', _str(period_d3), ',', _str(slowing3), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sto4 = iStochastic(None, PERIOD_CURRENT, period_k4, period_d4, slowing4, InpMethod4, InpPriceField4)
    if handle_sto4 == INVALID_HANDLE:
        Print('The iStochastic(', _str(period_k4), ',', _str(period_d4), ',', _str(slowing4), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sto5 = iStochastic(None, PERIOD_CURRENT, period_k5, period_d5, slowing5, InpMethod5, InpPriceField5)
    if handle_sto5 == INVALID_HANDLE:
        Print('The iStochastic(', _str(period_k5), ',', _str(period_d5), ',', _str(slowing5), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sto6 = iStochastic(None, PERIOD_CURRENT, period_k6, period_d6, slowing6, InpMethod6, InpPriceField6)
    if handle_sto6 == INVALID_HANDLE:
        Print('The iStochastic(', _str(period_k6), ',', _str(period_d6), ',', _str(slowing6), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sto7 = iStochastic(None, PERIOD_CURRENT, period_k7, period_d7, slowing7, InpMethod7, InpPriceField7)
    if handle_sto7 == INVALID_HANDLE:
        Print('The iStochastic(', _str(period_k7), ',', _str(period_d7), ',', _str(slowing7), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sto8 = iStochastic(None, PERIOD_CURRENT, period_k8, period_d8, slowing8, InpMethod8, InpPriceField8)
    if handle_sto8 == INVALID_HANDLE:
        Print('The iStochastic(', _str(period_k8), ',', _str(period_d8), ',', _str(slowing8), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferSS, EMPTY_VALUE)
        ArrayInitialize(BufferSto1, 0)
        ArrayInitialize(BufferSto2, 0)
        ArrayInitialize(BufferSto3, 0)
        ArrayInitialize(BufferSto4, 0)
        ArrayInitialize(BufferSto5, 0)
        ArrayInitialize(BufferSto6, 0)
        ArrayInitialize(BufferSto7, 0)
        ArrayInitialize(BufferSto8, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_sto1, MAIN_LINE, 0, count, BufferSto1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sto2, MAIN_LINE, 0, count, BufferSto2)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sto3, MAIN_LINE, 0, count, BufferSto3)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sto4, MAIN_LINE, 0, count, BufferSto4)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sto5, MAIN_LINE, 0, count, BufferSto5)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sto6, MAIN_LINE, 0, count, BufferSto6)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sto7, MAIN_LINE, 0, count, BufferSto7)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sto8, MAIN_LINE, 0, count, BufferSto8)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        Stoch1 = BufferSto1[i]
        Stoch2 = BufferSto2[i]
        Stoch3 = BufferSto3[i]
        Stoch4 = BufferSto4[i]
        Stoch5 = BufferSto5[i]
        Stoch6 = BufferSto6[i]
        Stoch7 = BufferSto7[i]
        Stoch8 = BufferSto8[i]
        BufferSS[i] = Stoch1 - Stoch2 + Stoch3 - Stoch4 + Stoch5 - Stoch6 + Stoch7 - Stoch8
        BufferColors[i] = (0 if (BufferSS[i] > 0) else 1 if (BufferSS[i] < 0) else 2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SS(_MQL5Indicator):
    name = 'SS'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodK1': 36,  # Stoch 1 %K period
        'InpPeriodD1': 18,  # Stoch 1 %D period
        'InpSlowing1': 9,  # Stoch 1 slowing
        'InpMethod1': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Stoch 1 Method
        'InpPriceField1': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stoch 1 Price field
        'InpPeriodK2': 40,  # Stoch 2 %K period
        'InpPeriodD2': 20,  # Stoch 2 %D period
        'InpSlowing2': 10,  # Stoch 2 slowing
        'InpMethod2': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Stoch 2 Method
        'InpPriceField2': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stoch 2 Price field
        'InpPeriodK3': 52,  # Stoch 3 %K period
        'InpPeriodD3': 26,  # Stoch 3 %D period
        'InpSlowing3': 13,  # Stoch 3 slowing
        'InpMethod3': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Stoch 3 Method
        'InpPriceField3': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stoch 3 Price field
        'InpPeriodK4': 60,  # Stoch 4 %K period
        'InpPeriodD4': 30,  # Stoch 4 %D period
        'InpSlowing4': 15,  # Stoch 4 slowing
        'InpMethod4': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Stoch 4 Method
        'InpPriceField4': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stoch 4 Price field
        'InpPeriodK5': 70,  # Stoch 5 %K period
        'InpPeriodD5': 17,  # Stoch 5 %D period
        'InpSlowing5': 8,  # Stoch 5 slowing
        'InpMethod5': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Stoch 5 Method
        'InpPriceField5': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stoch 5 Price field
        'InpPeriodK6': 84,  # Stoch 6 %K period
        'InpPeriodD6': 42,  # Stoch 6 %D period
        'InpSlowing6': 21,  # Stoch 6 slowing
        'InpMethod6': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Stoch 6 Method
        'InpPriceField6': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stoch 6 Price field
        'InpPeriodK7': 100,  # Stoch 7 %K period
        'InpPeriodD7': 50,  # Stoch 7 %D period
        'InpSlowing7': 25,  # Stoch 7 slowing
        'InpMethod7': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Stoch 7 Method
        'InpPriceField7': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stoch 7 Price field
        'InpPeriodK8': 120,  # Stoch 8 %K period
        'InpPeriodD8': 60,  # Stoch 8 %D period
        'InpSlowing8': 30,  # Stoch 8 slowing
        'InpMethod8': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Stoch 8 Method
        'InpPriceField8': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stoch 8 Price field
    }

