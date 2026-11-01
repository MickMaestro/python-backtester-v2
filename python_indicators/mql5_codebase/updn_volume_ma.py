"""UPDN Volume MA — converted from MQL5: MQL5 Indicators/Volume MA with candle color tracking/UPDN Volume MA.mq5

Copyright: Copyright 2025, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2025, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {}, 'colors': {1: [255], 2: [32768], 3: [12632256]}, 'widths': {3: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'UPDN Volume MA', 'source': 'MQL5 Indicators/Volume MA with candle color tracking/UPDN Volume MA.mq5', 'folder': 'Volume MA with candle color tracking', 'inputs': [{'mql': 'MA_Period', 'py': 'MA_Period', 'param': 'MA_Period', 'type': 'int', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'MA_Shift', 'py': 'MA_Shift', 'param': 'MA_Shift', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Green = 0x008000  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

# enum ENUM_MA_TYPE
sma = 0
ema = 1
smma = 2
lwma = 3
_enum('ENUM_MA_TYPE', {0: 'sma', 1: 'ema', 2: 'smma', 3: 'lwma'})

# ---- inputs and global variables
MA_Period = _input('MA_Period', 50)
MA_Shift = _input('MA_Shift', 0)
MA_Method = _input('MA_Method', 3)
VolBuffer1 = Arr(0, 0.0)  # value down
VolBuffer2 = Arr(0, 0.0)  # value up
VolBuffer3 = Arr(0, 0.0)  # moving average
ExtCountedBars = 0
lastcolor = 0

def OnInit():
    draw_begin = 0
    short_name = ""
    SetIndexBuffer(0, VolBuffer1)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_HISTOGRAM)
    PlotIndexSetInteger(0, PLOT_SHIFT, MA_Shift)
    SetIndexBuffer(1, VolBuffer2)
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DRAW_HISTOGRAM)
    PlotIndexSetInteger(1, PLOT_SHIFT, MA_Shift)
    SetIndexBuffer(2, VolBuffer3)
    PlotIndexSetInteger(2, PLOT_DRAW_TYPE, DRAW_LINE)
    PlotIndexSetInteger(2, PLOT_SHIFT, MA_Shift)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    draw_begin = MA_Period - 1
    _sw1 = MA_Method
    if _sw1 == 1:
        short_name = 'UD Vol EMA'
        draw_begin = 0
    elif _sw1 == 2:
        short_name = 'UD Vol SMMA'
    elif _sw1 == 3:
        short_name = 'UD Vol LWMA'
    else:
        short_name = 'UD Vol SMA'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name + '(' + IntegerToString(MA_Period) + ')')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, draw_begin)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total <= MA_Period:
        return rates_total
    start = ((MA_Period + 1) if (prev_calculated < MA_Period) else (prev_calculated - 1))
    for i in range(start, rates_total):
        _sw2 = MA_Method
        if _sw2 == 0:
            sma(tick_volume, open, close, i)
        elif _sw2 == 1:
            ema(tick_volume, open, close, i)
        elif _sw2 == 2:
            smma(tick_volume, open, close, i)
        elif _sw2 == 3:
            lwma(tick_volume, open, close, i)
        else:
            Print('Invalid MA_Method value: ', MA_Method)
    return rates_total

def sma(Volume, Open, Close, pos):
    sum_ = 0.0
    if pos < MA_Period:
        VolBuffer3[pos] = 0.0
    if pos < MA_Period:
        pos = MA_Period
    i = 1
    while i < MA_Period and (pos - i) > 0:
        sum_ += float(Volume[pos - i])
        i += 1
    VolBuffer3[pos] = sum_ / MA_Period
    Vcolor(pos, Open, Close, Volume)

def ema(Volume, Open, Close, pos):
    if pos < MA_Period:
        VolBuffer3[pos] = 0.0
    alpha = 2.0 / (MA_Period + 1)
    VolBuffer3[pos] = (Volume[pos] * alpha) + (VolBuffer3[pos - 1] * (1 - alpha))
    Vcolor(pos, Open, Close, Volume)

def smma(Volume, Open, Close, pos):
    if pos < MA_Period:
        VolBuffer3[pos] = 0.0
    if pos == MA_Period:
        sum_ = 0.0
        for i in range(0, MA_Period):
            sum_ += float(Volume[pos - i])
        VolBuffer3[pos] = sum_ / MA_Period
    else:
        VolBuffer3[pos] = ((VolBuffer3[pos - 1] * (MA_Period - 1)) + Volume[pos]) / MA_Period
    Vcolor(pos, Open, Close, Volume)

def lwma(Volume, Open, Close, pos):
    if pos < MA_Period:
        VolBuffer3[pos] = 0.0
    sum_ = 0.0
    weighted_sum = 0.0
    for i in range(0, MA_Period):
        sum_ += float(Volume[pos - i]) * (MA_Period - i)
        weighted_sum += MA_Period - i
    VolBuffer3[pos] = _fdiv(sum_, weighted_sum)
    Vcolor(pos, Open, Close, Volume)

def Vcolor(p, Open, Close, Volume):
    global lastcolor
    if Close[p] < Open[p]:
        VolBuffer1[p] = float(Volume[p])
        VolBuffer2[p] = 0.0
        lastcolor = _int(Red)
    if Close[p] >= Open[p]:
        VolBuffer1[p] = 0.0
        VolBuffer2[p] = float(Volume[p])
        lastcolor = _int(Green)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class UPDNVolumeMA(_MQL5Indicator):
    name = 'UPDN Volume MA'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Period': 50,
        'MA_Shift': 0,
        'MA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA'}, default=3),
    }

