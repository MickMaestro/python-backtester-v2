"""hilo — converted from MQL5: MQL5 Indicators/HI LO Indicator/hilo.mq5

Copyright: Copyright 2010, Charly King Her; Link: www.bussinessclubworldwide.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2010, Charly King Her', 'link': 'www.bussinessclubworldwide.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'SmoothLine'}, 'levels': [], 'description': [], 'name': 'hilo', 'source': 'MQL5 Indicators/HI LO Indicator/hilo.mq5', 'folder': 'HI LO Indicator', 'inputs': [{'mql': 'PreferPeriod', 'py': 'PreferPeriod', 'param': 'PreferPeriod', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
PreferPeriod = _input('PreferPeriod', 10)
SmoothLineBuffer = Arr(0, 0.0)
HMABuffer = Arr(0, 0.0)
LMABuffer = Arr(0, 0.0)
HighMA = 0
LowMA = 0

def OnInit():
    global HighMA, LowMA
    SetIndexBuffer(0, SmoothLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, HMABuffer, INDICATOR_DATA)
    SetIndexBuffer(2, LMABuffer, INDICATOR_DATA)
    HighMA = iMA(Symbol(), 0, PreferPeriod, 0, MODE_SMA, PRICE_HIGH)
    LowMA = iMA(Symbol(), 0, PreferPeriod, 0, MODE_SMA, PRICE_LOW)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    buffer_status = CopyBuffer(HighMA, 0, 0, rates_total, HMABuffer)
    buffer_status *= CopyBuffer(LowMA, 0, 0, rates_total, LMABuffer)
    bars = BarsCalculated(HighMA)
    bars = MathMax(bars, BarsCalculated(LowMA))
    if buffer_status > 0 and bars >= rates_total:
        start_idx = 1
        if prev_calculated > 0:
            start_idx = prev_calculated - 1
        for idx in range(start_idx, rates_total):
            if close[idx] < LMABuffer[idx - 1]:
                SmoothLineBuffer[idx] = HMABuffer[idx - 1]
            else:
                SmoothLineBuffer[idx] = LMABuffer[idx - 1]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Hilo(_MQL5Indicator):
    name = 'hilo'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PreferPeriod': 10,
    }

