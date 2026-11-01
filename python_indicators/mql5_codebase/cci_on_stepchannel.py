"""cci_on_stepchannel — converted from MQL5: MQL5 Indicators/CCI_On_StepChannel/cci_on_stepchannel.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [2330219, 16748574, 8421504, 9639167, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'CCI_On_StepChannel'}, 'levels': [100.0, 0.0, -100.0], 'description': [], 'name': 'cci_on_stepchannel', 'source': 'MQL5 Indicators/CCI_On_StepChannel/cci_on_stepchannel.mq5', 'folder': 'CCI_On_StepChannel', 'inputs': [{'mql': 'CCIPeriod', 'py': 'CCIPeriod', 'param': 'CCIPeriod', 'type': 'int', 'default': 14, 'label': 'Период CCI', 'sinput': False}, {'mql': 'MA_Method0', 'py': 'MA_Method0', 'param': 'MA_Method0', 'type': 'int', 'default': 0, 'label': 'Метод усреднения таймсерий', 'sinput': False}, {'mql': 'Length0', 'py': 'Length0', 'param': 'Length0', 'type': 'int', 'default': 3, 'label': 'Глубина усреднения таймсерий', 'sinput': False}, {'mql': 'Phase0', 'py': 'Phase0', 'param': 'Phase0', 'type': 'int', 'default': 15, 'label': 'Параметр усреднения таймсерий', 'sinput': False}, {'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 2, 'label': 'Метод усреднения скользящей средней', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'int', 'default': 10, 'label': 'Глубина усреднения скользящей средней', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'Параметр усреднения скользящей средней', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 0, 'label': 'метод сглаживания девиации', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'int', 'default': 70, 'label': 'Глубина сглаживания стандартного отклонения', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания стандартного отклонения', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'MA_Method3', 'py': 'MA_Method3', 'param': 'MA_Method3', 'type': 'int', 'default': 0, 'label': 'Метод сглаживания канала', 'sinput': False}, {'mql': 'Length3', 'py': 'Length3', 'param': 'Length3', 'type': 'int', 'default': 3, 'label': 'Глубина сглаживания канала', 'sinput': False}, {'mql': 'Phase3', 'py': 'Phase3', 'param': 'Phase3', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания канала,', 'sinput': False}, {'mql': 'BandsDeviation', 'py': 'BandsDeviation', 'param': 'BandsDeviation', 'type': 'double', 'default': 2.0, 'label': 'Отклонение', 'sinput': False}, {'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 2, 'label': 'Вариант алгоритма', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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

# enum MODE
ENAM_SIMPLE = 1
ENAM_HIBRID = 2
_enum('MODE', {1: 'ENAM_SIMPLE', 2: 'ENAM_HIBRID'})

# ---- inputs and global variables
CCIPeriod = _input('CCIPeriod', 14)  # Период CCI
MA_Method0 = _input('MA_Method0', MODE_SMA)  # Метод усреднения таймсерий
Length0 = _input('Length0', 3)  # Глубина усреднения таймсерий
Phase0 = _input('Phase0', 15)  # Параметр усреднения таймсерий
MA_Method1 = _input('MA_Method1', MODE_SMMA)  # Метод усреднения скользящей средней
Length1 = _input('Length1', 10)  # Глубина усреднения скользящей средней
Phase1 = _input('Phase1', 15)  # Параметр усреднения скользящей средней
MA_Method2 = _input('MA_Method2', MODE_SMA)  # метод сглаживания девиации
Length2 = _input('Length2', 70)  # Глубина сглаживания стандартного отклонения
Phase2 = _input('Phase2', 100)  # Параметр сглаживания стандартного отклонения
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
MA_Method3 = _input('MA_Method3', MODE_SMA)  # Метод сглаживания канала
Length3 = _input('Length3', 3)  # Глубина сглаживания канала
Phase3 = _input('Phase3', 100)  # Параметр сглаживания канала,
BandsDeviation = _input('BandsDeviation', 2.0)  # Отклонение
Mode = _input('Mode', ENAM_HIBRID)  # Вариант алгоритма
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
dMul = 0.0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
min_rates_3 = 0

def OnInit():
    global dMul, min_rates_1, min_rates_2, min_rates_3, min_rates_total
    min_rates_1 = GetStartBars(MA_Method1, Length1, Phase1) + 1
    min_rates_2 = min_rates_1 + Length1
    min_rates_total = min_rates_2 + GetStartBars(MA_Method2, Length2, Phase2)
    min_rates_0 = GetStartBars(MA_Method0, Length0, Phase0) + 1
    min_rates_3 = MathMax(min_rates_total, min_rates_0)
    min_rates_total = min_rates_3 + GetStartBars(MA_Method3, Length3, Phase3) + 1
    min_rates_total += CCIPeriod
    dMul = 0.015 / CCIPeriod
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    shortname = 'CCI_On_StepChannel'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_iClose_prev, _s_OnCalculate_iHigh_prev, _s_OnCalculate_iLow_prev
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    xma = 0.0
    stdev = 0.0
    xstdev = 0.0
    xlow = 0.0
    xhigh = 0.0
    xclose = 0.0
    base = 0.0
    base2 = 0.0
    Middle = 0.0
    xMiddle = 0.0
    dTmp = 0.0
    iLow_ = 0.0
    iHigh_ = 0.0
    iClose_ = 0.0
    ExtD = 0.0
    ExtM = 0.0
    first = 0
    bar = 0
    clr = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        _s_OnCalculate_iLow_prev = low[first]
        _s_OnCalculate_iHigh_prev = high[first]
        _s_OnCalculate_iClose_prev = close[first]
        bar = 0
        for bar in range(bar, min_rates_total + 1):
            IndBuffer[bar] = close[bar]
        else:
            bar = _range_end(bar, min_rates_total + 1, 1)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        iLow_ = low[bar]
        iHigh_ = high[bar]
        iClose_ = close[bar]
        price = PriceSeries(IPC, bar, open, low, high, close)
        xma = XMA1.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, price, bar, False)
        stdev = STD.StdDevSeries(min_rates_1, prev_calculated, rates_total, Length1, 1.0, price, xma, bar, False)
        xstdev = XMA2.XMASeries(min_rates_2, prev_calculated, rates_total, MA_Method2, Phase2, Length2, stdev, bar, False)
        base = xstdev * BandsDeviation
        base2 = base / 2.0
        xlow = XMA3.XMASeries(0, prev_calculated, rates_total, MA_Method0, Phase0, Length0, low[bar], bar, False)
        xhigh = XMA4.XMASeries(0, prev_calculated, rates_total, MA_Method0, Phase0, Length0, high[bar], bar, False)
        xclose = XMA5.XMASeries(0, prev_calculated, rates_total, MA_Method0, Phase0, Length0, close[bar], bar, False)
        if (xhigh - base) > _s_OnCalculate_iHigh_prev:
            iHigh_ = xhigh
        elif (xhigh + base) < _s_OnCalculate_iHigh_prev:
            iHigh_ = xhigh + base
        else:
            iHigh_ = _s_OnCalculate_iHigh_prev
        if (xlow + base) < _s_OnCalculate_iLow_prev:
            iLow_ = xlow
        elif (xlow - base) > _s_OnCalculate_iLow_prev:
            iLow_ = xlow - base
        else:
            iLow_ = _s_OnCalculate_iLow_prev
        _sw1 = Mode
        if _sw1 == ENAM_SIMPLE:
            if (xclose - base) > _s_OnCalculate_iClose_prev:
                iClose_ = xclose - base
            elif (xclose + base) < _s_OnCalculate_iClose_prev:
                iClose_ = xclose + base
            else:
                iClose_ = _s_OnCalculate_iClose_prev
            Middle = (iHigh_ + iLow_ + iClose_) / 3
        elif _sw1 == ENAM_HIBRID:
            if (xclose - base2) > _s_OnCalculate_iClose_prev:
                iClose_ = xclose - base2
            elif (xclose + base2) < _s_OnCalculate_iClose_prev:
                iClose_ = xclose + base2
            else:
                iClose_ = _s_OnCalculate_iClose_prev
            Middle = (iHigh_ + iLow_ + (2 * iClose_)) / 4
        xMiddle = XMA6.XMASeries(min_rates_3, prev_calculated, rates_total, MA_Method3, Phase3, Length3, Middle, bar, False)
        dTmp = 0.0
        for iii in range(0, CCIPeriod):
            dTmp += MathAbs(PriceSeries(IPC, MathMax(0, bar - iii), open, low, high, close) - xMiddle)
        ExtD = dTmp * dMul
        ExtM = PriceSeries(IPC, MathMax(0, bar), open, low, high, close) - xMiddle
        if ExtD:
            IndBuffer[bar] = _fdiv(ExtM, ExtD)
        else:
            IndBuffer[bar] = 0.0
        if bar < (rates_total - 1):
            _s_OnCalculate_iLow_prev = iLow_
            _s_OnCalculate_iHigh_prev = iHigh_
            _s_OnCalculate_iClose_prev = iClose_
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    bar = first
    for bar in range(bar, rates_total):
        clr = 2
        if IndBuffer[bar] > 0:
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                clr = 0
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                clr = 1
        if IndBuffer[bar] < 0:
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                clr = 3
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                clr = 4
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()
XMA3 = _alloc(CXMA)
XMA3.__init__()
XMA4 = _alloc(CXMA)
XMA4.__init__()
XMA5 = _alloc(CXMA)
XMA5.__init__()
XMA6 = _alloc(CXMA)
XMA6.__init__()
STD = _alloc(CStdDeviation)
STD.__init__()

# ---- static local variables
_s_OnCalculate_iLow_prev = 0.0
_s_OnCalculate_iHigh_prev = 0.0
_s_OnCalculate_iClose_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CciOnStepchannel(_MQL5Indicator):
    name = 'cci_on_stepchannel'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CCIPeriod': 14,  # Период CCI
        'MA_Method0': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения таймсерий
        'Length0': 3,  # Глубина усреднения таймсерий
        'Phase0': 15,  # Параметр усреднения таймсерий
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=2),  # Метод усреднения скользящей средней
        'Length1': 10,  # Глубина усреднения скользящей средней
        'Phase1': 15,  # Параметр усреднения скользящей средней
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод сглаживания девиации
        'Length2': 70,  # Глубина сглаживания стандартного отклонения
        'Phase2': 100,  # Параметр сглаживания стандартного отклонения
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'MA_Method3': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод сглаживания канала
        'Length3': 3,  # Глубина сглаживания канала
        'Phase3': 100,  # Параметр сглаживания канала,
        'BandsDeviation': 2.0,  # Отклонение
        'Mode': _Choice({1: 'Simple Mode', 2: 'hybrid Mode'}, default=2),  # Вариант алгоритма
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

