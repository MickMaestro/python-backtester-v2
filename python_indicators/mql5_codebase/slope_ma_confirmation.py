"""Slope_MA_Confirmation — converted from MQL5: MQL5 Indicators/Slope_MA_Confirmation/Slope_MA_Confirmation.mq5

Slope Direction Line / Moving Average confirmation candles indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 11, 'indicator_plots': 3}, 'types': {1: 17, 2: 8, 3: 1}, 'colors': {1: [32768, 9419919, 255, 9221330, 11119017], 2: [32768, 255, 11119017], 3: [16711680]}, 'widths': {1: 1, 2: 2, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Candle', 2: 'Slope trend', 3: 'MA'}, 'levels': [], 'description': ['Slope Direction Line / Moving Average confirmation candles indicator'], 'name': 'Slope_MA_Confirmation', 'source': 'MQL5 Indicators/Slope_MA_Confirmation/Slope_MA_Confirmation.mq5', 'folder': 'Slope_MA_Confirmation', 'inputs': [{'mql': 'InpPeriodMA', 'py': 'InpPeriodMA', 'param': 'InpPeriodMA', 'type': 'uint', 'default': 50, 'label': 'MA period', 'sinput': False}, {'mql': 'InpMethodMA', 'py': 'InpMethodMA', 'param': 'InpMethodMA', 'type': 'int', 'default': 0, 'label': 'MA method', 'sinput': False}, {'mql': 'InpAppliedPriceMA', 'py': 'InpAppliedPriceMA', 'param': 'InpAppliedPriceMA', 'type': 'int', 'default': 1, 'label': 'MA applied price', 'sinput': False}, {'mql': 'InpPeriodSlope', 'py': 'InpPeriodSlope', 'param': 'InpPeriodSlope', 'type': 'uint', 'default': 50, 'label': 'SDL period', 'sinput': False}, {'mql': 'InpMethodSlope', 'py': 'InpMethodSlope', 'param': 'InpMethodSlope', 'type': 'int', 'default': 0, 'label': 'SDL method', 'sinput': False}, {'mql': 'InpAppliedPriceSlope', 'py': 'InpAppliedPriceSlope', 'param': 'InpAppliedPriceSlope', 'type': 'int', 'default': 1, 'label': 'SDL applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodMA = _input('InpPeriodMA', 50)  # MA period
InpMethodMA = _input('InpMethodMA', MODE_SMA)  # MA method
InpAppliedPriceMA = _input('InpAppliedPriceMA', PRICE_CLOSE)  # MA applied price
InpPeriodSlope = _input('InpPeriodSlope', 50)  # SDL period
InpMethodSlope = _input('InpMethodSlope', MODE_SMA)  # SDL method
InpAppliedPriceSlope = _input('InpAppliedPriceSlope', PRICE_CLOSE)  # SDL applied price
BufferCandleO = Arr(0, 0.0)
BufferCandleH = Arr(0, 0.0)
BufferCandleL = Arr(0, 0.0)
BufferCandleC = Arr(0, 0.0)
BufferCandleColors = Arr(0, 0.0)
BufferSlope = Arr(0, 0.0)
BufferSlopeColors = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMA2 = Arr(0, 0.0)
BufferVect = Arr(0, 0.0)
period_slope = 0
period_slope2 = 0
period_sqrt = 0
period_ma = 0
period_max = 0
weight_sum = 0
handle_ma = 0
handle_ma1 = 0
handle_ma2 = 0

def OnInit():
    global handle_ma, handle_ma1, handle_ma2, period_ma, period_slope, period_slope2, period_sqrt
    period_ma = (1 if (InpPeriodMA < 1) else InpPeriodMA)
    period_slope = (2 if (InpPeriodSlope < 2) else InpPeriodSlope)
    period_slope2 = _int(floor(_idiv(period_slope, 2)))
    period_sqrt = _int(floor(sqrt(period_slope)))
    SetIndexBuffer(0, BufferCandleO, INDICATOR_DATA)
    SetIndexBuffer(1, BufferCandleH, INDICATOR_DATA)
    SetIndexBuffer(2, BufferCandleL, INDICATOR_DATA)
    SetIndexBuffer(3, BufferCandleC, INDICATOR_DATA)
    SetIndexBuffer(4, BufferCandleColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, BufferSlope, INDICATOR_DATA)
    SetIndexBuffer(6, BufferSlopeColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(7, BufferMA, INDICATOR_DATA)
    SetIndexBuffer(8, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, BufferMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, BufferVect, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Slope/MA candles (' + _str(period_slope) + ',' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetString(1, PLOT_LABEL, MethodToString(InpMethodSlope) + ' SDL')
    PlotIndexSetString(2, PLOT_LABEL, MethodToString(InpMethodMA))
    ArraySetAsSeries(BufferCandleO, True)
    ArraySetAsSeries(BufferCandleH, True)
    ArraySetAsSeries(BufferCandleL, True)
    ArraySetAsSeries(BufferCandleC, True)
    ArraySetAsSeries(BufferCandleColors, True)
    ArraySetAsSeries(BufferSlope, True)
    ArraySetAsSeries(BufferSlopeColors, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMA2, True)
    ArraySetAsSeries(BufferVect, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, period_ma, 0, InpMethodMA, InpAppliedPriceMA)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma1 = iMA(None, PERIOD_CURRENT, period_slope, 0, InpMethodSlope, InpAppliedPriceSlope)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(', _str(period_slope), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_ma2 = iMA(None, PERIOD_CURRENT, period_slope2, 0, InpMethodSlope, InpAppliedPriceSlope)
    if handle_ma2 == INVALID_HANDLE:
        Print('The iMA(', _str(period_slope2), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < fmax(period_slope, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferCandleO, EMPTY_VALUE)
        ArrayInitialize(BufferCandleH, EMPTY_VALUE)
        ArrayInitialize(BufferCandleL, EMPTY_VALUE)
        ArrayInitialize(BufferCandleC, EMPTY_VALUE)
        ArrayInitialize(BufferCandleColors, 4)
        ArrayInitialize(BufferSlope, EMPTY_VALUE)
        ArrayInitialize(BufferSlopeColors, 2)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferMA2, 0)
        ArrayInitialize(BufferVect, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_ma2, 0, 0, count, BufferMA2)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferVect[i] = (2.0 * BufferMA2[i]) - BufferMA1[i]
    _sw1 = InpMethodSlope
    _k2 = 0 if _sw1 == MODE_EMA else 1 if _sw1 == MODE_SMMA else 2 if _sw1 == MODE_LWMA else 3
    try:
        if _k2 <= 0:
            if ExponentialMAOnBuffer(rates_total, prev_calculated, period_slope, period_sqrt, BufferVect, BufferSlope) == 0:
                return 0
        if _k2 <= 1:
            if SmoothedMAOnBuffer(rates_total, prev_calculated, period_slope, period_sqrt, BufferVect, BufferSlope) == 0:
                return 0
        if _k2 <= 2:
            if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_slope, period_sqrt, BufferVect, BufferSlope, _GlobRef(globals(), 'weight_sum')) == 0:
                return 0
        if _k2 <= 3:
            if SimpleMAOnBuffer(rates_total, prev_calculated, period_slope, period_sqrt, BufferVect, BufferSlope) == 0:
                return 0
    except _SwitchBreak:
        pass
    for i in range(limit, 0 - 1, -1):
        BufferCandleC[i] = EMPTY_VALUE
        BufferCandleL[i] = BufferCandleC[i]
        BufferCandleH[i] = BufferCandleL[i]
        BufferCandleO[i] = BufferCandleH[i]
        if BufferSlope[i] > BufferSlope[i + 1]:
            BufferSlopeColors[i] = 0.0
            if BufferMA[i] > BufferMA[i + 1]:
                BufferCandleO[i] = open[i]
                BufferCandleH[i] = high[i]
                BufferCandleL[i] = low[i]
                BufferCandleC[i] = close[i]
                BufferCandleColors[i] = (0 if (open[i] < close[i]) else 1 if (open[i] > close[i]) else 4)
        elif BufferSlope[i] < BufferSlope[i + 1]:
            BufferSlopeColors[i] = 1.0
            if BufferMA[i] < BufferMA[i + 1]:
                BufferCandleO[i] = open[i]
                BufferCandleH[i] = high[i]
                BufferCandleL[i] = low[i]
                BufferCandleC[i] = close[i]
                BufferCandleColors[i] = (2 if (open[i] > close[i]) else 3 if (open[i] < close[i]) else 4)
        else:
            BufferSlopeColors[i] = 3.0
            BufferCandleC[i] = EMPTY_VALUE
            BufferCandleL[i] = BufferCandleC[i]
            BufferCandleH[i] = BufferCandleL[i]
            BufferCandleO[i] = BufferCandleH[i]
            BufferCandleColors[i] = 4.0
    return rates_total

def MethodToString(method):
    return StringSubstr(EnumToString(method, 'ENUM_MA_METHOD'), 5)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SlopeMAConfirmation(_MQL5Indicator):
    name = 'Slope_MA_Confirmation'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodMA': 50,  # MA period
        'InpMethodMA': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # MA method
        'InpAppliedPriceMA': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # MA applied price
        'InpPeriodSlope': 50,  # SDL period
        'InpMethodSlope': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # SDL method
        'InpAppliedPriceSlope': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # SDL applied price
    }

