"""wprsisignal — converted from MQL5: MQL5 Indicators/WPRSI signal/wprsisignal.mq5

Copyright: Copyright © 2009, gumgum; Link: 1967policmen@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, gumgum', 'link': '1967policmen@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'WPRSI signal Sell', 2: 'WPRSI signal Buy'}, 'levels': [], 'description': [], 'name': 'wprsisignal', 'source': 'MQL5 Indicators/WPRSI signal/wprsisignal.mq5', 'folder': 'WPRSI signal', 'inputs': [{'mql': 'WPRSI_period', 'py': 'WPRSI_period', 'param': 'WPRSI_period', 'type': 'int', 'default': 27, 'label': '', 'sinput': False}, {'mql': 'filterUP', 'py': 'filterUP', 'param': 'filterUP', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'filterDN', 'py': 'filterDN', 'param': 'filterDN', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
WPRSI_period = _input('WPRSI_period', 27)
filterUP = _input('filterUP', 10)
filterDN = _input('filterDN', 10)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
WPR_Handle = 0
RSI_Handle = 0
min_rates_total = 0
FilterMax = 0

def OnInit():
    global FilterMax, RSI_Handle, WPR_Handle, min_rates_total
    FilterMax = 2 + MathMax(filterUP, filterDN)
    min_rates_total = WPRSI_period + FilterMax
    WPR_Handle = iWPR(None, 0, WPRSI_period)
    if WPR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the WPR indicator')
    RSI_Handle = iRSI(None, 0, WPRSI_period, PRICE_CLOSE)
    if RSI_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the RSI indicator')
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'WPRSI signal'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(WPR_Handle) < rates_total or BarsCalculated(RSI_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    WPR = Arr(0, 0.0)
    RSI = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(RSI_Handle, 0, 0, to_copy, RSI) <= 0:
        return 0
    to_copy += FilterMax
    if CopyBuffer(WPR_Handle, 0, 0, to_copy, WPR) <= 0:
        return 0
    ArraySetAsSeries(WPR, True)
    ArraySetAsSeries(RSI, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = EMPTY_VALUE
        SellBuffer[bar] = EMPTY_VALUE
        if (WPR[bar] > -20 and WPR[bar + 1] < -20) and RSI[bar] > 50:
            z = 0.0
            for k in range(2, filterUP + 2 + 1):
                if WPR[bar + k] > -20:
                    z = 1.0
            if z == 0:
                BuyBuffer[bar] = low[bar] - ((high[bar] - low[bar]) / 2)
        if (WPR[bar + 1] > -80 and WPR[bar] < -80) and RSI[bar] < 50:
            h = 0.0
            for c in range(2, filterDN + 2 + 1):
                if WPR[bar + c] < -80:
                    h = 1.0
            if h == 0:
                SellBuffer[bar] = high[bar] + ((high[bar] - low[bar]) / 2)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Wprsisignal(_MQL5Indicator):
    name = 'wprsisignal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'WPRSI_period': 27,
        'filterUP': 10,
        'filterDN': 10,
    }

