"""Average_Change — converted from MQL5: MQL5 Indicators/Average_Change/Average_Change.mq5

Average change price indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'AC', 2: 'Average change'}, 'levels': [], 'description': ['Average change price indicator'], 'name': 'Average_Change', 'source': 'MQL5 Indicators/Average_Change/Average_Change.mq5', 'folder': 'Average_Change', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferAC = Arr(0, 0.0)
BufferAVG = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period_ma = 0
weight_sum = 0
handle_ma = 0

def OnInit():
    global handle_ma, period_ma
    period_ma = (2 if (InpPeriod < 2) else InpPeriod)
    SetIndexBuffer(0, BufferAC, INDICATOR_DATA)
    SetIndexBuffer(1, BufferAVG, INDICATOR_DATA)
    SetIndexBuffer(2, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Average change (' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferAC, True)
    ArraySetAsSeries(BufferAVG, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_ma, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferAC, 0)
        ArrayInitialize(BufferAVG, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferAC[i] = BufferMA[i] - BufferMA[i + 1]
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        return ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_ma, BufferAC, BufferAVG)
    elif _sw1 == MODE_SMMA:
        return SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_ma, BufferAC, BufferAVG)
    elif _sw1 == MODE_LWMA:
        return LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_ma, BufferAC, BufferAVG, _GlobRef(globals(), 'weight_sum'))
    else:
        return SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ma, BufferAC, BufferAVG)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AverageChange(_MQL5Indicator):
    name = 'Average_Change'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

