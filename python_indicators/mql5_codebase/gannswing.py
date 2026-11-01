"""GannSwing — converted from MQL5: MQL5 Indicators/GannSwing/GannSwing.mq5

Gann Swing indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 2}, 'colors': {1: [255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Gann Swing'}, 'levels': [], 'description': ['Gann Swing indicator'], 'name': 'GannSwing', 'source': 'MQL5 Indicators/GannSwing/GannSwing.mq5', 'folder': 'GannSwing', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BufferGS = Arr(0, 0.0)
BufferUS = Arr(0, 0.0)
BufferDS = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, BufferGS, INDICATOR_DATA)
    SetIndexBuffer(1, BufferUS, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferDS, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Gann Swing')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferGS, True)
    ArraySetAsSeries(BufferUS, True)
    ArraySetAsSeries(BufferDS, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < 5:
        return 0
    limit = rates_total - prev_calculated
    if limit > 0:
        limit = rates_total - 4
        ArrayInitialize(BufferGS, EMPTY_VALUE)
        ArrayInitialize(BufferUS, 0)
        ArrayInitialize(BufferDS, 0)
    for i in range(limit, 0 - 1, -1):
        ResetBuffers(i)
        if high[i] > high[i + 1] and high[i + 1] > high[i + 2]:
            BufferUS[i] = 1.0
        if low[i] < low[i + 1] and low[i + 1] < low[i + 2]:
            BufferDS[i] = 1.0
        if (BufferUS[i] == 0 and high[i] > high[i + 1]) and low[i] >= low[i + 1]:
            BufferUS[i] = 1.0
        if (BufferDS[i] == 0 and high[i] <= high[i + 1]) and low[i] < low[i + 1]:
            BufferDS[i] = 1.0
    swing_dir = 0
    for i in range(limit, 0 - 1, -1):
        if BufferUS[i] == 1:
            if swing_dir == 1:
                BufferGS[i] = high[i]
            elif swing_dir == -1:
                BufferGS[i] = high[i]
                swing_dir = 1
            else:
                swing_dir = 1
                BufferGS[i] = high[i]
        elif BufferDS[i] == 1:
            if swing_dir == -1:
                BufferGS[i] = low[i]
            elif swing_dir == 1:
                BufferGS[i] = low[i]
                swing_dir = -1
            else:
                swing_dir = -1
                BufferGS[i] = low[i]
        else:
            if high[i + 1] > high[i + 2] and low[i + 1] < low[i + 3]:
                if high[i] > high[i + 1] and low[i] >= low[i + 1]:
                    if swing_dir == -1:
                        BufferGS[i] = low[i]
                    elif swing_dir == 1:
                        BufferGS[i] = low[i]
                        swing_dir = -1
                elif high[i] <= high[i + 1] and low[i] < low[i + 1]:
                    if swing_dir == 1:
                        BufferGS[i] = high[i]
                    elif swing_dir == -1:
                        BufferGS[i] = high[i]
                        swing_dir = 1
    last = 0
    last_index = 0
    for i in range(limit, 0 - 1, -1):
        if BufferGS[i] == high[i]:
            if last == 1:
                BufferGS[last_index] = EMPTY_VALUE
            last = 1
            last_index = i
        if BufferGS[i] == low[i]:
            if last == -1:
                BufferGS[last_index] = EMPTY_VALUE
            last = -1
            last_index = i
    return rates_total

def ResetBuffers(shift):
    BufferGS[shift] = EMPTY_VALUE
    BufferDS[shift] = 0.0
    BufferUS[shift] = BufferDS[shift]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GannSwing(_MQL5Indicator):
    name = 'GannSwing'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
    }

