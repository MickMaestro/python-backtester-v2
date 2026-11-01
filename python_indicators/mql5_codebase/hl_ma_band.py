"""HL_MA_Band — converted from MQL5: MQL5 Indicators/HL_MA_Band/HL_MA_Band.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 11, 2: 1, 3: 1}, 'colors': {1: [3329434, 16711935, 32768, 7504122], 2: [255], 3: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 2, 2: 0, 3: 0}, 'labels': {1: 'Band upper;Band lower', 2: 'MA High', 3: 'MA Low'}, 'levels': [], 'description': [], 'name': 'HL_MA_Band', 'source': 'MQL5 Indicators/HL_MA_Band/HL_MA_Band.mq5', 'folder': 'HL_MA_Band', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'MA period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 1, 'label': 'MA method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # MA period
InpMethod = _input('InpMethod', MODE_EMA)  # MA method
BufferHIST1 = Arr(0, 0.0)
BufferHIST2 = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferH = Arr(0, 0.0)
BufferL = Arr(0, 0.0)
period_ma = 0
handle_mah = 0
handle_mal = 0

def OnInit():
    global handle_mah, handle_mal, period_ma
    period_ma = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferHIST1, INDICATOR_DATA)
    SetIndexBuffer(1, BufferHIST2, INDICATOR_DATA)
    SetIndexBuffer(2, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(3, BufferH, INDICATOR_DATA)
    SetIndexBuffer(4, BufferL, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 119)
    PlotIndexSetInteger(1, PLOT_ARROW, 119)
    IndicatorSetString(INDICATOR_SHORTNAME, 'High/Low MA band(' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(BufferHIST1, True)
    ArraySetAsSeries(BufferHIST2, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferH, True)
    ArraySetAsSeries(BufferL, True)
    ResetLastError()
    handle_mah = iMA(None, PERIOD_CURRENT, period_ma, 0, InpMethod, PRICE_HIGH)
    if handle_mah == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') by PRICE_HIGH object was not created: Error ', GetLastError())
        return INIT_FAILED
    ResetLastError()
    handle_mal = iMA(None, PERIOD_CURRENT, period_ma, 0, InpMethod, PRICE_LOW)
    if handle_mal == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') by PRICE_LOW object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_ma:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferHIST1, EMPTY_VALUE)
        ArrayInitialize(BufferHIST2, EMPTY_VALUE)
        ArrayInitialize(BufferColors, EMPTY_VALUE)
        ArrayInitialize(BufferH, EMPTY_VALUE)
        ArrayInitialize(BufferL, EMPTY_VALUE)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_mah, 0, 0, count, BufferH)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_mal, 0, 0, count, BufferL)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferHIST1[i] = BufferH[i]
        BufferHIST2[i] = BufferL[i]
        if BufferH[i] > BufferH[i + 1]:
            if BufferL[i] > BufferL[i + 1]:
                BufferColors[i] = 0.0
            else:
                BufferColors[i] = 3.0
        else:
            if BufferL[i] > BufferL[i + 1]:
                BufferColors[i] = 2.0
            else:
                BufferColors[i] = 1.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HLMABand(_MQL5Indicator):
    name = 'HL_MA_Band'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # MA period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # MA method
    }

