"""Stochastic_ROC — converted from MQL5: MQL5 Indicators/Stochastic_ROC/Stochastic_ROC.mq5

Stochastic ROC
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [32768]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'SROC'}, 'levels': [], 'description': ['Stochastic ROC'], 'name': 'Stochastic_ROC', 'source': 'MQL5 Indicators/Stochastic_ROC/Stochastic_ROC.mq5', 'folder': 'Stochastic_ROC', 'inputs': [{'mql': 'InpPeriodK', 'py': 'InpPeriodK', 'param': 'InpPeriodK', 'type': 'uint', 'default': 8, 'label': 'Stochastic K period', 'sinput': False}, {'mql': 'InpPeriodD', 'py': 'InpPeriodD', 'param': 'InpPeriodD', 'type': 'uint', 'default': 3, 'label': 'Stochastic D period', 'sinput': False}, {'mql': 'InpSlowing', 'py': 'InpSlowing', 'param': 'InpSlowing', 'type': 'uint', 'default': 3, 'label': 'Stochastic Slowing', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Stochastic MA Method', 'sinput': False}, {'mql': 'InpPriceField', 'py': 'InpPriceField', 'param': 'InpPriceField', 'type': 'int', 'default': 0, 'label': 'Stochastic Price field', 'sinput': False}, {'mql': 'InpLineMode', 'py': 'InpLineMode', 'param': 'InpLineMode', 'type': 'int', 'default': 0, 'label': 'Stochastic line', 'sinput': False}, {'mql': 'InpPeriodROC', 'py': 'InpPeriodROC', 'param': 'InpPeriodROC', 'type': 'uint', 'default': 1, 'label': 'ROC period', 'sinput': False}, {'mql': 'InpCalcType', 'py': 'InpCalcType', 'param': 'InpCalcType', 'type': 'int', 'default': 0, 'label': 'Calculation type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_MODE_LINE
LINE_MAIN = 0
LINE_SIGNAL = 1
_enum('ENUM_MODE_LINE', {0: 'LINE_MAIN', 1: 'LINE_SIGNAL'})

# enum ENUM_CALC_TYPE
CALC_TYPE_ABS = 0
CALC_TYPE_RLTV = 1
_enum('ENUM_CALC_TYPE', {0: 'CALC_TYPE_ABS', 1: 'CALC_TYPE_RLTV'})

# ---- inputs and global variables
InpPeriodK = _input('InpPeriodK', 8)  # Stochastic K period
InpPeriodD = _input('InpPeriodD', 3)  # Stochastic D period
InpSlowing = _input('InpSlowing', 3)  # Stochastic Slowing
InpMethod = _input('InpMethod', MODE_SMA)  # Stochastic MA Method
InpPriceField = _input('InpPriceField', STO_LOWHIGH)  # Stochastic Price field
InpLineMode = _input('InpLineMode', LINE_MAIN)  # Stochastic line
InpPeriodROC = _input('InpPeriodROC', 1)  # ROC period
InpCalcType = _input('InpCalcType', CALC_TYPE_ABS)  # Calculation type
BufferSROC = Arr(0, 0.0)
BufferSTO = Arr(0, 0.0)
period_k = 0
period_d = 0
slowing = 0
period_r = 0
handle_sto = 0

def OnInit():
    global handle_sto, period_d, period_k, period_r, slowing
    period_k = (1 if (InpPeriodK < 1) else InpPeriodK)
    period_d = (1 if (InpPeriodD < 1) else InpPeriodD)
    slowing = (1 if (InpSlowing < 1) else InpSlowing)
    period_r = (1 if (InpPeriodROC < 1) else InpPeriodROC)
    SetIndexBuffer(0, BufferSROC, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSTO, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'StochasticROC(' + _str(period_k) + ',' + _str(period_d) + ',' + _str(slowing) + ',' + _str(period_r) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferSROC, True)
    ArraySetAsSeries(BufferSTO, True)
    ResetLastError()
    handle_sto = iStochastic(None, PERIOD_CURRENT, period_k, period_d, slowing, InpMethod, InpPriceField)
    if handle_sto == INVALID_HANDLE:
        Print('The iStochastic(', _str(period_k), ',', _str(period_d), ',' + _str(slowing), ',', _str(period_r), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_r - 1
        ArrayInitialize(BufferSROC, EMPTY_VALUE)
        ArrayInitialize(BufferSTO, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_sto, InpLineMode, 0, count, BufferSTO)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferSROC[i] = ((BufferSTO[i] - BufferSTO[i + period_r]) if (InpCalcType == CALC_TYPE_ABS) else (_fdiv(BufferSTO[i] - BufferSTO[i + period_r], (BufferSTO[i + period_r] if (BufferSTO[i + period_r] != 0) else 1.0)) * 100.0))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticROC(_MQL5Indicator):
    name = 'Stochastic_ROC'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodK': 8,  # Stochastic K period
        'InpPeriodD': 3,  # Stochastic D period
        'InpSlowing': 3,  # Stochastic Slowing
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Stochastic MA Method
        'InpPriceField': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stochastic Price field
        'InpLineMode': _Choice({0: 'Main', 1: 'Signal'}, default=0),  # Stochastic line
        'InpPeriodROC': 1,  # ROC period
        'InpCalcType': _Choice({0: 'Absolute', 1: 'Relative'}, default=0),  # Calculation type
    }

