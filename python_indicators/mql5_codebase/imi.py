"""IMI — converted from MQL5: MQL5 Indicators/IMI/IMI.mq5

Intraday Momentum Index indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [2763429]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'IMI'}, 'levels': [], 'description': ['Intraday Momentum Index indicator'], 'name': 'IMI', 'source': 'MQL5 Indicators/IMI/IMI.mq5', 'folder': 'IMI', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 70.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 30.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpOverbought = _input('InpOverbought', 70.0)  # Overbought
InpOversold = _input('InpOversold', 30.0)  # Oversold
BufferIMI = Arr(0, 0.0)
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferAvgUP = Arr(0, 0.0)
BufferAvgDN = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_ind = 0

def OnInit():
    global overbought, oversold, period_ind
    period_ind = (2 if (InpPeriod < 2) else InpPeriod)
    oversold = (0 if (InpOversold < 0) else 99.9 if (InpOversold > 99.9) else InpOversold)
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    if overbought <= oversold:
        overbought = oversold + 0.1
    if oversold >= overbought:
        oversold = overbought - 0.1
    SetIndexBuffer(0, BufferIMI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferUP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferDN, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferAvgUP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferAvgDN, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Intraday Momentum Index (' + _str(period_ind) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 2, 'Oversold')
    ArraySetAsSeries(BufferIMI, True)
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferAvgUP, True)
    ArraySetAsSeries(BufferAvgDN, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferIMI, EMPTY_VALUE)
        ArrayInitialize(BufferUP, 0)
        ArrayInitialize(BufferDN, 0)
        ArrayInitialize(BufferAvgUP, 0)
        ArrayInitialize(BufferAvgDN, 0)
    for i in range(limit, 0 - 1, -1):
        diff = close[i] - open[i]
        if diff > 0:
            BufferUP[i] = diff
            BufferDN[i] = 0.0
        else:
            BufferUP[i] = 0.0
            BufferDN[i] = -diff
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferUP, BufferAvgUP)
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferDN, BufferAvgDN)
    for i in range(limit, 0 - 1, -1):
        U = BufferAvgUP[i]
        D = BufferAvgDN[i]
        BufferIMI[i] = (_fdiv(100.0 * U, U + D) if ((U + D) != 0) else EMPTY_VALUE)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IMI(_MQL5Indicator):
    name = 'IMI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpOverbought': 70.0,  # Overbought
        'InpOversold': 30.0,  # Oversold
    }

