"""Correlation — converted from MQL5: MQL5 Indicators/Correlation/Correlation.mq5

Correlation
Copyright: mladen; Link: https://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'https://www.mql5.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [6908265, 3329330, 3937500]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [0.8, -0.8], 'description': ['Correlation'], 'name': 'Correlation', 'source': 'MQL5 Indicators/Correlation/Correlation.mq5', 'folder': 'Correlation', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Correlation period', 'sinput': False}, {'mql': 'inpSymbol1', 'py': 'inpSymbol1', 'param': None, 'type': 'string', 'default': '', 'label': 'First symbol (leave empty for current chart symbol)', 'sinput': False}, {'mql': 'inpSymbol2', 'py': 'inpSymbol2', 'param': None, 'type': 'string', 'default': 'USDCHF', 'label': 'Second symbol (leave empty for current chart symbol)', 'sinput': False}, {'mql': 'inpColorMode', 'py': 'inpColorMode', 'param': 'inpColorMode', 'type': 'int', 'default': 0, 'label': 'Line colors :', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_NAME = 0  # MQL5 constant unknown to the converter

# enum enColorMode
clm_displayColorLine = 0
clm_displaySingleColorLine = 1
_enum('enColorMode', {0: 'clm_displayColorLine', 1: 'clm_displaySingleColorLine'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Correlation period
inpSymbol1 = _input('inpSymbol1', '')  # First symbol (leave empty for current chart symbol)
inpSymbol2 = _input('inpSymbol2', 'USDCHF')  # Second symbol (leave empty for current chart symbol)
inpColorMode = _input('inpColorMode', clm_displayColorLine)  # Line colors :
corr = Arr(0, 0.0)
corrc = Arr(0, 0.0)
diff1 = Arr(0, 0.0)
diff2 = Arr(0, 0.0)
_handle1 = 0
_handle2 = 0
_symbol1 = ""
_symbol2 = ""
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global _handle1, _handle2, _symbol1, _symbol2
    SetIndexBuffer(0, corr, INDICATOR_DATA)
    SetIndexBuffer(1, corrc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, diff1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, diff2, INDICATOR_CALCULATIONS)
    _symbol1 = (Symbol() if (inpSymbol1 == '') else inpSymbol1)
    _symbol2 = (Symbol() if (inpSymbol2 == '') else inpSymbol2)
    _handle1 = iMA(_symbol1, 0, inpPeriod, 0, MODE_SMA, PRICE_CLOSE)
    if _handle1 == INVALID_HANDLE:
        return INIT_FAILED
    _handle2 = iMA(_symbol2, 0, inpPeriod, 0, MODE_SMA, PRICE_CLOSE)
    if _handle2 == INVALID_HANDLE:
        IndicatorRelease(_handle1)
        return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, _symbol1 + ' to ' + _symbol2 + ' correlation (' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    if _handle1 != INVALID_HANDLE:
        IndicatorRelease(_handle1)
    if _handle2 != INVALID_HANDLE:
        IndicatorRelease(_handle2)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    if BarsCalculated(_handle1) < 0 or BarsCalculated(_handle2) < 0:
        return prev_calculated
    if not _symbolCheck(_symbol1, Period()):
        return prev_calculated
    if not _symbolCheck(_symbol2, Period()):
        return prev_calculated
    _val = Arr(1, 0.0, dyn=False)
    _rates = Arr(1, 0, dyn=False, factory=MqlRates)
    i = MathMax(prev_calculated - 1, 1)
    while i < rates_total:
        corr[i] = EMPTY_VALUE
        _copied = CopyBuffer(_handle1, 0, _DT(time[i]), 1, _val)
        if _copied != 1:
            i += 1
            continue
        _copied = CopyRates(_symbol1, 0, _DT(time[i]), 1, _rates)
        if _copied != 1:
            i += 1
            continue
        diff1[i] = _rates[0].close - _val[0]
        _copied = CopyBuffer(_handle2, 0, _DT(time[i]), 1, _val)
        if _copied != 1:
            i += 1
            continue
        _copied = CopyRates(_symbol2, 0, _DT(time[i]), 1, _rates)
        if _copied != 1:
            i += 1
            continue
        diff2[i] = _rates[0].close - _val[0]
        sum_ = 0.0
        sump1 = 0.0
        sump2 = 0.0
        k = 0
        while k < inpPeriod and (i - k) >= 0:
            sum_ += diff1[i - k] * diff2[i - k]
            sump1 += diff1[i - k] * diff1[i - k]
            sump2 += diff2[i - k] * diff2[i - k]
            k += 1
        corr[i] = (_fdiv(sum_, MathSqrt(sump1 * sump2)) if ((sump1 * sump2) != 0) else 0)
        corrc[i] = (0 if (inpColorMode == clm_displaySingleColorLine) else 1 if (corr[i] > 0) else 2)
        i += 1
    return i

def timeFrameToString(period):
    if period == PERIOD_CURRENT:
        period = Period()
    i = 0
    i = 0
    for i in range(i, ArraySize(_tfsPer)):
        if period == _tfsPer[i]:
            break
    else:
        i = _range_end(i, ArraySize(_tfsPer), 1)
    return _tfsStr[i]

def _symbolCheck(_symbol, _timeFrame):
    global _s__symbolCheck_warned
    _time = Arr(1, 0, dyn=False)
    _timeCopied = CopyTime(_symbol, _timeFrame, Bars(_symbol, _timeFrame) - 1, 1, _time)
    if _timeCopied == 1:
        if _time[0] < SeriesInfoInteger(_symbol, _timeFrame, SERIES_FIRSTDATE):
            startTime = Box(0)
            testTime = Arr(0, 0)
            if SeriesInfoInteger(_symbol, PERIOD_M1, SERIES_TERMINAL_FIRSTDATE, startTime):
                if startTime.v > 0:
                    CopyTime(_symbol, _timeFrame, _DT(_time[0]), 1, testTime)
                    SeriesInfoInteger(_symbol, _timeFrame, SERIES_FIRSTDATE, startTime)
            if startTime.v <= 0 or startTime.v > _time[0]:
                Comment(MQL5InfoString(MQL5_PROGRAM_NAME) + '\nMissing data for ' + _symbol + ' ' + timeFrameToString(_timeFrame) + ' time frame\nRe-trying on next tick')
                _s__symbolCheck_warned = True
                return False
        if _s__symbolCheck_warned:
            Comment('')
            _s__symbolCheck_warned = False
    return True

# ---- static local variables
_s__symbolCheck_warned = False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Correlation(_MQL5Indicator):
    name = 'Correlation'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Correlation period
        'inpColorMode': _Choice({0: 'Display two colored line', 1: 'Display single colored line'}, default=0),  # Line colors :
    }

