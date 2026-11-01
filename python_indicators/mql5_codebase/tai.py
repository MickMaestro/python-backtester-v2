"""TAI — converted from MQL5: MQL5 Indicators/TAI/TAI.mq5

Trend Analysis Index indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [6053069]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'TAI'}, 'levels': [], 'description': ['Trend Analysis Index indicator'], 'name': 'TAI', 'source': 'MQL5 Indicators/TAI/TAI.mq5', 'folder': 'TAI', 'inputs': [{'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 28, 'label': 'MA Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'MA Method', 'sinput': False}, {'mql': 'InpPeriodTAI', 'py': 'InpPeriodTAI', 'param': 'InpPeriodTAI', 'type': 'uint', 'default': 5, 'label': 'TAI Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodMA = _input('InpPeriodMA', 28)  # MA Period
InpMethod = _input('InpMethod', MODE_SMA)  # MA Method
InpPeriodTAI = _input('InpPeriodTAI', 5)  # TAI Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferTAI = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMAP = Arr(0, 0.0)
period_ma = 0
period_tai = 0
handle_ma1 = 0
handle_maP = 0

def OnInit():
    global handle_ma1, handle_maP, period_ma, period_tai
    period_ma = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    period_tai = (1 if (InpPeriodTAI < 1) else InpPeriodTAI)
    SetIndexBuffer(0, BufferTAI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferMAP, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Trend Analysis Index (' + _str(period_ma) + ',' + _str(period_tai) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    ArraySetAsSeries(BufferTAI, True)
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
    if rates_total < 4 or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferTAI, EMPTY_VALUE)
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
        bl = ArrayMinimum(BufferMAP, i, period_tai)
        bh = ArrayMaximum(BufferMAP, i, period_tai)
        if bl == WRONG_VALUE or bh == WRONG_VALUE:
            continue
        min_ = BufferMAP[bl]
        max_ = BufferMAP[bh]
        BufferTAI[i] = (_fdiv(max_ - min_, BufferMA1[i] * Point()) if (BufferMA1[i] != 0) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TAI(_MQL5Indicator):
    name = 'TAI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodMA': 28,  # MA Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA Method
        'InpPeriodTAI': 5,  # TAI Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

