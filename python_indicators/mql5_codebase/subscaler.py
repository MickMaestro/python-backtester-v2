"""SubScaler — converted from MQL5: MQL5 Indicators/SubScaler/SubScaler.mq5

Subwindow scaler: use Up/Down arrow keys to scale up/down; hold Shift with arrow keys to move up/down.\\n
Scaling up means that picture becomes larger (zoom in, can be clipped), whereas scaling down means that picture becomes smaller (zoom out).\\n
SubScaler must be the 1-st indicator in subwindow; affected indicator must be the next and switched to 'inherited scale'; chart must have keyboard focus for the keys to take effect.\\n
Copyright: Copyright (c) 2021, Marketeer; Link: https://www.mql5.com/en/users/marketeer; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright (c) 2021, Marketeer', 'link': 'https://www.mql5.com/en/users/marketeer', 'version': '1.0', 'window': 'separate', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Subwindow scaler: use Up/Down arrow keys to scale up/down; hold Shift with arrow keys to move up/down.\\n', 'Scaling up means that picture becomes larger (zoom in, can be clipped), whereas scaling down means that picture becomes smaller (zoom out).\\n', "SubScaler must be the 1-st indicator in subwindow; affected indicator must be the next and switched to 'inherited scale'; chart must have keyboard focus for the keys to take effect.\\n"], 'name': 'SubScaler', 'source': 'MQL5 Indicators/SubScaler/SubScaler.mq5', 'folder': 'SubScaler', 'inputs': [{'mql': 'FixedMaximum', 'py': 'FixedMaximum', 'param': 'FixedMaximum', 'type': 'double', 'default': 1000.0, 'label': 'Initial Maximum', 'sinput': False}, {'mql': 'FixedMinimum', 'py': 'FixedMinimum', 'param': 'FixedMinimum', 'type': 'double', 'default': -1000.0, 'label': 'Initial Minimum', 'sinput': False}, {'mql': '_ScaleFactor', 'py': '_ScaleFactor', 'param': '_ScaleFactor', 'type': 'double', 'default': 0.1, 'label': 'Scale Factor [0.01 ... 0.5]', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FixedMaximum = _input('FixedMaximum', 1000.0)  # Initial Maximum
FixedMinimum = _input('FixedMinimum', -1000.0)  # Initial Minimum
_ScaleFactor = _input('_ScaleFactor', 0.1)  # Scale Factor [0.01 ... 0.5]
ScaleFactor = 0.0
w = -1
n = -1

def OnInit():
    global ScaleFactor, n, w
    ScaleFactor = _ScaleFactor
    if ScaleFactor < 0.01 or ScaleFactor > 0.5:
        PrintFormat('ScaleFactor %f is adjusted to default value 0.1, valid range is [0.01, 0.5]', ScaleFactor)
        ScaleFactor = 0.1
    w = ChartWindowFind()
    n = ChartIndicatorsTotal(0, w)

def scale(cmd, shift):
    min_ = ChartGetDouble(0, CHART_PRICE_MIN, w)
    max_ = ChartGetDouble(0, CHART_PRICE_MAX, w)
    if (shift & 0x10000000) == 0:
        if cmd == 38:
            IndicatorSetDouble(INDICATOR_MINIMUM, _fdiv(min_, 1.0 + ScaleFactor))
            IndicatorSetDouble(INDICATOR_MAXIMUM, _fdiv(max_, 1.0 + ScaleFactor))
            ChartRedraw()
        elif cmd == 40:
            IndicatorSetDouble(INDICATOR_MINIMUM, min_ * (1.0 + ScaleFactor))
            IndicatorSetDouble(INDICATOR_MAXIMUM, max_ * (1.0 + ScaleFactor))
            ChartRedraw()
    else:
        if cmd == 38:
            d = (max_ - min_) * ScaleFactor
            IndicatorSetDouble(INDICATOR_MINIMUM, min_ - d)
            IndicatorSetDouble(INDICATOR_MAXIMUM, max_ - d)
            ChartRedraw()
        elif cmd == 40:
            d = (max_ - min_) * ScaleFactor
            IndicatorSetDouble(INDICATOR_MINIMUM, min_ + d)
            IndicatorSetDouble(INDICATOR_MAXIMUM, max_ + d)
            ChartRedraw()

def OnChartEvent(id_, lparam, dparam, sparam):
    global n
    _sw1 = id_
    if _sw1 == CHARTEVENT_KEYDOWN:
        scale(lparam, TerminalInfoInteger(TERMINAL_KEYSTATE_SHIFT))
    elif _sw1 == CHARTEVENT_CHART_CHANGE:
        if ChartIndicatorsTotal(0, w) > n:
            n = ChartIndicatorsTotal(0, w)
            min_ = ChartGetDouble(0, CHART_PRICE_MIN, w)
            max_ = ChartGetDouble(0, CHART_PRICE_MAX, w)
            PrintFormat('Change: %f %f %d', min_, max_, n)
            if min_ == 0 and max_ == 0:
                IndicatorSetDouble(INDICATOR_MINIMUM, FixedMinimum)
                IndicatorSetDouble(INDICATOR_MAXIMUM, FixedMaximum)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SubScaler(_MQL5Indicator):
    name = 'SubScaler'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FixedMaximum': 1000.0,  # Initial Maximum
        'FixedMinimum': -1000.0,  # Initial Minimum
        '_ScaleFactor': 0.1,  # Scale Factor [0.01 ... 0.5]
    }

