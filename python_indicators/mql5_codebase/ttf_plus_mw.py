"""ttf_plus_mw — converted from MQL5: MQL5 Indicators/TTF_Plus_MW/ttf_plus_mw.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711680], 2: [8721863]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Upper TTF_Plus_MW', 2: 'Lower TTF_Plus_MW'}, 'levels': [], 'description': [], 'name': 'ttf_plus_mw', 'source': 'MQL5 Indicators/TTF_Plus_MW/ttf_plus_mw.mq5', 'folder': 'TTF_Plus_MW', 'inputs': [{'mql': 'TTFbars', 'py': 'TTFbars', 'param': 'TTFbars', 'type': 'uint', 'default': 6, 'label': 'Extrema finding period', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 7, 'label': 'Method of averaging', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 12, 'label': 'Smoothing depth', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
TTFbars = _input('TTFbars', 6)  # Extrema finding period
XMA_Method = _input('XMA_Method', MODE_T3)  # Method of averaging
XLength = _input('XLength', 12)  # Smoothing depth
XPhase = _input('XPhase', 15)  # Smoothing parameter
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
ExtMapBufferUp = Arr(0, 0.0)
ExtMapBufferDown = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0
min_rates_ = 0

def OnInit():
    global ATR_Handle, min_rates_, min_rates_total
    ATRPeriod = 15
    ATR_Handle = iATR(None, 0, ATRPeriod)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
        return INIT_FAILED
    min_rates_ = _int(TTFbars + 1)
    min_rates_total = MathMax(XMA1.GetStartBars(XMA_Method, XLength, XPhase) + min_rates_, ATRPeriod)
    SetIndexBuffer(0, ExtMapBufferUp, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferUp, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ExtMapBufferDown, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferDown, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    Smooth = XMA1.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'TTF_Plus_MW(', TTFbars, ', ', Smooth, ', ', XLength, XPhase, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    ATR = Arr(0, 0.0)
    HighestHighRecent = 0.0
    HighestHighOlder = 0.0
    LowestLowRecent = 0.0
    LowestLowOlder = 0.0
    BuyPower = 0.0
    SellPower = 0.0
    res = 0.0
    TTF = 0.0
    limit = 0
    to_copy = 0
    bar = 0
    maxbar = 0
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_ - 1
    else:
        limit = rates_total - prev_calculated
    maxbar = rates_total - min_rates_ - 1
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtMapBufferUp[bar] = EMPTY_VALUE
        ExtMapBufferDown[bar] = EMPTY_VALUE
        HighestHighRecent = high[ArrayMaximum(high, bar + TTFbars + 1, TTFbars)]
        HighestHighOlder = high[ArrayMaximum(high, bar + 1, TTFbars)]
        LowestLowRecent = low[ArrayMinimum(low, bar + TTFbars + 1, TTFbars)]
        LowestLowOlder = low[ArrayMinimum(low, bar + 1, TTFbars)]
        BuyPower = HighestHighRecent - LowestLowOlder
        SellPower = HighestHighOlder - LowestLowRecent
        res = 0.5 * (BuyPower + SellPower)
        if res:
            TTF = _fdiv(100 * (BuyPower - SellPower), res)
        else:
            TTF = EMPTY_VALUE
        TTF = XMA1.XMASeries(maxbar, prev_calculated, rates_total, XMA_Method, XPhase, XLength, TTF, bar, True)
        if TTF <= -100:
            ExtMapBufferDown[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        if TTF >= 100:
            ExtMapBufferUp[bar] = low[bar] - ((ATR[bar] * 3) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TtfPlusMw(_MQL5Indicator):
    name = 'ttf_plus_mw'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TTFbars': 6,  # Extrema finding period
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # Method of averaging
        'XLength': 12,  # Smoothing depth
        'XPhase': 15,  # Smoothing parameter
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

