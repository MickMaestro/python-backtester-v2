"""LR_Ratio — converted from MQL5: MQL5 Indicators/LR_Ratio/LR_Ratio.mq5

Linear regression ratio
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [3937500]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'LSMAR'}, 'levels': [], 'description': ['Linear regression ratio'], 'name': 'LR_Ratio', 'source': 'MQL5 Indicators/LR_Ratio/LR_Ratio.mq5', 'folder': 'LR_Ratio', 'inputs': [{'mql': 'InpPeriod1', 'py': 'InpPeriod1', 'param': 'InpPeriod1', 'type': 'uint', 'default': 10, 'label': 'Period LSMA first', 'sinput': False}, {'mql': 'InpPeriod2', 'py': 'InpPeriod2', 'param': 'InpPeriod2', 'type': 'uint', 'default': 20, 'label': 'Period LSMA second', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod1 = _input('InpPeriod1', 10)  # Period LSMA first
InpPeriod2 = _input('InpPeriod2', 20)  # Period LSMA second
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferLRR = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferLRL1 = Arr(0, 0.0)
BufferLRL2 = Arr(0, 0.0)
period1 = 0
period2 = 0
handle_ma = 0

def OnInit():
    global handle_ma, period1, period2
    period1 = (1 if (InpPeriod1 < 1) else InpPeriod1)
    period2 = (1 if (InpPeriod2 < 1) else InpPeriod2)
    SetIndexBuffer(0, BufferLRR, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferLRL1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferLRL2, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'LSMA ratio(' + _str(period1) + ',' + _str(period2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferLRR, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferLRL1, True)
    ArraySetAsSeries(BufferLRL2, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    max_ = fmax(period1, period2)
    if rates_total < max_:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - max_ - 1
        ArrayInitialize(BufferLRR, EMPTY_VALUE)
        ArrayInitialize(BufferLRL1, EMPTY_VALUE)
        ArrayInitialize(BufferLRL2, EMPTY_VALUE)
        ArrayInitialize(BufferMA, EMPTY_VALUE)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        x_reg1 = 0.0
        y_reg1 = 0.0
        xy_reg1 = 0.0
        x2_reg1 = 0.0
        x_reg2 = 0.0
        y_reg2 = 0.0
        xy_reg2 = 0.0
        x2_reg2 = 0.0
        for j in range(0, period1):
            y_reg1 += BufferMA[i + j]
            xy_reg1 += BufferMA[i + j] * j
            x_reg1 += j
            x2_reg1 += j * j
        temp1 = (period1 * x2_reg1) - (x_reg1 * x_reg1)
        m1 = _fdiv((period1 * xy_reg1) - (x_reg1 * y_reg1), (temp1 if (temp1 != 0) else DBL_MIN))
        yint1 = _fdiv(y_reg1 + (m1 * x_reg1), period1)
        BufferLRL1[i] = yint1 - (m1 * period1)
        for j in range(0, period2):
            y_reg2 += BufferMA[i + j]
            xy_reg2 += BufferMA[i + j] * j
            x_reg2 += j
            x2_reg2 += j * j
        temp2 = (period2 * x2_reg2) - (x_reg2 * x_reg2)
        m2 = _fdiv((period2 * xy_reg2) - (x_reg2 * y_reg2), (temp2 if (temp2 != 0) else DBL_MIN))
        yint2 = _fdiv(y_reg2 + (m2 * x_reg2), period2)
        BufferLRL2[i] = yint2 - (m2 * period2)
    for i in range(limit, 0 - 1, -1):
        BufferLRR[i] = _fdiv(BufferLRL1[i], (BufferLRL2[i] if (BufferLRL2[i] > 0) else DBL_MIN))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class LRRatio(_MQL5Indicator):
    name = 'LR_Ratio'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod1': 10,  # Period LSMA first
        'InpPeriod2': 20,  # Period LSMA second
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

