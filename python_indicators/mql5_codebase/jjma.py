"""jjma — converted from MQL5: MQL5 Indicators/JMA adaptive average/jjma.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'JJMA'}, 'levels': [], 'description': [], 'name': 'jjma', 'source': 'MQL5 Indicators/JMA adaptive average/jjma.mq5', 'folder': 'JMA adaptive average', 'inputs': [{'mql': 'JMALength_', 'py': 'JMALength_', 'param': 'JMALength_', 'type': 'int', 'default': 7, 'label': 'Depth of smoothing', 'sinput': False}, {'mql': 'JMAPhase_', 'py': 'JMAPhase_', 'param': 'JMAPhase_', 'type': 'int', 'default': 100, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'JMAShift', 'py': 'JMAShift', 'param': 'JMAShift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'JMAPriceShift', 'py': 'JMAPriceShift', 'param': 'JMAPriceShift', 'type': 'int', 'default': 0, 'label': 'Vertical shift of the indicator in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
JMALength_ = _input('JMALength_', 7)  # Depth of smoothing
JMAPhase_ = _input('JMAPhase_', 100)  # Smoothing parameter
IPC = _input('IPC', PRICE_CLOSE_)  # Price constant
JMAShift = _input('JMAShift', 0)  # Horizontal shift of the indicator in bars
JMAPriceShift = _input('JMAPriceShift', 0)  # Vertical shift of the indicator in points
J1JMA = Arr(0, 0.0)
dPriceShift = 0.0

def OnInit():
    global dPriceShift
    SetIndexBuffer(0, J1JMA, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, JMAShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 31)
    PlotIndexSetString(0, PLOT_LABEL, 'JJMA')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'JJMA( Length_ = ', JMALength_, ', Phase_ = ', JMAPhase_, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    JMA = CJJMA()
    JMA.JJMALengthCheck('Length_', JMALength_)
    JMA.JJMAPhaseCheck('Phase_', JMAPhase_)
    dPriceShift = Point() * JMAPriceShift

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 31:
        return 0
    first = 0
    bar = 0
    series = 0.0
    j1jma = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        series = PriceSeries(IPC, bar, open, low, high, close)
        j1jma = _s_OnCalculate_JMA.JJMASeries(0, prev_calculated, rates_total, 0, JMAPhase_, JMALength_, series, bar, False)
        J1JMA[bar] = j1jma + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_JMA = CJJMA()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Jjma(_MQL5Indicator):
    name = 'jjma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'JMALength_': 7,  # Depth of smoothing
        'JMAPhase_': 100,  # Smoothing parameter
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'}, default=1),  # Price constant
        'JMAShift': 0,  # Horizontal shift of the indicator in bars
        'JMAPriceShift': 0,  # Vertical shift of the indicator in points
    }

