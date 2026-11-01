"""RSI_Oscillator_Histo — converted from MQL5: MQL5 Indicators/RSI_Oscillator_Histo/RSI_Oscillator_Histo.mq5

RSI Histogram Oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [65280, 17919, 14474460]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Osc RSI'}, 'levels': [], 'description': ['RSI Histogram Oscillator'], 'name': 'RSI_Oscillator_Histo', 'source': 'MQL5 Indicators/RSI_Oscillator_Histo/RSI_Oscillator_Histo.mq5', 'folder': 'RSI_Oscillator_Histo', 'inputs': [{'mql': 'InpPeriodFastRSI', 'py': 'InpPeriodFastRSI', 'param': 'InpPeriodFastRSI', 'type': 'uint', 'default': 10, 'label': 'Fast RSI period', 'sinput': False}, {'mql': 'InpPeriodSlowRSI', 'py': 'InpPeriodSlowRSI', 'param': 'InpPeriodSlowRSI', 'type': 'uint', 'default': 25, 'label': 'Slow RSI period', 'sinput': False}, {'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 5, 'label': 'Smoothing', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodFastRSI = _input('InpPeriodFastRSI', 10)  # Fast RSI period
InpPeriodSlowRSI = _input('InpPeriodSlowRSI', 25)  # Slow RSI period
InpPeriodMA = _input('InpPeriodMA', 5)  # Smoothing
BufferOscRSI = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferFRSI = Arr(0, 0.0)
BufferSRSI = Arr(0, 0.0)
BufferRAW = Arr(0, 0.0)
period_fast = 0
period_slow = 0
period_ma = 0
handle_frsi = 0
handle_srsi = 0

def OnInit():
    global handle_frsi, handle_srsi, period_fast, period_ma, period_slow
    period_fast = (1 if (InpPeriodFastRSI < 1) else InpPeriodFastRSI)
    period_slow = ((period_fast + 1) if (InpPeriodSlowRSI == period_fast) else 1 if (InpPeriodSlowRSI < 1) else InpPeriodSlowRSI)
    period_ma = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    SetIndexBuffer(0, BufferOscRSI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferFRSI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferSRSI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferRAW, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Osc RSI (' + _str(period_fast) + ',' + _str(period_slow) + ',' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferOscRSI, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferFRSI, True)
    ArraySetAsSeries(BufferSRSI, True)
    ArraySetAsSeries(BufferRAW, True)
    ResetLastError()
    handle_frsi = iRSI(None, PERIOD_CURRENT, period_fast, PRICE_CLOSE)
    if handle_frsi == INVALID_HANDLE:
        Print(64, ': The iRSI(', _str(period_fast), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_srsi = iRSI(None, PERIOD_CURRENT, period_slow, PRICE_CLOSE)
    if handle_srsi == INVALID_HANDLE:
        Print(70, ': The iRSI(', _str(period_slow), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_ma, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferOscRSI, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferFRSI, 0)
        ArrayInitialize(BufferSRSI, 0)
        ArrayInitialize(BufferRAW, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_frsi, 0, 0, count, BufferFRSI)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_srsi, 0, 0, count, BufferSRSI)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferRAW[i] = BufferFRSI[i] - BufferSRSI[i]
        BufferOscRSI[i] = GetSMA(rates_total, i, period_ma, BufferRAW)
        BufferColors[i] = (0 if (BufferOscRSI[i] > BufferOscRSI[i + 1]) else 1 if (BufferOscRSI[i] < BufferOscRSI[i + 1]) else 2)
    return rates_total

def GetSMA(rates_total, index, period, price, as_series=True):
    result = 0.0
    check_index = ((index <= (rates_total - period - 1)) if as_series else (index >= (period - 1)))
    if period < 1 or (not check_index):
        return 0.0
    for i in range(0, period):
        result = result + (price[index + i] if as_series else price[index - i])
    return _fdiv(result, period)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSIOscillatorHisto(_MQL5Indicator):
    name = 'RSI_Oscillator_Histo'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFastRSI': 10,  # Fast RSI period
        'InpPeriodSlowRSI': 25,  # Slow RSI period
        'InpPeriodMA': 5,  # Smoothing
    }

