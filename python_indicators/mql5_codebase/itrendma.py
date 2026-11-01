"""ITrendMA — converted from MQL5: MQL5 Indicators/ITrendMA/ITrendMA.mq5

Instantaneous Trendline by J.Ehlers
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'ITMA'}, 'levels': [], 'description': ['Instantaneous Trendline by J.Ehlers'], 'name': 'ITrendMA', 'source': 'MQL5 Indicators/ITrendMA/ITrendMA.mq5', 'folder': 'ITrendMA', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferITMA = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period_ma = 0
handle_ma = 0
alpha = 0.0
c1 = 0.0
c2 = 0.0
c3 = 0.0
c4 = 0.0
c5 = 0.0

def OnInit():
    global alpha, c1, c2, c3, c4, c5, handle_ma, period_ma
    period_ma = (1 if (InpPeriod < 1) else InpPeriod)
    alpha = _fdiv(2.0, float(period_ma + 1))
    c1 = alpha - ((alpha * alpha) / 4)
    c2 = (alpha * alpha) / 2
    c3 = alpha - (0.75 * alpha * alpha)
    c4 = 2 * (1 - alpha)
    c5 = (1 - alpha) * (1 - alpha)
    SetIndexBuffer(0, BufferITMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ITrendMA(' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferITMA, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_ma:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 3
        ArrayInitialize(BufferITMA, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        if i > (rates_total - 6):
            BufferITMA[i] = (BufferMA[i] + (2 * BufferMA[i + 1]) + BufferMA[i + 2]) / 4
        else:
            BufferITMA[i] = (c1 * BufferMA[i]) + (c2 * BufferMA[i + 1]) - (c3 * BufferMA[i + 2]) + (c4 * BufferITMA[i + 1]) - (c5 * BufferITMA[i + 2])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ITrendMA(_MQL5Indicator):
    name = 'ITrendMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

