"""FractalChannel_Cloud — converted from MQL5: MQL5 Indicators/FractalChannel_Cloud/FractalChannel_Cloud.mq5

Copyright: Copyright © 2005, TrendLaboratory Ltd.; Link: E-mail: igorad2004@list.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, TrendLaboratory Ltd.', 'link': 'E-mail: igorad2004@list.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 5}, 'types': {1: 7, 2: 7, 3: 1, 4: 1, 5: 1}, 'colors': {1: [16252904], 2: [16773375], 3: [5737262], 4: [8421504], 5: [255]}, 'widths': {3: 1, 4: 1, 5: 1}, 'styles': {3: 4, 4: 4, 5: 4}, 'labels': {1: 'Upper FractalChannel cloud', 2: 'Lower FractalChannel cloud', 3: 'Upper FractalChannel', 4: 'Middle FractalChannel', 5: 'Lower FractalChannel'}, 'levels': [], 'description': [], 'name': 'FractalChannel_Cloud', 'source': 'MQL5 Indicators/FractalChannel_Cloud/FractalChannel_Cloud.mq5', 'folder': 'FractalChannel_Cloud', 'inputs': [{'mql': 'ChannelType', 'py': 'ChannelType', 'param': 'ChannelType', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Margins', 'py': 'Margins', 'param': 'Margins', 'type': 'double', 'default': 0.0, 'label': '', 'sinput': False}, {'mql': 'Advance', 'py': 'Advance', 'param': 'Advance', 'type': 'double', 'default': 0.0, 'label': '', 'sinput': False}, {'mql': 'Prices', 'py': 'Prices', 'param': 'Prices', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Type
Type_1 = 1
Type_2 = 2
Type_3 = 3
_enum('Type', {1: 'Type_1', 2: 'Type_2', 3: 'Type_3'})

# enum PriceType
OpenClose = 0
LowHigh = 1
_enum('PriceType', {0: 'OpenClose', 1: 'LowHigh'})

# ---- inputs and global variables
ChannelType = _input('ChannelType', Type_1)
Margins = _input('Margins', 0.0)
Advance = _input('Advance', 0.0)
Prices = _input('Prices', OpenClose)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
UpUpBuffer = Arr(0, 0.0)
UpDnBuffer = Arr(0, 0.0)
DnUpBuffer = Arr(0, 0.0)
DnDnBuffer = Arr(0, 0.0)
UpperBuffer = Arr(0, 0.0)
MiddleBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
min_rates_total = 7

def OnInit():
    SetIndexBuffer(0, UpUpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(UpUpBuffer, True)
    SetIndexBuffer(1, UpDnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpDnBuffer, True)
    SetIndexBuffer(2, DnUpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(DnUpBuffer, True)
    SetIndexBuffer(3, DnDnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnDnBuffer, True)
    SetIndexBuffer(4, UpperBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpperBuffer, True)
    SetIndexBuffer(5, MiddleBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(MiddleBuffer, True)
    SetIndexBuffer(6, LowerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(LowerBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'FractalChannel_Cloud( ChannelType=', ChannelType, ',Prices=', Prices, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_smax_, _s_OnCalculate_smin_
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    smax = 0.0
    smin = 0.0
    Low0 = 0.0
    Low1 = 0.0
    Low2 = 0.0
    Low3 = 0.0
    Low4 = 0.0
    Low5 = 0.0
    Low6 = 0.0
    High0 = 0.0
    High1 = 0.0
    High2 = 0.0
    High3 = 0.0
    High4 = 0.0
    High5 = 0.0
    High6 = 0.0
    v1 = 0.0
    v2 = 0.0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        _s_OnCalculate_smax_ = 0.0
        _s_OnCalculate_smin_ = 1000000000000.0
    else:
        limit = rates_total - prev_calculated
    smax = _s_OnCalculate_smax_
    smin = _s_OnCalculate_smin_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == (rates_total - 1):
            _s_OnCalculate_smax_ = smax
            _s_OnCalculate_smin_ = smin
        v1 = -1.0
        v2 = -1.0
        _sw1 = Prices
        if _sw1 == OpenClose:
            High0 = high[bar + 0]
            High1 = high[bar + 1]
            High2 = high[bar + 2]
            High3 = high[bar + 3]
            High4 = high[bar + 4]
            High5 = high[bar + 5]
            High6 = high[bar + 6]
            Low0 = low[bar + 0]
            Low1 = low[bar + 1]
            Low2 = low[bar + 2]
            Low3 = low[bar + 3]
            Low4 = low[bar + 4]
            Low5 = low[bar + 5]
            Low6 = low[bar + 6]
        elif _sw1 == LowHigh:
            High0 = MathMax(close[bar + 0], open[bar + 1])
            High1 = MathMax(close[bar + 1], open[bar + 1])
            High2 = MathMax(close[bar + 2], open[bar + 2])
            High3 = MathMax(close[bar + 3], open[bar + 3])
            High4 = MathMax(close[bar + 4], open[bar + 4])
            High5 = MathMax(close[bar + 5], open[bar + 5])
            High6 = MathMax(close[bar + 6], open[bar + 6])
            Low0 = MathMin(close[bar + 0], open[bar + 1])
            Low1 = MathMin(close[bar + 1], open[bar + 1])
            Low2 = MathMin(close[bar + 2], open[bar + 2])
            Low3 = MathMin(close[bar + 3], open[bar + 3])
            Low4 = MathMin(close[bar + 4], open[bar + 4])
            Low5 = MathMin(close[bar + 5], open[bar + 5])
            Low6 = MathMin(close[bar + 6], open[bar + 6])
        else:
            High0 = high[bar + 0]
            High1 = high[bar + 1]
            High2 = high[bar + 2]
            High3 = high[bar + 3]
            High4 = high[bar + 4]
            High5 = high[bar + 5]
            High6 = high[bar + 6]
            Low0 = low[bar + 0]
            Low1 = low[bar + 1]
            Low2 = low[bar + 2]
            Low3 = low[bar + 3]
            Low4 = low[bar + 4]
            Low5 = low[bar + 5]
            Low6 = low[bar + 6]
        _sw2 = ChannelType
        if _sw2 == Type_1:
            if High2 <= High1 and High0 < High1:
                v1 = High1
            if Low2 >= Low1 and Low0 > Low1:
                v2 = Low1
        elif _sw2 == Type_2:
            if ((High4 <= High2 and High3 <= High2) and High0 < High2) and High1 < High2:
                v1 = High2
            if ((Low4 >= Low2 and Low3 >= Low2) and Low0 > Low2) and Low1 > Low2:
                v2 = Low2
        elif _sw2 == Type_3:
            if ((((High6 <= High3 and High5 <= High3) and High4 <= High3) and High0 < High3) and High1 < High3) and High2 < High3:
                v1 = High3
            if ((((Low6 >= Low3 and Low5 >= Low3) and Low4 >= Low3) and Low0 > Low3) and Low1 > Low3) and Low2 > Low3:
                v2 = Low3
        else:
            if High2 <= High1 and High0 < High1:
                v1 = High1
            if Low2 >= Low1 and Low0 > Low1:
                v2 = Low1
        if v1 > 0:
            smax = v1
        if High0 > smax:
            smax = High0
        if v2 > 0:
            smin = v2
        if Low0 < smin:
            smin = Low0
        UpUpBuffer[bar] = smax - ((smax - smin) * Margins)
        UpperBuffer[bar] = UpUpBuffer[bar]
        DnDnBuffer[bar] = smin + ((smax - smin) * Margins)
        LowerBuffer[bar] = DnDnBuffer[bar]
        DnUpBuffer[bar] = (UpperBuffer[bar] + LowerBuffer[bar]) / 2
        UpDnBuffer[bar] = DnUpBuffer[bar]
        MiddleBuffer[bar] = UpDnBuffer[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_smax_ = 0.0
_s_OnCalculate_smin_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FractalChannelCloud(_MQL5Indicator):
    name = 'FractalChannel_Cloud'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ChannelType': _Choice({1: 'Type_1', 2: 'Type_2', 3: 'Type_3'}, default=1),
        'Margins': 0.0,
        'Advance': 0.0,
        'Prices': _Choice({0: 'OpenClose', 1: 'LowHigh'}, default=0),
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

