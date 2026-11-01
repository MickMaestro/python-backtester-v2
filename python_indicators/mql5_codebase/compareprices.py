"""ComparePrices — converted from MQL5: MQL5 Indicators/ComparePrices/ComparePrices.mq5

Compare Prices indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Main Price', 2: 'Log10 Price'}, 'levels': [], 'description': ['Compare Prices indicator'], 'name': 'ComparePrices', 'source': 'MQL5 Indicators/ComparePrices/ComparePrices.mq5', 'folder': 'ComparePrices', 'inputs': [{'mql': 'InpShift', 'py': 'InpShift', 'param': 'InpShift', 'type': 'uint', 'default': 1, 'label': 'Prices shift', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpShift = _input('InpShift', 1)  # Prices shift
BufferMainPrice = Arr(0, 0.0)
BufferLogPrice = Arr(0, 0.0)
shift = 0

def OnInit():
    global shift
    shift = (1 if (InpShift < 1) else InpShift)
    SetIndexBuffer(0, BufferMainPrice, INDICATOR_DATA)
    SetIndexBuffer(1, BufferLogPrice, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ComparePrices (' + _str(shift) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMainPrice, True)
    ArraySetAsSeries(BufferLogPrice, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    if rates_total < fmax(shift, 2):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - shift - 1
        ArrayInitialize(BufferMainPrice, EMPTY_VALUE)
        ArrayInitialize(BufferLogPrice, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        BufferMainPrice[i] = close[i]
        BufferLogPrice[i] = (_fdiv(close[i], 1.0 + log10(_fdiv(close[i + shift], close[i]))) if (close[i] != 0) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ComparePrices(_MQL5Indicator):
    name = 'ComparePrices'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpShift': 1,  # Prices shift
    }

