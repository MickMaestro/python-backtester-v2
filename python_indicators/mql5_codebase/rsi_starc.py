"""RSI_STARC — converted from MQL5: MQL5 Indicators/RSI_STARC/RSI_STARC.mq5

RSI + STARC indicators
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [16711680], 2: [11119017], 3: [255], 4: [32768]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'RSI', 2: 'MA', 3: 'Top', 4: 'Bottom'}, 'levels': [], 'description': ['RSI + STARC indicators'], 'name': 'RSI_STARC', 'source': 'MQL5 Indicators/RSI_STARC/RSI_STARC.mq5', 'folder': 'RSI_STARC', 'inputs': [{'mql': 'InpPeriodRSI', 'py': 'InpPeriodRSI', 'param': 'InpPeriodRSI', 'type': 'uint', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'InpPeriodATR', 'py': 'InpPeriodATR', 'param': 'InpPeriodATR', 'type': 'uint', 'default': 10, 'label': 'ATR period', 'sinput': False}, {'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 14, 'label': 'Smoothing', 'sinput': False}, {'mql': 'InpMultiplierT', 'py': 'InpMultiplierT', 'param': 'InpMultiplierT', 'type': 'double', 'default': 2.0, 'label': 'Top line multiplier', 'sinput': False}, {'mql': 'InpMultiplierB', 'py': 'InpMultiplierB', 'param': 'InpMultiplierB', 'type': 'double', 'default': 2.0, 'label': 'Bottom line multiplier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodRSI = _input('InpPeriodRSI', 14)  # RSI period
InpPeriodATR = _input('InpPeriodATR', 10)  # ATR period
InpPeriodMA = _input('InpPeriodMA', 14)  # Smoothing
InpMultiplierT = _input('InpMultiplierT', 2.0)  # Top line multiplier
InpMultiplierB = _input('InpMultiplierB', 2.0)  # Bottom line multiplier
BufferRSI = Arr(0, 0.0)
BufferCenter = Arr(0, 0.0)
BufferTop = Arr(0, 0.0)
BufferBottom = Arr(0, 0.0)
BufferTR = Arr(0, 0.0)
period_rsi = 0
period_atr = 0
smoothing = 0
handle_rsi = 0
handle_maP = 0

def OnInit():
    global handle_rsi, period_atr, period_rsi, smoothing
    period_rsi = (2 if (InpPeriodRSI < 2) else InpPeriodRSI)
    period_atr = (1 if (InpPeriodATR < 1) else InpPeriodATR)
    smoothing = (2 if (InpPeriodMA < 2) else InpPeriodMA)
    SetIndexBuffer(0, BufferRSI, INDICATOR_DATA)
    SetIndexBuffer(1, BufferCenter, INDICATOR_DATA)
    SetIndexBuffer(2, BufferTop, INDICATOR_DATA)
    SetIndexBuffer(3, BufferBottom, INDICATOR_DATA)
    SetIndexBuffer(4, BufferTR, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSI STARC (' + _str(period_rsi) + ',' + _str(period_atr) + ',' + _str(smoothing) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferRSI, True)
    ArraySetAsSeries(BufferCenter, True)
    ArraySetAsSeries(BufferTop, True)
    ArraySetAsSeries(BufferBottom, True)
    ArraySetAsSeries(BufferTR, True)
    ResetLastError()
    handle_rsi = iRSI(None, PERIOD_CURRENT, period_rsi, PRICE_CLOSE)
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
        ArrayInitialize(BufferRSI, EMPTY_VALUE)
        ArrayInitialize(BufferCenter, EMPTY_VALUE)
        ArrayInitialize(BufferTop, EMPTY_VALUE)
        ArrayInitialize(BufferBottom, EMPTY_VALUE)
        ArrayInitialize(BufferTR, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_rsi, 0, 0, count, BufferRSI)
    if copied != count:
        return 0
    SimpleMAOnBuffer(rates_total, prev_calculated, period_rsi, smoothing, BufferRSI, BufferCenter)
    for i in range(limit, 0 - 1, -1):
        BufferTR[i] = fabs(BufferRSI[i] - BufferRSI[i + 1])
    for i in range(limit, 0 - 1, -1):
        atr = SMAOnArray(BufferTR, 0, period_atr, 0, i)
        BufferTop[i] = BufferCenter[i] + (InpMultiplierT * atr)
        BufferBottom[i] = BufferCenter[i] - (InpMultiplierB * atr)
    return rates_total

def SMAOnArray(array, total, period, ma_shift, shift):
    buf = Arr(0, 0.0)
    arr = Arr(0, 0.0)
    if total == 0:
        total = ArraySize(array)
    if total > 0 and total <= period:
        return 0.0
    if shift > (total - period - ma_shift):
        return 0.0
    total = ArrayCopy(arr, array, 0, shift + ma_shift, period)
    if ArrayResize(buf, total) < 0:
        return 0.0
    sum_ = 0.0
    i = 0
    pos = total - 1
    i = 1
    while i < period:
        sum_ += arr[pos]
        i += 1
        pos -= 1
    while pos >= 0:
        sum_ += arr[pos]
        buf[pos] = _fdiv(sum_, period)
        sum_ -= arr[pos + period - 1]
        pos -= 1
    return buf[0]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSISTARC(_MQL5Indicator):
    name = 'RSI_STARC'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodRSI': 14,  # RSI period
        'InpPeriodATR': 10,  # ATR period
        'InpPeriodMA': 14,  # Smoothing
        'InpMultiplierT': 2.0,  # Top line multiplier
        'InpMultiplierB': 2.0,  # Bottom line multiplier
    }

