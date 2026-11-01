"""colortsi-oscillator — converted from MQL5: MQL5 Indicators/TSI-Oscillator/colortsi-oscillator.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [13382297, 9639167]}, 'widths': {}, 'styles': {}, 'labels': {1: 'TSI-Oscillator'}, 'levels': [50.0, 0.0, -50.0], 'description': [], 'name': 'colortsi-oscillator', 'source': 'MQL5 Indicators/TSI-Oscillator/colortsi-oscillator.mq5', 'folder': 'TSI-Oscillator', 'inputs': [{'mql': 'First_Method', 'py': 'First_Method', 'param': 'First_Method', 'type': 'int', 'default': 0, 'label': 'Smoothing method 1', 'sinput': False}, {'mql': 'First_Length', 'py': 'First_Length', 'param': 'First_Length', 'type': 'int', 'default': 12, 'label': 'Smoothing depth 1', 'sinput': False}, {'mql': 'First_Phase', 'py': 'First_Phase', 'param': 'First_Phase', 'type': 'int', 'default': 15, 'label': 'Smoothing parameter 1', 'sinput': False}, {'mql': 'Second_Method', 'py': 'Second_Method', 'param': 'Second_Method', 'type': 'int', 'default': 0, 'label': 'Smoothing method 2', 'sinput': False}, {'mql': 'Second_Length', 'py': 'Second_Length', 'param': 'Second_Length', 'type': 'int', 'default': 12, 'label': 'Smoothing depth 2', 'sinput': False}, {'mql': 'Second_Phase', 'py': 'Second_Phase', 'param': 'Second_Phase', 'type': 'int', 'default': 15, 'label': 'Smoothing parameter 2', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'TriggerShift', 'py': 'TriggerShift', 'param': 'TriggerShift', 'type': 'uint', 'default': 1, 'label': 'Bar shift for the trigger', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
First_Method = _input('First_Method', MODE_SMA)  # Smoothing method 1
First_Length = _input('First_Length', 12)  # Smoothing depth 1
First_Phase = _input('First_Phase', 15)  # Smoothing parameter 1
Second_Method = _input('Second_Method', MODE_SMA)  # Smoothing method 2
Second_Length = _input('Second_Length', 12)  # Smoothing depth 2
Second_Phase = _input('Second_Phase', 15)  # Smoothing parameter 2
IPC = _input('IPC', PRICE_CLOSE)  # Price constant
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
TriggerShift = _input('TriggerShift', 1)  # Bar shift for the trigger
min_rates_total = 0
min_rates_total1 = 0
min_rates_total2 = 0
TSIBuffer = Arr(0, 0.0)
TriggerBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total, min_rates_total1, min_rates_total2
    min_rates_total1 = MTM1.GetStartBars(First_Method, First_Length, First_Phase) + 1
    min_rates_total2 = min_rates_total1 + MTM1.GetStartBars(First_Method, First_Length, First_Phase)
    min_rates_total = _int(min_rates_total1 + MTM1.GetStartBars(Second_Method, Second_Length, Second_Phase) + TriggerShift)
    MTM1.XMALengthCheck('First_Length', First_Length)
    MTM1.XMAPhaseCheck('First_Phase', First_Phase, First_Method)
    MTM1.XMALengthCheck('Second_Length', Second_Length)
    MTM1.XMAPhaseCheck('Second_Phase', Second_Phase, Second_Method)
    SetIndexBuffer(0, TSIBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, TriggerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    Smooth1 = MTM1.GetString_MA_Method(First_Method)
    Smooth2 = MTM1.GetString_MA_Method(Second_Method)
    StringConcatenate(shortname, 'TSI-Oscillator(', Smooth1, ', ', First_Length, ', ', Smooth2, ', ', Second_Length, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (min_rates_total + begin):
        return 0
    dprice = 0.0
    absdprice = 0.0
    mtm1 = 0.0
    absmtm1 = 0.0
    mtm2 = 0.0
    absmtm2 = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        dprice = price[bar] - price[bar - 1]
        absdprice = MathAbs(dprice)
        mtm1 = MTM1.XMASeries(1, prev_calculated, rates_total, First_Method, First_Phase, First_Length, dprice, bar, False)
        absmtm1 = ABSMTM1.XMASeries(1, prev_calculated, rates_total, First_Method, First_Phase, First_Length, absdprice, bar, False)
        mtm2 = MTM2.XMASeries(min_rates_total1, prev_calculated, rates_total, Second_Method, Second_Phase, Second_Length, mtm1, bar, False)
        absmtm2 = ABSMTM2.XMASeries(min_rates_total1, prev_calculated, rates_total, Second_Method, Second_Phase, Second_Length, absmtm1, bar, False)
        if bar > min_rates_total2:
            TSIBuffer[bar] = _fdiv(100.0 * mtm2, absmtm2)
        else:
            TSIBuffer[bar] = EMPTY_VALUE
        if bar > min_rates_total:
            TriggerBuffer[bar] = TSIBuffer[bar - TriggerShift]
        else:
            TriggerBuffer[bar] = EMPTY_VALUE
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
MTM1 = _alloc(CXMA)
MTM1.__init__()
MTM2 = _alloc(CXMA)
MTM2.__init__()
ABSMTM1 = _alloc(CXMA)
ABSMTM1.__init__()
ABSMTM2 = _alloc(CXMA)
ABSMTM2.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColortsiOscillator(_MQL5Indicator):
    name = 'colortsi-oscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'First_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Smoothing method 1
        'First_Length': 12,  # Smoothing depth 1
        'First_Phase': 15,  # Smoothing parameter 1
        'Second_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Smoothing method 2
        'Second_Length': 12,  # Smoothing depth 2
        'Second_Phase': 15,  # Smoothing parameter 2
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Price constant
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'TriggerShift': 1,  # Bar shift for the trigger
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

