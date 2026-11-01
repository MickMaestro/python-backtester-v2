"""XCCX_BB — converted from MQL5: MQL5 Indicators/XCCX/XCCX_BB.mq5

Relative Strength Index
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 7}, 'types': {1: 10, 2: 8, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'colors': {1: [8421504, 32768, 16711680, 255, 16711935], 2: [8421504, 16776960, 36095], 3: [14822282], 4: [9639167], 5: [8421504], 6: [9639167], 7: [14822282]}, 'widths': {1: 3, 2: 2, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'styles': {1: 0, 2: 1, 3: 4, 4: 4, 5: 4, 6: 4, 7: 4}, 'labels': {1: 'XCCX', 2: 'Signal line', 3: '+2Sigma', 4: '+Sigma', 5: 'Middle', 6: '-Sigma', 7: '-2Sigma'}, 'levels': [], 'description': ['Relative Strength Index'], 'name': 'XCCX_BB', 'source': 'MQL5 Indicators/XCCX/XCCX_BB.mq5', 'folder': 'XCCX', 'inputs': [{'mql': 'DSmoothMethod', 'py': 'DSmoothMethod', 'param': 'DSmoothMethod', 'type': 'int', 'default': 4, 'label': 'метод усреднения цены', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'uint', 'default': 15, 'label': 'период мувинга', 'sinput': False}, {'mql': 'DPhase', 'py': 'DPhase', 'param': 'DPhase', 'type': 'int', 'default': 15, 'label': 'параметр усреднения мувинга,', 'sinput': False}, {'mql': 'MSmoothMethod', 'py': 'MSmoothMethod', 'param': 'MSmoothMethod', 'type': 'int', 'default': 7, 'label': 'метод усреднения отклонения', 'sinput': False}, {'mql': 'MPeriod', 'py': 'MPeriod', 'param': 'MPeriod', 'type': 'uint', 'default': 15, 'label': 'период среднего отклонения', 'sinput': False}, {'mql': 'MPhase', 'py': 'MPhase', 'param': 'MPhase', 'type': 'int', 'default': 15, 'label': 'среднего отклонения,', 'sinput': False}, {'mql': 'SSmoothMethod', 'py': 'SSmoothMethod', 'param': 'SSmoothMethod', 'type': 'int', 'default': 7, 'label': 'метод усреднения сигнальной линии', 'sinput': False}, {'mql': 'SPeriod', 'py': 'SPeriod', 'param': 'SPeriod', 'type': 'uint', 'default': 7, 'label': 'период сигнальной линии', 'sinput': False}, {'mql': 'SPhase', 'py': 'SPhase', 'param': 'SPhase', 'type': 'int', 'default': 15, 'label': 'параметр сигнальной линии,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Style', 'py': 'Style', 'param': 'Style', 'type': 'int', 'default': 10, 'label': 'стиль отображения XCCX', 'sinput': False}, {'mql': 'BBPeriod', 'py': 'BBPeriod', 'param': 'BBPeriod', 'type': 'int', 'default': 100, 'label': 'период для уровней Боллинджера', 'sinput': False}, {'mql': 'BBDeviation1', 'py': 'BBDeviation1', 'param': 'BBDeviation1', 'type': 'double', 'default': 1.0, 'label': 'малая девиация', 'sinput': False}, {'mql': 'BBDeviation2', 'py': 'BBDeviation2', 'param': 'BBDeviation2', 'type': 'double', 'default': 1.6, 'label': 'большая девиация', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
DSmoothMethod = _input('DSmoothMethod', MODE_JJMA)  # метод усреднения цены
DPeriod = _input('DPeriod', 15)  # период мувинга
DPhase = _input('DPhase', 15)  # параметр усреднения мувинга,
MSmoothMethod = _input('MSmoothMethod', MODE_T3)  # метод усреднения отклонения
MPeriod = _input('MPeriod', 15)  # период среднего отклонения
MPhase = _input('MPhase', 15)  # среднего отклонения,
SSmoothMethod = _input('SSmoothMethod', MODE_T3)  # метод усреднения сигнальной линии
SPeriod = _input('SPeriod', 7)  # период сигнальной линии
SPhase = _input('SPhase', 15)  # параметр сигнальной линии,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
Style = _input('Style', COLOR_HISTOGRAM)  # стиль отображения XCCX
BBPeriod = _input('BBPeriod', 100)  # период для уровней Боллинджера
BBDeviation1 = _input('BBDeviation1', 1.0)  # малая девиация
BBDeviation2 = _input('BBDeviation2', 1.6)  # большая девиация
XCCX = Arr(0, 0.0)
XXCCX = Arr(0, 0.0)
ColorXCCX = Arr(0, 0.0)
ColorXXCCX = Arr(0, 0.0)
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
ExtLineBuffer4 = Arr(0, 0.0)
ExtLineBuffer5 = Arr(0, 0.0)
quotient = 0.0
StartBars = 0
StartBarsD = 0
StartBarsS = 0
StartBarsM = 0
StartBarsB = 0

def OnInit():
    global StartBars, StartBarsB, StartBarsD, StartBarsM, StartBarsS, quotient
    StartBarsD = XMA.GetStartBars(DSmoothMethod, DPeriod, DPhase) + 1
    StartBarsM = StartBarsD + XMA.GetStartBars(MSmoothMethod, MPeriod, MPhase)
    StartBarsS = StartBarsM + XMA.GetStartBars(SSmoothMethod, SPeriod, SPhase)
    StartBarsB = StartBarsM + BBPeriod
    StartBars = MathMax(StartBarsS, StartBarsB)
    XMA.XMALengthCheck('DPeriod', DPeriod)
    XMA.XMALengthCheck('MPeriod', MPeriod)
    XMA.XMALengthCheck('BBPeriod', BBPeriod)
    XMA.XMAPhaseCheck('DPhase', DPhase, DSmoothMethod)
    quotient = BBDeviation2 / BBDeviation1
    SetIndexBuffer(0, XCCX, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBarsM + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_DRAW_TYPE, Style)
    SetIndexBuffer(1, ColorXCCX, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBarsM + 1)
    SetIndexBuffer(2, XXCCX, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, StartBarsS + 1)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, ColorXXCCX, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, StartBarsS + 1)
    SetIndexBuffer(4, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(5, ExtLineBuffer2, INDICATOR_DATA)
    SetIndexBuffer(6, ExtLineBuffer3, INDICATOR_DATA)
    SetIndexBuffer(7, ExtLineBuffer4, INDICATOR_DATA)
    SetIndexBuffer(8, ExtLineBuffer5, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(7, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(8, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(7, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(8, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    SmoothD = ""
    SmoothM = ""
    SmoothD = XMA.GetString_MA_Method(DSmoothMethod)
    SmoothM = XMA.GetString_MA_Method(MSmoothMethod)
    StringConcatenate(shortname, 'Commodity Chanel Index(', _str(DPeriod), ',', _str(MPeriod), ',', SmoothD, ',', SmoothM, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBars:
        return 0
    price_ = 0.0
    xma = 0.0
    upccx = 0.0
    dnccx = 0.0
    xupccx = 0.0
    xdnccx = 0.0
    xxccx = 0.0
    stdev1 = 0.0
    stdev2 = 0.0
    first1 = 0
    first2 = 0
    first3 = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first1 = 0
        first2 = StartBarsD + 1
        first3 = StartBarsS + 1
    else:
        first1 = prev_calculated - 1
        first2 = first1
        first3 = first1
    bar = first1
    for bar in range(bar, rates_total):
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        XCCX[bar] = EMPTY_VALUE
        xma = XMAD.XMASeries(0, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, price_, bar, False)
        if bar < StartBarsD:
            continue
        upccx = price_ - xma
        dnccx = MathAbs(upccx)
        xupccx = UPXCCX.XMASeries(StartBarsD, prev_calculated, rates_total, MSmoothMethod, MPhase, MPeriod, upccx, bar, False)
        xdnccx = DNXCCX.XMASeries(StartBarsD, prev_calculated, rates_total, MSmoothMethod, MPhase, MPeriod, dnccx, bar, False)
        if xupccx != 0.0:
            XCCX[bar] = _fdiv(100 * xupccx, xdnccx)
        xxccx = XSIGN.XMASeries(StartBarsM, prev_calculated, rates_total, SSmoothMethod, SPhase, SPeriod, XCCX[bar], bar, False)
        XXCCX[bar] = xxccx
        xma = XMA.XMASeries(StartBarsD + 1, prev_calculated, rates_total, MODE_SMA_, 0, BBPeriod, XCCX[bar], bar, False)
        stdev1 = STD.StdDevSeries(StartBarsB, prev_calculated, rates_total, BBPeriod, BBDeviation1, XCCX[bar], xma, bar, False)
        stdev2 = stdev1 * quotient
        if bar <= (StartBarsB + BBPeriod):
            xma = EMPTY_VALUE
            stdev1 = 0.0
            stdev2 = 0.0
        ExtLineBuffer1[bar] = xma + stdev2
        ExtLineBuffer2[bar] = xma + stdev1
        ExtLineBuffer3[bar] = xma
        ExtLineBuffer4[bar] = xma - stdev1
        ExtLineBuffer5[bar] = xma - stdev2
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first2
    for bar in range(bar, rates_total):
        ColorXCCX[bar] = 0.0
        if XCCX[bar] > 0:
            if XCCX[bar] > XCCX[bar - 1]:
                ColorXCCX[bar] = 1.0
            if XCCX[bar] < XCCX[bar - 1]:
                ColorXCCX[bar] = 2.0
        if XCCX[bar] < 0:
            if XCCX[bar] < XCCX[bar - 1]:
                ColorXCCX[bar] = 3.0
            if XCCX[bar] > XCCX[bar - 1]:
                ColorXCCX[bar] = 4.0
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first3
    for bar in range(bar, rates_total):
        ColorXXCCX[bar] = 0.0
        if XCCX[bar] > XXCCX[bar - 1]:
            ColorXXCCX[bar] = 1.0
        if XCCX[bar] < XXCCX[bar - 1]:
            ColorXXCCX[bar] = 2.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMAD = _alloc(CXMA)
XMAD.__init__()
UPXCCX = _alloc(CXMA)
UPXCCX.__init__()
DNXCCX = _alloc(CXMA)
DNXCCX.__init__()
XSIGN = _alloc(CXMA)
XSIGN.__init__()
XMA = _alloc(CXMA)
XMA.__init__()
STD = _alloc(CStdDeviation)
STD.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XCCXBB(_MQL5Indicator):
    name = 'XCCX_BB'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'DSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения цены
        'DPeriod': 15,  # период мувинга
        'DPhase': 15,  # параметр усреднения мувинга,
        'MSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # метод усреднения отклонения
        'MPeriod': 15,  # период среднего отклонения
        'MPhase': 15,  # среднего отклонения,
        'SSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # метод усреднения сигнальной линии
        'SPeriod': 7,  # период сигнальной линии
        'SPhase': 15,  # параметр сигнальной линии,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'Style': _Choice({8: 'Цветная линия', 10: 'Цветная гистограмма', 12: 'Цветные значки'}, default=10),  # стиль отображения XCCX
        'BBPeriod': 100,  # период для уровней Боллинджера
        'BBDeviation1': 1.0,  # малая девиация
        'BBDeviation2': 1.6,  # большая девиация
    }

