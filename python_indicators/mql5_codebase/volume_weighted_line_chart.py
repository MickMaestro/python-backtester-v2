"""Volume-weighted line chart — converted from MQL5: MQL5 Indicators/Volume weighted line chart with smoothing/Volume-weighted line chart.mq5


Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 5, 3: 5}, 'colors': {1: [16748574], 2: [15453831], 3: [255]}, 'widths': {1: 2, 2: 1, 3: 1}, 'styles': {}, 'labels': {1: 'VW Line Chart', 2: 'Bulls', 3: 'Bears'}, 'levels': [], 'description': [], 'name': 'Volume-weighted line chart', 'source': 'MQL5 Indicators/Volume weighted line chart with smoothing/Volume-weighted line chart.mq5', 'folder': 'Volume weighted line chart with smoothing', 'inputs': [{'mql': 'SmoothingPeriod', 'py': 'SmoothingPeriod', 'param': 'SmoothingPeriod', 'type': 'int', 'default': 3, 'label': 'Smoothing period', 'sinput': False}, {'mql': 'SmoothingFactor', 'py': 'SmoothingFactor', 'param': 'SmoothingFactor', 'type': 'double', 'default': 2.0, 'label': 'Smoothing factor', 'sinput': False}, {'mql': 'VolumeOption', 'py': 'VolumeOption', 'param': 'VolumeOption', 'type': 'int', 'default': 0, 'label': 'Volume type', 'sinput': False}, {'mql': 'drawDots', 'py': 'drawDots', 'param': 'drawDots', 'type': 'bool', 'default': False, 'label': 'Draw bull and bear indicator arrows', 'sinput': False}, {'mql': 'UseDynamicSmoothing', 'py': 'UseDynamicSmoothing', 'param': 'UseDynamicSmoothing', 'type': 'bool', 'default': True, 'label': 'Use dynamic smoothing factor', 'sinput': False}, {'mql': 'ATRPeriod', 'py': 'ATRPeriod', 'param': 'ATRPeriod', 'type': 'int', 'default': 14, 'label': 'ATR period for dynamic smoothing factor', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum VolumeType
Tick_Volume = 0
Real_Volume = 1
_enum('VolumeType', {0: 'Tick_Volume', 1: 'Real_Volume'})

# ---- inputs and global variables
SmoothingPeriod = _input('SmoothingPeriod', 3)  # Smoothing period
SmoothingFactor = _input('SmoothingFactor', 2.0)  # Smoothing factor
VolumeOption = _input('VolumeOption', Tick_Volume)  # Volume type
drawDots = _input('drawDots', False)  # Draw bull and bear indicator arrows
UseDynamicSmoothing = _input('UseDynamicSmoothing', True)  # Use dynamic smoothing factor
ATRPeriod = _input('ATRPeriod', 14)  # ATR period for dynamic smoothing factor
MaxSmoothingFactor = 5.0  # Maximum smoothing factor
MinSmoothingFactor = 2.0  # Minimum smoothing factor
smoothingFactor = 0.0
VWLineBuffer = Arr(0, 0.0)
atr_buf = Arr(0, 0.0)
Bulls = Arr(0, 0.0)
Bears = Arr(0, 0.0)
atr_handle = INVALID_HANDLE

def OnInit():
    global atr_handle
    SetIndexBuffer(0, VWLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, Bulls, INDICATOR_DATA)
    SetIndexBuffer(2, Bears, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_ARROW, 108)
    PlotIndexSetInteger(2, PLOT_ARROW, 108)
    atr_handle = iATR(Symbol(), 0, ATRPeriod)
    ArraySetAsSeries(atr_buf, True)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global smoothingFactor
    start = ((prev_calculated - 1) if (prev_calculated > 0) else SmoothingPeriod)
    if CopyBuffer(atr_handle, 0, 0, 1, atr_buf) < 0:
        Print('Failed to copy ATR values!')
        return 0
    atr = atr_buf[0]
    if UseDynamicSmoothing:
        smoothingFactor = MinSmoothingFactor + ((MaxSmoothingFactor - MinSmoothingFactor) * _fdiv(atr, close[rates_total - 1]))
    else:
        smoothingFactor = SmoothingFactor
    alpha = smoothingFactor / (SmoothingPeriod + 1)
    for i in range(start, rates_total):
        vwPrice = 0.0
        totalVolume = 0.0
        for j in range(i - SmoothingPeriod + 1, i + 1):
            if j < 0:
                continue
            currentVolume = (float(tick_volume[j]) if (VolumeOption == Tick_Volume) else float(volume[j]))
            vwPrice += close[j] * currentVolume
            totalVolume += currentVolume
        if totalVolume != 0:
            vwPrice = _fdiv(vwPrice, totalVolume)
        if i == start:
            VWLineBuffer[i] = vwPrice
        else:
            VWLineBuffer[i] = VWLineBuffer[i - 1] + (alpha * (vwPrice - VWLineBuffer[i - 1]))
        if drawDots:
            if VWLineBuffer[i] > VWLineBuffer[i - 1]:
                Bulls[i] = VWLineBuffer[i]
            else:
                Bulls[i] = EMPTY_VALUE
            if VWLineBuffer[i] < VWLineBuffer[i - 1]:
                Bears[i] = VWLineBuffer[i]
            else:
                Bears[i] = EMPTY_VALUE
        else:
            Bulls[i] = EMPTY_VALUE
            Bears[i] = EMPTY_VALUE
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolumeWeightedLineChart(_MQL5Indicator):
    name = 'Volume-weighted line chart'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'SmoothingPeriod': 3,  # Smoothing period
        'SmoothingFactor': 2.0,  # Smoothing factor
        'VolumeOption': _Choice({0: 'Tick volume', 1: 'Real volume (only for stocks and futures)'}, default=0),  # Volume type
        'drawDots': False,  # Draw bull and bear indicator arrows
        'UseDynamicSmoothing': True,  # Use dynamic smoothing factor
        'ATRPeriod': 14,  # ATR period for dynamic smoothing factor
    }

