"""GetGridVals — converted from MQL5: MQL5 Indicators/Translating mouse click on chart into price value (Helper function)/GetGridVals.mq5


Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'GetGridVals', 'source': 'MQL5 Indicators/Translating mouse click on chart into price value (Helper function)/GetGridVals.mq5', 'folder': 'Translating mouse click on chart into price value (Helper function)', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
isMouseClicked = False

def OnInit():
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return 0

def OnChartEvent(id_, lparam, dparam, sparam):
    global isMouseClicked
    if id_ == CHARTEVENT_CLICK:
        isMouseClicked = True
    if isMouseClicked:
        Print('Clicked on grid at: x =', lparam, ' y =', dparam, ' => Price Level =', GetMouseY(dparam))

def GetMouseY(dparam):
    chartHeightInPixels = ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS)
    priceRange = ChartGetDouble(0, CHART_PRICE_MAX) - ChartGetDouble(0, CHART_PRICE_MIN)
    pixelsPerPrice = _fdiv(chartHeightInPixels, priceRange)
    mouseYValue = ChartGetDouble(0, CHART_PRICE_MAX) - _fdiv(dparam, pixelsPerPrice)
    return mouseYValue


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GetGridVals(_MQL5Indicator):
    name = 'GetGridVals'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

