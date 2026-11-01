"""BMA — converted from MQL5: MQL5 Indicators/BMA or Band Moving Average MT5/BMA.mq5

Copyright: www.Wolfforex.com, 2025; Version: 1.06

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'www.Wolfforex.com, 2025', 'version': '1.06', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [255], 2: [16711680], 3: [32768]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {}, 'levels': [], 'description': [], 'name': 'BMA', 'source': 'MQL5 Indicators/BMA or Band Moving Average MT5/BMA.mq5', 'folder': 'BMA or Band Moving Average MT5', 'inputs': [{'mql': 'MA_Period', 'py': 'MA_Period', 'param': 'MA_Period', 'type': 'int', 'default': 49, 'label': '', 'sinput': False}, {'mql': 'MA_Shift', 'py': 'MA_Shift', 'param': 'MA_Shift', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Percentage', 'py': 'Percentage', 'param': 'Percentage', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MA_Period = _input('MA_Period', 49)
MA_Shift = _input('MA_Shift', 0)
MA_Method = _input('MA_Method', MODE_SMA)
Percentage = _input('Percentage', 2.0)
ExtMapBuffer1 = Arr(0, 0.0)
ExtMapBuffer2 = Arr(0, 0.0)
ExtMapBuffer3 = Arr(0, 0.0)

def OnInit():
    draw_begin = 0
    short_name = ""
    if MA_Period < 2:
        Print('MA Period should be greater than 1.')
        return INIT_PARAMETERS_INCORRECT
    draw_begin = MA_Period - 1
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_SHIFT, MA_Shift)
    PlotIndexSetInteger(1, PLOT_SHIFT, MA_Shift)
    PlotIndexSetInteger(2, PLOT_SHIFT, MA_Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, draw_begin)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, draw_begin)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, draw_begin)
    _sw1 = MA_Method
    if _sw1 == MODE_SMA:
        short_name = 'Band SMA('
    elif _sw1 == MODE_EMA:
        short_name = 'Band EMA('
        draw_begin = 0
    elif _sw1 == MODE_SMMA:
        short_name = 'Band SMMA('
    elif _sw1 == MODE_LWMA:
        short_name = 'Band LWMA('
    IndicatorSetString(INDICATOR_SHORTNAME, short_name + IntegerToString(MA_Period) + ')')
    SetIndexBuffer(0, ExtMapBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ExtMapBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, ExtMapBuffer3, INDICATOR_DATA)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, Close, tick_volume, volume, spread):
    ArraySetAsSeries(Close, False)
    if prev_calculated == 0:
        ArrayInitialize(ExtMapBuffer1, 0.0)
        ArrayInitialize(ExtMapBuffer2, 0.0)
        ArrayInitialize(ExtMapBuffer3, 0.0)
    if rates_total <= MA_Period:
        return 0
    _sw2 = MA_Method
    if _sw2 == MODE_SMA:
        sma(Close, rates_total)
    elif _sw2 == MODE_EMA:
        ema(Close, rates_total)
    elif _sw2 == MODE_SMMA:
        smma(Close, rates_total)
    elif _sw2 == MODE_LWMA:
        lwma(Close, rates_total)
    return rates_total

def sma(Close, rates_total):
    sum_ = 0.0
    pos = 0
    i = 0
    while i < (MA_Period - 1):
        sum_ += Close[pos]
        i += 1
        pos += 1
    while pos < rates_total:
        sum_ += Close[pos]
        ExtMapBuffer1[pos] = sum_ / MA_Period
        ExtMapBuffer2[pos] = (ExtMapBuffer1[pos] / 100) * (100 + Percentage)
        ExtMapBuffer3[pos] = (ExtMapBuffer1[pos] / 100) * (100 - Percentage)
        sum_ -= Close[pos - MA_Period + 1]
        pos += 1

def ema(Close, rates_total):
    pr = 2.0 / (MA_Period + 1)
    pos = 1
    while pos < rates_total:
        if pos == 1:
            ExtMapBuffer1[0] = Close[0]
        ExtMapBuffer1[pos] = (Close[pos] * pr) + (ExtMapBuffer1[pos - 1] * (1 - pr))
        ExtMapBuffer2[pos] = (ExtMapBuffer1[pos] / 100) * (100 + Percentage)
        ExtMapBuffer3[pos] = (ExtMapBuffer1[pos] / 100) * (100 - Percentage)
        pos += 1

def smma(Close, rates_total):
    sum_ = 0.0
    i = 0
    pos = MA_Period
    while pos < rates_total:
        if pos == MA_Period:
            i = 0
            for i in range(i, MA_Period):
                sum_ += Close[i]
                ExtMapBuffer1[i] = 0.0
                ExtMapBuffer2[i] = 0.0
                ExtMapBuffer3[i] = 0.0
            else:
                i = _range_end(i, MA_Period, 1)
        else:
            sum_ = (ExtMapBuffer1[pos - 1] * (MA_Period - 1)) + Close[pos]
        ExtMapBuffer1[pos] = sum_ / MA_Period
        ExtMapBuffer2[pos] = (ExtMapBuffer1[pos] / 100) * (100 + Percentage)
        ExtMapBuffer3[pos] = (ExtMapBuffer1[pos] / 100) * (100 - Percentage)
        pos += 1

def lwma(Close, rates_total):
    sum_ = 0.0
    lsum = 0.0
    price = 0.0
    i = 0
    weight = 0
    pos = 0
    i = 1
    while i <= MA_Period:
        price = Close[pos]
        sum_ += price * i
        lsum += price
        weight += i
        i += 1
        pos += 1
    i = pos - MA_Period
    while pos < rates_total:
        ExtMapBuffer1[pos] = _fdiv(sum_, weight)
        ExtMapBuffer2[pos] = (ExtMapBuffer1[pos] / 100) * (100 + Percentage)
        ExtMapBuffer3[pos] = (ExtMapBuffer1[pos] / 100) * (100 - Percentage)
        if pos == (rates_total - 1):
            break
        pos += 1
        i += 1
        price = Close[pos]
        sum_ = sum_ - lsum + (price * MA_Period)
        lsum -= Close[i]
        lsum += price


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BMA(_MQL5Indicator):
    name = 'BMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Period': 49,
        'MA_Shift': 0,
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Percentage': 2.0,
    }

