"""Hurst_Difference — converted from MQL5: MQL5 Indicators/Hurst_Difference/Hurst_Difference.mq5

Hurst Difference oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Hurst difference'}, 'levels': [], 'description': ['Hurst Difference oscillator'], 'name': 'Hurst_Difference', 'source': 'MQL5 Indicators/Hurst_Difference/Hurst_Difference.mq5', 'folder': 'Hurst_Difference', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 30, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 30)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferHurst = Arr(0, 0.0)
BufferPrice = Arr(0, 0.0)
BufferFDI = Arr(0, 0.0)
period = 0
handle_ma = 0

def OnInit():
    global handle_ma, period
    period = (2 if (InpPeriod < 2) else InpPeriod)
    SetIndexBuffer(0, BufferHurst, INDICATOR_DATA)
    SetIndexBuffer(1, BufferPrice, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferFDI, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Hurst Difference (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferHurst, True)
    ArraySetAsSeries(BufferPrice, True)
    ArraySetAsSeries(BufferFDI, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferHurst, EMPTY_VALUE)
        ArrayInitialize(BufferPrice, 0)
        ArrayInitialize(BufferFDI, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferPrice)
    if copied != count:
        return 0
    max_ = 0.0
    min_ = DBL_MAX
    for i in range(limit, 0 - 1, -1):
        for j in range(i + period - 1, i - 1, -1):
            if j == (i + period - 1):
                min_ = BufferPrice[j]
                max_ = min_
            else:
                if BufferPrice[j] > max_:
                    max_ = BufferPrice[j]
                if BufferPrice[j] < min_:
                    min_ = BufferPrice[j]
        priorDiff = 0.0
        length = 0.0
        for j in range(i + period - 1, i - 1, -1):
            if (max_ - min_) > 0:
                diff = _fdiv(BufferPrice[j] - min_, max_ - min_)
                if max_ > min_:
                    length += sqrt(pow(diff - priorDiff, 2) + _fdiv(1.0, pow(period, 2)))
                priorDiff = diff
        BufferFDI[i] = (_fdiv(1.0 + (log(length) + log(2)), log(2 * (period - 1))) if (length > 0) else 0)
        BufferHurst[i] = BufferFDI[i + 1] - BufferFDI[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HurstDifference(_MQL5Indicator):
    name = 'Hurst_Difference'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 30,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

