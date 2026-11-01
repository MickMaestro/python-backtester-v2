"""CVI — converted from MQL5: MQL5 Indicators/CVI/CVI.mq5

Chartmill Value Indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'CVI'}, 'levels': [], 'description': ['Chartmill Value Indicator'], 'name': 'CVI', 'source': 'MQL5 Indicators/CVI/CVI.mq5', 'folder': 'CVI', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'MA method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 5, 'label': 'MA price', 'sinput': False}, {'mql': 'InpModifiedAlg', 'py': 'InpModifiedAlg', 'param': 'InpModifiedAlg', 'type': 'int', 'default': 1, 'label': 'Modified algorithm', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 0.5, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': -0.5, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpMethod = _input('InpMethod', MODE_SMA)  # MA method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_MEDIAN)  # MA price
InpModifiedAlg = _input('InpModifiedAlg', INPUT_YES)  # Modified algorithm
InpOverbought = _input('InpOverbought', 0.5)  # Overbought
InpOversold = _input('InpOversold', -0.5)  # Oversold
BufferCVI = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period = 0
handle_ma = 0
handle_atr = 0

def OnInit():
    global handle_atr, handle_ma, overbought, oversold, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    oversold = (0 if (InpOversold > 0) else InpOversold)
    overbought = (0 if (InpOverbought < 0) else InpOverbought)
    if overbought <= oversold:
        overbought = oversold + 0.01
    if oversold >= overbought:
        oversold = overbought - 0.01
    SetIndexBuffer(0, BufferCVI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferATR, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CVI(' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    ArraySetAsSeries(BufferCVI, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferATR, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_atr = iATR(None, PERIOD_CURRENT, period)
    if handle_atr == INVALID_HANDLE:
        Print('The iATR(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period:
        return 0
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferCVI, EMPTY_VALUE)
        ArrayInitialize(BufferMA, EMPTY_VALUE)
        ArrayInitialize(BufferATR, EMPTY_VALUE)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_atr, 0, 0, count, BufferATR)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferCVI[i] = _fdiv(close[i] - BufferMA[i], (((BufferATR[i] * sqrt(period)) if InpModifiedAlg else BufferATR[i]) if (BufferATR[i] != 0) else DBL_MIN))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CVI(_MQL5Indicator):
    name = 'CVI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # MA price
        'InpModifiedAlg': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Modified algorithm
        'InpOverbought': 0.5,  # Overbought
        'InpOversold': -0.5,  # Oversold
    }

