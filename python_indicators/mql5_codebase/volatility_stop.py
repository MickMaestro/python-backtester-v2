"""Volatility_Stop — converted from MQL5: MQL5 Indicators/Volatility_Stop/Volatility_Stop.mq5

Volatility Stop indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [14772545]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'VS'}, 'levels': [], 'description': ['Volatility Stop indicator'], 'name': 'Volatility_Stop', 'source': 'MQL5 Indicators/Volatility_Stop/Volatility_Stop.mq5', 'folder': 'Volatility_Stop', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpMultiplier', 'py': 'InpMultiplier', 'param': 'InpMultiplier', 'type': 'double', 'default': 2.0, 'label': 'Multiplier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
InpMultiplier = _input('InpMultiplier', 2.0)  # Multiplier
BufferVS = Arr(0, 0.0)
BufferDiff = Arr(0, 0.0)
multiplier = 0.0
period_sm = 0

def OnInit():
    global multiplier, period_sm
    multiplier = InpMultiplier
    period_sm = (2 if (InpPeriod < 2) else InpPeriod)
    SetIndexBuffer(0, BufferVS, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDiff, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volatility Stop (' + _str(period_sm) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferVS, True)
    ArraySetAsSeries(BufferDiff, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_sm, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferVS, EMPTY_VALUE)
        ArrayInitialize(BufferDiff, 0)
    for i in range(limit, 0 - 1, -1):
        BufferDiff[i] = high[i] - low[i]
        BufferVS[i] = close[i] - (multiplier * GetSMA(rates_total, i, period_sm, BufferDiff))
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


class VolatilityStop(_MQL5Indicator):
    name = 'Volatility_Stop'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'InpMultiplier': 2.0,  # Multiplier
    }

