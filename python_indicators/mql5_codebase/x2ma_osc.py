"""x2ma_osc — converted from MQL5: MQL5 Include/x2ma_osc.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [13850042]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'X2MA_Osc'}, 'levels': [0.0], 'description': [], 'name': 'x2ma_osc', 'source': 'MQL5 Include/x2ma_osc.mq5', 'folder': 'MQL5 Include', 'inputs': [{'mql': 'nPeriod', 'py': 'nPeriod', 'param': 'nPeriod', 'type': 'uint', 'default': 100, 'label': 'oscillator normalization period', 'sinput': False}, {'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': 'first smoothing averaging method', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'uint', 'default': 12, 'label': 'first smoothing depth', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'first smoothing parameter,', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 4, 'label': 'second smoothing averaging method', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'uint', 'default': 5, 'label': 'second smoothing depth', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 15, 'label': 'second smoothing parameter,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'vertical shift of the indicator in pointsх', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
nPeriod = _input('nPeriod', 100)  # oscillator normalization period
MA_Method1 = _input('MA_Method1', MODE_SMA)  # first smoothing averaging method
Length1 = _input('Length1', 12)  # first smoothing depth
Phase1 = _input('Phase1', 15)  # first smoothing parameter,
MA_Method2 = _input('MA_Method2', MODE_JJMA)  # second smoothing averaging method
Length2 = _input('Length2', 5)  # second smoothing depth
Phase2 = _input('Phase2', 15)  # second smoothing parameter,
IPC = _input('IPC', PRICE_CLOSE)  # price constant
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # vertical shift of the indicator in pointsх
X2MAOsc = Arr(0, 0.0)
Count = Arr(0, 0)
X2MA = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0

def Recount_ArrayZeroPos(CoArr, Size):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def Interpolation(a, b, c, d, X):
    if (b - a) == 0:
        return 10000000.0
    else:
        return d - _fdiv((b - X) * (d - c), b - a)

def OnInit():
    global min_rates_1, min_rates_2, min_rates_total
    min_rates_1 = XMA1.GetStartBars(MA_Method1, Length1, Phase1)
    min_rates_2 = XMA2.GetStartBars(MA_Method2, Length2, Phase2)
    min_rates_total = min_rates_1 + min_rates_2
    XMA1.XMALengthCheck('Length1', Length1)
    XMA2.XMALengthCheck('Length2', Length2)
    XMA1.XMAPhaseCheck('Phase1', Phase1, MA_Method1)
    XMA2.XMAPhaseCheck('Phase2', Phase2, MA_Method2)
    ArrayResize(Count, nPeriod)
    ArrayResize(X2MA, nPeriod)
    ArrayInitialize(Count, 0)
    ArrayInitialize(X2MA, 0.0)
    ArraySetAsSeries(Count, True)
    ArraySetAsSeries(X2MA, True)
    SetIndexBuffer(0, X2MAOsc, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(X2MAOsc, True)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(MA_Method1)
    Smooth2 = XMA1.GetString_MA_Method(MA_Method2)
    StringConcatenate(shortname, 'X2MA_Osc(', nPeriod, ', ', Length1, ', ', Length2, ', ', Smooth1, ', ', Smooth2, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(open, True)
    price_ = 0.0
    x1xma = 0.0
    x2xmaosc = 0.0
    MAX = 0.0
    MIN = 0.0
    limit = 0
    bar = 0
    maxbar1 = 0
    maxbar2 = 0
    maxbar1 = rates_total - 1
    maxbar2 = maxbar1 - min_rates_1
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        x1xma = XMA1.XMASeries(maxbar1, prev_calculated, rates_total, MA_Method1, Phase1, Length1, price_, bar, True)
        X2MA[Count[0]] = XMA2.XMASeries(maxbar2, prev_calculated, rates_total, MA_Method2, Phase2, Length2, x1xma, bar, True)
        MAX = X2MA[ArrayMaximum(X2MA, 0, WHOLE_ARRAY)]
        MIN = X2MA[ArrayMinimum(X2MA, 0, WHOLE_ARRAY)]
        x2xmaosc = Interpolation(MAX, MIN, 100.0, 0.0, X2MA[Count[0]])
        X2MAOsc[bar] = x2xmaosc - 50
        if bar > 0:
            Recount_ArrayZeroPos(Count, nPeriod)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class X2maOsc(_MQL5Indicator):
    name = 'x2ma_osc'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'nPeriod': 100,  # oscillator normalization period
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # first smoothing averaging method
        'Length1': 12,  # first smoothing depth
        'Phase1': 15,  # first smoothing parameter,
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # second smoothing averaging method
        'Length2': 5,  # second smoothing depth
        'Phase2': 15,  # second smoothing parameter,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # price constant
        'Shift': 0,  # horizontal shift of the indicator in bars
        'PriceShift': 0,  # vertical shift of the indicator in pointsх
    }

