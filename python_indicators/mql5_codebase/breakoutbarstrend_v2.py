"""breakoutbarstrend_v2 — converted from MQL5: MQL5 Indicators/Breakout Bars Trend v2/breakoutbarstrend_v2.mq5

The alternative indicator to determine the trend based on the breakthrough bars and the distance from extremums.
Copyright: Copyright 2012, Rone.; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, Rone.', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 4}, 'types': {1: 0, 2: 17, 3: 5, 4: 5}, 'colors': {1: [255], 2: [16711680, 14772545, 16760576, 255, 4678655, 42495], 3: [16748574], 4: [4678655]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'BBT Values', 2: 'BBT Open;BBT High;BBT Low;BBT Close', 3: 'Reverse To Down', 4: 'Reverse To Up'}, 'levels': [], 'description': ['The alternative indicator to determine the trend based on the breakthrough bars and the distance from extremums.'], 'name': 'breakoutbarstrend_v2', 'source': 'MQL5 Indicators/Breakout Bars Trend v2/breakoutbarstrend_v2.mq5', 'folder': 'Breakout Bars Trend v2', 'inputs': [{'mql': 'InpReversal', 'py': 'InpReversal', 'param': 'InpReversal', 'type': 'int', 'default': 0, 'label': 'Reversal', 'sinput': False}, {'mql': 'InpDelta', 'py': 'InpDelta', 'param': 'InpDelta', 'type': 'double', 'default': 1000.0, 'label': 'Delta', 'sinput': False}, {'mql': 'InpShowReverseLevels', 'py': 'InpShowReverseLevels', 'param': 'InpShowReverseLevels', 'type': 'bool', 'default': True, 'label': 'Show the reversal levels', 'sinput': False}, {'mql': 'InpShowTrendsInfo', 'py': 'InpShowTrendsInfo', 'param': 'InpShowTrendsInfo', 'type': 'bool', 'default': True, 'label': 'Show the trends info', 'sinput': False}, {'mql': 'InpTrendsQuantity', 'py': 'InpTrendsQuantity', 'param': 'InpTrendsQuantity', 'type': 'int', 'default': 5, 'label': 'Number of trends', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum REVERSAL_MODE
PIPS = 0
PERCENT = 1
_enum('REVERSAL_MODE', {0: 'PIPS', 1: 'PERCENT'})

# ---- inputs and global variables
InpReversal = _input('InpReversal', PIPS)  # Reversal
InpDelta = _input('InpDelta', 1000.0)  # Delta
InpShowReverseLevels = _input('InpShowReverseLevels', True)  # Show the reversal levels
InpShowTrendsInfo = _input('InpShowTrendsInfo', True)  # Show the trends info
InpTrendsQuantity = _input('InpTrendsQuantity', 5)  # Number of trends
ValuesBuffer = Arr(0, 0.0)
OpenBuffer = Arr(0, 0.0)
HighBuffer = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)
CloseBuffer = Arr(0, 0.0)
ColorsBuffer = Arr(0, 0.0)
ReverseToDownBuffer = Arr(0, 0.0)
ReverseToUpBuffer = Arr(0, 0.0)
minRequiredBars = 0
quantity = 0
delta = 0.0

class bbtData(MqlObject):
    _q_fields = ('value', 'result', 'firstPrice')
    def __init__(self, *args):
        self.value = 0
        self.result = 0
        self.firstPrice = 0.0

def OnInit():
    global delta, minRequiredBars, quantity
    minRequiredBars = 2
    delta = InpDelta
    if InpReversal == PIPS:
        if InpDelta < 30:
            delta = 1000.0
            printf('The "Delta" parameter is specified incorrectly: %d. the: %d. value will be used', _int(InpDelta), _int(delta))
        delta *= Point()
    else:
        if InpDelta < 0.03 or InpDelta > 30.0:
            delta = 1.0
            printf('The "Delta" parameter is specified incorrectly: %f. the: %f. value will be used', InpDelta, delta)
    if InpShowTrendsInfo:
        if InpTrendsQuantity < 2 or InpTrendsQuantity > 20:
            quantity = 5
            printf('The "Number of series" parameter is specified incorrectly: %d. the: %d. value will be used', InpTrendsQuantity, quantity)
        else:
            quantity = InpTrendsQuantity
    SetIndexBuffer(0, ValuesBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, OpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, HighBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, LowBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, CloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ColorsBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, ReverseToDownBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, ReverseToUpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    for i in range(0, 4):
        PlotIndexSetInteger(i, PLOT_DRAW_BEGIN, minRequiredBars)
        PlotIndexSetInteger(i, PLOT_SHIFT, 0)
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    modeData = ((DoubleToString(InpDelta, 0) + ' pips') if (InpReversal == PIPS) else (DoubleToString(InpDelta, 2) + '%'))
    IndicatorSetString(INDICATOR_SHORTNAME, 'Breakout Bars Trend v2 (' + modeData + ')')
    return 0

def OnDeinit(reason):
    Comment('')

def getReversal(price):
    if InpReversal == PIPS:
        return delta
    return NormalizeDouble((price / 100) * delta, Digits())

def calculateTrendsInfo(data, bar, price, qty):
    curPrice = price[bar]
    data[0].value = _int(ValuesBuffer[bar])
    i = 1
    while i < qty and bar > 0:
        if (ValuesBuffer[bar - 1] * ValuesBuffer[bar]) < 0:
            data[i].value = _int(ValuesBuffer[bar - 1])
            data[i - 1].firstPrice = price[bar]
            calculateResult(data[i - 1], curPrice)
            curPrice = price[bar]
            i += 1
        bar -= 1
    while bar > 0:
        if (ValuesBuffer[bar - 1] * ValuesBuffer[bar]) < 0:
            data[qty - 1].firstPrice = price[bar]
            calculateResult(data[qty - 1], curPrice)
            break
        bar -= 1

def calculateResult(data, price):
    if data.value > 0:
        data.result = _int(_fdiv(price - data.firstPrice, Point()))
    else:
        data.result = _int(_fdiv(data.firstPrice - price, Point()))

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate__maxPrice, _s_OnCalculate__minPrice, _s_OnCalculate__upTrend
    startBar = 0
    lastBar = 0
    upTrend = False
    minPrice = 0.0
    maxPrice = 0.0
    reversal = 0.0
    lastBar = rates_total - 1
    if prev_calculated > rates_total or prev_calculated <= 0:
        ArrayInitialize(ReverseToDownBuffer, 0.0)
        ArrayInitialize(ReverseToUpBuffer, 0.0)
        reversal = getReversal(close[0])
        startBar = 1
        while (MathAbs(close[startBar] - close[0]) - reversal) <= 1e-05:
            pass
            startBar += 1
        for bar in range(0, startBar):
            ValuesBuffer[bar] = 0.0
            OpenBuffer[bar] = 0.0
            HighBuffer[bar] = 0.0
            LowBuffer[bar] = 0.0
            CloseBuffer[bar] = 0.0
            ReverseToDownBuffer[bar] = 0.0
            ReverseToUpBuffer[bar] = 0.0
        if close[startBar] > close[0]:
            ValuesBuffer[startBar] = 1.0
            _s_OnCalculate__upTrend = True
            _s_OnCalculate__minPrice = low[0]
            _s_OnCalculate__maxPrice = high[startBar]
        else:
            ValuesBuffer[startBar] = -1.0
            _s_OnCalculate__upTrend = False
            _s_OnCalculate__minPrice = low[startBar]
            _s_OnCalculate__maxPrice = high[0]
    else:
        startBar = prev_calculated - 1
    upTrend = _s_OnCalculate__upTrend
    minPrice = _s_OnCalculate__minPrice
    maxPrice = _s_OnCalculate__maxPrice
    for bar in range(startBar, rates_total):
        prevBar = bar - 1
        minPrice = MathMin(minPrice, low[prevBar])
        maxPrice = MathMax(maxPrice, high[prevBar])
        if prev_calculated != rates_total and bar == lastBar:
            if (ValuesBuffer[prevBar] * ValuesBuffer[prevBar - 1]) < 0:
                minPrice = low[prevBar]
                maxPrice = high[prevBar]
            _s_OnCalculate__upTrend = upTrend
            _s_OnCalculate__minPrice = minPrice
            _s_OnCalculate__maxPrice = maxPrice
        OpenBuffer[bar] = open[bar]
        HighBuffer[bar] = high[bar]
        LowBuffer[bar] = low[bar]
        CloseBuffer[bar] = close[bar]
        if upTrend:
            reversal = getReversal(maxPrice)
            if close[bar] > maxPrice:
                ValuesBuffer[bar] = ValuesBuffer[prevBar] + 1
                ColorsBuffer[bar] = 0.0
            elif close[bar] < (MathMax(maxPrice, high[bar]) - reversal) and close[bar] < low[prevBar]:
                upTrend = False
                ValuesBuffer[bar] = -1.0
                ColorsBuffer[bar] = 3.0
                if bar != lastBar:
                    maxPrice = high[bar]
                    minPrice = low[bar]
            else:
                ValuesBuffer[bar] = ValuesBuffer[prevBar]
                if close[bar] >= open[bar]:
                    ColorsBuffer[bar] = 1.0
                else:
                    ColorsBuffer[bar] = 2.0
        else:
            reversal = getReversal(minPrice)
            if close[bar] < minPrice:
                ValuesBuffer[bar] = ValuesBuffer[prevBar] - 1
                ColorsBuffer[bar] = 3.0
            elif close[bar] > (MathMin(minPrice, low[bar]) + reversal) and close[bar] > high[prevBar]:
                upTrend = True
                ValuesBuffer[bar] = 1.0
                ColorsBuffer[bar] = 0.0
                if bar != lastBar:
                    minPrice = low[bar]
                    maxPrice = high[bar]
            else:
                ValuesBuffer[bar] = ValuesBuffer[prevBar]
                if close[bar] >= open[bar]:
                    ColorsBuffer[bar] = 5.0
                else:
                    ColorsBuffer[bar] = 4.0
        if InpShowReverseLevels:
            if upTrend:
                ReverseToDownBuffer[bar] = maxPrice - reversal
                ReverseToUpBuffer[bar] = 0.0
            else:
                ReverseToDownBuffer[bar] = 0.0
                ReverseToUpBuffer[bar] = minPrice + reversal
    if InpShowTrendsInfo:
        trendsData = Arr(0, 0, factory=bbtData)
        ArrayResize(trendsData, quantity)
        calculateTrendsInfo(trendsData, lastBar, close, quantity)
        comm = 'Trends Info:\n'
        for i in range(quantity - 1, 0 - 1, -1):
            comm += _str(trendsData[i].value) + ':  ' + _str(trendsData[i].result) + ' pips\n'
        Comment(comm)
    return rates_total

# ---- static local variables
_s_OnCalculate__upTrend = False
_s_OnCalculate__minPrice = 0.0
_s_OnCalculate__maxPrice = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BreakoutbarstrendV2(_MQL5Indicator):
    name = 'breakoutbarstrend_v2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpReversal': _Choice({0: 'In pips', 1: 'In percentage'}, default=0),  # Reversal
        'InpDelta': 1000.0,  # Delta
        'InpShowReverseLevels': True,  # Show the reversal levels
        'InpShowTrendsInfo': True,  # Show the trends info
        'InpTrendsQuantity': 5,  # Number of trends
    }

