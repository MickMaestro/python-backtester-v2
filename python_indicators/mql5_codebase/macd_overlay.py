"""MACD_Overlay — converted from MQL5: MQL5 Indicators/MACD_Overlay/MACD_Overlay.mq5

MACD Overlay indicator.
Colored bars depending on MACD Oscillator.
    Available modes:
1) Compare MACD and Signal Lines
2) MACD above or below Zero Line
3) Compare Current MACD value with Previous MACD value
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [2263842, 11193702, 255, 8894686, 11119017]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Open;High;Low;Close'}, 'levels': [], 'description': ['MACD Overlay indicator.', 'Colored bars depending on MACD Oscillator.', '    Available modes:', '1) Compare MACD and Signal Lines', '2) MACD above or below Zero Line', '3) Compare Current MACD value with Previous MACD value'], 'name': 'MACD_Overlay', 'source': 'MQL5 Indicators/MACD_Overlay/MACD_Overlay.mq5', 'folder': 'MACD_Overlay', 'inputs': [{'mql': 'InpMethodOvl', 'py': 'InpMethodOvl', 'param': 'InpMethodOvl', 'type': 'int', 'default': 0, 'label': 'Data MACD Compare mode', 'sinput': False}, {'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 12, 'label': 'MACD fast EMA period', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 26, 'label': 'MACD slow EMA period', 'sinput': False}, {'mql': 'InpPeriodSignal', 'py': 'InpPeriodSignal', 'param': 'InpPeriodSignal', 'type': 'uint', 'default': 9, 'label': 'MACD period signal line', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'MACD applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_METHOD_OVERLAY
METHOD_OVL_SIGNAL = 0
METHOD_OVL_ZERO = 1
METHOD_OVL_VALUES = 2
_enum('ENUM_METHOD_OVERLAY', {0: 'METHOD_OVL_SIGNAL', 1: 'METHOD_OVL_ZERO', 2: 'METHOD_OVL_VALUES'})

# enum ENUM_CANDLE_TYPE
CANDLE_TYPE_BULLISH = 0
CANDLE_TYPE_BEARISH = 1
CANDLE_TYPE_NEUTRAL = 2
_enum('ENUM_CANDLE_TYPE', {0: 'CANDLE_TYPE_BULLISH', 1: 'CANDLE_TYPE_BEARISH', 2: 'CANDLE_TYPE_NEUTRAL'})

# ---- inputs and global variables
InpMethodOvl = _input('InpMethodOvl', METHOD_OVL_SIGNAL)  # Data MACD Compare mode
InpPeriodFast = _input('InpPeriodFast', 12)  # MACD fast EMA period
InpPeriodSlow = _input('InpPeriodSlow', 26)  # MACD slow EMA period
InpPeriodSignal = _input('InpPeriodSignal', 9)  # MACD period signal line
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # MACD applied price
BufferCandleOpen = Arr(0, 0.0)
BufferCandleHigh = Arr(0, 0.0)
BufferCandleLow = Arr(0, 0.0)
BufferCandleClose = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferMACD = Arr(0, 0.0)
BufferSignal = Arr(0, 0.0)
period_fast = 0
period_slow = 0
period_signal = 0
period_max = 0
handle_macd = 0
prev_fgnd = False

def OnInit():
    global handle_macd, period_fast, period_max, period_signal, period_slow, prev_fgnd
    period_fast = (1 if (InpPeriodFast < 1) else InpPeriodFast)
    period_slow = ((period_fast + 1) if (InpPeriodSlow == period_fast) else 1 if (InpPeriodSlow < 1) else InpPeriodSlow)
    period_signal = (1 if (InpPeriodSignal < 1) else InpPeriodSignal)
    period_max = fmax(period_signal, fmax(period_fast, period_slow))
    prev_fgnd = (ChartGetInteger(0, CHART_FOREGROUND) != 0)
    ChartSetInteger(0, CHART_FOREGROUND, False)
    ChartRedraw()
    SetIndexBuffer(0, BufferCandleOpen, INDICATOR_DATA)
    SetIndexBuffer(1, BufferCandleHigh, INDICATOR_DATA)
    SetIndexBuffer(2, BufferCandleLow, INDICATOR_DATA)
    SetIndexBuffer(3, BufferCandleClose, INDICATOR_DATA)
    SetIndexBuffer(4, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, BufferMACD, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferSignal, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MACD Overlay (' + _str(period_fast) + ',' + _str(period_slow) + ',' + _str(period_signal) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferCandleOpen, True)
    ArraySetAsSeries(BufferCandleHigh, True)
    ArraySetAsSeries(BufferCandleLow, True)
    ArraySetAsSeries(BufferCandleClose, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferMACD, True)
    ArraySetAsSeries(BufferSignal, True)
    ResetLastError()
    handle_macd = iMACD(None, PERIOD_CURRENT, period_fast, period_slow, period_signal, InpAppliedPrice)
    if handle_macd == INVALID_HANDLE:
        Print('The iMACD(', _str(period_fast), ',', _str(period_slow), ',', _str(period_signal), ') object was not created: Error ', GetLastError())
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
        ArrayInitialize(BufferMACD, 0)
        ArrayInitialize(BufferSignal, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_macd, MAIN_LINE, 0, count, BufferMACD)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_macd, SIGNAL_LINE, 0, count, BufferSignal)
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
    return ((CANDLE_TYPE_BULLISH if (BufferMACD[shift] > BufferSignal[shift]) else CANDLE_TYPE_BEARISH if (BufferMACD[shift] < BufferSignal[shift]) else CANDLE_TYPE_NEUTRAL) if (InpMethodOvl == METHOD_OVL_SIGNAL) else (CANDLE_TYPE_BULLISH if (BufferMACD[shift] > BufferMACD[shift + 1]) else CANDLE_TYPE_BEARISH if (BufferMACD[shift] < BufferMACD[shift + 1]) else CANDLE_TYPE_NEUTRAL) if (InpMethodOvl == METHOD_OVL_VALUES) else CANDLE_TYPE_BULLISH if (BufferMACD[shift] > 0) else CANDLE_TYPE_BEARISH if (BufferMACD[shift] < 0) else CANDLE_TYPE_NEUTRAL)

def CandleType(shift, open, close):
    return (CANDLE_TYPE_BULLISH if (open[shift] < close[shift]) else CANDLE_TYPE_BEARISH if (open[shift] > close[shift]) else CANDLE_TYPE_NEUTRAL)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MACDOverlay(_MQL5Indicator):
    name = 'MACD_Overlay'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMethodOvl': _Choice({0: 'MACD and signal Lines', 1: 'MACD vs zero line', 2: 'Current and previous MACD values'}, default=0),  # Data MACD Compare mode
        'InpPeriodFast': 12,  # MACD fast EMA period
        'InpPeriodSlow': 26,  # MACD slow EMA period
        'InpPeriodSignal': 9,  # MACD period signal line
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MACD applied price
    }

