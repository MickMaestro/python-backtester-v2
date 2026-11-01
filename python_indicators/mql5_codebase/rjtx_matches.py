"""rjtx_matches — converted from MQL5: MQL5 Indicators/RJTX_Matches/rjtx_matches.mq5

We recommend adjust the body and head size of the matches for better visualization.
Copyright: Copyright 2015, Rafael Jimenez Tocino; Link: http://www.tradingrafa.com/indicadores/rjt_matches; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2015, Rafael Jimenez Tocino', 'link': 'http://www.tradingrafa.com/indicadores/rjt_matches', 'version': '2.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 5, 5: 5}, 'colors': {1: [16711680], 2: [16711680], 3: [16711680], 4: [16711935], 5: [65280]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2, 5: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'match 1', 2: 'match 2', 3: 'match 3', 4: 'RJTX_Matches Sell', 5: 'RJTX_Matches Buy'}, 'levels': [], 'description': ['We recommend adjust the body and head size of the matches for better visualization.'], 'name': 'rjtx_matches', 'source': 'MQL5 Indicators/RJTX_Matches/rjtx_matches.mq5', 'folder': 'RJTX_Matches', 'inputs': [{'mql': 'iPeriod', 'py': 'iPeriod', 'param': 'iPeriod', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
iPeriod = _input('iPeriod', 10)
LineBuffer0 = Arr(0, 0.0)
LineBuffer1 = Arr(0, 0.0)
LineBuffer2 = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(iPeriod)
    IndInit(0, LineBuffer0, 0.0, min_rates_total, 0)
    IndInit(1, LineBuffer1, 0.0, min_rates_total, 0)
    IndInit(2, LineBuffer2, 0.0, min_rates_total, 0)
    IndInit(3, SellBuffer, 0.0, min_rates_total, 0)
    IndInit(4, BuyBuffer, 0.0, min_rates_total, 0)
    PlotIndexSetInteger(3, PLOT_ARROW, 174)
    PlotIndexSetInteger(4, PLOT_ARROW, 174)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'RJTX_Matches'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def IndInit(Number, Buffer, Empty_Value, Draw_Begin, nShift):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    ArraySetAsSeries(Buffer, True)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_p
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(open, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if close[bar] > open[bar + iPeriod]:
            SellBuffer[bar] = 0.0
            BuyBuffer[bar] = close[bar]
        else:
            SellBuffer[bar] = close[bar]
            BuyBuffer[bar] = 0.0
        _sw1 = _s_OnCalculate_p
        if _sw1 == 0:
            LineBuffer0[bar] = open[bar + iPeriod - 1]
            LineBuffer1[bar] = 0.0
            LineBuffer2[bar] = close[bar]
        elif _sw1 == 1:
            LineBuffer0[bar] = close[bar]
            LineBuffer1[bar] = open[bar + iPeriod - 1]
            LineBuffer2[bar] = 0.0
        elif _sw1 == 2:
            LineBuffer0[bar] = 0.0
            LineBuffer1[bar] = close[bar]
            LineBuffer2[bar] = open[bar + iPeriod - 1]
        if bar:
            _s_OnCalculate_p += 1
        if _s_OnCalculate_p > 2:
            _s_OnCalculate_p = 0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_p = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RjtxMatches(_MQL5Indicator):
    name = 'rjtx_matches'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iPeriod': 10,
    }

