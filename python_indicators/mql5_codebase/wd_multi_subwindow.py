"""wd.Multi_SubWindow — converted from MQL5: MQL5 Indicators/wd.Multi_ClockPrice lite!/wd.Multi_SubWindow.mq5

An empty sub-window provides space for information, labels, simple notes, and works simultaneously with other 'wd.Multi/Range' EAs or indicators.
Copyright: Copyright © 2023, Karya Prima Rajasa Mediavestama.; Link: https://www.mql5.com/en/users/widhie75; Version: 2.23

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2023, Karya Prima Rajasa Mediavestama.', 'link': 'https://www.mql5.com/en/users/widhie75', 'version': '2.23', 'window': 'separate', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ["An empty sub-window provides space for information, labels, simple notes, and works simultaneously with other 'wd.Multi/Range' EAs or indicators."], 'name': 'wd.Multi_SubWindow', 'source': 'MQL5 Indicators/wd.Multi_ClockPrice lite!/wd.Multi_SubWindow.mq5', 'folder': 'wd.Multi_ClockPrice lite!', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}


def OnInit():
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WdMultiSubWindow(_MQL5Indicator):
    name = 'wd.Multi_SubWindow'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

