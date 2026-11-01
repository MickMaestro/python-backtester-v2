"""Trailing_Stop_Level — converted from MQL5: MQL5 Indicators/Trailing_Stop_Level/Trailing_Stop_Level.mq5

Trailing Stop level indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [32768]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Level for short', 2: 'Level for long'}, 'levels': [], 'description': ['Trailing Stop level indicator'], 'name': 'Trailing_Stop_Level', 'source': 'MQL5 Indicators/Trailing_Stop_Level/Trailing_Stop_Level.mq5', 'folder': 'Trailing_Stop_Level', 'inputs': [{'mql': 'InpPercent', 'py': 'InpPercent', 'param': 'InpPercent', 'type': 'double', 'default': 30.0, 'label': 'Percent', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPercent = _input('InpPercent', 30.0)  # Percent
BufferLevUP = Arr(0, 0.0)
BufferLevDN = Arr(0, 0.0)
BufferData = Arr(0, 0.0)
percent = 0.0

def OnInit():
    global percent
    percent = (1 if (InpPercent < 1) else (InpPercent / 100.0))
    SetIndexBuffer(0, BufferLevUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferLevDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferData, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TrailingStopLevel(' + DoubleToString(percent, 2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferLevUP, True)
    ArraySetAsSeries(BufferLevDN, True)
    ArraySetAsSeries(BufferData, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    ArraySetAsSeries(close, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferLevUP, EMPTY_VALUE)
        ArrayInitialize(BufferLevDN, EMPTY_VALUE)
        ArrayInitialize(BufferData, 0)
    for i in range(limit, 0 - 1, -1):
        loss = (close[i] * percent) / 100
        if close[i] > BufferData[i + 1] and close[i + 1] > BufferData[i + 1]:
            BufferData[i] = fmax(BufferData[i + 1], close[i] - loss)
            BufferLevDN[i] = BufferData[i]
            BufferLevDN[i + 1] = BufferData[i + 1]
        else:
            if close[i] < BufferData[i + 1] and close[i + 1] < BufferData[i + 1]:
                BufferData[i] = fmin(BufferData[i + 1], close[i] + loss)
                BufferLevUP[i] = BufferData[i]
                BufferLevUP[i + 1] = BufferData[i + 1]
            else:
                if close[i] > BufferData[i + 1]:
                    BufferData[i] = close[i] - loss
                    BufferLevDN[i] = BufferData[i]
                    BufferLevUP[i + 1] = BufferData[i + 1]
                else:
                    BufferData[i] = close[i] + loss
                    BufferLevUP[i] = BufferData[i]
                    BufferLevDN[i + 1] = BufferData[i + 1]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TrailingStopLevel(_MQL5Indicator):
    name = 'Trailing_Stop_Level'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPercent': 30.0,  # Percent
    }

