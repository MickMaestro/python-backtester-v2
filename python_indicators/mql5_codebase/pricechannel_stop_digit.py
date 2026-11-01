"""PriceChannel_Stop_Digit — converted from MQL5: MQL5 Indicators/PriceChannel_Stop_Digit/PriceChannel_Stop_Digit.mq5

Copyright: Copyright © 2005, TrendLaboratory Ltd.; Link: E-mail: igorad2004@list.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, TrendLaboratory Ltd.', 'link': 'E-mail: igorad2004@list.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 5, 2: 5, 3: 1, 4: 5, 5: 5, 6: 1}, 'colors': {1: [16711935], 2: [16711935], 3: [16711935], 4: [65280], 5: [65280], 6: [65280]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {}, 'labels': {1: 'SellSignal', 2: 'SellStopSignal', 3: 'SellStopLine', 4: 'BuySignal', 5: 'BuyStopSignal', 6: 'BuyStopLine'}, 'levels': [], 'description': [], 'name': 'PriceChannel_Stop_Digit', 'source': 'MQL5 Indicators/PriceChannel_Stop_Digit/PriceChannel_Stop_Digit.mq5', 'folder': 'PriceChannel_Stop_Digit', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'PriceChannel_Stop_Digit', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'ChannelPeriod', 'py': 'ChannelPeriod', 'param': 'ChannelPeriod', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'Risk', 'py': 'Risk', 'param': 'Risk', 'type': 'double', 'default': 0.1, 'label': '', 'sinput': False}, {'mql': 'Signal', 'py': 'Signal', 'param': 'Signal', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Line', 'py': 'Line', 'param': 'Line', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Digit', 'py': 'Digit', 'param': 'Digit', 'type': 'uint', 'default': 2, 'label': 'количество разрядов округления', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': 'показывать ценовые метки', 'sinput': False}, {'mql': 'Price_color', 'py': 'Price_color', 'param': None, 'type': 'color', 'default': 16711680, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SirName = _input('SirName', 'PriceChannel_Stop_Digit')  # Первая часть имени графических объектов
ChannelPeriod = _input('ChannelPeriod', 5)
Risk = _input('Risk', 0.1)
Signal = _input('Signal', True)
Line = _input('Line', True)
Digit = _input('Digit', 2)  # количество разрядов округления
ShowPrice = _input('ShowPrice', True)  # показывать ценовые метки
Price_color = _input('Price_color', clrBlue)
DownTrendSignal = Arr(0, 0.0)
DownTrendBuffer = Arr(0, 0.0)
DownTrendLine = Arr(0, 0.0)
UpTrendSignal = Arr(0, 0.0)
UpTrendBuffer = Arr(0, 0.0)
UpTrendLine = Arr(0, 0.0)
PointPow10 = 0.0
StartBars = 0
Price_name = ""

def OnInit():
    global PointPow10, Price_name, StartBars
    StartBars = ChannelPeriod + 1
    PointPow10 = Point() * MathPow(10, Digit)
    Price_name = SirName + 'Price'
    SetIndexBuffer(0, DownTrendSignal, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(0, PLOT_LABEL, 'SellSignal')
    PlotIndexSetInteger(0, PLOT_ARROW, 108)
    ArraySetAsSeries(DownTrendSignal, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, DownTrendBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(1, PLOT_LABEL, 'SellStopSignal')
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    ArraySetAsSeries(DownTrendBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(2, DownTrendLine, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(2, PLOT_LABEL, 'SellStopLine')
    ArraySetAsSeries(DownTrendLine, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(3, UpTrendSignal, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(3, PLOT_LABEL, 'BuySignal')
    PlotIndexSetInteger(3, PLOT_ARROW, 108)
    ArraySetAsSeries(UpTrendSignal, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(4, UpTrendBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(4, PLOT_LABEL, 'BuyStopSignal')
    PlotIndexSetInteger(4, PLOT_ARROW, 159)
    ArraySetAsSeries(UpTrendBuffer, True)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(5, UpTrendLine, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(5, PLOT_LABEL, 'BuyStopLine')
    ArraySetAsSeries(UpTrendLine, True)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'PriceChannel_Stop'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnDeinit(reason):
    ObjectDelete(0, Price_name)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_bsmax_, _s_OnCalculate_bsmin_, _s_OnCalculate_trend_
    if rates_total < StartBars:
        return 0
    limit = 0
    bar = 0
    iii = 0
    trend = 0
    bsmax = Arr(0, 0.0)
    bsmin = Arr(0, 0.0)
    High = 0.0
    Low = 0.0
    Price = 0.0
    dPrice = 0.0
    stop = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - StartBars
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    if ArrayResize(bsmax, limit + 2) != (limit + 2):
        return 0
    if ArrayResize(bsmin, limit + 2) != (limit + 2):
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        High = high[bar]
        Low = low[bar]
        iii = bar - 1 + ChannelPeriod
        while iii >= bar:
            Price = high[iii]
            if High < Price:
                High = Price
            Price = low[iii]
            if Low > Price:
                Low = Price
            iii -= 1
        dPrice = (High - Low) * Risk
        bsmax[bar] = High - dPrice
        bsmin[bar] = Low + dPrice
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bsmax[limit + 1] = _s_OnCalculate_bsmax_
    bsmin[limit + 1] = _s_OnCalculate_bsmin_
    trend = _s_OnCalculate_trend_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            _s_OnCalculate_bsmax_ = bsmax[1]
            _s_OnCalculate_bsmin_ = bsmin[1]
            _s_OnCalculate_trend_ = trend
        UpTrendBuffer[bar] = 0.0
        DownTrendBuffer[bar] = 0.0
        UpTrendSignal[bar] = 0.0
        DownTrendSignal[bar] = 0.0
        UpTrendLine[bar] = 0.0
        DownTrendLine[bar] = 0.0
        if close[bar] > bsmax[bar + 1]:
            trend = 1
        if close[bar] < bsmin[bar + 1]:
            trend = -1
        if trend > 0 and bsmin[bar] < bsmin[bar + 1]:
            bsmin[bar] = bsmin[bar + 1]
        if trend < 0 and bsmax[bar] > bsmax[bar + 1]:
            bsmax[bar] = bsmax[bar + 1]
        if trend > 0:
            Price = bsmin[bar]
            stop = PointPow10 * MathRound(_fdiv(Price, PointPow10))
            if Signal and DownTrendBuffer[bar + 1] > 0:
                UpTrendSignal[bar] = stop
                if Line:
                    UpTrendLine[bar] = stop
            else:
                UpTrendBuffer[bar] = stop
                if Line:
                    UpTrendLine[bar] = stop
        if trend < 0:
            Price = bsmax[bar]
            stop = PointPow10 * MathRound(_fdiv(Price, PointPow10))
            if Signal and UpTrendBuffer[bar + 1] > 0:
                DownTrendSignal[bar] = stop
                if Line:
                    DownTrendLine[bar] = stop
            else:
                DownTrendBuffer[bar] = stop
                if Line:
                    DownTrendLine[bar] = stop
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if ShowPrice:
        bar0 = 0
        time0 = time[bar0] + (1 * PeriodSeconds())
        SetRightPrice(0, Price_name, 0, time0, stop, Price_color)
    ChartRedraw(0)
    return rates_total

def CreateRightPrice(chart_id, name, nwin, time, price, Color):
    ObjectCreate(chart_id, name, OBJ_ARROW_RIGHT_PRICE, nwin, time, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, 2)

def SetRightPrice(chart_id, name, nwin, time, price, Color):
    if ObjectFind(chart_id, name) == -1:
        CreateRightPrice(chart_id, name, nwin, time, price, Color)
    else:
        ObjectMove(chart_id, name, 0, time, price)

# ---- static local variables
_s_OnCalculate_trend_ = 0
_s_OnCalculate_bsmax_ = 0.0
_s_OnCalculate_bsmin_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PriceChannelStopDigit(_MQL5Indicator):
    name = 'PriceChannel_Stop_Digit'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ChannelPeriod': 5,
        'Risk': 0.1,
        'Signal': True,
        'Line': True,
        'Digit': 2,  # количество разрядов округления
        'ShowPrice': True,  # показывать ценовые метки
    }

