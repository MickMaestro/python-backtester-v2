"""EveningStar — converted from MQL5: MQL5 Indicators/EveningStar/EveningStar.mq5

An \\"Evening Star\\" is a bearish candlestick pattern
Copyright: Copyright © 2017, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.005

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.005', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 5}, 'colors': {1: [32768]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'Evening Star'}, 'levels': [], 'description': ['An \\"Evening Star\\" is a bearish candlestick pattern'], 'name': 'EveningStar', 'source': 'MQL5 Indicators/EveningStar/EveningStar.mq5', 'folder': 'EveningStar', 'inputs': [{'mql': 'InpGap', 'py': 'InpGap', 'param': 'InpGap', 'type': 'bool', 'default': True, 'label': 'Gap. true -> gap is taken into account', 'sinput': False}, {'mql': 'InpCandle2Type', 'py': 'InpCandle2Type', 'param': 'InpCandle2Type', 'type': 'bool', 'default': True, 'label': 'Candle 2 type. true -> type of candle 2 is taken into account', 'sinput': False}, {'mql': 'InpCandleSizes', 'py': 'InpCandleSizes', 'param': 'InpCandleSizes', 'type': 'bool', 'default': True, 'label': 'Candle sizes. true -> candle sizes is taken into account', 'sinput': False}, {'mql': 'code', 'py': 'code', 'param': 'code', 'type': 'uchar', 'default': 74, 'label': 'Symbol code to draw in DRAW_ARROW', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpGap = _input('InpGap', True)  # Gap. true -> gap is taken into account
InpCandle2Type = _input('InpCandle2Type', True)  # Candle 2 type. true -> type of candle 2 is taken into account
InpCandleSizes = _input('InpCandleSizes', True)  # Candle sizes. true -> candle sizes is taken into account
code = _input('code', 74)  # Symbol code to draw in DRAW_ARROW
ArrowsBuffer = Arr(0, 0.0)
ExtDistance = 0.0  # minimum size of gap
m_adjusted_point = 0.0  # point value adjusted for 3 or 5 points

def OnInit():
    global ExtDistance, m_adjusted_point
    SetIndexBuffer(0, ArrowsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, code)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, -5)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(ArrowsBuffer, True)
    ArrayInitialize(ArrowsBuffer, 0.0)
    digits_adjust = 1
    if Digits() == 3 or Digits() == 5:
        digits_adjust = 10
    m_adjusted_point = Point() * digits_adjust
    ExtDistance = 1 * m_adjusted_point
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 10:
        return 0
    limit = rates_total - 1 - 3
    if prev_calculated == 0:
        ArrayInitialize(ArrowsBuffer, 0.0)
    else:
        limit = rates_total - prev_calculated
    for i in range(limit, 0, -1):
        if open[i + 0] > close[i + 0] and open[i + 2] < close[i + 2]:
            if InpCandleSizes:
                if MathAbs(open[i + 0] - close[i + 0]) < MathAbs(open[i + 1] - close[i + 1]) or MathAbs(open[i + 2] - close[i + 2]) < MathAbs(open[i + 1] - close[i + 1]):
                    ArrowsBuffer[i + 1] = 0.0
                    continue
            if InpCandle2Type:
                if open[i + 1] > close[i + 1]:
                    ArrowsBuffer[i + 1] = 0.0
                    continue
            else:
                if close[i + 1] > open[i + 1]:
                    ArrowsBuffer[i + 1] = 0.0
                    continue
            if InpGap:
                if open[i + 0] >= (close[i + 1] - ExtDistance) or open[i + 1] <= (close[i + 2] + ExtDistance):
                    ArrowsBuffer[i + 1] = 0.0
                    continue
            ArrowsBuffer[i + 1] = high[i + 1]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EveningStar(_MQL5Indicator):
    name = 'EveningStar'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpGap': True,  # Gap. true -> gap is taken into account
        'InpCandle2Type': True,  # Candle 2 type. true -> type of candle 2 is taken into account
        'InpCandleSizes': True,  # Candle sizes. true -> candle sizes is taken into account
        'code': 74,  # Symbol code to draw in DRAW_ARROW
    }

