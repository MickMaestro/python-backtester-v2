"""PercentChange — converted from MQL5: MQL5 Indicators/Multi Symbol Chart/PercentChange.mq5

Percent Change
Copyright: Copyright 2015, pipPod.; Link: https://www.mql5.com/en/users/pippod; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2015, pipPod.', 'link': 'https://www.mql5.com/en/users/pippod', 'version': '1.10', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [3329330, 2237106, 65535]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Open;High;Low;Close'}, 'levels': [], 'description': ['Percent Change'], 'name': 'PercentChange', 'source': 'MQL5 Indicators/Multi Symbol Chart/PercentChange.mq5', 'folder': 'Multi Symbol Chart', 'inputs': [{'mql': 'chartID', 'py': 'chartID', 'param': 'chartID', 'type': 'long', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'eventID', 'py': 'eventID', 'param': 'eventID', 'type': 'ushort', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
chartID = _input('chartID', 0)
eventID = _input('eventID', 0)
OpenBuffer = Arr(0, 0.0)
HighBuffer = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)
CloseBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)

def OnInit():
    IndicatorSetString(INDICATOR_SHORTNAME, 'Percent Change')
    IndicatorSetInteger(0, INDICATOR_DIGITS, 4)
    SetIndexBuffer(0, OpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, HighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, LowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, CloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ColorBuffer, INDICATOR_COLOR_INDEX)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prevClose, _s_OnCalculate_prevCloseBuffer
    begin = prev_calculated - 1
    if not prev_calculated:
        barsWindow = MathMin(_int(ChartGetInteger(ChartID(), CHART_VISIBLE_BARS)) + 20, rates_total)
        begin = rates_total - barsWindow
        CloseBuffer[begin] = 0.0
        LowBuffer[begin] = CloseBuffer[begin]
        HighBuffer[begin] = LowBuffer[begin]
        OpenBuffer[begin] = HighBuffer[begin]
        begin += 1
    for i in range(begin, rates_total):
        if rates_total != prev_calculated:
            _s_OnCalculate_prevClose = close[i - 1]
            _s_OnCalculate_prevCloseBuffer = CloseBuffer[i - 1]
        if _s_OnCalculate_prevClose:
            OpenBuffer[i] = _s_OnCalculate_prevCloseBuffer + _fdiv(open[i], _s_OnCalculate_prevClose) - 1
            HighBuffer[i] = _s_OnCalculate_prevCloseBuffer + _fdiv(high[i], _s_OnCalculate_prevClose) - 1
            LowBuffer[i] = _s_OnCalculate_prevCloseBuffer + _fdiv(low[i], _s_OnCalculate_prevClose) - 1
            CloseBuffer[i] = _s_OnCalculate_prevCloseBuffer + _fdiv(close[i], _s_OnCalculate_prevClose) - 1
        else:
            CloseBuffer[i] = _s_OnCalculate_prevCloseBuffer
            LowBuffer[i] = CloseBuffer[i]
            HighBuffer[i] = LowBuffer[i]
            OpenBuffer[i] = HighBuffer[i]
        ColorBuffer[i] = (0 if (OpenBuffer[i] < CloseBuffer[i]) else 1 if (OpenBuffer[i] > CloseBuffer[i]) else 2)
    if prev_calculated:
        EventChartCustom(chartID, eventID, eventID, rates_total - prev_calculated, Symbol())
    return rates_total

# ---- static local variables
_s_OnCalculate_prevClose = 0.0
_s_OnCalculate_prevCloseBuffer = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PercentChange(_MQL5Indicator):
    name = 'PercentChange'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'chartID': 0,
        'eventID': 0,
    }

