"""Multi-Day Dynamic VWAP — converted from MQL5: MQL5 Indicators/Multi-Day Dynamic VWAP/Multi-Day Dynamic VWAP.mq5

Copyright: Copyright phade 2025, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright phade 2025, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {}, 'colors': {1: [11119017, 6908265]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Close Prices'}, 'levels': [], 'description': [], 'name': 'Multi-Day Dynamic VWAP', 'source': 'MQL5 Indicators/Multi-Day Dynamic VWAP/Multi-Day Dynamic VWAP.mq5', 'folder': 'Multi-Day Dynamic VWAP', 'inputs': [{'mql': 'input_time', 'py': 'input_time', 'param': 'input_time', 'type': 'int', 'default': 16408, 'label': 'VWAP Timeframe', 'sinput': False}, {'mql': 'barsToUse', 'py': 'barsToUse', 'param': 'barsToUse', 'type': 'int', 'default': 5, 'label': 'VWAP Averaging Period', 'sinput': False}, {'mql': 'ha_smoothing', 'py': 'ha_smoothing', 'param': 'ha_smoothing', 'type': 'int', 'default': 2, 'label': 'HA Smoothing', 'sinput': False}, {'mql': 'show_info', 'py': 'show_info', 'param': 'show_info', 'type': 'bool', 'default': True, 'label': 'Display VWAP price information', 'sinput': False}, {'mql': 'drawing', 'py': 'drawing', 'param': 'drawing', 'type': 'int', 'default': 3, 'label': 'Plot to represent close prices', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_CUSTOM_PLOT
CANDLES = 0
BARS = 1
LINE = 2
HISTOGRAM = 3
_enum('ENUM_CUSTOM_PLOT', {0: 'CANDLES', 1: 'BARS', 2: 'LINE', 3: 'HISTOGRAM'})

# ---- inputs and global variables
input_time = _input('input_time', PERIOD_D1)  # VWAP Timeframe
barsToUse = _input('barsToUse', 5)  # VWAP Averaging Period
ha_smoothing = _input('ha_smoothing', 2)  # HA Smoothing
show_info = _input('show_info', True)  # Display VWAP price information
drawing = _input('drawing', HISTOGRAM)  # Plot to represent close prices
Buffer = Arr(0, 0.0)
timeBuf = Arr(0, 0)
ExtOBuffer = Arr(0, 0.0)
ExtCBuffer = Arr(0, 0.0)
ExtHBuffer = Arr(0, 0.0)
ExtLBuffer = Arr(0, 0.0)
dailyHigh = Arr(0, 0.0)
dailyLow = Arr(0, 0.0)
dailyClose = Arr(0, 0.0)
dailyVolume = Arr(0, 0)
closecol = Arr(0, 0.0)

def OnInit():
    short_name = ""
    if drawing == HISTOGRAM:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_COLOR_HISTOGRAM)
        SetIndexBuffer(0, Buffer, INDICATOR_DATA)
        SetIndexBuffer(1, closecol, INDICATOR_COLOR_INDEX)
        SetIndexBuffer(2, ExtOBuffer, INDICATOR_CALCULATIONS)
        SetIndexBuffer(3, ExtCBuffer, INDICATOR_CALCULATIONS)
    elif drawing == CANDLES:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_COLOR_CANDLES)
        SetIndexBuffer(0, ExtOBuffer, INDICATOR_DATA)
        SetIndexBuffer(1, ExtHBuffer, INDICATOR_DATA)
        SetIndexBuffer(2, ExtLBuffer, INDICATOR_DATA)
        SetIndexBuffer(3, ExtCBuffer, INDICATOR_DATA)
        SetIndexBuffer(4, closecol, INDICATOR_COLOR_INDEX)
    elif drawing == BARS:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_COLOR_BARS)
        SetIndexBuffer(0, ExtOBuffer, INDICATOR_DATA)
        SetIndexBuffer(1, ExtHBuffer, INDICATOR_DATA)
        SetIndexBuffer(2, ExtLBuffer, INDICATOR_DATA)
        SetIndexBuffer(3, ExtCBuffer, INDICATOR_DATA)
        SetIndexBuffer(4, closecol, INDICATOR_COLOR_INDEX)
    elif drawing == LINE:
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_COLOR_LINE)
        SetIndexBuffer(0, Buffer, INDICATOR_DATA)
        SetIndexBuffer(1, closecol, INDICATOR_COLOR_INDEX)
        SetIndexBuffer(2, ExtOBuffer, INDICATOR_CALCULATIONS)
        SetIndexBuffer(3, ExtCBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(timeBuf, True)
    ArraySetAsSeries(dailyHigh, True)
    ArraySetAsSeries(dailyLow, True)
    ArraySetAsSeries(dailyClose, True)
    ArraySetAsSeries(dailyVolume, True)
    short_name = 'Multi-Day Dynamic VWAP'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, clrDarkOrange)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, STYLE_SOLID)
    ChartNavigate(0, CHART_END)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_VWAP_Price, _s_OnCalculate_lastStatusAboveVWAP
    start = (1 if (prev_calculated == 0) else (prev_calculated - 1))
    cumulativePV = 0.0
    cumulativeVol = 0
    if (drawing != LINE and drawing != HISTOGRAM) and prev_calculated == 0:
        ExtLBuffer[0] = low[0]
        ExtHBuffer[0] = high[0]
        ExtOBuffer[0] = open[0]
        ExtCBuffer[0] = close[0]
    if ((CopyHigh(Symbol(), input_time, 0, barsToUse, dailyHigh) == barsToUse and CopyLow(Symbol(), input_time, 0, barsToUse, dailyLow) == barsToUse) and CopyClose(Symbol(), input_time, 0, barsToUse, dailyClose) == barsToUse) and CopyTickVolume(Symbol(), input_time, 0, barsToUse, dailyVolume) == barsToUse:
        for i in range(0, barsToUse):
            typicalPrice = (dailyHigh[i] + dailyLow[i] + dailyClose[i]) / 3.0
            cumulativePV += typicalPrice * dailyVolume[i]
            cumulativeVol += dailyVolume[i]
        if cumulativeVol > 0:
            _s_OnCalculate_VWAP_Price = _fdiv(cumulativePV, cumulativeVol)
    for i in range(1, rates_total):
        Vcolor(i, open, close, high, low)
    isAboveVWAP = close[rates_total - 1] > _s_OnCalculate_VWAP_Price
    if isAboveVWAP != _s_OnCalculate_lastStatusAboveVWAP:
        if show_info:
            Comment(('Price is above VWAP' if isAboveVWAP else 'Price is below VWAP'))
        _s_OnCalculate_lastStatusAboveVWAP = isAboveVWAP
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, _s_OnCalculate_VWAP_Price)
    return rates_total

def Vcolor(p, Open, Close, High, Low):
    ha_open = (ExtOBuffer[p - 1] + ExtCBuffer[p - 1]) / 2
    ha_close = (Open[p] + High[p] + Low[p] + Close[p]) / 4
    ha_high = MathMax(High[p], MathMax(ha_open, ha_close))
    ha_low = MathMin(Low[p], MathMin(ha_open, ha_close))
    if drawing == CANDLES or drawing == BARS:
        ExtLBuffer[p] = ha_low
        ExtHBuffer[p] = ha_high
    ExtOBuffer[p] = ha_open
    ExtCBuffer[p] = ha_close
    smoothingPeriod = ha_smoothing
    smooth_ha_open = CalculateEMA(p, ExtOBuffer, smoothingPeriod)
    smooth_ha_close = CalculateEMA(p, ExtCBuffer, smoothingPeriod)
    if drawing == CANDLES:
        ExtOBuffer[p] = smooth_ha_open
        ExtCBuffer[p] = smooth_ha_close
        ExtHBuffer[p] = ha_high
        ExtLBuffer[p] = ha_low
    elif drawing == BARS:
        ExtOBuffer[p] = smooth_ha_open
        ExtCBuffer[p] = smooth_ha_close
        ExtHBuffer[p] = ha_high
        ExtLBuffer[p] = ha_low
    elif drawing == LINE:
        Buffer[p] = Close[p]
    elif drawing == HISTOGRAM:
        Buffer[p] = Close[p]
    if smooth_ha_open < smooth_ha_close:
        closecol[p] = 0.0
    else:
        closecol[p] = 1.0

def CalculateEMA(index, src, period):
    alpha = _fdiv(2.0, period + 1)
    if index == 0:
        return src[0]
    return (alpha * src[index]) + ((1 - alpha) * src[index - 1])

def OnDeinit(reason):
    Comment('')

# ---- static local variables
_s_OnCalculate_VWAP_Price = 0.0
_s_OnCalculate_lastStatusAboveVWAP = False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MultiDayDynamicVWAP(_MQL5Indicator):
    name = 'Multi-Day Dynamic VWAP'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'input_time': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # VWAP Timeframe
        'barsToUse': 5,  # VWAP Averaging Period
        'ha_smoothing': 2,  # HA Smoothing
        'show_info': True,  # Display VWAP price information
        'drawing': _Choice({0: 'Candle', 1: 'Bar', 2: 'Line', 3: 'Histogram'}, default=3),  # Plot to represent close prices
    }

