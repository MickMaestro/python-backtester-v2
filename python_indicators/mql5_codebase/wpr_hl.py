"""WPR_HL — converted from MQL5: MQL5 Indicators/WPR_HL/WPR_HL.mq5

WPR_HL oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [11829830]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'WPR HL'}, 'levels': [], 'description': ['WPR_HL oscillator'], 'name': 'WPR_HL', 'source': 'MQL5 Indicators/WPR_HL/WPR_HL.mq5', 'folder': 'WPR_HL', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 20.0, 'label': 'Overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 80.0, 'label': 'Oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpOverbought = _input('InpOverbought', 20.0)  # Overbought
InpOversold = _input('InpOversold', 80.0)  # Oversold
BufferWPRHL = Arr(0, 0.0)
BufferHL = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period = 0

def OnInit():
    global overbought, oversold, period
    period = (2 if (InpPeriod < 2) else InpPeriod)
    ob = -fabs(InpOverbought)
    os = -fabs(InpOversold)
    overbought = (0 if (ob > 0) else -99.0 if (ob < -99.0) else ob)
    oversold = (-100.0 if (os < -100.0) else (overbought - 1.0) if (os >= overbought) else os)
    if overbought <= oversold:
        overbought = oversold + 1.0
    SetIndexBuffer(0, BufferWPRHL, INDICATOR_DATA)
    SetIndexBuffer(1, BufferHL, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'High/Low WPR (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, overbought)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, oversold)
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'Overbought')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Oversold')
    ArraySetAsSeries(BufferWPRHL, True)
    ArraySetAsSeries(BufferHL, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period - 1
        ArrayInitialize(BufferWPRHL, EMPTY_VALUE)
        ArrayInitialize(BufferHL, 0)
    for i in range(limit, 0 - 1, -1):
        BufferHL[i] = high[i] - low[i]
    for i in range(limit, 0 - 1, -1):
        bl = ArrayMinimum(BufferHL, i, period)
        bh = ArrayMaximum(BufferHL, i, period)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        min_ = BufferHL[bl]
        max_ = BufferHL[bh]
        BufferWPRHL[i] = (_fdiv(-100.0 * (max_ - BufferHL[i]), max_ - min_) if (max_ != min_) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WPRHL(_MQL5Indicator):
    name = 'WPR_HL'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpOverbought': 20.0,  # Overbought
        'InpOversold': 80.0,  # Oversold
    }

