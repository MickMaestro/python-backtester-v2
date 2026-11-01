"""Super_Smoother — converted from MQL5: MQL5 Indicators/Super_Smoother/Super_Smoother.mq5

Ehlers SuperSmoother indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [11829830]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'SuperSmoother'}, 'levels': [], 'description': ['Ehlers SuperSmoother indicator'], 'name': 'Super_Smoother', 'source': 'MQL5 Indicators/Super_Smoother/Super_Smoother.mq5', 'folder': 'Super_Smoother', 'inputs': [{'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferSS = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
handle_ma = 0
a1 = 0.0
b1 = 0.0
c2 = 0.0
c3 = 0.0
c1 = 0.0

def OnInit():
    global a1, b1, c1, c2, c3, handle_ma
    a1 = exp((-1.414 * 3.1415926) / 10.0)
    b1 = 2.0 * a1 * cos((1.414 * 180.0) / 10.0)
    c2 = b1
    c3 = (-a1) * a1
    c1 = 1.0 - c2 - c3
    SetIndexBuffer(0, BufferSS, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Ehlers SuperSmoother')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 16)
    ArraySetAsSeries(BufferSS, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (16 + 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 3
        ArrayInitialize(BufferSS, 0)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferSS[i] = ((c1 * (BufferMA[i] + BufferMA[i + 1])) / 2.0) + (c2 * BufferSS[i + 1]) + (c3 * BufferSS[i + 2])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SuperSmoother(_MQL5Indicator):
    name = 'Super_Smoother'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

