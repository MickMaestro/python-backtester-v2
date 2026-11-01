"""icci_nr — converted from MQL5: MQL5 Indicators/iCCI_NRCandle/icci_nr.mq5

Бесшумный Индикатор CCI с возможностью регулировки чувствительности во входных параметрах
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [65407, 8421376, 8421504, 6053069, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'iCCI_NR'}, 'levels': [], 'description': ['Бесшумный Индикатор CCI с возможностью регулировки чувствительности во входных параметрах'], 'name': 'icci_nr', 'source': 'MQL5 Indicators/iCCI_NRCandle/icci_nr.mq5', 'folder': 'iCCI_NRCandle', 'inputs': [{'mql': 'Sens', 'py': 'Sens', 'param': 'Sens', 'type': 'uint', 'default': 1, 'label': 'Порог чувствительности', 'sinput': False}, {'mql': 'CCIperiod', 'py': 'CCIperiod', 'param': 'CCIperiod', 'type': 'uint', 'default': 10, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 0, 'label': 'Метод усреднения первого сглаживания', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'int', 'default': 3, 'label': 'Глубина  первого сглаживания', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'Параметр первого сглаживания', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 4, 'label': 'Метод усреднения второго сглаживания', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'int', 'default': 10, 'label': 'Глубина  второго сглаживания', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 100, 'label': 'Параметр второго сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 6, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 100, 'label': '', 'sinput': False}, {'mql': 'MiddleLevel', 'py': 'MiddleLevel', 'param': 'MiddleLevel', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': -100, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
Sens = _input('Sens', 1)  # Порог чувствительности
CCIperiod = _input('CCIperiod', 10)  # Период индикатора
MA_Method1 = _input('MA_Method1', MODE_SMA)  # Метод усреднения первого сглаживания
Length1 = _input('Length1', 3)  # Глубина  первого сглаживания
Phase1 = _input('Phase1', 15)  # Параметр первого сглаживания
MA_Method2 = _input('MA_Method2', MODE_JJMA)  # Метод усреднения второго сглаживания
Length2 = _input('Length2', 10)  # Глубина  второго сглаживания
Phase2 = _input('Phase2', 100)  # Параметр второго сглаживания
IPC = _input('IPC', PRICE_TYPICAL)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
HighLevel = _input('HighLevel', 100)
MiddleLevel = _input('MiddleLevel', 0)
LowLevel = _input('LowLevel', -100)
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
sens = 0.0
mul = 0.0
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
len_ = 0

def OnInit():
    global len_, min_rates_1, min_rates_2, min_rates_total, mul, sens
    min_rates_1 = XMA1.GetStartBars(MA_Method1, Length1, Phase1)
    min_rates_2 = min_rates_1 + XMA2.GetStartBars(MA_Method2, Length2, Phase2)
    min_rates_total = min_rates_1 + min_rates_2 + 1 + _int(CCIperiod)
    sens = Sens * CCIperiod * Point()
    mul = 0.015 / CCIperiod
    len_ = _int(CCIperiod) - 1
    XMA1.XMALengthCheck('Length1', Length1)
    XMA2.XMALengthCheck('Length2', Length2)
    XMA1.XMAPhaseCheck('Phase1', Phase1, MA_Method1)
    XMA2.XMAPhaseCheck('Phase2', Phase2, MA_Method2)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'iCCI_NR')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, MiddleLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrTeal)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrRed)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    x1xma = 0.0
    x2xma = 0.0
    div = 0.0
    dif = 0.0
    first = 0
    bar = 0
    rate = 0
    clr = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    rate = rates_total - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        x1xma = XMA1.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, price, bar, False)
        x2xma = XMA2.XMASeries(min_rates_1, prev_calculated, rates_total, MA_Method2, Phase2, Length2, x1xma, bar, False)
        div = 0.0
        for iii in range(MathMax(bar - len_, 0), bar + 1):
            div += MathAbs(PriceSeries(IPC, iii, open, low, high, close) - x2xma)
        div = mul * MathMax(div, sens)
        dif = price - x2xma
        if div:
            IndBuffer[bar] = _fdiv(dif, div)
        else:
            IndBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    bar = first
    for bar in range(bar, rates_total):
        clr = 2
        if IndBuffer[bar] > MiddleLevel:
            if IndBuffer[bar] > HighLevel:
                clr = 0
            else:
                clr = 1
        if IndBuffer[bar] < MiddleLevel:
            if IndBuffer[bar] < LowLevel:
                clr = 4
            else:
                clr = 3
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IcciNr(_MQL5Indicator):
    name = 'icci_nr'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Sens': 1,  # Порог чувствительности
        'CCIperiod': 10,  # Период индикатора
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения первого сглаживания
        'Length1': 3,  # Глубина  первого сглаживания
        'Phase1': 15,  # Параметр первого сглаживания
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод усреднения второго сглаживания
        'Length2': 10,  # Глубина  второго сглаживания
        'Phase2': 100,  # Параметр второго сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=6),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'HighLevel': 100,
        'MiddleLevel': 0,
        'LowLevel': -100,
    }

