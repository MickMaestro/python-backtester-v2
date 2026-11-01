"""Rahul_Mohindar_Osc — converted from MQL5: MQL5 Indicators/Rahul_Mohindar_Osc/Rahul_Mohindar_Osc.mq5

Rahul Mohindar oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 3}, 'types': {1: 10, 2: 5, 3: 5}, 'colors': {1: [32768, 9498256, 255, 13353215, 11119017], 2: [16760576], 3: [17919]}, 'widths': {1: 2, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'RMO', 2: 'Bullish signal', 3: 'Bearish signal'}, 'levels': [], 'description': ['Rahul Mohindar oscillator'], 'name': 'Rahul_Mohindar_Osc', 'source': 'MQL5 Indicators/Rahul_Mohindar_Osc/Rahul_Mohindar_Osc.mq5', 'folder': 'Rahul_Mohindar_Osc', 'inputs': [{'mql': 'InpPeriodEMA1', 'py': 'InpPeriodEMA1', 'param': 'InpPeriodEMA1', 'type': 'uint', 'default': 30, 'label': 'First EMA period', 'sinput': False}, {'mql': 'InpPeriodEMA2', 'py': 'InpPeriodEMA2', 'param': 'InpPeriodEMA2', 'type': 'uint', 'default': 30, 'label': 'Second EMA period', 'sinput': False}, {'mql': 'InpPeriodEMA3', 'py': 'InpPeriodEMA3', 'param': 'InpPeriodEMA3', 'type': 'uint', 'default': 81, 'label': 'Third EMA period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodEMA1 = _input('InpPeriodEMA1', 30)  # First EMA period
InpPeriodEMA2 = _input('InpPeriodEMA2', 30)  # Second EMA period
InpPeriodEMA3 = _input('InpPeriodEMA3', 81)  # Third EMA period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
BufferRMO = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
BufferUP = Arr(0, 0.0)
BufferDN = Arr(0, 0.0)
BufferMA = Arr(0, 0.0)
BufferSwingTrd = Arr(0, 0.0)
BufferEMA1 = Arr(0, 0.0)
BufferEMA2 = Arr(0, 0.0)
BufferEMA3 = Arr(0, 0.0)
period_1 = 0
period_2 = 0
period_3 = 0
handle_ma = 0

def OnInit():
    global handle_ma, period_1, period_2, period_3
    period_1 = (2 if (InpPeriodEMA1 < 2) else InpPeriodEMA1)
    period_2 = (2 if (InpPeriodEMA2 < 2) else InpPeriodEMA2)
    period_3 = (2 if (InpPeriodEMA3 < 2) else InpPeriodEMA3)
    SetIndexBuffer(0, BufferRMO, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BufferUP, INDICATOR_DATA)
    SetIndexBuffer(3, BufferDN, INDICATOR_DATA)
    SetIndexBuffer(4, BufferMA, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferSwingTrd, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BufferEMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, BufferEMA2, INDICATOR_CALCULATIONS)
    SetIndexBuffer(8, BufferEMA3, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Rahul Mohindar oscillator (' + _str(period_1) + ',' + _str(period_2) + ',' + _str(period_3) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    ArraySetAsSeries(BufferRMO, True)
    ArraySetAsSeries(BufferColors, True)
    ArraySetAsSeries(BufferUP, True)
    ArraySetAsSeries(BufferDN, True)
    ArraySetAsSeries(BufferMA, True)
    ArraySetAsSeries(BufferSwingTrd, True)
    ArraySetAsSeries(BufferEMA1, True)
    ArraySetAsSeries(BufferEMA2, True)
    ArraySetAsSeries(BufferEMA3, True)
    ResetLastError()
    handle_ma = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma == INVALID_HANDLE:
        Print('The iMA(', _str(period_1), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_1, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 12
        ArrayInitialize(BufferRMO, EMPTY_VALUE)
        ArrayInitialize(BufferColors, 4)
        ArrayInitialize(BufferUP, EMPTY_VALUE)
        ArrayInitialize(BufferDN, EMPTY_VALUE)
        ArrayInitialize(BufferMA, 0)
        ArrayInitialize(BufferSwingTrd, 0)
        ArrayInitialize(BufferEMA1, 0)
        ArrayInitialize(BufferEMA2, 0)
        ArrayInitialize(BufferEMA3, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma, 0, 0, count, BufferMA)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        Pr0 = BufferMA[i]
        Pr1 = BufferMA[i + 1]
        Pr2 = BufferMA[i + 2]
        Pr3 = BufferMA[i + 3]
        Pr4 = BufferMA[i + 4]
        Pr5 = BufferMA[i + 5]
        Pr6 = BufferMA[i + 6]
        Pr7 = BufferMA[i + 7]
        Pr8 = BufferMA[i + 8]
        Pr9 = BufferMA[i + 9]
        Pr10 = BufferMA[i + 10]
        MA1 = (Pr0 + Pr1) / 2.0
        MA2 = (Pr0 + (2.0 * Pr1) + Pr2) / 4.0
        MA3 = (Pr0 + (3.0 * Pr1) + (3.0 * Pr2) + Pr3) / 8.0
        MA4 = (Pr0 + (4.0 * Pr1) + (6.0 * Pr2) + (4.0 * Pr3) + Pr4) / 16.0
        MA5 = (Pr0 + (5.0 * Pr1) + (10.0 * Pr2) + (10.0 * Pr3) + (5.0 * Pr4) + Pr5) / 32.0
        MA6 = (Pr0 + (6.0 * Pr1) + (15.0 * Pr2) + (20.0 * Pr3) + (15.0 * Pr4) + (6.0 * Pr5) + Pr6) / 64.0
        MA7 = (Pr0 + (7.0 * Pr1) + (21.0 * Pr2) + (35.0 * Pr3) + (35.0 * Pr4) + (21.0 * Pr5) + (7.0 * Pr6) + Pr7) / 128.0
        MA8 = (Pr0 + (8.0 * Pr1) + (28.0 * Pr2) + (56.0 * Pr3) + (70.0 * Pr4) + (56.0 * Pr5) + (28.0 * Pr6) + (8.0 * Pr7) + Pr8) / 256.0
        MA9 = (Pr0 + (9.0 * Pr1) + (36.0 * Pr2) + (84.0 * Pr3) + (126.0 * Pr4) + (126.0 * Pr5) + (84.0 * Pr6) + (36.0 * Pr7) + (9.0 * Pr8) + Pr9) / 512.0
        MA10 = (Pr0 + (10.0 * Pr1) + (45.0 * Pr2) + (120.0 * Pr3) + (210.0 * Pr4) + (252.0 * Pr5) + (210.0 * Pr6) + (120.0 * Pr7) + (45.0 * Pr8) + (10.0 * Pr9) + Pr10) / 1024.0
        Max = fmax(Pr0, fmax(Pr1, fmax(Pr2, fmax(Pr3, fmax(Pr4, fmax(Pr5, fmax(Pr6, fmax(Pr7, fmax(Pr8, Pr9)))))))))
        Min = fmin(Pr0, fmin(Pr1, fmin(Pr2, fmin(Pr3, fmin(Pr4, fmin(Pr5, fmin(Pr6, fmin(Pr7, fmin(Pr8, Pr9)))))))))
        BufferSwingTrd[i] = (_fdiv(100.0 * (Pr0 - ((MA1 + MA2 + MA3 + MA4 + MA5 + MA6 + MA7 + MA8 + MA9 + MA10) / 10.0)), Max - Min) if (Max != Min) else 0)
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_1, BufferSwingTrd, BufferEMA1) == 0:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, period_1, period_2, BufferEMA1, BufferEMA2) == 0:
        return 0
    if ExponentialMAOnBuffer(rates_total, prev_calculated, 0, period_3, BufferSwingTrd, BufferEMA3) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        EMA2_0 = BufferEMA2[i]
        EMA2_1 = BufferEMA2[i + 1]
        BufferRMO[i] = _fdiv(BufferEMA3[i], Point())
        BufferUP[i] = (BufferRMO[i] if (BufferEMA1[i + 1] < EMA2_1 and BufferEMA1[i] > EMA2_0) else EMPTY_VALUE)
        BufferDN[i] = (BufferRMO[i] if (BufferEMA1[i + 1] > EMA2_1 and BufferEMA1[i] < EMA2_0) else EMPTY_VALUE)
        BufferColors[i] = ((0 if (BufferEMA1[i] > 0) else 1) if (BufferRMO[i] > 0) else 3 if (BufferEMA1[i] > 0) else 2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RahulMohindarOsc(_MQL5Indicator):
    name = 'Rahul_Mohindar_Osc'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodEMA1': 30,  # First EMA period
        'InpPeriodEMA2': 30,  # Second EMA period
        'InpPeriodEMA3': 81,  # Third EMA period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

