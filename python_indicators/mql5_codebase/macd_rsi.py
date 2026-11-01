"""macd_rsi — converted from MQL5: MQL5 Indicators/MACD-RSI/macd_rsi.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 3, 2: 1, 3: 8}, 'colors': {1: [14822282], 2: [16711935]}, 'widths': {1: 2, 2: 1, 3: 2}, 'styles': {1: 0, 2: 4, 3: 0}, 'labels': {1: 'MACD', 2: 'Signal Line', 3: 'RSI'}, 'levels': [], 'description': [], 'name': 'macd_rsi', 'source': 'MQL5 Indicators/MACD-RSI/macd_rsi.mq5', 'folder': 'MACD-RSI', 'inputs': [{'mql': 'Fast_MA', 'py': 'Fast_MA', 'param': 'Fast_MA', 'type': 'int', 'default': 12, 'label': 'Period of MACD fast moving average', 'sinput': False}, {'mql': 'Slow_MA', 'py': 'Slow_MA', 'param': 'Slow_MA', 'type': 'int', 'default': 26, 'label': 'Depth of MACD slow moving average', 'sinput': False}, {'mql': 'MA_Method_', 'py': 'MA_Method_', 'param': 'MA_Method_', 'type': 'int', 'default': 1, 'label': 'Indicator averaging method', 'sinput': False}, {'mql': 'Signal_SMA', 'py': 'Signal_SMA', 'param': 'Signal_SMA', 'type': 'int', 'default': 9, 'label': 'Signal line period', 'sinput': False}, {'mql': 'AppliedPrice_', 'py': 'AppliedPrice_', 'param': 'AppliedPrice_', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'int', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'caliber', 'py': 'caliber', 'param': 'caliber', 'type': 'double', 'default': 4.0, 'label': 'Scaling', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

Gray = 0x808080  # MQL4 colour name
Lime = 0x00FF00  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

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
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
Fast_MA = _input('Fast_MA', 12)  # Period of MACD fast moving average
Slow_MA = _input('Slow_MA', 26)  # Depth of MACD slow moving average
MA_Method_ = _input('MA_Method_', MODE_EMA)  # Indicator averaging method
Signal_SMA = _input('Signal_SMA', 9)  # Signal line period
AppliedPrice_ = _input('AppliedPrice_', PRICE_CLOSE_)  # Price constant
RSIPeriod = _input('RSIPeriod', 14)  # RSI period
caliber = _input('caliber', 4.0)  # Scaling
MACDBuffer = Arr(0, 0.0)
SignBuffer = Arr(0, 0.0)
RSIBuffer = Arr(0, 0.0)
ColorRSIBuffer = Arr(0, 0.0)
positive_ = 0.0
negative_ = 0.0
macd_start = 0
sig_start = 0
rsi_start = 0

def OnInit():
    global macd_start, rsi_start, sig_start
    if MA_Method_ != MODE_EMA:
        macd_start = MathMax(Fast_MA, Slow_MA)
    else:
        macd_start = 0
    sig_start = macd_start + Signal_SMA
    rsi_start = sig_start + RSIPeriod
    SetIndexBuffer(0, MACDBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, macd_start)
    PlotIndexSetString(0, PLOT_LABEL, 'MACD')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, SignBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, sig_start)
    PlotIndexSetString(1, PLOT_LABEL, 'Signal SMA')
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, RSIBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, rsi_start + 1)
    PlotIndexSetString(2, PLOT_LABEL, 'RSI')
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, ColorRSIBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, rsi_start + 1)
    PlotIndexSetInteger(2, PLOT_COLOR_INDEXES, 3)
    for i in range(0, 3):
        PlotIndexSetInteger(2, PLOT_LINE_COLOR, i, ExtColor[i])
    shortname = Box("")
    StringConcatenate(shortname, 'MACD( ', Fast_MA, ', ', Slow_MA, ', ', Signal_SMA, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global negative_, positive_
    if rates_total < rsi_start:
        return 0
    first = 0
    bar = 0
    positive = 0.0
    negative = 0.0
    price_ = 0.0
    fast_ma = 0.0
    slow_ma = 0.0
    sumn = 0.0
    sump = 0.0
    rel = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price_ = PriceSeries(AppliedPrice_, bar, open, low, high, close)
        fast_ma = _s_OnCalculate_MA1.MASeries(0, prev_calculated, rates_total, Fast_MA, MA_Method_, price_, bar, False)
        slow_ma = _s_OnCalculate_MA2.MASeries(0, prev_calculated, rates_total, Slow_MA, MA_Method_, price_, bar, False)
        MACDBuffer[bar] = fast_ma - slow_ma
        SignBuffer[bar] = _s_OnCalculate_MA3.SMASeries(macd_start, prev_calculated, rates_total, Signal_SMA, MACDBuffer[bar], bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = macd_start + 1
        sumn = 0.0
        sump = 0.0
        bar = first
        for bar in range(bar, first + RSIPeriod):
            rel = MACDBuffer[bar] - MACDBuffer[bar - 1]
            if rel > 0:
                sump += rel
            else:
                sumn -= rel
        else:
            bar = _range_end(bar, first + RSIPeriod, 1)
        positive_ = sump / RSIPeriod
        negative_ = sumn / RSIPeriod
        first += RSIPeriod
    else:
        first = prev_calculated - 1
    positive = positive_
    negative = negative_
    bar = first
    for bar in range(bar, rates_total):
        if rates_total != prev_calculated and bar == 0:
            positive_ = positive
            negative_ = negative
        sump = 0.0
        sumn = 0.0
        rel = MACDBuffer[bar] - MACDBuffer[bar - 1]
        if rel > 0:
            sump = rel
        else:
            sumn = -rel
        positive = ((positive * (RSIPeriod - 1)) + sump) / RSIPeriod
        negative = ((negative * (RSIPeriod - 1)) + sumn) / RSIPeriod
        if negative == 0.0:
            RSIBuffer[bar] = 0.0
        else:
            RSIBuffer[bar] = caliber * Point() * (50.0 - _fdiv(100.0, 1 + _fdiv(positive, negative)))
        ColorRSIBuffer[bar] = 0.0
        if RSIBuffer[bar] > SignBuffer[bar]:
            ColorRSIBuffer[bar] = 1.0
        if RSIBuffer[bar] < SignBuffer[bar]:
            ColorRSIBuffer[bar] = 2.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
ExtColor = Arr.of([_uint(Gray), _uint(Lime), _uint(Red)], fill=0, dyn=False, size=3)

# ---- static local variables
_s_OnCalculate_MA1 = CMoving_Average()
_s_OnCalculate_MA2 = CMoving_Average()
_s_OnCalculate_MA3 = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MacdRsi(_MQL5Indicator):
    name = 'macd_rsi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Fast_MA': 12,  # Period of MACD fast moving average
        'Slow_MA': 26,  # Depth of MACD slow moving average
        'MA_Method_': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Indicator averaging method
        'Signal_SMA': 9,  # Signal line period
        'AppliedPrice_': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'}, default=1),  # Price constant
        'RSIPeriod': 14,  # RSI period
        'caliber': 4.0,  # Scaling
    }

