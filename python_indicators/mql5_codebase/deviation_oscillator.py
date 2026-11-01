"""Deviation_Oscillator — converted from MQL5: MQL5 Indicators/Deviation_Oscillator/Deviation_Oscillator.mq5

Deviation oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [8421376]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'OscDev'}, 'levels': [], 'description': ['Deviation oscillator'], 'name': 'Deviation_Oscillator', 'source': 'MQL5 Indicators/Deviation_Oscillator/Deviation_Oscillator.mq5', 'folder': 'Deviation_Oscillator', 'inputs': [{'mql': 'InpPeriod1', 'py': 'InpPeriod1', 'param': 'InpPeriod1', 'type': 'uint', 'default': 40, 'label': 'MA period', 'sinput': False}, {'mql': 'InpPeriod2', 'py': 'InpPeriod2', 'param': 'InpPeriod2', 'type': 'uint', 'default': 80, 'label': 'Min/Max period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod1 = _input('InpPeriod1', 40)  # MA period
InpPeriod2 = _input('InpPeriod2', 80)  # Min/Max period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferDO = Arr(0, 0.0)
BufferRAW = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMAP = Arr(0, 0.0)
period1 = 0
period2 = 0
handle_ma1 = 0
handle_maP = 0

def OnInit():
    global handle_ma1, handle_maP, period1, period2
    period1 = (1 if (InpPeriod1 < 1) else InpPeriod1)
    period2 = (1 if (InpPeriod2 < 1) else InpPeriod2)
    SetIndexBuffer(0, BufferDO, INDICATOR_DATA)
    SetIndexBuffer(1, BufferRAW, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMAP, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Deviation oscillator (' + _str(period1) + ',' + _str(period2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferDO, True)
    ArraySetAsSeries(BufferRAW, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMAP, True)
    ResetLastError()
    handle_ma1 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(1) by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_maP = iMA(None, PERIOD_CURRENT, period1, 0, InpMethod, InpAppliedPrice)
    if handle_maP == INVALID_HANDLE:
        Print('The iMA(', _str(period1), ') by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period2, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period2 - 1
        ArrayInitialize(BufferDO, EMPTY_VALUE)
        ArrayInitialize(BufferRAW, 0)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferMAP, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_maP, 0, 0, count, BufferMAP)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferRAW[i] = BufferMA1[i] - BufferMAP[i]
        bl = ArrayMinimum(BufferRAW, i, period2)
        bh = ArrayMaximum(BufferRAW, i, period2)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        min_ = BufferRAW[bl]
        max_ = BufferRAW[bh]
        BufferDO[i] = (((_fdiv(200.0, max_ - min_) * (BufferRAW[i] - min_)) - 100.0) if (min_ != max_) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DeviationOscillator(_MQL5Indicator):
    name = 'Deviation_Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod1': 40,  # MA period
        'InpPeriod2': 80,  # Min/Max period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

