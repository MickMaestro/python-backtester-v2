"""affinetransform — converted from MQL5: MQL5 Indicators/AffineTransform/affinetransform.mq5

Copyright: Copyright © 2009, xp3rienced; Link: no4ta[at]inbox.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, xp3rienced', 'link': 'no4ta[at]inbox.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16711935, 8421504, 10025880]}, 'widths': {}, 'styles': {}, 'labels': {1: 'AffineTransform Open'}, 'levels': [], 'description': [], 'name': 'affinetransform', 'source': 'MQL5 Indicators/AffineTransform/affinetransform.mq5', 'folder': 'AffineTransform', 'inputs': [{'mql': 'Trendline_Name', 'py': 'Trendline_Name', 'param': None, 'type': 'string', 'default': 'A_Line', 'label': 'Object name (trend line)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Trendline_Name = _input('Trendline_Name', 'A_Line')  # Object name (trend line)
min_rates_total = 0
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
LineAngleTg = 0.0  # Tangent of trend line inclination angle
LinePrice1 = 0.0  # Price coordinates of trend line points
LinePrice2 = 0.0  # Price coordinates of trend line points
LineTime1 = 0  # Time coordinates of trend line points
LineTime2 = 0  # Time coordinates of trend line points
Shift1 = 0  # Bar shifting of trend line points
Shift2 = 0  # Bar shifting of trend line points
Multiplier = 0  # Multiplier applied to the price (to reduce the margin of error)
NeedUpdate = False

def OnInit():
    global Multiplier, NeedUpdate, min_rates_total
    min_rates_total = 100
    NeedUpdate = True
    Multiplier = _int(MathPow(10, Digits()))
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Affine Transform Candles')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global NeedUpdate
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    CalcAngleTg()
    if NeedUpdate:
        limit = rates_total - 1
        NeedUpdate = False
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        res = (bar - Shift1) * LineAngleTg
        ExtOpenBuffer[bar] = ((open[bar] - LinePrice1) * Multiplier) + res
        ExtCloseBuffer[bar] = ((close[bar] - LinePrice1) * Multiplier) + res
        ExtHighBuffer[bar] = ((high[bar] - LinePrice1) * Multiplier) + res
        ExtLowBuffer[bar] = ((low[bar] - LinePrice1) * Multiplier) + res
        if close[bar] > open[bar]:
            ExtColorBuffer[bar] = 2.0
        elif close[bar] < open[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def iBarShift_u(symbol, timeframe, time):
    if time < 0:
        return -1
    Arr_ = Arr(0, 0)
    time1 = 0
    time1 = SeriesInfoInteger(symbol, timeframe, SERIES_LASTBAR_DATE)
    if CopyTime(symbol, timeframe, _DT(time), _DT(time1), Arr_) > 0:
        size = ArraySize(Arr_)
        return size - 1
    else:
        return -1

def CalcAngleTg():
    global LineAngleTg, LinePrice1, LinePrice2, LineTime1, LineTime2, NeedUpdate, Shift1, Shift2
    if ObjectFind(0, Trendline_Name) == -1:
        return
    tg = 0.0
    LinePrice1 = ObjectGetDouble(0, Trendline_Name, OBJPROP_PRICE, 0)
    LinePrice2 = ObjectGetDouble(0, Trendline_Name, OBJPROP_PRICE, 1)
    LineTime1 = ObjectGetInteger(0, Trendline_Name, OBJPROP_TIME, 0)
    LineTime2 = ObjectGetInteger(0, Trendline_Name, OBJPROP_TIME, 1)
    Shift1 = iBarShift_u("", PERIOD_CURRENT, LineTime1)
    Shift2 = iBarShift_u("", PERIOD_CURRENT, LineTime2)
    tg = _fdiv((LinePrice2 - LinePrice1) * Multiplier, Shift1 - Shift2)
    if tg != LineAngleTg:
        NeedUpdate = True
    LineAngleTg = tg


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Affinetransform(_MQL5Indicator):
    name = 'affinetransform'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

