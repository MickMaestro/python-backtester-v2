"""ad — converted from MQL5: MQL5 Indicators/Accumulation_Distribution/ad.mq5

Accumulation/Distribution
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [11186720]}, 'widths': {}, 'styles': {}, 'labels': {1: 'A/D'}, 'levels': [], 'description': ['Accumulation/Distribution'], 'name': 'ad', 'source': 'MQL5 Indicators/Accumulation_Distribution/ad.mq5', 'folder': 'Accumulation_Distribution', 'inputs': [{'mql': 'InpVolumeType', 'py': 'InpVolumeType', 'param': 'InpVolumeType', 'type': 'int', 'default': 0, 'label': 'Volume type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpVolumeType = _input('InpVolumeType', VOLUME_TICK)  # Volume type
ExtADbuffer = Arr(0, 0.0)

def OnInit():
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'A/D')
    SetIndexBuffer(0, ExtADbuffer)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 1)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    if rates_total < 2:
        return 0
    pos = prev_calculated - 1
    if pos < 0:
        pos = 0
    if InpVolumeType == VOLUME_TICK:
        Calculate(rates_total, pos, High, Low, Close, TickVolume)
    else:
        Calculate(rates_total, pos, High, Low, Close, Volume)
    return rates_total

def Calculate(rates_total, pos, High, Low, Close, Volume):
    hi = 0.0
    lo = 0.0
    cl = 0.0
    for i in range(pos, rates_total):
        hi = High[i]
        lo = Low[i]
        cl = Close[i]
        sum_ = cl - lo - (hi - cl)
        if hi == lo:
            sum_ = 0.0
        else:
            sum_ = _fdiv(sum_, hi - lo) * Volume[i]
        if i > 0:
            sum_ += ExtADbuffer[i - 1]
        ExtADbuffer[i] = sum_


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ad(_MQL5Indicator):
    name = 'ad'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpVolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volume type
    }

