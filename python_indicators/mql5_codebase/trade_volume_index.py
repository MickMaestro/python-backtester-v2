"""Trade_Volume_Index — converted from MQL5: MQL5 Indicators/TVI/Trade_Volume_Index.mq5

Trade Volume Index indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [14772545]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'TVI'}, 'levels': [], 'description': ['Trade Volume Index indicator'], 'name': 'Trade_Volume_Index', 'source': 'MQL5 Indicators/TVI/Trade_Volume_Index.mq5', 'folder': 'TVI', 'inputs': [{'mql': 'InpMinTickValue', 'py': 'InpMinTickValue', 'param': 'InpMinTickValue', 'type': 'uint', 'default': 10, 'label': 'Minimum tick value', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpMinTickValue = _input('InpMinTickValue', 10)  # Minimum tick value
BufferTVI = Arr(0, 0.0)
BufferDirection = Arr(0, 0.0)
BufferExtremePrice = Arr(0, 0.0)
min_tick_value = 0

def OnInit():
    global min_tick_value
    min_tick_value = (1 if (InpMinTickValue < 1) else InpMinTickValue)
    SetIndexBuffer(0, BufferTVI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDirection, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferExtremePrice, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trade Volume Index (' + _str(min_tick_value) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferTVI, True)
    ArraySetAsSeries(BufferDirection, True)
    ArraySetAsSeries(BufferExtremePrice, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < 4 or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferTVI, EMPTY_VALUE)
        ArrayInitialize(BufferDirection, 0)
        ArrayInitialize(BufferExtremePrice, 0)
    for i in range(limit, 0 - 1, -1):
        if i == (rates_total - 2):
            BufferDirection[i] = 0.0
            BufferExtremePrice[i] = close[i]
            BufferTVI[i] = 0.0
        else:
            change = _fdiv(close[i] - BufferExtremePrice[i + 1], Point())
            if change > min_tick_value:
                BufferDirection[i] = 1.0
                BufferExtremePrice[i] = close[i]
            else:
                if change < (-min_tick_value):
                    BufferDirection[i] = -1.0
                    BufferExtremePrice[i] = close[i]
                else:
                    BufferDirection[i] = BufferDirection[i + 1]
                    BufferExtremePrice[i] = BufferExtremePrice[i + 1]
            if BufferDirection[i] > 0:
                BufferTVI[i] = BufferTVI[i + 1] + tick_volume[i]
            else:
                if BufferDirection[i] < 0:
                    BufferTVI[i] = BufferTVI[i + 1] - tick_volume[i]
                else:
                    BufferTVI[i] = BufferTVI[i + 1]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TradeVolumeIndex(_MQL5Indicator):
    name = 'Trade_Volume_Index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMinTickValue': 10,  # Minimum tick value
    }

