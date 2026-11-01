"""Super_SAR — converted from MQL5: MQL5 Indicators/Super_SAR/Super_SAR.mq5

Super SAR indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 10, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [32768], 2: [255], 3: [8421504], 4: [11119017]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Up', 2: 'Down', 3: 'Neutral', 4: 'SAR'}, 'levels': [], 'description': ['Super SAR indicator'], 'name': 'Super_SAR', 'source': 'MQL5 Indicators/Super_SAR/Super_SAR.mq5', 'folder': 'Super_SAR', 'inputs': [{'mql': 'InpStepSAR', 'py': 'InpStepSAR', 'param': 'InpStepSAR', 'type': 'double', 'default': 0.02, 'label': 'SAR step', 'sinput': False}, {'mql': 'InpMaxSAR', 'py': 'InpMaxSAR', 'param': 'InpMaxSAR', 'type': 'double', 'default': 0.2, 'label': 'SAR max', 'sinput': False}, {'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'int', 'default': 8, 'label': 'ATR Period', 'sinput': False}, {'mql': 'InpMultiplier', 'py': 'InpMultiplier', 'param': 'InpMultiplier', 'type': 'double', 'default': 1.5, 'label': 'Multiplier', 'sinput': False}, {'mql': 'InpSwing', 'py': 'InpSwing', 'param': 'InpSwing', 'type': 'int', 'default': 0, 'label': 'Swing', 'sinput': False}, {'mql': 'InpShowSAR', 'py': 'InpShowSAR', 'param': 'InpShowSAR', 'type': 'int', 'default': 1, 'label': 'Show SAR', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpStepSAR = _input('InpStepSAR', 0.02)  # SAR step
InpMaxSAR = _input('InpMaxSAR', 0.2)  # SAR max
InpPeriod = _input('InpPeriod', 8)  # ATR Period
InpMultiplier = _input('InpMultiplier', 1.5)  # Multiplier
InpSwing = _input('InpSwing', INPUT_NO)  # Swing
InpShowSAR = _input('InpShowSAR', INPUT_YES)  # Show SAR
BufferArrUP = Arr(0, 0.0)
BufferArrDN = Arr(0, 0.0)
BufferArrNL = Arr(0, 0.0)
BufferSAR = Arr(0, 0.0)
BufferATR = Arr(0, 0.0)
BufferTrUP = Arr(0, 0.0)
BufferTrDN = Arr(0, 0.0)
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferTR = Arr(0, 0.0)
step = 0.0
max_ = 0.0
multiplier = 0.0
flagSAR = False
flagST = False
period = 0
flag = 0
handle_sar = 0
handle_atr = 0

def OnInit():
    global flag, flagSAR, flagST, handle_atr, handle_sar, max_, multiplier, period, step
    period = (1 if (InpPeriod < 1) else InpPeriod)
    step = (0.0001 if (InpStepSAR < 0.0001) else InpStepSAR)
    max_ = (0.0001 if (InpMaxSAR < 0.0001) else InpMaxSAR)
    multiplier = InpMultiplier
    flag = 0
    flagST = False
    flagSAR = flagST
    SetIndexBuffer(0, BufferArrUP, INDICATOR_DATA)
    SetIndexBuffer(1, BufferArrDN, INDICATOR_DATA)
    SetIndexBuffer(2, BufferArrNL, INDICATOR_DATA)
    SetIndexBuffer(3, BufferSAR, INDICATOR_DATA)
    SetIndexBuffer(4, BufferATR, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferTrUP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferTrDN, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferUP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferDN, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferTR, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(3, PLOT_DRAW_TYPE, (DRAW_ARROW if InpShowSAR else DRAW_NONE))
    PlotIndexSetInteger(0, PLOT_ARROW, 233)
    PlotIndexSetInteger(1, PLOT_ARROW, 234)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    PlotIndexSetInteger(3, PLOT_ARROW, 158)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Super SAR (' + DoubleToString(step, 4) + ',' + DoubleToString(max_, 4) + ',' + _str(period) + ',' + DoubleToString(multiplier, 4) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferArrUP, True)
    ArraySetAsSeries(BufferArrDN, True)
    ArraySetAsSeries(BufferArrNL, True)
    ArraySetAsSeries(BufferSAR, True)
    ArraySetAsSeries(BufferATR, True)
    ArraySetAsSeries(BufferTrUP, True)
    ArraySetAsSeries(BufferTrDN, True)
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferTR, True)
    ResetLastError()
    handle_sar = iSAR(None, PERIOD_CURRENT, step, max_)
    if handle_sar == INVALID_HANDLE:
        Print('The iSAR(', DoubleToString(step, 4), ',' + DoubleToString(max_, 4), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_atr = iATR(None, PERIOD_CURRENT, period)
    if handle_atr == INVALID_HANDLE:
        Print('The iATR(', _str(period), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global flag, flagSAR, flagST
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferArrUP, EMPTY_VALUE)
        ArrayInitialize(BufferArrDN, EMPTY_VALUE)
        ArrayInitialize(BufferArrNL, EMPTY_VALUE)
        ArrayInitialize(BufferSAR, EMPTY_VALUE)
        ArrayInitialize(BufferATR, 0)
        ArrayInitialize(BufferTrUP, 0)
        ArrayInitialize(BufferTrDN, 0)
        ArrayInitialize(BufferUP, 0)
        ArrayInitialize(BufferDN, 0)
        ArrayInitialize(BufferTR, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_sar, 0, 0, count, BufferSAR)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_atr, 0, 0, count, BufferATR)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        ATR = BufferATR[i]
        Median = (high[i] + low[i]) / 2.0
        BufferUP[i] = Median + (ATR * multiplier)
        BufferDN[i] = Median - (ATR * multiplier)
        BufferTR[i] = (1 if (close[i] > BufferUP[i + 1]) else -1 if (close[i] < BufferDN[i + 1]) else BufferTR[i + 1])
        flagl = (True if (BufferTR[i] < 0 and BufferTR[i + 1] > 0) else False)
        flagh = (True if (BufferTR[i] > 0 and BufferTR[i + 1] < 0) else False)
        if BufferTR[i] > 0 and BufferDN[i] < BufferDN[i + 1]:
            BufferDN[i] = BufferDN[i + 1]
        if BufferTR[i] < 0 and BufferUP[i] > BufferUP[i + 1]:
            BufferUP[i] = BufferUP[i + 1]
        if flagl:
            BufferUP[i] = Median + (ATR * multiplier)
        if flagh:
            BufferDN[i] = Median - (ATR * multiplier)
        if BufferTR[i] == 1:
            BufferTrUP[i] = BufferDN[i]
            BufferTrDN[i] = 0.0
        else:
            BufferTrDN[i] = BufferUP[i]
            BufferTrUP[i] = 0.0
    for i in range(limit, 0 - 1, -1):
        BufferArrUP[i] = EMPTY_VALUE
        BufferArrNL[i] = BufferArrUP[i]
        BufferArrDN[i] = BufferArrNL[i]
        SAR0 = BufferSAR[i]
        SAR1 = BufferSAR[i + 1]
        if InpSwing:
            flagSAR = (True if (SAR0 < close[i] and SAR1 > close[i + 1]) else False if (SAR0 > close[i] and SAR1 < close[i + 1]) else flagSAR)
            flagST = (True if (BufferTrUP[i] > 0) else False if (BufferTrDN[i] > 0) else flagST)
            if (flagSAR and flagST) and flag != 1:
                BufferArrUP[i] = open[i]
                flag = 1
            if ((not flagSAR) and (not flagST)) and flag != -1:
                BufferArrDN[i] = open[i]
                flag = -1
        else:
            if (SAR0 < close[i] and SAR1 > close[i + 1]) and BufferTrUP[i] > 0:
                BufferArrUP[i] = open[i]
            else:
                if (SAR0 > close[i] and SAR1 < close[i + 1]) and BufferTrDN[i] > 0:
                    BufferArrDN[i] = open[i]
                else:
                    if SAR0 < close[i] and SAR1 > close[i + 1]:
                        BufferArrNL[i] = high[i]
                    else:
                        if SAR0 > close[i] and SAR1 < close[i + 1]:
                            BufferArrNL[i] = low[i]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SuperSAR(_MQL5Indicator):
    name = 'Super_SAR'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpStepSAR': 0.02,  # SAR step
        'InpMaxSAR': 0.2,  # SAR max
        'InpPeriod': 8,  # ATR Period
        'InpMultiplier': 1.5,  # Multiplier
        'InpSwing': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Swing
        'InpShowSAR': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show SAR
    }

