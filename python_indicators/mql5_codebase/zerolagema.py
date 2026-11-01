"""ZeroLagEMA — converted from MQL5: MQL5 Indicators/ZeroLagEMA/ZeroLagEMA.mq5

Zero-Lag Exponential Moving Average
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'EMAZL'}, 'levels': [], 'description': ['Zero-Lag Exponential Moving Average'], 'name': 'ZeroLagEMA', 'source': 'MQL5 Indicators/ZeroLagEMA/ZeroLagEMA.mq5', 'folder': 'ZeroLagEMA', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferEMAZL = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
alpha = 0.0
period = 0
lag = 0
handle_ma = 0

def OnInit():
    global alpha, handle_ma, lag, period
    period = (2 if (InpPeriod < 2) else InpPeriod)
    alpha = _fdiv(2.0, period + 1.0)
    lag = _int(ceil((period - 1.0) / 2.0))
    SetIndexBuffer(0, BufferEMAZL, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Zero-Lag EMA (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, (period * 3) + lag)
    ArraySetAsSeries(BufferEMAZL, True)
    ArraySetAsSeries(BufferMA, True)
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
        limit = rates_total - lag - 2
        ArrayInitialize(BufferEMAZL, 0)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferEMAZL[i] = (alpha * ((2.0 * BufferMA[i]) - BufferMA[i + lag])) + ((1.0 - alpha) * BufferEMAZL[i + 1])
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ZeroLagEMA(_MQL5Indicator):
    name = 'ZeroLagEMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

