"""MA_Lag_Reduce — converted from MQL5: MQL5 Indicators/MA_Lag_Reduce/MA_Lag_Reduce.mq5

Moving Average with lag reduce indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [13434880]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'MA LR'}, 'levels': [], 'description': ['Moving Average with lag reduce indicator'], 'name': 'MA_Lag_Reduce', 'source': 'MQL5 Indicators/MA_Lag_Reduce/MA_Lag_Reduce.mq5', 'folder': 'MA_Lag_Reduce', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 7, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpFactorRL', 'py': 'InpFactorRL', 'param': 'InpFactorRL', 'type': 'double', 'default': 1.5, 'label': 'Lag Reduce factor', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 7)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpFactorRL = _input('InpFactorRL', 1.5)  # Lag Reduce factor
BufferMALR = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
factor = 0.0
period = 0
handle_ma = 0

def OnInit():
    global factor, handle_ma, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    factor = InpFactorRL
    SetIndexBuffer(0, BufferMALR, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MA LR (' + _str(period) + ',' + DoubleToString(factor, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMALR, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period, 4) or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferMALR, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
    bars = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, bars, BufferMA)
    if copied != bars:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferMALR[i] = ((pow(_fdiv(BufferMA[i], BufferMA[i + 1]), factor) * BufferMA[i]) if (BufferMA[i + 1] != 0) else EMPTY_VALUE)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MALagReduce(_MQL5Indicator):
    name = 'MA_Lag_Reduce'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 7,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpFactorRL': 1.5,  # Lag Reduce factor
    }

