"""Slope_Direction_Line — converted from MQL5: MQL5 Indicators/Slope_Direction_Line/Slope_Direction_Line.mq5

Slope Direction Line indicator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [32768, 255, 11119017], 2: [4294967295]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'SDL', 2: 'Trend direction'}, 'levels': [], 'description': ['Slope Direction Line indicator'], 'name': 'Slope_Direction_Line', 'source': 'MQL5 Indicators/Slope_Direction_Line/Slope_Direction_Line.mq5', 'folder': 'Slope_Direction_Line', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 80, 'label': 'Period', 'sinput': False}, {'mql': 'InpMethod', 'py': 'InpMethod', 'param': 'InpMethod', 'type': 'int', 'default': 1, 'label': 'Method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 80)  # Period
InpMethod = _input('InpMethod', MODE_EMA)  # Method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferSDL = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferTrend = Arr(0, 0.0)
BufferMAP = Arr(0, 0.0)
BufferMAP2 = Arr(0, 0.0)
BufferRAW = Arr(0, 0.0)
period_ma = 0
period2 = 0
periodSqrt = 0
handle_maP = 0
handle_maP2 = 0
weight_sum = 0

def OnInit():
    global handle_maP, handle_maP2, period2, periodSqrt, period_ma
    period_ma = (2 if (InpPeriod < 2) else InpPeriod)
    period2 = _int(floor(period_ma / 2.0))
    periodSqrt = _int(floor(sqrt(period_ma)))
    SetIndexBuffer(0, BufferSDL, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferTrend, INDICATOR_DATA)
    SetIndexBuffer(3, BufferMAP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMAP2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferRAW, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'SDL (' + _str(period_ma) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferSDL, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferTrend, True)
    ArraySetAsSeries(BufferMAP, True)
    ArraySetAsSeries(BufferMAP2, True)
    ArraySetAsSeries(BufferRAW, True)
    ResetLastError()
    handle_maP = iMA(None, PERIOD_CURRENT, period_ma, 0, InpMethod, InpAppliedPrice)
    if handle_maP == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_maP2 = iMA(None, PERIOD_CURRENT, period2, 0, InpMethod, InpAppliedPrice)
    if handle_maP2 == INVALID_HANDLE:
        Print('The iMA(', _str(period2), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_ma, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferSDL, EMPTY_VALUE)
        ArrayInitialize(BufferTrend, 0)
        ArrayInitialize(BufferMAP, 0)
        ArrayInitialize(BufferMAP2, 0)
        ArrayInitialize(BufferRAW, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_maP, 0, 0, count, BufferMAP)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_maP2, 0, 0, count, BufferMAP2)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferRAW[i] = (2.0 * BufferMAP2[i]) - BufferMAP[i]
    _sw1 = InpMethod
    if _sw1 == MODE_EMA:
        if ExponentialMAOnBuffer(rates_total, prev_calculated, period_ma, periodSqrt, BufferRAW, BufferSDL) == 0:
            return 0
    elif _sw1 == MODE_SMMA:
        if SmoothedMAOnBuffer(rates_total, prev_calculated, period_ma, periodSqrt, BufferRAW, BufferSDL) == 0:
            return 0
    elif _sw1 == MODE_LWMA:
        if LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, period_ma, periodSqrt, BufferRAW, BufferSDL, _GlobRef(globals(), 'weight_sum')) == 0:
            return 0
    else:
        if SimpleMAOnBuffer(rates_total, prev_calculated, period_ma, periodSqrt, BufferRAW, BufferSDL) == 0:
            return 0
    for i in range(limit, 0 - 1, -1):
        BufferTrend[i] = (1 if (BufferSDL[i] > BufferSDL[i + 1]) else -1 if (BufferSDL[i] < BufferSDL[i + 1]) else BufferTrend[i + 1])
        BufferColors[i] = 2.0
        if BufferTrend[i] > 0:
            BufferColors[i] = 0.0
            if BufferTrend[i + 1] < 0:
                BufferColors[i + 1] = 0.0
        else:
            BufferColors[i] = 1.0
            if BufferTrend[i + 1] > 0:
                BufferColors[i + 1] = 1.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SlopeDirectionLine(_MQL5Indicator):
    name = 'Slope_Direction_Line'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpPeriod': 80,  # Period
        'InpMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # Method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

