"""TrendlinebyAngle — converted from MQL5: MQL5 Indicators/Custom Angle Trendline/TrendlinebyAngle.mq5

Custom Angle Trendline
Copyright: Copyright 2021, Dark Ryd3r; Link: https://twitter.com/DarkRyd3r; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2021, Dark Ryd3r', 'link': 'https://twitter.com/DarkRyd3r', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Custom Angle Trendline'], 'name': 'TrendlinebyAngle', 'source': 'MQL5 Indicators/Custom Angle Trendline/TrendlinebyAngle.mq5', 'folder': 'Custom Angle Trendline', 'inputs': [{'mql': 'CandlesOnChartH', 'py': 'CandlesOnChartH', 'param': 'CandlesOnChartH', 'type': 'int', 'default': 500, 'label': 'Previous Number of Bars for Downside Line', 'sinput': False}, {'mql': 'CandlesOnChartL', 'py': 'CandlesOnChartL', 'param': 'CandlesOnChartL', 'type': 'int', 'default': 500, 'label': 'Previous Number of Bars for Upside Line', 'sinput': False}, {'mql': 'DownLineAngle', 'py': 'DownLineAngle', 'param': 'DownLineAngle', 'type': 'int', 'default': 45, 'label': 'DownLine Angle', 'sinput': False}, {'mql': 'UpLineAngle', 'py': 'UpLineAngle', 'param': 'UpLineAngle', 'type': 'int', 'default': 45, 'label': 'UpLine Angle', 'sinput': False}, {'mql': 'Style_DownLine', 'py': 'Style_DownLine', 'param': 'Style_DownLine', 'type': 'int', 'default': 4, 'label': 'DownLine style', 'sinput': False}, {'mql': 'Style_UpLine', 'py': 'Style_UpLine', 'param': 'Style_UpLine', 'type': 'int', 'default': 4, 'label': 'UpLine style', 'sinput': False}, {'mql': 'Width_DownLine', 'py': 'Width_DownLine', 'param': 'Width_DownLine', 'type': 'int', 'default': 1, 'label': 'DownLine width', 'sinput': False}, {'mql': 'Width_UpLine', 'py': 'Width_UpLine', 'param': 'Width_UpLine', 'type': 'int', 'default': 1, 'label': 'UpLine width', 'sinput': False}, {'mql': 'Color_DownLine', 'py': 'Color_DownLine', 'param': None, 'type': 'color', 'default': 9639167, 'label': 'DownLine Color', 'sinput': False}, {'mql': 'Color_UpLine', 'py': 'Color_UpLine', 'param': None, 'type': 'color', 'default': 16776960, 'label': 'UpLine Color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Width
Width_1 = 1
Width_2 = 2
Width_3 = 3
Width_4 = 4
Width_5 = 5
_enum('Width', {1: 'Width_1', 2: 'Width_2', 3: 'Width_3', 4: 'Width_4', 5: 'Width_5'})

# enum STYLE
SOLID_ = 0
DASH_ = 1
DOT_ = 2
DASHDOT_ = 3
DASHDOTDOT_ = 4
_enum('STYLE', {0: 'SOLID_', 1: 'DASH_', 2: 'DOT_', 3: 'DASHDOT_', 4: 'DASHDOTDOT_'})

# ---- inputs and global variables
CandlesOnChartH = _input('CandlesOnChartH', 500)  # Previous Number of Bars for Downside Line
CandlesOnChartL = _input('CandlesOnChartL', 500)  # Previous Number of Bars for Upside Line
DownLineAngle = _input('DownLineAngle', 45)  # DownLine Angle
UpLineAngle = _input('UpLineAngle', 45)  # UpLine Angle
Style_DownLine = _input('Style_DownLine', DASHDOTDOT_)  # DownLine style
Style_UpLine = _input('Style_UpLine', DASHDOTDOT_)  # UpLine style
Width_DownLine = _input('Width_DownLine', Width_1)  # DownLine width
Width_UpLine = _input('Width_UpLine', Width_1)  # UpLine width
Color_DownLine = _input('Color_DownLine', clrDeepPink)  # DownLine Color
Color_UpLine = _input('Color_UpLine', clrAqua)  # UpLine Color

def OnInit():
    IndicatorSetString(INDICATOR_SHORTNAME, 'Custom Angle Trendline')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(0, 'DownLine')
    ObjectDelete(0, 'UpLine')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if prev_calculated != rates_total:
        HighestCandle = 0
        LowestCandle = 0
        High = Arr(0, 0.0)
        Low = Arr(0, 0.0)
        ArraySetAsSeries(High, True)
        ArraySetAsSeries(Low, True)
        CopyHigh(Symbol(), Period(), 0, CandlesOnChartH, High)
        CopyLow(Symbol(), Period(), 0, CandlesOnChartL, Low)
        HighestCandle = ArrayMaximum(High, 0, CandlesOnChartH)
        LowestCandle = ArrayMinimum(Low, 0, CandlesOnChartL)
        PriceInformation = Arr(0, 0, factory=MqlRates)
        ArraySetAsSeries(PriceInformation, True)
        DataH = CopyRates(Symbol(), Period(), 0, CandlesOnChartH, PriceInformation)
        DataL = CopyRates(Symbol(), Period(), 0, CandlesOnChartL, PriceInformation)
        ObjectCreate(0, 'DownLine', OBJ_TRENDBYANGLE, 0, PriceInformation[HighestCandle].time, PriceInformation[HighestCandle].high, PriceInformation[0].time, PriceInformation[0].high)
        ObjectSetDouble(0, 'DownLine', OBJPROP_ANGLE, DownLineAngle)
        ObjectSetDouble(0, 'DownLine', OBJPROP_SCALE, 1.0)
        ObjectSetInteger(0, 'DownLine', OBJPROP_RAY_LEFT, True)
        ObjectSetInteger(0, 'DownLine', OBJPROP_WIDTH, 2)
        ObjectSetInteger(0, 'DownLine', OBJPROP_STYLE, Style_DownLine)
        ObjectSetInteger(0, 'DownLine', OBJPROP_COLOR, Color_DownLine)
        ObjectMove(0, 'DownLine', 0, PriceInformation[HighestCandle].time, PriceInformation[HighestCandle].high)
        ObjectCreate(0, 'UpLine', OBJ_TRENDBYANGLE, 0, PriceInformation[LowestCandle].time, PriceInformation[LowestCandle].low, PriceInformation[0].time, PriceInformation[0].low)
        ObjectSetDouble(0, 'UpLine', OBJPROP_ANGLE, UpLineAngle)
        ObjectSetDouble(0, 'UpLine', OBJPROP_SCALE, 1.0)
        ObjectSetInteger(0, 'UpLine', OBJPROP_RAY_RIGHT, True)
        ObjectSetInteger(0, 'UpLine', OBJPROP_WIDTH, 2)
        ObjectSetInteger(0, 'UpLine', OBJPROP_STYLE, Style_UpLine)
        ObjectSetInteger(0, 'UpLine', OBJPROP_COLOR, Color_UpLine)
        ObjectMove(0, 'UpLine', 0, PriceInformation[LowestCandle].time, PriceInformation[LowestCandle].low)
    ChartRedraw(0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendlinebyAngle(_MQL5Indicator):
    name = 'TrendlinebyAngle'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CandlesOnChartH': 500,  # Previous Number of Bars for Downside Line
        'CandlesOnChartL': 500,  # Previous Number of Bars for Upside Line
        'DownLineAngle': 45,  # DownLine Angle
        'UpLineAngle': 45,  # UpLine Angle
        'Style_DownLine': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # DownLine style
        'Style_UpLine': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=4),  # UpLine style
        'Width_DownLine': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # DownLine width
        'Width_UpLine': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # UpLine width
    }

