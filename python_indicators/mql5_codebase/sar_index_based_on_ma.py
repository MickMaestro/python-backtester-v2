"""SAR index based on MA — converted from MQL5: MQL5 Indicators/SAR index based on MA/SAR index based on MA.mq5

Copyright: Copyright © 2018, Vladimir Karputov; Link: http://wmua.ru/slesar/; Version: 1.008

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Vladimir Karputov', 'link': 'http://wmua.ru/slesar/', 'version': '1.008', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 5, 2: 1}, 'colors': {1: [16748574], 2: [255]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'SAR index based on MA', 'source': 'MQL5 Indicators/SAR index based on MA/SAR index based on MA.mq5', 'folder': 'SAR index based on MA', 'inputs': [{'mql': 'InpSARStep', 'py': 'InpSARStep', 'param': 'InpSARStep', 'type': 'double', 'default': 0.02, 'label': 'SAR: Step', 'sinput': False}, {'mql': 'InpSARMaximum', 'py': 'InpSARMaximum', 'param': 'InpSARMaximum', 'type': 'double', 'default': 0.04, 'label': 'SAR: Maximum', 'sinput': False}, {'mql': 'InpMAPeriod', 'py': 'InpMAPeriod', 'param': 'InpMAPeriod', 'type': 'int', 'default': 13, 'label': 'MA: Period', 'sinput': False}, {'mql': 'InpMAShift', 'py': 'InpMAShift', 'param': 'InpMAShift', 'type': 'int', 'default': 0, 'label': 'MA: Shift', 'sinput': False}, {'mql': 'InpMAMethod', 'py': 'InpMAMethod', 'param': 'InpMAMethod', 'type': 'int', 'default': 2, 'label': 'MA: Method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpSARStep = _input('InpSARStep', 0.02)  # SAR: Step
InpSARMaximum = _input('InpSARMaximum', 0.04)  # SAR: Maximum
InpMAPeriod = _input('InpMAPeriod', 13)  # MA: Period
InpMAShift = _input('InpMAShift', 0)  # MA: Shift
InpMAMethod = _input('InpMAMethod', MODE_SMMA)  # MA: Method
ExtSARBuffer = Arr(0, 0.0)
ExtMABuffer = Arr(0, 0.0)
ExtEPBuffer = Arr(0, 0.0)
ExtAFBuffer = Arr(0, 0.0)
ExtLastRevPos = 0
ExtDirectionLong = False
ExtSarStep = 0.0
ExtSarMaximum = 0.0
handle_iMA = 0  # variable for storing the handle of the iMA indicator
bars_calculated = 0

def OnInit():
    global ExtDirectionLong, ExtLastRevPos, ExtSarMaximum, ExtSarStep, handle_iMA
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
    SetIndexBuffer(0, ExtSARBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtMABuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtEPBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtAFBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetString(0, PLOT_LABEL, 'SAR(' + DoubleToString(ExtSarStep, 2) + ',' + DoubleToString(ExtSarMaximum, 2) + ')')
    ExtLastRevPos = 0
    ExtDirectionLong = False
    handle_iMA = iMA(Symbol(), Period(), InpMAPeriod, InpMAShift, InpMAMethod, PRICE_CLOSE)
    if handle_iMA == INVALID_HANDLE:
        PrintFormat('Failed to create handle of the iMA indicator for the symbol %s/%s, error code %d', Symbol(), EnumToString(Period(), ''), GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global ExtDirectionLong, ExtLastRevPos, bars_calculated
    if rates_total < 3:
        return 0
    values_to_copy = 0
    calculated = BarsCalculated(handle_iMA)
    if calculated <= 0:
        PrintFormat('BarsCalculated() returned %d, error code %d', calculated, GetLastError())
        return 0
    if (prev_calculated == 0 or calculated != bars_calculated) or rates_total > (prev_calculated + 1):
        if calculated > rates_total:
            values_to_copy = rates_total
        else:
            values_to_copy = calculated
    else:
        values_to_copy = rates_total - prev_calculated + 1
    if not FillArrayFromBuffer(ExtMABuffer, 0, handle_iMA, values_to_copy):
        return 0
    bars_calculated = calculated
    pos = rates_total - values_to_copy
    for i in range(pos, rates_total - 1):
        if i < 14:
            ExtAFBuffer[i] = ExtSarStep
            ExtSARBuffer[i] = ExtMABuffer[14]
            ExtLastRevPos = 0
            ExtDirectionLong = False
            ExtEPBuffer[i] = ExtMABuffer[14]
            continue
        high_curr = ExtMABuffer[i] + Point()
        low_curr = ExtMABuffer[i] - Point()
        high_prev = ExtMABuffer[i - 1] + Point()
        low_prev = ExtMABuffer[i - 1] - Point()
        if ExtDirectionLong:
            if ExtSARBuffer[i] > low_curr:
                ExtDirectionLong = False
                ExtSARBuffer[i] = GetHigh(i, ExtLastRevPos, ExtMABuffer)
                ExtEPBuffer[i] = low_curr
                ExtLastRevPos = i
                ExtAFBuffer[i] = ExtSarStep
        else:
            if ExtSARBuffer[i] < high_curr:
                ExtDirectionLong = True
                ExtSARBuffer[i] = GetLow(i, ExtLastRevPos, low)
                ExtEPBuffer[i] = high_curr
                ExtLastRevPos = i
                ExtAFBuffer[i] = ExtSarStep
        if ExtDirectionLong:
            if high_curr > ExtEPBuffer[i - 1] and i != ExtLastRevPos:
                ExtEPBuffer[i] = high_curr
                ExtAFBuffer[i] = ExtAFBuffer[i - 1] + ExtSarStep
                if ExtAFBuffer[i] > ExtSarMaximum:
                    ExtAFBuffer[i] = ExtSarMaximum
            else:
                if i != ExtLastRevPos:
                    ExtAFBuffer[i] = ExtAFBuffer[i - 1]
                    ExtEPBuffer[i] = ExtEPBuffer[i - 1]
            ExtSARBuffer[i + 1] = ExtSARBuffer[i] + (ExtAFBuffer[i] * (ExtEPBuffer[i] - ExtSARBuffer[i]))
            if ExtSARBuffer[i + 1] > low_curr or ExtSARBuffer[i + 1] > low_prev:
                ExtSARBuffer[i + 1] = MathMin(low_curr, low_prev)
        else:
            if low_curr < ExtEPBuffer[i - 1] and i != ExtLastRevPos:
                ExtEPBuffer[i] = low_curr
                ExtAFBuffer[i] = ExtAFBuffer[i - 1] + ExtSarStep
                if ExtAFBuffer[i] > ExtSarMaximum:
                    ExtAFBuffer[i] = ExtSarMaximum
            else:
                if i != ExtLastRevPos:
                    ExtAFBuffer[i] = ExtAFBuffer[i - 1]
                    ExtEPBuffer[i] = ExtEPBuffer[i - 1]
            ExtSARBuffer[i + 1] = ExtSARBuffer[i] + (ExtAFBuffer[i] * (ExtEPBuffer[i] - ExtSARBuffer[i]))
            if ExtSARBuffer[i + 1] < high_curr or ExtSARBuffer[i + 1] < high_prev:
                ExtSARBuffer[i + 1] = MathMax(high_curr, high_prev)
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

def FillArrayFromBuffer(values, shift, ind_handle, amount):
    ResetLastError()
    if CopyBuffer(ind_handle, 0, -shift, amount, values) < 0:
        PrintFormat('Failed to copy data from the iMA indicator, error code %d', GetLastError())
        return False
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SARIndexBasedOnMA(_MQL5Indicator):
    name = 'SAR index based on MA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpSARStep': 0.02,  # SAR: Step
        'InpSARMaximum': 0.04,  # SAR: Maximum
        'InpMAPeriod': 13,  # MA: Period
        'InpMAShift': 0,  # MA: Shift
        'InpMAMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),  # MA: Method
    }

