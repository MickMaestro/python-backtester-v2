"""colorxmacd_htf — converted from MQL5: MQL5 Indicators/XMACD_HTF/colorxmacd_htf.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 10, 2: 12}, 'colors': {1: [8421504, 8421376, 14822282, 6053069, 16711935], 2: [8421504, 65280, 255]}, 'widths': {1: 5, 2: 5}, 'styles': {1: 0}, 'labels': {1: 'XMACD HTF', 2: 'Signal Line'}, 'levels': [], 'description': [], 'name': 'colorxmacd_htf', 'source': 'MQL5 Indicators/XMACD_HTF/colorxmacd_htf.mq5', 'folder': 'XMACD_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Chart period', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 7, 'label': 'histogram smoothing method', 'sinput': False}, {'mql': 'Fast_XMA', 'py': 'Fast_XMA', 'param': 'Fast_XMA', 'type': 'int', 'default': 12, 'label': '/Fast moving average period', 'sinput': False}, {'mql': 'Slow_XMA', 'py': 'Slow_XMA', 'param': 'Slow_XMA', 'type': 'int', 'default': 26, 'label': 'Slow moving average period', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 100, 'label': 'moving averages smoothing parameter,', 'sinput': False}, {'mql': 'Signal_Method', 'py': 'Signal_Method', 'param': 'Signal_Method', 'type': 'int', 'default': 4, 'label': 'Signal line smoothing method', 'sinput': False}, {'mql': 'Signal_XMA', 'py': 'Signal_XMA', 'param': 'Signal_XMA', 'type': 'int', 'default': 9, 'label': 'signal line period', 'sinput': False}, {'mql': 'Signal_XPhase', 'py': 'Signal_XPhase', 'param': 'Signal_XPhase', 'type': 'int', 'default': 100, 'label': 'Ssignal line parameter,', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'price constant', 'sinput': False}, {'mql': 'ReDraw', 'py': 'ReDraw', 'param': 'ReDraw', 'type': 'bool', 'default': False, 'label': 'repeat display of information in the empty bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XMA_Method = _input('XMA_Method', MODE_T3)  # histogram smoothing method
Fast_XMA = _input('Fast_XMA', 12)  # /Fast moving average period
Slow_XMA = _input('Slow_XMA', 26)  # Slow moving average period
XPhase = _input('XPhase', 100)  # moving averages smoothing parameter,
Signal_Method = _input('Signal_Method', MODE_JJMA)  # Signal line smoothing method
Signal_XMA = _input('Signal_XMA', 9)  # signal line period
Signal_XPhase = _input('Signal_XPhase', 100)  # Ssignal line parameter,
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE_)  # price constant
ReDraw = _input('ReDraw', False)  # repeat display of information in the empty bars
Init = False
min_rates_total = 0
XMACD_Handle = 0
XMACDBuffer = Arr(0, 0.0)
SignBuffer = Arr(0, 0.0)
ColorXMACDBuffer = Arr(0, 0.0)
ColorSignBuffer = Arr(0, 0.0)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Init, XMACD_Handle, min_rates_total
    min_rates_total = 3
    Init = True
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('ColorXMACD indicator chart period cannot be less than the current chart period')
        Init = False
        return
    XMACD_Handle = iCustom(Symbol(), TimeFrame, 'ColorXMACD', XMA_Method, Fast_XMA, Slow_XMA, XPhase, Signal_Method, Signal_XMA, Signal_XPhase, AppliedPrice)
    if XMACD_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ColorXMACD indicator')
        Init = False
        return
    SetIndexBuffer(0, XMACDBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(0, PLOT_LABEL, 'XMACD_HTF')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(XMACDBuffer, True)
    SetIndexBuffer(1, ColorXMACDBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ColorXMACDBuffer, True)
    SetIndexBuffer(2, SignBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(2, PLOT_LABEL, 'Signal XMA')
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(SignBuffer, True)
    SetIndexBuffer(3, ColorSignBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ColorSignBuffer, True)
    XMA = CXMA()
    Smooth1 = XMA.GetString_MA_Method(XMA_Method)
    Smooth2 = XMA.GetString_MA_Method(Signal_Method)
    shortname = Box("")
    StringConcatenate(shortname, 'XMACD HTF( ', GetStringTimeframe(TimeFrame), ', ', Fast_XMA, ', ', Slow_XMA, ', ', Signal_XMA, ', ', Smooth1, ', ', Smooth2, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total or (not Init):
        return 0
    if BarsCalculated(XMACD_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    limit = 0
    bar = 0
    XMACD = Arr(2, 0.0, dyn=False)
    SIGN = Arr(2, 0.0, dyn=False)
    XMACDTime = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        XMACDBuffer[bar] = EMPTY_VALUE
        SignBuffer[bar] = EMPTY_VALUE
        ColorXMACDBuffer[bar] = 0.0
        ColorSignBuffer[bar] = 0.0
        if CopyTime(Symbol(), TimeFrame, _DT(time[bar]), 1, XMACDTime) <= 0:
            return 0
        if time[bar] >= XMACDTime[0] and time[bar + 1] < XMACDTime[0]:
            _s_OnCalculate_LastCountBar = bar
            if CopyBuffer(XMACD_Handle, 0, _DT(time[bar]), 2, XMACD) <= 0:
                return 0
            if CopyBuffer(XMACD_Handle, 2, _DT(time[bar]), 2, SIGN) <= 0:
                return 0
            XMACDBuffer[bar] = XMACD[1]
            SignBuffer[bar] = SIGN[1]
            if XMACDBuffer[bar] > 0:
                if XMACD[1] > XMACD[0]:
                    ColorXMACDBuffer[bar] = 1.0
                if XMACD[1] < XMACD[0]:
                    ColorXMACDBuffer[bar] = 2.0
            if XMACDBuffer[bar] < 0:
                if XMACD[1] < XMACD[0]:
                    ColorXMACDBuffer[bar] = 3.0
                if XMACD[1] > XMACD[0]:
                    ColorXMACDBuffer[bar] = 4.0
            if XMACDBuffer[bar] > SignBuffer[bar]:
                ColorSignBuffer[bar] = 1.0
            if XMACDBuffer[bar] < SignBuffer[bar]:
                ColorSignBuffer[bar] = 2.0
        if ReDraw:
            if XMACDBuffer[bar + 1] != EMPTY_VALUE and XMACDBuffer[bar] == EMPTY_VALUE:
                XMACDBuffer[bar] = XMACDBuffer[bar + 1]
                ColorXMACDBuffer[bar] = ColorXMACDBuffer[bar + 1]
                SignBuffer[bar] = SignBuffer[bar + 1]
                ColorSignBuffer[bar] = ColorSignBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorxmacdHtf(_MQL5Indicator):
    name = 'colorxmacd_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Chart period
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # histogram smoothing method
        'Fast_XMA': 12,  # /Fast moving average period
        'Slow_XMA': 26,  # Slow moving average period
        'XPhase': 100,  # moving averages smoothing parameter,
        'Signal_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Signal line smoothing method
        'Signal_XMA': 9,  # signal line period
        'Signal_XPhase': 100,  # Ssignal line parameter,
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # price constant
        'ReDraw': False,  # repeat display of information in the empty bars
    }

