"""Kuskus Starlight — converted from MQL5: MQL5 Indicators/Kuskus Starlight/Kuskus Starlight.mq5

Kuskus Starlight
Converted from MQL4 to MQL5.
Original MT4 Code and algorithm - https://www.mql5.com/en/code/8365
Copyright: Copyright © 2025, Marteo Cosme (simartspoako); Link: https://www.mql5.com/en/users/simartspoako; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2025, Marteo Cosme (simartspoako)', 'link': 'https://www.mql5.com/en/users/simartspoako', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {}, 'colors': {1: [16711680], 2: [255]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Kuskus Starlight', 'Converted from MQL4 to MQL5.', 'Original MT4 Code and algorithm - https://www.mql5.com/en/code/8365'], 'name': 'Kuskus Starlight', 'source': 'MQL5 Indicators/Kuskus Starlight/Kuskus Starlight.mq5', 'folder': 'Kuskus Starlight', 'inputs': [{'mql': 'RangePeriods', 'py': 'RangePeriods', 'param': 'RangePeriods', 'type': 'int', 'default': 9, 'label': 'Range periods', 'sinput': False}, {'mql': 'PriceSmoothing', 'py': 'PriceSmoothing', 'param': 'PriceSmoothing', 'type': 'double', 'default': 0.3, 'label': 'Price smoothing factor', 'sinput': False}, {'mql': 'IndexSmoothing', 'py': 'IndexSmoothing', 'param': 'IndexSmoothing', 'type': 'double', 'default': 0.9, 'label': 'Index smoothing factor', 'sinput': False}, {'mql': 'DrawType', 'py': 'DrawType', 'param': 'DrawType', 'type': 'int', 'default': 3, 'label': 'Line drawing type', 'sinput': False}, {'mql': 'DrawArrow', 'py': 'DrawArrow', 'param': 'DrawArrow', 'type': 'int', 'default': 251, 'label': 'Arrow type', 'sinput': False}, {'mql': 'DrawSize', 'py': 'DrawSize', 'param': 'DrawSize', 'type': 'int', 'default': 3, 'label': 'Line size', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enum_CustomDrawType
None_ = 0
Line = 1
Histogram = 2
StaryStaryNight = 3
_enum('enum_CustomDrawType', {0: 'None', 1: 'Line', 2: 'Histogram', 3: 'StaryStaryNight'})

# enum enum_CustomArrow
Kuskus_Classic = 251
Six_Pointed_Star = 172
Five_Pointed_Star_A = 171
Five_Pointed_Star_B = 182
Four_Pointed_Star_A = 170
Four_Pointed_Star_B = 178
Four_Pointed_Star_C = 179
Three_Pointed_Object = 169
Sunbust_A = 174
Sunbust_B = 175
Diamond_A = 117
Diamond_B = 116
Diamond_C = 119
Circle_Plain = 161
Circle_Narrow = 162
Circle_Bold = 163
Circle_Dotted = 164
Circle_Shadow_A = 166
Circle_Shadow_B = 109
Kaboom = 77
YingYang = 91
Snowflake = 84
Iron_Cross = 88
Star_David = 89
Crescent_Moon = 90
Radioactive = 62
Dotted_Object = 108
_enum('enum_CustomArrow', {251: 'Kuskus_Classic', 172: 'Six_Pointed_Star', 171: 'Five_Pointed_Star_A', 182: 'Five_Pointed_Star_B', 170: 'Four_Pointed_Star_A', 178: 'Four_Pointed_Star_B', 179: 'Four_Pointed_Star_C', 169: 'Three_Pointed_Object', 174: 'Sunbust_A', 175: 'Sunbust_B', 117: 'Diamond_A', 116: 'Diamond_B', 119: 'Diamond_C', 161: 'Circle_Plain', 162: 'Circle_Narrow', 163: 'Circle_Bold', 164: 'Circle_Dotted', 166: 'Circle_Shadow_A', 109: 'Circle_Shadow_B', 77: 'Kaboom', 91: 'YingYang', 84: 'Snowflake', 88: 'Iron_Cross', 89: 'Star_David', 90: 'Crescent_Moon', 62: 'Radioactive', 108: 'Dotted_Object'})

# ---- inputs and global variables
RangePeriods = _input('RangePeriods', 9)  # Range periods
PriceSmoothing = _input('PriceSmoothing', 0.3)  # Price smoothing factor
IndexSmoothing = _input('IndexSmoothing', 0.9)  # Index smoothing factor
DrawType = _input('DrawType', 3)  # Line drawing type
DrawArrow = _input('DrawArrow', 251)  # Arrow type
DrawSize = _input('DrawSize', 3)  # Line size
ExtMapBuffer_FisherIndex = Arr(0, 0.0)  # Smoothed Fisher index
ExtMapBuffer_Uptrend = Arr(0, 0.0)  # Uptrend values
ExtMapBuffer_Downtrend = Arr(0, 0.0)  # Downtrend values
ExtMapBuffer_PriceLocation = Arr(0, 0.0)  # Smoothed price location
DrawStart = 0  # Minimum bars to start drawing

def OnInit():
    global DrawStart
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0.0)
    SetIndexBuffer(0, ExtMapBuffer_Uptrend, INDICATOR_DATA)
    SetIndexBuffer(1, ExtMapBuffer_Downtrend, INDICATOR_DATA)
    SetIndexBuffer(2, ExtMapBuffer_FisherIndex, INDICATOR_DATA)
    SetIndexBuffer(3, ExtMapBuffer_PriceLocation, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(ExtMapBuffer_Uptrend, 1)
    ArraySetAsSeries(ExtMapBuffer_Downtrend, 1)
    ArraySetAsSeries(ExtMapBuffer_FisherIndex, 1)
    ArraySetAsSeries(ExtMapBuffer_PriceLocation, 1)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DrawType)
    PlotIndexSetInteger(0, PLOT_LINE_WIDTH, DrawSize)
    PlotIndexSetInteger(0, PLOT_ARROW, DrawArrow)
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, DrawType)
    PlotIndexSetInteger(1, PLOT_LINE_WIDTH, DrawSize)
    PlotIndexSetInteger(1, PLOT_ARROW, DrawArrow)
    IndicatorSetString(INDICATOR_SHORTNAME, StringFormat('Kuskus Starlight (rPeriods %d, pSmooth %.2f, iSmooth %.2f)', RangePeriods, PriceSmoothing, IndexSmoothing))
    DrawStart = (2 * RangePeriods) + 4
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, DrawStart)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, DrawStart)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    SetIndexBuffer(0, ExtMapBuffer_Uptrend, None)
    SetIndexBuffer(1, ExtMapBuffer_Downtrend, None)
    SetIndexBuffer(2, ExtMapBuffer_FisherIndex, None)
    SetIndexBuffer(3, ExtMapBuffer_PriceLocation, None)
    ArrayFree(ExtMapBuffer_Uptrend)
    ArrayFree(ExtMapBuffer_Downtrend)
    ArrayFree(ExtMapBuffer_FisherIndex)
    ArrayFree(ExtMapBuffer_PriceLocation)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < DrawStart:
        Print('Kuskus: Not enough bars to calculate')
        return 0
    ArraySetAsSeries(low, 1)
    ArraySetAsSeries(high, 1)
    startPos = MathMax(prev_calculated, RangePeriods - 1)
    endPos = rates_total - 1
    currentPos = endPos - startPos
    for i in range(currentPos, 0 - 1, -1):
        CalculateCurrentBar(i, high, low, rates_total)
    return rates_total

def CalculateCurrentBar(pos, high, low, rates_total):
    LowestLow = 0.0
    HighestHigh = 0.0
    GreatestRange = 0.0
    MidPrice = 0.0
    SmoothedLocation = 0.0
    FishIndex = 0.0
    SmoothedFish = 0.0
    PriceLocation = 0.0
    LowestLow = low[iLowest(None, 0, MODE_LOW, RangePeriods, pos)]
    HighestHigh = high[iHighest(None, 0, MODE_HIGH, RangePeriods, pos)]
    if (HighestHigh - LowestLow) < (0.1 * Point()):
        HighestHigh = LowestLow + (0.1 * Point())
    GreatestRange = HighestHigh - LowestLow
    MidPrice = (high[pos] + low[pos]) / 2.0
    PriceLocation = _fdiv(MidPrice - LowestLow, GreatestRange)
    PriceLocation = (2.0 * PriceLocation) - 1.0
    ExtMapBuffer_PriceLocation[pos] = (PriceSmoothing * ExtMapBuffer_PriceLocation[pos + 1]) + ((1.0 - PriceSmoothing) * PriceLocation)
    SmoothedLocation = ExtMapBuffer_PriceLocation[pos]
    if SmoothedLocation > 0.99:
        SmoothedLocation = 0.99
    if SmoothedLocation < -0.99:
        SmoothedLocation = -0.99
    FishIndex = MathLog(_fdiv(1.0 + SmoothedLocation, 1.0 - SmoothedLocation))
    ExtMapBuffer_FisherIndex[pos] = (IndexSmoothing * ExtMapBuffer_FisherIndex[pos + 1]) + ((1.0 - IndexSmoothing) * FishIndex)
    if (rates_total - pos) < DrawStart:
        ExtMapBuffer_FisherIndex[pos] = 0.0
    SmoothedFish = ExtMapBuffer_FisherIndex[pos]
    if SmoothedFish > 0:
        ExtMapBuffer_Uptrend[pos] = SmoothedFish
        ExtMapBuffer_Downtrend[pos] = 0.0
    else:
        ExtMapBuffer_Uptrend[pos] = 0.0
        ExtMapBuffer_Downtrend[pos] = SmoothedFish


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KuskusStarlight(_MQL5Indicator):
    name = 'Kuskus Starlight'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RangePeriods': 9,  # Range periods
        'PriceSmoothing': 0.3,  # Price smoothing factor
        'IndexSmoothing': 0.9,  # Index smoothing factor
        'DrawType': _Choice({0: 'None', 1: 'Line', 2: 'Histogram', 3: 'StaryStaryNight'}, default=3),  # Line drawing type
        'DrawArrow': _Choice({251: 'Kuskus_Classic', 172: 'Six_Pointed_Star', 171: 'Five_Pointed_Star_A', 182: 'Five_Pointed_Star_B', 170: 'Four_Pointed_Star_A', 178: 'Four_Pointed_Star_B', 179: 'Four_Pointed_Star_C', 169: 'Three_Pointed_Object', 174: 'Sunbust_A', 175: 'Sunbust_B', 117: 'Diamond_A', 116: 'Diamond_B', 119: 'Diamond_C', 161: 'Circle_Plain', 162: 'Circle_Narrow', 163: 'Circle_Bold', 164: 'Circle_Dotted', 166: 'Circle_Shadow_A', 109: 'Circle_Shadow_B', 77: 'Kaboom', 91: 'YingYang', 84: 'Snowflake', 88: 'Iron_Cross', 89: 'Star_David', 90: 'Crescent_Moon', 62: 'Radioactive', 108: 'Dotted_Object'}, default=251),  # Arrow type
        'DrawSize': 3,  # Line size
    }

