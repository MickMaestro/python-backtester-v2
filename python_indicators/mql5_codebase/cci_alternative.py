"""Cci (alternative) — converted from MQL5: MQL5 Indicators/CCI alternative/Cci (alternative).mq5

CCI (alternative)
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [11119017, 15453831, 16748574]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'CCI alternative'}, 'levels': [], 'description': ['CCI (alternative)'], 'name': 'Cci (alternative)', 'source': 'MQL5 Indicators/CCI alternative/Cci (alternative).mq5', 'folder': 'CCI alternative', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'CCI period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # CCI period
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
prices = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, prices, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CCI (alternative)(' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        _start = MathMax(i - inpPeriod + 1, 0)
        prices[i] = (high[ArrayMaximum(high, _start, inpPeriod)] + low[ArrayMinimum(low, _start, inpPeriod)] + close[i]) / 3
        avg = 0.0
        k = 0
        while k < inpPeriod and (i - k) >= 0:
            avg += prices[i - k]
            k += 1
        avg = avg / inpPeriod
        dev = 0.0
        k = 0
        while k < inpPeriod and (i - k) >= 0:
            dev += MathAbs(prices[i - k] - avg)
            k += 1
        dev = dev / inpPeriod
        val[i] = (_fdiv(prices[i] - avg, 0.015 * dev) if (dev != 0) else 0)
        valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        i += 1
    return i


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CciAlternative(_MQL5Indicator):
    name = 'Cci (alternative)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # CCI period
    }

