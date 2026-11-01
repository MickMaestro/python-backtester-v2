"""Reverse_MACD — converted from MQL5: MQL5 Indicators/Reverse_MACD/Reverse_MACD.mq5

Reverse MACD oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [255], 2: [16711680], 3: [32768]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 2, 3: 0}, 'labels': {1: 'MACD', 2: 'Signal', 3: 'Histogram'}, 'levels': [], 'description': ['Reverse MACD oscillator'], 'name': 'Reverse_MACD', 'source': 'MQL5 Indicators/Reverse_MACD/Reverse_MACD.mq5', 'folder': 'Reverse_MACD', 'inputs': [{'mql': 'InpPeriodFastMA', 'py': 'InpPeriodFastMA', 'param': 'InpPeriodFastMA', 'type': 'uint', 'default': 12, 'label': 'MACD Fast MA period', 'sinput': False}, {'mql': 'InpPeriodSlowMA', 'py': 'InpPeriodSlowMA', 'param': 'InpPeriodSlowMA', 'type': 'uint', 'default': 26, 'label': 'MACD Slow MA period', 'sinput': False}, {'mql': 'InpPeriodSignal', 'py': 'InpPeriodSignal', 'param': 'InpPeriodSignal', 'type': 'uint', 'default': 9, 'label': 'MACD Signal line period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 1, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum ENUM_METHOD
METHOD_SMA = 0
METHOD_EMA = 1
_enum('ENUM_METHOD', {0: 'METHOD_SMA', 1: 'METHOD_EMA'})

# ---- inputs and global variables
InpPeriodFastMA = _input('InpPeriodFastMA', 12)  # MACD Fast MA period
InpPeriodSlowMA = _input('InpPeriodSlowMA', 26)  # MACD Slow MA period
InpPeriodSignal = _input('InpPeriodSignal', 9)  # MACD Signal line period
InpMethod = _input('InpMethod', METHOD_EMA)  # Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferMACD = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferHist = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferFMA = Arr(0, 0.0)
BufferSMA = Arr(0, 0.0)
BufferRawMACD = Arr(0, 0.0)
BufferRawMacdAVG = Arr(0, 0.0)
period_fma = 0
period_sma = 0
period_sig = 0
period_max = 0
handle_ma1 = 0
handle_fma = 0
handle_sma = 0
ax = 0.0
ay = 0.0
az = 0.0

def OnInit():
    global ax, ay, az, handle_fma, handle_ma1, handle_sma, period_fma, period_max, period_sig, period_sma
    period_fma = (1 if (InpPeriodFastMA < 1) else InpPeriodFastMA)
    period_sma = ((period_fma + 1) if (InpPeriodSlowMA == period_fma) else 1 if (InpPeriodSlowMA < 1) else InpPeriodSlowMA)
    period_sig = (1 if (InpPeriodSignal < 1) else InpPeriodSignal)
    period_max = fmax(period_sig, fmax(period_fma, period_sma))
    ax = _fdiv(2.0, 1.0 + period_fma)
    ay = _fdiv(2.0, 1.0 + period_sma)
    az = _fdiv(2.0, 1.0 + period_sig)
    SetIndexBuffer(0, BufferMACD, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(2, BufferHist, INDICATOR_DATA)
    SetIndexBuffer(3, BufferMA1, INDICATOR_DATA)
    SetIndexBuffer(4, BufferFMA, INDICATOR_DATA)
    SetIndexBuffer(5, BufferSMA, INDICATOR_DATA)
    SetIndexBuffer(6, BufferRawMACD, INDICATOR_DATA)
    SetIndexBuffer(7, BufferRawMacdAVG, INDICATOR_DATA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Reverse MACD (' + _str(period_fma) + ',' + _str(period_sma) + ',' + _str(period_sig) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferMACD, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferHist, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferFMA, True)
    ArraySetAsSeries(BufferSMA, True)
    ArraySetAsSeries(BufferRawMACD, True)
    ArraySetAsSeries(BufferRawMacdAVG, True)
    ResetLastError()
    handle_fma = iMA(None, PERIOD_CURRENT, period_fma, 0, InpMethod, InpAppliedPrice)
    if handle_fma == INVALID_HANDLE:
        Print('The iMA(', _str(period_fma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_sma = iMA(None, PERIOD_CURRENT, period_sma, 0, InpMethod, InpAppliedPrice)
    if handle_sma == INVALID_HANDLE:
        Print('The iMA(', _str(period_sma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    if InpMethod == METHOD_SMA:
        handle_ma1 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
        if handle_ma1 == INVALID_HANDLE:
            Print('The iMA(1) object was not created: Error ', GetLastError())
            return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < period_max:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 1
        ArrayInitialize(BufferMACD, EMPTY_VALUE)
        ArrayInitialize(BufferSignal, EMPTY_VALUE)
        ArrayInitialize(BufferHist, EMPTY_VALUE)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferFMA, 0)
        ArrayInitialize(BufferSMA, 0)
        ArrayInitialize(BufferRawMACD, 0)
        ArrayInitialize(BufferRawMacdAVG, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_fma, 0, 0, count, BufferFMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sma, 0, 0, count, BufferSMA)
    if copied != count:
        return 0
    if InpMethod == METHOD_SMA:
        copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
        if copied != count:
            return 0
    for i in range(limit, 0 - 1, -1):
        BufferRawMACD[i] = BufferFMA[i] - BufferSMA[i]
    _sw1 = InpMethod
    if _sw1 == METHOD_SMA:
        SimpleMAOnBuffer(rates_total, prev_calculated, period_max, period_sig, BufferRawMACD, BufferRawMacdAVG)
    else:
        ExponentialMAOnBuffer(rates_total, prev_calculated, period_max, period_sig, BufferRawMACD, BufferRawMacdAVG)
    for i in range(limit, 0 - 1, -1):
        signal = BufferRawMacdAVG[i]
        _sw2 = InpMethod
        if _sw2 == METHOD_SMA:
            BufferMACD[i] = _fdiv((period_fma * BufferMA1[i + period_sma - 1]) - (period_sma * BufferMA1[i + period_fma - 1]), period_fma - period_sma)
            BufferSignal[i] = _fdiv((period_fma * period_sma * (BufferFMA[i] - BufferSMA[i])) + (period_fma * BufferMA1[i + period_sma - 1]) - (period_sma * BufferMA1[i + period_fma - 1]), period_fma - period_sma)
            BufferHist[i] = _fdiv((((period_fma * period_sma * period_sig) - (period_fma * period_sma)) * BufferRawMACD[i]) - (period_fma * period_sma * period_sig * signal) - (((period_sma * period_sig) - period_sma) * BufferMA1[i + period_fma - 1]) + (((period_fma * period_sig) - period_fma) * BufferMA1[i + period_sma - 1]) + (period_fma * period_sma * BufferRawMACD[i + period_sig - 1]), (period_fma * period_sig) - (period_sma * period_sig) - period_fma + period_sma)
        else:
            BufferMACD[i] = _fdiv((ax * BufferFMA[i]) - (ay * BufferSMA[i]), ax - ay)
            BufferSignal[i] = _fdiv(((1.0 - ay) * BufferSMA[i]) - ((1.0 - ax) * BufferFMA[i]), ax - ay)
            BufferHist[i] = _fdiv(signal - ((1.0 - ax) * BufferFMA[i]) + ((1.0 - ay) * BufferSMA[i]), ax - ay)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ReverseMACD(_MQL5Indicator):
    name = 'Reverse_MACD'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFastMA': 12,  # MACD Fast MA period
        'InpPeriodSlowMA': 26,  # MACD Slow MA period
        'InpPeriodSignal': 9,  # MACD Signal line period
        'InpMethod': _Choice({0: 'Simple', 1: 'Exponential'}, default=1),  # Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

