"""alligator — converted from MQL5: MQL5 Indicators/Alligator/alligator.mq5

Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16711680], 2: [255], 3: [65280]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {}, 'labels': {1: 'Jaws', 2: 'Teeth', 3: 'Lips'}, 'levels': [], 'description': [], 'name': 'alligator', 'source': 'MQL5 Indicators/Alligator/alligator.mq5', 'folder': 'Alligator', 'inputs': [{'mql': 'InpJawsPeriod', 'py': 'InpJawsPeriod', 'param': 'InpJawsPeriod', 'type': 'int', 'default': 13, 'label': 'Jaws period', 'sinput': False}, {'mql': 'InpJawsShift', 'py': 'InpJawsShift', 'param': 'InpJawsShift', 'type': 'int', 'default': 8, 'label': 'Jaws shift', 'sinput': False}, {'mql': 'InpTeethPeriod', 'py': 'InpTeethPeriod', 'param': 'InpTeethPeriod', 'type': 'int', 'default': 8, 'label': 'Teeth period', 'sinput': False}, {'mql': 'InpTeethShift', 'py': 'InpTeethShift', 'param': 'InpTeethShift', 'type': 'int', 'default': 5, 'label': 'Teeth shift', 'sinput': False}, {'mql': 'InpLipsPeriod', 'py': 'InpLipsPeriod', 'param': 'InpLipsPeriod', 'type': 'int', 'default': 5, 'label': 'Lips period', 'sinput': False}, {'mql': 'InpLipsShift', 'py': 'InpLipsShift', 'param': 'InpLipsShift', 'type': 'int', 'default': 3, 'label': 'Lips shift', 'sinput': False}, {'mql': 'InpMAMethod', 'py': 'InpMAMethod', 'param': 'InpMAMethod', 'type': 'int', 'default': 2, 'label': 'Moving average method', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 5, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpJawsPeriod = _input('InpJawsPeriod', 13)  # Jaws period
InpJawsShift = _input('InpJawsShift', 8)  # Jaws shift
InpTeethPeriod = _input('InpTeethPeriod', 8)  # Teeth period
InpTeethShift = _input('InpTeethShift', 5)  # Teeth shift
InpLipsPeriod = _input('InpLipsPeriod', 5)  # Lips period
InpLipsShift = _input('InpLipsShift', 3)  # Lips shift
InpMAMethod = _input('InpMAMethod', MODE_SMMA)  # Moving average method
InpAppliedPrice = _input('InpAppliedPrice', PRICE_MEDIAN)  # Applied price
ExtJaws = Arr(0, 0.0)
ExtTeeth = Arr(0, 0.0)
ExtLips = Arr(0, 0.0)
ExtJawsHandle = 0
ExtTeethHandle = 0
ExtLipsHandle = 0
ExtBarsMinimum = 0

def OnInit():
    global ExtBarsMinimum, ExtJawsHandle, ExtLipsHandle, ExtTeethHandle
    SetIndexBuffer(0, ExtJaws, INDICATOR_DATA)
    SetIndexBuffer(1, ExtTeeth, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLips, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpJawsPeriod - 1)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, InpTeethPeriod - 1)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, InpLipsPeriod - 1)
    PlotIndexSetInteger(0, PLOT_SHIFT, InpJawsShift)
    PlotIndexSetInteger(1, PLOT_SHIFT, InpTeethShift)
    PlotIndexSetInteger(2, PLOT_SHIFT, InpLipsShift)
    PlotIndexSetString(0, PLOT_LABEL, 'Jaws(' + _str(InpJawsPeriod) + ')')
    PlotIndexSetString(1, PLOT_LABEL, 'Teeth(' + _str(InpTeethPeriod) + ')')
    PlotIndexSetString(2, PLOT_LABEL, 'Lips(' + _str(InpLipsPeriod) + ')')
    ExtJawsHandle = iMA(None, 0, InpJawsPeriod, 0, InpMAMethod, InpAppliedPrice)
    ExtTeethHandle = iMA(None, 0, InpTeethPeriod, 0, InpMAMethod, InpAppliedPrice)
    ExtLipsHandle = iMA(None, 0, InpLipsPeriod, 0, InpMAMethod, InpAppliedPrice)
    ExtBarsMinimum = InpJawsPeriod + InpJawsShift
    if ExtBarsMinimum < (InpTeethPeriod + InpTeethShift):
        ExtBarsMinimum = InpTeethPeriod + InpTeethShift
    if ExtBarsMinimum < (InpLipsPeriod + InpLipsPeriod):
        ExtBarsMinimum = InpLipsPeriod + InpLipsPeriod

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    if rates_total < ExtBarsMinimum:
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
    if CopyBuffer(ExtJawsHandle, 0, 0, to_copy, ExtJaws) <= 0:
        Print('getting ExtJawsHandle is failed! Error', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(ExtTeethHandle, 0, 0, to_copy, ExtTeeth) <= 0:
        Print('getting ExtTeethHandle is failed! Error', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(ExtLipsHandle, 0, 0, to_copy, ExtLips) <= 0:
        Print('getting ExtLipsHandle is failed! Error', GetLastError())
        return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Alligator(_MQL5Indicator):
    name = 'alligator'
    pane = _Pane.PRICE
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

