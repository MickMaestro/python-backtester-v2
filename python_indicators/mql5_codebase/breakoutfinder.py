"""BreakOutFinder_ — converted from MQL5: MQL5 Indicators/Breakout Finder by LonesomeTheBlue/BreakOutFinder_.mq5

Copyright: Copyright 2025, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2025, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'UpArrow', 2: 'DnArrow'}, 'levels': [], 'description': [], 'name': 'BreakOutFinder_', 'source': 'MQL5 Indicators/Breakout Finder by LonesomeTheBlue/BreakOutFinder_.mq5', 'folder': 'Breakout Finder by LonesomeTheBlue', 'inputs': [{'mql': 'lookback', 'py': 'lookback', 'param': 'lookback', 'type': 'int', 'default': 3000, 'label': 'Lookback bars', 'sinput': False}, {'mql': 'prd', 'py': 'prd', 'param': 'prd', 'type': 'int', 'default': 5, 'label': 'Period', 'sinput': False}, {'mql': 'bo_len', 'py': 'bo_len', 'param': 'bo_len', 'type': 'int', 'default': 200, 'label': 'Max Breakout Length', 'sinput': False}, {'mql': 'cwidthu', 'py': 'cwidthu', 'param': 'cwidthu', 'type': 'double', 'default': 3.0, 'label': 'Threshold Rate %', 'sinput': False}, {'mql': 'mintest', 'py': 'mintest', 'param': 'mintest', 'type': 'int', 'default': 2, 'label': 'Minimum Number of Tests', 'sinput': False}, {'mql': 'bocolordown', 'py': 'bocolordown', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'bocolorup', 'py': 'bocolorup', 'param': None, 'type': 'color', 'default': 16711680, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
UpArrowBuffer = Arr(0, 0.0)
DnArrowBuffer = Arr(0, 0.0)
lookback = _input('lookback', 3000)  # Lookback bars
prd = _input('prd', 5)  # Period
bo_len = _input('bo_len', 200)  # Max Breakout Length
cwidthu = _input('cwidthu', 3.0)  # Threshold Rate %
mintest = _input('mintest', 2)  # Minimum Number of Tests
bocolordown = _input('bocolordown', clrRed)
bocolorup = _input('bocolorup', clrBlue)
phval = Arr(0, 0.0)
phloc = Arr(0, 0.0)
plval = Arr(0, 0.0)
plloc = Arr(0, 0.0)
_cwidthu = 0.0

def OnInit():
    global _cwidthu
    SetIndexBuffer(0, UpArrowBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnArrowBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpArrowBuffer, True)
    ArraySetAsSeries(DnArrowBuffer, True)
    PlotIndexSetInteger(0, PLOT_ARROW, 233)
    PlotIndexSetInteger(1, PLOT_ARROW, 234)
    _cwidthu = cwidthu / 100
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BreakOutFinder(_MQL5Indicator):
    name = 'BreakOutFinder_'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'lookback': 3000,  # Lookback bars
        'prd': 5,  # Period
        'bo_len': 200,  # Max Breakout Length
        'cwidthu': 3.0,  # Threshold Rate %
        'mintest': 2,  # Minimum Number of Tests
    }

