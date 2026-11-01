"""2xma — converted from MQL5: MQL5 Indicators/2XMA/2xma.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [128, 9125192], 2: [55295], 3: [13422920]}, 'widths': {2: 1, 3: 1}, 'styles': {2: 0, 3: 0}, 'labels': {1: 'Lower XMACD', 2: 'Fast Signal Line', 3: 'Slow Signal Line'}, 'levels': [], 'description': [], 'name': '2xma', 'source': 'MQL5 Indicators/2XMA/2xma.mq5', 'folder': '2XMA', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 3, 'label': 'method of averaging of the fast XMA', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'uint', 'default': 28, 'label': 'fast XMA period', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'fast XMA parameter,', 'sinput': False}, {'mql': 'IPC1', 'py': 'IPC1', 'param': 'IPC1', 'type': 'int', 'default': 1, 'label': 'fast XMA price constant', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 3, 'label': 'method of averaging of the slow XMA', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'uint', 'default': 144, 'label': 'slow XMA period', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 15, 'label': 'slow XMA parameter,', 'sinput': False}, {'mql': 'IPC2', 'py': 'IPC2', 'param': 'IPC2', 'type': 'int', 'default': 1, 'label': 'slow XMA price constant', 'sinput': False}, {'mql': 'MA_Method3', 'py': 'MA_Method3', 'param': 'MA_Method3', 'type': 'int', 'default': 0, 'label': 'method of averaging of the fast signal line', 'sinput': False}, {'mql': 'Length3', 'py': 'Length3', 'param': 'Length3', 'type': 'uint', 'default': 14, 'label': 'fast signal line period', 'sinput': False}, {'mql': 'Phase3', 'py': 'Phase3', 'param': 'Phase3', 'type': 'int', 'default': 15, 'label': 'fast signal line parameter,', 'sinput': False}, {'mql': 'MA_Method4', 'py': 'MA_Method4', 'param': 'MA_Method4', 'type': 'int', 'default': 0, 'label': 'method of averaging of the slow signal line', 'sinput': False}, {'mql': 'Length4', 'py': 'Length4', 'param': 'Length4', 'type': 'uint', 'default': 70, 'label': 'slow signal line period', 'sinput': False}, {'mql': 'Phase4', 'py': 'Phase4', 'param': 'Phase4', 'type': 'int', 'default': 15, 'label': 'slow signal line parameter,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'vertical shift of the indicator in pointsх', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
MA_Method1 = _input('MA_Method1', MODE_LWMA)  # method of averaging of the fast XMA
Length1 = _input('Length1', 28)  # fast XMA period
Phase1 = _input('Phase1', 15)  # fast XMA parameter,
IPC1 = _input('IPC1', PRICE_CLOSE)  # fast XMA price constant
MA_Method2 = _input('MA_Method2', MODE_LWMA)  # method of averaging of the slow XMA
Length2 = _input('Length2', 144)  # slow XMA period
Phase2 = _input('Phase2', 15)  # slow XMA parameter,
IPC2 = _input('IPC2', PRICE_CLOSE)  # slow XMA price constant
MA_Method3 = _input('MA_Method3', MODE_SMA)  # method of averaging of the fast signal line
Length3 = _input('Length3', 14)  # fast signal line period
Phase3 = _input('Phase3', 15)  # fast signal line parameter,
MA_Method4 = _input('MA_Method4', MODE_SMA)  # method of averaging of the slow signal line
Length4 = _input('Length4', 70)  # slow signal line period
Phase4 = _input('Phase4', 15)  # slow signal line parameter,
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # vertical shift of the indicator in pointsх
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
FastSignBuffer = Arr(0, 0.0)
SlowSignBuffer = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_xmacd = 0
min_rates_total = 0

def OnInit():
    global dPriceShift, min_rates_total, min_rates_xmacd
    min_rates_fast1 = XMA1.GetStartBars(MA_Method1, Length1, Phase1)
    min_rates_slow1 = XMA2.GetStartBars(MA_Method2, Length2, Phase2)
    min_rates_fast2 = XMA3.GetStartBars(MA_Method3, Length3, Phase3)
    min_rates_slow2 = XMA4.GetStartBars(MA_Method4, Length4, Phase4)
    min_rates_xmacd = MathMax(min_rates_fast1, min_rates_slow1)
    min_rates_total = min_rates_xmacd + MathMax(min_rates_fast2, min_rates_slow2)
    XMA1.XMALengthCheck('Length1', Length1)
    XMA2.XMALengthCheck('Length2', Length2)
    XMA3.XMALengthCheck('Length3', Length3)
    XMA4.XMALengthCheck('Length4', Length4)
    XMA1.XMAPhaseCheck('Phase1', Phase1, MA_Method1)
    XMA2.XMAPhaseCheck('Phase2', Phase2, MA_Method2)
    XMA3.XMAPhaseCheck('Phase3', Phase3, MA_Method3)
    XMA4.XMAPhaseCheck('Phase4', Phase4, MA_Method4)
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, DnBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, FastSignBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, SlowSignBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = '2XMA'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    fastxma = 0.0
    slowxma = 0.0
    fastsignal = 0.0
    slowsignal = 0.0
    fprice = 0.0
    sprice = 0.0
    xmacd = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        fprice = PriceSeries(IPC1, bar, open, low, high, close)
        sprice = PriceSeries(IPC2, bar, open, low, high, close)
        fastxma = XMA1.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, fprice, bar, False)
        slowxma = XMA2.XMASeries(0, prev_calculated, rates_total, MA_Method2, Phase2, Length2, sprice, bar, False)
        UpBuffer[bar] = NormalizeDouble(fastxma + dPriceShift, Digits())
        DnBuffer[bar] = NormalizeDouble(slowxma + dPriceShift, Digits())
        xmacd = fastxma - slowxma
        fastsignal = XMA3.XMASeries(min_rates_xmacd, prev_calculated, rates_total, MA_Method3, Phase3, Length3, xmacd, bar, False)
        slowsignal = XMA4.XMASeries(min_rates_xmacd, prev_calculated, rates_total, MA_Method4, Phase4, Length4, xmacd, bar, False)
        FastSignBuffer[bar] = NormalizeDouble(slowxma + fastsignal + dPriceShift, Digits())
        SlowSignBuffer[bar] = NormalizeDouble(slowxma + slowsignal + dPriceShift, Digits())
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()
XMA3 = _alloc(CXMA)
XMA3.__init__()
XMA4 = _alloc(CXMA)
XMA4.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ind2xma(_MQL5Indicator):
    name = '2xma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # method of averaging of the fast XMA
        'Length1': 28,  # fast XMA period
        'Phase1': 15,  # fast XMA parameter,
        'IPC1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # fast XMA price constant
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # method of averaging of the slow XMA
        'Length2': 144,  # slow XMA period
        'Phase2': 15,  # slow XMA parameter,
        'IPC2': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # slow XMA price constant
        'MA_Method3': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # method of averaging of the fast signal line
        'Length3': 14,  # fast signal line period
        'Phase3': 15,  # fast signal line parameter,
        'MA_Method4': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # method of averaging of the slow signal line
        'Length4': 70,  # slow signal line period
        'Phase4': 15,  # slow signal line parameter,
        'Shift': 0,  # horizontal shift of the indicator in bars
        'PriceShift': 0,  # vertical shift of the indicator in pointsх
    }

