"""adxcrossing — converted from MQL5: MQL5 Indicators/ADXCrossing/adxcrossing.mq5

Copyright: Copyright © 2005, Amir; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Amir', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'ADXCrossing Sell', 2: 'ADXCrossing Buy'}, 'levels': [], 'description': [], 'name': 'adxcrossing', 'source': 'MQL5 Indicators/ADXCrossing/adxcrossing.mq5', 'folder': 'ADXCrossing', 'inputs': [{'mql': 'ADXPeriod', 'py': 'ADXPeriod', 'param': 'ADXPeriod', 'type': 'uint', 'default': 50, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ADXPeriod = _input('ADXPeriod', 50)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
ATR_Handle = 0
ADX_Handle = 0

def OnInit():
    global ADX_Handle, ATR_Handle, min_rates_total
    AtrPeriod = 14
    min_rates_total = _int(ADXPeriod) + 1
    min_rates_total = MathMax(min_rates_total, AtrPeriod)
    ATR_Handle = iATR(None, 0, AtrPeriod)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
        return INIT_FAILED
    ADX_Handle = iADX(None, 0, ADXPeriod)
    if ADX_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of the iADX indicator')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 108)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 108)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'ADXCrossing'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(ATR_Handle) < rates_total or BarsCalculated(ADX_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    ATR = Arr(0, 0.0)
    Up = Arr(0, 0.0)
    Dn = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    to_copy += 1
    if CopyBuffer(ADX_Handle, 1, 0, to_copy, Up) <= 0:
        return 0
    if CopyBuffer(ADX_Handle, 2, 0, to_copy, Dn) <= 0:
        return 0
    ArraySetAsSeries(Up, True)
    ArraySetAsSeries(Dn, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if Up[bar] > Dn[bar] and Up[bar + 1] <= Dn[bar + 1]:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if Up[bar] < Dn[bar] and Up[bar + 1] >= Dn[bar + 1]:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Adxcrossing(_MQL5Indicator):
    name = 'adxcrossing'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ADXPeriod': 50,
    }

