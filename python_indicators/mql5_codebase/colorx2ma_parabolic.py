"""colorx2ma-parabolic — converted from MQL5: MQL5 Indicators/ColorX2MA-Parabolic/colorx2ma-parabolic.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 5}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 8}, 'colors': {1: [255], 2: [64636], 3: [9639167], 4: [64636], 5: [8421504, 8421376, 16711935]}, 'widths': {1: 4, 2: 4, 3: 4, 4: 4, 5: 2}, 'styles': {5: 0}, 'labels': {1: 'Lower Parabolic', 2: 'Upper Parabolic', 3: 'Parabolic Sell', 4: 'Parabolic Buy', 5: 'X2MA'}, 'levels': [], 'description': [], 'name': 'colorx2ma-parabolic', 'source': 'MQL5 Indicators/ColorX2MA-Parabolic/colorx2ma-parabolic.mq5', 'folder': 'ColorX2MA-Parabolic', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': 'Method of averaging of the first smoothing', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'uint', 'default': 12, 'label': 'first smoothing depth', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'First smoothing parameter,', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 4, 'label': 'method of averaging of the second smoothing', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'uint', 'default': 5, 'label': 'second smoothing depth', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 15, 'label': 'Second smoothing parameter,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'price constant', 'sinput': False}, {'mql': 'StepH_', 'py': 'StepH_', 'param': 'StepH_', 'type': 'double', 'default': 0.2, 'label': 'Step for high points', 'sinput': False}, {'mql': 'MaximumH', 'py': 'MaximumH', 'param': 'MaximumH', 'type': 'double', 'default': 0.5, 'label': 'Maximum for high points', 'sinput': False}, {'mql': 'StepL_', 'py': 'StepL_', 'param': 'StepL_', 'type': 'double', 'default': 0.02, 'label': 'Step for low points', 'sinput': False}, {'mql': 'MaximumL', 'py': 'MaximumL', 'param': 'MaximumL', 'type': 'double', 'default': 0.05, 'label': 'Maximum for low points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
MA_Method1 = _input('MA_Method1', MODE_SMA)  # Method of averaging of the first smoothing
Length1 = _input('Length1', 12)  # first smoothing depth
Phase1 = _input('Phase1', 15)  # First smoothing parameter,
MA_Method2 = _input('MA_Method2', MODE_JJMA)  # method of averaging of the second smoothing
Length2 = _input('Length2', 5)  # second smoothing depth
Phase2 = _input('Phase2', 15)  # Second smoothing parameter,
IPC = _input('IPC', PRICE_CLOSE)  # price constant
StepH_ = _input('StepH_', 0.2)  # Step for high points
MaximumH = _input('MaximumH', 0.5)  # Maximum for high points
StepL_ = _input('StepL_', 0.02)  # Step for low points
MaximumL = _input('MaximumL', 0.05)  # Maximum for low points
X2MA = Arr(0, 0.0)
ColorX2MA = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
UpSarBuffer = Arr(0, 0.0)
DnSarBuffer = Arr(0, 0.0)
dirlong_ = False
first_ = False
ep_ = 0.0
start_ = 0.0
last_high_ = 0.0
last_low_ = 0.0
StepH = 0.0
StepL = 0.0
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0

def OnInit():
    global StepH, StepL, min_rates_1, min_rates_2, min_rates_total
    min_rates_1 = XMA1.GetStartBars(MA_Method1, Length1, Phase1)
    min_rates_2 = XMA2.GetStartBars(MA_Method2, Length2, Phase2)
    min_rates_total = min_rates_1 + min_rates_2 + 2
    XMA1.XMALengthCheck('Length1', Length1)
    XMA2.XMALengthCheck('Length2', Length2)
    XMA1.XMAPhaseCheck('Phase1', Phase1, MA_Method1)
    XMA2.XMAPhaseCheck('Phase2', Phase2, MA_Method2)
    StepH = MathMin(StepH_, MaximumH)
    StepL = MathMin(StepL_, MaximumL)
    SetIndexBuffer(0, UpSarBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 158)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, DnSarBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 158)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(3, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(4, X2MA, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(5, ColorX2MA, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'X2MA-Parabolic')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global dirlong_, ep_, first_, last_high_, last_low_, start_
    if rates_total < min_rates_total:
        return 0
    price_ = 0.0
    x1xma = 0.0
    x2xma = 0.0
    price_low = 0.0
    price_high = 0.0
    sar = 0.0
    ep = 0.0
    start = 0.0
    last_high = 0.0
    last_low = 0.0
    gfirst = 0
    bar = 0
    dirlong = False
    first = False
    if prev_calculated > rates_total or prev_calculated <= 0:
        gfirst = 0
        first_ = False
        dirlong_ = False
        last_high_ = 0.0
        last_low_ = 999999999.0
        ep_ = close[min_rates_total - 1]
        start_ = 0.0
    else:
        gfirst = prev_calculated - 1
    ep = ep_
    start = start_
    last_high = last_high_
    last_low = last_low_
    dirlong = dirlong_
    first = first_
    bar = gfirst
    for bar in range(bar, rates_total):
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        x1xma = XMA1.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, price_, bar, False)
        x2xma = XMA2.XMASeries(min_rates_1, prev_calculated, rates_total, MA_Method2, Phase2, Length2, x1xma, bar, False)
        X2MA[bar] = x2xma
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        gfirst = min_rates_total
    bar = gfirst
    for bar in range(bar, rates_total):
        ColorX2MA[bar] = 0.0
        if X2MA[bar - 1] < X2MA[bar]:
            ColorX2MA[bar] = 1.0
        if X2MA[bar - 1] > X2MA[bar]:
            ColorX2MA[bar] = 2.0
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = gfirst
    for bar in range(bar, rates_total):
        price_low = X2MA[bar] - Point()
        price_high = X2MA[bar] + Point()
        prev_sar = MathMax(UpSarBuffer[bar - 1], DnSarBuffer[bar - 1])
        sar = prev_sar + (start * (ep - prev_sar))
        if dirlong:
            if ep < price_high and (start + StepL) <= MaximumL:
                start += StepL
            if sar >= price_low:
                start = StepL
                dirlong = False
                ep = price_low
                last_low = price_low
                if price_high < last_high:
                    sar = last_high
                else:
                    sar = price_high
            else:
                if ep < price_low and (start + StepL) <= MaximumL:
                    start += StepL
                if ep < price_high:
                    last_high = price_high
                    ep = price_high
        else:
            if ep > price_low and (start + StepH) <= MaximumH:
                start += StepH
            if sar <= price_high:
                start = StepH
                dirlong = True
                ep = price_high
                last_high = price_high
                if price_low > last_low:
                    sar = last_low
                else:
                    sar = price_low
            else:
                if ep > price_high and (start + StepH) <= MaximumH:
                    start += StepH
                if ep > price_low:
                    last_low = price_low
                    ep = price_low
        DnSarBuffer[bar] = 0.0
        UpSarBuffer[bar] = 0.0
        if X2MA[bar] < sar:
            UpSarBuffer[bar] = sar
        else:
            DnSarBuffer[bar] = sar
        if bar == (rates_total - 2):
            ep_ = ep
            start_ = start
            last_high_ = last_high
            last_low_ = last_low
            dirlong_ = dirlong
            first_ = first
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        gfirst += 1
    bar = gfirst
    for bar in range(bar, rates_total):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if UpSarBuffer[bar - 1] > 0.0 and DnSarBuffer[bar] > 0.0:
            BuyBuffer[bar] = MathMax(UpSarBuffer[bar], DnSarBuffer[bar])
        if DnSarBuffer[bar - 1] > 0.0 and UpSarBuffer[bar] > 0.0:
            SellBuffer[bar] = MathMax(UpSarBuffer[bar], DnSarBuffer[bar])
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorx2maParabolic(_MQL5Indicator):
    name = 'colorx2ma-parabolic'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Method of averaging of the first smoothing
        'Length1': 12,  # first smoothing depth
        'Phase1': 15,  # First smoothing parameter,
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # method of averaging of the second smoothing
        'Length2': 5,  # second smoothing depth
        'Phase2': 15,  # Second smoothing parameter,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # price constant
        'StepH_': 0.2,  # Step for high points
        'MaximumH': 0.5,  # Maximum for high points
        'StepL_': 0.02,  # Step for low points
        'MaximumL': 0.05,  # Maximum for low points
    }

