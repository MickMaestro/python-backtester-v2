"""parabolicsar — converted from MQL5: MQL5 Indicators/Parabolic SAR/parabolicsar.mq5

Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 5}, 'colors': {1: [16748574]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'parabolicsar', 'source': 'MQL5 Indicators/Parabolic SAR/parabolicsar.mq5', 'folder': 'Parabolic SAR', 'inputs': [{'mql': 'InpSARStep', 'py': 'InpSARStep', 'param': 'InpSARStep', 'type': 'double', 'default': 0.02, 'label': 'Step', 'sinput': False}, {'mql': 'InpSARMaximum', 'py': 'InpSARMaximum', 'param': 'InpSARMaximum', 'type': 'double', 'default': 0.2, 'label': 'Maximum', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpSARStep = _input('InpSARStep', 0.02)  # Step
InpSARMaximum = _input('InpSARMaximum', 0.2)  # Maximum
ExtSARBuffer = Arr(0, 0.0)
ExtEPBuffer = Arr(0, 0.0)
ExtAFBuffer = Arr(0, 0.0)
ExtLastRevPos = 0
ExtDirectionLong = False
ExtSarStep = 0.0
ExtSarMaximum = 0.0

def OnInit():
    global ExtDirectionLong, ExtLastRevPos, ExtSarMaximum, ExtSarStep
    if InpSARStep < 0.0:
        ExtSarStep = 0.02
        Print('Input parametr InpSARStep has incorrect value. Indicator will use value', ExtSarStep, 'for calculations.')
    else:
        ExtSarStep = InpSARStep
    if InpSARMaximum < 0.0:
        ExtSarMaximum = 0.2
        Print('Input parametr InpSARMaximum has incorrect value. Indicator will use value', ExtSarMaximum, 'for calculations.')
    else:
        ExtSarMaximum = InpSARMaximum
    SetIndexBuffer(0, ExtSARBuffer)
    SetIndexBuffer(1, ExtEPBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, ExtAFBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetString(0, PLOT_LABEL, 'SAR(' + DoubleToString(ExtSarStep, 2) + ',' + DoubleToString(ExtSarMaximum, 2) + ')')
    ExtLastRevPos = 0
    ExtDirectionLong = False

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    global ExtDirectionLong, ExtLastRevPos
    if rates_total < 3:
        return 0
    pos = prev_calculated - 1
    if pos < 1:
        pos = 1
        ExtAFBuffer[0] = ExtSarStep
        ExtAFBuffer[1] = ExtSarStep
        ExtSARBuffer[0] = High[0]
        ExtLastRevPos = 0
        ExtDirectionLong = False
        ExtSARBuffer[1] = GetHigh(pos, ExtLastRevPos, High)
        ExtEPBuffer[0] = Low[pos]
        ExtEPBuffer[1] = Low[pos]
    for i in range(pos, rates_total - 1):
        if ExtDirectionLong:
            if ExtSARBuffer[i] > Low[i]:
                ExtDirectionLong = False
                ExtSARBuffer[i] = GetHigh(i, ExtLastRevPos, High)
                ExtEPBuffer[i] = Low[i]
                ExtLastRevPos = i
                ExtAFBuffer[i] = ExtSarStep
        else:
            if ExtSARBuffer[i] < High[i]:
                ExtDirectionLong = True
                ExtSARBuffer[i] = GetLow(i, ExtLastRevPos, Low)
                ExtEPBuffer[i] = High[i]
                ExtLastRevPos = i
                ExtAFBuffer[i] = ExtSarStep
        if ExtDirectionLong:
            if High[i] > ExtEPBuffer[i - 1] and i != ExtLastRevPos:
                ExtEPBuffer[i] = High[i]
                ExtAFBuffer[i] = ExtAFBuffer[i - 1] + ExtSarStep
                if ExtAFBuffer[i] > ExtSarMaximum:
                    ExtAFBuffer[i] = ExtSarMaximum
            else:
                if i != ExtLastRevPos:
                    ExtAFBuffer[i] = ExtAFBuffer[i - 1]
                    ExtEPBuffer[i] = ExtEPBuffer[i - 1]
            ExtSARBuffer[i + 1] = ExtSARBuffer[i] + (ExtAFBuffer[i] * (ExtEPBuffer[i] - ExtSARBuffer[i]))
            if ExtSARBuffer[i + 1] > Low[i] or ExtSARBuffer[i + 1] > Low[i - 1]:
                ExtSARBuffer[i + 1] = MathMin(Low[i], Low[i - 1])
        else:
            if Low[i] < ExtEPBuffer[i - 1] and i != ExtLastRevPos:
                ExtEPBuffer[i] = Low[i]
                ExtAFBuffer[i] = ExtAFBuffer[i - 1] + ExtSarStep
                if ExtAFBuffer[i] > ExtSarMaximum:
                    ExtAFBuffer[i] = ExtSarMaximum
            else:
                if i != ExtLastRevPos:
                    ExtAFBuffer[i] = ExtAFBuffer[i - 1]
                    ExtEPBuffer[i] = ExtEPBuffer[i - 1]
            ExtSARBuffer[i + 1] = ExtSARBuffer[i] + (ExtAFBuffer[i] * (ExtEPBuffer[i] - ExtSARBuffer[i]))
            if ExtSARBuffer[i + 1] < High[i] or ExtSARBuffer[i + 1] < High[i - 1]:
                ExtSARBuffer[i + 1] = MathMax(High[i], High[i - 1])
    return rates_total

def GetHigh(nPosition, nStartPeriod, HiData):
    result = HiData[nStartPeriod]
    for i in range(nStartPeriod, nPosition + 1):
        if result < HiData[i]:
            result = HiData[i]
    return result

def GetLow(nPosition, nStartPeriod, LoData):
    result = LoData[nStartPeriod]
    for i in range(nStartPeriod, nPosition + 1):
        if result > LoData[i]:
            result = LoData[i]
    return result


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Parabolicsar(_MQL5Indicator):
    name = 'parabolicsar'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpSARStep': 0.02,  # Step
        'InpSARMaximum': 0.2,  # Maximum
    }

