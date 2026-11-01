"""jmacd — converted from MQL5: MQL5 Indicators/JMACD/jmacd.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 3, 2: 1}, 'colors': {1: [14822282], 2: [16711935]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 4}, 'labels': {1: 'JMACD', 2: 'Signal Line'}, 'levels': [], 'description': [], 'name': 'jmacd', 'source': 'MQL5 Indicators/JMACD/jmacd.mq5', 'folder': 'JMACD', 'inputs': [{'mql': 'Fast_JMA', 'py': 'Fast_JMA', 'param': 'Fast_JMA', 'type': 'int', 'default': 12, 'label': 'Period of the fast MA', 'sinput': False}, {'mql': 'Slow_JMA', 'py': 'Slow_JMA', 'param': 'Slow_JMA', 'type': 'int', 'default': 26, 'label': 'Depth of the SMMA smoothing', 'sinput': False}, {'mql': 'Signal_JMA', 'py': 'Signal_JMA', 'param': 'Signal_JMA', 'type': 'int', 'default': 9, 'label': 'Signal line period', 'sinput': False}, {'mql': 'Phase_', 'py': 'Phase_', 'param': 'Phase_', 'type': 'int', 'default': 100, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
Fast_JMA = _input('Fast_JMA', 12)  # Period of the fast MA
Slow_JMA = _input('Slow_JMA', 26)  # Depth of the SMMA smoothing
Signal_JMA = _input('Signal_JMA', 9)  # Signal line period
Phase_ = _input('Phase_', 100)  # Smoothing parameter
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE_)  # Price constant
MACDBuffer = Arr(0, 0.0)
SignBuffer = Arr(0, 0.0)
start = 60
macd_start = 30

def OnInit():
    SetIndexBuffer(0, MACDBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, macd_start + 1)
    PlotIndexSetString(0, PLOT_LABEL, 'JMACD')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, SignBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, start + 1)
    PlotIndexSetString(1, PLOT_LABEL, 'Signal JMA')
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'JMACD( ', Fast_JMA, ', ', Slow_JMA, ', ', Signal_JMA, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    JMA = CJJMA()
    JMA.JJMALengthCheck('Fast_JMA', Fast_JMA)
    JMA.JJMALengthCheck('Slow_JMA', Slow_JMA)
    JMA.JJMALengthCheck('Slow_JMA', Signal_JMA)
    JMA.JJMAPhaseCheck('Phase_', Phase_)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < start:
        return 0
    first = 0
    bar = 0
    price_ = 0.0
    fast_jma = 0.0
    slow_jma = 0.0
    jmacd = 0.0
    sign_jma = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        bar = 0
        for bar in range(bar, macd_start + 1):
            MACDBuffer[bar] = 0.0
        else:
            bar = _range_end(bar, macd_start + 1, 1)
        bar = 0
        for bar in range(bar, start + 1):
            SignBuffer[bar] = 0.0
        else:
            bar = _range_end(bar, start + 1, 1)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price_ = PriceSeries(AppliedPrice, bar, open, low, high, close)
        fast_jma = _s_OnCalculate_JMA1.JJMASeries(0, prev_calculated, rates_total, 0, Phase_, Fast_JMA, price_, bar, False)
        slow_jma = _s_OnCalculate_JMA2.JJMASeries(0, prev_calculated, rates_total, 0, Phase_, Slow_JMA, price_, bar, False)
        jmacd = fast_jma - slow_jma
        sign_jma = _s_OnCalculate_JMA3.JJMASeries(macd_start, prev_calculated, rates_total, 0, Phase_, Signal_JMA, jmacd, bar, False)
        MACDBuffer[bar] = jmacd
        SignBuffer[bar] = sign_jma
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_JMA1 = CJJMA()
_s_OnCalculate_JMA2 = CJJMA()
_s_OnCalculate_JMA3 = CJJMA()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Jmacd(_MQL5Indicator):
    name = 'jmacd'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Fast_JMA': 12,  # Period of the fast MA
        'Slow_JMA': 26,  # Depth of the SMMA smoothing
        'Signal_JMA': 9,  # Signal line period
        'Phase_': 100,  # Smoothing parameter
        'AppliedPrice': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'}, default=1),  # Price constant
    }

