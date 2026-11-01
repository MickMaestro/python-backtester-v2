"""Pain — converted from MQL5: MQL5 Indicators/PAIN/Pain.mq5

Pain oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [11186720]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Pain'}, 'levels': [], 'description': ['Pain oscillator'], 'name': 'Pain', 'source': 'MQL5 Indicators/PAIN/Pain.mq5', 'folder': 'PAIN', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
BufferPain = Arr(0, 0.0)
BufferMAOpen = Arr(0, 0.0)
BufferMAHigh = Arr(0, 0.0)
BufferMALow = Arr(0, 0.0)
BufferMAClose = Arr(0, 0.0)
period = 0
handle_mao = 0
handle_mah = 0
handle_mal = 0
handle_mac = 0

def OnInit():
    global handle_mac, handle_mah, handle_mal, handle_mao, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferPain, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMAOpen, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferMAHigh, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMALow, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMAClose, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Pain (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferPain, True)
    ArraySetAsSeries(BufferMAOpen, True)
    ArraySetAsSeries(BufferMAHigh, True)
    ArraySetAsSeries(BufferMALow, True)
    ArraySetAsSeries(BufferMAClose, True)
    ResetLastError()
    handle_mao = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, PRICE_OPEN)
    if handle_mao == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') by PRICE_OPEN object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_mah = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, PRICE_HIGH)
    if handle_mah == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') by PRICE_HIGH object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_mal = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, PRICE_LOW)
    if handle_mal == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') by PRICE_LOW object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_mac = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, PRICE_CLOSE)
    if handle_mac == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') by PRICE_CLOSE object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferPain, EMPTY_VALUE)
        ArrayInitialize(BufferMAOpen, 0)
        ArrayInitialize(BufferMAHigh, 0)
        ArrayInitialize(BufferMALow, 0)
        ArrayInitialize(BufferMAClose, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_mao, 0, 0, count, BufferMAOpen)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_mah, 0, 0, count, BufferMAHigh)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_mal, 0, 0, count, BufferMALow)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_mac, 0, 0, count, BufferMAClose)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferPain[i] = ((3.0 * BufferMAClose[i]) - BufferMAOpen[i] - BufferMAHigh[i] - BufferMALow[i]) / 2.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Pain(_MQL5Indicator):
    name = 'Pain'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
    }

