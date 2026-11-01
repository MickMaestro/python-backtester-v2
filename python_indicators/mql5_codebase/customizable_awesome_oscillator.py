"""Customizable_Awesome_Oscillator — converted from MQL5: MQL5 Indicators/Customizable_Awesome_Oscillator/Customizable_Awesome_Oscillator.mq5

Customizable BW Awesome Oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [3329330, 255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'CAO'}, 'levels': [], 'description': ['Customizable BW Awesome Oscillator'], 'name': 'Customizable_Awesome_Oscillator', 'source': 'MQL5 Indicators/Customizable_Awesome_Oscillator/Customizable_Awesome_Oscillator.mq5', 'folder': 'Customizable_Awesome_Oscillator', 'inputs': [{'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 5, 'label': 'MA Fast period', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 35, 'label': 'MA Slow period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodFast = _input('InpPeriodFast', 5)  # MA Fast period
InpPeriodSlow = _input('InpPeriodSlow', 35)  # MA Slow period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferAO = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferMAF = Arr(0, 0.0)
BufferMAS = Arr(0, 0.0)
period_fast = 0
period_slow = 0
handle_maf = 0
handle_mas = 0

def OnInit():
    global handle_maf, handle_mas, period_fast, period_slow
    period_fast = (1 if (InpPeriodFast < 1) else InpPeriodFast)
    period_slow = (1 if (InpPeriodSlow < 1) else InpPeriodSlow)
    SetIndexBuffer(0, BufferAO, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferMAF, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMAS, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CAO(' + _str(period_fast) + ',' + _str(period_slow) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferAO, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferMAF, True)
    ArraySetAsSeries(BufferMAS, True)
    ResetLastError()
    handle_maf = iMA(None, PERIOD_CURRENT, period_fast, 0, InpMethod, InpAppliedPrice)
    if handle_maf == INVALID_HANDLE:
        Print('The Fast iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_mas = iMA(None, PERIOD_CURRENT, period_slow, 0, InpMethod, InpAppliedPrice)
    if handle_mas == INVALID_HANDLE:
        Print('The Slow iMA(1) by PRICE_LOW object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 2:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferAO, EMPTY_VALUE)
        ArrayInitialize(BufferMAF, 0)
        ArrayInitialize(BufferMAS, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_maf, 0, 0, count, BufferMAF)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_mas, 0, 0, count, BufferMAS)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferAO[i] = BufferMAF[i] - BufferMAS[i]
        BufferColors[i] = (0 if (BufferAO[i] > BufferAO[i + 1]) else 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CustomizableAwesomeOscillator(_MQL5Indicator):
    name = 'Customizable_Awesome_Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFast': 5,  # MA Fast period
        'InpPeriodSlow': 35,  # MA Slow period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

