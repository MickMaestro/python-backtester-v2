"""WVF — converted from MQL5: MQL5 Indicators/WVF/WVF.mq5

William's Vix Fix indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [3329330, 17919]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'WVF'}, 'levels': [], 'description': ["William's Vix Fix indicator"], 'name': 'WVF', 'source': 'MQL5 Indicators/WVF/WVF.mq5', 'folder': 'WVF', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 22, 'label': 'Period', 'sinput': False}, {'mql': 'InpDrawingType', 'py': 'InpDrawingType', 'param': 'InpDrawingType', 'type': 'int', 'default': 8, 'label': 'Drawing style', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_DRAWING_STYLE
STYLE_DRAW_LINE = 8
STYLE_DRAW_HIST = 10
_enum('ENUM_DRAWING_STYLE', {8: 'STYLE_DRAW_LINE', 10: 'STYLE_DRAW_HIST'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 22)  # Period
InpDrawingType = _input('InpDrawingType', STYLE_DRAW_LINE)  # Drawing style
BufferWVF = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
period = 0

def OnInit():
    global period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferWVF, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'WVF(' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, InpDrawingType)
    ArraySetAsSeries(BufferWVF, True)
    ArraySetAsSeries(BufferColors, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period:
        return 0
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 2
        ArrayInitialize(BufferWVF, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        h = HighestClose(period, i)
        if h == WRONG_VALUE:
            continue
        max_ = close[h]
        BufferWVF[i] = (_fdiv(100 * (max_ - low[i]), max_) if (max_ > 0) else 0)
        BufferColors[i] = (1 if (BufferWVF[i] > BufferWVF[i + 1]) else 0)
    return rates_total

def HighestClose(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyClose(None, PERIOD_CURRENT, start, count, array) == count:
        return ArrayMaximum(array) + start
    return WRONG_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WVF(_MQL5Indicator):
    name = 'WVF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 22,  # Period
        'InpDrawingType': _Choice({8: 'Line', 10: 'Histogramm'}, default=8),  # Drawing style
    }

