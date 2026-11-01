"""xrsx_bb_htf — converted from MQL5: MQL5 Indicators/XRSX_BB_HTF/xrsx_bb_htf.mq5

Relative Strength Index
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 7}, 'types': {1: 10, 2: 8, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'colors': {1: [8421504, 65280, 16711680, 255, 16711935], 2: [8421504, 8421376, 9639167], 3: [16711680], 4: [255], 5: [8421504], 6: [255], 7: [16711680]}, 'widths': {1: 5, 2: 5, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'styles': {1: 0, 2: 0, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4}, 'labels': {1: 'XRSX HTF', 2: 'Signal line', 3: '+2Sigma', 4: '+Sigma', 5: 'Middle', 6: '-Sigma', 7: '-2Sigma'}, 'levels': [], 'description': ['Relative Strength Index'], 'name': 'xrsx_bb_htf', 'source': 'MQL5 Indicators/XRSX_BB_HTF/xrsx_bb_htf.mq5', 'folder': 'XRSX_BB_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Chart period', 'sinput': False}, {'mql': 'DSmoothMethod', 'py': 'DSmoothMethod', 'param': 'DSmoothMethod', 'type': 'int', 'default': 5, 'label': 'Price smoothing method', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'int', 'default': 15, 'label': 'Moving average period', 'sinput': False}, {'mql': 'DPhase', 'py': 'DPhase', 'param': 'DPhase', 'type': 'int', 'default': 100, 'label': 'Moving average smoothing parameter', 'sinput': False}, {'mql': 'SSmoothMethod', 'py': 'SSmoothMethod', 'param': 'SSmoothMethod', 'type': 'int', 'default': 4, 'label': 'Signal line smoothing method', 'sinput': False}, {'mql': 'SPeriod', 'py': 'SPeriod', 'param': 'SPeriod', 'type': 'int', 'default': 7, 'label': 'Signal line period', 'sinput': False}, {'mql': 'SPhase', 'py': 'SPhase', 'param': 'SPhase', 'type': 'int', 'default': 100, 'label': 'Signal line parameter', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'BBPeriod', 'py': 'BBPeriod', 'param': 'BBPeriod', 'type': 'int', 'default': 100, 'label': 'Bollinger bands period', 'sinput': False}, {'mql': 'BBDeviation1', 'py': 'BBDeviation1', 'param': 'BBDeviation1', 'type': 'double', 'default': 1.0, 'label': 'Small deviation', 'sinput': False}, {'mql': 'BBDeviation2', 'py': 'BBDeviation2', 'param': 'BBDeviation2', 'type': 'double', 'default': 1.6, 'label': 'Big deviation', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Chart period
DSmoothMethod = _input('DSmoothMethod', MODE_JurX)  # Price smoothing method
DPeriod = _input('DPeriod', 15)  # Moving average period
DPhase = _input('DPhase', 100)  # Moving average smoothing parameter
SSmoothMethod = _input('SSmoothMethod', MODE_JJMA)  # Signal line smoothing method
SPeriod = _input('SPeriod', 7)  # Signal line period
SPhase = _input('SPhase', 100)  # Signal line parameter
IPC = _input('IPC', PRICE_CLOSE)  # Price constant
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
BBPeriod = _input('BBPeriod', 100)  # Bollinger bands period
BBDeviation1 = _input('BBDeviation1', 1.0)  # Small deviation
BBDeviation2 = _input('BBDeviation2', 1.6)  # Big deviation
XRSX = Arr(0, 0.0)
XXRSX = Arr(0, 0.0)
ColorXRSX = Arr(0, 0.0)
ColorXXRSX = Arr(0, 0.0)
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
ExtLineBuffer4 = Arr(0, 0.0)
ExtLineBuffer5 = Arr(0, 0.0)
quotient = 0.0
Init = False
min_rates_total = 0
XRSX_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Init, XRSX_Handle, min_rates_total, quotient
    min_rates_total = 3
    Init = True
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('XRSX_BB indicator chart period cannot be less than the current chart period')
        Init = False
        return INIT_FAILED
    XRSX_Handle = iCustom(Symbol(), TimeFrame, 'XRSX_BB', DSmoothMethod, DPeriod, DPhase, SSmoothMethod, SPeriod, SPhase, IPC, 0, 1, BBPeriod, BBDeviation1, BBDeviation2)
    if XRSX_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the XRSX_BB indicator')
        Init = False
        return INIT_FAILED
    quotient = BBDeviation2 / BBDeviation1
    SetIndexBuffer(0, XRSX, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(XRSX, True)
    SetIndexBuffer(1, ColorXRSX, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ColorXRSX, True)
    SetIndexBuffer(2, XXRSX, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(XXRSX, True)
    SetIndexBuffer(3, ColorXXRSX, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ColorXXRSX, True)
    SetIndexBuffer(4, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(5, ExtLineBuffer2, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLineBuffer3, INDICATOR_DATA)
    SetIndexBuffer(7, ExtLineBuffer4, INDICATOR_DATA)
    SetIndexBuffer(8, ExtLineBuffer5, INDICATOR_DATA)
    ArraySetAsSeries(ExtLineBuffer1, True)
    ArraySetAsSeries(ExtLineBuffer2, True)
    ArraySetAsSeries(ExtLineBuffer3, True)
    ArraySetAsSeries(ExtLineBuffer4, True)
    ArraySetAsSeries(ExtLineBuffer5, True)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(7, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(8, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(7, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(8, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    Smooth = ""
    Smooth = XMA.GetString_MA_Method(DSmoothMethod)
    StringConcatenate(shortname, 'Relative Strength Index(', GetStringTimeframe(TimeFrame), ', ', _str(DPeriod), ',', Smooth, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total or (not Init):
        return 0
    if BarsCalculated(XRSX_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    limit = 0
    bar = 0
    Xrsx = Arr(2, 0.0, dyn=False)
    Xxrsx = Arr(2, 0.0, dyn=False)
    BB2 = Arr(1, 0.0, dyn=False)
    BB3 = Arr(1, 0.0, dyn=False)
    XRSXTime = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        XRSX[bar] = EMPTY_VALUE
        XXRSX[bar] = EMPTY_VALUE
        ColorXRSX[bar] = 0.0
        ColorXXRSX[bar] = 0.0
        ExtLineBuffer1[bar] = EMPTY_VALUE
        ExtLineBuffer2[bar] = EMPTY_VALUE
        ExtLineBuffer3[bar] = EMPTY_VALUE
        ExtLineBuffer4[bar] = EMPTY_VALUE
        ExtLineBuffer5[bar] = EMPTY_VALUE
        if CopyTime(Symbol(), TimeFrame, _DT(time[bar]), 1, XRSXTime) <= 0:
            return 0
        if time[bar] >= XRSXTime[0] and time[bar + 1] < XRSXTime[0]:
            _s_OnCalculate_LastCountBar = bar
            if CopyBuffer(XRSX_Handle, 0, _DT(time[bar]), 2, Xrsx) <= 0:
                return 0
            if CopyBuffer(XRSX_Handle, 2, _DT(time[bar]), 2, Xxrsx) <= 0:
                return 0
            if CopyBuffer(XRSX_Handle, 5, _DT(time[bar]), 1, BB2) <= 0:
                return 0
            if CopyBuffer(XRSX_Handle, 6, _DT(time[bar]), 1, BB3) <= 0:
                return 0
            XRSX[bar] = Xrsx[1]
            XXRSX[bar] = Xxrsx[1]
            ExtLineBuffer2[bar] = BB2[0]
            ExtLineBuffer3[bar] = BB3[0]
            dBB = BB2[0] - BB3[0]
            ExtLineBuffer1[bar] = BB3[0] + (dBB * quotient)
            ExtLineBuffer4[bar] = BB3[0] - dBB
            ExtLineBuffer5[bar] = BB3[0] - (dBB * quotient)
            if XRSX[bar] > 0:
                if Xrsx[1] > Xrsx[0]:
                    ColorXRSX[bar] = 1.0
                if Xrsx[1] < Xrsx[0]:
                    ColorXRSX[bar] = 2.0
            if XRSX[bar] < 0:
                if Xrsx[1] < Xrsx[0]:
                    ColorXRSX[bar] = 3.0
                if Xrsx[1] > Xrsx[0]:
                    ColorXRSX[bar] = 4.0
            if XRSX[bar] > XXRSX[bar]:
                ColorXXRSX[bar] = 1.0
            if XRSX[bar] < XXRSX[bar]:
                ColorXXRSX[bar] = 2.0
        if XRSX[bar + 1] != EMPTY_VALUE and XRSX[bar] == EMPTY_VALUE:
            XRSX[bar] = XRSX[bar + 1]
            ColorXRSX[bar] = ColorXRSX[bar + 1]
            XXRSX[bar] = XXRSX[bar + 1]
            ColorXXRSX[bar] = ColorXXRSX[bar + 1]
            ExtLineBuffer1[bar] = ExtLineBuffer1[bar + 1]
            ExtLineBuffer2[bar] = ExtLineBuffer2[bar + 1]
            ExtLineBuffer3[bar] = ExtLineBuffer3[bar + 1]
            ExtLineBuffer4[bar] = ExtLineBuffer4[bar + 1]
            ExtLineBuffer5[bar] = ExtLineBuffer5[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA = _alloc(CXMA)
XMA.__init__()

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XrsxBbHtf(_MQL5Indicator):
    name = 'xrsx_bb_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Chart period
        'DSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=5),  # Price smoothing method
        'DPeriod': 15,  # Moving average period
        'DPhase': 100,  # Moving average smoothing parameter
        'SSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Signal line smoothing method
        'SPeriod': 7,  # Signal line period
        'SPhase': 100,  # Signal line parameter
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Price constant
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'BBPeriod': 100,  # Bollinger bands period
        'BBDeviation1': 1.0,  # Small deviation
        'BBDeviation2': 1.6,  # Big deviation
    }

