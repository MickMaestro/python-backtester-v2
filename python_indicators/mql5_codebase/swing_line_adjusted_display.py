"""Swing line (adjusted display) — converted from MQL5: MQL5 Indicators/Swing Line (adjusted display)/Swing line (adjusted display).mq5

Swing line - adjusted display
Copyright: Copyright 2017, mladen; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2017, mladen', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 10, 'indicator_plots': 3}, 'types': {1: 8, 2: 11, 3: 17}, 'colors': {1: [3329330, 9662683], 2: [3329330, 9662683], 3: [3329330, 9662683]}, 'widths': {1: 3, 2: 3, 3: 3}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Swing line', 2: 'Swing line bars', 3: 'Swing line candles'}, 'levels': [], 'description': ['Swing line - adjusted display'], 'name': 'Swing line (adjusted display)', 'source': 'MQL5 Indicators/Swing Line (adjusted display)/Swing line (adjusted display).mq5', 'folder': 'Swing Line (adjusted display)', 'inputs': [{'mql': 'inpDisplayType', 'py': 'inpDisplayType', 'param': 'inpDisplayType', 'type': 'int', 'default': 9999, 'label': 'Display type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enDisplayType
dis_line = 2
dis_bars = 0
dis_candle = 1
dis_auto = 9999
_enum('enDisplayType', {2: 'dis_line', 0: 'dis_bars', 1: 'dis_candle', 9999: 'dis_auto'})

# ---- inputs and global variables
inpDisplayType = _input('inpDisplayType', dis_auto)  # Display type
swli = Arr(0, 0.0)
swlicc = Arr(0, 0.0)
baru = Arr(0, 0.0)
bard = Arr(0, 0.0)
barcc = Arr(0, 0.0)
candleo = Arr(0, 0.0)
candleh = Arr(0, 0.0)
candlel = Arr(0, 0.0)
candlec = Arr(0, 0.0)
candlecc = Arr(0, 0.0)
work = Arr(0, 0.0, dims=(5,))

def OnInit():
    SetIndexBuffer(0, swli, INDICATOR_DATA)
    SetIndexBuffer(1, swlicc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, baru, INDICATOR_DATA)
    SetIndexBuffer(3, bard, INDICATOR_DATA)
    SetIndexBuffer(4, barcc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, candleo, INDICATOR_DATA)
    SetIndexBuffer(6, candleh, INDICATOR_DATA)
    SetIndexBuffer(7, candlel, INDICATOR_DATA)
    SetIndexBuffer(8, candlec, INDICATOR_DATA)
    SetIndexBuffer(9, candlecc, INDICATOR_COLOR_INDEX)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_sChartStyle
    limit = MathMax(prev_calculated - 1, 0)
    chartStyle = Box(0)
    ChartGetInteger(0, CHART_MODE, 0, chartStyle)
    if inpDisplayType == dis_auto:
        if _s_OnCalculate_sChartStyle != chartStyle.v:
            _s_OnCalculate_sChartStyle = chartStyle.v
            limit = 0
    else:
        _s_OnCalculate_sChartStyle = inpDisplayType
    if ArrayRange(work, 0) != rates_total:
        ArrayResize(work, rates_total)
    for i in range(limit, rates_total):
        if i == 0:
            work[i][0] = high[i]
            work[i][1] = low[i]
            work[i][2] = high[i]
            work[i][3] = low[i]
            work[i][4] = -1.0
            continue
        work[i][4] = work[i - 1][4]
        work[i][0] = work[i - 1][0]
        work[i][1] = work[i - 1][1]
        work[i][2] = work[i - 1][2]
        work[i][3] = work[i - 1][3]
        if work[i - 1][4] == 1:
            work[i][0] = MathMax(work[i - 1][0], high[i])
            work[i][1] = MathMax(work[i - 1][1], low[i])
            if high[i] < work[i][1]:
                work[i][4] = -1.0
                work[i][2] = high[i]
                work[i][3] = low[i]
        if work[i - 1][4] == -1:
            work[i][2] = MathMin(work[i - 1][2], high[i])
            work[i][3] = MathMin(work[i - 1][3], low[i])
            if low[i] > work[i][2]:
                work[i][4] = 1.0
                work[i][0] = high[i]
                work[i][1] = low[i]
        swli[i] = EMPTY_VALUE
        baru[i] = EMPTY_VALUE
        bard[i] = baru[i]
        candlec[i] = EMPTY_VALUE
        candlel[i] = candlec[i]
        candleh[i] = candlel[i]
        candleo[i] = candleh[i]
        _sw1 = _int(_s_OnCalculate_sChartStyle)
        if _sw1 == CHART_LINE:
            swli[i] = (work[i][1] if (work[i][4] == 1) else work[i][2])
            swlicc[i] = (0 if (work[i][4] == 1) else 1 if (work[i][4] == -1) else swlicc[i - 1] if (i > 0) else 0)
        elif _sw1 == CHART_BARS:
            baru[i] = high[i]
            bard[i] = low[i]
            barcc[i] = (0 if (work[i][4] == 1) else 1 if (work[i][4] == -1) else barcc[i - 1] if (i > 0) else 0)
        elif _sw1 == CHART_CANDLES:
            candleh[i] = high[i]
            candlel[i] = low[i]
            candleo[i] = open[i]
            candlec[i] = close[i]
            candlecc[i] = (0 if (work[i][4] == 1) else 1 if (work[i][4] == -1) else candlecc[i - 1] if (i > 0) else 0)
    return rates_total

# ---- static local variables
_s_OnCalculate_sChartStyle = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SwingLineAdjustedDisplay(_MQL5Indicator):
    name = 'Swing line (adjusted display)'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpDisplayType': _Choice({2: 'Display colored line', 0: 'Display colored bars', 1: 'Display colored candles', 9999: 'Adjust automatically depending on chart type'}, default=9999),  # Display type
    }

