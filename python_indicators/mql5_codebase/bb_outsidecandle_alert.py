"""BB_OutsideCandle_Alert — converted from MQL5: MQL5 Indicators/BB_OutsideCandle_Alert/BB_OutsideCandle_Alert.mq5

Bollinger Bands Outside Candle Alert indicator
Candle opening and closing outside the bands for buy/sell signals
Optional Inside/Out Mode for open inside and close outside
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 10, 'indicator_plots': 5}, 'types': {1: 5, 2: 5, 3: 1, 4: 1, 5: 17}, 'colors': {1: [16711680], 2: [255], 3: [1993170], 4: [2263842], 5: [7451452, 36095, 11119017]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}, 'labels': {1: 'Long Signal', 2: 'Short Signal', 3: 'Upper Band', 4: 'Lower Band', 5: 'Signal Candle'}, 'levels': [], 'description': ['Bollinger Bands Outside Candle Alert indicator', 'Candle opening and closing outside the bands for buy/sell signals', 'Optional Inside/Out Mode for open inside and close outside'], 'name': 'BB_OutsideCandle_Alert', 'source': 'MQL5 Indicators/BB_OutsideCandle_Alert/BB_OutsideCandle_Alert.mq5', 'folder': 'BB_OutsideCandle_Alert', 'inputs': [{'mql': 'InpPeriodBB', 'py': 'InpPeriodBB', 'param': 'InpPeriodBB', 'type': 'uint', 'default': 12, 'label': 'BB period', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'double', 'default': 2.2, 'label': 'BB deviation', 'sinput': False}, {'mql': 'InpModeCandle', 'py': 'InpModeCandle', 'param': 'InpModeCandle', 'type': 'int', 'default': 1, 'label': 'BB line breakdown method', 'sinput': False}, {'mql': 'InpShowBands', 'py': 'InpShowBands', 'param': 'InpShowBands', 'type': 'int', 'default': 1, 'label': 'Show bands', 'sinput': False}, {'mql': 'InpShowCandles', 'py': 'InpShowCandles', 'param': 'InpShowCandles', 'type': 'int', 'default': 1, 'label': 'Show signal candles', 'sinput': False}, {'mql': 'InpShowAlerts', 'py': 'InpShowAlerts', 'param': 'InpShowAlerts', 'type': 'int', 'default': 1, 'label': 'Use alerts', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# enum ENUM_MODE_OP_CL
MODE_CANDLE_INSIDE_OUT = 0
MODE_CANDLE_OUTSIDE = 1
_enum('ENUM_MODE_OP_CL', {0: 'MODE_CANDLE_INSIDE_OUT', 1: 'MODE_CANDLE_OUTSIDE'})

# ---- inputs and global variables
InpPeriodBB = _input('InpPeriodBB', 12)  # BB period
InpDeviation = _input('InpDeviation', 2.2)  # BB deviation
InpModeCandle = _input('InpModeCandle', MODE_CANDLE_OUTSIDE)  # BB line breakdown method
InpShowBands = _input('InpShowBands', INPUT_YES)  # Show bands
InpShowCandles = _input('InpShowCandles', INPUT_YES)  # Show signal candles
InpShowAlerts = _input('InpShowAlerts', INPUT_YES)  # Use alerts
BufferSigB = Arr(0, 0.0)
BufferSigS = Arr(0, 0.0)
BufferBandUP = Arr(0, 0.0)
BufferBandDN = Arr(0, 0.0)
BufferCandleO = Arr(0, 0.0)
BufferCandleH = Arr(0, 0.0)
BufferCandleL = Arr(0, 0.0)
BufferCandleC = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferBB = Arr(0, 0.0)
deviation = 0.0
period_bb = 0
handle_bb = 0

def OnInit():
    global deviation, handle_bb, period_bb
    period_bb = (1 if (InpPeriodBB < 1) else InpPeriodBB)
    deviation = InpDeviation
    SetIndexBuffer(0, BufferSigB, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSigS, INDICATOR_DATA)
    SetIndexBuffer(2, BufferBandUP, INDICATOR_DATA)
    SetIndexBuffer(3, BufferBandDN, INDICATOR_DATA)
    SetIndexBuffer(4, BufferCandleO, INDICATOR_DATA)
    SetIndexBuffer(5, BufferCandleH, INDICATOR_DATA)
    SetIndexBuffer(6, BufferCandleL, INDICATOR_DATA)
    SetIndexBuffer(7, BufferCandleC, INDICATOR_DATA)
    SetIndexBuffer(8, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(9, BufferBB, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 233)
    PlotIndexSetInteger(1, PLOT_ARROW, 234)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BB Outside Candle Alert+(' + _str(period_bb) + ',' + DoubleToString(deviation, 1) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(2, PLOT_DRAW_TYPE, InpShowBands)
    PlotIndexSetInteger(3, PLOT_DRAW_TYPE, InpShowBands)
    ArraySetAsSeries(BufferSigB, True)
    ArraySetAsSeries(BufferSigS, True)
    ArraySetAsSeries(BufferBandUP, True)
    ArraySetAsSeries(BufferBandDN, True)
    ArraySetAsSeries(BufferCandleO, True)
    ArraySetAsSeries(BufferCandleH, True)
    ArraySetAsSeries(BufferCandleL, True)
    ArraySetAsSeries(BufferCandleC, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferBB, True)
    ResetLastError()
    handle_bb = iBands(None, PERIOD_CURRENT, period_bb, 0, deviation, PRICE_CLOSE)
    if handle_bb == INVALID_HANDLE:
        Print('The iBands (', _str(period_bb) + ',' + _str(deviation), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_last_time
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferSigB, EMPTY_VALUE)
        ArrayInitialize(BufferSigS, EMPTY_VALUE)
        ArrayInitialize(BufferBandUP, EMPTY_VALUE)
        ArrayInitialize(BufferBandDN, EMPTY_VALUE)
        ArrayInitialize(BufferCandleO, EMPTY_VALUE)
        ArrayInitialize(BufferCandleH, EMPTY_VALUE)
        ArrayInitialize(BufferCandleL, EMPTY_VALUE)
        ArrayInitialize(BufferCandleC, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 2)
        ArrayInitialize(BufferBB, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_bb, UPPER_BAND, 0, count, BufferBandUP)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_bb, LOWER_BAND, 0, count, BufferBandDN)
    if copied != count:
        return 0
    alert = ''
    for i in range(limit, 0 - 1, -1):
        BufferCandleC[i] = EMPTY_VALUE
        BufferCandleL[i] = BufferCandleC[i]
        BufferCandleH[i] = BufferCandleL[i]
        BufferCandleO[i] = BufferCandleH[i]
        if InpModeCandle == MODE_CANDLE_INSIDE_OUT:
            if open[i + 1] < BufferBandUP[i + 1] and close[i + 1] > BufferBandUP[i + 1]:
                BufferSigS[i] = high[i]
                if InpShowCandles:
                    DrawColorCandle(i + 1, open, high, low, close)
                if (i == 0 and InpShowAlerts) and time[0] > _s_OnCalculate_last_time:
                    Alert(Symbol() + ' ' + TimeframeToString(Period()) + ': Bollinger Bands Outside Candle SHORT Signal')
                    _s_OnCalculate_last_time = TimeCurrent()
            if open[i + 1] > BufferBandDN[i + 1] and close[i + 1] < BufferBandDN[i + 1]:
                BufferSigB[i] = low[i]
                if InpShowCandles:
                    DrawColorCandle(i + 1, open, high, low, close)
                if (i == 0 and InpShowAlerts) and time[0] > _s_OnCalculate_last_time:
                    Alert(Symbol() + ' ' + TimeframeToString(Period()) + ': Bollinger Bands Outside Candle LONG Signal')
                    _s_OnCalculate_last_time = TimeCurrent()
        else:
            if open[i + 1] > close[i + 1] and close[i + 1] > BufferBandUP[i + 1]:
                BufferSigS[i] = high[i]
                if InpShowCandles:
                    DrawColorCandle(i + 1, open, high, low, close)
                if (i == 0 and InpShowAlerts) and time[0] > _s_OnCalculate_last_time:
                    Alert(Symbol() + ' ' + TimeframeToString(Period()) + ': Bollinger Bands Outside Candle SHORT Signal')
                    _s_OnCalculate_last_time = TimeCurrent()
            if open[i + 1] < close[i + 1] and close[i + 1] < BufferBandDN[i + 1]:
                BufferSigB[i] = low[i]
                if InpShowCandles:
                    DrawColorCandle(i + 1, open, high, low, close)
                if (i == 0 and InpShowAlerts) and time[0] > _s_OnCalculate_last_time:
                    Alert(Symbol() + ' ' + TimeframeToString(Period()) + ': Bollinger Bands Outside Candle LONG Signal')
                    _s_OnCalculate_last_time = TimeCurrent()
    return rates_total

def TimeframeToString(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7)

def DrawColorCandle(shift, open, high, low, close):
    BufferCandleO[shift] = open[shift]
    BufferCandleH[shift] = high[shift]
    BufferCandleL[shift] = low[shift]
    BufferCandleC[shift] = close[shift]
    BufferColors[shift] = (0 if (open[shift] < close[shift]) else 1 if (open[shift] > close[shift]) else 2)

# ---- static local variables
_s_OnCalculate_last_time = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BBOutsideCandleAlert(_MQL5Indicator):
    name = 'BB_OutsideCandle_Alert'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodBB': 12,  # BB period
        'InpDeviation': 2.2,  # BB deviation
        'InpModeCandle': _Choice({0: 'Opening inside, then closing outside', 1: 'Opening and closing outside'}, default=1),  # BB line breakdown method
        'InpShowBands': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show bands
        'InpShowCandles': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show signal candles
        'InpShowAlerts': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Use alerts
    }

