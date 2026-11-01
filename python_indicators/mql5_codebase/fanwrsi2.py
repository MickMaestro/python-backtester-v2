"""FanWRSI2 — converted from MQL5: MQL5 Indicators/FanWRSI2/FanWRSI2.mq5

Fan J.Welles Wilder's RSI with Average line indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 10, 2: 1}, 'colors': {1: [32768, 255, 11119017], 2: [16748574]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'FanWRSI Hist', 2: 'FanWRSI Avg'}, 'levels': [], 'description': ["Fan J.Welles Wilder's RSI with Average line indicator"], 'name': 'FanWRSI2', 'source': 'MQL5 Indicators/FanWRSI2/FanWRSI2.mq5', 'folder': 'FanWRSI2', 'inputs': [{'mql': 'InpPeriodFirst', 'py': 'InpPeriodFirst', 'param': 'InpPeriodFirst', 'type': 'uint', 'default': 5, 'label': 'First RSI period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 6, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpCountRSI', 'py': 'InpCountRSI', 'param': 'InpCountRSI', 'type': 'uint', 'default': 10, 'label': 'RSI count', 'sinput': False}, {'mql': 'InpModeInc', 'py': 'InpModeInc', 'param': 'InpModeInc', 'type': 'int', 'default': 0, 'label': 'Incremental method', 'sinput': False}, {'mql': 'InpCoeff', 'py': 'InpCoeff', 'param': 'InpCoeff', 'type': 'uint', 'default': 2, 'label': 'Coefficient of increment', 'sinput': False}, {'mql': 'InpPeriodAvg', 'py': 'InpPeriodAvg', 'param': 'InpPeriodAvg', 'type': 'uint', 'default': 10, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'InpMethodAvg', 'py': 'InpMethodAvg', 'param': 'InpMethodAvg', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_MODE_INC
MODE_ADD = 0
MODE_MLT = 1
_enum('ENUM_MODE_INC', {0: 'MODE_ADD', 1: 'MODE_MLT'})

# ---- inputs and global variables
InpPeriodFirst = _input('InpPeriodFirst', 5)  # First RSI period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_TYPICAL)  # Applied price
InpCountRSI = _input('InpCountRSI', 10)  # RSI count
InpModeInc = _input('InpModeInc', MODE_ADD)  # Incremental method
InpCoeff = _input('InpCoeff', 2)  # Coefficient of increment
InpPeriodAvg = _input('InpPeriodAvg', 10)  # Smoothing period
InpMethodAvg = _input('InpMethodAvg', MODE_SMA)  # Smoothing method
BufferHist = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferAvg = Arr(0, 0.0)
BufferPrice = Arr(0, 0.0)
period_first = 0
period_sm = 0
cnt = 0
coeff = 0
handle_ma = 0
weight_sum = 0

def OnInit():
    global cnt, coeff, handle_ma, period_first, period_sm
    period_first = (1 if (InpPeriodFirst < 1) else InpPeriodFirst)
    period_sm = (2 if (InpPeriodAvg < 2) else InpPeriodAvg)
    cnt = (1 if (_int(InpCountRSI) < 1) else InpCountRSI)
    k = (1 if (InpModeInc == MODE_ADD) else 2)
    coeff = (k if (InpCoeff < k) else InpCoeff)
    SetIndexBuffer(0, BufferHist, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferAvg, INDICATOR_DATA)
    SetIndexBuffer(3, BufferPrice, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'FanWRSI (Periods from ' + _str(period_first) + ', step ' + _str(coeff) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    ArraySetAsSeries(BufferHist, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferAvg, True)
    ArraySetAsSeries(BufferPrice, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferHist, 0)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferAvg, 0)
        ArrayInitialize(BufferPrice, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferPrice)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        s = 0.0
        length = period_first
        j = 0
        while j < cnt:
            rsi0 = GetRSI(rates_total, length, i, BufferPrice)
            rsi1 = GetRSI(rates_total, length, i + 1, BufferPrice)
            if rsi0 == 0 or rsi1 == 0:
                j += 1
                continue
            s += (1 if (rsi0 > rsi1) else -1)
            if InpModeInc == MODE_ADD:
                length += coeff
            else:
                length *= coeff
            j += 1
        BufferHist[i] = _fdiv(s, cnt)
        BufferColors[i] = (0 if (s > 0) else 1 if (s < 0) else 2)
    _sw1 = InpMethodAvg
    if _sw1 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferHist, BufferAvg) == 0:
            return 0
    elif _sw1 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferHist, BufferAvg) == 0:
            return 0
    elif _sw1 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, 0, period_sm, BufferHist, BufferAvg, _GlobRef(globals(), 'weight_sum')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, 0, period_sm, BufferHist, BufferAvg) == 0:
            return 0
    return rates_total

def GetRSI(rates_total, period, index, price):
    if period < 1 or index > (rates_total - period - 1):
        return 0.0
    pos = 0.0
    neg = 0.0
    for j in range(0, period):
        diff = price[index + j] - price[index + j + 1]
        if diff > 0:
            pos += diff
        elif diff < 0:
            neg += -diff
    pos = _fdiv(pos, period)
    neg = _fdiv(neg, period)
    return ((100.0 - _fdiv(100.0, 1 + _fdiv(pos, neg))) if (neg != 0) else 100.0 if (pos != 0) else 50.0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FanWRSI2(_MQL5Indicator):
    name = 'FanWRSI2'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFirst': 5,  # First RSI period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),  # Applied price
        'InpCountRSI': 10,  # RSI count
        'InpModeInc': _Choice({0: 'Addition', 1: 'Multiplication'}, default=0),  # Incremental method
        'InpCoeff': 2,  # Coefficient of increment
        'InpPeriodAvg': 10,  # Smoothing period
        'InpMethodAvg': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Smoothing method
    }

