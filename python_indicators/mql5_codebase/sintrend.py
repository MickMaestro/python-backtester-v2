"""sintrend — converted from MQL5: MQL5 Indicators/SinTrend/sintrend.mq5

Copyright: Copyright © 2005, DVYU; Link: http://www.DVYU.ox/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, DVYU', 'link': 'http://www.DVYU.ox/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 9639167, 16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'SinTrend'}, 'levels': [0.0], 'description': [], 'name': 'sintrend', 'source': 'MQL5 Indicators/SinTrend/sintrend.mq5', 'folder': 'SinTrend', 'inputs': [{'mql': 'g_period', 'py': 'g_period', 'param': 'g_period', 'type': 'int', 'default': 30, 'label': 'Period', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
g_period = _input('g_period', 30)  # Period
IPC = _input('IPC', PRICE_CLOSE)  # Applied price
ExtBuffer = Arr(0, 0.0)
ColorExtBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = g_period + 1
    SetIndexBuffer(0, ExtBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(1, ColorExtBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    short_name = 'SinTrend'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total + 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        ExtBuffer[bar] = MathSin((PriceSeries(IPC, bar, open, low, high, close) - PriceSeries(IPC, bar - g_period, open, low, high, close)) / g_period)
        ColorExtBuffer[bar] = 0.0
        if ExtBuffer[bar] > 0:
            ColorExtBuffer[bar] = 2.0
        if ExtBuffer[bar] < 0:
            ColorExtBuffer[bar] = 1.0
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
    else:
        return Close[bar]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Sintrend(_MQL5Indicator):
    name = 'sintrend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'g_period': 30,  # Period
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Applied price
    }

