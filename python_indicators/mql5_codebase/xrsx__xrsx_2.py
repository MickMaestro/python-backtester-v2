"""xrsx_ — converted from MQL5: MQL5 Indicators/XRSX/xrsx_.mq5

Relative Strength Index
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [36095]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'XRSX'}, 'levels': [70.0, 30.0], 'description': ['Relative Strength Index'], 'name': 'xrsx_', 'source': 'MQL5 Indicators/XRSX/xrsx_.mq5', 'folder': 'XRSX', 'inputs': [{'mql': 'DSmoothMethod', 'py': 'DSmoothMethod', 'param': 'DSmoothMethod', 'type': 'int', 'default': 5, 'label': 'Price smoothing method', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'int', 'default': 15, 'label': 'Moving average period', 'sinput': False}, {'mql': 'DPhase', 'py': 'DPhase', 'param': 'DPhase', 'type': 'int', 'default': 100, 'label': 'Moving average smoothing parameter', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
DSmoothMethod = _input('DSmoothMethod', MODE_JurX)  # Price smoothing method
DPeriod = _input('DPeriod', 15)  # Moving average period
DPhase = _input('DPhase', 100)  # Moving average smoothing parameter
IPC = _input('IPC', PRICE_CLOSE)  # Price constant
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
XRSX = Arr(0, 0.0)
StartBars = 0

def OnInit():
    global StartBars
    StartBars = UPXRSX.GetStartBars(DSmoothMethod, DPeriod, DPhase)
    UPXRSX.XMALengthCheck('DPeriod', DPeriod)
    UPXRSX.XMAPhaseCheck('DPhase', DPhase, DSmoothMethod)
    SetIndexBuffer(0, XRSX, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(0, PLOT_LABEL, 'XRSX')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    Smooth = ""
    Smooth = UPXRSX.GetString_MA_Method(DSmoothMethod)
    StringConcatenate(shortname, 'Relative Strength Index(', _str(DPeriod), ',', Smooth, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBars:
        return 0
    dprice_ = 0.0
    absdprice_ = 0.0
    up_xrsx = 0.0
    dn_xrsx = 0.0
    xrsx = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        dprice_ = PriceSeries(IPC, bar, open, low, high, close) - PriceSeries(IPC, bar - 1, open, low, high, close)
        absdprice_ = MathAbs(dprice_)
        up_xrsx = UPXRSX.XMASeries(1, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, dprice_, bar, False)
        dn_xrsx = DNXRSX.XMASeries(1, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, absdprice_, bar, False)
        if dn_xrsx == 0:
            xrsx = EMPTY_VALUE
        else:
            xrsx = _fdiv(up_xrsx, dn_xrsx)
            if xrsx > 1:
                xrsx = 1.0
            if xrsx < -1:
                xrsx = -1.0
        XRSX[bar] = (xrsx * 50) + 50
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
UPXRSX = _alloc(CXMA)
UPXRSX.__init__()
DNXRSX = _alloc(CXMA)
DNXRSX.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Xrsx(_MQL5Indicator):
    name = 'xrsx_'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'DSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=5),  # Price smoothing method
        'DPeriod': 15,  # Moving average period
        'DPhase': 100,  # Moving average smoothing parameter
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Price constant
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

