"""Moving Average applied price — converted from MQL5: MQL5 Indicators/Moving Average applied price/Moving Average applied price.mq5

Copyright: Copyright © 2018, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [3145645]}, 'widths': {1: 3}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Moving Average applied price', 'source': 'MQL5 Indicators/Moving Average applied price/Moving Average applied price.mq5', 'folder': 'Moving Average applied price', 'inputs': [{'mql': 'Inp_MA_Period', 'py': 'Inp_MA_Period', 'param': 'Inp_MA_Period', 'type': 'int', 'default': 13, 'label': 'Period', 'sinput': False}, {'mql': 'Inp_MA_Shift', 'py': 'Inp_MA_Shift', 'param': 'Inp_MA_Shift', 'type': 'int', 'default': 0, 'label': 'Shift', 'sinput': False}, {'mql': 'Inp_MA_Method', 'py': 'Inp_MA_Method', 'param': 'Inp_MA_Method', 'type': 'int', 'default': 2, 'label': 'Method', 'sinput': False}, {'mql': 'Inp_MA_applied_price', 'py': 'Inp_MA_applied_price', 'param': 'Inp_MA_applied_price', 'type': 'int', 'default': 7, 'label': 'Type of price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Inp_MA_Period = _input('Inp_MA_Period', 13)  # Period
Inp_MA_Shift = _input('Inp_MA_Shift', 0)  # Shift
Inp_MA_Method = _input('Inp_MA_Method', MODE_SMMA)  # Method
Inp_MA_applied_price = _input('Inp_MA_applied_price', PRICE_WEIGHTED)  # Type of price
ExtLineBuffer = Arr(0, 0.0)
ExtPriceBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtPriceBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Inp_MA_Period)
    PlotIndexSetInteger(0, PLOT_SHIFT, Inp_MA_Shift)
    short_name = 'unknown ma'
    _sw1 = Inp_MA_Method
    if _sw1 == MODE_EMA:
        short_name = 'EMA'
    elif _sw1 == MODE_LWMA:
        short_name = 'LWMA'
    elif _sw1 == MODE_SMA:
        short_name = 'SMA'
    elif _sw1 == MODE_SMMA:
        short_name = 'SMMA'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name + '(' + _str(Inp_MA_Period) + ')')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Inp_MA_Period - 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < (Inp_MA_Period - 1):
        return 0
    limit = prev_calculated - 1
    if prev_calculated == 0:
        ArrayInitialize(ExtLineBuffer, 0)
        limit = 0
    for i in range(limit, rates_total):
        _sw2 = Inp_MA_applied_price
        if _sw2 == PRICE_CLOSE:
            ExtPriceBuffer[i] = close[i]
        elif _sw2 == PRICE_OPEN:
            ExtPriceBuffer[i] = open[i]
        elif _sw2 == PRICE_HIGH:
            ExtPriceBuffer[i] = high[i]
        elif _sw2 == PRICE_LOW:
            ExtPriceBuffer[i] = low[i]
        elif _sw2 == PRICE_MEDIAN:
            ExtPriceBuffer[i] = (high[i] + low[i]) / 2.0
        elif _sw2 == PRICE_TYPICAL:
            ExtPriceBuffer[i] = (high[i] + low[i] + close[i]) / 3.0
        elif _sw2 == PRICE_WEIGHTED:
            ExtPriceBuffer[i] = (high[i] + low[i] + (close[i] * 2.0)) / 4.0
    _sw3 = Inp_MA_Method
    if _sw3 == MODE_EMA:
        CalculateEMA(rates_total, prev_calculated, 0, ExtPriceBuffer)
    elif _sw3 == MODE_LWMA:
        CalculateLWMA(rates_total, prev_calculated, 0, ExtPriceBuffer)
    elif _sw3 == MODE_SMMA:
        CalculateSmoothedMA(rates_total, prev_calculated, 0, ExtPriceBuffer)
    elif _sw3 == MODE_SMA:
        CalculateSimpleMA(rates_total, prev_calculated, 0, ExtPriceBuffer)
    return rates_total

def CalculateSimpleMA(rates_total, prev_calculated, begin, price):
    i = 0
    limit = 0
    if prev_calculated == 0:
        limit = Inp_MA_Period + begin
        i = 0
        for i in range(i, limit - 1):
            ExtLineBuffer[i] = 0.0
        else:
            i = _range_end(i, limit - 1, 1)
        firstValue = 0.0
        i = begin
        for i in range(i, limit):
            firstValue += price[i]
        else:
            i = _range_end(i, limit, 1)
        firstValue = firstValue / Inp_MA_Period
        ExtLineBuffer[limit - 1] = firstValue
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        ExtLineBuffer[i] = ExtLineBuffer[i - 1] + ((price[i] - price[i - Inp_MA_Period]) / Inp_MA_Period)
    else:
        i = _range_end(i, rates_total, 1)

def CalculateEMA(rates_total, prev_calculated, begin, price):
    i = 0
    limit = 0
    SmoothFactor = _fdiv(2.0, 1.0 + Inp_MA_Period)
    if prev_calculated == 0:
        limit = Inp_MA_Period + begin
        ExtLineBuffer[begin] = price[begin]
        i = begin + 1
        for i in range(i, limit):
            ExtLineBuffer[i] = (price[i] * SmoothFactor) + (ExtLineBuffer[i - 1] * (1.0 - SmoothFactor))
        else:
            i = _range_end(i, limit, 1)
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        ExtLineBuffer[i] = (price[i] * SmoothFactor) + (ExtLineBuffer[i - 1] * (1.0 - SmoothFactor))
    else:
        i = _range_end(i, rates_total, 1)

def CalculateLWMA(rates_total, prev_calculated, begin, price):
    global _s_CalculateLWMA_weightsum
    i = 0
    limit = 0
    sum_ = 0.0
    if prev_calculated == 0:
        _s_CalculateLWMA_weightsum = 0
        limit = Inp_MA_Period + begin
        i = 0
        for i in range(i, limit):
            ExtLineBuffer[i] = 0.0
        else:
            i = _range_end(i, limit, 1)
        firstValue = 0.0
        i = begin
        for i in range(i, limit):
            k = i - begin + 1
            _s_CalculateLWMA_weightsum += k
            firstValue += k * price[i]
        else:
            i = _range_end(i, limit, 1)
        firstValue = _fdiv(firstValue, float(_s_CalculateLWMA_weightsum))
        ExtLineBuffer[limit - 1] = firstValue
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        sum_ = 0.0
        for j in range(0, Inp_MA_Period):
            sum_ += (Inp_MA_Period - j) * price[i - j]
        ExtLineBuffer[i] = _fdiv(sum_, _s_CalculateLWMA_weightsum)
    else:
        i = _range_end(i, rates_total, 1)

def CalculateSmoothedMA(rates_total, prev_calculated, begin, price):
    i = 0
    limit = 0
    if prev_calculated == 0:
        limit = Inp_MA_Period + begin
        i = 0
        for i in range(i, limit - 1):
            ExtLineBuffer[i] = 0.0
        else:
            i = _range_end(i, limit - 1, 1)
        firstValue = 0.0
        i = begin
        for i in range(i, limit):
            firstValue += price[i]
        else:
            i = _range_end(i, limit, 1)
        firstValue = firstValue / Inp_MA_Period
        ExtLineBuffer[limit - 1] = firstValue
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        ExtLineBuffer[i] = ((ExtLineBuffer[i - 1] * (Inp_MA_Period - 1)) + price[i]) / Inp_MA_Period
    else:
        i = _range_end(i, rates_total, 1)

# ---- static local variables
_s_CalculateLWMA_weightsum = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MovingAverageAppliedPrice(_MQL5Indicator):
    name = 'Moving Average applied price'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Inp_MA_Period': 13,  # Period
        'Inp_MA_Shift': 0,  # Shift
        'Inp_MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # Method
        'Inp_MA_applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=7),  # Type of price
    }

