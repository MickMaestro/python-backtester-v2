"""Glitch_Index — converted from MQL5: MQL5 Indicators/Glitch_Index/Glitch_Index.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [3329330, 10156544, 17919, 8036607]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'GI'}, 'levels': [], 'description': [], 'name': 'Glitch_Index', 'source': 'MQL5 Indicators/Glitch_Index/Glitch_Index.mq5', 'folder': 'Glitch_Index', 'inputs': [{'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 30, 'label': 'MA Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'MA method', 'sinput': False}, {'mql': 'InpPeriodROC', 'py': 'InpPeriodROC', 'param': 'InpPeriodROC', 'type': 'uint', 'default': 1, 'label': 'ROC Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodMA = _input('InpPeriodMA', 30)  # MA Period
InpMethod = _input('InpMethod', MODE_SMA)  # MA method
InpPeriodROC = _input('InpPeriodROC', 1)  # ROC Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferGI = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMAP = Arr(0, 0.0)
period_ma = 0
period_roc = 0
handle_ma1 = 0
handle_maP = 0

def OnInit():
    global handle_ma1, handle_maP, period_ma, period_roc
    period_ma = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    period_roc = (1 if (InpPeriodROC < 1) else InpPeriodROC)
    SetIndexBuffer(0, BufferGI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMAP, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Glitch Index(' + _str(period_ma) + ',' + _str(period_roc) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferGI, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMAP, True)
    ResetLastError()
    handle_ma1 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_maP = iMA(None, PERIOD_CURRENT, period_ma, 0, InpMethod, InpAppliedPrice)
    if handle_maP == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_roc - 1
        ArrayInitialize(BufferGI, EMPTY_VALUE)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferMAP, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_maP, 0, 0, count, BufferMAP)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        Pr = BufferMA1[i]
        MA = BufferMAP[i]
        MA_ROC = BufferMAP[i + period_roc]
        rocsma = ((MA - MA_ROC) * 0.1) + 1.0
        smamult = MA * rocsma
        diff = Pr - smamult
        BufferGI[i] = _fdiv(100.0 * diff, Pr)
        BufferColors[i] = ((3 if (BufferGI[i + 1] < BufferGI[i]) else 2) if (BufferGI[i] < 0) else 0 if (BufferGI[i + 1] < BufferGI[i]) else 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class GlitchIndex(_MQL5Indicator):
    name = 'Glitch_Index'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodMA': 30,  # MA Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA method
        'InpPeriodROC': 1,  # ROC Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

