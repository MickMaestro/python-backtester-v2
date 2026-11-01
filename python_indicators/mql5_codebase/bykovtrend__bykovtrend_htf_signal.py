"""bykovtrend — converted from MQL5: MQL5 Indicators/BykovTrend_HTF_Signal/bykovtrend.mq5

Copyright: Ramdass - Conversion only; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Ramdass - Conversion only', 'link': '', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'BykovTrend Sell', 2: 'BykovTrend Buy'}, 'levels': [], 'description': [], 'name': 'bykovtrend', 'source': 'MQL5 Indicators/BykovTrend_HTF_Signal/bykovtrend.mq5', 'folder': 'BykovTrend_HTF_Signal', 'inputs': [{'mql': 'RISK', 'py': 'RISK', 'param': 'RISK', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'SSP', 'py': 'SSP', 'param': 'SSP', 'type': 'int', 'default': 9, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RISK = _input('RISK', 3)
SSP = _input('SSP', 9)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
uptrend_ = False
old = False
K = 0
WPR_Handle = 0
ATR_Handle = 0
StartBars = 0

def OnInit():
    global ATR_Handle, K, StartBars, WPR_Handle
    K = 33 - RISK
    StartBars = MathMax(SSP, 15) + 1
    WPR_Handle = iWPR(None, 0, SSP)
    if WPR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iWPR indicator')
    ATR_Handle = iATR(None, 0, 15)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(0, PLOT_LABEL, 'BykovTrend Sell')
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(1, PLOT_LABEL, 'BykovTrend Buy')
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'BykovTrendSig'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global old, uptrend_
    if (BarsCalculated(WPR_Handle) < rates_total or BarsCalculated(ATR_Handle) < rates_total) or rates_total < StartBars:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    range_ = 0.0
    wpr = 0.0
    WPR = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    uptrend = False
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
        limit = rates_total - StartBars
        uptrend_ = False
        old = False
    else:
        to_copy = rates_total - prev_calculated + 1
        limit = rates_total - prev_calculated
    if CopyBuffer(WPR_Handle, 0, 0, to_copy, WPR) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(WPR, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    uptrend = uptrend_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            uptrend_ = uptrend
        wpr = WPR[bar]
        range_ = (ATR[bar] * 3) / 8
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if wpr < (-100 + K):
            uptrend = False
        if wpr > (-K):
            uptrend = True
        if (not old) and uptrend:
            BuyBuffer[bar] = low[bar] - range_
        if old and (not uptrend):
            SellBuffer[bar] = high[bar] + range_
        if bar:
            old = uptrend
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Bykovtrend(_MQL5Indicator):
    name = 'bykovtrend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RISK': 3,
        'SSP': 9,
    }

