"""Onisuk_Filter — converted from MQL5: MQL5 Indicators/Onisuk_Filter/Onisuk_Filter.mq5

Onisuk Filter Helper indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 14, 'indicator_plots': 6}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5}, 'colors': {1: [32768], 2: [255], 3: [32768], 4: [255], 5: [32768], 6: [255]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'Scenario 1 UP', 2: 'Scenario 1 DN', 3: 'Scenario 2 UP', 4: 'Scenario 2 DN', 5: 'Scenario 3 UP', 6: 'Scenario 3 DN'}, 'levels': [], 'description': ['Onisuk Filter Helper indicator'], 'name': 'Onisuk_Filter', 'source': 'MQL5 Indicators/Onisuk_Filter/Onisuk_Filter.mq5', 'folder': 'Onisuk_Filter', 'inputs': [{'mql': 'InpUseSC1', 'py': 'InpUseSC1', 'param': 'InpUseSC1', 'type': 'int', 'default': 1, 'label': 'Use scenario 1 "Power Trend"', 'sinput': False}, {'mql': 'InpPeriod11', 'py': 'InpPeriod11', 'param': 'InpPeriod11', 'type': 'uint', 'default': 3, 'label': 'Scenario 1, Period 1', 'sinput': False}, {'mql': 'InpMethod11', 'py': 'InpMethod11', 'param': 'InpMethod11', 'type': 'int', 'default': 1, 'label': 'Scenario 1, Method 1', 'sinput': False}, {'mql': 'InpPeriod12', 'py': 'InpPeriod12', 'param': 'InpPeriod12', 'type': 'uint', 'default': 7, 'label': 'Scenario 1, Period 2', 'sinput': False}, {'mql': 'InpMethod12', 'py': 'InpMethod12', 'param': 'InpMethod12', 'type': 'int', 'default': 1, 'label': 'Scenario 1, Method 2', 'sinput': False}, {'mql': 'InpPeriod13', 'py': 'InpPeriod13', 'param': 'InpPeriod13', 'type': 'uint', 'default': 50, 'label': 'Scenario 1, Period 3', 'sinput': False}, {'mql': 'InpMethod13', 'py': 'InpMethod13', 'param': 'InpMethod13', 'type': 'int', 'default': 1, 'label': 'Scenario 1, Method 3', 'sinput': False}, {'mql': 'InpUseSC2', 'py': 'InpUseSC2', 'param': 'InpUseSC2', 'type': 'int', 'default': 0, 'label': 'Use scenario 2 "Medium MA Bounce"', 'sinput': False}, {'mql': 'InpPeriod21', 'py': 'InpPeriod21', 'param': 'InpPeriod21', 'type': 'uint', 'default': 20, 'label': 'Scenario 2, Period 1', 'sinput': False}, {'mql': 'InpMethod21', 'py': 'InpMethod21', 'param': 'InpMethod21', 'type': 'int', 'default': 1, 'label': 'Scenario 2, Method 1', 'sinput': False}, {'mql': 'InpPeriod22', 'py': 'InpPeriod22', 'param': 'InpPeriod22', 'type': 'uint', 'default': 50, 'label': 'Scenario 2, Period 2', 'sinput': False}, {'mql': 'InpMethod22', 'py': 'InpMethod22', 'param': 'InpMethod22', 'type': 'int', 'default': 1, 'label': 'Scenario 2, Method 2', 'sinput': False}, {'mql': 'InpUseSC3', 'py': 'InpUseSC3', 'param': 'InpUseSC3', 'type': 'int', 'default': 0, 'label': 'Use scenario 3 "Slow MA Bounce"', 'sinput': False}, {'mql': 'InpPeriod31', 'py': 'InpPeriod31', 'param': 'InpPeriod31', 'type': 'uint', 'default': 20, 'label': 'Scenario 3, Period 1', 'sinput': False}, {'mql': 'InpMethod31', 'py': 'InpMethod31', 'param': 'InpMethod31', 'type': 'int', 'default': 1, 'label': 'Scenario 3, Method 1', 'sinput': False}, {'mql': 'InpPeriod32', 'py': 'InpPeriod32', 'param': 'InpPeriod32', 'type': 'uint', 'default': 50, 'label': 'Scenario 3, Period 2', 'sinput': False}, {'mql': 'InpMethod32', 'py': 'InpMethod32', 'param': 'InpMethod32', 'type': 'int', 'default': 1, 'label': 'Scenario 3, Method 2', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpUseSC1 = _input('InpUseSC1', INPUT_YES)  # Use scenario 1 "Power Trend"
InpPeriod11 = _input('InpPeriod11', 3)  # Scenario 1, Period 1
InpMethod11 = _input('InpMethod11', MODE_EMA)  # Scenario 1, Method 1
InpPeriod12 = _input('InpPeriod12', 7)  # Scenario 1, Period 2
InpMethod12 = _input('InpMethod12', MODE_EMA)  # Scenario 1, Method 2
InpPeriod13 = _input('InpPeriod13', 50)  # Scenario 1, Period 3
InpMethod13 = _input('InpMethod13', MODE_EMA)  # Scenario 1, Method 3
InpUseSC2 = _input('InpUseSC2', INPUT_NO)  # Use scenario 2 "Medium MA Bounce"
InpPeriod21 = _input('InpPeriod21', 20)  # Scenario 2, Period 1
InpMethod21 = _input('InpMethod21', MODE_EMA)  # Scenario 2, Method 1
InpPeriod22 = _input('InpPeriod22', 50)  # Scenario 2, Period 2
InpMethod22 = _input('InpMethod22', MODE_EMA)  # Scenario 2, Method 2
InpUseSC3 = _input('InpUseSC3', INPUT_NO)  # Use scenario 3 "Slow MA Bounce"
InpPeriod31 = _input('InpPeriod31', 20)  # Scenario 3, Period 1
InpMethod31 = _input('InpMethod31', MODE_EMA)  # Scenario 3, Method 1
InpPeriod32 = _input('InpPeriod32', 50)  # Scenario 3, Period 2
InpMethod32 = _input('InpMethod32', MODE_EMA)  # Scenario 3, Method 2
BufferUP1 = Arr(0, 0.0)
BufferDN1 = Arr(0, 0.0)
BufferUP2 = Arr(0, 0.0)
BufferDN2 = Arr(0, 0.0)
BufferUP3 = Arr(0, 0.0)
BufferDN3 = Arr(0, 0.0)
BufferMA11 = Arr(0, 0.0)
BufferMA12 = Arr(0, 0.0)
BufferMA13 = Arr(0, 0.0)
BufferMA21 = Arr(0, 0.0)
BufferMA22 = Arr(0, 0.0)
BufferMA31 = Arr(0, 0.0)
BufferMA32 = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
period11 = 0
period12 = 0
period13 = 0
period21 = 0
period22 = 0
period31 = 0
period32 = 0
period_atr = 0
handle_ma11 = 0
handle_ma12 = 0
handle_ma13 = 0
handle_ma21 = 0
handle_ma22 = 0
handle_ma31 = 0
handle_ma32 = 0
handle_atr = 0

def OnInit():
    global handle_atr, handle_ma11, handle_ma12, handle_ma13, handle_ma21, handle_ma22, handle_ma31, handle_ma32, period11, period12, period13, period21, period22, period31, period32, period_atr
    period_atr = 14
    period11 = (1 if (InpPeriod11 < 1) else InpPeriod11)
    period12 = (1 if (InpPeriod12 < 1) else InpPeriod12)
    period13 = (1 if (InpPeriod13 < 1) else InpPeriod13)
    period21 = (1 if (InpPeriod21 < 1) else InpPeriod21)
    period22 = (1 if (InpPeriod22 < 1) else InpPeriod22)
    period31 = (1 if (InpPeriod31 < 1) else InpPeriod31)
    period32 = (1 if (InpPeriod32 < 1) else InpPeriod32)
    SetIndexBuffer(0, BufferUP1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDN1, INDICATOR_DATA)
    SetIndexBuffer(2, BufferUP2, INDICATOR_DATA)
    SetIndexBuffer(3, BufferDN2, INDICATOR_DATA)
    SetIndexBuffer(4, BufferUP3, INDICATOR_DATA)
    SetIndexBuffer(5, BufferDN3, INDICATOR_DATA)
    SetIndexBuffer(6, BufferMA11, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferMA12, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferMA13, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferMA21, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, BufferMA22, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, BufferMA31, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, BufferMA32, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, BufferATR, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 241)
    PlotIndexSetInteger(1, PLOT_ARROW, 242)
    PlotIndexSetInteger(2, PLOT_ARROW, 241)
    PlotIndexSetInteger(3, PLOT_ARROW, 242)
    PlotIndexSetInteger(4, PLOT_ARROW, 241)
    PlotIndexSetInteger(5, PLOT_ARROW, 242)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Onisuk Filter Helper')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferUP1, True)
    ArraySetAsSeries(BufferDN1, True)
    ArraySetAsSeries(BufferUP2, True)
    ArraySetAsSeries(BufferDN2, True)
    ArraySetAsSeries(BufferUP3, True)
    ArraySetAsSeries(BufferDN3, True)
    ArraySetAsSeries(BufferMA11, True)
    ArraySetAsSeries(BufferMA12, True)
    ArraySetAsSeries(BufferMA13, True)
    ArraySetAsSeries(BufferMA21, True)
    ArraySetAsSeries(BufferMA22, True)
    ArraySetAsSeries(BufferMA31, True)
    ArraySetAsSeries(BufferMA32, True)
    ArraySetAsSeries(BufferATR, True)
    ResetLastError()
    handle_ma11 = iMA(None, PERIOD_CURRENT, period11, 0, InpMethod11, PRICE_CLOSE)
    if handle_ma11 == INVALID_HANDLE:
        Print('The iMA(', _str(period11), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma12 = iMA(None, PERIOD_CURRENT, period12, 0, InpMethod12, PRICE_CLOSE)
    if handle_ma12 == INVALID_HANDLE:
        Print('The iMA(', _str(period12), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma13 = iMA(None, PERIOD_CURRENT, period13, 0, InpMethod13, PRICE_CLOSE)
    if handle_ma13 == INVALID_HANDLE:
        Print('The iMA(', _str(period13), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma21 = iMA(None, PERIOD_CURRENT, period21, 0, InpMethod21, PRICE_CLOSE)
    if handle_ma21 == INVALID_HANDLE:
        Print('The iMA(', _str(period21), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma22 = iMA(None, PERIOD_CURRENT, period22, 0, InpMethod22, PRICE_CLOSE)
    if handle_ma22 == INVALID_HANDLE:
        Print('The iMA(', _str(period22), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma31 = iMA(None, PERIOD_CURRENT, period31, 0, InpMethod31, PRICE_CLOSE)
    if handle_ma31 == INVALID_HANDLE:
        Print('The iMA(', _str(period31), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma32 = iMA(None, PERIOD_CURRENT, period32, 0, InpMethod32, PRICE_CLOSE)
    if handle_ma32 == INVALID_HANDLE:
        Print('The iMA(', _str(period32), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_atr = iATR(None, PERIOD_CURRENT, period_atr)
    if handle_atr == INVALID_HANDLE:
        Print('The iATR(', _str(period_atr), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferUP1, EMPTY_VALUE)
        ArrayInitialize(BufferDN1, EMPTY_VALUE)
        ArrayInitialize(BufferUP2, EMPTY_VALUE)
        ArrayInitialize(BufferDN2, EMPTY_VALUE)
        ArrayInitialize(BufferUP3, EMPTY_VALUE)
        ArrayInitialize(BufferDN3, EMPTY_VALUE)
        ArrayInitialize(BufferMA11, 0)
        ArrayInitialize(BufferMA12, 0)
        ArrayInitialize(BufferMA13, 0)
        ArrayInitialize(BufferMA21, 0)
        ArrayInitialize(BufferMA22, 0)
        ArrayInitialize(BufferMA31, 0)
        ArrayInitialize(BufferMA32, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma11, 0, 0, count, BufferMA11)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma12, 0, 0, count, BufferMA12)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma13, 0, 0, count, BufferMA13)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma21, 0, 0, count, BufferMA21)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma22, 0, 0, count, BufferMA22)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma31, 0, 0, count, BufferMA31)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma32, 0, 0, count, BufferMA32)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_atr, 0, 0, count, BufferATR)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferDN3[i] = EMPTY_VALUE
        BufferUP3[i] = BufferDN3[i]
        BufferDN2[i] = BufferUP3[i]
        BufferUP2[i] = BufferDN2[i]
        BufferDN1[i] = BufferUP2[i]
        BufferUP1[i] = BufferDN1[i]
        res1 = GetData1(i, open, close)
        res2 = GetData2(i, open, high, low, close)
        res3 = GetData3(i, open, high, low, close)
        if res1 == 1:
            BufferUP1[i] = low[i] - (BufferATR[i] / 2.0)
        if res2 == 1:
            BufferUP2[i] = low[i] - (BufferATR[i] / 2.0)
        if res3 == 1:
            BufferUP3[i] = low[i] - (BufferATR[i] / 2.0)
        if res1 == -1:
            BufferDN1[i] = high[i] + (BufferATR[i] / 2.0)
        if res2 == -1:
            BufferDN2[i] = high[i] + (BufferATR[i] / 2.0)
        if res3 == -1:
            BufferDN3[i] = high[i] + (BufferATR[i] / 2.0)
    return rates_total

def GetData1(index, open, close):
    if not InpUseSC1:
        return 0
    MA1 = BufferMA11[index]
    MA2 = BufferMA12[index]
    MA3 = BufferMA13[index]
    return (1 if ((MA1 > MA2 and MA2 > MA3) and close[index] < open[index]) else -1 if ((MA1 < MA2 and MA2 < MA3) and close[index] < open[index]) else 0)

def GetData2(index, open, high, low, close):
    if not InpUseSC2:
        return 0
    MA1 = BufferMA21[index]
    MA2 = BufferMA22[index]
    return (1 if (((MA1 > MA2 and low[index] < MA1) and open[index] > MA1) and close[index] > MA1) else -1 if (((MA1 < MA2 and high[index] > MA1) and open[index] < MA1) and close[index] < MA1) else 0)

def GetData3(index, open, high, low, close):
    if not InpUseSC3:
        return 0
    MA1 = BufferMA31[index]
    MA2 = BufferMA32[index]
    return (1 if (((MA1 > MA2 and low[index] < MA2) and open[index] > MA2) and close[index] > MA2) else -1 if (((MA1 < MA2 and high[index] > MA2) and open[index] < MA2) and close[index] < MA2) else 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class OnisukFilter(_MQL5Indicator):
    name = 'Onisuk_Filter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpUseSC1': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use scenario 1 "Power Trend"
        'InpPeriod11': 3,  # Scenario 1, Period 1
        'InpMethod11': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Scenario 1, Method 1
        'InpPeriod12': 7,  # Scenario 1, Period 2
        'InpMethod12': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Scenario 1, Method 2
        'InpPeriod13': 50,  # Scenario 1, Period 3
        'InpMethod13': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Scenario 1, Method 3
        'InpUseSC2': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Use scenario 2 "Medium MA Bounce"
        'InpPeriod21': 20,  # Scenario 2, Period 1
        'InpMethod21': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Scenario 2, Method 1
        'InpPeriod22': 50,  # Scenario 2, Period 2
        'InpMethod22': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Scenario 2, Method 2
        'InpUseSC3': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Use scenario 3 "Slow MA Bounce"
        'InpPeriod31': 20,  # Scenario 3, Period 1
        'InpMethod31': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Scenario 3, Method 1
        'InpPeriod32': 50,  # Scenario 3, Period 2
        'InpMethod32': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Scenario 3, Method 2
    }

