"""centerofgravity — converted from MQL5: MQL5 Indicators/Center of Gravity J. F. Ehlers/centerofgravity.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [8421504, 65280, 255], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 4}, 'labels': {1: 'Center of Gravity', 2: 'Signal Line'}, 'levels': [], 'description': [], 'name': 'centerofgravity', 'source': 'MQL5 Indicators/Center of Gravity J. F. Ehlers/centerofgravity.mq5', 'folder': 'Center of Gravity J. F. Ehlers', 'inputs': [{'mql': 'Period_', 'py': 'Period_', 'param': 'Period_', 'type': 'int', 'default': 10, 'label': 'Indicator averaging period', 'sinput': False}, {'mql': 'SmoothPeriod', 'py': 'SmoothPeriod', 'param': 'SmoothPeriod', 'type': 'int', 'default': 3, 'label': 'Signal line smoothing period', 'sinput': False}, {'mql': 'MA_Method_', 'py': 'MA_Method_', 'param': 'MA_Method_', 'type': 'int', 'default': 0, 'label': 'Signal line averaging method', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
Period_ = _input('Period_', 10)  # Indicator averaging period
SmoothPeriod = _input('SmoothPeriod', 3)  # Signal line smoothing period
MA_Method_ = _input('MA_Method_', MODE_SMA)  # Signal line averaging method
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE_)  # Price constant
Ext1Buffer = Arr(0, 0.0)
Ext2Buffer = Arr(0, 0.0)
ColorExt2Buffer = Arr(0, 0.0)
StartBar = 0

def OnInit():
    global StartBar
    StartBar = Period_
    SetIndexBuffer(0, Ext1Buffer, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, 'Center of Gravity')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBar)
    SetIndexBuffer(1, ColorExt2Buffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBar + 1)
    SetIndexBuffer(2, Ext2Buffer, INDICATOR_DATA)
    PlotIndexSetString(2, PLOT_LABEL, 'Signal Line')
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, StartBar + 1)
    shortname = Box("")
    StringConcatenate(shortname, 'Center of Gravity(', Period_, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBar:
        return 0
    price_ = 0.0
    sma = 0.0
    lwma = 0.0
    first1 = 0
    first2 = 0
    first3 = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first1 = 0
        first2 = Period_ + 1
        first3 = Period_ + SmoothPeriod + 3
    else:
        first1 = prev_calculated - 1
        first2 = first1
        first3 = first1
    bar = first1
    for bar in range(bar, rates_total):
        price_ = PriceSeries(AppliedPrice, bar, open, low, high, close)
        sma = _s_OnCalculate_MA.MASeries(0, prev_calculated, rates_total, Period_, MODE_SMA, price_, bar, False)
        lwma = _s_OnCalculate_LWMA.MASeries(0, prev_calculated, rates_total, Period_, MODE_LWMA, price_, bar, False)
        Ext1Buffer[bar] = _fdiv(sma * lwma, Point())
        Ext2Buffer[bar] = _s_OnCalculate_SIGN.MASeries(first2, prev_calculated, rates_total, SmoothPeriod, MA_Method_, Ext1Buffer[bar], bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first3
    for bar in range(bar, rates_total):
        ColorExt2Buffer[bar] = 0.0
        if Ext1Buffer[bar] < Ext2Buffer[bar]:
            ColorExt2Buffer[bar] = 2.0
        else:
            ColorExt2Buffer[bar] = 1.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_MA = CMoving_Average()
_s_OnCalculate_LWMA = CMoving_Average()
_s_OnCalculate_SIGN = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Centerofgravity(_MQL5Indicator):
    name = 'centerofgravity'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period_': 10,  # Indicator averaging period
        'SmoothPeriod': 3,  # Signal line smoothing period
        'MA_Method_': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Signal line averaging method
        'AppliedPrice': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPLE_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'}, default=1),  # Price constant
    }

