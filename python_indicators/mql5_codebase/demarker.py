"""demarker — converted from MQL5: MQL5 Indicators/DeMarker (DeM)/demarker.mq5

Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [0.3, 0.7], 'description': [], 'name': 'demarker', 'source': 'MQL5 Indicators/DeMarker (DeM)/demarker.mq5', 'folder': 'DeMarker (DeM)', 'inputs': [{'mql': 'InpDeMarkerPeriod', 'py': 'InpDeMarkerPeriod', 'param': 'InpDeMarkerPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpDeMarkerPeriod = _input('InpDeMarkerPeriod', 14)  # Period
ExtDeMarkerBuffer = Arr(0, 0.0)
ExtDeMaxBuffer = Arr(0, 0.0)
ExtDeMinBuffer = Arr(0, 0.0)
ExtAvgDeMaxBuffer = Arr(0, 0.0)
ExtAvgDeMinBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtDeMarkerBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtDeMaxBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, ExtDeMinBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtAvgDeMaxBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ExtAvgDeMinBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, 3)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpDeMarkerPeriod)
    IndicatorSetString(INDICATOR_SHORTNAME, 'DeM(' + _str(InpDeMarkerPeriod) + ')')

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    limit = 0
    dNum = 0.0
    if rates_total < InpDeMarkerPeriod:
        return 0
    if prev_calculated == 0:
        ExtDeMaxBuffer[0] = 0.0
        ExtDeMinBuffer[0] = 0.0
        i = 1
        for i in range(i, InpDeMarkerPeriod):
            if High[i] > High[i - 1]:
                ExtDeMaxBuffer[i] = High[i] - High[i - 1]
            else:
                ExtDeMaxBuffer[i] = 0.0
            if Low[i - 1] > Low[i]:
                ExtDeMinBuffer[i] = Low[i - 1] - Low[i]
            else:
                ExtDeMinBuffer[i] = 0.0
        else:
            i = _range_end(i, InpDeMarkerPeriod, 1)
        i = 0
        for i in range(i, InpDeMarkerPeriod):
            ExtDeMarkerBuffer[i] = 0.0
        else:
            i = _range_end(i, InpDeMarkerPeriod, 1)
        limit = InpDeMarkerPeriod - 1
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        if High[i] > High[i - 1]:
            ExtDeMaxBuffer[i] = High[i] - High[i - 1]
        else:
            ExtDeMaxBuffer[i] = 0.0
        if Low[i - 1] > Low[i]:
            ExtDeMinBuffer[i] = Low[i - 1] - Low[i]
        else:
            ExtDeMinBuffer[i] = 0.0
        ExtAvgDeMaxBuffer[i] = SimpleMA(i, InpDeMarkerPeriod, ExtDeMaxBuffer)
        ExtAvgDeMinBuffer[i] = SimpleMA(i, InpDeMarkerPeriod, ExtDeMinBuffer)
        dNum = ExtAvgDeMaxBuffer[i] + ExtAvgDeMinBuffer[i]
        if dNum != 0:
            ExtDeMarkerBuffer[i] = _fdiv(ExtAvgDeMaxBuffer[i], dNum)
        else:
            ExtDeMarkerBuffer[i] = 0.0
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Demarker(_MQL5Indicator):
    name = 'demarker'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpDeMarkerPeriod': 14,  # Period
    }

