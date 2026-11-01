"""xrsx — converted from MQL5: MQL5 Indicators/ColorXRSXCandle/xrsx.mq5

Relative Strength Index
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 10, 2: 8}, 'colors': {1: [8421504, 32768, 16711680, 255, 16711935], 2: [8421504, 65280, 36095]}, 'widths': {1: 3, 2: 2}, 'styles': {1: 0, 2: 1}, 'labels': {1: 'XRSX', 2: 'Signal'}, 'levels': [-50.0, 50.0], 'description': ['Relative Strength Index'], 'name': 'xrsx', 'source': 'MQL5 Indicators/ColorXRSXCandle/xrsx.mq5', 'folder': 'ColorXRSXCandle', 'inputs': [{'mql': 'DSmoothMethod', 'py': 'DSmoothMethod', 'param': 'DSmoothMethod', 'type': 'int', 'default': 4, 'label': 'Метод усреднения цены', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'int', 'default': 15, 'label': 'Период скользящей средней', 'sinput': False}, {'mql': 'DPhase', 'py': 'DPhase', 'param': 'DPhase', 'type': 'int', 'default': 100, 'label': 'Параметр усреднения скользящей средней', 'sinput': False}, {'mql': 'SSmoothMethod', 'py': 'SSmoothMethod', 'param': 'SSmoothMethod', 'type': 'int', 'default': 5, 'label': 'Метод усреднения сигнальной линии', 'sinput': False}, {'mql': 'SPeriod', 'py': 'SPeriod', 'param': 'SPeriod', 'type': 'int', 'default': 7, 'label': 'Период сигнальной линии', 'sinput': False}, {'mql': 'SPhase', 'py': 'SPhase', 'param': 'SPhase', 'type': 'int', 'default': 100, 'label': 'Параметр сигнальной линии', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Style', 'py': 'Style', 'param': 'Style', 'type': 'int', 'default': 10, 'label': 'Стиль отображения XRSX', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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

# enum IndStyle
COLOR_LINE = 8
COLOR_HISTOGRAM = 10
COLOR_ARROW = 12
_enum('IndStyle', {8: 'COLOR_LINE', 10: 'COLOR_HISTOGRAM', 12: 'COLOR_ARROW'})

# ---- inputs and global variables
DSmoothMethod = _input('DSmoothMethod', MODE_JJMA)  # Метод усреднения цены
DPeriod = _input('DPeriod', 15)  # Период скользящей средней
DPhase = _input('DPhase', 100)  # Параметр усреднения скользящей средней
SSmoothMethod = _input('SSmoothMethod', MODE_JurX)  # Метод усреднения сигнальной линии
SPeriod = _input('SPeriod', 7)  # Период сигнальной линии
SPhase = _input('SPhase', 100)  # Параметр сигнальной линии
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
Style = _input('Style', COLOR_HISTOGRAM)  # Стиль отображения XRSX
XRSX = Arr(0, 0.0)
XXRSX = Arr(0, 0.0)
ColorXRSX = Arr(0, 0.0)
ColorXXRSX = Arr(0, 0.0)
StartBars = 0
StartBarsD = 0
StartBarsS = 0

def OnInit():
    global StartBars, StartBarsD, StartBarsS
    StartBarsD = UPXRSX.GetStartBars(DSmoothMethod, DPeriod, DPhase) + 1
    StartBarsS = StartBarsD + UPXRSX.GetStartBars(SSmoothMethod, SPeriod, SPhase)
    StartBars = StartBarsS
    UPXRSX.XMALengthCheck('DPeriod', DPeriod)
    UPXRSX.XMALengthCheck('SPeriod', SPeriod)
    UPXRSX.XMAPhaseCheck('DPhase', DPhase, DSmoothMethod)
    UPXRSX.XMAPhaseCheck('SPhase', SPhase, SSmoothMethod)
    SetIndexBuffer(0, XRSX, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(0, PLOT_LABEL, 'XRSX')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, Style)
    SetIndexBuffer(1, ColorXRSX, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBarsD + 1)
    SetIndexBuffer(2, XXRSX, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(2, PLOT_LABEL, 'Signal line')
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, ColorXXRSX, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, StartBars + 1)
    shortname = Box("")
    Smooth = ""
    Smooth = UPXRSX.GetString_MA_Method(DSmoothMethod)
    StringConcatenate(shortname, 'Relative Strength Index(', _str(DPeriod), ',', Smooth, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBars:
        return 0
    dprice_ = 0.0
    absdprice_ = 0.0
    up_xrsx = 0.0
    dn_xrsx = 0.0
    xrsx = 0.0
    xxrsx = 0.0
    first1 = 0
    first2 = 0
    first3 = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first1 = 1
        first2 = StartBarsD + 1
        first3 = StartBars + 1
    else:
        first1 = prev_calculated - 1
        first2 = first1
        first3 = first1
    bar = first1
    for bar in range(bar, rates_total):
        dprice_ = PriceSeries(IPC, bar, open, low, high, close) - PriceSeries(IPC, bar - 1, open, low, high, close)
        absdprice_ = MathAbs(dprice_)
        up_xrsx = UPXRSX.XMASeries(1, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, dprice_, bar, False)
        dn_xrsx = DNXRSX.XMASeries(1, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, absdprice_, bar, False)
        if dn_xrsx == 0:
            xrsx = EMPTY_VALUE
        else:
            xrsx = _fdiv(up_xrsx, dn_xrsx)
            if xrsx > 1:
                xrsx = 1.0
            if xrsx < -1:
                xrsx = -1.0
        XRSX[bar] = xrsx * 100
        xxrsx = XSIGN.XMASeries(StartBarsD, prev_calculated, rates_total, SSmoothMethod, SPhase, SPeriod, XRSX[bar], bar, False)
        XXRSX[bar] = xxrsx
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first2
    for bar in range(bar, rates_total):
        ColorXRSX[bar] = 0.0
        if XRSX[bar] > 0:
            if XRSX[bar] > XRSX[bar - 1]:
                ColorXRSX[bar] = 1.0
            if XRSX[bar] < XRSX[bar - 1]:
                ColorXRSX[bar] = 2.0
        if XRSX[bar] < 0:
            if XRSX[bar] < XRSX[bar - 1]:
                ColorXRSX[bar] = 3.0
            if XRSX[bar] > XRSX[bar - 1]:
                ColorXRSX[bar] = 4.0
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first3
    for bar in range(bar, rates_total):
        ColorXXRSX[bar] = 0.0
        if XRSX[bar] > XXRSX[bar - 1]:
            ColorXXRSX[bar] = 1.0
        if XRSX[bar] < XXRSX[bar - 1]:
            ColorXXRSX[bar] = 2.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
UPXRSX = _alloc(CXMA)
UPXRSX.__init__()
DNXRSX = _alloc(CXMA)
DNXRSX.__init__()
XSIGN = _alloc(CXMA)
XSIGN.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Xrsx(_MQL5Indicator):
    name = 'xrsx'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'DSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод усреднения цены
        'DPeriod': 15,  # Период скользящей средней
        'DPhase': 100,  # Параметр усреднения скользящей средней
        'SSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=5),  # Метод усреднения сигнальной линии
        'SPeriod': 7,  # Период сигнальной линии
        'SPhase': 100,  # Параметр сигнальной линии
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'Style': _Choice({8: 'цветная линия', 10: 'цветная гистограмма', 12: 'цветные значки'}, default=10),  # Стиль отображения XRSX
    }

