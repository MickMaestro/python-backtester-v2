"""draw_none — converted from MQL5: MQL5 Indicators/DRAW_NONE/draw_none.mq5

Copyright: Copyright 2011, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2011, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 0}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Bar Index'}, 'levels': [], 'description': [], 'name': 'draw_none', 'source': 'MQL5 Indicators/DRAW_NONE/draw_none.mq5', 'folder': 'DRAW_NONE', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InvisibleBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, InvisibleBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_lastbar
    if prev_calculated == 0:
        CalcValues(rates_total, close)
        _s_OnCalculate_lastbar = SeriesInfoInteger(Symbol(), Period(), SERIES_LASTBAR_DATE)
    else:
        if _s_OnCalculate_lastbar != SeriesInfoInteger(Symbol(), Period(), SERIES_LASTBAR_DATE):
            CalcValues(rates_total, close)
            _s_OnCalculate_lastbar = SeriesInfoInteger(Symbol(), Period(), SERIES_LASTBAR_DATE)
    return rates_total

def CalcValues(total, array):
    ArraySetAsSeries(InvisibleBuffer, True)
    for i in range(0, total):
        InvisibleBuffer[i] = i

# ---- static local variables
_s_OnCalculate_lastbar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DrawNone(_MQL5Indicator):
    name = 'draw_none'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
    }

