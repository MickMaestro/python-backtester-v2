"""EMAHLC_Envelope_Oscillator — converted from MQL5: MQL5 Indicators/EMAHLC_Envelope_Oscillator/EMAHLC_Envelope_Oscillator.mq5

EMA HLC Envelope Oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16760576, 42495, 11119017]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'EMA HLC Env Osc'}, 'levels': [], 'description': ['EMA HLC Envelope Oscillator'], 'name': 'EMAHLC_Envelope_Oscillator', 'source': 'MQL5 Indicators/EMAHLC_Envelope_Oscillator/EMAHLC_Envelope_Oscillator.mq5', 'folder': 'EMAHLC_Envelope_Oscillator', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
BufferHistHL = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferMAH = Arr(0, 0.0)
BufferMAL = Arr(0, 0.0)
period = 0
handle_mah = 0
handle_mal = 0

def OnInit():
    global handle_mah, handle_mal, period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferHistHL, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferMAH, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMAL, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EMA HLC Envelope Osc(' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(BufferHistHL, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferMAH, True)
    ArraySetAsSeries(BufferMAL, True)
    ResetLastError()
    handle_mah = iMA(None, PERIOD_CURRENT, period, 0, MODE_EMA, PRICE_HIGH)
    if handle_mah == INVALID_HANDLE:
        Print('The iMA(', _str(period), ') by PRICE_HIGH object was not created: Error ', GetLastError())
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
        ArrayInitialize(BufferHistHL, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferMAH, 0)
        ArrayInitialize(BufferMAL, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_mah, 0, 0, count, BufferMAH)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_mal, 0, 0, count, BufferMAL)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferColors[i] = 2.0
        BufferHistHL[i] = 0.0
        if high[i] > 0 and high[i] > BufferMAH[i]:
            BufferHistHL[i] = high[i] - BufferMAH[i]
            BufferColors[i] = 0.0
        if low[i] > 0 and low[i] < BufferMAL[i]:
            BufferHistHL[i] = low[i] - BufferMAL[i]
            BufferColors[i] = 1.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EMAHLCEnvelopeOscillator(_MQL5Indicator):
    name = 'EMAHLC_Envelope_Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
    }

