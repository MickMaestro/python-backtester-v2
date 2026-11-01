"""dummy — converted from MQL5: MQL5 Indicators/Currency Strength Index (CSI)/dummy.mq5

Accumulation/Distribution
Copyright: 2009-2017, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009-2017, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [11186720]}, 'widths': {}, 'styles': {}, 'labels': {1: 'dummy'}, 'levels': [], 'description': ['Accumulation/Distribution'], 'name': 'dummy', 'source': 'MQL5 Indicators/Currency Strength Index (CSI)/dummy.mq5', 'folder': 'Currency Strength Index (CSI)', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}


def OnInit():
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dummy(_MQL5Indicator):
    name = 'dummy'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

