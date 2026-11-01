"""XMA — converted from MQL5: MQL5 Indicators/XMA/XMA.mq5

Digital adaptive Moving Average
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [17919]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'XMA'}, 'levels': [], 'description': ['Digital adaptive Moving Average'], 'name': 'XMA', 'source': 'MQL5 Indicators/XMA/XMA.mq5', 'folder': 'XMA', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpStep', 'py': 'InpStep', 'param': 'InpStep', 'type': 'double', 'default': 20.0, 'label': 'Price X step', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpStep = _input('InpStep', 20.0)  # Price X step
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferXMA = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
step = 0.0
step_pt = 0.0
period = 0
handle_ma = 0

def OnInit():
    global handle_ma, period, step, step_pt
    period = (1 if (InpPeriod < 1) else InpPeriod)
    step = (0 if (InpStep < 0) else InpStep)
    step_pt = fabs(InpStep) * Point()
    SetIndexBuffer(0, BufferXMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'XMA (' + _str(period) + ',' + DoubleToString(step, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferXMA, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferXMA, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        ma0 = BufferMA[i]
        ma1 = BufferMA[i + 1]
        BufferXMA[i] = (BufferXMA[i + 1] if (fabs(ma0 - ma1) < step_pt) else ma0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XMA(_MQL5Indicator):
    name = 'XMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpStep': 20.0,  # Price X step
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

