"""NonLagRSI — converted from MQL5: MQL5 Indicators/Non Lag Relative Strength Index for MT5/NonLagRSI.mq5

Non Lag Relative Strength Index
Eliminates unnecessary preliminary calculations on the built-in RSI
Copyright: 2009-2020, MetaQuotes Software Corp. ~ By 3rjfx ~ Created: 04/04/2020; Link: https://www.mql5.com/en/users/3rjfx; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009-2020, MetaQuotes Software Corp. ~ By 3rjfx ~ Created: 04/04/2020', 'link': 'https://www.mql5.com/en/users/3rjfx', 'version': '1.00', 'window': 'separate', 'indicator_minimum': 0.0, 'indicator_maximum': 100.0, 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [30.0, 50.0, 70.0], 'description': ['Non Lag Relative Strength Index', 'Eliminates unnecessary preliminary calculations on the built-in RSI'], 'name': 'NonLagRSI', 'source': 'MQL5 Indicators/Non Lag Relative Strength Index for MT5/NonLagRSI.mq5', 'folder': 'Non Lag Relative Strength Index for MT5', 'inputs': [{'mql': 'InpPeriodRSI', 'py': 'InpPeriodRSI', 'param': 'InpPeriodRSI', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'eprice', 'py': 'eprice', 'param': 'eprice', 'type': 'int', 'default': 7, 'label': 'Calculation Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodRSI = _input('InpPeriodRSI', 14)  # Period
eprice = _input('eprice', PRICE_WEIGHTED)  # Calculation Price
ExtRSIBuffer = Arr(0, 0.0)
ExtPosBuffer = Arr(0, 0.0)
ExtNegBuffer = Arr(0, 0.0)
diffup = Arr(0, 0.0)
diffdn = Arr(0, 0.0)
ExtPeriodRSI = 0

def OnInit():
    global ExtPeriodRSI
    if InpPeriodRSI < 1:
        ExtPeriodRSI = 14
        Print('Incorrect value for input variable InpPeriodRSI =', InpPeriodRSI, 'Indicator will use value =', ExtPeriodRSI, 'for calculations.')
    else:
        ExtPeriodRSI = InpPeriodRSI
    SetIndexBuffer(0, ExtRSIBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtPosBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, ExtNegBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, diffup, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, diffdn, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtPeriodRSI)
    nameadd = ''
    _sw1 = eprice
    if _sw1 == PRICE_CLOSE:
        nameadd = 'Close price'
    elif _sw1 == PRICE_OPEN:
        nameadd = 'Open price'
    elif _sw1 == PRICE_HIGH:
        nameadd = 'High price'
    elif _sw1 == PRICE_LOW:
        nameadd = 'Low price'
    elif _sw1 == PRICE_MEDIAN:
        nameadd = 'Median price'
    elif _sw1 == PRICE_TYPICAL:
        nameadd = 'Typical price'
    elif _sw1 == PRICE_WEIGHTED:
        nameadd = 'Average price'
    IndicatorSetString(INDICATOR_SHORTNAME, 'NonLagRSI(' + _str(ExtPeriodRSI) + '-' + nameadd + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    PrintFormat('%s: Deinitialization reason code=%d', 'OnDeinit', reason)
    Print(getUninitReasonText(reason))
    ObjectsDeleteAll(0, -1, -1)
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = 0
    pos = 0
    diff = 0.0
    if rates_total < 125:
        return 0
    limit = rates_total - prev_calculated
    if limit == 0:
        limit = ExtPeriodRSI + 3
    if limit < ExtPeriodRSI:
        limit = ExtPeriodRSI + 3
    if prev_calculated > 0:
        limit += 1
    if limit > rates_total:
        limit = rates_total
    ArrayResize(ExtRSIBuffer, rates_total, rates_total)
    ArrayResize(ExtPosBuffer, rates_total, rates_total)
    ArrayResize(ExtNegBuffer, rates_total, rates_total)
    ArrayResize(diffup, rates_total, rates_total)
    ArrayResize(diffdn, rates_total, rates_total)
    pos = ExtPeriodRSI + 1
    for i in range(pos, rates_total):
        diff = 0.0
        _sw2 = eprice
        if _sw2 == PRICE_CLOSE:
            diff = close[i] - close[i - 1]
        elif _sw2 == PRICE_OPEN:
            diff = open[i] - open[i - 1]
        elif _sw2 == PRICE_HIGH:
            diff = high[i] - high[i - 1]
        elif _sw2 == PRICE_LOW:
            diff = low[i] - low[i - 1]
        elif _sw2 == PRICE_MEDIAN:
            diff = ((high[i] + low[i]) / 2.0) - ((high[i - 1] + low[i - 1]) / 2.0)
        elif _sw2 == PRICE_TYPICAL:
            diff = ((high[i] + low[i] + close[i]) / 3.0) - ((high[i - 1] + low[i - 1] + close[i - 1]) / 3.0)
        elif _sw2 == PRICE_WEIGHTED:
            diff = ((high[i] + low[i] + close[i] + close[i]) / 4.0) - ((high[i - 1] + low[i - 1] + close[i - 1] + close[i - 1]) / 4.0)
        diffup[i] = (diff if (diff > 0.0) else 0.0)
        diffdn[i] = ((-diff) if (diff < 0.0) else 0.0)
        ExtPosBuffer[i] = _fdiv((ExtPosBuffer[i - 1] * (ExtPeriodRSI - 1)) + diffup[i], ExtPeriodRSI)
        ExtNegBuffer[i] = _fdiv((ExtNegBuffer[i - 1] * (ExtPeriodRSI - 1)) + diffdn[i], ExtPeriodRSI)
        if ExtNegBuffer[i] != 0.0:
            ExtRSIBuffer[i] = 100.0 - _fdiv(100.0, 1 + _fdiv(ExtPosBuffer[i], ExtNegBuffer[i]))
        else:
            if ExtPosBuffer[i] != 0.0:
                ExtRSIBuffer[i] = 100.0
            else:
                ExtRSIBuffer[i] = 50.0
    return rates_total

def getUninitReasonText(reasonCode):
    text = ''
    _sw3 = reasonCode
    if _sw3 == REASON_PROGRAM:
        text = 'The EA has stopped working calling by remove function.'
    elif _sw3 == REASON_REMOVE:
        text = 'Program ' + 'NonLagRSI.mq5' + ' was removed from chart'
    elif _sw3 == REASON_RECOMPILE:
        text = 'Program recompiled.'
    elif _sw3 == REASON_CHARTCHANGE:
        text = 'Symbol or timeframe was changed'
    elif _sw3 == REASON_CHARTCLOSE:
        text = 'Chart was closed'
    elif _sw3 == REASON_PARAMETERS:
        text = 'Input-parameter was changed'
    elif _sw3 == REASON_ACCOUNT:
        text = 'Account was changed'
    elif _sw3 == REASON_TEMPLATE:
        text = 'New template was applied to chart'
    elif _sw3 == REASON_INITFAILED:
        text = 'The OnInit() handler returned a non-zero value.'
    elif _sw3 == REASON_CLOSE:
        text = 'Terminal closed.'
    else:
        text = 'Another reason'
    return text


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NonLagRSI(_MQL5Indicator):
    name = 'NonLagRSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodRSI': 14,  # Period
        'eprice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=7),  # Calculation Price
    }
    y_range = (0.0, 100.0)

