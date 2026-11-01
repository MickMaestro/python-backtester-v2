"""TriMAgen — converted from MQL5: MQL5 Indicators/TriMAgen/TriMAgen.mq5

Triangular Moving Average generalized by J.Ehlers
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [2330219]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'TriMAgen'}, 'levels': [], 'description': ['Triangular Moving Average generalized by J.Ehlers'], 'name': 'TriMAgen', 'source': 'MQL5 Indicators/TriMAgen/TriMAgen.mq5', 'folder': 'TriMAgen', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferTriMAgen = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period = 0
handle_ma = 0
len1 = 0
len2 = 0

def OnInit():
    global handle_ma, len1, len2, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    len1 = _int(floor((period + 1.0) / 2))
    len2 = _int(ceil((period + 1.0) / 2))
    SetIndexBuffer(0, BufferTriMAgen, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TriMAgen(' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferTriMAgen, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, len1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(len1), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(len2, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - len2 - 1
        ArrayInitialize(BufferTriMAgen, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        sum_ = 0.0
        for j in range(0, len2):
            sum_ += BufferMA[i + j]
        BufferTriMAgen[i] = _fdiv(sum_, len2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TriMAgen(_MQL5Indicator):
    name = 'TriMAgen'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

