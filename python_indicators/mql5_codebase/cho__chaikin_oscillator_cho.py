"""cho — converted from MQL5: MQL5 Indicators/Chaikin Oscillator (CHO)/cho.mq5

Chaikin Oscillator
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [11186720]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Chaikin Oscillator'], 'name': 'cho', 'source': 'MQL5 Indicators/Chaikin Oscillator (CHO)/cho.mq5', 'folder': 'Chaikin Oscillator (CHO)', 'inputs': [{'mql': 'InpFastMA', 'py': 'InpFastMA', 'param': 'InpFastMA', 'type': 'int', 'default': 3, 'label': 'Fast MA period', 'sinput': False}, {'mql': 'InpSlowMA', 'py': 'InpSlowMA', 'param': 'InpSlowMA', 'type': 'int', 'default': 10, 'label': 'Slow MA period', 'sinput': False}, {'mql': 'InpSmoothMethod', 'py': 'InpSmoothMethod', 'param': 'InpSmoothMethod', 'type': 'int', 'default': 1, 'label': 'MA method', 'sinput': False}, {'mql': 'InpVolumeType', 'py': 'InpVolumeType', 'param': 'InpVolumeType', 'type': 'int', 'default': 0, 'label': 'Volumes', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpFastMA = _input('InpFastMA', 3)  # Fast MA period
InpSlowMA = _input('InpSlowMA', 10)  # Slow MA period
InpSmoothMethod = _input('InpSmoothMethod', MODE_EMA)  # MA method
InpVolumeType = _input('InpVolumeType', VOLUME_TICK)  # Volumes
ExtCHOBuffer = Arr(0, 0.0)
ExtFastEMABuffer = Arr(0, 0.0)
ExtSlowEMABuffer = Arr(0, 0.0)
ExtADBuffer = Arr(0, 0.0)
weightfast = 0
weightslow = 0

def OnInit():
    SetIndexBuffer(0, ExtCHOBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtFastEMABuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(2, ExtSlowEMABuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, ExtADBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, InpSlowMA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'CHO(' + _str(InpSlowMA) + ',' + _str(InpFastMA) + ')')

def AD(high, low, close, volume):
    res = 0.0
    if high != low:
        res = _fdiv((2 * close) - high - low, high - low) * volume
    return res

def AverageOnArray(mode, rates_total, prev_calculated, begin, period, source, destination, weightsum):
    _sw1 = mode
    if _sw1 == MODE_EMA:
        ExponentialMAOnBuffer(rates_total, prev_calculated, begin, period, source, destination)
    elif _sw1 == MODE_SMMA:
        SmoothedMAOnBuffer(rates_total, prev_calculated, begin, period, source, destination)
    elif _sw1 == MODE_LWMA:
        LinearWeightedMAOnBuffer_2(rates_total, prev_calculated, begin, period, source, destination, weightsum)
    else:
        SimpleMAOnBuffer(rates_total, prev_calculated, begin, period, source, destination)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    i = 0
    limit = 0
    if rates_total < InpSlowMA:
        return 0
    if prev_calculated < 1:
        limit = 1
        if InpVolumeType == VOLUME_TICK:
            ExtADBuffer[0] = AD(High[0], Low[0], Close[0], TickVolume[0])
        else:
            ExtADBuffer[0] = AD(High[0], Low[0], Close[0], Volume[0])
        ExtSlowEMABuffer[0] = ExtADBuffer[0]
        ExtFastEMABuffer[0] = ExtADBuffer[0]
    else:
        limit = prev_calculated - 1
    if InpVolumeType == VOLUME_TICK:
        i = limit
        for i in range(i, rates_total):
            ExtADBuffer[i] = ExtADBuffer[i - 1] + AD(High[i], Low[i], Close[i], TickVolume[i])
        else:
            i = _range_end(i, rates_total, 1)
    else:
        i = limit
        for i in range(i, rates_total):
            ExtADBuffer[i] = ExtADBuffer[i - 1] + AD(High[i], Low[i], Close[i], Volume[i])
        else:
            i = _range_end(i, rates_total, 1)
    AverageOnArray(InpSmoothMethod, rates_total, prev_calculated, 0, InpSlowMA, ExtADBuffer, ExtSlowEMABuffer, _GlobRef(globals(), 'weightslow'))
    AverageOnArray(InpSmoothMethod, rates_total, prev_calculated, 0, InpFastMA, ExtADBuffer, ExtFastEMABuffer, _GlobRef(globals(), 'weightfast'))
    i = limit
    for i in range(i, rates_total):
        ExtCHOBuffer[i] = ExtFastEMABuffer[i] - ExtSlowEMABuffer[i]
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Cho(_MQL5Indicator):
    name = 'cho'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpFastMA': 3,  # Fast MA period
        'InpSlowMA': 10,  # Slow MA period
        'InpSmoothMethod': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # MA method
        'InpVolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volumes
    }

