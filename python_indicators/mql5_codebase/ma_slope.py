"""MA_Slope — converted from MQL5: MQL5 Indicators/MA_Slope/MA_Slope.mq5

Moving Average Slope indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [32768, 255, 11119017]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'MASlope'}, 'levels': [], 'description': ['Moving Average Slope indicator'], 'name': 'MA_Slope', 'source': 'MQL5 Indicators/MA_Slope/MA_Slope.mq5', 'folder': 'MA_Slope', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 50, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpSlope', 'py': 'InpSlope', 'param': 'InpSlope', 'type': 'double', 'default': 0.0, 'label': 'Slope', 'sinput': False}, {'mql': 'InpLength', 'py': 'InpLength', 'param': 'InpLength', 'type': 'uint', 'default': 1, 'label': 'Slope length', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 50)  # Period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpSlope = _input('InpSlope', 0.0)  # Slope
InpLength = _input('InpLength', 1)  # Slope length
BufferMASlope = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
slope = 0.0
period = 0
length = 0
handle_ma = 0

def OnInit():
    global handle_ma, length, period, slope
    period = (1 if (InpPeriod < 1) else InpPeriod)
    length = (1 if (InpLength < 1) else InpLength)
    slope = (0 if (InpSlope < 0) else InpSlope)
    SetIndexBuffer(0, BufferMASlope, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, MethodToString(InpMethod) + ' Slope (' + _str(period) + ',' + DoubleToString(slope, 1) + ',' + _str(length) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMASlope, True)
    ArraySetAsSeries(BufferColors, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(length, 4) or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - length - 1
        ArrayInitialize(BufferMASlope, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 2)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMASlope)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        Sl = _fdiv(BufferMASlope[i] - BufferMASlope[i + length], Point())
        BufferColors[i] = (0 if (Sl > slope) else 1 if (Sl < (-slope)) else 2)
    return rates_total

def MethodToString(method):
    return StringSubstr(EnumToString(method, 'ENUM_MA_METHOD'), 5)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MASlope(_MQL5Indicator):
    name = 'MA_Slope'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 50,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpSlope': 0.0,  # Slope
        'InpLength': 1,  # Slope length
    }

