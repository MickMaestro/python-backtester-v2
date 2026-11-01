"""gator — converted from MQL5: MQL5 Indicators/Gator Oscillator/gator.mq5

Gator Oscillator
based on 3 non-shifted moving averages
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 2}, 'types': {1: 10, 2: 10}, 'colors': {1: [32768, 255], 2: [32768, 255]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'Gator Upper', 2: 'Gator Lower'}, 'levels': [], 'description': ['Gator Oscillator', 'based on 3 non-shifted moving averages'], 'name': 'gator', 'source': 'MQL5 Indicators/Gator Oscillator/gator.mq5', 'folder': 'Gator Oscillator', 'inputs': [{'mql': 'InpJawsPeriod', 'py': 'InpJawsPeriod', 'param': 'InpJawsPeriod', 'type': 'int', 'default': 13, 'label': 'Jaws period', 'sinput': False}, {'mql': 'InpJawsShift', 'py': 'InpJawsShift', 'param': 'InpJawsShift', 'type': 'int', 'default': 8, 'label': 'Jaws shift', 'sinput': False}, {'mql': 'InpTeethPeriod', 'py': 'InpTeethPeriod', 'param': 'InpTeethPeriod', 'type': 'int', 'default': 8, 'label': 'Teeth period', 'sinput': False}, {'mql': 'InpTeethShift', 'py': 'InpTeethShift', 'param': 'InpTeethShift', 'type': 'int', 'default': 5, 'label': 'Teeth shift', 'sinput': False}, {'mql': 'InpLipsPeriod', 'py': 'InpLipsPeriod', 'param': 'InpLipsPeriod', 'type': 'int', 'default': 5, 'label': 'Lips period', 'sinput': False}, {'mql': 'InpLipsShift', 'py': 'InpLipsShift', 'param': 'InpLipsShift', 'type': 'int', 'default': 3, 'label': 'Lips shift', 'sinput': False}, {'mql': 'InpMAMethod', 'py': 'InpMAMethod', 'param': 'InpMAMethod', 'type': 'int', 'default': 2, 'label': 'Moving average method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 5, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpJawsPeriod = _input('InpJawsPeriod', 13)  # Jaws period
InpJawsShift = _input('InpJawsShift', 8)  # Jaws shift
InpTeethPeriod = _input('InpTeethPeriod', 8)  # Teeth period
InpTeethShift = _input('InpTeethShift', 5)  # Teeth shift
InpLipsPeriod = _input('InpLipsPeriod', 5)  # Lips period
InpLipsShift = _input('InpLipsShift', 3)  # Lips shift
InpMAMethod = _input('InpMAMethod', MODE_SMMA)  # Moving average method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_MEDIAN)  # Applied price
ExtUpperBuffer = Arr(0, 0.0)
ExtUpColorsBuffer = Arr(0, 0.0)
ExtLowerBuffer = Arr(0, 0.0)
ExtLoColorsBuffer = Arr(0, 0.0)
ExtJawsBuffer = Arr(0, 0.0)
ExtTeethBuffer = Arr(0, 0.0)
ExtLipsBuffer = Arr(0, 0.0)
ExtJawsHandle = 0
ExtTeethHandle = 0
ExtLipsHandle = 0
ExtUpperShift = 0
ExtLowerShift = 0
ExtFlag = False

def OnInit():
    global ExtFlag, ExtJawsHandle, ExtLipsHandle, ExtLowerShift, ExtTeethHandle, ExtUpperShift
    SetIndexBuffer(0, ExtUpperBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtUpColorsBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, ExtLowerBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtLoColorsBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, ExtJawsBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, ExtTeethBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, ExtLipsBuffer, INDICATOR_CALCULATIONS)
    ExtJawsHandle = iMA(None, 0, InpJawsPeriod, 0, InpMAMethod, InpAppliedPrice)
    ExtTeethHandle = iMA(None, 0, InpTeethPeriod, 0, InpMAMethod, InpAppliedPrice)
    ExtLipsHandle = iMA(None, 0, InpLipsPeriod, 0, InpMAMethod, InpAppliedPrice)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpTeethShift + InpTeethPeriod)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, InpLipsShift + InpLipsPeriod)
    PlotIndexSetInteger(0, PLOT_SHIFT, InpTeethShift)
    PlotIndexSetInteger(1, PLOT_SHIFT, InpLipsShift)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Gator(' + _str(InpJawsPeriod) + ',' + _str(InpTeethPeriod) + ',' + _str(InpLipsPeriod) + ')')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    ExtUpperShift = InpJawsShift - InpTeethShift
    ExtLowerShift = InpTeethShift - InpLipsShift
    ExtFlag = CheckForInput()
    if not ExtFlag:
        Print("Wrong input parameters. Indicator won't work.")
    return not ExtFlag

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    pos = 0
    shift = 0
    dCurr = 0.0
    dPrev = 0.0
    if ExtUpperShift > ExtLowerShift:
        shift = ExtUpperShift
    else:
        shift = ExtLowerShift
    if (not ExtFlag) or shift > rates_total:
        return 0
    calculated = BarsCalculated(ExtJawsHandle)
    if calculated < rates_total:
        Print('Not all data of ExtJawsHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    calculated = BarsCalculated(ExtTeethHandle)
    if calculated < rates_total:
        Print('Not all data of ExtTeethHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    calculated = BarsCalculated(ExtLipsHandle)
    if calculated < rates_total:
        Print('Not all data of ExtLipsHandle is calculated (', calculated, 'bars ). Error', GetLastError())
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
    if CopyBuffer(ExtJawsHandle, 0, 0, to_copy, ExtJawsBuffer) <= 0:
        Print('getting ExtJawsHandle is failed! Error', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(ExtTeethHandle, 0, 0, to_copy, ExtTeethBuffer) <= 0:
        Print('getting ExtTeethHandle is failed! Error', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(ExtLipsHandle, 0, 0, to_copy, ExtLipsBuffer) <= 0:
        Print('getting ExtLipsHandle is failed! Error', GetLastError())
        return 0
    pos = prev_calculated - 2
    if pos < shift:
        for i in range(0, shift):
            ExtUpperBuffer[i] = 0.0
            ExtUpColorsBuffer[i] = 0.0
            ExtLowerBuffer[i] = 0.0
            ExtLoColorsBuffer[i] = 0.0
        pos = shift
    lower_limit = ExtLowerShift + InpLipsShift + InpLipsPeriod
    upper_limit = ExtUpperShift + InpTeethShift + InpTeethPeriod
    for i in range(pos, rates_total):
        if i >= lower_limit:
            dCurr = -fabs(ExtTeethBuffer[i - ExtLowerShift] - ExtLipsBuffer[i])
            dPrev = ExtLowerBuffer[i - 1]
            ExtLowerBuffer[i] = dCurr
            if dPrev == dCurr:
                ExtLoColorsBuffer[i] = ExtLoColorsBuffer[i - 1]
            else:
                if dPrev < dCurr:
                    ExtLoColorsBuffer[i] = 1.0
                else:
                    ExtLoColorsBuffer[i] = 0.0
        else:
            ExtLowerBuffer[i] = 0.0
            ExtLoColorsBuffer[i] = 0.0
        if i >= upper_limit:
            dCurr = fabs(ExtJawsBuffer[i - ExtUpperShift] - ExtTeethBuffer[i])
            ExtUpperBuffer[i] = dCurr
            dPrev = ExtUpperBuffer[i - 1]
            if dPrev == dCurr:
                ExtUpColorsBuffer[i] = ExtUpColorsBuffer[i - 1]
            else:
                if dPrev < dCurr:
                    ExtUpColorsBuffer[i] = 0.0
                else:
                    ExtUpColorsBuffer[i] = 1.0
        else:
            ExtUpperBuffer[i] = 0.0
            ExtUpColorsBuffer[i] = 0.0
    return rates_total

def CheckForInput():
    if InpJawsPeriod <= InpTeethPeriod or InpTeethPeriod <= InpLipsPeriod:
        return False
    if InpJawsShift <= InpTeethShift or InpTeethShift <= InpLipsShift:
        return False
    if InpJawsPeriod <= InpJawsShift:
        return False
    if InpTeethPeriod <= InpTeethShift:
        return False
    if InpLipsPeriod <= InpLipsShift:
        return False
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Gator(_MQL5Indicator):
    name = 'gator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpJawsPeriod': 13,  # Jaws period
        'InpJawsShift': 8,  # Jaws shift
        'InpTeethPeriod': 8,  # Teeth period
        'InpTeethShift': 5,  # Teeth shift
        'InpLipsPeriod': 5,  # Lips period
        'InpLipsShift': 3,  # Lips shift
        'InpMAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # Moving average method
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=5),  # Applied price
    }

