"""CandleMidPoint — converted from MQL5: MQL5 Indicators/CandleMidPoint/CandleMidPoint.mq5

Candle's Middle Point indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 5}, 'colors': {1: [16760576]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Middle Point'}, 'levels': [], 'description': ["Candle's Middle Point indicator"], 'name': 'CandleMidPoint', 'source': 'MQL5 Indicators/CandleMidPoint/CandleMidPoint.mq5', 'folder': 'CandleMidPoint', 'inputs': [{'mql': 'InpTypeCandle', 'py': 'InpTypeCandle', 'param': 'InpTypeCandle', 'type': 'int', 'default': 0, 'label': 'Middle point for', 'sinput': False}, {'mql': 'InpTypeArrow', 'py': 'InpTypeArrow', 'param': 'InpTypeArrow', 'type': 'int', 'default': 159, 'label': 'Dots type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_CANDLE_TYPE
TYPE_CANDLE_HL = 0
TYPE_CANDLE_OC = 1
_enum('ENUM_CANDLE_TYPE', {0: 'TYPE_CANDLE_HL', 1: 'TYPE_CANDLE_OC'})

# enum ENUM_ARROW_TYPE
TYPE_ARROW_DOT0 = 158
TYPE_ARROW_DOT1 = 159
TYPE_ARROW_DOT2 = 108
TYPE_ARROW_SQUARE1 = 167
TYPE_ARROW_SQUARE2 = 110
TYPE_ARROW_DIAMOND1 = 115
TYPE_ARROW_DIAMOND2 = 116
TYPE_ARROW_CROSS = 251
_enum('ENUM_ARROW_TYPE', {158: 'TYPE_ARROW_DOT0', 159: 'TYPE_ARROW_DOT1', 108: 'TYPE_ARROW_DOT2', 167: 'TYPE_ARROW_SQUARE1', 110: 'TYPE_ARROW_SQUARE2', 115: 'TYPE_ARROW_DIAMOND1', 116: 'TYPE_ARROW_DIAMOND2', 251: 'TYPE_ARROW_CROSS'})

# ---- inputs and global variables
InpTypeCandle = _input('InpTypeCandle', TYPE_CANDLE_HL)  # Middle point for
InpTypeArrow = _input('InpTypeArrow', TYPE_ARROW_DOT1)  # Dots type
BufferMP = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BufferMP, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, InpTypeArrow)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CandleMidPoint')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMP, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 1:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferMP, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        BufferMP[i] = (((open[i] + close[i]) / 2.0) if (InpTypeCandle == TYPE_CANDLE_OC) else ((high[i] + low[i]) / 2.0))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandleMidPoint(_MQL5Indicator):
    name = 'CandleMidPoint'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpTypeCandle': _Choice({0: 'Candle', 1: 'Body'}, default=0),  # Middle point for
        'InpTypeArrow': _Choice({158: 'Smallest Dot', 159: 'Small Dot', 108: 'Big Dot', 167: 'Small Square', 110: 'Big Square', 115: 'Small Diamond', 116: 'Big Diamond', 251: 'Cross'}, default=159),  # Dots type
    }

