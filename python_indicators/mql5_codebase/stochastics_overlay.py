"""Stochastics_Overlay — converted from MQL5: MQL5 Indicators/Stochastics_Overlay/Stochastics_Overlay.mq5

Stochastic Overlay indicator.
Colored bars depending on Stochastic Oscillator.
    Available modes:
1) Compare Stochastic Main and Signal Lines
2) Stochastic above or below 50 Line
3) Compare Current Stochastic value with Previous Stochastic value
4) Stochastic Above Overbought or Below Oversold
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [2263842, 11193702, 255, 8894686, 13882323]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Open;High;Low;Close'}, 'levels': [], 'description': ['Stochastic Overlay indicator.', 'Colored bars depending on Stochastic Oscillator.', '    Available modes:', '1) Compare Stochastic Main and Signal Lines', '2) Stochastic above or below 50 Line', '3) Compare Current Stochastic value with Previous Stochastic value', '4) Stochastic Above Overbought or Below Oversold'], 'name': 'Stochastics_Overlay', 'source': 'MQL5 Indicators/Stochastics_Overlay/Stochastics_Overlay.mq5', 'folder': 'Stochastics_Overlay', 'inputs': [{'mql': 'InpMethodOvl', 'py': 'InpMethodOvl', 'param': 'InpMethodOvl', 'type': 'int', 'default': 1, 'label': 'Data Stochastic Compare mode', 'sinput': False}, {'mql': 'InpPeriodK', 'py': 'InpPeriodK', 'param': 'InpPeriodK', 'type': 'uint', 'default': 8, 'label': 'Stochastic %K period', 'sinput': False}, {'mql': 'InpPeriodD', 'py': 'InpPeriodD', 'param': 'InpPeriodD', 'type': 'uint', 'default': 3, 'label': 'Stochastic %D period', 'sinput': False}, {'mql': 'InpSlowing', 'py': 'InpSlowing', 'param': 'InpSlowing', 'type': 'uint', 'default': 3, 'label': 'Stochastic slowing', 'sinput': False}, {'mql': 'InpPriceField', 'py': 'InpPriceField', 'param': 'InpPriceField', 'type': 'int', 'default': 0, 'label': 'Stochastic price field', 'sinput': False}, {'mql': 'InpMethodSTO', 'py': 'InpMethodSTO', 'param': 'InpMethodSTO', 'type': 'int', 'default': 0, 'label': 'Stochastic method', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 80.0, 'label': 'Stochastic overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 20.0, 'label': 'Stochastic oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_METHOD_OVERLAY
METHOD_OVL_SIGNAL = 0
METHOD_OVL_50 = 1
METHOD_OVL_VALUES = 2
METHOD_OVL_OBOS = 3
_enum('ENUM_METHOD_OVERLAY', {0: 'METHOD_OVL_SIGNAL', 1: 'METHOD_OVL_50', 2: 'METHOD_OVL_VALUES', 3: 'METHOD_OVL_OBOS'})

# enum ENUM_CANDLE_TYPE
CANDLE_TYPE_BULLISH = 0
CANDLE_TYPE_BEARISH = 1
CANDLE_TYPE_NEUTRAL = 2
_enum('ENUM_CANDLE_TYPE', {0: 'CANDLE_TYPE_BULLISH', 1: 'CANDLE_TYPE_BEARISH', 2: 'CANDLE_TYPE_NEUTRAL'})

# ---- inputs and global variables
InpMethodOvl = _input('InpMethodOvl', METHOD_OVL_50)  # Data Stochastic Compare mode
InpPeriodK = _input('InpPeriodK', 8)  # Stochastic %K period
InpPeriodD = _input('InpPeriodD', 3)  # Stochastic %D period
InpSlowing = _input('InpSlowing', 3)  # Stochastic slowing
InpPriceField = _input('InpPriceField', STO_LOWHIGH)  # Stochastic price field
InpMethodSTO = _input('InpMethodSTO', MODE_SMA)  # Stochastic method
InpOverbought = _input('InpOverbought', 80.0)  # Stochastic overbought
InpOversold = _input('InpOversold', 20.0)  # Stochastic oversold
BufferCandleOpen = Arr(0, 0.0)
BufferCandleHigh = Arr(0, 0.0)
BufferCandleLow = Arr(0, 0.0)
BufferCandleClose = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferSTO = Arr(0, 0.0)
BufferSig = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period_k = 0
period_d = 0
slowing = 0
period_max = 0
handle_sto = 0
prev_fgnd = False

def OnInit():
    global handle_sto, overbought, oversold, period_d, period_k, period_max, prev_fgnd, slowing
    period_k = (1 if (InpPeriodK < 1) else InpPeriodK)
    period_d = (1 if (InpPeriodD < 1) else InpPeriodD)
    slowing = (1 if (InpSlowing < 1) else InpSlowing)
    period_max = fmax(slowing, fmax(period_k, period_d))
    overbought = (100 if (InpOverbought > 100) else 0.1 if (InpOverbought < 0.1) else InpOverbought)
    oversold = (0 if (InpOversold < 0) else (overbought - 0.1) if (InpOversold >= overbought) else InpOversold)
    prev_fgnd = (ChartGetInteger(0, CHART_FOREGROUND) != 0)
    ChartSetInteger(0, CHART_FOREGROUND, False)
    ChartRedraw()
    SetIndexBuffer(0, BufferCandleOpen, INDICATOR_DATA)
    SetIndexBuffer(1, BufferCandleHigh, INDICATOR_DATA)
    SetIndexBuffer(2, BufferCandleLow, INDICATOR_DATA)
    SetIndexBuffer(3, BufferCandleClose, INDICATOR_DATA)
    SetIndexBuffer(4, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, BufferSTO, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferSig, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stochastics Overlay (' + _str(period_k) + ',' + _str(period_d) + ',' + _str(slowing) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferCandleOpen, True)
    ArraySetAsSeries(BufferCandleHigh, True)
    ArraySetAsSeries(BufferCandleLow, True)
    ArraySetAsSeries(BufferCandleClose, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferSTO, True)
    ArraySetAsSeries(BufferSig, True)
    ResetLastError()
    handle_sto = iStochastic(None, PERIOD_CURRENT, period_k, period_d, slowing, InpMethodSTO, InpPriceField)
    if handle_sto == INVALID_HANDLE:
        Print('The iStochastic(', _str(period_k), ',', _str(period_d), ',', _str(slowing), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ChartSetInteger(0, CHART_FOREGROUND, prev_fgnd)
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    if rates_total < fmax(period_max, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferCandleOpen, EMPTY_VALUE)
        ArrayInitialize(BufferCandleHigh, EMPTY_VALUE)
        ArrayInitialize(BufferCandleLow, EMPTY_VALUE)
        ArrayInitialize(BufferCandleClose, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 4)
        ArrayInitialize(BufferSTO, 0)
        ArrayInitialize(BufferSig, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_sto, MAIN_LINE, 0, count, BufferSTO)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_sto, SIGNAL_LINE, 0, count, BufferSig)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferCandleOpen[i] = open[i]
        BufferCandleHigh[i] = high[i]
        BufferCandleLow[i] = low[i]
        BufferCandleClose[i] = close[i]
        type_ = CandleType(i, open, close)
        overlay = CandleTypeOverlay(i)
        BufferColors[i] = ((0 if (type_ == CANDLE_TYPE_BULLISH) else 1 if (type_ == CANDLE_TYPE_BEARISH) else 4) if (overlay == CANDLE_TYPE_BULLISH) else (2 if (type_ == CANDLE_TYPE_BEARISH) else 3 if (type_ == CANDLE_TYPE_BULLISH) else 4) if (overlay == CANDLE_TYPE_BEARISH) else 4)
    return rates_total

def CandleTypeOverlay(shift):
    return ((CANDLE_TYPE_BULLISH if (BufferSTO[shift] > BufferSig[shift]) else CANDLE_TYPE_BEARISH if (BufferSTO[shift] < BufferSig[shift]) else CANDLE_TYPE_NEUTRAL) if (InpMethodOvl == METHOD_OVL_SIGNAL) else (CANDLE_TYPE_BULLISH if (BufferSTO[shift] > BufferSTO[shift + 1]) else CANDLE_TYPE_BEARISH if (BufferSTO[shift] < BufferSTO[shift + 1]) else CANDLE_TYPE_NEUTRAL) if (InpMethodOvl == METHOD_OVL_VALUES) else (CANDLE_TYPE_BULLISH if (BufferSTO[shift] > overbought) else CANDLE_TYPE_BEARISH if (BufferSTO[shift] < oversold) else CANDLE_TYPE_NEUTRAL) if (InpMethodOvl == METHOD_OVL_OBOS) else CANDLE_TYPE_BULLISH if (BufferSTO[shift] > 50) else CANDLE_TYPE_BEARISH if (BufferSTO[shift] < 50) else CANDLE_TYPE_NEUTRAL)

def CandleType(shift, open, close):
    return (CANDLE_TYPE_BULLISH if (open[shift] < close[shift]) else CANDLE_TYPE_BEARISH if (open[shift] > close[shift]) else CANDLE_TYPE_NEUTRAL)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticsOverlay(_MQL5Indicator):
    name = 'Stochastics_Overlay'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMethodOvl': _Choice({0: "Stochastic's main and signal lines", 1: 'Stochastic vs level 50', 2: 'Current and previous stochastic values', 3: 'Stochastic vs OB/OS levels'}, default=1),  # Data Stochastic Compare mode
        'InpPeriodK': 8,  # Stochastic %K period
        'InpPeriodD': 3,  # Stochastic %D period
        'InpSlowing': 3,  # Stochastic slowing
        'InpPriceField': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stochastic price field
        'InpMethodSTO': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Stochastic method
        'InpOverbought': 80.0,  # Stochastic overbought
        'InpOversold': 20.0,  # Stochastic oversold
    }

