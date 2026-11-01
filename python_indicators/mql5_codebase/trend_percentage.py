"""Trend_Percentage — converted from MQL5: MQL5 Indicators/Trend_Percentage/Trend_Percentage.mq5

Trend Percentage
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [3329330], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Bulls', 2: 'Bears'}, 'levels': [], 'description': ['Trend Percentage'], 'name': 'Trend_Percentage', 'source': 'MQL5 Indicators/Trend_Percentage/Trend_Percentage.mq5', 'folder': 'Trend_Percentage', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferBulls = Arr(0, 0.0)
BufferBears = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period = 0
handle_ma = 0

def OnInit():
    global handle_ma, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferBulls, INDICATOR_DATA)
    SetIndexBuffer(1, BufferBears, INDICATOR_DATA)
    SetIndexBuffer(2, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trend Percentage(' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferBulls, True)
    ArraySetAsSeries(BufferBears, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period:
        return 0
    limit = rates_total - prev_calculated
    limit1 = limit
    if limit > 1:
        limit = rates_total - period - 2
        limit1 = limit - period
        ArrayInitialize(BufferBulls, 0)
        ArrayInitialize(BufferBears, 0)
        ArrayInitialize(BufferMA, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        SBull = 0.0
        SBear = 0.0
        for j in range(1, period + 1):
            Pr0 = BufferMA[i + j]
            Pr1 = BufferMA[i + j + 1]
            if Pr0 > Pr1:
                SBull += fabs(Pr0 - Pr1)
            elif Pr0 < Pr1:
                SBear += fabs(Pr0 - Pr1)
        Sum = SBull + SBear
        BufferBulls[i] = _fdiv(100 * SBull, (Sum if (Sum > 0) else DBL_MIN))
        BufferBears[i] = _fdiv(100 * SBear, (Sum if (Sum > 0) else DBL_MIN))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendPercentage(_MQL5Indicator):
    name = 'Trend_Percentage'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

