"""sr-rateindicator — converted from MQL5: MQL5 Indicators/SR-RateIndicator/sr-rateindicator.mq5

Copyright: Copyright © 2007, Tinytjan; Link: tinytjan@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Tinytjan', 'link': 'tinytjan@mail.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16711935, 8388736, 8421504, 8421376, 65407]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'SR-Rate'}, 'levels': [], 'description': [], 'name': 'sr-rateindicator', 'source': 'MQL5 Indicators/SR-RateIndicator/sr-rateindicator.mq5', 'folder': 'SR-RateIndicator', 'inputs': [{'mql': 'WindowSize', 'py': 'WindowSize', 'param': 'WindowSize', 'type': 'uint', 'default': 20, 'label': 'window width', 'sinput': False}, {'mql': 'inHighLevel', 'py': 'inHighLevel', 'param': 'inHighLevel', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'inLowLevel', 'py': 'inLowLevel', 'param': 'inLowLevel', 'type': 'int', 'default': -20, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
WindowSize = _input('WindowSize', 20)  # window width
inHighLevel = _input('inHighLevel', 20)
inLowLevel = _input('inLowLevel', -20)
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
GaussianBuffer_1 = Arr(22, 0.0, dyn=False)
GaussianBuffer_2 = Arr(22, 0.0, dyn=False)
GaussianBuffer_3 = Arr(22, 0.0, dyn=False)
GaussianBuffer_5 = Arr(22, 0.0, dyn=False)
GaussianBuffer_8 = Arr(22, 0.0, dyn=False)
GaussianBuffer_13 = Arr(22, 0.0, dyn=False)
GaussianBuffer_21 = Arr(22, 0.0, dyn=False)

def Gaussian(Size, X):
    return MathExp(_idiv((-X) * X * 9, (Size + 1) * (Size + 1)))

def BuffersInit():
    i = 0
    i = 0
    for i in range(i, 22 - 1):
        GaussianBuffer_1[i] = 0.0
        GaussianBuffer_2[i] = 0.0
        GaussianBuffer_3[i] = 0.0
        GaussianBuffer_5[i] = 0.0
        GaussianBuffer_8[i] = 0.0
        GaussianBuffer_13[i] = 0.0
        GaussianBuffer_21[i] = 0.0
    else:
        i = _range_end(i, 22 - 1, 1)
    i = 0
    for i in range(i, 1):
        GaussianBuffer_1[i] = Gaussian(1, i)
    else:
        i = _range_end(i, 1, 1)
    i = 0
    for i in range(i, 2):
        GaussianBuffer_2[i] = Gaussian(2, i)
    else:
        i = _range_end(i, 2, 1)
    i = 0
    for i in range(i, 3):
        GaussianBuffer_3[i] = Gaussian(3, i)
    else:
        i = _range_end(i, 3, 1)
    i = 0
    for i in range(i, 5):
        GaussianBuffer_5[i] = Gaussian(5, i)
    else:
        i = _range_end(i, 5, 1)
    i = 0
    for i in range(i, 8):
        GaussianBuffer_8[i] = Gaussian(8, i)
    else:
        i = _range_end(i, 8, 1)
    i = 0
    for i in range(i, 13):
        GaussianBuffer_13[i] = Gaussian(13, i)
    else:
        i = _range_end(i, 13, 1)
    i = 0
    for i in range(i, 21):
        GaussianBuffer_21[i] = Gaussian(21, i)
    else:
        i = _range_end(i, 21, 1)
    sum_ = 0.0
    sum_ = 0.0
    i = 0
    for i in range(i, 1):
        sum_ += GaussianBuffer_1[i]
    else:
        i = _range_end(i, 1, 1)
    i = 0
    for i in range(i, 1):
        GaussianBuffer_1[i] = _fdiv(GaussianBuffer_1[i], sum_)
    else:
        i = _range_end(i, 1, 1)
    sum_ = 0.0
    i = 0
    for i in range(i, 2):
        sum_ += GaussianBuffer_2[i]
    else:
        i = _range_end(i, 2, 1)
    i = 0
    for i in range(i, 2):
        GaussianBuffer_2[i] = _fdiv(GaussianBuffer_2[i], sum_)
    else:
        i = _range_end(i, 2, 1)
    sum_ = 0.0
    i = 0
    for i in range(i, 3):
        sum_ += GaussianBuffer_3[i]
    else:
        i = _range_end(i, 3, 1)
    i = 0
    for i in range(i, 3):
        GaussianBuffer_3[i] = _fdiv(GaussianBuffer_3[i], sum_)
    else:
        i = _range_end(i, 3, 1)
    sum_ = 0.0
    i = 0
    for i in range(i, 5):
        sum_ += GaussianBuffer_5[i]
    else:
        i = _range_end(i, 5, 1)
    i = 0
    for i in range(i, 5):
        GaussianBuffer_5[i] = _fdiv(GaussianBuffer_5[i], sum_)
    else:
        i = _range_end(i, 5, 1)
    sum_ = 0.0
    i = 0
    for i in range(i, 8):
        sum_ += GaussianBuffer_8[i]
    else:
        i = _range_end(i, 8, 1)
    i = 0
    for i in range(i, 8):
        GaussianBuffer_8[i] = _fdiv(GaussianBuffer_8[i], sum_)
    else:
        i = _range_end(i, 8, 1)
    sum_ = 0.0
    i = 0
    for i in range(i, 13):
        sum_ += GaussianBuffer_13[i]
    else:
        i = _range_end(i, 13, 1)
    i = 0
    for i in range(i, 13):
        GaussianBuffer_13[i] = _fdiv(GaussianBuffer_13[i], sum_)
    else:
        i = _range_end(i, 13, 1)
    sum_ = 0.0
    i = 0
    for i in range(i, 21):
        sum_ += GaussianBuffer_21[i]
    else:
        i = _range_end(i, 21, 1)
    i = 0
    for i in range(i, 21):
        GaussianBuffer_21[i] = _fdiv(GaussianBuffer_21[i], sum_)
    else:
        i = _range_end(i, 21, 1)

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

def Smooth_1(Rates_total, PriceMode, index, Open, Low, High, Close):
    if Rates_total <= (index + 1):
        return 0.0
    sum_ = 0.0
    for i in range(0, 1 + 1):
        sum_ += GaussianBuffer_1[i] * CountPrice(PriceMode, i + index, Open, Low, High, Close)
    return sum_

def Smooth_2(Rates_total, PriceMode, index, Open, Low, High, Close):
    if Rates_total <= (index + 2):
        return 0.0
    sum_ = 0.0
    for i in range(0, 2 + 1):
        sum_ += GaussianBuffer_2[i] * CountPrice(PriceMode, i + index, Open, Low, High, Close)
    return sum_

def Smooth_3(Rates_total, PriceMode, index, Open, Low, High, Close):
    if Rates_total <= (index + 3):
        return 0.0
    sum_ = 0.0
    for i in range(0, 3 + 1):
        sum_ += GaussianBuffer_3[i] * CountPrice(PriceMode, i + index, Open, Low, High, Close)
    return sum_

def Smooth_5(Rates_total, PriceMode, index, Open, Low, High, Close):
    if Rates_total <= (index + 5):
        return 0.0
    sum_ = 0.0
    for i in range(0, 5 + 1):
        sum_ += GaussianBuffer_5[i] * CountPrice(PriceMode, i + index, Open, Low, High, Close)
    return sum_

def Smooth_8(Rates_total, PriceMode, index, Open, Low, High, Close):
    if Rates_total <= (index + 8):
        return 0.0
    sum_ = 0.0
    for i in range(0, 8 + 1):
        sum_ += GaussianBuffer_8[i] * CountPrice(PriceMode, i + index, Open, Low, High, Close)
    return sum_

def Smooth_13(Rates_total, PriceMode, index, Open, Low, High, Close):
    if Rates_total <= (index + 13):
        return 0.0
    sum_ = 0.0
    for i in range(0, 13 + 1):
        sum_ += GaussianBuffer_13[i] * CountPrice(PriceMode, i + index, Open, Low, High, Close)
    return sum_

def Smooth_21(Rates_total, PriceMode, index, Open, Low, High, Close):
    if Rates_total <= (index + 21):
        return 0.0
    sum_ = 0.0
    for i in range(0, 21 + 1):
        sum_ += GaussianBuffer_21[i] * CountPrice(PriceMode, i + index, Open, Low, High, Close)
    return sum_

def OnInit():
    global min_rates_total
    min_rates_total = _int(WindowSize)
    BuffersInit()
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SR-Rate Indicator')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, inHighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, inLowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    clr = 0
    Max = 0.0
    Min = 0.0
    Range = 0.0
    slow = 0.0
    shigh = 0.0
    res = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        IndBuffer[limit + 1] = 0.0
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Max = 0.0
        Min = 999999999.0
        for kkk in range(bar, _int(bar + WindowSize)):
            slow = Smooth_5(rates_total, PRICE_LOW, kkk, open, low, high, close)
            if slow < Min:
                Min = slow
            shigh = Smooth_5(rates_total, PRICE_HIGH, kkk, open, low, high, close)
            if shigh > Max:
                Max = shigh
        Range = Max - Min
        if Range:
            res = _fdiv(200 * (Smooth_5(rates_total, PRICE_WEIGHTED, bar, open, low, high, close) - Min), Range) - 100.0
        else:
            res = 0.0
        IndBuffer[bar] = res
        clr = 2
        if res > 0:
            if res > inHighLevel:
                clr = 4
            else:
                clr = 3
        if res < 0:
            if res < inLowLevel:
                clr = 0
            else:
                clr = 1
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SrRateindicator(_MQL5Indicator):
    name = 'sr-rateindicator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'WindowSize': 20,  # window width
        'inHighLevel': 20,
        'inLowLevel': -20,
    }

