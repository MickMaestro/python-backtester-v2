"""pivot — converted from MQL5: MQL5 Indicators/PivotPoint/pivot.mq5

Copyright: 2010, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2010, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 7}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'colors': {1: [36095], 2: [3329330], 3: [3329330], 4: [3329330], 5: [255], 6: [255], 7: [255]}, 'widths': {1: 2, 2: 3, 3: 2, 4: 1, 5: 3, 6: 2, 7: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}, 'labels': {1: 'Pivot', 2: 'R1', 3: 'R2', 4: 'R3', 5: 'S1', 6: 'S2', 7: 'S3'}, 'levels': [], 'description': [], 'name': 'pivot', 'source': 'MQL5 Indicators/PivotPoint/pivot.mq5', 'folder': 'PivotPoint', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
PivotBuffer = Arr(0, 0.0)
R1Buffer = Arr(0, 0.0)
R2Buffer = Arr(0, 0.0)
R3Buffer = Arr(0, 0.0)
S1Buffer = Arr(0, 0.0)
S2Buffer = Arr(0, 0.0)
S3Buffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, PivotBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, R1Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, R2Buffer, INDICATOR_DATA)
    SetIndexBuffer(3, R3Buffer, INDICATOR_DATA)
    SetIndexBuffer(4, S1Buffer, INDICATOR_DATA)
    SetIndexBuffer(5, S2Buffer, INDICATOR_DATA)
    SetIndexBuffer(6, S3Buffer, INDICATOR_DATA)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    rates = Arr(0, 0, factory=MqlRates)
    ArraySetAsSeries(rates, True)
    copied = CopyRates(Symbol(), PERIOD_D1, 0, 2, rates)
    pivot = (rates[1].high + rates[1].close + rates[1].low) / 3
    r1 = (2 * pivot) - rates[1].low
    s1 = (2 * pivot) - rates[1].high
    r2 = pivot + (r1 - s1)
    r3 = rates[1].high + (2 * (pivot - rates[1].low))
    s2 = pivot - (r1 - s1)
    s3 = rates[1].low - (2 * (rates[1].high - pivot))
    pos = prev_calculated - 1
    if pos < 0:
        pos = 0
    for i in range(pos, rates_total):
        PivotBuffer[i] = pivot
        R1Buffer[i] = r1
        R2Buffer[i] = r2
        R3Buffer[i] = r3
        S1Buffer[i] = s1
        S2Buffer[i] = s2
        S3Buffer[i] = s3
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Pivot(_MQL5Indicator):
    name = 'pivot'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
    }

