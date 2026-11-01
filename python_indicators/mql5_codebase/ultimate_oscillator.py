"""ultimate_oscillator — converted from MQL5: MQL5 Indicators/Ultimate Oscillator/ultimate_oscillator.mq5

Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'ultimate_oscillator', 'source': 'MQL5 Indicators/Ultimate Oscillator/ultimate_oscillator.mq5', 'folder': 'Ultimate Oscillator', 'inputs': [{'mql': 'InpFastPeriod', 'py': 'InpFastPeriod', 'param': 'InpFastPeriod', 'type': 'int', 'default': 7, 'label': 'Fast ATR period', 'sinput': False}, {'mql': 'InpMiddlePeriod', 'py': 'InpMiddlePeriod', 'param': 'InpMiddlePeriod', 'type': 'int', 'default': 14, 'label': 'Middle ATR period', 'sinput': False}, {'mql': 'InpSlowPeriod', 'py': 'InpSlowPeriod', 'param': 'InpSlowPeriod', 'type': 'int', 'default': 28, 'label': 'Slow ATR period', 'sinput': False}, {'mql': 'InpFastK', 'py': 'InpFastK', 'param': 'InpFastK', 'type': 'int', 'default': 4, 'label': 'Fast K', 'sinput': False}, {'mql': 'InpMiddleK', 'py': 'InpMiddleK', 'param': 'InpMiddleK', 'type': 'int', 'default': 2, 'label': 'Middle K', 'sinput': False}, {'mql': 'InpSlowK', 'py': 'InpSlowK', 'param': 'InpSlowK', 'type': 'int', 'default': 1, 'label': 'Slow K', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpFastPeriod = _input('InpFastPeriod', 7)  # Fast ATR period
InpMiddlePeriod = _input('InpMiddlePeriod', 14)  # Middle ATR period
InpSlowPeriod = _input('InpSlowPeriod', 28)  # Slow ATR period
InpFastK = _input('InpFastK', 4)  # Fast K
InpMiddleK = _input('InpMiddleK', 2)  # Middle K
InpSlowK = _input('InpSlowK', 1)  # Slow K
ExtUOBuffer = Arr(0, 0.0)
ExtBPBuffer = Arr(0, 0.0)
ExtFastATRBuffer = Arr(0, 0.0)
ExtMiddleATRBuffer = Arr(0, 0.0)
ExtSlowATRBuffer = Arr(0, 0.0)
ExtFastATRhandle = 0
ExtMiddleATRhandle = 0
ExtSlowATRhandle = 0
ExtDivider = 0.0
ExtMaxPeriod = 0

def OnInit():
    global ExtDivider, ExtFastATRhandle, ExtMaxPeriod, ExtMiddleATRhandle, ExtSlowATRhandle
    SetIndexBuffer(0, ExtUOBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtBPBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, ExtFastATRBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtMiddleATRBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, ExtSlowATRBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 30)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 70)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 100)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpSlowPeriod - 1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'UOS(' + _str(InpFastPeriod) + ', ' + _str(InpMiddlePeriod) + ', ' + _str(InpSlowPeriod) + ')')
    ExtFastATRhandle = iATR(Symbol(), 0, InpFastPeriod)
    ExtMiddleATRhandle = iATR(Symbol(), 0, InpMiddlePeriod)
    ExtSlowATRhandle = iATR(Symbol(), 0, InpSlowPeriod)
    ExtDivider = InpFastK + InpMiddleK + InpSlowK
    ExtMaxPeriod = InpSlowPeriod
    if ExtMaxPeriod < InpMiddlePeriod:
        ExtMaxPeriod = InpMiddlePeriod
    if ExtMaxPeriod < InpFastPeriod:
        ExtMaxPeriod = InpFastPeriod

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    limit = 0
    TL = 0.0
    RawUO = 0.0
    if rates_total < ExtMaxPeriod:
        return 0
    calculated = BarsCalculated(ExtFastATRhandle)
    if calculated < rates_total:
        Print('Not all data of ExtFastATRhandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    calculated = BarsCalculated(ExtMiddleATRhandle)
    if calculated < rates_total:
        Print('Not all data of ExtMiddleATRhandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    calculated = BarsCalculated(ExtSlowATRhandle)
    if calculated < rates_total:
        Print('Not all data of ExtSlowATRhandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if False:
        return 0
    if CopyBuffer(ExtFastATRhandle, 0, 0, to_copy, ExtFastATRBuffer) <= 0:
        Print('getting ExtFastATRhandle is failed! Error', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(ExtMiddleATRhandle, 0, 0, to_copy, ExtMiddleATRBuffer) <= 0:
        Print('getting ExtMiddleATRhandle is failed! Error', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(ExtSlowATRhandle, 0, 0, to_copy, ExtSlowATRBuffer) <= 0:
        Print('getting ExtSlowATRhandle is failed! Error', GetLastError())
        return 0
    if prev_calculated == 0:
        ExtBPBuffer[0] = 0.0
        ExtUOBuffer[0] = 0.0
        i = 1
        for i in range(i, InpSlowPeriod + 1):
            ExtUOBuffer[i] = 0.0
            TL = MathMin(Low[i], Close[i - 1])
            ExtBPBuffer[i] = Close[i] - TL
        else:
            i = _range_end(i, InpSlowPeriod + 1, 1)
        limit = InpSlowPeriod + 1
    else:
        limit = prev_calculated - 1
    i = limit
    for i in range(i, rates_total):
        TL = MathMin(Low[i], Close[i - 1])
        ExtBPBuffer[i] = Close[i] - TL
        if (ExtFastATRBuffer[i] != 0.0 and ExtMiddleATRBuffer[i] != 0.0) and ExtSlowATRBuffer[i] != 0.0:
            RawUO = _fdiv(InpFastK * SimpleMA(i, InpFastPeriod, ExtBPBuffer), ExtFastATRBuffer[i]) + _fdiv(InpMiddleK * SimpleMA(i, InpMiddlePeriod, ExtBPBuffer), ExtMiddleATRBuffer[i]) + _fdiv(InpSlowK * SimpleMA(i, InpSlowPeriod, ExtBPBuffer), ExtSlowATRBuffer[i])
            ExtUOBuffer[i] = _fdiv(RawUO, ExtDivider) * 100
        else:
            ExtUOBuffer[i] = ExtUOBuffer[i - 1]
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class UltimateOscillator(_MQL5Indicator):
    name = 'ultimate_oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpFastPeriod': 7,  # Fast ATR period
        'InpMiddlePeriod': 14,  # Middle ATR period
        'InpSlowPeriod': 28,  # Slow ATR period
        'InpFastK': 4,  # Fast K
        'InpMiddleK': 2,  # Middle K
        'InpSlowK': 1,  # Slow K
    }

