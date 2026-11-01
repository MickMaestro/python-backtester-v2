"""iunima_mtf — converted from MQL5: MQL5 Indicators/Moving Averages, multi-timeframe [v03]/iunima_mtf.mq5

iUniMA, Multi-timeframe of version the Universal Moving Average
Copyright: 2010, traderak20@gmail.com; Version: V03

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2010, traderak20@gmail.com', 'version': 'V03', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'MA_TF2'}, 'levels': [], 'description': ['iUniMA, Multi-timeframe of version the Universal Moving Average'], 'name': 'iunima_mtf', 'source': 'MQL5 Indicators/Moving Averages, multi-timeframe [v03]/iunima_mtf.mq5', 'folder': 'Moving Averages, multi-timeframe [v03]', 'inputs': [{'mql': 'InpTimeFrame_2', 'py': 'InpTimeFrame_2', 'param': 'InpTimeFrame_2', 'type': 'int', 'default': 16385, 'label': 'Timeframe 2 (TF2) period', 'sinput': False}, {'mql': 'InpAppliedMA', 'py': 'InpAppliedMA', 'param': 'InpAppliedMA', 'type': 'int', 'default': 0, 'label': 'Applied MA method for signal line', 'sinput': False}, {'mql': 'InpMaPeriod', 'py': 'InpMaPeriod', 'param': 'InpMaPeriod', 'type': 'int', 'default': 14, 'label': 'MA Period', 'sinput': False}, {'mql': 'InpAmaFast', 'py': 'InpAmaFast', 'param': 'InpAmaFast', 'type': 'int', 'default': 2, 'label': 'Fast AMA period', 'sinput': False}, {'mql': 'InpAmaSlow', 'py': 'InpAmaSlow', 'param': 'InpAmaSlow', 'type': 'int', 'default': 30, 'label': 'Slow AMA period', 'sinput': False}, {'mql': 'InpCmoPeriod', 'py': 'InpCmoPeriod', 'param': 'InpCmoPeriod', 'type': 'int', 'default': 9, 'label': 'CMO period for VIDYA', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum maswitch
Simple = 0
Exponential = 1
Smoothed = 2
LinearWeighted = 3
AMA = 5
DEMA = 15
FRAMA = 20
TEMA = 34
VIDYA = 36
_enum('maswitch', {0: 'Simple', 1: 'Exponential', 2: 'Smoothed', 3: 'LinearWeighted', 5: 'AMA', 15: 'DEMA', 20: 'FRAMA', 34: 'TEMA', 36: 'VIDYA'})

# ---- inputs and global variables
InpTimeFrame_2 = _input('InpTimeFrame_2', PERIOD_H1)  # Timeframe 2 (TF2) period
InpAppliedMA = _input('InpAppliedMA', MODE_SMA)  # Applied MA method for signal line
InpMaPeriod = _input('InpMaPeriod', 14)  # MA Period
InpAmaFast = _input('InpAmaFast', 2)  # Fast AMA period
InpAmaSlow = _input('InpAmaSlow', 30)  # Slow AMA period
InpCmoPeriod = _input('InpCmoPeriod', 9)  # CMO period for VIDYA
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
ExtMaBuffer_TF2 = Arr(0, 0.0)
ExtMaArray_TF2 = Arr(0, 0.0)  # intermediate array to hold TF2 ma buffer values
PeriodRatio = 1  # ratio between timeframe 1 (TF1) and timeframe 2 (TF2)
PeriodSeconds_TF1 = 0  # TF1 period in seconds
PeriodSeconds_TF2 = 0  # TF2 period in seconds
ExtMaHandle_TF2 = 0  # ma handle TF2
ShowErrorMessages = True  # turn on/off error messages for debugging

def fNamePriceShort(aPrice):
    _sw1 = aPrice
    if _sw1 == PRICE_CLOSE:
        return 'C'
    elif _sw1 == PRICE_HIGH:
        return 'H'
    elif _sw1 == PRICE_LOW:
        return 'L'
    elif _sw1 == PRICE_MEDIAN:
        return 'M'
    elif _sw1 == PRICE_OPEN:
        return 'O'
    elif _sw1 == PRICE_TYPICAL:
        return 'T'
    elif _sw1 == PRICE_WEIGHTED:
        return 'W'
    else:
        return ''

def OnInit():
    global ExtMaHandle_TF2, PeriodRatio, PeriodSeconds_TF1, PeriodSeconds_TF2
    SetIndexBuffer(0, ExtMaBuffer_TF2, INDICATOR_DATA)
    ArraySetAsSeries(ExtMaBuffer_TF2, True)
    ArraySetAsSeries(ExtMaArray_TF2, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() - 1)
    PeriodSeconds_TF1 = PeriodSeconds()
    PeriodSeconds_TF2 = PeriodSeconds(InpTimeFrame_2)
    if PeriodSeconds_TF1 < PeriodSeconds_TF2:
        PeriodRatio = _idiv(PeriodSeconds_TF2, PeriodSeconds_TF1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MA(' + _str(InpMaPeriod) + ')')
    Label = ""
    _sw2 = InpAppliedMA
    if _sw2 == Simple:
        Label = 'SMA(' + _str(InpMaPeriod) + ',' + fNamePriceShort(InpAppliedPrice) + ')'
    elif _sw2 == Exponential:
        Label = 'EMA(' + _str(InpMaPeriod) + ',' + fNamePriceShort(InpAppliedPrice) + ')'
    elif _sw2 == Smoothed:
        Label = 'SMMA(' + _str(InpMaPeriod) + ',' + fNamePriceShort(InpAppliedPrice) + ')'
    elif _sw2 == LinearWeighted:
        Label = 'LWMA(' + _str(InpMaPeriod) + ',' + fNamePriceShort(InpAppliedPrice) + ')'
    elif _sw2 == AMA:
        Label = 'AMA(' + _str(InpMaPeriod) + ',' + _str(InpAmaFast) + ',' + _str(InpAmaSlow) + ',' + fNamePriceShort(InpAppliedPrice) + ')'
    elif _sw2 == DEMA:
        Label = 'DEMA(' + _str(InpMaPeriod) + ',' + fNamePriceShort(InpAppliedPrice) + ')'
    elif _sw2 == FRAMA:
        Label = 'FRAM(' + _str(InpMaPeriod) + ',' + fNamePriceShort(InpAppliedPrice) + ')'
    elif _sw2 == TEMA:
        Label = 'TEMA(' + _str(InpMaPeriod) + ',' + fNamePriceShort(InpAppliedPrice) + ')'
    elif _sw2 == VIDYA:
        Label = 'VIDYA(' + _str(InpMaPeriod) + ',' + _str(InpCmoPeriod) + ',' + fNamePriceShort(InpAppliedPrice) + ')'
    PlotIndexSetString(0, PLOT_LABEL, Label)
    _sw3 = InpAppliedMA
    if _sw3 == Simple:
        ExtMaHandle_TF2 = iMA(None, InpTimeFrame_2, InpMaPeriod, 0, MODE_SMA, InpAppliedPrice)
    elif _sw3 == Exponential:
        ExtMaHandle_TF2 = iMA(None, InpTimeFrame_2, InpMaPeriod, 0, MODE_EMA, InpAppliedPrice)
    elif _sw3 == Smoothed:
        ExtMaHandle_TF2 = iMA(None, InpTimeFrame_2, InpMaPeriod, 0, MODE_SMMA, InpAppliedPrice)
    elif _sw3 == LinearWeighted:
        ExtMaHandle_TF2 = iMA(None, InpTimeFrame_2, InpMaPeriod, 0, MODE_LWMA, InpAppliedPrice)
    elif _sw3 == AMA:
        ExtMaHandle_TF2 = iAMA(None, InpTimeFrame_2, InpMaPeriod, InpAmaFast, InpAmaSlow, 0, InpAppliedPrice)
    elif _sw3 == DEMA:
        ExtMaHandle_TF2 = iDEMA(None, InpTimeFrame_2, InpMaPeriod, 0, InpAppliedPrice)
    elif _sw3 == FRAMA:
        ExtMaHandle_TF2 = iFrAMA(None, InpTimeFrame_2, InpMaPeriod, 0, InpAppliedPrice)
    elif _sw3 == TEMA:
        ExtMaHandle_TF2 = iTEMA(None, InpTimeFrame_2, InpMaPeriod, 0, InpAppliedPrice)
    elif _sw3 == VIDYA:
        ExtMaHandle_TF2 = iVIDyA(None, InpTimeFrame_2, InpCmoPeriod, InpMaPeriod, 0, InpAppliedPrice)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    ArraySetAsSeries(Time, True)
    bars_TF2 = Bars(None, InpTimeFrame_2)
    if bars_TF2 < InpMaPeriod:
        return 0
    calculated_TF2 = 0
    calculated_TF2 = BarsCalculated(ExtMaHandle_TF2)
    if calculated_TF2 < bars_TF2:
        if ShowErrorMessages:
            Print('Not all data of ExtMaHandle_TF2 has been calculated (', calculated_TF2, ' bars). Error', GetLastError())
        return 0
    limit = 0
    if (prev_calculated == 0 or prev_calculated < 0) or prev_calculated > rates_total:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    convertedTime = 0
    for i in range(limit, 0 - 1, -1):
        if InpAppliedPrice != PRICE_OPEN:
            convertedTime = Time[i] + PeriodSeconds_TF1 - PeriodSeconds_TF2
        if InpAppliedPrice == PRICE_OPEN:
            convertedTime = Time[i]
        tempTimeArray_TF2 = Arr(0, 0)
        CopyTime(None, InpTimeFrame_2, calculated_TF2 - 1, 1, tempTimeArray_TF2)
        if convertedTime < tempTimeArray_TF2[0]:
            ExtMaBuffer_TF2[i] = EMPTY_VALUE
            continue
        if CopyBuffer(ExtMaHandle_TF2, 0, _DT(convertedTime), 1, ExtMaArray_TF2) <= 0:
            if ShowErrorMessages:
                Print('Getting MA TF2 failed! Error', GetLastError())
            return 0
        else:
            ExtMaBuffer_TF2[i] = ExtMaArray_TF2[0]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IunimaMtf(_MQL5Indicator):
    name = 'iunima_mtf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpTimeFrame_2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # Timeframe 2 (TF2) period
        'InpAppliedMA': _Choice({0: 'Simple', 1: 'Exponential', 2: 'Smoothed', 3: 'LinearWeighted', 5: 'AMA', 15: 'DEMA', 20: 'FRAMA', 34: 'TEMA', 36: 'VIDYA'}, default=0),  # Applied MA method for signal line
        'InpMaPeriod': 14,  # MA Period
        'InpAmaFast': 2,  # Fast AMA period
        'InpAmaSlow': 30,  # Slow AMA period
        'InpCmoPeriod': 9,  # CMO period for VIDYA
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

