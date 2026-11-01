"""VAMA_MACD — converted from MQL5: MQL5 Indicators/VAMA_MACD/VAMA_MACD.mq5

MACD oscillator by Volume Adjusted Moving Average
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 10}, 'colors': {1: [255], 2: [16711680], 3: [32768, 65280, 255, 42495, 11119017]}, 'widths': {1: 1, 2: 1, 3: 2}, 'styles': {1: 0, 2: 2, 3: 0}, 'labels': {1: 'MACD', 2: 'Signal', 3: 'Histogram'}, 'levels': [], 'description': ['MACD oscillator by Volume Adjusted Moving Average'], 'name': 'VAMA_MACD', 'source': 'MQL5 Indicators/VAMA_MACD/VAMA_MACD.mq5', 'folder': 'VAMA_MACD', 'inputs': [{'mql': 'InpPeriodFastMA', 'py': 'InpPeriodFastMA', 'param': 'InpPeriodFastMA', 'type': 'uint', 'default': 12, 'label': 'Fast MA period', 'sinput': False}, {'mql': 'InpPeriodSlowMA', 'py': 'InpPeriodSlowMA', 'param': 'InpPeriodSlowMA', 'type': 'uint', 'default': 26, 'label': 'Slow MA period', 'sinput': False}, {'mql': 'InpPeriodSignal', 'py': 'InpPeriodSignal', 'param': 'InpPeriodSignal', 'type': 'uint', 'default': 9, 'label': 'Signal line period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodFastMA = _input('InpPeriodFastMA', 12)  # Fast MA period
InpPeriodSlowMA = _input('InpPeriodSlowMA', 26)  # Slow MA period
InpPeriodSignal = _input('InpPeriodSignal', 9)  # Signal line period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferMACD = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferHistogram = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
period_fma = 0
period_sma = 0
period_sig = 0
period_max = 0
handle_ma = 0

def OnInit():
    global handle_ma, period_fma, period_max, period_sig, period_sma
    period_fma = (1 if (InpPeriodFastMA < 1) else InpPeriodFastMA)
    period_sma = ((period_fma + 1) if (InpPeriodSlowMA == period_fma) else 1 if (InpPeriodSlowMA < 1) else InpPeriodSlowMA)
    period_sig = (1 if (InpPeriodSignal < 1) else InpPeriodSignal)
    period_max = fmax(period_sig, fmax(period_fma, period_sma))
    SetIndexBuffer(0, BufferMACD, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(2, BufferHistogram, INDICATOR_DATA)
    SetIndexBuffer(3, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, BufferMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'VAMA MACD (' + _str(period_fma) + ',' + _str(period_sma) + ',' + _str(period_sig) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(BufferMACD, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferHistogram, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferMA, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(1) object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(tick_volume, True)
    if rates_total < period_max:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 2
        ArrayInitialize(BufferMACD, 0)
        ArrayInitialize(BufferSignal, 0)
        ArrayInitialize(BufferHistogram, 0)
        ArrayInitialize(BufferMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        S_PV_Short = SumPrVolume(i, period_fma, tick_volume)
        S_PV_Long = SumPrVolume(i, period_sma, tick_volume)
        S_V_Short = SumVolume(i, period_fma, tick_volume)
        S_V_Long = SumVolume(i, period_sma, tick_volume)
        if S_V_Long != 0.0 and S_V_Short != 0.0:
            MAS = _fdiv(S_PV_Short, S_V_Short)
            MAL = _fdiv(S_PV_Long, S_V_Long)
            BufferMACD[i] = MAS - MAL
    for i in range(limit, 0 - 1, -1):
        S_MACD = SumMACDVolume(i, period_sig, tick_volume)
        S_V = SumVolume(i, period_sig, tick_volume)
        if S_V != 0:
            BufferSignal[i] = _fdiv(S_MACD, S_V)
            BufferHistogram[i] = BufferMACD[i] - BufferSignal[i]
            BufferColors[i] = ((0 if (BufferHistogram[i] > BufferHistogram[i + 1]) else 1) if (BufferHistogram[i] > 0) else (2 if (BufferHistogram[i] < BufferHistogram[i + 1]) else 3) if (BufferHistogram[i] < 0) else 4)
    return rates_total

def SumPrVolume(index, period, volume):
    sum_ = 0.0
    for i in range(index, index + period - 1 + 1):
        sum_ += BufferMA[i] * volume[i]
    return sum_

def SumMACDVolume(index, period, volume):
    sum_ = 0.0
    for i in range(index, index + period - 1 + 1):
        sum_ += BufferMACD[i] * volume[i]
    return sum_

def SumVolume(index, period, volume):
    sum_ = 0.0
    for i in range(index, index + period - 1 + 1):
        sum_ += float(volume[i])
    return sum_


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VAMAMACD(_MQL5Indicator):
    name = 'VAMA_MACD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFastMA': 12,  # Fast MA period
        'InpPeriodSlowMA': 26,  # Slow MA period
        'InpPeriodSignal': 9,  # Signal line period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

