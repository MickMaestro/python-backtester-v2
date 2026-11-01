"""fx_fish_2ma — converted from MQL5: MQL5 Indicators/FX_FISH_2MA/fx_fish_2ma.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 10, 2: 1, 3: 1, 4: 1}, 'colors': {1: [16711935, 8388736, 8421504, 16711680, 16748574], 2: [13828244], 3: [8421376], 4: [36095]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'FX_FISH Histogram', 2: 'FX_FISH Line', 3: 'FX_FISH MA Line1', 4: 'FX_FISH MA Line2'}, 'levels': [], 'description': [], 'name': 'fx_fish_2ma', 'source': 'MQL5 Indicators/FX_FISH_2MA/fx_fish_2ma.mq5', 'folder': 'FX_FISH_2MA', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'uint', 'default': 10, 'label': 'Extrema finding period', 'sinput': False}, {'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': 'Histogram averaging method', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'uint', 'default': 9, 'label': 'Histogram averaging period', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 100, 'label': 'Histogram averaging parameter', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 0, 'label': 'Signal line averaging method', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'uint', 'default': 45, 'label': 'Signal line averaging period', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 100, 'label': 'Signal line averaging parameter', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
period = _input('period', 10)  # Extrema finding period
MA_Method1 = _input('MA_Method1', MODE_SMA)  # Histogram averaging method
Length1 = _input('Length1', 9)  # Histogram averaging period
Phase1 = _input('Phase1', 100)  # Histogram averaging parameter
MA_Method2 = _input('MA_Method2', MODE_SMA)  # Signal line averaging method
Length2 = _input('Length2', 45)  # Signal line averaging period
Phase2 = _input('Phase2', 100)  # Signal line averaging parameter
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE_)  # Price constant
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
IndBuffer1 = Arr(0, 0.0)
IndBuffer2 = Arr(0, 0.0)
IndBuffer3 = Arr(0, 0.0)
IndBuffer4 = Arr(0, 0.0)
IndBuffer = Arr(0, 0.0)
ColorIndBuffer1 = Arr(0, 0.0)

def OnInit():
    global min_rates_1, min_rates_2, min_rates_total
    min_rates_1 = _int(period)
    min_rates_2 = min_rates_1 + XMA1.GetStartBars(MA_Method1, Length1, Phase1)
    min_rates_total = min_rates_2 + XMA1.GetStartBars(MA_Method2, Length2, Phase2)
    SetIndexBuffer(0, IndBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer1, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, IndBuffer2, INDICATOR_DATA)
    SetIndexBuffer(3, IndBuffer3, INDICATOR_DATA)
    SetIndexBuffer(4, IndBuffer4, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer1, True)
    ArraySetAsSeries(ColorIndBuffer1, True)
    ArraySetAsSeries(IndBuffer2, True)
    ArraySetAsSeries(IndBuffer3, True)
    ArraySetAsSeries(IndBuffer4, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    XMA1.XMALengthCheck('Length1', Length1)
    XMA1.XMALengthCheck('Length2', Length2)
    XMA1.XMAPhaseCheck('Phase1', Phase1, MA_Method1)
    XMA1.XMAPhaseCheck('Phase2', Phase2, MA_Method2)
    shortname = Box("")
    StringConcatenate(shortname, 'FX_FISH_2MA( ', period, ', ', Length1, ', ', Length2, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Fish1, _s_OnCalculate_Value1
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    maxbar1 = 0
    maxbar2 = 0
    price = 0.0
    Value = 0.0
    Range = 0.0
    Fish = 0.0
    MaxH = 0.0
    MinL = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_1 - 1
        _s_OnCalculate_Value1 = 0.0
        _s_OnCalculate_Fish1 = 0.0
    else:
        limit = rates_total - prev_calculated
    maxbar1 = rates_total - min_rates_1 - 1
    maxbar2 = rates_total - min_rates_2 - 1
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    Value = _s_OnCalculate_Value1
    Fish = _s_OnCalculate_Fish1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        MaxH = high[ArrayMaximum(high, bar, period)]
        MinL = low[ArrayMinimum(low, bar, period)]
        price = PriceSeries(AppliedPrice, bar, open, low, high, close)
        Range = MaxH - MinL
        if Range:
            Value = (0.33 * 2 * (_fdiv(price - MinL, Range) - 0.5)) + (0.67 * _s_OnCalculate_Value1)
        else:
            Value = 0.0
        Value = MathMin(MathMax(Value, -0.999), 0.999)
        Fish = (0.5 * MathLog(_fdiv(1 + Value, 1 - Value))) + (0.5 * _s_OnCalculate_Fish1)
        IndBuffer1[bar] = Fish
        IndBuffer2[bar] = Fish
        if bar:
            _s_OnCalculate_Value1 = Value
            _s_OnCalculate_Fish1 = Fish
        IndBuffer3[bar] = XMA1.XMASeries(maxbar1, prev_calculated, rates_total, MA_Method1, Phase1, Length1, Fish, bar, True)
        IndBuffer4[bar] = XMA2.XMASeries(maxbar2, prev_calculated, rates_total, MA_Method2, Phase2, Length2, IndBuffer3[bar], bar, True)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        clr = 2
        if IndBuffer1[bar] > 0:
            if IndBuffer1[bar] > IndBuffer1[bar + 1]:
                clr = 4
            if IndBuffer1[bar] < IndBuffer1[bar + 1]:
                clr = 3
        if IndBuffer1[bar] < 0:
            if IndBuffer1[bar] < IndBuffer1[bar + 1]:
                clr = 0
            if IndBuffer1[bar] > IndBuffer1[bar + 1]:
                clr = 1
        ColorIndBuffer1[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()

# ---- static local variables
_s_OnCalculate_Value1 = 0.0
_s_OnCalculate_Fish1 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FxFish2ma(_MQL5Indicator):
    name = 'fx_fish_2ma'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 10,  # Extrema finding period
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Histogram averaging method
        'Length1': 9,  # Histogram averaging period
        'Phase1': 100,  # Histogram averaging parameter
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Signal line averaging method
        'Length2': 45,  # Signal line averaging period
        'Phase2': 100,  # Signal line averaging parameter
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Price constant
    }

