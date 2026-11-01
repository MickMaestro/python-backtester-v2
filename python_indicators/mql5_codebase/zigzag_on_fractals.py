"""ZigZag on Fractals — converted from MQL5: MQL5 Indicators/ZigZag on Fractals/ZigZag on Fractals.mq5

\\"ZigZag\\" on the indicator \\"Fractals\\"
Copyright: Copyright © 2018, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 2.000

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '2.000', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 2}, 'colors': {1: [8721863]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Zigzag on Fractals'}, 'levels': [], 'description': ['\\"ZigZag\\" on the indicator \\"Fractals\\"'], 'name': 'ZigZag on Fractals', 'source': 'MQL5 Indicators/ZigZag on Fractals/ZigZag on Fractals.mq5', 'folder': 'ZigZag on Fractals', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ZigzagBuffer = Arr(0, 0.0)  # main buffer
FractalUpBuffer = Arr(0, 0.0)  # fractals up
FractalDownBuffer = Arr(0, 0.0)  # fractals down

def OnInit():
    SetIndexBuffer(0, ZigzagBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, FractalUpBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, FractalDownBuffer, INDICATOR_CALCULATIONS)
    short_name = StringFormat('ZigZag on Fractals(%s/%s)', Symbol(), EnumToString(Period(), ''))
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    limit = 0
    if rates_total < 5:
        return 0
    if prev_calculated < 7:
        limit = 2
        ArrayInitialize(ZigzagBuffer, EMPTY_VALUE)
        ArrayInitialize(FractalUpBuffer, EMPTY_VALUE)
        ArrayInitialize(FractalDownBuffer, EMPTY_VALUE)
    else:
        limit = rates_total - 5
    i = limit
    for i in range(i, rates_total - 3):
        if ((high[i] > high[i + 1] and high[i] > high[i + 2]) and high[i] >= high[i - 1]) and high[i] >= high[i - 2]:
            FractalUpBuffer[i] = high[i]
            fractal_buffer = Box(INT_MAX)
            price = Box(0.0)
            index_last_zigzag = SearchLastZigzag(i, fractal_buffer, price)
            if index_last_zigzag == -1 and (fractal_buffer.v != 0 or fractal_buffer.v != INT_MAX):
                ZigzagBuffer[i] = FractalUpBuffer[i]
            if index_last_zigzag != -1:
                if fractal_buffer.v == 1 and price.v < FractalUpBuffer[i]:
                    ZigzagBuffer[index_last_zigzag] = EMPTY_VALUE
                    ZigzagBuffer[i] = FractalUpBuffer[i]
                if fractal_buffer.v == -1:
                    ZigzagBuffer[i] = FractalUpBuffer[i]
        else:
            FractalUpBuffer[i] = EMPTY_VALUE
        if ((low[i] < low[i + 1] and low[i] < low[i + 2]) and low[i] <= low[i - 1]) and low[i] <= low[i - 2]:
            FractalDownBuffer[i] = low[i]
            fractal_buffer = Box(INT_MAX)
            price = Box(0.0)
            index_last_zigzag = SearchLastZigzag(i, fractal_buffer, price)
            if index_last_zigzag == -1 and (fractal_buffer.v != 0 or fractal_buffer.v != INT_MAX):
                ZigzagBuffer[i] = FractalDownBuffer[i]
            if index_last_zigzag != -1:
                if fractal_buffer.v == -1 and price.v > FractalDownBuffer[i]:
                    ZigzagBuffer[index_last_zigzag] = EMPTY_VALUE
                    ZigzagBuffer[i] = FractalDownBuffer[i]
                if fractal_buffer.v == 1:
                    ZigzagBuffer[i] = FractalDownBuffer[i]
        else:
            FractalDownBuffer[i] = EMPTY_VALUE
        if (FractalUpBuffer[i] == EMPTY_VALUE or FractalUpBuffer[i] == 0.0) and (FractalDownBuffer[i] == EMPTY_VALUE or FractalDownBuffer[i] == 0.0):
            ZigzagBuffer[i] = EMPTY_VALUE
    else:
        i = _range_end(i, rates_total - 3, 1)
    ZigzagBuffer[rates_total - 3] = EMPTY_VALUE
    ZigzagBuffer[rates_total - 2] = EMPTY_VALUE
    ZigzagBuffer[rates_total - 1] = EMPTY_VALUE
    return rates_total

def SearchLastZigzag(start, fractal_buffer, price):
    if start <= 0:
        Print('Parameter "start" can\'t be less or is equal to zero')
        return -1
    for i in range(start, 0 - 1, -1):
        if ZigzagBuffer[i] != EMPTY_VALUE and ZigzagBuffer[i] != 0.0:
            if FractalUpBuffer[i] != EMPTY_VALUE and FractalUpBuffer[i] != 0.0:
                fractal_buffer.v = 1
                price.v = FractalUpBuffer[i]
            if FractalDownBuffer[i] != EMPTY_VALUE and FractalDownBuffer[i] != 0.0:
                fractal_buffer.v = -1
                price.v = FractalDownBuffer[i]
            if (FractalUpBuffer[i] != EMPTY_VALUE and FractalUpBuffer[i] != 0.0) and (FractalDownBuffer[i] != EMPTY_VALUE and FractalDownBuffer[i] != 0.0):
                fractal_buffer.v = 0
                return -1
            return i
    return -1

def OnDeinit(reason):
    Comment('')


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ZigZagOnFractals(_MQL5Indicator):
    name = 'ZigZag on Fractals'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

