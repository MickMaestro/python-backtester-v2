"""rsi_mtf — converted from MQL5: MQL5 Indicators/RSI multi-timeframe [v03]/rsi_mtf.mq5

RSI, Multi-timeframe
Copyright: 2010, traderak20@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2010, traderak20@gmail.com', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'RSI_TF2'}, 'levels': [], 'description': ['RSI, Multi-timeframe'], 'name': 'rsi_mtf', 'source': 'MQL5 Indicators/RSI multi-timeframe [v03]/rsi_mtf.mq5', 'folder': 'RSI multi-timeframe [v03]', 'inputs': [{'mql': 'InpTimeFrame_2', 'py': 'InpTimeFrame_2', 'param': 'InpTimeFrame_2', 'type': 'int', 'default': 16385, 'label': 'Timeframe 2 (TF2) period', 'sinput': False}, {'mql': 'InpPeriodRSI', 'py': 'InpPeriodRSI', 'param': 'InpPeriodRSI', 'type': 'int', 'default': 14, 'label': 'RSI period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpTimeFrame_2 = _input('InpTimeFrame_2', PERIOD_H1)  # Timeframe 2 (TF2) period
InpPeriodRSI = _input('InpPeriodRSI', 14)  # RSI period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
ExtRsiBuffer_TF2 = Arr(0, 0.0)
ExtRsiArray_TF2 = Arr(0, 0.0)  # intermediate array to hold TF2 RSI buffer values
PeriodRatio = 1  # ratio between timeframe 1 (TF1) and timeframe 2 (TF2)
PeriodSeconds_TF1 = 0  # TF1 period in seconds
PeriodSeconds_TF2 = 0  # TF2 period in seconds
ExtRsiHandle_TF2 = 0  # RSI handle TF2
ShowErrorMessages = True  # turn on/off error messages for debugging

def OnInit():
    global ExtRsiHandle_TF2, PeriodRatio, PeriodSeconds_TF1, PeriodSeconds_TF2
    SetIndexBuffer(0, ExtRsiBuffer_TF2, INDICATOR_DATA)
    ArraySetAsSeries(ExtRsiBuffer_TF2, True)
    ArraySetAsSeries(ExtRsiArray_TF2, True)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 30)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 70)
    IndicatorSetDouble(INDICATOR_MINIMUM, 0)
    IndicatorSetDouble(INDICATOR_MAXIMUM, 100)
    PeriodSeconds_TF1 = PeriodSeconds()
    PeriodSeconds_TF2 = PeriodSeconds(InpTimeFrame_2)
    if PeriodSeconds_TF1 < PeriodSeconds_TF2:
        PeriodRatio = _idiv(PeriodSeconds_TF2, PeriodSeconds_TF1)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSI(' + _str(InpPeriodRSI) + ')')
    ExtRsiHandle_TF2 = iRSI(None, InpTimeFrame_2, InpPeriodRSI, InpAppliedPrice)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    ArraySetAsSeries(Time, True)
    bars_TF2 = Bars(None, InpTimeFrame_2)
    if bars_TF2 < InpPeriodRSI:
        return 0
    calculated_TF2 = 0
    calculated_TF2 = BarsCalculated(ExtRsiHandle_TF2)
    if calculated_TF2 < bars_TF2:
        if ShowErrorMessages:
            Print('Not all data of ExtRsiHandle_TF2 has been calculated (', calculated_TF2, ' bars). Error', GetLastError())
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
            ExtRsiBuffer_TF2[i] = EMPTY_VALUE
            continue
        if CopyBuffer(ExtRsiHandle_TF2, 0, _DT(convertedTime), 1, ExtRsiArray_TF2) <= 0:
            if ShowErrorMessages:
                Print('Getting RSI TF2 failed! Error', GetLastError())
            return 0
        else:
            ExtRsiBuffer_TF2[i] = ExtRsiArray_TF2[0]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RsiMtf(_MQL5Indicator):
    name = 'rsi_mtf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpTimeFrame_2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # Timeframe 2 (TF2) period
        'InpPeriodRSI': 14,  # RSI period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
    }

