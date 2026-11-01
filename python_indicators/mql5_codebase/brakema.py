"""brakema — converted from MQL5: MQL5 Indicators/BrakeMA/brakema.mq5

Copyright: Copyright © 2012, Ivan Kornilov; Link: excelf@gmail.com; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Ivan Kornilov', 'link': 'excelf@gmail.com', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [16748574], 2: [16711935], 3: [16748574], 4: [16711935]}, 'widths': {1: 1, 2: 1, 3: 4, 4: 4}, 'styles': {}, 'labels': {1: 'Lower BrakeMA', 2: 'Upper BrakeMA', 3: 'BrakeMA Buy', 4: 'BrakeMA Sell'}, 'levels': [], 'description': [''], 'name': 'brakema', 'source': 'MQL5 Indicators/BrakeMA/brakema.mq5', 'folder': 'BrakeMA', 'inputs': [{'mql': 'ma', 'py': 'ma', 'param': 'ma', 'type': 'int', 'default': 34, 'label': '', 'sinput': False}, {'mql': 'speed', 'py': 'speed', 'param': 'speed', 'type': 'double', 'default': 0.0, 'label': '', 'sinput': False}, {'mql': 'maType', 'py': 'maType', 'param': 'maType', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ma = _input('ma', 34)
speed = _input('speed', 0.0)
maType = _input('maType', MODE_LWMA)
maxPrice_ = 0.0
minPrice_ = 0.0
beginPrice_ = 0.0
isLong_ = False
beginBar_ = 0
MABuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
min_rates_total = 0
MA_Handle = 0

def OnInit():
    global MA_Handle, min_rates_total
    min_rates_total = ma + 2
    MA_Handle = iMA(None, 0, ma, 0, maType, PRICE_CLOSE)
    if MA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the MA indicator')
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 158)
    ArraySetAsSeries(UpBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 158)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 174)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(3, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 174)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(4, MABuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(MABuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'BrakeMA'
    short_name = 'BrakeMa(' + _str(ma) + ',' + EnumToString(maType, 'ENUM_MA_METHOD') + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    global beginBar_, beginPrice_, isLong_, maxPrice_, minPrice_
    if BarsCalculated(MA_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar = 0
    maxPrice = 0.0
    minPrice = 0.0
    beginPrice = 0.0
    isLong = False
    beginBar = 0
    maxbar = rates_total - min_rates_total - 1
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
        maxPrice_ = -999999.0
        minPrice_ = 999999.0
        beginBar_ = 0
        beginPrice_ = Low[limit]
        isLong_ = True
    else:
        limit = rates_total - prev_calculated
    beginBar = beginBar_ + limit
    if beginBar > maxbar:
        limit = maxbar
        maxPrice_ = -999999.0
        minPrice_ = 999999.0
        beginBar_ = 0
        beginPrice_ = Low[limit]
        isLong_ = True
    to_copy = limit + 1
    isLong = isLong_
    maxPrice = maxPrice_
    minPrice = minPrice_
    beginPrice = beginPrice_
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy += 1
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MABuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if maxPrice < High[bar]:
            maxPrice = High[bar]
        if minPrice > Low[bar]:
            minPrice = Low[bar]
        value = 0.0
        move = 0.0
        maShift = MABuffer[beginBar] - beginPrice
        if isLong:
            if MABuffer[bar + 1] > MABuffer[bar]:
                move = (MABuffer[bar + 1] - MABuffer[bar]) * speed
                value = MABuffer[bar + 1] + move - maShift
                beginPrice += move
                MABuffer[bar] = MABuffer[bar + 1]
            else:
                value = MABuffer[bar] - maShift
        else:
            if MABuffer[bar + 1] < MABuffer[bar]:
                move = (MABuffer[bar] - MABuffer[bar + 1]) * speed
                value = MABuffer[bar + 1] - move - maShift
                beginPrice -= move
                MABuffer[bar] = MABuffer[bar + 1]
            else:
                value = MABuffer[bar] - maShift
        if isLong and value > Low[bar]:
            isLong = False
            beginPrice = maxPrice
            value = beginPrice
            beginBar = bar
            maxPrice = -999999.0
            minPrice = 999999.0
        elif (not isLong) and value < High[bar]:
            isLong = True
            beginPrice = minPrice
            value = beginPrice
            beginBar = bar
            maxPrice = -999999.0
            minPrice = 999999.0
        if isLong:
            UpBuffer[bar] = value
            DnBuffer[bar] = 0.0
        else:
            UpBuffer[bar] = 0.0
            DnBuffer[bar] = value
        if bar == 1:
            isLong_ = isLong
            maxPrice_ = maxPrice
            minPrice_ = minPrice
            beginPrice_ = beginPrice
            beginBar_ = beginBar
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if UpBuffer[bar + 1] > 0.0 and DnBuffer[bar] > 0.0:
            BuyBuffer[bar] = DnBuffer[bar]
        if DnBuffer[bar + 1] > 0.0 and UpBuffer[bar] > 0.0:
            SellBuffer[bar] = UpBuffer[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Brakema(_MQL5Indicator):
    name = 'brakema'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ma': 34,
        'speed': 0.0,
        'maType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=3),
    }

