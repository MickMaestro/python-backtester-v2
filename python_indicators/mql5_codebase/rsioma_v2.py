"""rsioma_v2 — converted from MQL5: MQL5 Indicators/RSIOMA_V2/rsioma_v2.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 5}, 'types': {1: 3, 2: 3, 3: 5, 4: 5, 5: 7}, 'colors': {1: [8421376], 2: [255], 3: [16760576], 4: [16711935], 5: [65280, 255]}, 'widths': {1: 2, 2: 2, 3: 4, 4: 4}, 'styles': {}, 'labels': {1: 'Upper', 2: 'Lower', 3: 'Buy', 4: 'Sell', 5: 'RSIOMA'}, 'levels': [], 'description': [], 'name': 'rsioma_v2', 'source': 'MQL5 Indicators/RSIOMA_V2/rsioma_v2.mq5', 'folder': 'RSIOMA_V2', 'inputs': [{'mql': 'RSIOMA_Method', 'py': 'RSIOMA_Method', 'param': 'RSIOMA_Method', 'type': 'int', 'default': 1, 'label': 'RSIOMA averaging method', 'sinput': False}, {'mql': 'RSIOMA', 'py': 'RSIOMA', 'param': 'RSIOMA', 'type': 'uint', 'default': 14, 'label': 'Depth of averaging of RSIOMA', 'sinput': False}, {'mql': 'RSIOMAPhase', 'py': 'RSIOMAPhase', 'param': 'RSIOMAPhase', 'type': 'int', 'default': 15, 'label': 'RSIOMA averaging parameter', 'sinput': False}, {'mql': 'MARSIOMA_Method', 'py': 'MARSIOMA_Method', 'param': 'MARSIOMA_Method', 'type': 'int', 'default': 1, 'label': 'MARSIOMA averaging method', 'sinput': False}, {'mql': 'MARSIOMA', 'py': 'MARSIOMA', 'param': 'MARSIOMA', 'type': 'uint', 'default': 21, 'label': 'RSIOMA averaging depth', 'sinput': False}, {'mql': 'MARSIOMAPhase', 'py': 'MARSIOMAPhase', 'param': 'MARSIOMAPhase', 'type': 'int', 'default': 15, 'label': 'RSIOMA averaging parameter', 'sinput': False}, {'mql': 'MomPeriod', 'py': 'MomPeriod', 'param': 'MomPeriod', 'type': 'uint', 'default': 1, 'label': 'Period of Momentum', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'BuyTrigger', 'py': 'BuyTrigger', 'param': 'BuyTrigger', 'type': 'uint', 'default': 80, 'label': 'Buy level', 'sinput': False}, {'mql': 'SellTrigger', 'py': 'SellTrigger', 'param': 'SellTrigger', 'type': 'uint', 'default': 20, 'label': 'Sell level', 'sinput': False}, {'mql': 'BuyTriggerColor', 'py': 'BuyTriggerColor', 'param': None, 'type': 'color', 'default': 16748574, 'label': 'Buy color', 'sinput': False}, {'mql': 'SellTriggerColor', 'py': 'SellTriggerColor', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'Sell color', 'sinput': False}, {'mql': 'MainTrendLong', 'py': 'MainTrendLong', 'param': 'MainTrendLong', 'type': 'uint', 'default': 60, 'label': 'Upper trigger level', 'sinput': False}, {'mql': 'MainTrendShort', 'py': 'MainTrendShort', 'param': 'MainTrendShort', 'type': 'uint', 'default': 40, 'label': 'Lower trigger level', 'sinput': False}, {'mql': 'MainTrendLongColor', 'py': 'MainTrendLongColor', 'param': None, 'type': 'color', 'default': 32768, 'label': 'Uptrend color', 'sinput': False}, {'mql': 'MainTrendShortColor', 'py': 'MainTrendShortColor', 'param': None, 'type': 'color', 'default': 255, 'label': 'Downtrend color', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
RSIOMA_Method = _input('RSIOMA_Method', MODE_EMA)  # RSIOMA averaging method
RSIOMA = _input('RSIOMA', 14)  # Depth of averaging of RSIOMA
RSIOMAPhase = _input('RSIOMAPhase', 15)  # RSIOMA averaging parameter
MARSIOMA_Method = _input('MARSIOMA_Method', MODE_EMA)  # MARSIOMA averaging method
MARSIOMA = _input('MARSIOMA', 21)  # RSIOMA averaging depth
MARSIOMAPhase = _input('MARSIOMAPhase', 15)  # RSIOMA averaging parameter
MomPeriod = _input('MomPeriod', 1)  # Period of Momentum
IPC = _input('IPC', PRICE_CLOSE)  # Price constant
BuyTrigger = _input('BuyTrigger', 80)  # Buy level
SellTrigger = _input('SellTrigger', 20)  # Sell level
BuyTriggerColor = _input('BuyTriggerColor', clrDodgerBlue)  # Buy color
SellTriggerColor = _input('SellTriggerColor', clrMagenta)  # Sell color
MainTrendLong = _input('MainTrendLong', 60)  # Upper trigger level
MainTrendShort = _input('MainTrendShort', 40)  # Lower trigger level
MainTrendLongColor = _input('MainTrendLongColor', clrGreen)  # Uptrend color
MainTrendShortColor = _input('MainTrendShortColor', clrRed)  # Downtrend color
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
IndBuffer = Arr(0, 0.0)
TriggerBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
min_rates_3 = 0

def OnInit():
    global min_rates_1, min_rates_2, min_rates_3, min_rates_total
    min_rates_1 = XMA1.GetStartBars(RSIOMA_Method, RSIOMA, RSIOMAPhase)
    min_rates_2 = _int(min_rates_1 + MomPeriod)
    min_rates_3 = _int(min_rates_2 + RSIOMA + 1)
    min_rates_total = min_rates_3
    XMA1.XMALengthCheck('RSIOMA', RSIOMA)
    XMA1.XMAPhaseCheck('RSIOMAPhase', RSIOMAPhase, RSIOMA_Method)
    XMA1.XMALengthCheck('MARSIOMA', MARSIOMA)
    XMA1.XMAPhaseCheck('RSIOMAPhase', RSIOMAPhase, MARSIOMA_Method)
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, BuyBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, SellBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, TriggerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSIOMA')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 4)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, BuyTrigger)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, SellTrigger)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, MainTrendLong)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, MainTrendShort)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, BuyTriggerColor)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, SellTriggerColor)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, MainTrendLongColor)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 3, MainTrendShortColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 3, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_negative, _s_OnCalculate_prev_positive
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    x1xma = 0.0
    rel = 0.0
    RSI = 0.0
    positive = 0.0
    negative = 0.0
    sump = 0.0
    sumn = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        sumn = 0.0
        sump = 0.0
        end = first + min_rates_3
        bar = first
        for bar in range(bar, end):
            price = PriceSeries(IPC, bar, open, low, high, close)
            x1xma = XMA1.XMASeries(0, prev_calculated, rates_total, RSIOMA_Method, RSIOMAPhase, RSIOMA, price, bar, False)
            rel = Mom.MomentumSeries(min_rates_1, prev_calculated, rates_total, MomPeriod, x1xma, bar, False)
            if bar >= min_rates_2:
                sump += MathMax(rel, 0)
                sumn -= MathMin(rel, 0)
        else:
            bar = _range_end(bar, end, 1)
        _s_OnCalculate_prev_positive = sump / RSIOMA
        _s_OnCalculate_prev_negative = sumn / RSIOMA
        first += min_rates_3
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        x1xma = XMA1.XMASeries(0, prev_calculated, rates_total, RSIOMA_Method, RSIOMAPhase, RSIOMA, price, bar, False)
        rel = Mom.MomentumSeries(min_rates_1, prev_calculated, rates_total, MomPeriod, x1xma, bar, False)
        sump = MathMax(rel, 0)
        sumn = -MathMin(rel, 0)
        positive = ((_s_OnCalculate_prev_positive * (RSIOMA - 1)) + sump) / RSIOMA
        negative = ((_s_OnCalculate_prev_negative * (RSIOMA - 1)) + sumn) / RSIOMA
        if negative:
            RSI = 100.0 - _fdiv(100.0, 1 + _fdiv(positive, negative))
        else:
            RSI = 0.0
        IndBuffer[bar] = RSI
        TriggerBuffer[bar] = XMA2.XMASeries(min_rates_3, prev_calculated, rates_total, MARSIOMA_Method, MARSIOMAPhase, MARSIOMA, RSI, bar, False)
        if bar < (rates_total - 1):
            _s_OnCalculate_prev_positive = positive
            _s_OnCalculate_prev_negative = negative
        UpBuffer[bar] = EMPTY_VALUE
        DnBuffer[bar] = EMPTY_VALUE
        BuyBuffer[bar] = EMPTY_VALUE
        SellBuffer[bar] = EMPTY_VALUE
        if RSI > MainTrendLong:
            UpBuffer[bar] = -10.0
        if RSI < MainTrendShort:
            DnBuffer[bar] = -10.0
        if RSI < SellTrigger and RSI > IndBuffer[bar - 1]:
            BuyBuffer[bar] = -15.0
        if RSI > BuyTrigger and RSI < IndBuffer[bar - 1]:
            SellBuffer[bar] = -15.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()
Mom = _alloc(CMomentum)
Mom.__init__()

# ---- static local variables
_s_OnCalculate_prev_positive = 0.0
_s_OnCalculate_prev_negative = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RsiomaV2(_MQL5Indicator):
    name = 'rsioma_v2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSIOMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # RSIOMA averaging method
        'RSIOMA': 14,  # Depth of averaging of RSIOMA
        'RSIOMAPhase': 15,  # RSIOMA averaging parameter
        'MARSIOMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # MARSIOMA averaging method
        'MARSIOMA': 21,  # RSIOMA averaging depth
        'MARSIOMAPhase': 15,  # RSIOMA averaging parameter
        'MomPeriod': 1,  # Period of Momentum
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Price constant
        'BuyTrigger': 80,  # Buy level
        'SellTrigger': 20,  # Sell level
        'MainTrendLong': 60,  # Upper trigger level
        'MainTrendShort': 40,  # Lower trigger level
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

