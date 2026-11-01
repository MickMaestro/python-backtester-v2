"""chv — converted from MQL5: MQL5 Indicators/Chaikin Volatility (CHV)/chv.mq5

Chaikin Volatility
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Chaikin Volatility'], 'name': 'chv', 'source': 'MQL5 Indicators/Chaikin Volatility (CHV)/chv.mq5', 'folder': 'Chaikin Volatility (CHV)', 'inputs': [{'mql': 'InpSmoothPeriod', 'py': 'InpSmoothPeriod', 'param': 'InpSmoothPeriod', 'type': 'int', 'default': 10, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'InpCHVPeriod', 'py': 'InpCHVPeriod', 'param': 'InpCHVPeriod', 'type': 'int', 'default': 10, 'label': 'CHV period', 'sinput': False}, {'mql': 'InpSmoothType', 'py': 'InpSmoothType', 'param': 'InpSmoothType', 'type': 'int', 'default': 1, 'label': 'Smoothing method', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum SmoothMethod
SMA = 0
EMA = 1
_enum('SmoothMethod', {0: 'SMA', 1: 'EMA'})

# ---- inputs and global variables
InpSmoothPeriod = _input('InpSmoothPeriod', 10)  # Smoothing period
InpCHVPeriod = _input('InpCHVPeriod', 10)  # CHV period
InpSmoothType = _input('InpSmoothType', EMA)  # Smoothing method
ExtCHVBuffer = Arr(0, 0.0)
ExtHLBuffer = Arr(0, 0.0)
ExtSHLBuffer = Arr(0, 0.0)
ExtSmoothPeriod = 0
ExtCHVPeriod = 0

def OnInit():
    global ExtCHVPeriod, ExtSmoothPeriod
    MAName = ""
    if InpSmoothType == SMA:
        MAName = 'SMA'
    else:
        MAName = 'EMA'
    if InpSmoothPeriod <= 0:
        ExtSmoothPeriod = 10
        printf('Incorrect value for input variable InpSmoothPeriod=%d. Indicator will use value=%d for calculations.', InpSmoothPeriod, ExtSmoothPeriod)
    else:
        ExtSmoothPeriod = InpSmoothPeriod
    if InpCHVPeriod <= 0:
        ExtCHVPeriod = 10
        printf('Incorrect value for input variable InpCHVPeriod=%d. Indicator will use value=%d for calculations.', InpCHVPeriod, ExtCHVPeriod)
    else:
        ExtCHVPeriod = InpCHVPeriod
    SetIndexBuffer(0, ExtCHVBuffer)
    SetIndexBuffer(1, ExtHLBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, ExtSHLBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtSmoothPeriod + ExtCHVPeriod - 1)
    PlotIndexSetString(0, PLOT_LABEL, 'CHV(' + _str(ExtSmoothPeriod) + ',' + MAName + ')')
    IndicatorSetString(INDICATOR_SHORTNAME, 'Chaikin Volatility(' + _str(ExtSmoothPeriod) + ',' + MAName + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 1)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    pos = 0
    posCHV = 0
    posCHV = ExtCHVPeriod + ExtSmoothPeriod - 2
    if rates_total < posCHV:
        return 0
    if prev_calculated < 1:
        pos = 0
    else:
        pos = prev_calculated - 1
    i = pos
    for i in range(i, rates_total):
        ExtHLBuffer[i] = High[i] - Low[i]
    else:
        i = _range_end(i, rates_total, 1)
    if pos < (ExtSmoothPeriod - 1):
        pos = ExtSmoothPeriod - 1
        i = 0
        for i in range(i, pos):
            ExtSHLBuffer[i] = 0.0
        else:
            i = _range_end(i, pos, 1)
    if InpSmoothType == SMA:
        SimpleMAOnBuffer(rates_total, prev_calculated, 0, ExtSmoothPeriod, ExtHLBuffer, ExtSHLBuffer)
    else:
        ExponentialMAOnBuffer(rates_total, prev_calculated, 0, ExtSmoothPeriod, ExtHLBuffer, ExtSHLBuffer)
    if pos < posCHV:
        pos = posCHV
    i = pos
    for i in range(i, rates_total):
        if ExtSHLBuffer[i - ExtCHVPeriod] != 0.0:
            ExtCHVBuffer[i] = _fdiv(100.0 * (ExtSHLBuffer[i] - ExtSHLBuffer[i - ExtCHVPeriod]), ExtSHLBuffer[i - ExtCHVPeriod])
        else:
            ExtCHVBuffer[i] = 0.0
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Chv(_MQL5Indicator):
    name = 'chv'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpSmoothPeriod': 10,  # Smoothing period
        'InpCHVPeriod': 10,  # CHV period
        'InpSmoothType': _Choice({0: 'Simple MA', 1: 'Exponential MA'}, default=1),  # Smoothing method
    }

