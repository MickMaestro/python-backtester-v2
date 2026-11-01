"""BBMA — converted from MQL5: MQL5 Indicators/BBMA - Bollinger Band Moving Average/BBMA.mq5

Download Expert Advisors and Indicator for FREE!
Want an EA with Indicator, contact me on telegram: @sopheak_khmer_trader
Copyright: BestForexScript.Com; Link: https://bestforexscript.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'BestForexScript.Com', 'link': 'https://bestforexscript.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 16, 'indicator_plots': 16}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1}, 'colors': {1: [0], 2: [32768], 3: [0], 4: [255], 5: [255], 6: [255], 7: [255], 8: [255], 9: [255], 10: [255], 11: [16711680], 12: [16711680], 13: [16711680], 14: [16711680], 15: [16711680], 16: [16711680]}, 'widths': {1: 1, 2: 2, 3: 1, 4: 2, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 2, 7: 2, 8: 2, 9: 2, 10: 0, 11: 0, 12: 2, 13: 2, 14: 2, 15: 2, 16: 0}, 'labels': {1: 'Upper Band', 2: 'Base', 3: 'Lower Band', 4: 'MA50', 5: 'MH5', 6: 'MH6', 7: 'MH7', 8: 'MH8', 9: 'MH9', 10: 'MH10', 11: 'ML5', 12: 'ML6', 13: 'ML7', 14: 'ML8', 15: 'ML9', 16: 'ML10'}, 'levels': [], 'description': ['Download Expert Advisors and Indicator for FREE!', 'Want an EA with Indicator, contact me on telegram: @sopheak_khmer_trader'], 'name': 'BBMA', 'source': 'MQL5 Indicators/BBMA - Bollinger Band Moving Average/BBMA.mq5', 'folder': 'BBMA - Bollinger Band Moving Average', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
UpperBandBuffer = Arr(0, 0.0)
BaseBuffer = Arr(0, 0.0)
LowerBandBuffer = Arr(0, 0.0)
MA50Buffer = Arr(0, 0.0)
MH5Buffer = Arr(0, 0.0)
MH6Buffer = Arr(0, 0.0)
MH7Buffer = Arr(0, 0.0)
MH8Buffer = Arr(0, 0.0)
MH9Buffer = Arr(0, 0.0)
MH10Buffer = Arr(0, 0.0)
ML5Buffer = Arr(0, 0.0)
ML6Buffer = Arr(0, 0.0)
ML7Buffer = Arr(0, 0.0)
ML8Buffer = Arr(0, 0.0)
ML9Buffer = Arr(0, 0.0)
ML10Buffer = Arr(0, 0.0)
bbandhandler = 0
ma50handler = 0
mh5handler = 0
mh6handler = 0
mh7handler = 0
mh8handler = 0
mh9handler = 0
mh10handler = 0
ml5handler = 0
ml6handler = 0
ml7handler = 0
ml8handler = 0
ml9handler = 0
ml10handler = 0

def OnInit():
    global bbandhandler, ma50handler, mh10handler, mh5handler, mh6handler, mh7handler, mh8handler, mh9handler, ml10handler, ml5handler, ml6handler, ml7handler, ml8handler, ml9handler
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, UpperBandBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, BaseBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, LowerBandBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, MA50Buffer, INDICATOR_DATA)
    SetIndexBuffer(4, MH5Buffer, INDICATOR_DATA)
    SetIndexBuffer(5, MH6Buffer, INDICATOR_DATA)
    SetIndexBuffer(6, MH7Buffer, INDICATOR_DATA)
    SetIndexBuffer(7, MH8Buffer, INDICATOR_DATA)
    SetIndexBuffer(8, MH9Buffer, INDICATOR_DATA)
    SetIndexBuffer(9, MH10Buffer, INDICATOR_DATA)
    SetIndexBuffer(10, ML5Buffer, INDICATOR_DATA)
    SetIndexBuffer(11, ML6Buffer, INDICATOR_DATA)
    SetIndexBuffer(12, ML7Buffer, INDICATOR_DATA)
    SetIndexBuffer(13, ML8Buffer, INDICATOR_DATA)
    SetIndexBuffer(14, ML9Buffer, INDICATOR_DATA)
    SetIndexBuffer(15, ML10Buffer, INDICATOR_DATA)
    PlotIndexGetInteger(0, PLOT_DRAW_BEGIN, 50)
    PlotIndexGetInteger(1, PLOT_DRAW_BEGIN, 50)
    PlotIndexGetInteger(2, PLOT_DRAW_BEGIN, 50)
    PlotIndexGetInteger(3, PLOT_DRAW_BEGIN, 50)
    PlotIndexGetInteger(4, PLOT_DRAW_BEGIN, 50)
    PlotIndexGetInteger(5, PLOT_DRAW_BEGIN, 50)
    PlotIndexGetInteger(6, PLOT_DRAW_BEGIN, 50)
    PlotIndexGetInteger(7, PLOT_DRAW_BEGIN, 50)
    PlotIndexGetInteger(8, PLOT_DRAW_BEGIN, 50)
    PlotIndexGetInteger(9, PLOT_DRAW_BEGIN, 50)
    PlotIndexGetInteger(10, PLOT_DRAW_BEGIN, 50)
    PlotIndexGetInteger(11, PLOT_DRAW_BEGIN, 50)
    PlotIndexGetInteger(12, PLOT_DRAW_BEGIN, 50)
    PlotIndexGetInteger(13, PLOT_DRAW_BEGIN, 50)
    PlotIndexGetInteger(14, PLOT_DRAW_BEGIN, 50)
    PlotIndexGetInteger(15, PLOT_DRAW_BEGIN, 50)
    ArraySetAsSeries(BaseBuffer, True)
    ArraySetAsSeries(UpperBandBuffer, True)
    ArraySetAsSeries(LowerBandBuffer, True)
    ArraySetAsSeries(MA50Buffer, True)
    ArraySetAsSeries(MH5Buffer, True)
    ArraySetAsSeries(MH6Buffer, True)
    ArraySetAsSeries(MH7Buffer, True)
    ArraySetAsSeries(MH8Buffer, True)
    ArraySetAsSeries(MH9Buffer, True)
    ArraySetAsSeries(MH10Buffer, True)
    ArraySetAsSeries(ML5Buffer, True)
    ArraySetAsSeries(ML6Buffer, True)
    ArraySetAsSeries(ML7Buffer, True)
    ArraySetAsSeries(ML8Buffer, True)
    ArraySetAsSeries(ML9Buffer, True)
    ArraySetAsSeries(ML10Buffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BBMA Indicator')
    bbandhandler = iBands(Symbol(), PERIOD_CURRENT, 20, 0, 2, PRICE_CLOSE)
    ma50handler = iMA(Symbol(), PERIOD_CURRENT, 50, 0, MODE_EMA, PRICE_CLOSE)
    mh5handler = iMA(Symbol(), PERIOD_CURRENT, 5, 0, MODE_LWMA, PRICE_HIGH)
    mh6handler = iMA(Symbol(), PERIOD_CURRENT, 6, 0, MODE_LWMA, PRICE_HIGH)
    mh7handler = iMA(Symbol(), PERIOD_CURRENT, 7, 0, MODE_LWMA, PRICE_HIGH)
    mh8handler = iMA(Symbol(), PERIOD_CURRENT, 8, 0, MODE_LWMA, PRICE_HIGH)
    mh9handler = iMA(Symbol(), PERIOD_CURRENT, 9, 0, MODE_LWMA, PRICE_HIGH)
    mh10handler = iMA(Symbol(), PERIOD_CURRENT, 10, 0, MODE_LWMA, PRICE_HIGH)
    ml5handler = iMA(Symbol(), PERIOD_CURRENT, 5, 0, MODE_LWMA, PRICE_LOW)
    ml6handler = iMA(Symbol(), PERIOD_CURRENT, 6, 0, MODE_LWMA, PRICE_LOW)
    ml7handler = iMA(Symbol(), PERIOD_CURRENT, 7, 0, MODE_LWMA, PRICE_LOW)
    ml8handler = iMA(Symbol(), PERIOD_CURRENT, 8, 0, MODE_LWMA, PRICE_LOW)
    ml9handler = iMA(Symbol(), PERIOD_CURRENT, 9, 0, MODE_LWMA, PRICE_LOW)
    ml10handler = iMA(Symbol(), PERIOD_CURRENT, 10, 0, MODE_LWMA, PRICE_LOW)
    if ((((((((((((bbandhandler < 0 or ma50handler < 0) or mh5handler < 0) or mh6handler < 0) or mh7handler < 0) or mh8handler < 0) or mh9handler < 0) or mh10handler < 0) or ml5handler < 0) or ml6handler < 0) or ml7handler < 0) or ml8handler < 0) or ml9handler < 0) or ml10handler < 0:
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    IndicatorRelease(bbandhandler)
    IndicatorRelease(ma50handler)
    IndicatorRelease(mh5handler)
    IndicatorRelease(mh6handler)
    IndicatorRelease(mh7handler)
    IndicatorRelease(mh8handler)
    IndicatorRelease(mh9handler)
    IndicatorRelease(mh10handler)
    IndicatorRelease(ml5handler)
    IndicatorRelease(ml6handler)
    IndicatorRelease(ml7handler)
    IndicatorRelease(ml8handler)
    IndicatorRelease(ml9handler)
    IndicatorRelease(ml10handler)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 50:
        return 0
    limit = fmin(rates_total - 1, rates_total - prev_calculated)
    for i in range(limit, 0 - 1, -1):
        if CopyBuffer(bbandhandler, BASE_LINE, i, 1, BaseBuffer) <= 0:
            return 0
        if CopyBuffer(bbandhandler, UPPER_BAND, i, 1, UpperBandBuffer) <= 0:
            return 0
        if CopyBuffer(bbandhandler, LOWER_BAND, i, 1, LowerBandBuffer) <= 0:
            return 0
        if CopyBuffer(ma50handler, 0, i, 1, MA50Buffer) <= 0:
            return 0
        if CopyBuffer(mh5handler, 0, i, 1, MH5Buffer) <= 0:
            return 0
        if CopyBuffer(mh6handler, 0, i, 1, MH6Buffer) <= 0:
            return 0
        if CopyBuffer(mh7handler, 0, i, 1, MH7Buffer) <= 0:
            return 0
        if CopyBuffer(mh8handler, 0, i, 1, MH8Buffer) <= 0:
            return 0
        if CopyBuffer(mh9handler, 0, i, 1, MH9Buffer) <= 0:
            return 0
        if CopyBuffer(mh10handler, 0, i, 1, MH10Buffer) <= 0:
            return 0
        if CopyBuffer(ml5handler, 0, i, 1, ML5Buffer) <= 0:
            return 0
        if CopyBuffer(ml6handler, 0, i, 1, ML6Buffer) <= 0:
            return 0
        if CopyBuffer(ml7handler, 0, i, 1, ML7Buffer) <= 0:
            return 0
        if CopyBuffer(ml8handler, 0, i, 1, ML8Buffer) <= 0:
            return 0
        if CopyBuffer(ml9handler, 0, i, 1, ML9Buffer) <= 0:
            return 0
        if CopyBuffer(ml10handler, 0, i, 1, ML10Buffer) <= 0:
            return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BBMA(_MQL5Indicator):
    name = 'BBMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
    }

