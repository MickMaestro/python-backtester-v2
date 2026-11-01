"""blaucmi — converted from MQL5: MQL5 Indicators/BlauCMI_Signal/blaucmi.mq5

Candle Momentum Index
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 10}, 'colors': {1: [9639167, 42495, 8421504, 3329434, 8421376]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'BlauCMI'}, 'levels': [25.0, 0.0, -25.0], 'description': ['Candle Momentum Index'], 'name': 'blaucmi', 'source': 'MQL5 Indicators/BlauCMI_Signal/blaucmi.mq5', 'folder': 'BlauCMI_Signal', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 1, 'label': 'averaging method', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 1, 'label': 'depth of Momentum averaging', 'sinput': False}, {'mql': 'XLength1', 'py': 'XLength1', 'param': 'XLength1', 'type': 'uint', 'default': 20, 'label': 'first averaging depth', 'sinput': False}, {'mql': 'XLength2', 'py': 'XLength2', 'param': 'XLength2', 'type': 'uint', 'default': 5, 'label': 'second averaging depth', 'sinput': False}, {'mql': 'XLength3', 'py': 'XLength3', 'param': 'XLength3', 'type': 'uint', 'default': 3, 'label': 'third averaging depth', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'smoothing parameter', 'sinput': False}, {'mql': 'IPC1', 'py': 'IPC1', 'param': 'IPC1', 'type': 'int', 'default': 1, 'label': 'close price constant', 'sinput': False}, {'mql': 'IPC2', 'py': 'IPC2', 'param': 'IPC2', 'type': 'int', 'default': 2, 'label': 'open price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XMA_Method = _input('XMA_Method', MODE_EMA)  # averaging method
XLength = _input('XLength', 1)  # depth of Momentum averaging
XLength1 = _input('XLength1', 20)  # first averaging depth
XLength2 = _input('XLength2', 5)  # second averaging depth
XLength3 = _input('XLength3', 3)  # third averaging depth
XPhase = _input('XPhase', 15)  # smoothing parameter
IPC1 = _input('IPC1', PRICE_CLOSE)  # close price constant
IPC2 = _input('IPC2', PRICE_OPEN)  # open price constant
Shift = _input('Shift', 0)  # Horizontal shift of the indicator
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
min_rates_3 = 0

def OnInit():
    global min_rates_1, min_rates_2, min_rates_3, min_rates_total
    min_rates_1 = _int(XLength - 1)
    min_rates_2 = min_rates_1 + XMA1.GetStartBars(XMA_Method, XLength1, XPhase)
    min_rates_3 = min_rates_2 + XMA1.GetStartBars(XMA_Method, XLength2, XPhase)
    min_rates_total = min_rates_3 + XMA1.GetStartBars(XMA_Method, XLength3, XPhase)
    if IPC1 == IPC2 and XLength == 1:
        Print('Invalid price constant values!')
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BlauCMI')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    Mom = 0.0
    XMom = 0.0
    XXMom = 0.0
    XXXMom = 0.0
    AbsMom = 0.0
    XAbsMom = 0.0
    XXAbsMom = 0.0
    XXXAbsMom = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        Mom = PriceSeries(IPC1, bar, open, low, high, close) - PriceSeries(IPC2, bar - XLength + 1, open, low, high, close)
        AbsMom = MathAbs(Mom)
        XMom = XMA1.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method, XPhase, XLength1, Mom, bar, False)
        XAbsMom = XMA2.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method, XPhase, XLength1, AbsMom, bar, False)
        XXMom = XMA3.XMASeries(min_rates_2, prev_calculated, rates_total, XMA_Method, XPhase, XLength2, XMom, bar, False)
        XXAbsMom = XMA4.XMASeries(min_rates_2, prev_calculated, rates_total, XMA_Method, XPhase, XLength2, XAbsMom, bar, False)
        XXXMom = XMA5.XMASeries(min_rates_3, prev_calculated, rates_total, XMA_Method, XPhase, XLength3, XXMom, bar, False)
        XXXAbsMom = XMA6.XMASeries(min_rates_3, prev_calculated, rates_total, XMA_Method, XPhase, XLength3, XXAbsMom, bar, False)
        if XXXAbsMom:
            IndBuffer[bar] = _fdiv(100 * XXXMom, XXXAbsMom)
        else:
            IndBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        clr = 2
        if IndBuffer[bar] > 0:
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                clr = 4
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                clr = 3
        if IndBuffer[bar] < 0:
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                clr = 0
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                clr = 1
        ColorIndBuffer[bar] = clr
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
XMA5 = _alloc(CXMA)
XMA5.__init__()
XMA6 = _alloc(CXMA)
XMA6.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Blaucmi(_MQL5Indicator):
    name = 'blaucmi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # averaging method
        'XLength': 1,  # depth of Momentum averaging
        'XLength1': 20,  # first averaging depth
        'XLength2': 5,  # second averaging depth
        'XLength3': 3,  # third averaging depth
        'XPhase': 15,  # smoothing parameter
        'IPC1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # close price constant
        'IPC2': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=2),  # open price constant
        'Shift': 0,  # Horizontal shift of the indicator
    }

