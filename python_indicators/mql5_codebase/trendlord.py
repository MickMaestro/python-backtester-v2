"""TrendLord — converted from MQL5: MQL5 Indicators/TrendLord/TrendLord.mq5

Trend Lord indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255, 11119017]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'TrendLord'}, 'levels': [], 'description': ['Trend Lord indicator'], 'name': 'TrendLord', 'source': 'MQL5 Indicators/TrendLord/TrendLord.mq5', 'folder': 'TrendLord', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 50, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 50)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferTL = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period_ma = 0
period_sqrt = 0
handle_ma = 0
weight_sum = 0

def OnInit():
    global handle_ma, period_ma, period_sqrt
    period_ma = (1 if (InpPeriod < 1) else InpPeriod)
    period_sqrt = _int(sqrt(period_ma))
    if period_sqrt < 2:
        period_sqrt = 2
    SetIndexBuffer(0, BufferTL, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TrendLord (' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    ArraySetAsSeries(BufferTL, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period_ma, 0, MODE_LWMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_ma, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferTL, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_sqrt, BufferMA, BufferTL, _GlobRef(globals(), 'weight_sum')) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferColors[i] = (0 if (BufferTL[i] > BufferTL[i + 1]) else 1 if (BufferTL[i] < BufferTL[i + 1]) else 2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendLord(_MQL5Indicator):
    name = 'TrendLord'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 50,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

