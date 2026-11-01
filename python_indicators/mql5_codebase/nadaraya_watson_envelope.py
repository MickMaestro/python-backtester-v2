"""Nadaraya Watson Envelope — converted from MQL5: MQL5 Indicators/Nadaraya Watson Envelope/Nadaraya Watson Envelope.mq5

Copyright: Copyright 2022, Grasco.; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2022, Grasco.', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Nadaraya Watson Envelope', 'source': 'MQL5 Indicators/Nadaraya Watson Envelope/Nadaraya Watson Envelope.mq5', 'folder': 'Nadaraya Watson Envelope', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 500, 'label': 'Bars Count', 'sinput': False}, {'mql': 'Bandwidth', 'py': 'Bandwidth', 'param': 'Bandwidth', 'type': 'int', 'default': 17, 'label': 'Bandwidth', 'sinput': False}, {'mql': 'Multiplayer', 'py': 'Multiplayer', 'param': 'Multiplayer', 'type': 'double', 'default': 1.5, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 500)  # Bars Count
Bandwidth = _input('Bandwidth', 17)  # Bandwidth
Multiplayer = _input('Multiplayer', 1.5)
ExtUpBuffer = Arr(0, 0.0)
ExtDownBuffer = Arr(0, 0.0)
ExtCABuffer = Arr(0, 0.0)
y = Arr(0, 0.0)  # for calculation
ExtBarsHandle = 0
k = 2

def OnInit():
    global ExtBarsHandle
    SetIndexBuffer(0, ExtUpBuffer)
    SetIndexBuffer(1, ExtDownBuffer)
    SetIndexBuffer(2, y, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 0)
    PlotIndexGetInteger(1, PLOT_DRAW_BEGIN, 0)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    short_name = StringFormat('Nadraya', Length)
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    PlotIndexSetString(0, PLOT_LABEL, short_name + ' Upper')
    PlotIndexSetString(1, PLOT_LABEL, short_name + ' Lower')
    ExtBarsHandle = iMA(Symbol(), Period(), Length, 0, MODE_EMA, PRICE_WEIGHTED)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    if False:
        return 0
    calculated = BarsCalculated(ExtBarsHandle)
    if rates_total < calculated:
        return 0
    if rates_total < Length:
        return 0
    copyBars = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        copyBars = rates_total
    else:
        copyBars = rates_total - prev_calculated
        if prev_calculated > 0:
            copyBars += 1
    start = prev_calculated - 1
    if start < Length:
        start = Length
    sum_e = 0.0
    for i in range(rates_total - Length, rates_total):
        sum_ = 0.0
        sumw = 0.0
        for j in range(rates_total - Length, rates_total - 1):
            w = MathExp(-(MathPow(i - j, 2) / (Bandwidth * Bandwidth * 2)))
            sum_ += price[j] * w
            sumw += w
        y2 = _fdiv(sum_, sumw)
        sum_e += MathAbs(price[i] - y2)
        y[i] = y2
    mae = (sum_e / Length) * Multiplayer
    for i in range(rates_total - Length + 1, rates_total):
        y2 = y[i]
        y1 = y[i - 1]
        ExtUpBuffer[i] = y2 + mae
        ExtDownBuffer[i] = y2 - mae
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NadarayaWatsonEnvelope(_MQL5Indicator):
    name = 'Nadaraya Watson Envelope'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Length': 500,  # Bars Count
        'Bandwidth': 17,  # Bandwidth
        'Multiplayer': 1.5,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

