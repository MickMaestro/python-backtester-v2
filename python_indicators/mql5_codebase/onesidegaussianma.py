"""onesidegaussianma — converted from MQL5: MQL5 Indicators/OneSideGaussianMA/onesidegaussianma.mq5

Moving Average on the basis of Gauss algorithm
Copyright: Copyright © 2007, Tinytjan; Link: tinytjan@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Tinytjan', 'link': 'tinytjan@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [9639167, 8421504, 15624315]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'OneSideGaussianMA'}, 'levels': [], 'description': ['Moving Average on the basis of Gauss algorithm'], 'name': 'onesidegaussianma', 'source': 'MQL5 Indicators/OneSideGaussianMA/onesidegaussianma.mq5', 'folder': 'OneSideGaussianMA', 'inputs': [{'mql': 'SmoothType', 'py': 'SmoothType', 'param': 'SmoothType', 'type': 'int', 'default': 5, 'label': 'type of averaging', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum SmoothMode
Smooth1 = 0
Smooth2 = 1
Smooth3 = 2
Smooth4 = 3
Smooth5 = 4
Smooth6 = 5
Smooth7 = 6
Smooth8 = 7
_enum('SmoothMode', {0: 'Smooth1', 1: 'Smooth2', 2: 'Smooth3', 3: 'Smooth4', 4: 'Smooth5', 5: 'Smooth6', 6: 'Smooth7', 7: 'Smooth8'})

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
levels = Arr.of([1, 2, 3, 5, 8, 13, 21, 34], fill=0)
GaussianBuffer = Arr(0, 0.0, dims=(8,))
SmoothType = _input('SmoothType', Smooth6)  # type of averaging
IPC = _input('IPC', PRICE_CLOSE_)  # price constant
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0

def Gaussian(Size, X):
    return MathExp(_idiv((-X) * X * 9, (Size + 1) * (Size + 1)))

def GaussianInit():
    ArrayResize(GaussianBuffer, 34)
    for k in range(0, 8):
        sum_ = 0.0
        for i in range(0, 34):
            if i >= levels[k]:
                break
            GaussianBuffer[i][k] = Gaussian(levels[k], i)
            sum_ += GaussianBuffer[i][k]
        for i in range(0, 34):
            if i >= levels[k]:
                break
            GaussianBuffer[i][k] = _fdiv(GaussianBuffer[i][k], sum_)

def Smooth(level, Rates_total, PriceMode, index, Open, Low, High, Close):
    sum_ = 0.0
    limit = levels[level]
    if index >= (Rates_total - limit):
        return CountPrice(PriceMode, index, Open, Low, High, Close)
    for i in range(0, limit):
        sum_ += GaussianBuffer[i][level] * CountPrice(PriceMode, index + i, Open, Low, High, Close)
    return sum_

def SmoothArray(level, array, Rates_total, PriceMode, index):
    sum_ = 0.0
    limit = levels[level]
    if index >= (Rates_total - limit):
        return array[index]
    for i in range(0, limit):
        sum_ += GaussianBuffer[i][level] * array[index + i]
    return sum_

def CountPrice(PriceMode, index, Open, Low, High, Close):
    _sw1 = PriceMode
    if _sw1 == PRICE_CLOSE:
        return Close[index]
    elif _sw1 == PRICE_OPEN:
        return Open[index]
    elif _sw1 == PRICE_HIGH:
        return High[index]
    elif _sw1 == PRICE_LOW:
        return Low[index]
    elif _sw1 == PRICE_MEDIAN:
        return (High[index] + Low[index]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (Close[index] + High[index] + Low[index]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return ((2 * Close[index]) + High[index] + Low[index]) / 4.0
    elif _sw1 == 8:
        return (Open[index] + Close[index]) / 2.0
    elif _sw1 == 9:
        return (Open[index] + Close[index] + High[index] + Low[index]) / 4.0
    elif _sw1 == 10:
        if Close[index] > Open[index]:
            return High[index]
        else:
            if Close[index] < Open[index]:
                return Low[index]
            else:
                return Close[index]
    elif _sw1 == 11:
        if Close[index] > Open[index]:
            return (High[index] + Close[index]) / 2.0
        else:
            if Close[index] < Open[index]:
                return (Low[index] + Close[index]) / 2.0
            else:
                return Close[index]
    elif _sw1 == 12:
        res = High[index] + Low[index] + Close[index]
        if Close[index] < Open[index]:
            res = (res + Low[index]) / 2
        if Close[index] > Open[index]:
            res = (res + High[index]) / 2
        if Close[index] == Open[index]:
            res = (res + Close[index]) / 2
        return (res - Low[index] + (res - High[index])) / 2
    else:
        return Close[index]

def OnInit():
    global min_rates_total
    min_rates_total = (34 * 2) + 1
    GaussianInit()
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ColorIndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'One side Gaussian MA (', EnumToString(SmoothType, 'SmoothMode'), ', ', EnumToString(IPC, 'Applied_price_'), ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IndBuffer[bar] = Smooth(SmoothType, rates_total, IPC, bar, open, low, high, close)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if IndBuffer[bar + 1] < IndBuffer[bar]:
            ColorIndBuffer[bar] = 2.0
        elif IndBuffer[bar + 1] > IndBuffer[bar]:
            ColorIndBuffer[bar] = 0.0
        else:
            ColorIndBuffer[limit] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Onesidegaussianma(_MQL5Indicator):
    name = 'onesidegaussianma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SmoothType': _Choice({0: 'Smooth1', 1: 'Smooth2', 2: 'Smooth3', 3: 'Smooth4', 4: 'Smooth5', 5: 'Smooth6', 6: 'Smooth7', 7: 'Smooth8'}, default=5),  # type of averaging
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # price constant
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

