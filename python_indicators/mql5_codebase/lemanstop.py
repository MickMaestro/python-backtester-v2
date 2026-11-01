"""lemanstop — converted from MQL5: MQL5 Indicators/LeManStop/lemanstop.mq5

Copyright: Copyright © 2009, LeMan.; Link: b-market@mail.ru; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, LeMan.', 'link': 'b-market@mail.ru', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [3329330], 2: [9639167], 3: [3329330], 4: [9639167]}, 'widths': {1: 3, 2: 3, 3: 2, 4: 2}, 'styles': {}, 'labels': {1: 'Lower LeManStop', 2: 'Upper LeManStop', 3: 'LeManStop Buy', 4: 'LeManStop Sell'}, 'levels': [], 'description': [''], 'name': 'lemanstop', 'source': 'MQL5 Indicators/LeManStop/lemanstop.mq5', 'folder': 'LeManStop', 'inputs': [{'mql': 'per', 'py': 'per', 'param': 'per', 'type': 'uint', 'default': 24, 'label': '', 'sinput': False}, {'mql': 'coef', 'py': 'coef', 'param': 'coef', 'type': 'uint', 'default': 4, 'label': '', 'sinput': False}, {'mql': 'fastEMA', 'py': 'fastEMA', 'param': 'fastEMA', 'type': 'uint', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'slowEMA', 'py': 'slowEMA', 'param': 'slowEMA', 'type': 'uint', 'default': 18, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
per = _input('per', 24)
coef = _input('coef', 4)
fastEMA = _input('fastEMA', 9)
slowEMA = _input('slowEMA', 18)
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
BuyBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
min_rates_total = 0
SEMA_Handle = 0
FEMA_Handle = 0

def OnInit():
    global FEMA_Handle, SEMA_Handle, min_rates_total
    min_rates_total = _int(per + 3)
    FEMA_Handle = iMA(None, 0, fastEMA, 0, MODE_EMA, PRICE_CLOSE)
    if FEMA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the FastEMA indicator')
    SEMA_Handle = iMA(None, 0, slowEMA, 0, MODE_EMA, PRICE_CLOSE)
    if SEMA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the SlowEma indicator')
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 158)
    ArraySetAsSeries(UpBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 158)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 163)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(3, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 163)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'LeManStop')

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if (BarsCalculated(FEMA_Handle) < rates_total or BarsCalculated(SEMA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    to_copy = 0
    Counter = 0
    fEMA = Arr(0, 0.0)
    sEMA = Arr(0, 0.0)
    EMA0 = 0.0
    EMA1 = 0.0
    Stop = 0.0
    PreStop = 0.0
    Sum = 0.0
    res = 0.0
    ArraySetAsSeries(Open, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Close, True)
    ArraySetAsSeries(fEMA, True)
    ArraySetAsSeries(sEMA, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(FEMA_Handle, MAIN_LINE, 0, to_copy, fEMA) <= 0:
        return 0
    if CopyBuffer(SEMA_Handle, MAIN_LINE, 0, to_copy, sEMA) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        DnBuffer[bar] = 0.0
        UpBuffer[bar] = 0.0
        EMA0 = fEMA[bar] - sEMA[bar]
        EMA1 = fEMA[bar + 1] - sEMA[bar + 1]
        PreStop = UpBuffer[bar + 1] + DnBuffer[bar + 1]
        Sum = 0.0
        Counter = 0
        if EMA0 > 0:
            for kkk in range(0, _int(per) + 1):
                Sum += Close[bar + kkk] - Low[bar + kkk]
                Counter += 1
            res = coef * Sum
            if Counter:
                Stop = Close[bar] - _fdiv(res, Counter)
            else:
                Stop = Open[bar] - res
            if Stop < PreStop and EMA1 > 0:
                Stop = PreStop
            UpBuffer[bar] = Stop
        if EMA0 < 0:
            for kkk in range(0, _int(per) + 1):
                Sum = High[bar + kkk] - Close[bar + kkk] + Sum
                Counter += 1
            res = coef * Sum
            if Counter:
                Stop = Close[bar + 1] + _fdiv(res, Counter)
            else:
                Stop = Open[bar + 1] + res
            if Stop > PreStop and EMA1 < 0:
                Stop = PreStop
            DnBuffer[bar] = Stop
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if UpBuffer[bar + 1] > 0.0 and DnBuffer[bar] > 0.0:
            BuyBuffer[bar] = DnBuffer[bar]
        if DnBuffer[bar + 1] > 0.0 and UpBuffer[bar] > 0.0:
            SellBuffer[bar] = UpBuffer[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Lemanstop(_MQL5Indicator):
    name = 'lemanstop'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'per': 24,
        'coef': 4,
        'fastEMA': 9,
        'slowEMA': 18,
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

