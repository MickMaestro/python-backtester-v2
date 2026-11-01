"""Stochastic_MACD — converted from MQL5: MQL5 Indicators/Stochastic_MACD/Stochastic_MACD.mq5

Stochastic MACD
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [14772545]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'StochMACD'}, 'levels': [], 'description': ['Stochastic MACD'], 'name': 'Stochastic_MACD', 'source': 'MQL5 Indicators/Stochastic_MACD/Stochastic_MACD.mq5', 'folder': 'Stochastic_MACD', 'inputs': [{'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 12, 'label': 'MACD Fast MA', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 35, 'label': 'MACD Slow MA', 'sinput': False}, {'mql': 'InpPeriodSig', 'py': 'InpPeriodSig', 'param': 'InpPeriodSig', 'type': 'uint', 'default': 9, 'label': 'MACD Signal period', 'sinput': False}, {'mql': 'InpPeriodSTO', 'py': 'InpPeriodSTO', 'param': 'InpPeriodSTO', 'type': 'uint', 'default': 18, 'label': 'Stoch period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodFast = _input('InpPeriodFast', 12)  # MACD Fast MA
InpPeriodSlow = _input('InpPeriodSlow', 35)  # MACD Slow MA
InpPeriodSig = _input('InpPeriodSig', 9)  # MACD Signal period
InpPeriodSTO = _input('InpPeriodSTO', 18)  # Stoch period
InpMethod = _input('InpMethod', MODE_SMA)  # Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferStoMACD = Arr(0, 0.0)
BufferMAF = Arr(0, 0.0)
BufferMAS = Arr(0, 0.0)
BufferB1 = Arr(0, 0.0)
BufferB2 = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period_fma = 0
period_sma = 0
period_sig = 0
period_sto = 0
handle_fma = 0
handle_sma = 0
weight_sum = 0

def OnInit():
    global handle_fma, handle_sma, period_fma, period_sig, period_sma, period_sto
    period_fma = (1 if (InpPeriodFast < 1) else InpPeriodFast)
    period_sma = (1 if (InpPeriodSlow < 1) else InpPeriodSlow)
    period_sig = (2 if (InpPeriodSig < 2) else InpPeriodSig)
    period_sto = (1 if (InpPeriodSTO < 1) else InpPeriodSTO)
    SetIndexBuffer(0, BufferStoMACD, INDICATOR_DATA)
    SetIndexBuffer(1, BufferB1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferB2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMAF, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferMAS, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'StochMACD(' + _str(period_fma) + ',' + _str(period_sma) + ',' + _str(period_sig) + ',' + _str(period_sto) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferStoMACD, True)
    ArraySetAsSeries(BufferB1, True)
    ArraySetAsSeries(BufferB2, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferMAF, True)
    ArraySetAsSeries(BufferMAS, True)
    ResetLastError()
    handle_fma = iMA(None, PERIOD_CURRENT, period_fma, 0, InpMethod, InpAppliedPrice)
    if handle_fma == INVALID_HANDLE:
        Print('The Fast iMA(', _str(period_fma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sma = iMA(None, PERIOD_CURRENT, period_sma, 0, InpMethod, InpAppliedPrice)
    if handle_sma == INVALID_HANDLE:
        Print('The Slow iMA(', _str(period_sma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    max_ = fmax(period_fma, fmax(period_sma, period_sig))
    if rates_total < max_:
        return 0
    ArraySetAsSeries(low, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - max_ - 1
        ArrayInitialize(BufferStoMACD, EMPTY_VALUE)
        ArrayInitialize(BufferB1, 0)
        ArrayInitialize(BufferB2, 0)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferMAF, 0)
        ArrayInitialize(BufferMAS, 0)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_fma, 0, 0, count, BufferMAF)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sma, 0, 0, count, BufferMAS)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferB1[i] = BufferMAF[i] - BufferMAS[i]
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sig, BufferB1, BufferMA)
    elif _sw1 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_sig, BufferB1, BufferMA)
    elif _sw1 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_sig, BufferB1, BufferMA, _GlobRef(globals(), 'weight_sum'))
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sig, BufferB1, BufferMA)
    for i in range(limit, 0 - 1, -1):
        BufferB2[i] = BufferB1[i] - BufferMA[i]
    for i in range(limit, 0 - 1, -1):
        imin = ArrayMinimum(BufferB2, i, period_sto)
        imax = ArrayMaximum(BufferB2, i, period_sto)
        if imin == WRONG_VALUE or imax == WRONG_VALUE:
            continue
        BufferStoMACD[i] = (_fdiv(100 * (BufferB1[i] - BufferMA[i] - BufferB2[imin]), BufferB2[imax] - BufferB2[imin]) if (BufferB2[imin] != BufferB2[imax]) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticMACD(_MQL5Indicator):
    name = 'Stochastic_MACD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFast': 12,  # MACD Fast MA
        'InpPeriodSlow': 35,  # MACD Slow MA
        'InpPeriodSig': 9,  # MACD Signal period
        'InpPeriodSTO': 18,  # Stoch period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

