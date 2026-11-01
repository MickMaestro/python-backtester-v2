"""KAMA — converted from MQL5: MQL5 Indicators/KAMA/KAMA.mq5

Kaufman Moving Average
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [2237106]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'KAMA'}, 'levels': [], 'description': ['Kaufman Moving Average'], 'name': 'KAMA', 'source': 'MQL5 Indicators/KAMA/KAMA.mq5', 'folder': 'KAMA', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferKAMA = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferABS = Arr(0, 0.0)
BufferMAA = Arr(0, 0.0)
period_kama = 0
handle_ma = 0

def OnInit():
    global handle_ma, period_kama
    period_kama = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferKAMA, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferABS, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMAA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'KAMA(' + _str(period_kama) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferKAMA, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferABS, True)
    ArraySetAsSeries(BufferMAA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_kama:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_kama - 2
        ArrayInitialize(BufferKAMA, 0)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferABS, 0)
        ArrayInitialize(BufferMAA, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferABS[i] = fabs(BufferMA[i] - BufferMA[i + 1])
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_kama, BufferABS, BufferMAA)
    for i in range(limit, 0 - 1, -1):
        er = BufferMAA[i] * period_kama
        if er != 0:
            er = _fdiv(fabs(BufferMA[i] - BufferMA[i + period_kama - 1]), er)
        sc = (er * 0.6015) + 0.0645
        sc *= sc
        BufferKAMA[i] = BufferKAMA[i + 1] + (sc * (BufferMA[i] - BufferKAMA[i + 1]))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KAMA(_MQL5Indicator):
    name = 'KAMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

