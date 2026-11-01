"""HVR — converted from MQL5: MQL5 Indicators/HVR/HVR.mq5

Historical Volatility Ratio indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [2970272]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'HVR'}, 'levels': [], 'description': ['Historical Volatility Ratio indicator'], 'name': 'HVR', 'source': 'MQL5 Indicators/HVR/HVR.mq5', 'folder': 'HVR', 'inputs': [{'mql': 'InpPeriod1', 'py': 'InpPeriod1', 'param': 'InpPeriod1', 'type': 'uint', 'default': 6, 'label': 'First deviation period', 'sinput': False}, {'mql': 'InpPeriod2', 'py': 'InpPeriod2', 'param': 'InpPeriod2', 'type': 'uint', 'default': 100, 'label': 'Second deviation period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpThreshold', 'py': 'InpThreshold', 'param': 'InpThreshold', 'type': 'double', 'default': 0.5, 'label': 'Threshold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod1 = _input('InpPeriod1', 6)  # First deviation period
InpPeriod2 = _input('InpPeriod2', 100)  # Second deviation period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpThreshold = _input('InpThreshold', 0.5)  # Threshold
BufferHVR = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferST = Arr(0, 0.0)
period_1 = 0
period_2 = 0
handle_ma = 0
period_max = 0
threshold = 0.0

def OnInit():
    global handle_ma, period_1, period_2, period_max, threshold
    period_1 = (1 if (InpPeriod1 < 1) else InpPeriod1)
    period_2 = (1 if (InpPeriod2 < 1) else InpPeriod2)
    period_max = fmax(period_1, period_2)
    threshold = (0.01 if (InpThreshold < 0.01) else InpThreshold)
    SetIndexBuffer(0, BufferHVR, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferST, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Historical Volatility Ratio (' + _str(period_1) + ',' + _str(period_2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, threshold)
    ArraySetAsSeries(BufferHVR, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferST, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_max:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 2
        ArrayInitialize(BufferHVR, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferST, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferST[i] = log(_fdiv(BufferMA[i], BufferMA[i + 1]))
    for i in range(limit, 0 - 1, -1):
        Dev2 = StdDev(BufferST, period_2, i)
        BufferHVR[i] = _fdiv(StdDev(BufferST, period_1, i), (Dev2 if (Dev2 != 0) else 1.0))
    return rates_total

def StdDev(array, period, index):
    avg = 0.0
    for i in range(0, period):
        avg += array[index + i]
    avg = _fdiv(avg, period)
    SD = 0.0
    for i in range(0, period):
        SD += (avg - array[index + i]) * (avg - array[index + i])
    SD = sqrt(_fdiv(SD, period))
    return SD


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HVR(_MQL5Indicator):
    name = 'HVR'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod1': 6,  # First deviation period
        'InpPeriod2': 100,  # Second deviation period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpThreshold': 0.5,  # Threshold
    }

