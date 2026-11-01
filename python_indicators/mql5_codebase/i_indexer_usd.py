"""i_indexer_usd — converted from MQL5: MQL5 Indicators/Simple dollar index indicator/i_indexer_usd.mq5

Copyright: Copyright 2013, Silent; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2013, Silent', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [65280]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'USD'}, 'levels': [], 'description': [], 'name': 'i_indexer_usd', 'source': 'MQL5 Indicators/Simple dollar index indicator/i_indexer_usd.mq5', 'folder': 'Simple dollar index indicator', 'inputs': [{'mql': 'countBars', 'py': 'countBars', 'param': 'countBars', 'type': 'int', 'default': 216, 'label': 'bars for calculation', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
countBars = _input('countBars', 216)  # bars for calculation
i = 0
ShortName = ""
bad = False
success = False
USDBufferPlot = Arr(0, 0.0)
EURUSD = Arr(0, 0.0)
GBPUSD = Arr(0, 0.0)
USDCHF = Arr(0, 0.0)
USDJPY = Arr(0, 0.0)
AUDUSD = Arr(0, 0.0)
USDCAD = Arr(0, 0.0)
NZDUSD = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, USDBufferPlot, INDICATOR_DATA)
    SetIndexBuffer(1, EURUSD, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, GBPUSD, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, USDCHF, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, USDJPY, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, AUDUSD, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, USDCAD, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, NZDUSD, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(USDBufferPlot, True)
    ArraySetAsSeries(EURUSD, True)
    ArraySetAsSeries(GBPUSD, True)
    ArraySetAsSeries(USDCHF, True)
    ArraySetAsSeries(USDJPY, True)
    ArraySetAsSeries(AUDUSD, True)
    ArraySetAsSeries(USDCAD, True)
    ArraySetAsSeries(NZDUSD, True)
    copied()
    EventSetTimer(1)
    StringConcatenate(_GlobRef(globals(), 'ShortName'), 'i_Indexer_USD ', Symbol())
    IndicatorSetString(INDICATOR_SHORTNAME, ShortName)
    IndicatorSetInteger(INDICATOR_DIGITS, 6)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    global success
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, rates_total - countBars + 1)
    if prev_calculated == 0:
        ArrayInitialize(USDBufferPlot, EMPTY_VALUE)
        ArrayInitialize(EURUSD, EMPTY_VALUE)
        ArrayInitialize(GBPUSD, EMPTY_VALUE)
        ArrayInitialize(USDCHF, EMPTY_VALUE)
        ArrayInitialize(USDJPY, EMPTY_VALUE)
        ArrayInitialize(AUDUSD, EMPTY_VALUE)
        ArrayInitialize(USDCAD, EMPTY_VALUE)
        ArrayInitialize(NZDUSD, EMPTY_VALUE)
        if (not copied()) or (not GetLastError()):
            success = False
            return prev_calculated
        if copied() and GetLastError():
            countBuf()
            success = True
    if (rates_total - prev_calculated) != 0:
        if (not copied()) or (not GetLastError()):
            success = False
            return prev_calculated
        if copied() and GetLastError():
            countBuf()
            success = True
    if (not GetLastError()) or success == False:
        copied()
        ResetLastError()
        return rates_total
    return rates_total

def OnTimer():
    if (copied() and GetLastError()) and success == True:
        countBuf()
    ChartRedraw()

def OnDeinit(reason):
    EventKillTimer()
    ChartRedraw()

def copied():
    global bad
    if ((((((not CopyClose('EURUSD', Period(), 0, countBars, EURUSD)) or (not CopyClose('GBPUSD', Period(), 0, countBars, GBPUSD))) or (not CopyClose('USDCHF', Period(), 0, countBars, USDCHF))) or (not CopyClose('USDJPY', Period(), 0, countBars, USDJPY))) or (not CopyClose('AUDUSD', Period(), 0, countBars, AUDUSD))) or (not CopyClose('USDCAD', Period(), 0, countBars, USDCAD))) or (not CopyClose('NZDUSD', Period(), 0, countBars, NZDUSD)):
        bad = False
    if (((((CopyClose('EURUSD', Period(), 0, countBars, EURUSD) and CopyClose('GBPUSD', Period(), 0, countBars, GBPUSD)) and CopyClose('USDCHF', Period(), 0, countBars, USDCHF)) and CopyClose('USDJPY', Period(), 0, countBars, USDJPY)) and CopyClose('AUDUSD', Period(), 0, countBars, AUDUSD)) and CopyClose('USDCAD', Period(), 0, countBars, USDCAD)) and CopyClose('NZDUSD', Period(), 0, countBars, NZDUSD):
        bad = True
    return bad

def countBuf():
    global i, success
    i = 0
    while i < countBars:
        USDBufferPlot[i] = ((100 * MathPow(EURUSD[i], 0.125)) + (100 * MathPow(GBPUSD[i], 0.125)) + (100 * MathPow(USDCHF[i], 0.125)) + (100 * MathPow(USDJPY[i], 0.125)) + (100 * MathPow(AUDUSD[i], 0.125)) + (100 * MathPow(USDCAD[i], 0.125)) + (100 * MathPow(NZDUSD[i], 0.125))) / 8
        i += 1
    success = False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IIndexerUsd(_MQL5Indicator):
    name = 'i_indexer_usd'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'countBars': 216,  # bars for calculation
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

