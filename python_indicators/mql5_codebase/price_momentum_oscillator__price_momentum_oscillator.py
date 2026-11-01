"""Price_Momentum_Oscillator — converted from MQL5: MQL5 Indicators/Price_Momentum_Oscillator/Price_Momentum_Oscillator.mq5

Price Momentum Oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'PMO', 2: 'Signal'}, 'levels': [], 'description': ['Price Momentum Oscillator'], 'name': 'Price_Momentum_Oscillator', 'source': 'MQL5 Indicators/Price_Momentum_Oscillator/Price_Momentum_Oscillator.mq5', 'folder': 'Price_Momentum_Oscillator', 'inputs': [{'mql': 'InpPeriod1', 'py': 'InpPeriod1', 'param': 'InpPeriod1', 'type': 'uint', 'default': 35, 'label': 'Period one', 'sinput': False}, {'mql': 'InpPeriod2', 'py': 'InpPeriod2', 'param': 'InpPeriod2', 'type': 'uint', 'default': 20, 'label': 'Period two', 'sinput': False}, {'mql': 'InpPeriodSm', 'py': 'InpPeriodSm', 'param': 'InpPeriodSm', 'type': 'uint', 'default': 10, 'label': 'Signal period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod1 = _input('InpPeriod1', 35)  # Period one
InpPeriod2 = _input('InpPeriod2', 20)  # Period two
InpPeriodSm = _input('InpPeriodSm', 10)  # Signal period
BufferPMO = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferRaw1 = Arr(0, 0.0)
BufferRaw2 = Arr(0, 0.0)
BufferSmoothing1 = Arr(0, 0.0)
smoothing1 = 0.0
smoothing2 = 0.0
periodS = 0
period1 = 0
period2 = 0
period_max = 0

def OnInit():
    global period1, period2, periodS, period_max, smoothing1, smoothing2
    periodS = (1 if (InpPeriodSm < 1) else InpPeriodSm)
    period1 = (1 if (InpPeriod1 < 1) else InpPeriod1)
    period2 = (1 if (InpPeriod2 < 1) else InpPeriod2)
    smoothing1 = _fdiv(2.0, period1)
    smoothing2 = _fdiv(2.0, period2)
    period_max = _int(fmax(periodS, fmax(smoothing1, smoothing2)))
    SetIndexBuffer(0, BufferPMO, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(2, BufferRaw1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferRaw2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferSmoothing1, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Price Momentum Osc (' + _str(period1) + ',' + _str(period2) + ',' + _str(periodS) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferPMO, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferRaw1, True)
    ArraySetAsSeries(BufferRaw2, True)
    ArraySetAsSeries(BufferSmoothing1, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 2
        ArrayInitialize(BufferPMO, 0)
        ArrayInitialize(BufferSignal, EMPTY_VALUE)
        ArrayInitialize(BufferRaw1, 0)
        ArrayInitialize(BufferRaw2, 0)
        ArrayInitialize(BufferSmoothing1, 0)
    for i in range(limit, 0 - 1, -1):
        BufferRaw1[i] = (((_fdiv(close[i], close[i + 1]) * 100.0) - 100.0) if (close[i + 1] != 0) else 0)
        BufferSmoothing1[i] = ((BufferRaw1[i] - BufferSmoothing1[i + 1]) * smoothing1) + BufferSmoothing1[i + 1]
        BufferRaw2[i] = 10.0 * BufferSmoothing1[i]
        BufferPMO[i] = ((BufferRaw2[i] - BufferPMO[i + 1]) * smoothing2) + BufferPMO[i + 1]
        BufferSignal[i] = ExponentialMA(rates_total, periodS, i, BufferPMO)
    return rates_total

def ExponentialMA(rates_total, period, index, price):
    global _s_ExponentialMA_prev_value
    result = 0.0
    if period < 1 or index > (rates_total - period - 1):
        return 0.0
    pr = _fdiv(2.0, period + 1.0)
    if index == (rates_total - period - 1) or _s_ExponentialMA_prev_value == 0:
        result = SimpleMA(rates_total, period, index, price)
        _s_ExponentialMA_prev_value = result
    else:
        result = _s_ExponentialMA_prev_value + (pr * (price[index] - _s_ExponentialMA_prev_value))
        if index != 0:
            _s_ExponentialMA_prev_value = result
    return result

def SimpleMA(rates_total, period, index, price):
    result = 0.0
    if period < 1 or index > (rates_total - period - 1):
        return 0.0
    for i in range(0, period):
        result = result + price[index + i]
    result = _fdiv(result, period)
    return result

# ---- static local variables
_s_ExponentialMA_prev_value = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PriceMomentumOscillator(_MQL5Indicator):
    name = 'Price_Momentum_Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod1': 35,  # Period one
        'InpPeriod2': 20,  # Period two
        'InpPeriodSm': 10,  # Signal period
    }

