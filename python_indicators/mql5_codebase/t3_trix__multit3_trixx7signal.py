"""t3_trix — converted from MQL5: MQL5 Indicators/MultiT3_TRIXx7Signal/t3_trix.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 10}, 'colors': {1: [16776960, 15631086], 2: [255, 8388736, 8421504, 8421376, 3329330]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'T3_TRIX Signal', 2: 'T3_TRIX'}, 'levels': [], 'description': [''], 'name': 't3_trix', 'source': 'MQL5 Indicators/MultiT3_TRIXx7Signal/t3_trix.mq5', 'folder': 'MultiT3_TRIXx7Signal', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 7, 'label': 'Method of averaging', 'sinput': False}, {'mql': 'XLength1', 'py': 'XLength1', 'param': 'XLength1', 'type': 'uint', 'default': 10, 'label': 'Fast averaging depth', 'sinput': False}, {'mql': 'XLength2', 'py': 'XLength2', 'param': 'XLength2', 'type': 'uint', 'default': 18, 'label': 'Slow averaging depth', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 70, 'label': 'Smoothing factor', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XMA_Method = _input('XMA_Method', MODE_T3)  # Method of averaging
XLength1 = _input('XLength1', 10)  # Fast averaging depth
XLength2 = _input('XLength2', 18)  # Slow averaging depth
XPhase = _input('XPhase', 70)  # Smoothing factor
IPC = _input('IPC', PRICE_CLOSE)  # Price constant
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_1 = XMA1.GetStartBars(XMA_Method, XLength1, XPhase)
    min_rates_2 = XMA1.GetStartBars(XMA_Method, XLength2, XPhase)
    min_rates_total = MathMax(min_rates_1, min_rates_2)
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'T3_TRIX')
    IndicatorSetInteger(INDICATOR_DIGITS, 4)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_xfast, _s_OnCalculate_prev_xslow, _s_OnCalculate_start
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    xfast = 0.0
    xslow = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        _s_OnCalculate_start = 1
        first = _int(_s_OnCalculate_start)
        _s_OnCalculate_prev_xfast = PriceSeries(IPC, _s_OnCalculate_start - 1, open, low, high, close)
        _s_OnCalculate_prev_xslow = _s_OnCalculate_prev_xfast
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        xfast = XMA1.XMASeries(_s_OnCalculate_start, prev_calculated, rates_total, XMA_Method, XPhase, XLength1, price, bar, False)
        xslow = XMA2.XMASeries(_s_OnCalculate_start, prev_calculated, rates_total, XMA_Method, XPhase, XLength2, price, bar, False)
        if _s_OnCalculate_prev_xfast:
            IndBuffer[bar] = _fdiv(xfast - _s_OnCalculate_prev_xfast, _s_OnCalculate_prev_xfast)
        else:
            IndBuffer[bar] = 0.0
        if _s_OnCalculate_prev_xslow:
            DnBuffer[bar] = _fdiv(xslow - _s_OnCalculate_prev_xslow, _s_OnCalculate_prev_xslow)
        else:
            DnBuffer[bar] = 0.0
        UpBuffer[bar] = IndBuffer[bar]
        if bar != (rates_total - 1):
            _s_OnCalculate_prev_xfast = xfast
            _s_OnCalculate_prev_xslow = xslow
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

# ---- static local variables
_s_OnCalculate_prev_xfast = 0.0
_s_OnCalculate_prev_xslow = 0.0
_s_OnCalculate_start = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class T3Trix(_MQL5Indicator):
    name = 't3_trix'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # Method of averaging
        'XLength1': 10,  # Fast averaging depth
        'XLength2': 18,  # Slow averaging depth
        'XPhase': 70,  # Smoothing factor
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Price constant
    }

