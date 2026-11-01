"""supersr6 — converted from MQL5: MQL5 Indicators/SuperSR6/supersr6.mq5

Indicator to build the possible lines of support and resistance
Copyright: Copyright © 2006, Scorpion; Link: http://www.fxfisherman.com/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Scorpion', 'link': 'http://www.fxfisherman.com/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Support', 2: 'Resistance'}, 'levels': [], 'description': ['Indicator to build the possible lines of support and resistance'], 'name': 'supersr6', 'source': 'MQL5 Indicators/SuperSR6/supersr6.mq5', 'folder': 'SuperSR6', 'inputs': [{'mql': 'Contract_Step', 'py': 'Contract_Step', 'param': 'Contract_Step', 'type': 'uint', 'default': 150, 'label': '', 'sinput': False}, {'mql': 'Precision', 'py': 'Precision', 'param': 'Precision', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'Shift_Bars', 'py': 'Shift_Bars', 'param': 'Shift_Bars', 'type': 'uint', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Contract_Step = _input('Contract_Step', 150)
Precision = _input('Precision', 10)
Shift_Bars = _input('Shift_Bars', 1)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
contract = 0.0
dPrecision = 0.0

def OnInit():
    global contract, dPrecision, min_rates_total
    min_rates_total = _int(6 + Shift_Bars)
    contract = (Contract_Step + Precision) * Point()
    dPrecision = Precision * Point()
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(0, PLOT_LABEL, 'Support')
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(1, PLOT_LABEL, 'Resistance')
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'SuperSR6'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    shift = 0
    limit = 0
    bar = 0
    fractal = False
    price = 0.0
    gap = 0.0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        BuyBuffer[bar] = high[limit + 1]
        SellBuffer[bar] = low[limit + 1]
    else:
        limit = rates_total - prev_calculated + 2
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        shift = _int(bar + Shift_Bars)
        price = high[shift + 2]
        fractal = ((price >= high[shift + 4] and price >= high[shift + 3]) and price > high[shift + 1]) and price > high[shift]
        gap = BuyBuffer[bar + 1] - price
        if fractal and (gap >= contract or gap < 0):
            BuyBuffer[bar] = price + dPrecision
        else:
            BuyBuffer[bar] = BuyBuffer[bar + 1]
        price = low[shift + 2]
        fractal = ((price <= low[shift + 4] and price <= low[shift + 3]) and price < low[shift + 1]) and price < low[shift]
        gap = price - SellBuffer[bar + 1]
        if fractal and (gap >= contract or gap < 0):
            SellBuffer[bar] = price - dPrecision
        else:
            SellBuffer[bar] = SellBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Supersr6(_MQL5Indicator):
    name = 'supersr6'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Contract_Step': 150,
        'Precision': 10,
        'Shift_Bars': 1,
    }

