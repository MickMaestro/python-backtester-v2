"""Darvas_Box — converted from MQL5: MQL5 Indicators/Darvas_Box/Darvas_Box.mq5

Darvas Box indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [32768], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Box Top', 2: 'Box Bottom'}, 'levels': [], 'description': ['Darvas Box indicator'], 'name': 'Darvas_Box', 'source': 'MQL5 Indicators/Darvas_Box/Darvas_Box.mq5', 'folder': 'Darvas_Box', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferState = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferState, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Darvas Box')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferState, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferState, 0)
        BufferState[limit] = 1.0
    for i in range(limit, 0 - 1, -1):
        box_top = BufferUP[i + 1]
        box_bottom = BufferDN[i + 1]
        state = BufferState[i + 1]
        if state == 1:
            box_top = high[i]
        else:
            if state == 2:
                if box_top <= high[i]:
                    box_top = high[i]
            else:
                if state == 3:
                    if box_top > high[i]:
                        box_bottom = high[i]
                    else:
                        box_top = high[i]
                else:
                    if state == 4:
                        if box_top > high[i]:
                            if box_bottom >= low[i]:
                                box_bottom = low[i]
                        else:
                            box_top = high[i]
                    else:
                        if box_top > high[i]:
                            if box_bottom >= low[i]:
                                box_bottom = low[i]
                        else:
                            box_top = high[i]
                        state = 0.0
        state += 1
        BufferState[i] = state
        BufferUP[i] = box_top
        BufferDN[i] = box_bottom
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DarvasBox(_MQL5Indicator):
    name = 'Darvas_Box'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

