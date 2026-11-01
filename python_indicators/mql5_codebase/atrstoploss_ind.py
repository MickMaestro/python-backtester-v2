"""ATRStopLoss_Ind — converted from MQL5: MQL5 Indicators/ATR Stop Loss/ATRStopLoss_Ind.mq5

Based on https://www.mql5.com/en/forum/349885 , this indicator will draw ATR based stop loss calculation with adjustable multiplier and ATR period.
This indicator includes helper functions and example to run calculation via function call so the calculation logic can be placed in external include file
Copyright: Rosh Jardine (MQL5/MQL4); Link: https://roshjardine.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Rosh Jardine (MQL5/MQL4)', 'link': 'https://roshjardine.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [14053594], 2: [16711680]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Up', 2: 'Dn'}, 'levels': [], 'description': ['Based on https://www.mql5.com/en/forum/349885 , this indicator will draw ATR based stop loss calculation with adjustable multiplier and ATR period.', 'This indicator includes helper functions and example to run calculation via function call so the calculation logic can be placed in external include file'], 'name': 'ATRStopLoss_Ind', 'source': 'MQL5 Indicators/ATR Stop Loss/ATRStopLoss_Ind.mq5', 'folder': 'ATR Stop Loss', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 10, 'label': 'how many look back periods to check the price', 'sinput': False}, {'mql': 'ATRperiod', 'py': 'ATRperiod', 'param': 'ATRperiod', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'Kv', 'py': 'Kv', 'param': 'Kv', 'type': 'double', 'default': 2.5, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 10)  # how many look back periods to check the price
ATRperiod = _input('ATRperiod', 10)
Kv = _input('Kv', 2.5)
UpBuffer1 = Arr(0, 0.0)
DnBuffer1 = Arr(0, 0.0)
smin = Arr(0, 0.0)
smax = Arr(0, 0.0)
trend = Arr(0, 0.0)
AtrHandle = 0
AtrBfr = Arr(1, 0.0, dyn=False)
bars_calculated = 0
short_name = ""

def OnInit():
    global AtrHandle, bars_calculated, short_name
    bars_calculated = 0
    short_name = 'ATRStopLoss_Ind'
    AtrHandle = iATR(Symbol(), Period(), ATRperiod)
    if AtrHandle == INVALID_HANDLE:
        return INIT_FAILED
    ArrayInitialize(AtrBfr, EMPTY_VALUE)
    SetIndexBuffer(0, UpBuffer1)
    SetIndexBuffer(1, DnBuffer1)
    SetIndexBuffer(2, smin)
    SetIndexBuffer(3, smax)
    SetIndexBuffer(4, trend)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, Length)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, Length)
    PlotIndexSetInteger(0, PLOT_SHIFT, 0)
    PlotIndexSetInteger(1, PLOT_SHIFT, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global bars_calculated
    limit = 0
    if rates_total <= Length:
        return 0
    if prev_calculated < 1:
        limit = rates_total - Length - 1
        if not AtrStopFirstRun(limit, UpBuffer1, DnBuffer1, smin, smax, trend, _GlobRef(globals(), 'AtrHandle'), AtrBfr, Length, Symbol(), Period(), Kv):
            StopIndicator()
        bars_calculated = limit
        return rates_total
    else:
        limit = prev_calculated - Length - 1
        if limit > bars_calculated:
            if not AtrStopNextRun(bars_calculated + 1, UpBuffer1, DnBuffer1, smin, smax, trend, _GlobRef(globals(), 'AtrHandle'), AtrBfr, Length, Symbol(), Period(), Kv, False):
                StopIndicator()
            bars_calculated += 1
        else:
            if not AtrStopNextRun(bars_calculated + 1, UpBuffer1, DnBuffer1, smin, smax, trend, _GlobRef(globals(), 'AtrHandle'), AtrBfr, Length, Symbol(), Period(), Kv, True):
                StopIndicator()
        return rates_total

def AtrStopNextRun(newlimit, upbfr, dnbfr, min_, max_, trd, atrhandler, atrbuffer, atrlength, symbol, tframe, multiplier, samebar):
    if not samebar:
        ArrayResize(upbfr, newlimit)
        ArrayResize(dnbfr, newlimit)
        ArrayResize(min_, newlimit)
        ArrayResize(max_, newlimit)
        ArrayResize(trd, newlimit)
        trd[0] = EMPTY_VALUE
        max_[0] = trd[0]
        min_[0] = max_[0]
        dnbfr[0] = min_[0]
        upbfr[0] = dnbfr[0]
    else:
        trd[0] = EMPTY_VALUE
        max_[0] = trd[0]
        min_[0] = max_[0]
        dnbfr[0] = min_[0]
        upbfr[0] = dnbfr[0]
    for j in range(0, 1 + 1):
        min_[j] = -100000.0
        max_[j] = 100000.0
        for k in range(0, atrlength - 1 + 1):
            copybuffer = CopyBuffer(atrhandler.v, 0, j + k, 1, atrbuffer)
            if copybuffer < 1:
                return False
            min_[j] = MathMax(smin[j], iHigh(symbol, tframe, j + k) - (multiplier * AtrBfr[0]))
            max_[j] = MathMin(smax[j], iLow(symbol, tframe, j + k) + (multiplier * AtrBfr[0]))
        trd[j] = trd[j + 1]
        if iClose(symbol, tframe, j) > max_[j + 1]:
            trd[j] = 1.0
        if iClose(symbol, tframe, j) < min_[j + 1]:
            trd[j] = -1.0
        if trd[j] > 0:
            if min_[j] < min_[j + 1]:
                min_[j] = min_[j + 1]
            upbfr[j] = min_[j]
            dnbfr[j] = EMPTY_VALUE
        if trend[j] < 0:
            if max_[j] > max_[j + 1]:
                max_[j] = max_[j + 1]
            upbfr[j] = EMPTY_VALUE
            dnbfr[j] = max_[j]
    return True

def AtrStopFirstRun(limit, upbfr, dnbfr, min_, max_, trd, atrhandler, atrbuffer, atrlength, symbol, tframe, multiplier):
    ArrayInitialize(upbfr, EMPTY_VALUE)
    ArrayInitialize(dnbfr, EMPTY_VALUE)
    ArrayInitialize(min_, EMPTY_VALUE)
    ArrayInitialize(max_, EMPTY_VALUE)
    ArrayInitialize(trd, EMPTY_VALUE)
    ArraySetAsSeries(upbfr, True)
    ArraySetAsSeries(dnbfr, True)
    ArraySetAsSeries(min_, True)
    ArraySetAsSeries(max_, True)
    ArraySetAsSeries(trd, True)
    shift = 0
    shift = limit
    for shift in range(shift, 0 - 1, -1):
        min_[shift] = -100000.0
        max_[shift] = 100000.0
        for i in range(atrlength - 1, 0 - 1, -1):
            copybuffer = CopyBuffer(atrhandler.v, 0, shift + i, 1, atrbuffer)
            if copybuffer < 1:
                return False
            min_[shift] = MathMax(min_[shift], iHigh(symbol, tframe, shift + i) - (multiplier * atrbuffer[0]))
            max_[shift] = MathMin(max_[shift], iLow(symbol, tframe, shift + i) + (multiplier * atrbuffer[0]))
        trd[shift] = trd[shift + 1]
        if iClose(symbol, tframe, shift) > max_[shift + 1]:
            trd[shift] = 1.0
        if iClose(symbol, tframe, shift) < min_[shift + 1]:
            trd[shift] = -1.0
        if trd[shift] > 0:
            if min_[shift] < min_[shift + 1]:
                min_[shift] = min_[shift + 1]
            upbfr[shift] = min_[shift]
            dnbfr[shift] = EMPTY_VALUE
        if trd[shift] < 0:
            if max_[shift] > max_[shift + 1]:
                max_[shift] = max_[shift + 1]
            upbfr[shift] = EMPTY_VALUE
            dnbfr[shift] = max_[shift]
    else:
        shift = _range_end(shift, 0 - 1, -1)
    return True

def StopIndicator():
    IndicatorRelease(AtrHandle)
    ChartIndicatorDelete(ChartID(), 0, short_name)

def OnDeinit(reason):
    if AtrHandle != INVALID_HANDLE:
        IndicatorRelease(AtrHandle)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ATRStopLossInd(_MQL5Indicator):
    name = 'ATRStopLoss_Ind'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 10,  # how many look back periods to check the price
        'ATRperiod': 10,
        'Kv': 2.5,
    }

