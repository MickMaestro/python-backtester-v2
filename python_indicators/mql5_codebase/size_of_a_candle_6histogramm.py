"""Size_of_a_candle_6histogramm — converted from MQL5: MQL5 Indicators/Size of a candle (histogram)/Size_of_a_candle_6histogramm.mq5

Size of a candle (histogram)
Copyright: Copyright © 2017, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.001

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.001', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [16711680, 255]}, 'widths': {1: 3}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Size of a candle (histogram)'], 'name': 'Size_of_a_candle_6histogramm', 'source': 'MQL5 Indicators/Size of a candle (histogram)/Size_of_a_candle_6histogramm.mq5', 'folder': 'Size of a candle (histogram)', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Size of a candle'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    ArraySetAsSeries(ExtBuffer, False)
    ArraySetAsSeries(ExtColorBuffer, False)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(time, False)
    ArraySetAsSeries(open, False)
    ArraySetAsSeries(high, False)
    ArraySetAsSeries(low, False)
    ArraySetAsSeries(close, False)
    limit = -1
    if prev_calculated == 0:
        limit = 0
    else:
        limit = prev_calculated - 1
    for i in range(limit, rates_total):
        calculations = high[i] - low[i]
        close_or_open = (True if ((close[i] - open[i]) > 0) else False)
        ExtBuffer[i] = (calculations if close_or_open else (-calculations))
        ExtColorBuffer[i] = (0 if ((close[i] - open[i]) > 0) else 1)
        g = 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SizeOfACandle6histogramm(_MQL5Indicator):
    name = 'Size_of_a_candle_6histogramm'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

