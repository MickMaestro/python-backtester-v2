"""backgroundcandle_colorstepxccx_htf — converted from MQL5: MQL5 Indicators/BackgroundCandle_ColorStepXCCX_HTF/backgroundcandle_colorstepxccx_htf.mq5

A candlestick indicator colored based on the ColorStepXCCX indicator with timeframe selection option available in input parameters
Copyright: Copyright © 2014, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 12, 'indicator_plots': 6}, 'types': {1: 7, 2: 7, 3: 7, 4: 7, 5: 7, 6: 7}, 'colors': {1: [16436871, 12695295], 2: [16748574, 36095], 3: [16436871, 12695295], 4: [16436871, 12695295], 5: [16748574, 36095], 6: [16436871, 12695295]}, 'widths': {}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'Upper Shade', 2: 'Body', 3: 'Lower Shade', 4: 'Upper Shade', 5: 'Body', 6: 'Lower Shade'}, 'levels': [], 'description': ['A candlestick indicator colored based on the ColorStepXCCX indicator with timeframe selection option available in input parameters'], 'name': 'backgroundcandle_colorstepxccx_htf', 'source': 'MQL5 Indicators/BackgroundCandle_ColorStepXCCX_HTF/backgroundcandle_colorstepxccx_htf.mq5', 'folder': 'BackgroundCandle_ColorStepXCCX_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Indicator chart period', 'sinput': False}, {'mql': 'DSmoothMethod', 'py': 'DSmoothMethod', 'param': 'DSmoothMethod', 'type': 'int', 'default': 4, 'label': 'Price smoothing method', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'int', 'default': 30, 'label': 'Moving average period', 'sinput': False}, {'mql': 'DPhase', 'py': 'DPhase', 'param': 'DPhase', 'type': 'int', 'default': 100, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'MSmoothMethod', 'py': 'MSmoothMethod', 'param': 'MSmoothMethod', 'type': 'int', 'default': 7, 'label': 'Deviation smoothing method', 'sinput': False}, {'mql': 'MPeriod', 'py': 'MPeriod', 'param': 'MPeriod', 'type': 'int', 'default': 7, 'label': 'Average deviation period', 'sinput': False}, {'mql': 'MPhase', 'py': 'MPhase', 'param': 'MPhase', 'type': 'int', 'default': 15, 'label': 'Deviation smoothing parameter', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 6, 'label': 'Applied price', 'sinput': False}, {'mql': 'StepSizeFast', 'py': 'StepSizeFast', 'param': 'StepSizeFast', 'type': 'int', 'default': 5, 'label': 'Fast step', 'sinput': False}, {'mql': 'StepSizeSlow', 'py': 'StepSizeSlow', 'param': 'StepSizeSlow', 'type': 'int', 'default': 30, 'label': 'Slow step', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# enum Smooth_Method
MODE_SMA_ = 0
MODE_EMA_ = 1
MODE_SMMA_ = 2
MODE_LWMA_ = 3
MODE_JJMA = 4
MODE_JurX = 5
MODE_ParMA = 6
MODE_T3 = 7
MODE_VIDYA = 8
MODE_AMA = 9
_enum('Smooth_Method', {0: 'MODE_SMA_', 1: 'MODE_EMA_', 2: 'MODE_SMMA_', 3: 'MODE_LWMA_', 4: 'MODE_JJMA', 5: 'MODE_JurX', 6: 'MODE_ParMA', 7: 'MODE_T3', 8: 'MODE_VIDYA', 9: 'MODE_AMA'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Indicator chart period
DSmoothMethod = _input('DSmoothMethod', MODE_JJMA)  # Price smoothing method
DPeriod = _input('DPeriod', 30)  # Moving average period
DPhase = _input('DPhase', 100)  # Smoothing parameter
MSmoothMethod = _input('MSmoothMethod', MODE_T3)  # Deviation smoothing method
MPeriod = _input('MPeriod', 7)  # Average deviation period
MPhase = _input('MPhase', 15)  # Deviation smoothing parameter
IPC = _input('IPC', PRICE_TYPICAL)  # Applied price
StepSizeFast = _input('StepSizeFast', 5)  # Fast step
StepSizeSlow = _input('StepSizeSlow', 30)  # Slow step
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
ExtA1Buffer = Arr(0, 0.0)
ExtB1Buffer = Arr(0, 0.0)
ExtA2Buffer = Arr(0, 0.0)
ExtB2Buffer = Arr(0, 0.0)
ExtA3Buffer = Arr(0, 0.0)
ExtB3Buffer = Arr(0, 0.0)
ExtA4Buffer = Arr(0, 0.0)
ExtB4Buffer = Arr(0, 0.0)
ExtA5Buffer = Arr(0, 0.0)
ExtB5Buffer = Arr(0, 0.0)
ExtA6Buffer = Arr(0, 0.0)
ExtB6Buffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def OnInit():
    global Ind_Handle, min_rates_total
    if not TimeFramesCheck('BackgroundCandle_ColorStepXCCX', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'ColorStepXCCX', DSmoothMethod, DPeriod, DPhase, MSmoothMethod, MPeriod, MPhase, IPC, StepSizeFast, StepSizeSlow, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of the ColorStepXCCX indicator')
        return INIT_FAILED
    ArrayInit(0, ExtA1Buffer)
    ArrayInit(1, ExtB1Buffer)
    ArrayInit(2, ExtA2Buffer)
    ArrayInit(3, ExtB2Buffer)
    ArrayInit(4, ExtA3Buffer)
    ArrayInit(5, ExtB3Buffer)
    ArrayInit(6, ExtA4Buffer)
    ArrayInit(7, ExtB4Buffer)
    ArrayInit(8, ExtA5Buffer)
    ArrayInit(9, ExtB5Buffer)
    ArrayInit(10, ExtA6Buffer)
    ArrayInit(11, ExtB6Buffer)
    PlotInit(0, 2, Shift)
    PlotInit(1, 2, Shift)
    PlotInit(2, 2, Shift)
    PlotInit(3, 2, Shift)
    PlotInit(4, 2, Shift)
    PlotInit(5, 2, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'BackgroundCandle_ColorStepXCCX', '(', EnumToString(TimeFrame, 'ENUM_TIMEFRAMES'), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, Symbol(), TimeFrame, Ind_Handle, ExtA1Buffer, ExtB1Buffer, ExtA2Buffer, ExtB2Buffer, ExtA3Buffer, ExtB3Buffer, ExtA4Buffer, ExtB4Buffer, ExtA5Buffer, ExtB5Buffer, ExtA6Buffer, ExtB6Buffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def CountIndicator(Numb, Symb, TFrame, IndHandle, ExtA1Buff, ExtB1Buff, ExtA2Buff, ExtB2Buff, ExtA3Buff, ExtB3Buff, ExtA4Buff, ExtB4Buff, ExtA5Buff, ExtB5Buff, ExtA6Buff, ExtB6Buff, Time, Rates_Total, Prev_Calculated, Min_Rates_Total):
    global _s_CountIndicator_LastTime, _s_CountIndicator_Sign
    iOpen_ = Arr(1, 0.0, dyn=False)
    iLow_ = Arr(1, 0.0, dyn=False)
    iHigh_ = Arr(1, 0.0, dyn=False)
    iClose_ = Arr(1, 0.0, dyn=False)
    iUp = Arr(1, 0.0, dyn=False)
    iDn = Arr(1, 0.0, dyn=False)
    iTime_ = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
        _s_CountIndicator_LastTime = 0
        _s_CountIndicator_Sign = 1
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        if CopyTime(Symbol(), TFrame, _DT(Time[bar]), 1, iTime_) <= 0:
            return (0 != 0)
        if Time[bar] >= iTime_[0] and Time[bar + 1] < iTime_[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            if iTime_[0] != _s_CountIndicator_LastTime:
                _s_CountIndicator_LastTime = iTime_[0]
                _s_CountIndicator_Sign *= -1
            if CopyBuffer(IndHandle, 0, _DT(Time[bar]), 1, iUp) <= 0:
                return (0 != 0)
            if CopyBuffer(IndHandle, 1, _DT(Time[bar]), 1, iDn) <= 0:
                return (0 != 0)
            if CopyOpen(Symbol(), TFrame, _DT(Time[bar]), 1, iOpen_) <= 0:
                return (0 != 0)
            if CopyLow(Symbol(), TFrame, _DT(Time[bar]), 1, iLow_) <= 0:
                return (0 != 0)
            if CopyHigh(Symbol(), TFrame, _DT(Time[bar]), 1, iHigh_) <= 0:
                return (0 != 0)
            if CopyClose(Symbol(), TFrame, _DT(Time[bar]), 1, iClose_) <= 0:
                return (0 != 0)
            mathmax = MathMax(iOpen_[0], iClose_[0])
            mathmin = MathMin(iOpen_[0], iClose_[0])
            if _s_CountIndicator_Sign > 0:
                if iUp[0] > iDn[0]:
                    ExtA1Buff[bar] = iHigh_[0]
                    ExtB1Buff[bar] = mathmax
                    ExtA2Buff[bar] = mathmax
                    ExtB2Buff[bar] = mathmin
                    ExtA3Buff[bar] = mathmin
                    ExtB3Buff[bar] = iLow_[0]
                if iUp[0] < iDn[0]:
                    ExtB1Buff[bar] = iHigh_[0]
                    ExtA1Buff[bar] = mathmax
                    ExtB2Buff[bar] = mathmax
                    ExtA2Buff[bar] = mathmin
                    ExtB3Buff[bar] = mathmin
                    ExtA3Buff[bar] = iLow_[0]
                if iUp[0] == iDn[0]:
                    ExtB1Buff[bar] = 0.0
                    ExtA1Buff[bar] = 0.0
                    ExtA2Buff[bar] = 0.0
                    ExtB2Buff[bar] = 0.0
                    ExtB3Buff[bar] = 0.0
                    ExtA3Buff[bar] = 0.0
                ExtA4Buff[bar] = 0.0
                ExtB4Buff[bar] = 0.0
                ExtA5Buff[bar] = 0.0
                ExtB5Buff[bar] = 0.0
                ExtA6Buff[bar] = 0.0
                ExtB6Buff[bar] = 0.0
            else:
                if iUp[0] > iDn[0]:
                    ExtA4Buff[bar] = iHigh_[0]
                    ExtB4Buff[bar] = mathmax
                    ExtA5Buff[bar] = mathmax
                    ExtB5Buff[bar] = mathmin
                    ExtA6Buff[bar] = mathmin
                    ExtB6Buff[bar] = iLow_[0]
                if iUp[0] < iDn[0]:
                    ExtB4Buff[bar] = iHigh_[0]
                    ExtA4Buff[bar] = mathmax
                    ExtB5Buff[bar] = mathmax
                    ExtA5Buff[bar] = mathmin
                    ExtB6Buff[bar] = mathmin
                    ExtA6Buff[bar] = iLow_[0]
                if iUp[0] == iDn[0]:
                    ExtB4Buff[bar] = 0.0
                    ExtA4Buff[bar] = 0.0
                    ExtA5Buff[bar] = 0.0
                    ExtB5Buff[bar] = 0.0
                    ExtB6Buff[bar] = 0.0
                    ExtA6Buff[bar] = 0.0
                ExtA1Buff[bar] = 0.0
                ExtB1Buff[bar] = 0.0
                ExtA2Buff[bar] = 0.0
                ExtB2Buff[bar] = 0.0
                ExtA3Buff[bar] = 0.0
                ExtB3Buff[bar] = 0.0
        else:
            bar1 = bar + 1
            ExtA1Buff[bar] = ExtA1Buff[bar1]
            ExtB1Buff[bar] = ExtB1Buff[bar1]
            ExtA2Buff[bar] = ExtA2Buff[bar1]
            ExtB2Buff[bar] = ExtB2Buff[bar1]
            ExtA3Buff[bar] = ExtA3Buff[bar1]
            ExtB3Buff[bar] = ExtB3Buff[bar1]
            ExtA4Buff[bar] = ExtA4Buff[bar1]
            ExtB4Buff[bar] = ExtB4Buff[bar1]
            ExtA5Buff[bar] = ExtA5Buff[bar1]
            ExtB5Buff[bar] = ExtB5Buff[bar1]
            ExtA6Buff[bar] = ExtA6Buff[bar1]
            ExtB6Buff[bar] = ExtB6Buff[bar1]
    return True

def PlotInit(PlotNumber, DrawBegin, PlotShift):
    PlotIndexSetInteger(PlotNumber, PLOT_DRAW_BEGIN, DrawBegin)
    PlotIndexSetInteger(PlotNumber, PLOT_SHIFT, PlotShift)

def ArrayInit(ArrNumber, Array):
    SetIndexBuffer(ArrNumber, Array, INDICATOR_DATA)
    ArraySetAsSeries(Array, True)

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Print('Chart period for the ' + IndName + ' indicator cannot be less than the period of the current chart!')
        Print('You must change the indicator input parameters!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountIndicator_Sign = 0
_s_CountIndicator_LastTime = 0
_s_CountIndicator_LastCountBar = Arr(1, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BackgroundcandleColorstepxccxHtf(_MQL5Indicator):
    name = 'backgroundcandle_colorstepxccx_htf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Indicator chart period
        'DSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Price smoothing method
        'DPeriod': 30,  # Moving average period
        'DPhase': 100,  # Smoothing parameter
        'MSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # Deviation smoothing method
        'MPeriod': 7,  # Average deviation period
        'MPhase': 15,  # Deviation smoothing parameter
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=6),  # Applied price
        'StepSizeFast': 5,  # Fast step
        'StepSizeSlow': 30,  # Slow step
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

