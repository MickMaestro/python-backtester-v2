"""Volatility_Ratio — converted from MQL5: MQL5 Indicators/Volatility_Ratio/Volatility_Ratio.mq5

Volatility Ratio oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [13434880]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'VR'}, 'levels': [], 'description': ['Volatility Ratio oscillator'], 'name': 'Volatility_Ratio', 'source': 'MQL5 Indicators/Volatility_Ratio/Volatility_Ratio.mq5', 'folder': 'Volatility_Ratio', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
BufferVR = Arr(0, 0.0)
period = 0

def OnInit():
    global period
    period = (1 if (InpPeriod < 1) else InpPeriod)
    SetIndexBuffer(0, BufferVR, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Volatility Ratio (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 0.5)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0.01)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 1.0)
    ArraySetAsSeries(BufferVR, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < period:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferVR, EMPTY_VALUE)
    for i in range(limit, 0 - 1, -1):
        bl = Lowest(period, i)
        bh = Highest(period, i)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        min_ = low[bl]
        max_ = high[bh]
        pr = fmax(max_, open[i + period - 1]) - fmin(min_, open[i + period - 1])
        hl = fabs(high[i] - low[i])
        hc = fabs(high[i] - close[i + 1])
        lc = fabs(low[i] - close[i + 1])
        tr = fmax(hl, fmin(hc, lc))
        BufferVR[i] = _fdiv(tr, (pr if (pr != 0) else 1.0))
    return rates_total

def Highest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyHigh(Symbol(), PERIOD_CURRENT, start, count, array) == count:
        return ArrayMaximum(array) + start
    return WRONG_VALUE

def Lowest(count, start):
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyLow(Symbol(), PERIOD_CURRENT, start, count, array) == count:
        return ArrayMinimum(array) + start
    return WRONG_VALUE


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolatilityRatio(_MQL5Indicator):
    name = 'Volatility_Ratio'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
    }

