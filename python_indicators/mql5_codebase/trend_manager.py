"""trend_manager — converted from MQL5: MQL5 Indicators/TrendManager/trend_manager.mq5

Copyright: Copyright © 2006,  Alejandro Galindo; Link: http://elCactus.com/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006,  Alejandro Galindo', 'link': 'http://elCactus.com/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 11}, 'colors': {1: [8421504, 9639167, 13749760]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'Trend Manager'}, 'levels': [], 'description': [], 'name': 'trend_manager', 'source': 'MQL5 Indicators/TrendManager/trend_manager.mq5', 'folder': 'TrendManager', 'inputs': [{'mql': 'DVLimit', 'py': 'DVLimit', 'param': 'DVLimit', 'type': 'uint', 'default': 70, 'label': 'Limit in points', 'sinput': False}, {'mql': 'Fast_Period', 'py': 'Fast_Period', 'param': 'Fast_Period', 'type': 'uint', 'default': 23, 'label': 'Fast MA period', 'sinput': False}, {'mql': 'Fast_Price', 'py': 'Fast_Price', 'param': 'Fast_Price', 'type': 'int', 'default': 2, 'label': 'Fast MA price type', 'sinput': False}, {'mql': 'Fast_Method', 'py': 'Fast_Method', 'param': 'Fast_Method', 'type': 'int', 'default': 0, 'label': 'Fast MA smoothing method', 'sinput': False}, {'mql': 'Slow_Period', 'py': 'Slow_Period', 'param': 'Slow_Period', 'type': 'uint', 'default': 84, 'label': 'Slow MA period', 'sinput': False}, {'mql': 'Slow_Price', 'py': 'Slow_Price', 'param': 'Slow_Price', 'type': 'int', 'default': 2, 'label': 'Slow MA price type', 'sinput': False}, {'mql': 'Slow_Method', 'py': 'Slow_Method', 'param': 'Slow_Method', 'type': 'int', 'default': 0, 'label': 'Slow MA smoothing method', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
DVLimit = _input('DVLimit', 70)  # Limit in points
Fast_Period = _input('Fast_Period', 23)  # Fast MA period
Fast_Price = _input('Fast_Price', PRICE_OPEN)  # Fast MA price type
Fast_Method = _input('Fast_Method', MODE_SMA)  # Fast MA smoothing method
Slow_Period = _input('Slow_Period', 84)  # Slow MA period
Slow_Price = _input('Slow_Price', PRICE_OPEN)  # Slow MA price type
Slow_Method = _input('Slow_Method', MODE_SMA)  # Slow MA smoothing method
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
dDVLimit = 0.0
MAa_Handle = 0
MAb_Handle = 0
min_rates_total = 0
min_rates_total1 = 0
min_rates_total2 = 0
SpanA_Buffer = Arr(0, 0.0)
SpanB_Buffer = Arr(0, 0.0)
Color_Buffer = Arr(0, 0.0)

def OnInit():
    global MAa_Handle, MAb_Handle, dDVLimit, min_rates_total
    min_rates_total = _int(MathMax(Fast_Period, Slow_Period))
    dDVLimit = DVLimit * Point()
    MAa_Handle = iMA(None, 0, Fast_Period, 0, Fast_Method, Fast_Price)
    if MAa_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the MA a indicator')
    MAb_Handle = iMA(None, 0, Slow_Period, 0, Slow_Method, Slow_Price)
    if MAb_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the MA b indicator')
    SetIndexBuffer(0, SpanA_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(SpanA_Buffer, True)
    SetIndexBuffer(1, SpanB_Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(SpanB_Buffer, True)
    SetIndexBuffer(2, Color_Buffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Color_Buffer, True)
    shortname = 'Trend Manager'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if (BarsCalculated(MAa_Handle) < rates_total or BarsCalculated(MAb_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    MAA = Arr(0, 0.0)
    MAB = Arr(0, 0.0)
    D = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(MAa_Handle, 0, 0, to_copy, MAA) <= 0:
        return 0
    if CopyBuffer(MAb_Handle, 0, 0, to_copy, MAB) <= 0:
        return 0
    ArraySetAsSeries(MAA, True)
    ArraySetAsSeries(MAB, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(High, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        D = MAA[bar] - MAB[bar]
        SpanA_Buffer[bar] = 0.0
        SpanB_Buffer[bar] = 0.0
        Color_Buffer[bar] = 0.0
        if D >= dDVLimit:
            SpanA_Buffer[bar] = High[bar]
            SpanB_Buffer[bar] = High[bar] + (D - dDVLimit)
            Color_Buffer[bar] = 2.0
        if D <= (-dDVLimit):
            SpanA_Buffer[bar] = Low[bar]
            SpanB_Buffer[bar] = Low[bar] + (D - dDVLimit)
            Color_Buffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrendManager(_MQL5Indicator):
    name = 'trend_manager'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'DVLimit': 70,  # Limit in points
        'Fast_Period': 23,  # Fast MA period
        'Fast_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=2),  # Fast MA price type
        'Fast_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Fast MA smoothing method
        'Slow_Period': 84,  # Slow MA period
        'Slow_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=2),  # Slow MA price type
        'Slow_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Slow MA smoothing method
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

