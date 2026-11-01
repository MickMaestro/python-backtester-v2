"""DPO_Bar — converted from MQL5: MQL5 Indicators/DPO_Bar/DPO_Bar.mq5

Detrended Price Oscillator Bar
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [7451452, 42495, 8421504]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Open;High;Low;Close'}, 'levels': [], 'description': ['Detrended Price Oscillator Bar'], 'name': 'DPO_Bar', 'source': 'MQL5 Indicators/DPO_Bar/DPO_Bar.mq5', 'folder': 'DPO_Bar', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
BufferOpen = Arr(0, 0.0)
BufferHigh = Arr(0, 0.0)
BufferLow = Arr(0, 0.0)
BufferClose = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferOpenMA = Arr(0, 0.0)
BufferHighMA = Arr(0, 0.0)
BufferLowMA = Arr(0, 0.0)
BufferCloseMA = Arr(0, 0.0)
period = 0
handle_ma_o = 0
handle_ma_h = 0
handle_ma_l = 0
handle_ma_c = 0

def OnInit():
    global handle_ma_c, handle_ma_h, handle_ma_l, handle_ma_o, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferOpen, INDICATOR_DATA)
    SetIndexBuffer(1, BufferHigh, INDICATOR_DATA)
    SetIndexBuffer(2, BufferLow, INDICATOR_DATA)
    SetIndexBuffer(3, BufferClose, INDICATOR_DATA)
    SetIndexBuffer(4, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, BufferOpenMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferHighMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferLowMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferCloseMA, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'DPO Bar(' + _str(period) + ')')
    ArraySetAsSeries(BufferOpen, True)
    ArraySetAsSeries(BufferHigh, True)
    ArraySetAsSeries(BufferLow, True)
    ArraySetAsSeries(BufferClose, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferOpenMA, True)
    ArraySetAsSeries(BufferHighMA, True)
    ArraySetAsSeries(BufferLowMA, True)
    ArraySetAsSeries(BufferCloseMA, True)
    ResetLastError()
    handle_ma_o = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, PRICE_OPEN)
    if handle_ma_o == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') by PRICE_OPEN object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_ma_h = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, PRICE_HIGH)
    if handle_ma_h == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') by PRICE_HIGH object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_ma_l = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, PRICE_LOW)
    if handle_ma_l == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') by PRICE_LOW object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_ma_c = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, PRICE_CLOSE)
    if handle_ma_c == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') by PRICE_CLOSE object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferOpen, EMPTY_VALUE)
        ArrayInitialize(BufferHigh, EMPTY_VALUE)
        ArrayInitialize(BufferLow, EMPTY_VALUE)
        ArrayInitialize(BufferClose, EMPTY_VALUE)
        ArrayInitialize(BufferOpenMA, EMPTY_VALUE)
        ArrayInitialize(BufferHighMA, EMPTY_VALUE)
        ArrayInitialize(BufferLowMA, EMPTY_VALUE)
        ArrayInitialize(BufferCloseMA, EMPTY_VALUE)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma_o, 0, 0, count, BufferOpenMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma_h, 0, 0, count, BufferHighMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma_l, 0, 0, count, BufferLowMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma_c, 0, 0, count, BufferCloseMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferOpen[i] = open[i] - BufferOpenMA[i]
        BufferHigh[i] = high[i] - BufferHighMA[i]
        BufferLow[i] = low[i] - BufferLowMA[i]
        BufferClose[i] = close[i] - BufferCloseMA[i]
        BufferColors[i] = (0 if (BufferClose[i] > BufferOpen[i]) else 1 if (BufferClose[i] < BufferOpen[i]) else 2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DPOBar(_MQL5Indicator):
    name = 'DPO_Bar'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
    }

