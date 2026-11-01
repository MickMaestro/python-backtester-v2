"""ytg_japan_candles — converted from MQL5: MQL5 Indicators/ytg_Japan_Candles/ytg_japan_candles.mq5

Indicator of candle combinations
Copyright: Copyright © 2009, Yuriy Tokman; Link: yuriytokman@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, Yuriy Tokman', 'link': 'yuriytokman@gmail.com', 'window': 'chart', 'indicator_buffers': 9, 'indicator_plots': 9}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5}, 'colors': {1: [65280], 2: [65280], 3: [65280], 4: [65280], 5: [16711680], 6: [16711935], 7: [16711935], 8: [16711935], 9: [16711935]}, 'widths': {1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 3, 8: 3, 9: 3}, 'styles': {}, 'labels': {1: "Bull's hammer", 2: "Bull's absorbtion", 3: "Bull's curtain of dark clouds", 4: "Bull's clearance in the clouds", 5: 'Dodge', 6: "Bear's clearance in the clouds", 7: "Bear's curtain of dark clouds", 8: "Bear's absorbtion", 9: "Bear's hammer"}, 'levels': [], 'description': ['Indicator of candle combinations'], 'name': 'ytg_japan_candles', 'source': 'MQL5 Indicators/ytg_Japan_Candles/ytg_japan_candles.mq5', 'folder': 'ytg_Japan_Candles', 'inputs': [{'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
IndBuffer1 = Arr(0, 0.0)
IndBuffer2 = Arr(0, 0.0)
IndBuffer3 = Arr(0, 0.0)
IndBuffer4 = Arr(0, 0.0)
IndBuffer5 = Arr(0, 0.0)
IndBuffer6 = Arr(0, 0.0)
IndBuffer7 = Arr(0, 0.0)
IndBuffer8 = Arr(0, 0.0)
IndBuffer9 = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 2
    IndicatorInit(0, Shift, min_rates_total, EMPTY_VALUE, 170, IndBuffer1)
    IndicatorInit(1, Shift, min_rates_total, EMPTY_VALUE, 110, IndBuffer2)
    IndicatorInit(2, Shift, min_rates_total, EMPTY_VALUE, 116, IndBuffer3)
    IndicatorInit(3, Shift, min_rates_total, EMPTY_VALUE, 163, IndBuffer4)
    IndicatorInit(4, Shift, min_rates_total, EMPTY_VALUE, 174, IndBuffer5)
    IndicatorInit(5, Shift, min_rates_total, EMPTY_VALUE, 163, IndBuffer6)
    IndicatorInit(6, Shift, min_rates_total, EMPTY_VALUE, 116, IndBuffer7)
    IndicatorInit(7, Shift, min_rates_total, EMPTY_VALUE, 110, IndBuffer8)
    IndicatorInit(8, Shift, min_rates_total, EMPTY_VALUE, 170, IndBuffer9)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ytg_Japan_Candles')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def IndicatorInit(number, shift, drawbegin, empty_value, arrow, Arrow):
    SetIndexBuffer(number, Arrow, INDICATOR_DATA)
    PlotIndexSetInteger(number, PLOT_SHIFT, shift)
    PlotIndexSetInteger(number, PLOT_DRAW_BEGIN, drawbegin)
    PlotIndexSetDouble(number, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(number, PLOT_ARROW, arrow)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    k = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total - 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        IndBuffer1[bar] = EMPTY_VALUE
        IndBuffer2[bar] = EMPTY_VALUE
        IndBuffer3[bar] = EMPTY_VALUE
        IndBuffer4[bar] = EMPTY_VALUE
        IndBuffer5[bar] = EMPTY_VALUE
        IndBuffer6[bar] = EMPTY_VALUE
        IndBuffer7[bar] = EMPTY_VALUE
        IndBuffer8[bar] = EMPTY_VALUE
        IndBuffer9[bar] = EMPTY_VALUE
        k = (High[bar] - Low[bar]) / 3
        if Open[bar] > (Low[bar] + (2 * k)) and Close[bar] > (Low[bar] + (2 * k)):
            IndBuffer9[bar] = High[bar] + (10 * Point())
        if Open[bar] < (High[bar] - (2 * k)) and Close[bar] < (High[bar] + (2 * k)):
            IndBuffer1[bar] = Low[bar] - (10 * Point())
        if (Open[bar - 1] > Close[bar - 1] and Close[bar - 1] > Open[bar]) and Close[bar] > Open[bar - 1]:
            IndBuffer2[bar] = Low[bar] - (15 * Point())
        if (Close[bar - 1] > Open[bar - 1] and Open[bar] > Close[bar - 1]) and Open[bar - 1] > Close[bar]:
            IndBuffer8[bar] = High[bar] + (15 * Point())
        if (Open[bar - 1] < Close[bar - 1] and Open[bar] > High[bar - 1]) and Close[bar] < (Open[bar - 1] + ((Close[bar - 1] - Open[bar - 1]) / 2)):
            IndBuffer3[bar] = Low[bar] - (25 * Point())
        if (Open[bar - 1] > Close[bar - 1] and Open[bar] < Low[bar - 1]) and Close[bar] < (Open[bar - 1] + ((Close[bar - 1] - Open[bar - 1]) / 2)):
            IndBuffer7[bar] = High[bar] + (25 * Point())
        if (Open[bar - 1] > Close[bar - 1] and High[bar - 1] > Open[bar]) and Close[bar] > (Close[bar - 1] + ((Open[bar - 1] - Close[bar - 1]) / 2)):
            IndBuffer4[bar] = Low[bar] - (25 * Point())
        if (Open[bar - 1] < Close[bar - 1] and Low[bar - 1] < Open[bar]) and Close[bar] < (Close[bar - 1] + ((Open[bar - 1] - Close[bar - 1]) / 2)):
            IndBuffer6[bar] = High[bar] + (25 * Point())
        if Open[bar] == Close[bar]:
            IndBuffer5[bar] = High[bar] + (30 * Point())
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class YtgJapanCandles(_MQL5Indicator):
    name = 'ytg_japan_candles'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

