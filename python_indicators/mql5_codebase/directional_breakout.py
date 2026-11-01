"""Directional_Breakout — converted from MQL5: MQL5 Indicators/Directional_Breakout/Directional_Breakout.mq5

Directional Breakout indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 10, 2: 10}, 'colors': {1: [32768, 42495, 12632256], 2: [255, 55295, 12632256]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'UP', 2: 'DN'}, 'levels': [], 'description': ['Directional Breakout indicator'], 'name': 'Directional_Breakout', 'source': 'MQL5 Indicators/Directional_Breakout/Directional_Breakout.mq5', 'folder': 'Directional_Breakout', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'MA Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'MA Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # MA Period
InpMethod = _input('InpMethod', MODE_SMA)  # MA Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferUP = Arr(0, 0.0)
BufferColorsUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferColorsDN = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period = 0
handle_ma = 0

def OnInit():
    global handle_ma, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColorsUP, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(3, BufferColorsDN, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, BufferMA, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Directional Breakout (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferColorsUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferColorsDN, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period, 0, InpMethod, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        MA = BufferMA[i]
        BufferUP[i] = EMPTY_VALUE
        BufferDN[i] = EMPTY_VALUE
        BufferColorsDN[i] = 2.0
        BufferColorsUP[i] = BufferColorsDN[i]
        BufferUP[i] = BufferMA[i]
        if low[i] > MA:
            BufferUP[i] = 2.0
            BufferColorsUP[i] = 0.0
            BufferDN[i] = 0.0
        else:
            if high[i] < MA:
                BufferDN[i] = -2.0
                BufferColorsDN[i] = 0.0
                BufferUP[i] = 0.0
            else:
                BufferUP[i] = 1.0
                BufferDN[i] = -1.0
                BufferColorsUP[i] = 1.0
                BufferColorsDN[i] = 1.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DirectionalBreakout(_MQL5Indicator):
    name = 'Directional_Breakout'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # MA Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

