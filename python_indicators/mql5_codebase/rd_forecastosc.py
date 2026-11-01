"""rd-forecastosc — converted from MQL5: MQL5 Indicators/RD-ForecastOsc/rd-forecastosc.mq5

Copyright: Copyright © 2005, Nick Bilak; Link: http://metatrader.50webs.com/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Nick Bilak', 'link': 'http://metatrader.50webs.com/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [7451452, 9639167]}, 'widths': {}, 'styles': {}, 'labels': {1: 'RD-Forecast Oscilator'}, 'levels': [], 'description': [], 'name': 'rd-forecastosc', 'source': 'MQL5 Indicators/RD-ForecastOsc/rd-forecastosc.mq5', 'folder': 'RD-ForecastOsc', 'inputs': [{'mql': 'length', 'py': 'length', 'param': 'length', 'type': 'uint', 'default': 15, 'label': '', 'sinput': False}, {'mql': 't3', 'py': 't3', 'param': 't3', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'b', 'py': 'b', 'param': 'b', 'type': 'double', 'default': 0.7, 'label': '', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
length = _input('length', 15)
t3 = _input('t3', 3)
b = _input('b', 0.7)
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
IndBuffer = Arr(0, 0.0)
SigBuffer = Arr(0, 0.0)
min_rates_total = 0
b2 = 0.0
b3 = 0.0
c1 = 0.0
c2 = 0.0
c3 = 0.0
c4 = 0.0
w1 = 0.0
w2 = 0.0
n = 0.0
Kx = 0.0
Br = 0.0

def OnInit():
    global Br, Kx, b2, b3, c1, c2, c3, c4, min_rates_total, n, w1, w2
    b2 = b * b
    b3 = b2 * b
    c1 = -b3
    c2 = 3 * (b2 + b3)
    c3 = -3 * ((2 * b2) + b + b3)
    c4 = 1 + (3 * b) + b3 + (3 * b2)
    n = MathMax(n, t3)
    n = 1 + (0.5 * (n - 1))
    w1 = _fdiv(2, n + 1)
    w2 = 1 - w1
    Kx = _fdiv(6.0, length * (length + 1.0))
    Br = (length + 1.0) / 3.0
    min_rates_total = _int(length + 1)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SigBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'RD-ForecastOsc'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_e1_, _s_OnCalculate_e2_, _s_OnCalculate_e3_, _s_OnCalculate_e4_, _s_OnCalculate_e5_, _s_OnCalculate_e6_
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    bar1 = 0
    WT = 0.0
    forecastosc = 0.0
    t3_fosc = 0.0
    sum_ = 0.0
    e1 = 0.0
    e2 = 0.0
    e3 = 0.0
    e4 = 0.0
    e5 = 0.0
    e6 = 0.0
    tmp = 0.0
    tmp2 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total + 1
        _s_OnCalculate_e1_ = 0.0
        _s_OnCalculate_e2_ = 0.0
        _s_OnCalculate_e3_ = 0.0
        _s_OnCalculate_e4_ = 0.0
        _s_OnCalculate_e5_ = 0.0
        _s_OnCalculate_e6_ = 0.0
    else:
        first = prev_calculated - 1
    bar1 = rates_total - 2
    e1 = _s_OnCalculate_e1_
    e2 = _s_OnCalculate_e2_
    e3 = _s_OnCalculate_e3_
    e4 = _s_OnCalculate_e4_
    e5 = _s_OnCalculate_e5_
    e6 = _s_OnCalculate_e6_
    bar = first
    for bar in range(bar, rates_total):
        sum_ = 0.0
        for i in range(_int(length), 0, -1):
            tmp = Br
            tmp2 = i
            tmp = tmp2 - tmp
            sum_ += tmp * PriceSeries(IPC, bar - length + i, open, low, high, close)
        WT = sum_ * Kx
        forecastosc = _fdiv(PriceSeries(IPC, bar, open, low, high, close) - WT, WT) * 100
        e1 = (w1 * forecastosc) + (w2 * e1)
        e2 = (w1 * e1) + (w2 * e2)
        e3 = (w1 * e2) + (w2 * e3)
        e4 = (w1 * e3) + (w2 * e4)
        e5 = (w1 * e4) + (w2 * e5)
        e6 = (w1 * e5) + (w2 * e6)
        t3_fosc = (c1 * e6) + (c2 * e5) + (c3 * e4) + (c4 * e3)
        IndBuffer[bar] = forecastosc
        SigBuffer[bar] = t3_fosc
        if bar == bar1:
            _s_OnCalculate_e1_ = e1
            _s_OnCalculate_e2_ = e2
            _s_OnCalculate_e3_ = e3
            _s_OnCalculate_e4_ = e4
            _s_OnCalculate_e5_ = e5
            _s_OnCalculate_e6_ = e6
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def PriceSeries(applied_price, bar, Open, Low, High, Close):
    _sw1 = applied_price
    if _sw1 == PRICE_CLOSE:
        return Close[bar]
    elif _sw1 == PRICE_OPEN:
        return Open[bar]
    elif _sw1 == PRICE_HIGH:
        return High[bar]
    elif _sw1 == PRICE_LOW:
        return Low[bar]
    elif _sw1 == PRICE_MEDIAN:
        return (High[bar] + Low[bar]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (Close[bar] + High[bar] + Low[bar]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return ((2 * Close[bar]) + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 8:
        return (Open[bar] + Close[bar]) / 2.0
    elif _sw1 == 9:
        return (Open[bar] + Close[bar] + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 10:
        if Close[bar] > Open[bar]:
            return High[bar]
        else:
            if Close[bar] < Open[bar]:
                return Low[bar]
            else:
                return Close[bar]
    elif _sw1 == 11:
        if Close[bar] > Open[bar]:
            return (High[bar] + Close[bar]) / 2.0
        else:
            if Close[bar] < Open[bar]:
                return (Low[bar] + Close[bar]) / 2.0
            else:
                return Close[bar]
    elif _sw1 == 12:
        res = High[bar] + Low[bar] + Close[bar]
        if Close[bar] < Open[bar]:
            res = (res + Low[bar]) / 2
        if Close[bar] > Open[bar]:
            res = (res + High[bar]) / 2
        if Close[bar] == Open[bar]:
            res = (res + Close[bar]) / 2
        return (res - Low[bar] + (res - High[bar])) / 2
    else:
        return Close[bar]

# ---- static local variables
_s_OnCalculate_e1_ = 0.0
_s_OnCalculate_e2_ = 0.0
_s_OnCalculate_e3_ = 0.0
_s_OnCalculate_e4_ = 0.0
_s_OnCalculate_e5_ = 0.0
_s_OnCalculate_e6_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RdForecastosc(_MQL5Indicator):
    name = 'rd-forecastosc'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'length': 15,
        't3': 3,
        'b': 0.7,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
    }

