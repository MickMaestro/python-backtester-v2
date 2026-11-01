"""jfatlspeed — converted from MQL5: MQL5 Indicators/JFatlSpeed/jfatlspeed.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16711680]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'JFATL'}, 'levels': [], 'description': [], 'name': 'jfatlspeed', 'source': 'MQL5 Indicators/JFatlSpeed/jfatlspeed.mq5', 'folder': 'JFatlSpeed', 'inputs': [{'mql': 'Length_', 'py': 'Length_', 'param': 'Length_', 'type': 'int', 'default': 8, 'label': 'JMA period of Fatl smoothing', 'sinput': False}, {'mql': 'Phase_', 'py': 'Phase_', 'param': 'Phase_', 'type': 'int', 'default': 100, 'label': 'JMA parameter of Fatl smoothing,', 'sinput': False}, {'mql': 'MomPeriod', 'py': 'MomPeriod', 'param': 'MomPeriod', 'type': 'int', 'default': 1, 'label': 'Momentum indicator period for rate measuring', 'sinput': False}, {'mql': 'Smooth', 'py': 'Smooth', 'param': 'Smooth', 'type': 'int', 'default': 2, 'label': 'Depth of the JMA smoothing of the indicator', 'sinput': False}, {'mql': 'SmPhase', 'py': 'SmPhase', 'param': 'SmPhase', 'type': 'int', 'default': 100, 'label': 'Parameter of the JMA smoothing of the indicator', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'FATLShift', 'py': 'FATLShift', 'param': 'FATLShift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
Length_ = _input('Length_', 8)  # JMA period of Fatl smoothing
Phase_ = _input('Phase_', 100)  # JMA parameter of Fatl smoothing,
MomPeriod = _input('MomPeriod', 1)  # Momentum indicator period for rate measuring
Smooth = _input('Smooth', 2)  # Depth of the JMA smoothing of the indicator
SmPhase = _input('SmPhase', 100)  # Parameter of the JMA smoothing of the indicator
IPC = _input('IPC', PRICE_CLOSE_)  # Price constant
FATLShift = _input('FATLShift', 0)  # Horizontal shift of the indicator in bars
FATLPeriod = 39
ExtLineBuffer = Arr(0, 0.0)
start = 0
fstart = 0
jfstart = 0
mstart = 0
FATLSize = 0
dPriceShift = 0.0

def OnInit():
    global fstart, jfstart, mstart, start
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, FATLShift)
    fstart = FATLPeriod
    jfstart = fstart + 30
    mstart = jfstart + MomPeriod
    start = mstart + 30
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start)
    shortname = Box("")
    StringConcatenate(shortname, 'JFATLSpeed(', Length_, ' ,', Phase_, ' ,', MomPeriod, ')')
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    JMA = CJJMA()
    JMA.JJMALengthCheck('Length_', Length_)
    JMA.JJMAPhaseCheck('Phase_', Phase_)
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
        jfatl = _s_OnCalculate_JMA1.JJMASeries(fstart, prev_calculated, rates_total, 0, Phase_, Length_, fatl, bar, False)
        jmom = _s_OnCalculate_MOM.MomentumSeries(jfstart, prev_calculated, rates_total, MomPeriod, jfatl, bar, False)
        jfspeed = _s_OnCalculate_JMA2.JJMASeries(mstart, prev_calculated, rates_total, 0, SmPhase, Smooth, jmom, bar, False)
        jfspeed = _fdiv(jfspeed, Point())
        ExtLineBuffer[bar] = jfspeed
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


class Jfatlspeed(_MQL5Indicator):
    name = 'jfatlspeed'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length_': 8,  # JMA period of Fatl smoothing
        'Phase_': 100,  # JMA parameter of Fatl smoothing,
        'MomPeriod': 1,  # Momentum indicator period for rate measuring
        'Smooth': 2,  # Depth of the JMA smoothing of the indicator
        'SmPhase': 100,  # Parameter of the JMA smoothing of the indicator
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPLE_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'}, default=1),  # Price constant
        'FATLShift': 0,  # Horizontal shift of the indicator in bars
    }

