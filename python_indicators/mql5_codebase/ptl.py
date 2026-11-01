"""PTL — converted from MQL5: MQL5 Indicators/Perfect trend line/PTL.mq5

Perfect trend line
Copyright: © mladen, 2018; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 8, 4: 12}, 'colors': {1: [16748574], 2: [3937500], 3: [16748574, 3937500], 4: [16748574, 3937500]}, 'widths': {1: 2, 2: 2, 4: 2}, 'styles': {3: 2}, 'labels': {1: 'PTL slow line up', 2: 'PTL slow line down', 3: 'PTL fast line', 4: 'PTL trend start'}, 'levels': [], 'description': ['Perfect trend line'], 'name': 'PTL', 'source': 'MQL5 Indicators/Perfect trend line/PTL.mq5', 'folder': 'Perfect trend line', 'inputs': [{'mql': 'inpFastLength', 'py': 'inpFastLength', 'param': 'inpFastLength', 'type': 'int', 'default': 3, 'label': 'Fast length', 'sinput': False}, {'mql': 'inpSlowLength', 'py': 'inpSlowLength', 'param': 'inpSlowLength', 'type': 'int', 'default': 7, 'label': 'Slow length', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpFastLength = _input('inpFastLength', 3)  # Fast length
inpSlowLength = _input('inpSlowLength', 7)  # Slow length
slowlu = Arr(0, 0.0)
slowld = Arr(0, 0.0)
slowln = Arr(0, 0.0)
fastln = Arr(0, 0.0)
fastcl = Arr(0, 0.0)
arrowcl = Arr(0, 0.0)
arrowar = Arr(0, 0.0)
trend = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, slowlu, INDICATOR_DATA)
    SetIndexBuffer(1, slowld, INDICATOR_DATA)
    SetIndexBuffer(2, fastln, INDICATOR_DATA)
    SetIndexBuffer(3, fastcl, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, arrowar, INDICATOR_DATA)
    SetIndexBuffer(5, arrowcl, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, trend, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, slowln, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _startf = i - inpFastLength + 1
        if _startf < 0:
            _startf = 0
        _starts = i - inpSlowLength + 1
        if _starts < 0:
            _starts = 0
        thighs = high[ArrayMaximum(high, _starts, inpSlowLength)]
        tlows = low[ArrayMinimum(low, _starts, inpSlowLength)]
        thighf = high[ArrayMaximum(high, _startf, inpFastLength)]
        tlowf = low[ArrayMinimum(low, _startf, inpFastLength)]
        if i > 0:
            slowln[i] = (tlows if (close[i] > slowln[i - 1]) else thighs)
            fastln[i] = (tlowf if (close[i] > fastln[i - 1]) else thighf)
            trend[i] = trend[i - 1]
            if close[i] < slowln[i] and close[i] < fastln[i]:
                trend[i] = 1.0
            if close[i] > slowln[i] and close[i] > fastln[i]:
                trend[i] = 0.0
            arrowar[i] = (slowln[i] if (trend[i] != trend[i - 1]) else EMPTY_VALUE)
            slowlu[i] = (slowln[i] if (trend[i] == 0) else EMPTY_VALUE)
            slowld[i] = (slowln[i] if (trend[i] == 1) else EMPTY_VALUE)
        else:
            slowld[i] = EMPTY_VALUE
            slowlu[i] = slowld[i]
            arrowar[i] = slowlu[i]
            arrowcl[i] = 0.0
            fastcl[i] = arrowcl[i]
            trend[i] = fastcl[i]
            slowln[i] = close[i]
            fastln[i] = slowln[i]
        arrowcl[i] = trend[i]
        fastcl[i] = arrowcl[i]
        i += 1
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PTL(_MQL5Indicator):
    name = 'PTL'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpFastLength': 3,  # Fast length
        'inpSlowLength': 7,  # Slow length
    }

