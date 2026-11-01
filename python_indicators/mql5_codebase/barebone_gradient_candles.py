"""Barebone Gradient Candles — converted from MQL5: MQL5 Indicators/Barebone Gradient Candles/Barebone Gradient Candles.mq5

Colored Candlestick exemplifying a gradient
Copyright: 2021, Mateus Matucuma Teixeira; Link: https://github.com/BRMateus2/; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2021, Mateus Matucuma Teixeira', 'link': 'https://github.com/BRMateus2/', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Colored Candlestick exemplifying a gradient'], 'name': 'Barebone Gradient Candles', 'source': 'MQL5 Indicators/Barebone Gradient Candles/Barebone Gradient Candles.mq5', 'folder': 'Barebone Gradient Candles', 'inputs': [{'mql': 'cStart', 'py': 'cStart', 'param': None, 'type': 'color', 'default': 0, 'label': 'Beginning of the Gradient', 'sinput': False}, {'mql': 'cEnd', 'py': 'cEnd', 'param': None, 'type': 'color', 'default': 8388352, 'label': 'End of the Gradient', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
cStart = _input('cStart', 0x000000)  # Beginning of the Gradient
cEnd = _input('cEnd', 0x7FFF00)  # End of the Gradient
iBufOpenI = 0  # Index for Open Buffer values, also this is the first index and is the most important for setting the next plots
iBufOpen = Arr.of([], fill=0.0)  # Open Buffer values
iBufHighI = 1
iBufHigh = Arr.of([], fill=0.0)
iBufLowI = 2
iBufLow = Arr.of([], fill=0.0)
iBufCloseI = 3
iBufClose = Arr.of([], fill=0.0)
iBufColorI = 4
iBufColor = Arr.of([], fill=0.0)

def OnInit():
    SetIndexBuffer(iBufOpenI, iBufOpen, INDICATOR_DATA)
    SetIndexBuffer(iBufHighI, iBufHigh, INDICATOR_DATA)
    SetIndexBuffer(iBufLowI, iBufLow, INDICATOR_DATA)
    SetIndexBuffer(iBufCloseI, iBufClose, INDICATOR_DATA)
    SetIndexBuffer(iBufColorI, iBufColor, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(iBufOpenI, PLOT_DRAW_TYPE, DRAW_COLOR_CANDLES)
    PlotIndexSetDouble(iBufOpenI, PLOT_EMPTY_VALUE, DBL_MIN)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 64)
    for i in range(0, 64):
        PlotIndexSetInteger(iBufOpenI, PLOT_LINE_COLOR, i, argbGradient(cStart, cEnd, 1.0 - ((64.0 - i) / 64), 1.0 - ((64.0 - i) / 64)))
    PlotIndexSetString(iBufOpenI, PLOT_LABEL, 'Open;' + 'High;' + 'Low;' + 'Close')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_bars, _s_OnCalculate_colors
    for i in range(prev_calculated - 1, rates_total):
        if i < 0:
            continue
        iBufOpen[i] = open[i]
        iBufHigh[i] = high[i]
        iBufLow[i] = low[i]
        iBufClose[i] = close[i]
        iBufColor[i] = _s_OnCalculate_colors
        if _s_OnCalculate_bars != Bars(Symbol(), PERIOD_CURRENT):
            _s_OnCalculate_colors += 1
        if _s_OnCalculate_colors >= 64:
            _s_OnCalculate_colors = 0
    _s_OnCalculate_bars = Bars(Symbol(), PERIOD_CURRENT)
    return rates_total

def argbGradient(c1, c2, gradient=0.5, alpha=0.0):
    c = 0x00000000
    if gradient > 1.0:
        gradient = 1.0
    elif gradient < 0.0:
        gradient = 0.0
    if alpha > 1.0:
        alpha = 1.0
    elif alpha < 0.0:
        alpha = 0.0
    red1 = c1 & 0xFF
    green1 = (c1 & 0xFF00) >> 8
    blue1 = (c1 & 0xFF0000) >> 16
    alpha1 = (c1 & 0xFF000000) >> 24
    red2 = c2 & 0xFF
    green2 = (c2 & 0xFF00) >> 8
    blue2 = (c2 & 0xFF0000) >> 16
    alpha2 = (c2 & 0xFF000000) >> 24
    if red1 > red2:
        c = _uint(red1 - ((red1 - red2) * gradient)) & 0xFF
    else:
        c = _uint(red1 + ((red2 - red1) * gradient)) & 0xFF
    if green1 > green2:
        c = _uint((_uint(green1 - ((green1 - green2) * gradient)) & 0xFF) << 8) + c
    else:
        c = _uint((_uint(green1 + ((green2 - green1) * gradient)) & 0xFF) << 8) + c
    if blue1 > blue2:
        c = _uint((_uint(blue1 - ((blue1 - blue2) * gradient)) & 0xFF) << 16) + c
    else:
        c = _uint((_uint(blue1 + ((blue2 - blue1) * gradient)) & 0xFF) << 16) + c
    if alpha1 > alpha2:
        c = _uint((_uint(alpha1 - ((alpha1 - alpha2) * alpha)) & 0xFF) << 24) + c
    else:
        c = _uint((_uint(alpha1 + ((alpha2 - alpha1) * alpha)) & 0xFF) << 24) + c
    return c

# ---- static local variables
_s_OnCalculate_colors = 0
_s_OnCalculate_bars = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BareboneGradientCandles(_MQL5Indicator):
    name = 'Barebone Gradient Candles'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

