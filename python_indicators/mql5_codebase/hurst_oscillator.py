"""Hurst_Oscillator — converted from MQL5: MQL5 Indicators/Hurst_Oscillator/Hurst_Oscillator.mq5

Hurst oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [2263842]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Hurst Osc'}, 'levels': [], 'description': ['Hurst oscillator'], 'name': 'Hurst_Oscillator', 'source': 'MQL5 Indicators/Hurst_Oscillator/Hurst_Oscillator.mq5', 'folder': 'Hurst_Oscillator', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpPeriodSM', 'py': 'InpPeriodSM', 'param': 'InpPeriodSM', 'type': 'uint', 'default': 1, 'label': 'Smoothing', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
InpPeriodSM = _input('InpPeriodSM', 1)  # Smoothing
BufferHO = Arr(0, 0.0)
BufferFlowValue = Arr(0, 0.0)
BufferCMA = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period_ma = 0
period_sm = 0
displacement = 0
handle_ma = 0

def OnInit():
    global displacement, handle_ma, period_ma, period_sm
    period_ma = (1 if (InpPeriod < 1) else InpPeriod)
    period_sm = (1 if (InpPeriodSM < 1) else InpPeriodSM)
    displacement = _int((period_ma / 2.0) + 1.0)
    SetIndexBuffer(0, BufferHO, INDICATOR_DATA)
    SetIndexBuffer(1, BufferFlowValue, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferCMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Hurst oscillator (' + _str(period_ma) + ',' + _str(period_sm) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferHO, True)
    ArraySetAsSeries(BufferFlowValue, True)
    ArraySetAsSeries(BufferCMA, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period_ma, 0, MODE_SMA, PRICE_MEDIAN)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(displacement + period_ma, 4) or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - displacement - period_ma - 2
        ArrayInitialize(BufferHO, EMPTY_VALUE)
        ArrayInitialize(BufferFlowValue, 0)
        ArrayInitialize(BufferCMA, 0)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferCMA[i] = BufferMA[i + displacement]
        BufferFlowValue[i] = (high[i] if (close[i] > close[i + 1]) else low[i] if (close[i] < close[i + 1]) else ((high[i] + low[i]) / 2.0))
        MA = GetSMA(rates_total, i, period_sm, BufferFlowValue)
        BufferHO[i] = _fdiv(MA - BufferCMA[i], Point())
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


class HurstOscillator(_MQL5Indicator):
    name = 'Hurst_Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # Period
        'InpPeriodSM': 1,  # Smoothing
    }

