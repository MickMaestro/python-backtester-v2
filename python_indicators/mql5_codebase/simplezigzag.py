"""simplezigzag — converted from MQL5: MQL5 Indicators/Simple ZigZag/simplezigzag.mq5

Copyright: Copyright 2014, Andrey Litvichenko, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2014, Andrey Litvichenko, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 6}, 'colors': {1: [8421376]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'ZZline'}, 'levels': [], 'description': [], 'name': 'simplezigzag', 'source': 'MQL5 Indicators/Simple ZigZag/simplezigzag.mq5', 'folder': 'Simple ZigZag', 'inputs': [{'mql': 'min_delta', 'py': 'min_delta', 'param': 'min_delta', 'type': 'int', 'default': 100, 'label': 'minimum range in points/минимальнный диапазон в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ETrendStatus
up = 0
down = 1
_enum('ETrendStatus', {0: 'up', 1: 'down'})

# ---- inputs and global variables
min_delta = _input('min_delta', 100)  # minimum range in points/минимальнный диапазон в пунктах
ZZHigh = Arr(0, 0.0)
ZZLow = Arr(0, 0.0)
delta = 0.0
state = 0

class SDot(MqlObject):
    _q_fields = ('price', 'time')
    def __init__(self, *args):
        self.price = 0.0
        self.time = 0

def OnInit():
    global delta
    SetIndexBuffer(0, ZZHigh, INDICATOR_DATA)
    SetIndexBuffer(1, ZZLow, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SimpleZigZag' + '(' + _str(min_delta) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    delta = min_delta * Point()
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global state
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        for i in range(0, rates_total):
            ZZHigh[bar] = 0.0
            ZZLow[bar] = 0.0
        first = 1
        if close[first] > open[first]:
            state = up
        else:
            state = down
        last_dot.price = close[first]
        last_dot.time = time[first]
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if bar == (rates_total - 1) and prev_calculated < rates_total:
            ZZHigh[bar] = 0.0
            ZZLow[bar] = 0.0
        _sw1 = state
        if _sw1 == up:
            if high[bar] > last_dot.price:
                if time[bar] > last_dot.time:
                    ZZHigh[ArrayBsearch(time, last_dot.time)] = 0.0
                last_dot.price = high[bar]
                last_dot.time = time[bar]
                ZZHigh[bar] = high[bar]
            if low[bar] < (last_dot.price - delta) and (time[bar] > last_dot.time or (high[bar - 1] - low[bar]) > delta):
                last_dot.time = time[bar]
                last_dot.price = low[bar]
                state = down
                ZZLow[bar] = low[bar]
                CheckInsideBar(bar, time, open, high, low, close)
        elif _sw1 == down:
            if low[bar] < last_dot.price:
                if time[bar] > last_dot.time:
                    ZZLow[ArrayBsearch(time, last_dot.time)] = 0.0
                last_dot.price = low[bar]
                last_dot.time = time[bar]
                ZZLow[bar] = low[bar]
            if high[bar] > (last_dot.price + delta) and (time[bar] > last_dot.time or (high[bar] - low[bar - 1]) > delta):
                last_dot.time = time[bar]
                last_dot.price = high[bar]
                state = up
                ZZHigh[bar] = high[bar]
                CheckInsideBar(bar, time, open, high, low, close)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def CheckInsideBar(bar, time, open, high, low, close):
    global state
    if high[bar - 1] > high[bar] and low[bar - 1] < low[bar]:
        _sw2 = state
        if _sw2 == up:
            if low[bar] < (high[bar] - delta):
                last_dot.time = time[bar]
                last_dot.price = low[bar]
                state = down
                ZZLow[bar] = low[bar]
        elif _sw2 == down:
            if high[bar] > (low[bar] + delta):
                last_dot.time = time[bar]
                last_dot.price = high[bar]
                state = up
                ZZHigh[bar] = high[bar]

# ---- global variables initialised from expressions
last_dot = _alloc(SDot)
last_dot.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Simplezigzag(_MQL5Indicator):
    name = 'simplezigzag'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'min_delta': 100,  # minimum range in points/минимальнный диапазон в пунктах
    }

