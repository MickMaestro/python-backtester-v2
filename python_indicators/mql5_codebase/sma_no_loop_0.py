"""SMA(no loop)_0 — converted from MQL5: MQL5 Indicators/SMA(no loop)/SMA(no loop)_0.mq5

Copyright: Copyright 2021, PuguForex; Link: https://www.mql5.com/en/users/puguforex; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2021, PuguForex', 'link': 'https://www.mql5.com/en/users/puguforex', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'SMA'}, 'levels': [], 'description': [], 'name': 'SMA(no loop)_0', 'source': 'MQL5 Indicators/SMA(no loop)/SMA(no loop)_0.mq5', 'folder': 'SMA(no loop)', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'SMA period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # SMA period
sma = Arr(0, 0.0)
sumSma = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, sma, INDICATOR_DATA)
    SetIndexBuffer(1, sumSma, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SMA(no loop)(' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = ((prev_calculated - 1) if prev_calculated else 0)
    for i in range(limit, rates_total):
        sumSma[i] = ((sumSma[i - 1] + close[i] - close[i - inpPeriod]) if (i > inpPeriod) else (sumSma[i - 1] + close[i] - ((i == inpPeriod) * close[0])) if (i > 0 and i <= inpPeriod) else close[i])
        sma[i] = sumSma[i] / inpPeriod
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SMANoLoop0(_MQL5Indicator):
    name = 'SMA(no loop)_0'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # SMA period
    }

