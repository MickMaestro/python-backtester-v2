"""RSI_Overlay — converted from MQL5: MQL5 Indicators/RSI_Overlay/RSI_Overlay.mq5

RSI Overlay indicator.
Colored bars depending on RSI Oscillator.
    Available modes:
1) RSI above or below 50 Line
2) Compare Current RSI value with Previous RSI value
3) RSI Above Overbought or Below Oversold
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [2263842, 11193702, 255, 8894686, 13882323]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Open;High;Low;Close'}, 'levels': [], 'description': ['RSI Overlay indicator.', 'Colored bars depending on RSI Oscillator.', '    Available modes:', '1) RSI above or below 50 Line', '2) Compare Current RSI value with Previous RSI value', '3) RSI Above Overbought or Below Oversold'], 'name': 'RSI_Overlay', 'source': 'MQL5 Indicators/RSI_Overlay/RSI_Overlay.mq5', 'folder': 'RSI_Overlay', 'inputs': [{'mql': 'InpMethodOvl', 'py': 'InpMethodOvl', 'param': 'InpMethodOvl', 'type': 'int', 'default': 0, 'label': 'Data RSI Compare mode', 'sinput': False}, {'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'RSI applied price', 'sinput': False}, {'mql': 'InpOverbought', 'py': 'InpOverbought', 'param': 'InpOverbought', 'type': 'double', 'default': 70.0, 'label': 'RSI overbought', 'sinput': False}, {'mql': 'InpOversold', 'py': 'InpOversold', 'param': 'InpOversold', 'type': 'double', 'default': 30.0, 'label': 'RSI oversold', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_METHOD_OVERLAY
METHOD_OVL_50 = 0
METHOD_OVL_OBOS = 1
METHOD_OVL_VALUES = 2
_enum('ENUM_METHOD_OVERLAY', {0: 'METHOD_OVL_50', 1: 'METHOD_OVL_OBOS', 2: 'METHOD_OVL_VALUES'})

# enum ENUM_CANDLE_TYPE
CANDLE_TYPE_BULLISH = 0
CANDLE_TYPE_BEARISH = 1
CANDLE_TYPE_NEUTRAL = 2
_enum('ENUM_CANDLE_TYPE', {0: 'CANDLE_TYPE_BULLISH', 1: 'CANDLE_TYPE_BEARISH', 2: 'CANDLE_TYPE_NEUTRAL'})

# ---- inputs and global variables
InpMethodOvl = _input('InpMethodOvl', METHOD_OVL_50)  # Data RSI Compare mode
InpPeriod = _input('InpPeriod', 14)  # RSI period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # RSI applied price
InpOverbought = _input('InpOverbought', 70.0)  # RSI overbought
InpOversold = _input('InpOversold', 30.0)  # RSI oversold
BufferCandleOpen = Arr(0, 0.0)
BufferCandleHigh = Arr(0, 0.0)
BufferCandleLow = Arr(0, 0.0)
BufferCandleClose = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferRSI = Arr(0, 0.0)
overbought = 0.0
oversold = 0.0
period = 0
handle_rsi = 0
prev_fgnd = False

def OnInit():
    global handle_rsi, overbought, oversold, period, prev_fgnd
    period = (1 if (InpPeriod < 1) else InpPeriod)
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
    SetIndexBuffer(5, BufferRSI, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSI Overlay (' + _str(period) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferCandleOpen, True)
    ArraySetAsSeries(BufferCandleHigh, True)
    ArraySetAsSeries(BufferCandleLow, True)
    ArraySetAsSeries(BufferCandleClose, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferRSI, True)
    ResetLastError()
    handle_rsi = iRSI(None, PERIOD_CURRENT, period, InpAppliedPrice)
    if handle_rsi == INVALID_HANDLE:
        Print('The iRSI(', _str(period), ') object was not created: Error ', GetLastError())
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
    if rates_total < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferCandleOpen, EMPTY_VALUE)
        ArrayInitialize(BufferCandleHigh, EMPTY_VALUE)
        ArrayInitialize(BufferCandleLow, EMPTY_VALUE)
        ArrayInitialize(BufferCandleClose, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 4)
        ArrayInitialize(BufferRSI, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_rsi, 0, 0, count, BufferRSI)
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
    return ((CANDLE_TYPE_BULLISH if (BufferRSI[shift] > overbought) else CANDLE_TYPE_BEARISH if (BufferRSI[shift] < oversold) else CANDLE_TYPE_NEUTRAL) if (InpMethodOvl == METHOD_OVL_OBOS) else (CANDLE_TYPE_BULLISH if (BufferRSI[shift] > BufferRSI[shift + 1]) else CANDLE_TYPE_BEARISH if (BufferRSI[shift] < BufferRSI[shift + 1]) else CANDLE_TYPE_NEUTRAL) if (InpMethodOvl == METHOD_OVL_VALUES) else CANDLE_TYPE_BULLISH if (BufferRSI[shift] > 50) else CANDLE_TYPE_BEARISH if (BufferRSI[shift] < 50) else CANDLE_TYPE_NEUTRAL)

def CandleType(shift, open, close):
    return (CANDLE_TYPE_BULLISH if (open[shift] < close[shift]) else CANDLE_TYPE_BEARISH if (open[shift] > close[shift]) else CANDLE_TYPE_NEUTRAL)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSIOverlay(_MQL5Indicator):
    name = 'RSI_Overlay'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpMethodOvl': _Choice({0: 'RSI vs level 50', 1: 'RSI vs OB/OS levels', 2: 'Current and previous RSI values'}, default=0),  # Data RSI Compare mode
        'InpPeriod': 14,  # RSI period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # RSI applied price
        'InpOverbought': 70.0,  # RSI overbought
        'InpOversold': 30.0,  # RSI oversold
    }

