"""SSSAR — converted from MQL5: MQL5 Indicators/SSSAR/SSSAR.mq5

Single Stream SAR
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [32768]}, 'widths': {1: 5, 2: 5}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'SAR Bearish', 2: 'SAR Bullish'}, 'levels': [], 'description': ['Single Stream SAR'], 'name': 'SSSAR', 'source': 'MQL5 Indicators/SSSAR/SSSAR.mq5', 'folder': 'SSSAR', 'inputs': [{'mql': 'InpStep', 'py': 'InpStep', 'param': 'InpStep', 'type': 'double', 'default': 0.02, 'label': 'Step', 'sinput': False}, {'mql': 'InpMax', 'py': 'InpMax', 'param': 'InpMax', 'type': 'double', 'default': 0.2, 'label': 'Maximum', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpStep = _input('InpStep', 0.02)  # Step
InpMax = _input('InpMax', 0.2)  # Maximum
BufferBullish = Arr(0, 0.0)
BufferBearish = Arr(0, 0.0)
BufferTradeHigh = Arr(0, 0.0)
BufferTradeLow = Arr(0, 0.0)
BufferPosition = Arr(0, 0.0)
BufferParOp = Arr(0, 0.0)
BufferAF = Arr(0, 0.0)
BufferSAR = Arr(0, 0.0)
step = 0.0
max_ = 0.0

def OnInit():
    global max_, step
    step = (0.0001 if (InpStep < 0.0001) else InpStep)
    max_ = (0.0001 if (InpMax < 0.0001) else InpMax)
    SetIndexBuffer(0, BufferBearish, INDICATOR_DATA)
    SetIndexBuffer(1, BufferBullish, INDICATOR_DATA)
    SetIndexBuffer(2, BufferTradeHigh, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferTradeLow, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferPosition, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferParOp, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferAF, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferSAR, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 158)
    PlotIndexSetInteger(1, PLOT_ARROW, 158)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SSSAR (' + DoubleToString(step, 2) + ',' + DoubleToString(max_, 2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferBearish, True)
    ArraySetAsSeries(BufferBullish, True)
    ArraySetAsSeries(BufferTradeHigh, True)
    ArraySetAsSeries(BufferTradeLow, True)
    ArraySetAsSeries(BufferPosition, True)
    ArraySetAsSeries(BufferParOp, True)
    ArraySetAsSeries(BufferAF, True)
    ArraySetAsSeries(BufferSAR, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferBearish, EMPTY_VALUE)
        ArrayInitialize(BufferBullish, EMPTY_VALUE)
        ArrayInitialize(BufferTradeHigh, 0)
        ArrayInitialize(BufferTradeLow, 0)
        ArrayInitialize(BufferPosition, 0)
        ArrayInitialize(BufferParOp, 0)
        ArrayInitialize(BufferAF, 0)
        ArrayInitialize(BufferSAR, 0)
    for i in range(limit, 0 - 1, -1):
        if i == (rates_total - 2):
            BufferTradeHigh[i] = high[i + 1]
            BufferTradeLow[i] = low[i + 1]
            BufferPosition[i] = -1.0
            BufferParOp[i] = high[i + 1]
            BufferAF[i] = 0.0
        else:
            BufferParOp[i] = BufferParOp[i + 1]
            BufferPosition[i] = BufferPosition[i + 1]
            BufferTradeHigh[i] = BufferTradeHigh[i + 1]
            BufferTradeLow[i] = BufferTradeLow[i + 1]
            BufferAF[i] = BufferAF[i + 1]
        if high[i] > BufferTradeHigh[i]:
            BufferTradeHigh[i] = high[i]
        if low[i] < BufferTradeLow[i]:
            BufferTradeLow[i] = low[i]
        if BufferPosition[i] == 1:
            if low[i] < BufferParOp[i]:
                BufferPosition[i] = -1.0
                BufferSAR[i] = BufferTradeHigh[i]
                BufferTradeHigh[i] = high[i]
                BufferTradeLow[i] = low[i]
                BufferAF[i] = step
                BufferParOp[i] = BufferSAR[i] + (BufferAF[i] * (BufferTradeLow[i] - BufferSAR[i]))
                if BufferParOp[i] < high[i]:
                    BufferParOp[i] = high[i]
                if BufferParOp[i] < high[i + 1]:
                    BufferParOp[i] = high[i + 1]
            else:
                BufferSAR[i] = BufferParOp[i]
                if BufferTradeHigh[i] > BufferTradeHigh[i + 1] and BufferAF[i] < max_:
                    BufferAF[i] = BufferAF[i] + step
                    if BufferAF[i] > max_:
                        BufferAF[i] = max_
                BufferParOp[i] = BufferSAR[i] + (BufferAF[i] * (BufferTradeHigh[i] - BufferSAR[i]))
                if BufferParOp[i] > low[i]:
                    BufferParOp[i] = low[i]
                if BufferParOp[i] > low[i + 1]:
                    BufferParOp[i] = low[i + 1]
        else:
            if high[i] > BufferParOp[i]:
                BufferPosition[i] = 1.0
                BufferSAR[i] = BufferTradeLow[i]
                BufferTradeHigh[i] = high[i]
                BufferTradeLow[i] = low[i]
                BufferAF[i] = step
                BufferParOp[i] = BufferSAR[i] + (BufferAF[i] * (BufferTradeHigh[i] - BufferSAR[i]))
                if BufferParOp[i] > low[i]:
                    BufferParOp[i] = low[i]
                if BufferParOp[i] > low[i + 1]:
                    BufferParOp[i] = low[i + 1]
            else:
                BufferSAR[i] = BufferParOp[i]
                if BufferTradeLow[i] < BufferTradeLow[i + 1] and BufferAF[i] < max_:
                    BufferAF[i] = BufferAF[i] + step
                    if BufferAF[i] > max_:
                        BufferAF[i] = max_
                BufferParOp[i] = BufferSAR[i] + (BufferAF[i] * (BufferTradeLow[i] - BufferSAR[i]))
                if BufferParOp[i] < high[i]:
                    BufferParOp[i] = high[i]
                if BufferParOp[i] < high[i + 1]:
                    BufferParOp[i] = high[i + 1]
        if BufferPosition[i] == 1:
            BufferBullish[i] = BufferSAR[i]
            BufferBearish[i] = EMPTY_VALUE
        else:
            BufferBearish[i] = BufferSAR[i]
            BufferBullish[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SSSAR(_MQL5Indicator):
    name = 'SSSAR'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpStep': 0.02,  # Step
        'InpMax': 0.2,  # Maximum
    }

