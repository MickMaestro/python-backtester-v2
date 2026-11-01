"""Support_and_Resistance_-_barry — converted from MQL5: MQL5 Indicators/Support ressitance - Barry (extended)/Support_and_Resistance_-_barry.mq5

Copyright: © mladen, 2016, MetaQuotes Software Corp.; Link: www.forex-tsd.com, www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2016, MetaQuotes Software Corp.', 'link': 'www.forex-tsd.com, www.mql5.com', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [14474460, 14474460], 2: [13422920], 3: [9221330]}, 'widths': {2: 2, 3: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Support_and_Resistance_-_barry', 'source': 'MQL5 Indicators/Support ressitance - Barry (extended)/Support_and_Resistance_-_barry.mq5', 'folder': 'Support ressitance - Barry (extended)', 'inputs': [{'mql': 'FractalPeriod', 'py': 'FractalPeriod', 'param': 'FractalPeriod', 'type': 'int', 'default': 25, 'label': 'Fractals period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FractalPeriod = _input('FractalPeriod', 25)  # Fractals period
res = Arr(0, 0.0)
sup = Arr(0, 0.0)
fup = Arr(0, 0.0)
fdn = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, fup, INDICATOR_DATA)
    SetIndexBuffer(1, fdn, INDICATOR_DATA)
    SetIndexBuffer(2, res, INDICATOR_DATA)
    SetIndexBuffer(3, sup, INDICATOR_DATA)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    k = 0
    half = _idiv(FractalPeriod, 2)
    compareTo = 0.0
    for i in range(MathMax(prev_calculated - half, half), rates_total):
        compareTo = high[i]
        k = 1
        while k <= half and (i + k) < rates_total:
            if high[i + k] > compareTo:
                break
            if high[i - k] >= compareTo:
                break
            k += 1
        fractalUp = (high[i] if (k == (half + 1)) else EMPTY_VALUE)
        compareTo = low[i]
        k = 1
        while k <= half and (i + k) < rates_total:
            if low[i + k] < compareTo:
                break
            if low[i - k] <= compareTo:
                break
            k += 1
        fractalDn = (high[i] if (k == (half + 1)) else EMPTY_VALUE)
        res[i] = (high[i] if (fractalUp != EMPTY_VALUE) else res[i - 1] if (i > 0) else high[i])
        fup[i] = res[i]
        sup[i] = (low[i] if (fractalDn != EMPTY_VALUE) else sup[i - 1] if (i > 0) else low[i])
        fdn[i] = sup[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SupportAndResistanceBarry(_MQL5Indicator):
    name = 'Support_and_Resistance_-_barry'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'FractalPeriod': 25,  # Fractals period
    }

