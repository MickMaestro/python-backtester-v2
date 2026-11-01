"""Breakdown_Oscillator — converted from MQL5: MQL5 Indicators/Breakdown_Oscillator/Breakdown_Oscillator.mq5

Breakdown oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [10526303]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Breakdown'}, 'levels': [], 'description': ['Breakdown oscillator'], 'name': 'Breakdown_Oscillator', 'source': 'MQL5 Indicators/Breakdown_Oscillator/Breakdown_Oscillator.mq5', 'folder': 'Breakdown_Oscillator', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 10, 'label': 'Period', 'sinput': False}, {'mql': 'InpPeriodBand', 'py': 'InpPeriodBand', 'param': 'InpPeriodBand', 'type': 'uint', 'default': 20, 'label': 'Band period', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'double', 'default': 1.5, 'label': 'Deviation', 'sinput': False}, {'mql': 'InpSlopeFactor', 'py': 'InpSlopeFactor', 'param': 'InpSlopeFactor', 'type': 'double', 'default': 2.0, 'label': 'Slope factor', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpLevel', 'py': 'InpLevel', 'param': 'InpLevel', 'type': 'double', 'default': 2.0, 'label': 'Upper level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 10)  # Period
InpPeriodBand = _input('InpPeriodBand', 20)  # Band period
InpDeviation = _input('InpDeviation', 1.5)  # Deviation
InpSlopeFactor = _input('InpSlopeFactor', 2.0)  # Slope factor
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpLevel = _input('InpLevel', 2.0)  # Upper level
BufferBD = Arr(0, 0.0)
BufferDiff = Arr(0, 0.0)
BufferMA1 = Arr(0, 0.0)
BufferMAP = Arr(0, 0.0)
BufferDev = Arr(0, 0.0)
BufferEMA = Arr(0, 0.0)
deviation = 0.0
slope = 0.0
level = 0.0
period_ma = 0
period_dev = 0
handle_ma1 = 0
handle_maP = 0
handle_dev = 0

def OnInit():
    global deviation, handle_dev, handle_ma1, handle_maP, level, period_dev, period_ma, slope
    period_ma = (2 if (InpPeriod < 2) else InpPeriod)
    period_dev = (1 if (InpPeriodBand < 1) else InpPeriodBand)
    deviation = InpDeviation
    slope = InpSlopeFactor
    level = (0 if (InpLevel < 0) else InpLevel)
    SetIndexBuffer(0, BufferBD, INDICATOR_DATA)
    SetIndexBuffer(1, BufferDiff, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, BufferMA1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufferMAP, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferDev, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferEMA, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Breakdown (' + _str(period_ma) + ',' + _str(period_dev) + ',' + DoubleToString(deviation, 2) + DoubleToString(slope, 2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, level)
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(BufferBD, True)
    ArraySetAsSeries(BufferDiff, True)
    ArraySetAsSeries(BufferMA1, True)
    ArraySetAsSeries(BufferMAP, True)
    ArraySetAsSeries(BufferDev, True)
    ArraySetAsSeries(BufferEMA, True)
    ResetLastError()
    handle_ma1 = iMA(None, PERIOD_CURRENT, 1, 0, MODE_SMA, InpAppliedPrice)
    if handle_ma1 == INVALID_HANDLE:
        Print('The iMA(1) by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_maP = iMA(None, PERIOD_CURRENT, period_ma, 0, MODE_SMA, InpAppliedPrice)
    if handle_maP == INVALID_HANDLE:
        Print('The iMA(', _str(period_ma), ') by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    handle_dev = iStdDev(None, PERIOD_CURRENT, period_dev, 0, MODE_SMA, InpAppliedPrice)
    if handle_dev == INVALID_HANDLE:
        Print('The iStdDev(', _str(period_dev), ') by ', EnumToString(InpAppliedPrice, 'ENUM_APPLIED_PRICE'), ' object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < fmax(period_ma, 4) or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - period_ma - 2
        ArrayInitialize(BufferBD, EMPTY_VALUE)
        ArrayInitialize(BufferDiff, 0)
        ArrayInitialize(BufferMA1, 0)
        ArrayInitialize(BufferMAP, 0)
        ArrayInitialize(BufferDev, 0)
        ArrayInitialize(BufferEMA, 0)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_ma1, 0, 0, count, BufferMA1)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_maP, 0, 0, count, BufferMAP)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_dev, 0, 0, count, BufferDev)
    if copied != count:
        return 0
    Bottom = 0.0
    for i in range(limit, 0 - 1, -1):
        SMA0 = BufferMAP[i]
        SMA1 = BufferMAP[i + 1]
        StdDev = BufferDev[i]
        Bottom = SMA0 - (deviation * StdDev)
        BufferDiff[i] = BufferMA1[i] - Bottom + (slope * (SMA0 - SMA1))
    if ExponentialMAOnBuffer(rates_total, prev_calculated, period_dev, period_ma, BufferDiff, BufferEMA) == 0:
        return 0
    for i in range(limit, 0 - 1, -1):
        BufferBD[i] = (_fdiv(100.0 * BufferEMA[i], Bottom) if (Bottom != 0) else 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BreakdownOscillator(_MQL5Indicator):
    name = 'Breakdown_Oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpPeriod': 10,  # Period
        'InpPeriodBand': 20,  # Band period
        'InpDeviation': 1.5,  # Deviation
        'InpSlopeFactor': 2.0,  # Slope factor
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpLevel': 2.0,  # Upper level
    }

