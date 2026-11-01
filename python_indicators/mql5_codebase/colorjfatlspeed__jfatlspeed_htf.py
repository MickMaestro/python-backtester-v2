"""colorjfatlspeed — converted from MQL5: MQL5 Indicators/JFatlSpeed HTF/colorjfatlspeed.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 1, 2: 12}, 'colors': {1: [8421504], 2: [8421504, 16711680, 16711935]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'JFATL SPEED', 2: 'JFATL SPEED'}, 'levels': [], 'description': [], 'name': 'colorjfatlspeed', 'source': 'MQL5 Indicators/JFatlSpeed HTF/colorjfatlspeed.mq5', 'folder': 'JFatlSpeed HTF', 'inputs': [{'mql': 'LengthFatl', 'py': 'LengthFatl', 'param': 'LengthFatl', 'type': 'int', 'default': 8, 'label': 'JMA period of Fatl smoothing', 'sinput': False}, {'mql': 'PhaseFatl', 'py': 'PhaseFatl', 'param': 'PhaseFatl', 'type': 'int', 'default': 100, 'label': 'JMA smoothing Fatl parameter [-100...+100],', 'sinput': False}, {'mql': 'MomPeriod', 'py': 'MomPeriod', 'param': 'MomPeriod', 'type': 'int', 'default': 1, 'label': 'Momentum indicator period for rate measuring', 'sinput': False}, {'mql': 'Smooth', 'py': 'Smooth', 'param': 'Smooth', 'type': 'int', 'default': 2, 'label': 'Indicator JMA smoothing depth', 'sinput': False}, {'mql': 'SmPhase', 'py': 'SmPhase', 'param': 'SmPhase', 'type': 'int', 'default': 100, 'label': 'Indicator JMA smoothing parameter [-100...+100]', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'FATLShift', 'py': 'FATLShift', 'param': 'FATLShift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
LengthFatl = _input('LengthFatl', 8)  # JMA period of Fatl smoothing
PhaseFatl = _input('PhaseFatl', 100)  # JMA smoothing Fatl parameter [-100...+100],
MomPeriod = _input('MomPeriod', 1)  # Momentum indicator period for rate measuring
Smooth = _input('Smooth', 2)  # Indicator JMA smoothing depth
SmPhase = _input('SmPhase', 100)  # Indicator JMA smoothing parameter [-100...+100]
IPC = _input('IPC', PRICE_CLOSE_)  # Applied price
FATLShift = _input('FATLShift', 0)  # Horizontal shift of the indicator in bars
FATLPeriod = 39
IndBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
LineIndBuffer = Arr(0, 0.0)
start = 0
fstart = 0
jfstart = 0
mstart = 0
FATLSize = 0
dPriceShift = 0.0

def OnInit():
    global fstart, jfstart, mstart, start
    fstart = FATLPeriod
    jfstart = fstart + 30
    mstart = jfstart + MomPeriod
    start = mstart + 30 + 1
    SetIndexBuffer(0, LineIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, FATLShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, FATLShift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, start)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    SetIndexBuffer(2, ColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, start)
    shortname = Box("")
    StringConcatenate(shortname, 'JFATL Speed(', LengthFatl, ' ,', PhaseFatl, ' ,', MomPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    JMA = CJJMA()
    JMA.JJMALengthCheck('Length_', LengthFatl)
    JMA.JJMAPhaseCheck('Phase_', PhaseFatl)
    JMA.JJMALengthCheck('MomPeriod', MomPeriod)
    JMA.JJMALengthCheck('Smooth', Smooth)
    JMA.JJMAPhaseCheck('SmPhase', SmPhase)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < start:
        return 0
    first = 0
    bar = 0
    price = 0.0
    jfatl = 0.0
    fatl = 0.0
    jmom = 0.0
    jfspeed = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        fatl = _s_OnCalculate_FATL.FATLSeries(0, prev_calculated, rates_total, price, bar, False)
        jfatl = _s_OnCalculate_JMA1.JJMASeries(fstart, prev_calculated, rates_total, 0, PhaseFatl, LengthFatl, fatl, bar, False)
        jmom = _s_OnCalculate_MOM.MomentumSeries(jfstart, prev_calculated, rates_total, MomPeriod, jfatl, bar, False)
        jfspeed = _s_OnCalculate_JMA2.JJMASeries(mstart, prev_calculated, rates_total, 0, SmPhase, Smooth, jmom, bar, False)
        jfspeed = _fdiv(jfspeed, Point())
        IndBuffer[bar] = jfspeed
        LineIndBuffer[bar] = jfspeed
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = start
    bar = first
    for bar in range(bar, rates_total):
        ColorBuffer[bar] = 0.0
        if IndBuffer[bar] > IndBuffer[bar - 1]:
            ColorBuffer[bar] = 1.0
        if IndBuffer[bar] < IndBuffer[bar - 1]:
            ColorBuffer[bar] = 2.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_JMA1 = CJJMA()
_s_OnCalculate_JMA2 = CJJMA()
_s_OnCalculate_FATL = CFATL()
_s_OnCalculate_MOM = CMomentum()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorjfatlspeed(_MQL5Indicator):
    name = 'colorjfatlspeed'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'LengthFatl': 8,  # JMA period of Fatl smoothing
        'PhaseFatl': 100,  # JMA smoothing Fatl parameter [-100...+100],
        'MomPeriod': 1,  # Momentum indicator period for rate measuring
        'Smooth': 2,  # Indicator JMA smoothing depth
        'SmPhase': 100,  # Indicator JMA smoothing parameter [-100...+100]
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'}, default=1),  # Applied price
        'FATLShift': 0,  # Horizontal shift of the indicator in bars
    }

