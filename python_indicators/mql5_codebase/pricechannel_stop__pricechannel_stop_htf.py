"""PriceChannel_Stop — converted from MQL5: MQL5 Indicators/PriceChannel_Stop_HTF/PriceChannel_Stop.mq5

Copyright: Copyright © 2005, TrendLaboratory Ltd.; Link: E-mail: igorad2004@list.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, TrendLaboratory Ltd.', 'link': 'E-mail: igorad2004@list.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 5, 2: 5, 3: 1, 4: 5, 5: 5, 6: 1}, 'colors': {1: [16711935], 2: [16711935], 3: [16711935], 4: [65280], 5: [65280], 6: [65280]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {}, 'labels': {1: 'SellSignal', 2: 'SellStopSignal', 3: 'SellStopLine', 4: 'BuySignal', 5: 'BuyStopSignal', 6: 'BuyStopLine'}, 'levels': [], 'description': [], 'name': 'PriceChannel_Stop', 'source': 'MQL5 Indicators/PriceChannel_Stop_HTF/PriceChannel_Stop.mq5', 'folder': 'PriceChannel_Stop_HTF', 'inputs': [{'mql': 'ChannelPeriod', 'py': 'ChannelPeriod', 'param': 'ChannelPeriod', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'Risk', 'py': 'Risk', 'param': 'Risk', 'type': 'double', 'default': 0.1, 'label': '', 'sinput': False}, {'mql': 'Signal', 'py': 'Signal', 'param': 'Signal', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Line', 'py': 'Line', 'param': 'Line', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ChannelPeriod = _input('ChannelPeriod', 5)
Risk = _input('Risk', 0.1)
Signal = _input('Signal', True)
Line = _input('Line', True)
DownTrendSignal = Arr(0, 0.0)
DownTrendBuffer = Arr(0, 0.0)
DownTrendLine = Arr(0, 0.0)
UpTrendSignal = Arr(0, 0.0)
UpTrendBuffer = Arr(0, 0.0)
UpTrendLine = Arr(0, 0.0)
StartBars = 0

def OnInit():
    global StartBars
    StartBars = ChannelPeriod + 1
    SetIndexBuffer(0, DownTrendSignal, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(0, PLOT_LABEL, 'SellSignal')
    PlotIndexSetInteger(0, PLOT_ARROW, 108)
    ArraySetAsSeries(DownTrendSignal, True)
    SetIndexBuffer(1, DownTrendBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(1, PLOT_LABEL, 'SellStopSignal')
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    ArraySetAsSeries(DownTrendBuffer, True)
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
    SetIndexBuffer(4, UpTrendBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(4, PLOT_LABEL, 'BuyStopSignal')
    PlotIndexSetInteger(4, PLOT_ARROW, 159)
    ArraySetAsSeries(UpTrendBuffer, True)
    SetIndexBuffer(5, UpTrendLine, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(5, PLOT_LABEL, 'BuyStopLine')
    ArraySetAsSeries(UpTrendLine, True)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'PriceChannel_Stop'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

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
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - StartBars
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
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
            if Signal and DownTrendBuffer[bar + 1] > 0:
                UpTrendSignal[bar] = Price
                if Line:
                    UpTrendLine[bar] = Price
            else:
                UpTrendBuffer[bar] = Price
                if Line:
                    UpTrendLine[bar] = Price
        if trend < 0:
            Price = bsmax[bar]
            if Signal and UpTrendBuffer[bar + 1] > 0:
                DownTrendSignal[bar] = Price
                if Line:
                    DownTrendLine[bar] = Price
            else:
                DownTrendBuffer[bar] = Price
                if Line:
                    DownTrendLine[bar] = Price
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_trend_ = 0
_s_OnCalculate_bsmax_ = 0.0
_s_OnCalculate_bsmin_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PriceChannelStop(_MQL5Indicator):
    name = 'PriceChannel_Stop'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ChannelPeriod': 5,
        'Risk': 0.1,
        'Signal': True,
        'Line': True,
    }

