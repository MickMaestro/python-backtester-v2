"""Other_Candles — converted from MQL5: MQL5 Indicators/Other_Candles/Other_Candles.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [3329330, 17919, 8421504]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Candle'}, 'levels': [], 'description': [], 'name': 'Other_Candles', 'source': 'MQL5 Indicators/Other_Candles/Other_Candles.mq5', 'folder': 'Other_Candles', 'inputs': [{'mql': 'InpColorBullish', 'py': 'InpColorBullish', 'param': None, 'type': 'color', 'default': 3329330, 'label': 'Bullish candle color', 'sinput': False}, {'mql': 'InpColorBearish', 'py': 'InpColorBearish', 'param': None, 'type': 'color', 'default': 17919, 'label': 'Bearish candle color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_CANDLE_TYPE
CANDLE_TYPE_BULLISH = 0
CANDLE_TYPE_BEARISH = 1
CANDLE_TYPE_DOJI = 2
_enum('ENUM_CANDLE_TYPE', {0: 'CANDLE_TYPE_BULLISH', 1: 'CANDLE_TYPE_BEARISH', 2: 'CANDLE_TYPE_DOJI'})

# ---- inputs and global variables
InpColorBullish = _input('InpColorBullish', clrLimeGreen)  # Bullish candle color
InpColorBearish = _input('InpColorBearish', clrOrangeRed)  # Bearish candle color
BufferOpen = Arr(0, 0.0)
BufferHigh = Arr(0, 0.0)
BufferLow = Arr(0, 0.0)
BufferClose = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)

class SDataCandles(MqlObject):
    _q_fields = ('type', 'body_size', 'shadow_up_size', 'shadow_dn_size')
    def __init__(self, *args):
        self.type = 0
        self.body_size = 0.0
        self.shadow_up_size = 0.0
        self.shadow_dn_size = 0.0

def OnInit():
    SetIndexBuffer(0, BufferOpen, INDICATOR_DATA)
    SetIndexBuffer(1, BufferHigh, INDICATOR_DATA)
    SetIndexBuffer(2, BufferLow, INDICATOR_DATA)
    SetIndexBuffer(3, BufferClose, INDICATOR_DATA)
    SetIndexBuffer(4, BufferColors, INDICATOR_COLOR_INDEX)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0)
    symbol = Symbol()
    PlotIndexSetString(0, PLOT_LABEL, symbol + ' Open;' + symbol + ' High;' + symbol + ' Low;' + symbol + ' Close')
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 0, InpColorBullish)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, 1, InpColorBearish)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Other candles')
    ArraySetAsSeries(BufferOpen, True)
    ArraySetAsSeries(BufferHigh, True)
    ArraySetAsSeries(BufferLow, True)
    ArraySetAsSeries(BufferClose, True)
    ArraySetAsSeries(BufferColors, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 1:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferOpen, 0)
        ArrayInitialize(BufferHigh, 0)
        ArrayInitialize(BufferLow, 0)
        ArrayInitialize(BufferClose, 0)
    for i in range(limit, 0 - 1, -1):
        SetCandleParams(i, open, high, low, close)
        BufferOpen[i] = 0.0
        if candle.type == CANDLE_TYPE_BULLISH:
            BufferColors[i] = 0.0
            BufferHigh[i] = candle.body_size + candle.shadow_up_size
            BufferClose[i] = candle.body_size
            BufferLow[i] = BufferOpen[i] - candle.shadow_dn_size
        elif candle.type == CANDLE_TYPE_BEARISH:
            BufferColors[i] = 1.0
            BufferLow[i] = (-candle.body_size) - candle.shadow_dn_size
            BufferClose[i] = -candle.body_size
            BufferHigh[i] = candle.shadow_up_size
        else:
            BufferClose[i] = 0.0
            BufferHigh[i] = candle.shadow_up_size
            BufferLow[i] = -candle.shadow_dn_size
            BufferColors[i] = 2.0
    return rates_total

def SetCandleParams(index, open, high, low, close):
    ZeroMemory(candle)
    candle.type = CandleType(index, open, close)
    candle.body_size = fabs(open[index] - close[index])
    candle.shadow_up_size = high[index] - fmax(open[index], close[index])
    candle.shadow_dn_size = fmin(open[index], close[index]) - low[index]

def CandleType(index, open, close):
    return (CANDLE_TYPE_BULLISH if (close[index] > open[index]) else CANDLE_TYPE_BEARISH if (close[index] < open[index]) else CANDLE_TYPE_DOJI)

# ---- global variables initialised from expressions
candle = _alloc(SDataCandles)
candle.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class OtherCandles(_MQL5Indicator):
    name = 'Other_Candles'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

