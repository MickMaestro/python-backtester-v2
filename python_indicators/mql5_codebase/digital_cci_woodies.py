"""digital_cci_woodies — converted from MQL5: MQL5 Indicators/Digital_CCI_Woodies/digital_cci_woodies.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [11823615, 11193702]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Digital_CCI_Woodies'}, 'levels': [], 'description': [], 'name': 'digital_cci_woodies', 'source': 'MQL5 Indicators/Digital_CCI_Woodies/digital_cci_woodies.mq5', 'folder': 'Digital_CCI_Woodies', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': 'Метод усреднения первого сглаживания', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'int', 'default': 14, 'label': 'Глубина  первого сглаживания', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'Параметр первого сглаживания', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 0, 'label': 'Метод усреднения второго сглаживания', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'int', 'default': 6, 'label': 'Глубина  второго сглаживания', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 15, 'label': 'Параметр второго сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
MA_Method1 = _input('MA_Method1', MODE_SMA)  # Метод усреднения первого сглаживания
Length1 = _input('Length1', 14)  # Глубина  первого сглаживания
Phase1 = _input('Phase1', 15)  # Параметр первого сглаживания
MA_Method2 = _input('MA_Method2', MODE_SMA)  # Метод усреднения второго сглаживания
Length2 = _input('Length2', 6)  # Глубина  второго сглаживания
Phase2 = _input('Phase2', 15)  # Параметр второго сглаживания
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_ = 0
min_rates_1 = 0
min_rates_2 = 0

def OnInit():
    global min_rates_, min_rates_1, min_rates_2, min_rates_total
    min_rates_ = 26
    min_rates_1 = min_rates_ + GetStartBars(MA_Method1, Length1, Phase1)
    min_rates_2 = min_rates_ + GetStartBars(MA_Method2, Length2, Phase2)
    min_rates_total = (2 * (MathMax(min_rates_1, min_rates_2) - min_rates_)) + min_rates_
    XMA1.XMALengthCheck('Length1', Length1)
    XMA2.XMALengthCheck('Length2', Length2)
    XMA1.XMAPhaseCheck('Phase1', Phase1, MA_Method1)
    XMA2.XMAPhaseCheck('Phase2', Phase2, MA_Method2)
    SetIndexBuffer(0, ExtABuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtBBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(MA_Method1)
    Smooth2 = XMA1.GetString_MA_Method(MA_Method2)
    StringConcatenate(shortname, 'Digital_CCI_Woodies(', Length1, ', ', Length2, ', ', Smooth1, ', ', Smooth2, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    res = 0.0
    xres1 = 0.0
    xres2 = 0.0
    rel1 = 0.0
    rel2 = 0.0
    dev1 = 0.0
    dev2 = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        res = Get_Filter(IPC, open, low, high, close, bar)
        xres1 = XMA1.XMASeries(min_rates_, prev_calculated, rates_total, MA_Method1, Phase1, Length1, res, bar, False)
        xres2 = XMA2.XMASeries(min_rates_, prev_calculated, rates_total, MA_Method2, Phase2, Length2, res, bar, False)
        rel1 = res - xres1
        rel2 = res - xres2
        dev1 = 0.015 * XMA3.XMASeries(min_rates_1, prev_calculated, rates_total, MA_Method1, Phase1, Length1, MathAbs(rel1), bar, False)
        dev2 = 0.015 * XMA4.XMASeries(min_rates_2, prev_calculated, rates_total, MA_Method2, Phase2, Length2, MathAbs(rel2), bar, False)
        if dev1:
            ExtABuffer[bar] = _fdiv(rel1, dev1)
        else:
            ExtABuffer[bar] = 0.0
        if dev2:
            ExtBBuffer[bar] = _fdiv(rel2, dev2)
        else:
            ExtBBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def Get_Filter(Price, Open, Low, High, Close, index):
    sum_ = (0.225654509516691 * PriceSeries(Price, index - 0, Open, Low, High, Close)) + (0.219241264585139 * PriceSeries(Price, index - 1, Open, Low, High, Close)) + (0.200688479689899 * PriceSeries(Price, index - 2, Open, Low, High, Close)) + (0.171992513765923 * PriceSeries(Price, index - 3, Open, Low, High, Close)) + (0.136270408129286 * PriceSeries(Price, index - 4, Open, Low, High, Close)) + (0.0971644469103302 * PriceSeries(Price, index - 5, Open, Low, High, Close)) + (0.0585064796603445 * PriceSeries(Price, index - 6, Open, Low, High, Close)) + (0.0237448140297671 * PriceSeries(Price, index - 7, Open, Low, High, Close)) - (0.00442869436477854 * PriceSeries(Price, index - 8, Open, Low, High, Close)) - (0.0243636783229045 * PriceSeries(Price, index - 9, Open, Low, High, Close)) - (0.0355617365834807 * PriceSeries(Price, index - 10, Open, Low, High, Close)) - (0.0386306817434228 * PriceSeries(Price, index - 11, Open, Low, High, Close)) - (0.0350564564449243 * PriceSeries(Price, index - 12, Open, Low, High, Close)) - (0.0268963490805002 * PriceSeries(Price, index - 13, Open, Low, High, Close)) - (0.0164157887033052 * PriceSeries(Price, index - 14, Open, Low, High, Close)) - (0.00573862260748731 * PriceSeries(Price, index - 15, Open, Low, High, Close)) + (0.00342620684434 * PriceSeries(Price, index - 16, Open, Low, High, Close)) + (0.00996574022237624 * PriceSeries(Price, index - 17, Open, Low, High, Close)) + (0.0134223280887248 * PriceSeries(Price, index - 18, Open, Low, High, Close)) + (0.0139394004237978 * PriceSeries(Price, index - 19, Open, Low, High, Close)) + (0.0121149938483286 * PriceSeries(Price, index - 20, Open, Low, High, Close)) + (0.00883315067608292 * PriceSeries(Price, index - 21, Open, Low, High, Close)) + (0.0050235681107559 * PriceSeries(Price, index - 22, Open, Low, High, Close)) + (0.00151954406404245 * PriceSeries(Price, index - 23, Open, Low, High, Close)) - (0.00108567173532015 * PriceSeries(Price, index - 24, Open, Low, High, Close)) - (0.0133301689797048 * PriceSeries(Price, index - 25, Open, Low, High, Close))
    return sum_

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()
XMA3 = _alloc(CXMA)
XMA3.__init__()
XMA4 = _alloc(CXMA)
XMA4.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DigitalCciWoodies(_MQL5Indicator):
    name = 'digital_cci_woodies'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения первого сглаживания
        'Length1': 14,  # Глубина  первого сглаживания
        'Phase1': 15,  # Параметр первого сглаживания
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения второго сглаживания
        'Length2': 6,  # Глубина  второго сглаживания
        'Phase2': 15,  # Параметр второго сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

