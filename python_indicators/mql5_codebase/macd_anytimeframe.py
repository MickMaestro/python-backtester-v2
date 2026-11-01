"""macd_anytimeframe — converted from MQL5: MQL5 Indicators/MACD - Any higher timeframe/macd_anytimeframe.mq5

Moving Average Convergence/Divergence - Any higher timeframe
Copyright: Slacktrader

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Slacktrader', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 3, 2: 1}, 'colors': {1: [12632256], 2: [255]}, 'widths': {1: 2, 2: 1}, 'styles': {}, 'labels': {1: 'MACD', 2: 'Signal'}, 'levels': [], 'description': ['Moving Average Convergence/Divergence - Any higher timeframe'], 'name': 'macd_anytimeframe', 'source': 'MQL5 Indicators/MACD - Any higher timeframe/macd_anytimeframe.mq5', 'folder': 'MACD - Any higher timeframe', 'inputs': [{'mql': 'ANY_TIMEFRAME', 'py': 'ANY_TIMEFRAME', 'param': 'ANY_TIMEFRAME', 'type': 'int', 'default': 16385, 'label': 'Timeframe of MACD which we want to see instead of current Period', 'sinput': False}, {'mql': 'InpFastEMA', 'py': 'InpFastEMA', 'param': 'InpFastEMA', 'type': 'int', 'default': 12, 'label': 'Fast EMA period', 'sinput': False}, {'mql': 'InpSlowEMA', 'py': 'InpSlowEMA', 'param': 'InpSlowEMA', 'type': 'int', 'default': 26, 'label': 'Slow EMA period', 'sinput': False}, {'mql': 'InpSignalSMA', 'py': 'InpSignalSMA', 'param': 'InpSignalSMA', 'type': 'int', 'default': 9, 'label': 'Signal SMA period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ANY_TIMEFRAME = _input('ANY_TIMEFRAME', PERIOD_H1)  # Timeframe of MACD which we want to see instead of current Period
InpFastEMA = _input('InpFastEMA', 12)  # Fast EMA period
InpSlowEMA = _input('InpSlowEMA', 26)  # Slow EMA period
InpSignalSMA = _input('InpSignalSMA', 9)  # Signal SMA period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
ExtMacdBuffer = Arr(0, 0.0)
ExtSignalBuffer = Arr(0, 0.0)
ExtMacdBuffer2pom = Arr(0, 0.0)
ExtSignalBuffer2pom = Arr(0, 0.0)
MacdHandle = 0
PeriodRatio = 0

def PeriodStr(val):
    i = 0
    if val < 0:
        return 'ERROR'
    if val == PERIOD_CURRENT:
        val = ChartPeriod()
    i = 0
    for i in range(i, 20):
        if val == _s_PeriodStr__p_int[i]:
            break
    else:
        i = _range_end(i, 20, 1)
    return _s_PeriodStr__p_str[i]

def OnInit():
    global MacdHandle, PeriodRatio
    SetIndexBuffer(0, ExtMacdBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtSignalBuffer, INDICATOR_DATA)
    MacdHandle = iMACD(None, ANY_TIMEFRAME, InpFastEMA, InpSlowEMA, InpSignalSMA, InpAppliedPrice)
    PeriodRatio = _idiv(PeriodSeconds(ANY_TIMEFRAME), PeriodSeconds())
    IndicatorSetString(INDICATOR_SHORTNAME, 'MACD - Any Timeframe - ' + PeriodStr(ANY_TIMEFRAME))
    Comment('')
    if PeriodRatio < 1:
        Comment('Variable ANY_TIMEFRAME has to be a Timeframe equal or higher then current chart!', 'Please coose right timeframe!')
        return -1
    return 0

def OnCalculate(rates_total, prev_calculated, begin, price):
    if BarsCalculated(MacdHandle) < _idiv(rates_total, PeriodRatio):
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        to_copy += 1
    CopyBuffer(MacdHandle, 0, 0, _idiv(to_copy, PeriodRatio), ExtMacdBuffer2pom)
    CopyBuffer(MacdHandle, 1, 0, _idiv(to_copy, PeriodRatio), ExtSignalBuffer2pom)
    ArrayResize(ExtMacdBuffer, ArraySize(ExtMacdBuffer2pom) * PeriodRatio)
    for i in range(0, ArraySize(ExtMacdBuffer2pom)):
        for j in range(0, PeriodRatio):
            ExtMacdBuffer[_int(fmod(to_copy, PeriodRatio)) + (i * PeriodRatio) + j] = ExtMacdBuffer2pom[i]
    ArrayResize(ExtSignalBuffer, ArraySize(ExtSignalBuffer2pom) * PeriodRatio)
    for i in range(0, ArraySize(ExtSignalBuffer2pom)):
        for j in range(0, PeriodRatio):
            ExtSignalBuffer[_int(fmod(to_copy, PeriodRatio)) + (i * PeriodRatio) + j] = ExtSignalBuffer2pom[i]
    return rates_total

# ---- static local variables
_s_PeriodStr__p_str = Arr.of(['M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M10', 'M12', 'M15', 'M20', 'M30', 'H1', 'H2', 'H3', 'H4', 'H6', 'H12', 'D1', 'W1', 'MN', 'UNKNOWN'], fill="")
_s_PeriodStr__p_int = Arr.of([1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 0x4001, 0x4002, 0x4003, 0x4004, 0x4006, 0x400c, 0x4018, 0x8001, 0xc001], fill=0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MacdAnytimeframe(_MQL5Indicator):
    name = 'macd_anytimeframe'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ANY_TIMEFRAME': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # Timeframe of MACD which we want to see instead of current Period
        'InpFastEMA': 12,  # Fast EMA period
        'InpSlowEMA': 26,  # Slow EMA period
        'InpSignalSMA': 9,  # Signal SMA period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

