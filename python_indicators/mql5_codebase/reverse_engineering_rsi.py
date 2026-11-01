"""Reverse_Engineering_RSI — converted from MQL5: MQL5 Indicators/Reverse_Engineering_RSI/Reverse_Engineering_RSI.mq5

Reverse Engineering RSI
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [14822282]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'RE RSI'}, 'levels': [], 'description': ['Reverse Engineering RSI'], 'name': 'Reverse_Engineering_RSI', 'source': 'MQL5 Indicators/Reverse_Engineering_RSI/Reverse_Engineering_RSI.mq5', 'folder': 'Reverse_Engineering_RSI', 'inputs': [{'mql': 'InpPeriodRSI', 'py': 'InpPeriodRSI', 'param': 'InpPeriodRSI', 'type': 'uint', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 45, 'label': 'MA period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodRSI = _input('InpPeriodRSI', 14)  # RSI period
InpPeriodMA = _input('InpPeriodMA', 45)  # MA period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferReRSI = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferRSI = Arr(0, 0.0)
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferAvgRSI = Arr(0, 0.0)
BufferAvgUP = Arr(0, 0.0)
BufferAvgDN = Arr(0, 0.0)
period_rsi = 0
period_ma = 0
period_exp = 0
weight_sum = 0
handle_ma = 0
handle_rsi = 0

def OnInit():
    global handle_ma, handle_rsi, period_exp, period_ma, period_rsi
    period_ma = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    period_rsi = (1 if (InpPeriodRSI < 1) else InpPeriodRSI)
    period_exp = (2 * period_rsi) - 1
    SetIndexBuffer(0, BufferReRSI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferRSI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferUP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferDN, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferAvgRSI, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferAvgUP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferAvgDN, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ReEngineering RSI (' + _str(period_rsi) + ',' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferReRSI, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferRSI, True)
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferAvgRSI, True)
    ArraySetAsSeries(BufferAvgUP, True)
    ArraySetAsSeries(BufferAvgDN, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_rsi = iRSI(None, PERIOD_CURRENT, period_rsi, InpAppliedPrice)
    if handle_rsi == INVALID_HANDLE:
        Print('The iRSI(', _str(period_rsi), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferReRSI, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferRSI, 0)
        ArrayInitialize(BufferUP, 0)
        ArrayInitialize(BufferDN, 0)
        ArrayInitialize(BufferAvgRSI, 0)
        ArrayInitialize(BufferAvgUP, 0)
        ArrayInitialize(BufferAvgDN, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_rsi, 0, 0, count, BufferRSI)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        if BufferMA[i] > BufferMA[i + 1]:
            BufferUP[i] = BufferMA[i] - BufferMA[i + 1]
            BufferDN[i] = 0.0
        else:
            BufferUP[i] = 0.0
            BufferDN[i] = BufferMA[i + 1] - BufferMA[i]
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_exp, BufferUP, BufferAvgUP)
    ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_exp, BufferDN, BufferAvgDN)
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, period_exp, period_ma, BufferRSI, BufferAvgRSI)
    elif _sw1 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, period_exp, period_ma, BufferRSI, BufferAvgRSI)
    elif _sw1 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_exp, period_ma, BufferRSI, BufferAvgRSI, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, period_rsi, period_ma, BufferRSI, BufferAvgRSI)
    for i in range(limit, 0 - 1, -1):
        AUC_MA = BufferAvgUP[i]
        ADC_MA = BufferAvgDN[i]
        RSI_MA = BufferAvgRSI[i]
        x = (((period_rsi - 1.0) * (_fdiv(ADC_MA * RSI_MA, 100.0 - RSI_MA) - AUC_MA)) if (RSI_MA != 100) else 0)
        BufferReRSI[i] = ((BufferMA[i] + x) if (x >= 0 or RSI_MA == 0) else (BufferMA[i] + _fdiv(x * (100.0 - RSI_MA), RSI_MA)))
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ReverseEngineeringRSI(_MQL5Indicator):
    name = 'Reverse_Engineering_RSI'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodRSI': 14,  # RSI period
        'InpPeriodMA': 45,  # MA period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

