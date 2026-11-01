"""AhrensMACD — converted from MQL5: MQL5 Indicators/AhrensMACD/AhrensMACD.mq5

Ahrens Moving Average Convergence Divergence
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 3}, 'types': {1: 10, 2: 1, 3: 1}, 'colors': {1: [16760576, 36095, 11119017], 2: [255], 3: [32768]}, 'widths': {1: 2, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Ahrens Histogram', 2: 'Ahrens MACD', 3: 'Ahrens Signal'}, 'levels': [], 'description': ['Ahrens Moving Average Convergence Divergence'], 'name': 'AhrensMACD', 'source': 'MQL5 Indicators/AhrensMACD/AhrensMACD.mq5', 'folder': 'AhrensMACD', 'inputs': [{'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 12, 'label': 'Fast Ahrens MA period', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 26, 'label': 'Slow Ahrens MA period', 'sinput': False}, {'mql': 'InpPeriodSig', 'py': 'InpPeriodSig', 'param': 'InpPeriodSig', 'type': 'uint', 'default': 9, 'label': 'Signal line period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriodFast = _input('InpPeriodFast', 12)  # Fast Ahrens MA period
InpPeriodSlow = _input('InpPeriodSlow', 26)  # Slow Ahrens MA period
InpPeriodSig = _input('InpPeriodSig', 9)  # Signal line period
BufferHist = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferMACD = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
BufferFastAHRMA = Arr(0, 0.0)
BufferSlowAHRMA = Arr(0, 0.0)
BufferSignalAHRMA = Arr(0, 0.0)
period_fast = 0
period_slow = 0
period_signal = 0
period_max = 0

def OnInit():
    global period_fast, period_max, period_signal, period_slow
    period_fast = (1 if (InpPeriodFast < 1) else InpPeriodFast)
    period_slow = ((period_fast + 1) if (InpPeriodSlow == period_fast) else 1 if (InpPeriodSlow < 1) else InpPeriodSlow)
    period_signal = (1 if (InpPeriodSig < 1) else InpPeriodSig)
    period_max = fmax(period_fast, fmax(period_slow, period_signal))
    SetIndexBuffer(0, BufferHist, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferMACD, INDICATOR_DATA)
    SetIndexBuffer(3, BufferSignal, INDICATOR_DATA)
    SetIndexBuffer(4, BufferFastAHRMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferSlowAHRMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferSignalAHRMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Ahrens MACD (' + _str(period_fast) + ',' + _str(period_slow) + ',' + _str(period_signal) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferHist, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferMACD, True)
    ArraySetAsSeries(BufferSignal, True)
    ArraySetAsSeries(BufferFastAHRMA, True)
    ArraySetAsSeries(BufferSlowAHRMA, True)
    ArraySetAsSeries(BufferSignalAHRMA, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if rates_total < fmax(period_max + 1, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_max - 2
        ArrayInitialize(BufferHist, 0)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferMACD, 0)
        ArrayInitialize(BufferSignal, 0)
        ArrayInitialize(BufferFastAHRMA, 0)
        ArrayInitialize(BufferSlowAHRMA, 0)
        ArrayInitialize(BufferSignalAHRMA, 0)
    for i in range(limit, 0 - 1, -1):
        MedianPrice = (high[i] + low[i]) / 2.0
        MedianMA1 = (BufferFastAHRMA[i + 1] + BufferFastAHRMA[i + period_fast]) / 2.0
        BufferFastAHRMA[i] = BufferFastAHRMA[i + 1] + _fdiv(MedianPrice - MedianMA1, period_fast)
        MedianMA2 = (BufferSlowAHRMA[i + 1] + BufferSlowAHRMA[i + period_slow]) / 2.0
        BufferSlowAHRMA[i] = BufferSlowAHRMA[i + 1] + _fdiv(MedianPrice - MedianMA2, period_slow)
        BufferMACD[i] = BufferFastAHRMA[i] - BufferSlowAHRMA[i]
        MedianMA3 = (BufferSignal[i + 1] + BufferSignal[i + period_signal]) / 2.0
        BufferSignal[i] = BufferSignal[i + 1] + _fdiv(BufferMACD[i] - MedianMA3, period_signal)
        BufferHist[i] = BufferMACD[i] - BufferSignal[i]
        BufferColors[i] = (0 if (BufferHist[i] > BufferHist[i + 1]) else 1 if (BufferHist[i] < BufferHist[i + 1]) else 2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AhrensMACD(_MQL5Indicator):
    name = 'AhrensMACD'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFast': 12,  # Fast Ahrens MA period
        'InpPeriodSlow': 26,  # Slow Ahrens MA period
        'InpPeriodSig': 9,  # Signal line period
    }

