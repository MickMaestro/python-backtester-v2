"""Speed_of_trade — converted from MQL5: MQL5 Indicators/Speed_of_trade/Speed_of_trade.mq5

Speed of trade indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711680], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Upwards', 2: 'Downwards'}, 'levels': [], 'description': ['Speed of trade indicator'], 'name': 'Speed_of_trade', 'source': 'MQL5 Indicators/Speed_of_trade/Speed_of_trade.mq5', 'folder': 'Speed_of_trade', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpMultiplier', 'py': 'InpMultiplier', 'param': 'InpMultiplier', 'type': 'double', 'default': 2.0, 'label': 'Multiplier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Period
InpMultiplier = _input('InpMultiplier', 2.0)  # Multiplier
BufferToUP = Arr(0, 0.0)
BufferToDN = Arr(0, 0.0)
BufferSoT = Arr(0, 0.0)
BufferAVG = Arr(0, 0.0)
period_ind = 0
multiplier = 0.0

def OnInit():
    global multiplier, period_ind
    period_ind = (2 if (InpPeriod < 2) else InpPeriod)
    multiplier = (0.01 if (InpMultiplier < 0.01) else InpMultiplier)
    SetIndexBuffer(0, BufferToUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferToDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferSoT, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferAVG, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Speed of trade (' + _str(period_ind) + ',' + DoubleToString(InpMultiplier, 2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    ArraySetAsSeries(BufferToUP, True)
    ArraySetAsSeries(BufferToDN, True)
    ArraySetAsSeries(BufferSoT, True)
    ArraySetAsSeries(BufferAVG, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < 2:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferToUP, EMPTY_VALUE)
        ArrayInitialize(BufferToDN, EMPTY_VALUE)
        ArrayInitialize(BufferSoT, 0)
        ArrayInitialize(BufferAVG, 0)
    for i in range(limit, 0 - 1, -1):
        BufferSoT[i] = ((_fdiv(close[i] - open[i], tick_volume[i]) * 1000000000) if (tick_volume[i] != 0) else 0)
    SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_ind, BufferSoT, BufferAVG)
    for i in range(limit, 0 - 1, -1):
        AVG = BufferAVG[i] * multiplier
        if BufferSoT[i] < AVG:
            BufferToUP[i] = EMPTY_VALUE
            BufferToDN[i] = EMPTY_VALUE
        else:
            if close[i] > open[i]:
                BufferToDN[i] = EMPTY_VALUE
                BufferToUP[i] = high[i]
            if close[i] < open[i]:
                BufferToDN[i] = low[i]
                BufferToUP[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SpeedOfTrade(_MQL5Indicator):
    name = 'Speed_of_trade'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Period
        'InpMultiplier': 2.0,  # Multiplier
    }

