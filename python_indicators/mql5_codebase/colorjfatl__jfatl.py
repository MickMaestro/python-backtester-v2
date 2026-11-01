"""colorjfatl — converted from MQL5: MQL5 Indicators/JFATL/colorjfatl.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [8421504, 55295, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'JFATL'}, 'levels': [], 'description': [], 'name': 'colorjfatl', 'source': 'MQL5 Indicators/JFATL/colorjfatl.mq5', 'folder': 'JFATL', 'inputs': [{'mql': 'JMALength_', 'py': 'JMALength_', 'param': 'JMALength_', 'type': 'int', 'default': 5, 'label': 'Depth of the JMA smoothing', 'sinput': False}, {'mql': 'JMAPhase_', 'py': 'JMAPhase_', 'param': 'JMAPhase_', 'type': 'int', 'default': -100, 'label': 'JMA smoothing parameter,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'FATLShift', 'py': 'FATLShift', 'param': 'FATLShift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of FATL in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Vertical shift of FATL in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
JMALength_ = _input('JMALength_', 5)  # Depth of the JMA smoothing
JMAPhase_ = _input('JMAPhase_', -100)  # JMA smoothing parameter,
IPC = _input('IPC', PRICE_CLOSE_)  # Price constant
FATLShift = _input('FATLShift', 0)  # Horizontal shift of FATL in bars
PriceShift = _input('PriceShift', 0)  # Vertical shift of FATL in points
FATLPeriod = 39
ExtLineBuffer = Arr(0, 0.0)
ColorExtLineBuffer = Arr(0, 0.0)
start = 0
fstart = 0
FATLSize = 0
dPriceShift = 0.0
FATLTable = Arr.of([0.436040945, 0.3658689069, 0.2460452079, 0.1104506886, -0.0054034585, -0.0760367731, -0.0933058722, -0.0670110374, -0.0190795053, 0.0259609206, 0.0502044896, 0.0477818607, 0.0249252327, -0.0047706151, -0.0272432537, -0.0338917071, -0.0244141482, -0.0055774838, 0.0128149838, 0.0226522218, 0.0208778257, 0.0100299086, -0.0036771622, -0.013674485, -0.0160483392, -0.0108597376, -0.0016060704, 0.0069480557, 0.0110573605, 0.0095711419, 0.0040444064, -0.0023824623, -0.0067093714, -0.00720034, -0.004771771, 0.0005541115, 0.000786016, 0.0130129076, 0.0040364019], fill=0.0)

def OnInit():
    global FATLSize, dPriceShift, start
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, FATLShift)
    FATLSize = ArraySize(FATLTable)
    start = FATLSize + 30
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start)
    shortname = Box("")
    StringConcatenate(shortname, 'JFATL(', JMALength_, ' ,', JMAPhase_, ')')
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, ColorExtLineBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, start + 1)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    dPriceShift = Point() * PriceShift
    JMA = CJJMA()
    JMA.JJMALengthCheck('Length_', JMALength_)
    JMA.JJMAPhaseCheck('Phase_', JMAPhase_)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global fstart
    if rates_total < start:
        return 0
    first = 0
    bar = 0
    jfatl = 0.0
    FATL = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = FATLPeriod - 1
        fstart = first
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        FATL = 0.0
        iii = 0
        while iii < FATLSize:
            FATL += FATLTable[iii] * PriceSeries(IPC, bar - iii, open, low, high, close)
            iii += 1
        jfatl = _s_OnCalculate_JMA.JJMASeries(fstart, prev_calculated, rates_total, 0, JMAPhase_, JMALength_, FATL, bar, False)
        ExtLineBuffer[bar] = jfatl + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        ColorExtLineBuffer[bar] = 0.0
        if ExtLineBuffer[bar - 1] < ExtLineBuffer[bar]:
            ColorExtLineBuffer[bar] = 1.0
        if ExtLineBuffer[bar - 1] > ExtLineBuffer[bar]:
            ColorExtLineBuffer[bar] = 2.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_JMA = CJJMA()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorjfatl(_MQL5Indicator):
    name = 'colorjfatl'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'JMALength_': 5,  # Depth of the JMA smoothing
        'JMAPhase_': -100,  # JMA smoothing parameter,
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'}, default=1),  # Price constant
        'FATLShift': 0,  # Horizontal shift of FATL in bars
        'PriceShift': 0,  # Vertical shift of FATL in points
    }

