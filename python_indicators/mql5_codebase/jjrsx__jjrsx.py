"""jjrsx — converted from MQL5: MQL5 Indicators/JJRSX/jjrsx.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [14822282]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'JJRSX'}, 'levels': [0.5, -0.5, 0.0], 'description': [], 'name': 'jjrsx', 'source': 'MQL5 Indicators/JJRSX/jjrsx.mq5', 'folder': 'JJRSX', 'inputs': [{'mql': 'JJMALength', 'py': 'JJMALength', 'param': 'JJMALength', 'type': 'int', 'default': 8, 'label': 'Depth of smoothing', 'sinput': False}, {'mql': 'JJMASmooth', 'py': 'JJMASmooth', 'param': 'JJMASmooth', 'type': 'int', 'default': 8, 'label': 'Depth of the JJMA smoothing', 'sinput': False}, {'mql': 'JJMAPhase', 'py': 'JJMAPhase', 'param': 'JJMAPhase', 'type': 'int', 'default': 100, 'label': 'Parameter of the JJMA smoothing,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
JJMALength = _input('JJMALength', 8)  # Depth of smoothing
JJMASmooth = _input('JJMASmooth', 8)  # Depth of the JJMA smoothing
JJMAPhase = _input('JJMAPhase', 100)  # Parameter of the JJMA smoothing,
IPC = _input('IPC', PRICE_CLOSE_)  # Price constant
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
JJRSX = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, JJRSX, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 32)
    PlotIndexSetString(0, PLOT_LABEL, 'JJRSX')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'JJRSX( Length = ', JJMALength, ', Smooth = ', JJMASmooth, ', Phase = ', JJMAPhase, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    JMA = CJJMA()
    JMA.JJMALengthCheck('Length', JJMALength)
    JMA.JJMALengthCheck('Smooth', JJMASmooth)
    JMA.JJMAPhaseCheck('Phase', JJMAPhase)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 32:
        return 0
    dprice_ = 0.0
    udprice_ = 0.0
    up_jrsx = 0.0
    dn_jrsx = 0.0
    jrsx = 0.0
    jjrsx = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        dprice_ = PriceSeries(IPC, bar, open, low, high, close) - PriceSeries(IPC, bar - 1, open, low, high, close)
        udprice_ = MathAbs(dprice_)
        up_jrsx = _s_OnCalculate_Jur1.JurXSeries(1, prev_calculated, rates_total, 0, JJMALength, dprice_, bar, False)
        dn_jrsx = _s_OnCalculate_Jur2.JurXSeries(1, prev_calculated, rates_total, 0, JJMALength, udprice_, bar, False)
        if dn_jrsx == 0:
            jrsx = EMPTY_VALUE
        else:
            jrsx = _fdiv(up_jrsx, dn_jrsx)
            if jrsx > 1:
                jrsx = 1.0
            if jrsx < -1:
                jrsx = -1.0
        jjrsx = _s_OnCalculate_JMA.JJMASeries(1, prev_calculated, rates_total, 0, JJMAPhase, JJMASmooth, jrsx, bar, False)
        JJRSX[bar] = jjrsx
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_Jur1 = CJurX()
_s_OnCalculate_Jur2 = CJurX()
_s_OnCalculate_JMA = CJJMA()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Jjrsx(_MQL5Indicator):
    name = 'jjrsx'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'JJMALength': 8,  # Depth of smoothing
        'JJMASmooth': 8,  # Depth of the JJMA smoothing
        'JJMAPhase': 100,  # Parameter of the JJMA smoothing,
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'}, default=1),  # Price constant
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

