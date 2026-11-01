"""Donchian_Oscillator — converted from MQL5: MQL5 Indicators/Donchian_Oscillator/Donchian_Oscillator.mq5

Donchian Oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [3329330, 255, 11119017]}, 'widths': {1: 8}, 'styles': {1: 0}, 'labels': {1: 'Donchian Osc'}, 'levels': [], 'description': ['Donchian Oscillator'], 'name': 'Donchian_Oscillator', 'source': 'MQL5 Indicators/Donchian_Oscillator/Donchian_Oscillator.mq5', 'folder': 'Donchian_Oscillator', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 20, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
BufferDOsc = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
period = 0

def OnInit():
    global period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferDOsc, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Donchian Oscillator (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_DIGITS, 6)
    ArraySetAsSeries(BufferDOsc, True)
    ArraySetAsSeries(BufferColors, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferDOsc, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 2)
    for i in range(limit, 0 - 1, -1):
        max_ = 0.0
        min_ = 0.0
        for j in range(i + period - 1, i, -1):
            if j == (i + period - 1):
                max_ = high[j]
                min_ = low[j]
            else:
                if high[j] > max_:
                    max_ = high[j]
                if low[j] < min_:
                    min_ = low[j]
        if close[i] > max_:
            BufferDOsc[i] = close[i] - max_
            BufferColors[i] = 0.0
        elif close[i] < min_:
            BufferDOsc[i] = close[i] - min_
            BufferColors[i] = 1.0
        else:
            BufferDOsc[i] = 0.0
            BufferColors[i] = 2.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DonchianOscillator(_MQL5Indicator):
    name = 'Donchian_Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
    }

