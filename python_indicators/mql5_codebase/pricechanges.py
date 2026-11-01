"""PriceChanges — converted from MQL5: MQL5 Indicators/PriceChanges/PriceChanges.mq5

Original Filename: 
Compile Time: 
Compiler Version: 
Link: https://www.mql5.com/ru/code/49132

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'link': 'https://www.mql5.com/ru/code/49132', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Original Filename: ', 'Compile Time: ', 'Compiler Version: '], 'name': 'PriceChanges', 'source': 'MQL5 Indicators/PriceChanges/PriceChanges.mq5', 'folder': 'PriceChanges', 'inputs': [], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}


def OnCalculate(_p0, _p1, _p2, _p3):
    return 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PriceChanges(_MQL5Indicator):
    name = 'PriceChanges'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

