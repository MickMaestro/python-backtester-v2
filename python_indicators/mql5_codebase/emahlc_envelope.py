"""EMAHLC_Envelope — converted from MQL5: MQL5 Indicators/EMAHLC_Envelope/EMAHLC_Envelope.mq5

EMA HLC Envelope indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 5}, 'types': {1: 5, 2: 5, 3: 1, 4: 1, 5: 1}, 'colors': {1: [16748574], 2: [36095], 3: [65280], 4: [11119017], 5: [255]}, 'widths': {1: 2, 2: 2, 3: 1, 4: 1, 5: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'High broken', 2: 'Low broken', 3: 'EMA High Env', 4: 'EMA Close Env', 5: 'EMA Low Env'}, 'levels': [], 'description': ['EMA HLC Envelope indicator'], 'name': 'EMAHLC_Envelope', 'source': 'MQL5 Indicators/EMAHLC_Envelope/EMAHLC_Envelope.mq5', 'folder': 'EMAHLC_Envelope', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
BufferArrowTop = Arr(0, 0.0)
BufferArrowBottom = Arr(0, 0.0)
BufferMAH = Arr(0, 0.0)
BufferMAC = Arr(0, 0.0)
BufferMAL = Arr(0, 0.0)
period = 0
handle_mah = 0
handle_mal = 0
handle_mac = 0

def OnInit():
    global handle_mac, handle_mah, handle_mal, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferArrowTop, INDICATOR_DATA)
    SetIndexBuffer(1, BufferArrowBottom, INDICATOR_DATA)
    SetIndexBuffer(2, BufferMAH, INDICATOR_DATA)
    SetIndexBuffer(3, BufferMAC, INDICATOR_DATA)
    SetIndexBuffer(4, BufferMAL, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 158)
    PlotIndexSetInteger(1, PLOT_ARROW, 158)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EMA HLC Envelope (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferArrowTop, True)
    ArraySetAsSeries(BufferArrowBottom, True)
    ArraySetAsSeries(BufferMAH, True)
    ArraySetAsSeries(BufferMAC, True)
    ArraySetAsSeries(BufferMAL, True)
    ResetLastError()
    handle_mah = iMA(None, PERIOD_CURRENT, period, 0, MODE_EMA, PRICE_HIGH)
    if handle_mah == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') by PRICE_HIGH object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_mac = iMA(None, PERIOD_CURRENT, period, 0, MODE_EMA, PRICE_CLOSE)
    if handle_mac == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') by PRICE_CLOSE object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_mal = iMA(None, PERIOD_CURRENT, period, 0, MODE_EMA, PRICE_LOW)
    if handle_mal == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') by PRICE_LOW object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferArrowTop, EMPTY_VALUE)
        ArrayInitialize(BufferArrowBottom, EMPTY_VALUE)
        ArrayInitialize(BufferMAH, EMPTY_VALUE)
        ArrayInitialize(BufferMAC, EMPTY_VALUE)
        ArrayInitialize(BufferMAL, EMPTY_VALUE)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_mah, 0, 0, count, BufferMAH)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_mac, 0, 0, count, BufferMAC)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_mal, 0, 0, count, BufferMAL)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferArrowBottom[i] = EMPTY_VALUE
        BufferArrowTop[i] = BufferArrowBottom[i]
        if high[i] > BufferMAH[i]:
            BufferArrowTop[i] = high[i]
        if low[i] < BufferMAL[i]:
            BufferArrowBottom[i] = low[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EMAHLCEnvelope(_MQL5Indicator):
    name = 'EMAHLC_Envelope'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
    }

