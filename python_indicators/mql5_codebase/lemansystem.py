"""lemansystem — converted from MQL5: MQL5 Indicators/LeManSystem/lemansystem.mq5

Copyright: Copyright © 2009, LeMan.; Link: b-market@mail.ru; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, LeMan.', 'link': 'b-market@mail.ru', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [3329330], 2: [9639167], 3: [9639167], 4: [3329330]}, 'widths': {1: 1, 2: 1, 3: 2, 4: 2}, 'styles': {}, 'labels': {1: 'Lower LeMan', 2: 'Upper LeMan', 3: 'LeManStop Sell', 4: 'LeManStop Buy'}, 'levels': [], 'description': [''], 'name': 'lemansystem', 'source': 'MQL5 Indicators/LeManSystem/lemansystem.mq5', 'folder': 'LeManSystem', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'uint', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
period = _input('period', 12)
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
BuyBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(period + 3)
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(UpBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(3, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'LeManStop')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    HL1 = 0.0
    HL2 = 0.0
    LH1 = 0.0
    LH2 = 0.0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        HL1 = low[ArrayMaximum(low, bar + 1, period)]
        HL2 = low[ArrayMaximum(low, bar + 2, period)]
        LH1 = high[ArrayMinimum(high, bar + 1, period)]
        LH2 = high[ArrayMinimum(high, bar + 2, period)]
        if low[bar + 2] <= LH2 and low[bar + 1] > LH1:
            BuyBuffer[bar] = high[bar + 1] + Point()
        if high[bar + 2] >= HL2 and high[bar + 1] < HL1:
            SellBuffer[bar] = low[bar + 1] - Point()
        DnBuffer[bar] = low[ArrayMinimum(low, bar + 1, period)]
        UpBuffer[bar] = high[ArrayMaximum(high, bar + 1, period)]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Lemansystem(_MQL5Indicator):
    name = 'lemansystem'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 12,
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

