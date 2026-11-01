"""EWO — converted from MQL5: MQL5 Indicators/EWO/EWO.mq5

Elliot Wave Oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [9498256, 32768, 42495, 2237106, 11119017]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'EWO'}, 'levels': [], 'description': ['Elliot Wave Oscillator'], 'name': 'EWO', 'source': 'MQL5 Indicators/EWO/EWO.mq5', 'folder': 'EWO', 'inputs': [{'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 5, 'label': 'Fast MA period', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 35, 'label': 'Slow MA period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodFast = _input('InpPeriodFast', 5)  # Fast MA period
InpPeriodSlow = _input('InpPeriodSlow', 35)  # Slow MA period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferEWO = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferFMA = Arr(0, 0.0)
BufferSMA = Arr(0, 0.0)
period_fast = 0
period_slow = 0
handle_fma = 0
handle_sma = 0

def OnInit():
    global handle_fma, handle_sma, period_fast, period_slow
    period_fast = (1 if (InpPeriodFast < 1) else InpPeriodFast)
    period_slow = ((period_fast + 1) if (InpPeriodSlow == period_fast) else 1 if (InpPeriodSlow < 1) else InpPeriodSlow)
    SetIndexBuffer(0, BufferEWO, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferFMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferSMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EWOsc (' + _str(period_fast) + ',' + _str(period_slow) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferEWO, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferFMA, True)
    ArraySetAsSeries(BufferSMA, True)
    ResetLastError()
    handle_fma = iMA(None, PERIOD_CURRENT, period_fast, 0, InpMethod, InpAppliedPrice)
    if handle_fma == INVALID_HANDLE:
        Print('The iMA(', _str(period_fast), ') by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sma = iMA(None, PERIOD_CURRENT, period_slow, 0, InpMethod, InpAppliedPrice)
    if handle_sma == INVALID_HANDLE:
        Print('The iMA(', _str(period_slow), ') by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferEWO, 0)
        ArrayInitialize(BufferColors, 4)
        ArrayInitialize(BufferFMA, 0)
        ArrayInitialize(BufferSMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_fma, 0, 0, count, BufferFMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sma, 0, 0, count, BufferSMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferEWO[i] = BufferFMA[i] - BufferSMA[i]
        BufferColors[i] = ((0 if (BufferEWO[i] > BufferEWO[i + 1]) else 1) if (BufferEWO[i] > 0) else (2 if (BufferEWO[i] < BufferEWO[i + 1]) else 3) if (BufferEWO[i] < 0) else 4)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EWO(_MQL5Indicator):
    name = 'EWO'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFast': 5,  # Fast MA period
        'InpPeriodSlow': 35,  # Slow MA period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

