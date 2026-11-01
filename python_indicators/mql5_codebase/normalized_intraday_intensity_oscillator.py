"""Normalized_Intraday_Intensity_Oscillator — converted from MQL5: MQL5 Indicators/Normalized_Intraday_Intensity_Oscillator/Normalized_Intraday_Intensity_Oscillator.mq5

Normalized Intraday Intensity Oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16760576]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Intensity'}, 'levels': [], 'description': ['Normalized Intraday Intensity Oscillator'], 'name': 'Normalized_Intraday_Intensity_Oscillator', 'source': 'MQL5 Indicators/Normalized_Intraday_Intensity_Oscillator/Normalized_Intraday_Intensity_Oscillator.mq5', 'folder': 'Normalized_Intraday_Intensity_Oscillator', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
BufferNII = Arr(0, 0.0)
BufferTemp = Arr(0, 0.0)
BufferRaw = Arr(0, 0.0)
period_sm = 0

def OnInit():
    global period_sm
    period_sm = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferNII, INDICATOR_DATA)
    SetIndexBuffer(1, BufferRaw, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferTemp, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Normalized Intraday Intensity (' + _str(period_sm) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferNII, True)
    ArraySetAsSeries(BufferTemp, True)
    ArraySetAsSeries(BufferRaw, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < fmax(period_sm, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferNII, EMPTY_VALUE)
        ArrayInitialize(BufferTemp, 0)
        ArrayInitialize(BufferRaw, 0)
    for i in range(limit, 0 - 1, -1):
        BufferTemp[i] = ((_fdiv((2.0 * close[i]) - high[i] - low[i], high[i] - low[i]) * tick_volume[i]) if ((high[i] - low[i]) != 0) else 0)
        BufferRaw[i] = float(tick_volume[i])
        raw_avg = GetSMA(rates_total, i, period_sm, BufferRaw)
        BufferNII[i] = ((_fdiv(GetSMA(rates_total, i, period_sm, BufferTemp), raw_avg) * 100.0) if (raw_avg != 0) else 0)
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


class NormalizedIntradayIntensityOscillator(_MQL5Indicator):
    name = 'Normalized_Intraday_Intensity_Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 10,  # Period
    }

