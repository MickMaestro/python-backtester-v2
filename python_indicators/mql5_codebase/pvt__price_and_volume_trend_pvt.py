"""pvt — converted from MQL5: MQL5 Indicators/Price and Volume Trend (PVT)/pvt.mq5

Price and Volume Trend
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Price and Volume Trend'], 'name': 'pvt', 'source': 'MQL5 Indicators/Price and Volume Trend (PVT)/pvt.mq5', 'folder': 'Price and Volume Trend (PVT)', 'inputs': [{'mql': 'InpVolumeType', 'py': 'InpVolumeType', 'param': 'InpVolumeType', 'type': 'int', 'default': 0, 'label': 'Volumes', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpVolumeType = _input('InpVolumeType', VOLUME_TICK)  # Volumes
ExtPVTBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtPVTBuffer)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'PVT')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 1)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    pos = 0
    if rates_total < 2:
        return 0
    pos = prev_calculated - 1
    if pos < 0:
        pos = 1
        ExtPVTBuffer[0] = 0.0
    if InpVolumeType == VOLUME_TICK:
        CalculatePVT(pos, rates_total, Close, TickVolume)
    else:
        CalculatePVT(pos, rates_total, Close, Volume)
    return rates_total

def CalculatePVT(nPosition, nRatesCount, ClBuffer, VolBuffer):
    if nPosition <= 0:
        nPosition = 1
    for i in range(nPosition, nRatesCount):
        PrevClose = ClBuffer[i - 1]
        if PrevClose != 0:
            ExtPVTBuffer[i] = (_fdiv(ClBuffer[i] - PrevClose, PrevClose) * VolBuffer[i]) + ExtPVTBuffer[i - 1]
        else:
            ExtPVTBuffer[i] = ExtPVTBuffer[i - 1]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Pvt(_MQL5Indicator):
    name = 'pvt'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpVolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volumes
    }

