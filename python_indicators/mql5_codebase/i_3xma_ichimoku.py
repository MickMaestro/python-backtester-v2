"""3xma_ichimoku — converted from MQL5: MQL5 Indicators/3XMA_Iсhimoku/3xma_ichimoku.mq5

3Ichimoku XMA
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 7}, 'colors': {1: [16711680], 2: [65280, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Ichimoku Cloud'}, 'levels': [], 'description': ['3Ichimoku XMA'], 'name': '3xma_ichimoku', 'source': 'MQL5 Indicators/3XMA_Iсhimoku/3xma_ichimoku.mq5', 'folder': '3XMA_Iсhimoku', 'inputs': [{'mql': 'Up_period1', 'py': 'Up_period1', 'param': 'Up_period1', 'type': 'uint', 'default': 3, 'label': 'Period 1 for the highest prices calculation', 'sinput': False}, {'mql': 'Dn_period1', 'py': 'Dn_period1', 'param': 'Dn_period1', 'type': 'uint', 'default': 3, 'label': 'Period 1 for the lowest prices calculation', 'sinput': False}, {'mql': 'Up_period2', 'py': 'Up_period2', 'param': 'Up_period2', 'type': 'uint', 'default': 6, 'label': 'Period 2 for the highest prices calculation', 'sinput': False}, {'mql': 'Dn_period2', 'py': 'Dn_period2', 'param': 'Dn_period2', 'type': 'uint', 'default': 6, 'label': 'Period 2 for the lowest prices calculation', 'sinput': False}, {'mql': 'Up_period3', 'py': 'Up_period3', 'param': 'Up_period3', 'type': 'uint', 'default': 9, 'label': 'Period 3 for the highest prices calculation', 'sinput': False}, {'mql': 'Dn_period3', 'py': 'Dn_period3', 'param': 'Dn_period3', 'type': 'uint', 'default': 9, 'label': 'Period 3 for the lowest prices calculation', 'sinput': False}, {'mql': 'Up_mode1', 'py': 'Up_mode1', 'param': 'Up_mode1', 'type': 'int', 'default': 2, 'label': 'Price type 1 for searching for highs', 'sinput': False}, {'mql': 'Dn_mode1', 'py': 'Dn_mode1', 'param': 'Dn_mode1', 'type': 'int', 'default': 1, 'label': 'Price type 1 for searching for lows', 'sinput': False}, {'mql': 'Up_mode2', 'py': 'Up_mode2', 'param': 'Up_mode2', 'type': 'int', 'default': 2, 'label': 'Price type 2 for searching for highs', 'sinput': False}, {'mql': 'Dn_mode2', 'py': 'Dn_mode2', 'param': 'Dn_mode2', 'type': 'int', 'default': 1, 'label': 'Price type 2 for searching for lows', 'sinput': False}, {'mql': 'Up_mode3', 'py': 'Up_mode3', 'param': 'Up_mode3', 'type': 'int', 'default': 2, 'label': 'Price type 3 for searching for highs', 'sinput': False}, {'mql': 'Dn_mode3', 'py': 'Dn_mode3', 'param': 'Dn_mode3', 'type': 'int', 'default': 1, 'label': 'Price type 3 for searching for lows', 'sinput': False}, {'mql': 'XMA1_Method', 'py': 'XMA1_Method', 'param': 'XMA1_Method', 'type': 'int', 'default': 0, 'label': 'Smoothing method 1', 'sinput': False}, {'mql': 'XMA2_Method', 'py': 'XMA2_Method', 'param': 'XMA2_Method', 'type': 'int', 'default': 0, 'label': 'Smoothing method 2', 'sinput': False}, {'mql': 'XMA3_Method', 'py': 'XMA3_Method', 'param': 'XMA3_Method', 'type': 'int', 'default': 0, 'label': 'Smoothing method 3', 'sinput': False}, {'mql': 'XLength1', 'py': 'XLength1', 'param': 'XLength1', 'type': 'int', 'default': 8, 'label': 'Smoothing depth 1', 'sinput': False}, {'mql': 'XLength2', 'py': 'XLength2', 'param': 'XLength2', 'type': 'int', 'default': 25, 'label': 'Smoothing depth 2', 'sinput': False}, {'mql': 'XLength3', 'py': 'XLength3', 'param': 'XLength3', 'type': 'int', 'default': 80, 'label': 'Smoothing depth 3', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'Shift1', 'py': 'Shift1', 'param': 'Shift1', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator 1 in bars', 'sinput': False}, {'mql': 'Shift2', 'py': 'Shift2', 'param': 'Shift2', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator 2 in bars', 'sinput': False}, {'mql': 'Shift3', 'py': 'Shift3', 'param': 'Shift3', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator 3 in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum MODE_PRICE
OPEN = 0
LOW = 1
HIGH = 2
CLOSE = 3
_enum('MODE_PRICE', {0: 'OPEN', 1: 'LOW', 2: 'HIGH', 3: 'CLOSE'})

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
Up_period1 = _input('Up_period1', 3)  # Period 1 for the highest prices calculation
Dn_period1 = _input('Dn_period1', 3)  # Period 1 for the lowest prices calculation
Up_period2 = _input('Up_period2', 6)  # Period 2 for the highest prices calculation
Dn_period2 = _input('Dn_period2', 6)  # Period 2 for the lowest prices calculation
Up_period3 = _input('Up_period3', 9)  # Period 3 for the highest prices calculation
Dn_period3 = _input('Dn_period3', 9)  # Period 3 for the lowest prices calculation
Up_mode1 = _input('Up_mode1', HIGH)  # Price type 1 for searching for highs
Dn_mode1 = _input('Dn_mode1', LOW)  # Price type 1 for searching for lows
Up_mode2 = _input('Up_mode2', HIGH)  # Price type 2 for searching for highs
Dn_mode2 = _input('Dn_mode2', LOW)  # Price type 2 for searching for lows
Up_mode3 = _input('Up_mode3', HIGH)  # Price type 3 for searching for highs
Dn_mode3 = _input('Dn_mode3', LOW)  # Price type 3 for searching for lows
XMA1_Method = _input('XMA1_Method', MODE_SMA)  # Smoothing method 1
XMA2_Method = _input('XMA2_Method', MODE_SMA)  # Smoothing method 2
XMA3_Method = _input('XMA3_Method', MODE_SMA)  # Smoothing method 3
XLength1 = _input('XLength1', 8)  # Smoothing depth 1
XLength2 = _input('XLength2', 25)  # Smoothing depth 2
XLength3 = _input('XLength3', 80)  # Smoothing depth 3
XPhase = _input('XPhase', 15)  # Smoothing parameter
Shift1 = _input('Shift1', 0)  # Horizontal shift of the indicator 1 in bars
Shift2 = _input('Shift2', 0)  # Horizontal shift of the indicator 2 in bars
Shift3 = _input('Shift3', 0)  # Horizontal shift of the indicator 3 in bars
XMA1 = Arr(0, 0.0)
XMA2 = Arr(0, 0.0)
XMA3 = Arr(0, 0.0)
StartBars = 0
XMA1_Handle = 0
XMA2_Handle = 0
XMA3_Handle = 0

def OnInit():
    global StartBars, XMA1_Handle, XMA2_Handle, XMA3_Handle
    XMA = CXMA()
    StartBars1 = _int(MathMax(Up_period1, Dn_period1))
    StartBars1 += XMA.GetStartBars(XMA1_Method, XLength1, XPhase)
    StartBars2 = _int(MathMax(Up_period2, Dn_period2))
    StartBars1 += XMA.GetStartBars(XMA2_Method, XLength2, XPhase)
    StartBars3 = _int(MathMax(Up_period3, Dn_period3))
    StartBars3 += XMA.GetStartBars(XMA3_Method, XLength3, XPhase)
    StartBars = MathMax(StartBars1, MathMax(StartBars2, StartBars))
    XMA1_Handle = iCustom(Symbol(), PERIOD_CURRENT, 'XMA_Ichimoku', Up_period1, Dn_period1, Up_mode1, Dn_mode1, XMA1_Method, XLength1, XPhase, Shift1, 0)
    if XMA1_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the XMA_Ichimoku 1 indicator')
        return 1
    XMA2_Handle = iCustom(Symbol(), PERIOD_CURRENT, 'XMA_Ichimoku', Up_period2, Dn_period2, Up_mode2, Dn_mode2, XMA2_Method, XLength2, XPhase, Shift2, 0)
    if XMA2_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the XMA_Ichimoku 2 indicator')
        return 1
    XMA3_Handle = iCustom(Symbol(), PERIOD_CURRENT, 'XMA_Ichimoku', Up_period3, Dn_period3, Up_mode3, Dn_mode3, XMA3_Method, XLength3, XPhase, Shift3, 0)
    if XMA3_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the XMA_Ichimoku 3 indicator')
        return 1
    SetIndexBuffer(0, XMA1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(XMA1, True)
    SetIndexBuffer(1, XMA2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift2)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(XMA2, True)
    SetIndexBuffer(2, XMA3, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift3)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(XMA3, True)
    shortname = '3 Ichimoku XMA'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((BarsCalculated(XMA1_Handle) < rates_total or BarsCalculated(XMA2_Handle) < rates_total) or BarsCalculated(XMA3_Handle) < rates_total) or StartBars > rates_total:
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total - 1
    else:
        to_copy = rates_total - prev_calculated + 1
    if CopyBuffer(XMA1_Handle, 0, 0, to_copy, XMA1) <= 0:
        return 0
    if CopyBuffer(XMA2_Handle, 0, 0, to_copy, XMA2) <= 0:
        return 0
    if CopyBuffer(XMA3_Handle, 0, 0, to_copy, XMA3) <= 0:
        return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ind3xmaIchimoku(_MQL5Indicator):
    name = '3xma_ichimoku'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Up_period1': 3,  # Period 1 for the highest prices calculation
        'Dn_period1': 3,  # Period 1 for the lowest prices calculation
        'Up_period2': 6,  # Period 2 for the highest prices calculation
        'Dn_period2': 6,  # Period 2 for the lowest prices calculation
        'Up_period3': 9,  # Period 3 for the highest prices calculation
        'Dn_period3': 9,  # Period 3 for the lowest prices calculation
        'Up_mode1': _Choice({0: 'by open prices', 1: 'by lows', 2: 'by highs', 3: 'by close prices'}, default=2),  # Price type 1 for searching for highs
        'Dn_mode1': _Choice({0: 'by open prices', 1: 'by lows', 2: 'by highs', 3: 'by close prices'}, default=1),  # Price type 1 for searching for lows
        'Up_mode2': _Choice({0: 'by open prices', 1: 'by lows', 2: 'by highs', 3: 'by close prices'}, default=2),  # Price type 2 for searching for highs
        'Dn_mode2': _Choice({0: 'by open prices', 1: 'by lows', 2: 'by highs', 3: 'by close prices'}, default=1),  # Price type 2 for searching for lows
        'Up_mode3': _Choice({0: 'by open prices', 1: 'by lows', 2: 'by highs', 3: 'by close prices'}, default=2),  # Price type 3 for searching for highs
        'Dn_mode3': _Choice({0: 'by open prices', 1: 'by lows', 2: 'by highs', 3: 'by close prices'}, default=1),  # Price type 3 for searching for lows
        'XMA1_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Smoothing method 1
        'XMA2_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Smoothing method 2
        'XMA3_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Smoothing method 3
        'XLength1': 8,  # Smoothing depth 1
        'XLength2': 25,  # Smoothing depth 2
        'XLength3': 80,  # Smoothing depth 3
        'XPhase': 15,  # Smoothing parameter
        'Shift1': 0,  # Horizontal shift of the indicator 1 in bars
        'Shift2': 0,  # Horizontal shift of the indicator 2 in bars
        'Shift3': 0,  # Horizontal shift of the indicator 3 in bars
    }

