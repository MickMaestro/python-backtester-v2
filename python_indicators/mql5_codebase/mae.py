"""MAE — converted from MQL5: MQL5 Indicators/MAE/MAE.mq5

Moving Average Envelopes Percentage (MAE%)
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [7451452]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'MAE'}, 'levels': [], 'description': ['Moving Average Envelopes Percentage (MAE%)'], 'name': 'MAE', 'source': 'MQL5 Indicators/MAE/MAE.mq5', 'folder': 'MAE', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpOffset', 'py': 'InpOffset', 'param': 'InpOffset', 'type': 'double', 'default': 0.5, 'label': 'Deviation', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 100.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 0.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
InpOffset = _input('InpOffset', 0.5)  # Deviation
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpOverbought = _input('InpOverbought', 100.0)  # Overbought
InpOversold = _input('InpOversold', 0.0)  # Oversold
BufferMAE = Arr(0, 0.0)
BufferMAP = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
deviation = 0.0
period = 0
handle_ma1 = 0
handle_maP = 0

def OnInit():
    global deviation, handle_ma1, handle_maP, overbought, oversold, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    deviation = (0.01 if (InpOffset == 0) else InpOffset)
    overbought = (50.01 if (InpOverbought < 50.01) else InpOverbought)
    oversold = (49.99 if (InpOversold > 49.99) else InpOversold)
    SetIndexBuffer(0, BufferMAE, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMAP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferMA1, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MAE% (' + _str(period) + ',' + DoubleToString(deviation, 2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 2, 'Oversold')
    ArraySetAsSeries(BufferMAE, True)
    ArraySetAsSeries(BufferMAP, True)
    ArraySetAsSeries(BufferMA1, True)
    ResetLastError()
    handle_maP = iMA(None, PERIOD_CURRENT, period, 0, MODE_SMA, InpAppliedPrice)
    if handle_maP == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma1 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferMAE, EMPTY_VALUE)
        ArrayInitialize(BufferMAP, 0)
        ArrayInitialize(BufferMA1, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_maP, 0, 0, count, BufferMAP)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        up = BufferMAP[i] * (1.0 + (deviation / 100.0))
        dn = BufferMAP[i] * (1.0 - (deviation / 100.0))
        BufferMAE[i] = (_fdiv(100.0 * (BufferMA1[i] - dn), up - dn) if (up != dn) else 50.0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MAE(_MQL5Indicator):
    name = 'MAE'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # Period
        'InpOffset': 0.5,  # Deviation
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpOverbought': 100.0,  # Overbought
        'InpOversold': 0.0,  # Oversold
    }

