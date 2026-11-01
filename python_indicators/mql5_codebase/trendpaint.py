"""trendpaint — converted from MQL5: MQL5 Indicators/TrendPaint/trendpaint.mq5

TrendPaint
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [255, 8388736, 11119017, 16443110, 8421376, 65280]}, 'widths': {}, 'styles': {}, 'labels': {1: 'TrendPaint Open'}, 'levels': [], 'description': ['TrendPaint'], 'name': 'trendpaint', 'source': 'MQL5 Indicators/TrendPaint/trendpaint.mq5', 'folder': 'TrendPaint', 'inputs': [{'mql': 'Fast_Method', 'py': 'Fast_Method', 'param': 'Fast_Method', 'type': 'int', 'default': 4, 'label': "'Fast' averaging method", 'sinput': False}, {'mql': 'Fast_Period', 'py': 'Fast_Period', 'param': 'Fast_Period', 'type': 'uint', 'default': 10, 'label': "Depth of the 'Fast' averaging", 'sinput': False}, {'mql': 'Fast_Phase', 'py': 'Fast_Phase', 'param': 'Fast_Phase', 'type': 'int', 'default': 100, 'label': "'Fast' averaging parameter,", 'sinput': False}, {'mql': 'Fast_Round', 'py': 'Fast_Round', 'param': 'Fast_Round', 'type': 'uint', 'default': 0, 'label': "The 'Rounding Fast' rounding ratio in points", 'sinput': False}, {'mql': 'Slow_Method', 'py': 'Slow_Method', 'param': 'Slow_Method', 'type': 'int', 'default': 0, 'label': "'Slow' averaging method", 'sinput': False}, {'mql': 'Slow_Period', 'py': 'Slow_Period', 'param': 'Slow_Period', 'type': 'int', 'default': 30, 'label': "Depth of the 'Slow' averaging", 'sinput': False}, {'mql': 'Slow_Phase', 'py': 'Slow_Phase', 'param': 'Slow_Phase', 'type': 'int', 'default': 100, 'label': "'Slow' averaging parameter,", 'sinput': False}, {'mql': 'Slow_Round', 'py': 'Slow_Round', 'param': 'Slow_Round', 'type': 'uint', 'default': 0, 'label': "The 'Rounding Slow' rounding ratio in points", 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'price constant', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
Fast_Method = _input('Fast_Method', MODE_JJMA)  # 'Fast' averaging method
Fast_Period = _input('Fast_Period', 10)  # Depth of the 'Fast' averaging
Fast_Phase = _input('Fast_Phase', 100)  # 'Fast' averaging parameter,
Fast_Round = _input('Fast_Round', 0)  # The 'Rounding Fast' rounding ratio in points
Slow_Method = _input('Slow_Method', MODE_SMA)  # 'Slow' averaging method
Slow_Period = _input('Slow_Period', 30)  # Depth of the 'Slow' averaging
Slow_Phase = _input('Slow_Phase', 100)  # 'Slow' averaging parameter,
Slow_Round = _input('Slow_Round', 0)  # The 'Rounding Slow' rounding ratio in points
IPC = _input('IPC', PRICE_CLOSE)  # price constant
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
Fast_nRound = 0.0
Slow_nRound = 0.0
Count = Arr(0, 0)
Round_Fast = Arr(0, 0.0)
Round_Slow = Arr(0, 0.0)

def OnInit():
    global Fast_nRound, Slow_nRound, min_rates_total
    min_rates_1 = XMA1.GetStartBars(Fast_Method, Fast_Period, Fast_Phase)
    min_rates_2 = XMA2.GetStartBars(Slow_Method, Slow_Period, Slow_Phase)
    min_rates_total = MathMax(min_rates_1, min_rates_2) + 4
    Slow_nRound = Slow_Round * Point()
    Fast_nRound = Fast_Round * Point()
    ArrayResize(Count, 4)
    ArrayResize(Round_Fast, 4)
    ArrayResize(Round_Slow, 4)
    XMA1.XMALengthCheck('Fast_Period', Fast_Period)
    XMA2.XMALengthCheck('Slow_Period', Slow_Period)
    XMA1.XMAPhaseCheck('Fast_Phase', Fast_Phase, Fast_Method)
    XMA2.XMAPhaseCheck('Slow_Phase', Slow_Phase, Slow_Method)
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'TrendPaint'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_ExtremumLong_, _s_OnCalculate_ExtremumShort_, _s_OnCalculate_Fast_Al_1, _s_OnCalculate_Fast_MA_1, _s_OnCalculate_Slow_Al_1, _s_OnCalculate_Slow_MA_1, _s_OnCalculate_Trend_
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    bar0 = 0
    bar1 = 0
    bar2 = 0
    bar3 = 0
    Trend = 0
    Fast_Al_0 = 0
    Slow_Al_0 = 0
    price_ = 0.0
    Fast_MA_0 = 0.0
    Slow_MA_0 = 0.0
    HHigh = 0.0
    LLow = 0.0
    ExtremumLong = 0.0
    ExtremumShort = 0.0
    res0 = 0.0
    res1 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        _s_OnCalculate_Fast_MA_1 = PriceSeries(IPC, first, open, low, high, close)
        _s_OnCalculate_Slow_MA_1 = _s_OnCalculate_Fast_MA_1
        _s_OnCalculate_Trend_ = 0
        _s_OnCalculate_Fast_Al_1 = 0
        _s_OnCalculate_Slow_Al_1 = 0
        _s_OnCalculate_ExtremumLong_ = 999999999.0
        _s_OnCalculate_ExtremumShort_ = 0.0
        _s_OnCalculate_Fast_Al_1 = 0
        _s_OnCalculate_Slow_Al_1 = 0
    else:
        first = prev_calculated - 1
    Trend = _s_OnCalculate_Trend_
    ExtremumLong = _s_OnCalculate_ExtremumLong_
    ExtremumShort = _s_OnCalculate_ExtremumShort_
    bar = first
    for bar in range(bar, rates_total):
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        Fast_MA_0 = XMA1.XMASeries(0, prev_calculated, rates_total, Fast_Method, Fast_Phase, Fast_Period, price_, bar, False)
        Slow_MA_0 = XMA2.XMASeries(0, prev_calculated, rates_total, Slow_Method, Slow_Phase, Slow_Period, price_, bar, False)
        bar0 = Count[0]
        bar1 = Count[1]
        bar2 = Count[2]
        bar3 = Count[3]
        res1 = Round_Fast[bar1]
        if ((((Fast_MA_0 > (_s_OnCalculate_Fast_MA_1 + Fast_nRound) or Fast_MA_0 < (_s_OnCalculate_Fast_MA_1 - Fast_nRound)) or Fast_MA_0 > (res1 + Fast_nRound)) or Fast_MA_0 < (res1 - Fast_nRound)) or (Fast_MA_0 > res1 and _s_OnCalculate_Fast_Al_1 == 1)) or (Fast_MA_0 < res1 and _s_OnCalculate_Fast_Al_1 == -1):
            Round_Fast[bar0] = Fast_MA_0
        else:
            Round_Fast[bar0] = res1
        res0 = Round_Fast[bar0]
        if res0 < res1:
            Fast_Al_0 = -1
        if res0 > res1:
            Fast_Al_0 = 1
        if res0 == res1:
            Fast_Al_0 = _s_OnCalculate_Fast_Al_1
        res1 = Round_Slow[bar1]
        if ((((Slow_MA_0 > (_s_OnCalculate_Slow_MA_1 + Slow_nRound) or Slow_MA_0 < (_s_OnCalculate_Slow_MA_1 - Slow_nRound)) or Slow_MA_0 > (res1 + Slow_nRound)) or Slow_MA_0 < (res1 - Slow_nRound)) or (Slow_MA_0 > res1 and _s_OnCalculate_Slow_Al_1 == 1)) or (Slow_MA_0 < res1 and _s_OnCalculate_Slow_Al_1 == -1):
            Round_Slow[bar0] = Slow_MA_0
        else:
            Round_Slow[bar0] = res1
        res0 = Round_Slow[bar0]
        if res0 < res1:
            Slow_Al_0 = -1
        if res0 > res1:
            Slow_Al_0 = 1
        if res0 == res1:
            Slow_Al_0 = _s_OnCalculate_Slow_Al_1
        if open[bar] > close[bar]:
            HHigh = open[bar]
            LLow = close[bar]
        elif open[bar] < close[bar]:
            HHigh = close[bar]
            LLow = open[bar]
        else:
            HHigh = close[bar]
            LLow = open[bar]
        if HHigh > ExtremumLong:
            ExtremumLong = HHigh
        if LLow < ExtremumShort:
            ExtremumShort = LLow
        if (Round_Slow[bar1] < Round_Fast[bar1] and Round_Slow[bar2] >= Round_Fast[bar2]) and Round_Slow[bar3] > Round_Fast[bar3]:
            Trend = 2
        if (Round_Slow[bar1] > Round_Fast[bar1] and Round_Slow[bar2] <= Round_Fast[bar2]) and Round_Slow[bar3] < Round_Fast[bar3]:
            Trend = -2
        if (Trend == 2 and Round_Slow[bar1] > Round_Fast[bar1]) or (Trend == -2 and Round_Slow[bar1] < Round_Fast[bar1]):
            Trend = 0
        ExtOpenBuffer[bar] = open[bar]
        ExtCloseBuffer[bar] = close[bar]
        ExtHighBuffer[bar] = high[bar]
        ExtLowBuffer[bar] = low[bar]
        _sw1 = Trend
        if _sw1 == -2:
            if close[bar] >= open[bar]:
                ExtColorBuffer[bar] = 1.0
            else:
                ExtColorBuffer[bar] = 0.0
        elif _sw1 == 0:
            if close[bar] >= open[bar]:
                ExtColorBuffer[bar] = 3.0
            else:
                ExtColorBuffer[bar] = 2.0
        elif _sw1 == 2:
            if close[bar] >= open[bar]:
                ExtColorBuffer[bar] = 5.0
            else:
                ExtColorBuffer[bar] = 4.0
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count)
            _s_OnCalculate_Fast_MA_1 = Fast_MA_0
            _s_OnCalculate_Slow_MA_1 = Slow_MA_0
            _s_OnCalculate_Fast_Al_1 = Fast_Al_0
            _s_OnCalculate_Slow_Al_1 = Slow_Al_0
        if bar == (rates_total - 2):
            _s_OnCalculate_Trend_ = Trend
            _s_OnCalculate_ExtremumLong_ = ExtremumLong
            _s_OnCalculate_ExtremumShort_ = ExtremumShort
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def Recount_ArrayZeroPos(CoArr):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = 4
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()

# ---- static local variables
_s_OnCalculate_Fast_MA_1 = 0.0
_s_OnCalculate_Slow_MA_1 = 0.0
_s_OnCalculate_ExtremumLong_ = 0.0
_s_OnCalculate_ExtremumShort_ = 0.0
_s_OnCalculate_Trend_ = 0
_s_OnCalculate_Fast_Al_1 = 0
_s_OnCalculate_Slow_Al_1 = 0
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Trendpaint(_MQL5Indicator):
    name = 'trendpaint'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Fast_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # 'Fast' averaging method
        'Fast_Period': 10,  # Depth of the 'Fast' averaging
        'Fast_Phase': 100,  # 'Fast' averaging parameter,
        'Fast_Round': 0,  # The 'Rounding Fast' rounding ratio in points
        'Slow_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # 'Slow' averaging method
        'Slow_Period': 30,  # Depth of the 'Slow' averaging
        'Slow_Phase': 100,  # 'Slow' averaging parameter,
        'Slow_Round': 0,  # The 'Rounding Slow' rounding ratio in points
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # price constant
    }

