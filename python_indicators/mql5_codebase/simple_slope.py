"""Simple_Slope — converted from MQL5: MQL5 Indicators/Simple_Slope/Simple_Slope.mq5

Simple slope oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Simple slope'}, 'levels': [], 'description': ['Simple slope oscillator'], 'name': 'Simple_Slope', 'source': 'MQL5 Indicators/Simple_Slope/Simple_Slope.mq5', 'folder': 'Simple_Slope', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
BufferSS = Arr(0, 0.0)
period = 0

def OnInit():
    global period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferSS, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Simple slope (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferSS, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferSS, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        BufferSS[i] = _fdiv(close[i] - close[i + period], period)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SimpleSlope(_MQL5Indicator):
    name = 'Simple_Slope'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
    }

