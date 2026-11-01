"""colormacd — converted from MQL5: MQL5 Indicators/ColorMACD/colormacd.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 10, 2: 8}, 'colors': {1: [8421504, 8421376, 13828244, 6053069, 16711935], 2: [8421504, 65280, 255]}, 'widths': {1: 2, 2: 3}, 'styles': {1: 0, 2: 4}, 'labels': {1: 'MACD', 2: 'Signal Line'}, 'levels': [], 'description': [], 'name': 'colormacd', 'source': 'MQL5 Indicators/ColorMACD/colormacd.mq5', 'folder': 'ColorMACD', 'inputs': [{'mql': 'Fast_MA', 'py': 'Fast_MA', 'param': 'Fast_MA', 'type': 'int', 'default': 12, 'label': 'Fast moving average period', 'sinput': False}, {'mql': 'Slow_MA', 'py': 'Slow_MA', 'param': 'Slow_MA', 'type': 'int', 'default': 26, 'label': 'SMMA smoothing depth', 'sinput': False}, {'mql': 'MA_Method_', 'py': 'MA_Method_', 'param': 'MA_Method_', 'type': 'int', 'default': 1, 'label': 'Indicator averaging method', 'sinput': False}, {'mql': 'Signal_SMA', 'py': 'Signal_SMA', 'param': 'Signal_SMA', 'type': 'int', 'default': 9, 'label': 'Signal line period', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
Fast_MA = _input('Fast_MA', 12)  # Fast moving average period
Slow_MA = _input('Slow_MA', 26)  # SMMA smoothing depth
MA_Method_ = _input('MA_Method_', MODE_EMA)  # Indicator averaging method
Signal_SMA = _input('Signal_SMA', 9)  # Signal line period
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE_)  # Price constant
start = 0
macd_start = 0
MACDBuffer = Arr(0, 0.0)
SignBuffer = Arr(0, 0.0)
ColorMACDBuffer = Arr(0, 0.0)
ColorSignBuffer = Arr(0, 0.0)

def OnInit():
    global macd_start, start
    if MA_Method_ != MODE_EMA:
        macd_start = MathMax(Fast_MA, Slow_MA)
    start = macd_start + Signal_SMA + 1
    SetIndexBuffer(0, MACDBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, macd_start)
    PlotIndexSetString(0, PLOT_LABEL, 'MACD')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ColorMACDBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, macd_start + 1)
    SetIndexBuffer(2, SignBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, start)
    PlotIndexSetString(2, PLOT_LABEL, 'Signal SMA')
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, ColorSignBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, start + 1)
    shortname = Box("")
    StringConcatenate(shortname, 'MACD( ', Fast_MA, ', ', Slow_MA, ', ', Signal_SMA, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < start:
        return 0
    first1 = 0
    first2 = 0
    first3 = 0
    bar = 0
    price_ = 0.0
    fast_ma = 0.0
    slow_ma = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first1 = 0
        first2 = macd_start + 1
        first3 = start + 1
    else:
        first1 = prev_calculated - 1
        first2 = first1
        first3 = first1
    bar = first1
    for bar in range(bar, rates_total):
        price_ = PriceSeries(AppliedPrice, bar, open, low, high, close)
        fast_ma = _s_OnCalculate_MA1.MASeries(0, prev_calculated, rates_total, Fast_MA, MA_Method_, price_, bar, False)
        slow_ma = _s_OnCalculate_MA2.MASeries(0, prev_calculated, rates_total, Slow_MA, MA_Method_, price_, bar, False)
        MACDBuffer[bar] = fast_ma - slow_ma
        SignBuffer[bar] = _s_OnCalculate_MA3.SMASeries(macd_start, prev_calculated, rates_total, Signal_SMA, MACDBuffer[bar], bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first2
    for bar in range(bar, rates_total):
        ColorMACDBuffer[bar] = 0.0
        if MACDBuffer[bar] > 0:
            if MACDBuffer[bar] > MACDBuffer[bar - 1]:
                ColorMACDBuffer[bar] = 1.0
            if MACDBuffer[bar] < MACDBuffer[bar - 1]:
                ColorMACDBuffer[bar] = 2.0
        if MACDBuffer[bar] < 0:
            if MACDBuffer[bar] < MACDBuffer[bar - 1]:
                ColorMACDBuffer[bar] = 3.0
            if MACDBuffer[bar] > MACDBuffer[bar - 1]:
                ColorMACDBuffer[bar] = 4.0
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first3
    for bar in range(bar, rates_total):
        ColorSignBuffer[bar] = 0.0
        if MACDBuffer[bar] > SignBuffer[bar - 1]:
            ColorSignBuffer[bar] = 1.0
        if MACDBuffer[bar] < SignBuffer[bar - 1]:
            ColorSignBuffer[bar] = 2.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_MA1 = CMoving_Average()
_s_OnCalculate_MA2 = CMoving_Average()
_s_OnCalculate_MA3 = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colormacd(_MQL5Indicator):
    name = 'colormacd'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Fast_MA': 12,  # Fast moving average period
        'Slow_MA': 26,  # SMMA smoothing depth
        'MA_Method_': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Indicator averaging method
        'Signal_SMA': 9,  # Signal line period
        'AppliedPrice': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'}, default=1),  # Price constant
    }

