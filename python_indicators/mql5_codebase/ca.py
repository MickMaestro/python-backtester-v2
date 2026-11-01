"""CA — converted from MQL5: MQL5 Indicators/CA/CA.mq5

Corrected Average indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [2970272]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'CA'}, 'levels': [], 'description': ['Corrected Average indicator'], 'name': 'CA', 'source': 'MQL5 Indicators/CA/CA.mq5', 'folder': 'CA', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferCA = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferDev = Arr(0, 0.0)
period = 0
handle_ma = 0
handle_dev = 0

def OnInit():
    global handle_dev, handle_ma, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferCA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferDev, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CA (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, period)
    ArraySetAsSeries(BufferCA, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferDev, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_dev = iStdDev(None, PERIOD_CURRENT, period, 0, MODE_SMA, InpAppliedPrice)
    if handle_dev == INVALID_HANDLE:
        Print('The iStdDev(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferCA, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferDev, 0)
        BufferCA[limit] = 0.0
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_dev, 0, 0, count, BufferDev)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        dev = BufferDev[i] * BufferDev[i]
        diff = (BufferCA[i + 1] - BufferMA[i]) * (BufferCA[i + 1] - BufferMA[i])
        k = ((1.0 - _fdiv(dev, diff)) if (diff > dev and diff != 0) else 0)
        BufferCA[i] = BufferCA[i + 1] + (k * (BufferMA[i] - BufferCA[i + 1]))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CA(_MQL5Indicator):
    name = 'CA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

