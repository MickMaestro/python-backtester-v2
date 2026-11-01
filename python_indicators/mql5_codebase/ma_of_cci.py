"""MA_Of_CCI — converted from MQL5: MQL5 Indicators/MA_Of_CCI/MA_Of_CCI.mq5

MA of CCI oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711680], 2: [2237106]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'CCI', 2: 'MA'}, 'levels': [], 'description': ['MA of CCI oscillator'], 'name': 'MA_Of_CCI', 'source': 'MQL5 Indicators/MA_Of_CCI/MA_Of_CCI.mq5', 'folder': 'MA_Of_CCI', 'inputs': [{'mql': 'InpPeriodCCI', 'py': 'InpPeriodCCI', 'param': 'InpPeriodCCI', 'type': 'uint', 'default': 14, 'label': 'CCI period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'CCI applied price', 'sinput': False}, {'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 20, 'label': 'MA period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'MA method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodCCI = _input('InpPeriodCCI', 14)  # CCI period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # CCI applied price
InpPeriodMA = _input('InpPeriodMA', 20)  # MA period
InpMethod = _input('InpMethod', MODE_SMA)  # MA method
BufferCCI = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period_cci = 0
period_ma = 0
period_max = 0
handle_cci = 0
weight_sum = 0

def OnInit():
    global handle_cci, period_cci, period_ma, period_max
    period_cci = (1 if (InpPeriodCCI < 1) else InpPeriodCCI)
    period_ma = (2 if (InpPeriodMA < 2) else InpPeriodMA)
    period_max = fmax(period_cci, period_ma)
    SetIndexBuffer(0, BufferCCI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MA of CCI (' + _str(period_cci) + ',' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferCCI, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_cci = iCCI(None, PERIOD_CURRENT, period_cci, InpAppliedPrice)
    if handle_cci == INVALID_HANDLE:
        Print('The iCCI(', _str(period_cci), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferCCI, EMPTY_VALUE)
        ArrayInitialize(BufferMA, EMPTY_VALUE)
    count = (rates_total if (limit > 1) else 1)
    ResetLastError()
    copied = CopyBuffer(handle_cci, 0, 0, count, BufferCCI)
    if copied != count:
        return 0
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        return ExponentialMAOnBuffer(rates_total, prev_calculated, period_cci, period_ma, BufferCCI, BufferMA)
    elif _sw1 == MODE_SMMA:
        return SmoothedMAOnBuffer(rates_total, prev_calculated, period_cci, period_ma, BufferCCI, BufferMA)
    elif _sw1 == MODE_LWMA:
        return LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_cci, period_ma, BufferCCI, BufferMA, _GlobRef(globals(), 'weight_sum'))
    else:
        return SimpleMAOnBuffer(rates_total, prev_calculated, period_cci, period_ma, BufferCCI, BufferMA)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MAOfCCI(_MQL5Indicator):
    name = 'MA_Of_CCI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodCCI': 14,  # CCI period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # CCI applied price
        'InpPeriodMA': 20,  # MA period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA method
    }

