"""vsi — converted from MQL5: MQL5 Indicators/VSI/vsi.mq5

Indicator that calculates volume per second (or period) and the corresponding MA.
Uses volume per second since it will be uniform for all chart periods.
Indicator seems to work best on 15m to 4h charts. IMHO, 1m and 5m periods are
too short for valid results and 1d+ will show low periods for partial days on MT4.
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711935], 2: [16711680]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 4, 2: 0}, 'labels': {1: 'VSI', 2: 'Signal VSI'}, 'levels': [], 'description': ['Indicator that calculates volume per second (or period) and the corresponding MA.', 'Uses volume per second since it will be uniform for all chart periods.', 'Indicator seems to work best on 15m to 4h charts. IMHO, 1m and 5m periods are', 'too short for valid results and 1d+ will show low periods for partial days on MT4.'], 'name': 'vsi', 'source': 'MQL5 Indicators/VSI/vsi.mq5', 'folder': 'VSI', 'inputs': [{'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'volume', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 1, 'label': 'averaging method', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'int', 'default': 5, 'label': 'smoothing depth', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'smoothing parameter,', 'sinput': False}, {'mql': 'showPerPeriod', 'py': 'showPerPeriod', 'param': 'showPerPeriod', 'type': 'bool', 'default': False, 'label': 'showPerPeriod (false = volume per second, true = volume per chart period)', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
VolumeType = _input('VolumeType', VOLUME_TICK)  # volume
XMA_Method = _input('XMA_Method', MODE_EMA)  # averaging method
XLength = _input('XLength', 5)  # smoothing depth
XPhase = _input('XPhase', 15)  # smoothing parameter,
showPerPeriod = _input('showPerPeriod', False)  # showPerPeriod (false = volume per second, true = volume per chart period)
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
VSIBuffer = Arr(0, 0.0)
SignBuffer = Arr(0, 0.0)
min_rates_total = 0
PSec = 0

def OnInit():
    global PSec, min_rates_total
    min_rates_total = XMA.GetStartBars(XMA_Method, XLength, XPhase) + 1
    PSec = PeriodSeconds(PERIOD_CURRENT)
    SetIndexBuffer(0, VSIBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, SignBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'VSI')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    timeDiff = 0
    Vol = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if VolumeType == VOLUME_TICK:
            Vol = float(tick_volume[bar])
        else:
            Vol = float(volume[bar])
        timeDiff = _int(TimeCurrent() - time[bar])
        if bar == (rates_total - 1) and timeDiff > 0:
            VSIBuffer[bar] = _fdiv(Vol, timeDiff)
        else:
            VSIBuffer[bar] = _fdiv(Vol, PSec)
        if showPerPeriod:
            VSIBuffer[bar] *= PSec
        SignBuffer[bar] = XMA.XMASeries(1, prev_calculated, rates_total, XMA_Method, XPhase, XLength, VSIBuffer[bar], bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA = _alloc(CXMA)
XMA.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Vsi(_MQL5Indicator):
    name = 'vsi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # volume
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # averaging method
        'XLength': 5,  # smoothing depth
        'XPhase': 15,  # smoothing parameter,
        'showPerPeriod': False,  # showPerPeriod (false = volume per second, true = volume per chart period)
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

