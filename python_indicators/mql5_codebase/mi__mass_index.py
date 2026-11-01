"""mi — converted from MQL5: MQL5 Indicators/Mass Index/mi.mq5

Mass Index
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [27.0, 26.5], 'description': ['Mass Index'], 'name': 'mi', 'source': 'MQL5 Indicators/Mass Index/mi.mq5', 'folder': 'Mass Index', 'inputs': [{'mql': 'InpPeriodEMA', 'py': 'InpPeriodEMA', 'param': 'InpPeriodEMA', 'type': 'int', 'default': 9, 'label': 'First EMA period', 'sinput': False}, {'mql': 'InpSecondPeriodEMA', 'py': 'InpSecondPeriodEMA', 'param': 'InpSecondPeriodEMA', 'type': 'int', 'default': 9, 'label': 'Second EMA period', 'sinput': False}, {'mql': 'InpSumPeriod', 'py': 'InpSumPeriod', 'param': 'InpSumPeriod', 'type': 'int', 'default': 25, 'label': 'Mass period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpPeriodEMA = _input('InpPeriodEMA', 9)  # First EMA period
InpSecondPeriodEMA = _input('InpSecondPeriodEMA', 9)  # Second EMA period
InpSumPeriod = _input('InpSumPeriod', 25)  # Mass period
ExtPeriodEMA = 0
ExtSecondPeriodEMA = 0
ExtSumPeriod = 0
ExtHLBuffer = Arr(0, 0.0)
ExtEHLBuffer = Arr(0, 0.0)
ExtEEHLBuffer = Arr(0, 0.0)
ExtMIBuffer = Arr(0, 0.0)

def OnInit():
    global ExtPeriodEMA, ExtSecondPeriodEMA, ExtSumPeriod
    if InpPeriodEMA <= 0:
        ExtPeriodEMA = 9
        printf('Incorrect value for input variable InpPeriodEMA=%d. Indicator will use value=%d for calculations.', InpPeriodEMA, ExtPeriodEMA)
    else:
        ExtPeriodEMA = InpPeriodEMA
    if InpSecondPeriodEMA <= 0:
        ExtSecondPeriodEMA = 9
        printf('Incorrect value for input variable InpSecondPeriodEMA=%d. Indicator will use value=%d for calculations.', InpSecondPeriodEMA, ExtSecondPeriodEMA)
    else:
        ExtSecondPeriodEMA = InpSecondPeriodEMA
    if InpSumPeriod <= 0:
        ExtSumPeriod = 25
        printf('Incorrect value for input variable PeriodSum=%d. Indicator will use value=%d for calculations.', InpSumPeriod, ExtSumPeriod)
    else:
        ExtSumPeriod = InpSumPeriod
    SetIndexBuffer(0, ExtMIBuffer)
    SetIndexBuffer(1, ExtEHLBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, ExtEEHLBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtHLBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Mass Index(' + _str(ExtPeriodEMA) + ',' + _str(ExtSecondPeriodEMA) + ',' + _str(ExtSumPeriod) + ')')
    PlotIndexSetString(0, PLOT_LABEL, 'MI(' + _str(ExtPeriodEMA) + ',' + _str(ExtSecondPeriodEMA) + ',' + _str(ExtSumPeriod) + ')')
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtPeriodEMA + ExtSecondPeriodEMA + ExtSumPeriod - 3)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    posMI = ExtSumPeriod + ExtPeriodEMA + ExtSecondPeriodEMA - 3
    if rates_total < posMI:
        return 0
    pos = prev_calculated - 1
    if pos < 1:
        ExtHLBuffer[0] = High[0] - Low[0]
        pos = 1
    for i in range(pos, rates_total):
        ExtHLBuffer[i] = High[i] - Low[i]
        ExtEHLBuffer[i] = ExponentialMA(i, ExtPeriodEMA, ExtEHLBuffer[i - 1], ExtHLBuffer)
        ExtEEHLBuffer[i] = ExponentialMA(i, ExtSecondPeriodEMA, ExtEEHLBuffer[i - 1], ExtEHLBuffer)
        dTmp = 0.0
        j = 0
        while j < ExtSumPeriod and i >= posMI:
            if ExtEEHLBuffer[i - j] != 0.0:
                dTmp += _fdiv(ExtEHLBuffer[i - j], ExtEEHLBuffer[i - j])
            j += 1
        ExtMIBuffer[i] = dTmp
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Mi(_MQL5Indicator):
    name = 'mi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodEMA': 9,  # First EMA period
        'InpSecondPeriodEMA': 9,  # Second EMA period
        'InpSumPeriod': 25,  # Mass period
    }

