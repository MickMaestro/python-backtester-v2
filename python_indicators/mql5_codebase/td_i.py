"""TD_I — converted from MQL5: MQL5 Indicators/TD_I/TD_I.mq5

Modified Thomas DeMark Indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [11829830]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'TDI'}, 'levels': [], 'description': ['Modified Thomas DeMark Indicator'], 'name': 'TD_I', 'source': 'MQL5 Indicators/TD_I/TD_I.mq5', 'folder': 'TD_I', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 8, 'label': 'Period', 'sinput': False}, {'mql': 'InpShift', 'py': 'InpShift', 'param': 'InpShift', 'type': 'uint', 'default': 1, 'label': 'Shift', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 70.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 30.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 8)  # Period
InpShift = _input('InpShift', 1)  # Shift
InpOverbought = _input('InpOverbought', 70.0)  # Overbought
InpOversold = _input('InpOversold', 30.0)  # Oversold
BufferTDI = Arr(0, 0.0)
BufferHighDiff = Arr(0, 0.0)
BufferLowDiff = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_ind = 0
shift = 0
period_max = 0

def OnInit():
    global overbought, oversold, period_ind, period_max, shift
    period_ind = (1 if (InpPeriod < 1) else InpPeriod)
    shift = (1 if (InpShift < 1) else InpShift)
    period_max = fmax(period_ind, shift)
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else (overbought - 0.1) if (InpOversold >= overbought) else InpOversold)
    SetIndexBuffer(0, BufferTDI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferHighDiff, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferLowDiff, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TD I(' + _str(period_ind) + ',' + _str(shift) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Oversold')
    PlotIndexSetString(0, PLOT_LABEL, 'TD I(' + _str(period_ind) + ',' + _str(shift) + ')')
    ArraySetAsSeries(BufferTDI, True)
    ArraySetAsSeries(BufferHighDiff, True)
    ArraySetAsSeries(BufferLowDiff, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 1
        ArrayInitialize(BufferTDI, EMPTY_VALUE)
        ArrayInitialize(BufferHighDiff, 0)
        ArrayInitialize(BufferLowDiff, 0)
    for i in range(limit, 0 - 1, -1):
        BufferHighDiff[i] = fmax(0, high[i] - high[i + shift])
        BufferLowDiff[i] = fmax(0, low[i + shift] - low[i])
    for i in range(limit, 0 - 1, -1):
        HighAvg = GetSMA(rates_total, i, period_ind, BufferHighDiff)
        LowAvg = GetSMA(rates_total, i, period_ind, BufferLowDiff)
        BufferTDI[i] = (_fdiv(100.0 * HighAvg, HighAvg + LowAvg) if ((HighAvg + LowAvg) != 0) else 0)
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


class TDI(_MQL5Indicator):
    name = 'TD_I'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 8,  # Period
        'InpShift': 1,  # Shift
        'InpOverbought': 70.0,  # Overbought
        'InpOversold': 30.0,  # Oversold
    }

