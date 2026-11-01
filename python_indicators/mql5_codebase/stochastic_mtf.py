"""stochastic_mtf — converted from MQL5: MQL5 Indicators/Stochastic multi-timeframe [v04]/stochastic_mtf.mq5

Stochastic, Multi-timeframe
Copyright: 2010, traderak20@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2010, traderak20@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [11186720], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Main_TF2', 2: 'Signal_TF2'}, 'levels': [], 'description': ['Stochastic, Multi-timeframe'], 'name': 'stochastic_mtf', 'source': 'MQL5 Indicators/Stochastic multi-timeframe [v04]/stochastic_mtf.mq5', 'folder': 'Stochastic multi-timeframe [v04]', 'inputs': [{'mql': 'InpTimeFrame_2', 'py': 'InpTimeFrame_2', 'param': 'InpTimeFrame_2', 'type': 'int', 'default': 16385, 'label': 'Timeframe 2 (TF2) period', 'sinput': False}, {'mql': 'InpKPeriod', 'py': 'InpKPeriod', 'param': 'InpKPeriod', 'type': 'int', 'default': 5, 'label': 'K period', 'sinput': False}, {'mql': 'InpDPeriod', 'py': 'InpDPeriod', 'param': 'InpDPeriod', 'type': 'int', 'default': 3, 'label': 'D period', 'sinput': False}, {'mql': 'InpSlowing', 'py': 'InpSlowing', 'param': 'InpSlowing', 'type': 'int', 'default': 3, 'label': 'Slowing', 'sinput': False}, {'mql': 'InpAppliedMA', 'py': 'InpAppliedMA', 'param': 'InpAppliedMA', 'type': 'int', 'default': 0, 'label': 'Applied MA method for signal line', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 0, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpTimeFrame_2 = _input('InpTimeFrame_2', PERIOD_H1)  # Timeframe 2 (TF2) period
InpKPeriod = _input('InpKPeriod', 5)  # K period
InpDPeriod = _input('InpDPeriod', 3)  # D period
InpSlowing = _input('InpSlowing', 3)  # Slowing
InpAppliedMA = _input('InpAppliedMA', MODE_SMA)  # Applied MA method for signal line
InpAppliedPrice = _input('InpAppliedPrice', STO_LOWHIGH)  # Applied price
ExtMainBuffer_TF2 = Arr(0, 0.0)
ExtSignalBuffer_TF2 = Arr(0, 0.0)
ExtMainArray_TF2 = Arr(0, 0.0)  # intermediate array to hold TF2 main buffer values
ExtSignalArray_TF2 = Arr(0, 0.0)  # intermediate array to hold TF2 signal buffer values
PeriodRatio = 1  # ratio between timeframe 1 (TF1) and timeframe 2 (TF2)
PeriodSeconds_TF1 = 0  # TF1 period in seconds
PeriodSeconds_TF2 = 0  # TF2 period in seconds
ExtStochasticHandle_TF2 = 0  # stochastic handle TF2
ShowErrorMessages = True  # turn on/off error messages for debugging

def OnInit():
    global ExtStochasticHandle_TF2, PeriodRatio, PeriodSeconds_TF1, PeriodSeconds_TF2
    SetIndexBuffer(0, ExtMainBuffer_TF2, INDICATOR_DATA)
    SetIndexBuffer(1, ExtSignalBuffer_TF2, INDICATOR_DATA)
    ArraySetAsSeries(ExtMainBuffer_TF2, True)
    ArraySetAsSeries(ExtSignalBuffer_TF2, True)
    ArraySetAsSeries(ExtMainArray_TF2, True)
    ArraySetAsSeries(ExtSignalArray_TF2, True)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 20)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 80)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 100)
    PeriodSeconds_TF1 = PeriodSeconds()
    PeriodSeconds_TF2 = PeriodSeconds(InpTimeFrame_2)
    if PeriodSeconds_TF1 < PeriodSeconds_TF2:
        PeriodRatio = _idiv(PeriodSeconds_TF2, PeriodSeconds_TF1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Stoch(' + _str(InpKPeriod) + ',' + _str(InpDPeriod) + ',' + _str(InpSlowing) + ')')
    ExtStochasticHandle_TF2 = iStochastic(None, InpTimeFrame_2, InpKPeriod, InpDPeriod, InpSlowing, InpAppliedMA, InpAppliedPrice)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    ArraySetAsSeries(Time, True)
    bars_TF2 = Bars(None, InpTimeFrame_2)
    if bars_TF2 < (InpKPeriod + InpDPeriod + InpSlowing):
        return 0
    calculated_TF2 = 0
    calculated_TF2 = BarsCalculated(ExtStochasticHandle_TF2)
    if calculated_TF2 < bars_TF2:
        if ShowErrorMessages:
            Print('Not all data of ExtStochasticHandle_TF2 has been calculated (', calculated_TF2, ' bars). Error', GetLastError())
        return 0
    limit = 0
    if (prev_calculated == 0 or prev_calculated < 0) or prev_calculated > rates_total:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    convertedTime = 0
    for i in range(limit, 0 - 1, -1):
        convertedTime = Time[i] + PeriodSeconds_TF1 - PeriodSeconds_TF2
        tempTimeArray_TF2 = Arr(0, 0)
        CopyTime(None, InpTimeFrame_2, calculated_TF2 - 1, 1, tempTimeArray_TF2)
        if convertedTime < tempTimeArray_TF2[0]:
            ExtMainBuffer_TF2[i] = EMPTY_VALUE
            ExtSignalBuffer_TF2[i] = EMPTY_VALUE
            continue
        if CopyBuffer(ExtStochasticHandle_TF2, 0, _DT(convertedTime), 1, ExtMainArray_TF2) <= 0:
            if ShowErrorMessages:
                Print('Getting Stochastic TF2 failed! Error', GetLastError())
            return 0
        else:
            ExtMainBuffer_TF2[i] = ExtMainArray_TF2[0]
        if CopyBuffer(ExtStochasticHandle_TF2, 1, _DT(convertedTime), 1, ExtSignalArray_TF2) <= 0:
            if ShowErrorMessages:
                Print('Getting Signal TF2 failed! Error', GetLastError())
            return 0
        else:
            ExtSignalBuffer_TF2[i] = ExtSignalArray_TF2[0]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class StochasticMtf(_MQL5Indicator):
    name = 'stochastic_mtf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpTimeFrame_2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # Timeframe 2 (TF2) period
        'InpKPeriod': 5,  # K period
        'InpDPeriod': 3,  # D period
        'InpSlowing': 3,  # Slowing
        'InpAppliedMA': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # Applied MA method for signal line
        'InpAppliedPrice': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Applied price
    }

