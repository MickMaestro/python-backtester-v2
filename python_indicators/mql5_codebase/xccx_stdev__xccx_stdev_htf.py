"""XCCX_StDev — converted from MQL5: MQL5 Indicators/XCCX_StDev_HTF/XCCX_StDev.mq5

Commodity Chanel Index
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 8, 2: 5, 3: 5}, 'colors': {1: [8421504, 16748574, 42495], 2: [255], 3: [10156544]}, 'widths': {1: 3, 2: 3, 3: 3}, 'styles': {1: 0}, 'labels': {1: 'XCCX', 2: 'Dn_Signal', 3: 'Up_Signal'}, 'levels': [-50.0, 50.0], 'description': ['Commodity Chanel Index'], 'name': 'XCCX_StDev', 'source': 'MQL5 Indicators/XCCX_StDev_HTF/XCCX_StDev.mq5', 'folder': 'XCCX_StDev_HTF', 'inputs': [{'mql': 'DSmoothMethod', 'py': 'DSmoothMethod', 'param': 'DSmoothMethod', 'type': 'int', 'default': 4, 'label': 'метод усреднения цены', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'uint', 'default': 15, 'label': 'период мувинга', 'sinput': False}, {'mql': 'DPhase', 'py': 'DPhase', 'param': 'DPhase', 'type': 'int', 'default': 15, 'label': 'параметр усреднения мувинга,', 'sinput': False}, {'mql': 'MSmoothMethod', 'py': 'MSmoothMethod', 'param': 'MSmoothMethod', 'type': 'int', 'default': 7, 'label': 'метод усреднения отклонения', 'sinput': False}, {'mql': 'MPeriod', 'py': 'MPeriod', 'param': 'MPeriod', 'type': 'uint', 'default': 15, 'label': 'период среднего отклонения', 'sinput': False}, {'mql': 'MPhase', 'py': 'MPhase', 'param': 'MPhase', 'type': 'int', 'default': 15, 'label': 'среднего отклонения,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 6, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'dK', 'py': 'dK', 'param': 'dK', 'type': 'double', 'default': 2.0, 'label': 'коэффициент для квадратичного фильтра', 'sinput': False}, {'mql': 'std_period', 'py': 'std_period', 'param': 'std_period', 'type': 'uint', 'default': 9, 'label': 'период квадратичного фильтра', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price
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
_enum('Applied_price', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
DSmoothMethod = _input('DSmoothMethod', MODE_JJMA)  # метод усреднения цены
DPeriod = _input('DPeriod', 15)  # период мувинга
DPhase = _input('DPhase', 15)  # параметр усреднения мувинга,
MSmoothMethod = _input('MSmoothMethod', MODE_T3)  # метод усреднения отклонения
MPeriod = _input('MPeriod', 15)  # период среднего отклонения
MPhase = _input('MPhase', 15)  # среднего отклонения,
IPC = _input('IPC', PRICE_TYPICAL_)  # ценовая константа
dK = _input('dK', 2.0)  # коэффициент для квадратичного фильтра
std_period = _input('std_period', 9)  # период квадратичного фильтра
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
XCCXBuffer = Arr(0, 0.0)
ColorXCCXBuffer = Arr(0, 0.0)
BearsBuffer = Arr(0, 0.0)
BullsBuffer = Arr(0, 0.0)
dXCCX = Arr(0, 0.0)
min_rates_total = 0
min_rates_D = 0
min_rates_M = 0

def OnInit():
    global min_rates_D, min_rates_M, min_rates_total
    min_rates_D = XMAD.GetStartBars(DSmoothMethod, DPeriod, DPhase)
    min_rates_M = XMAD.GetStartBars(MSmoothMethod, MPeriod, MPhase)
    min_rates_total = min_rates_D + min_rates_M + 1 + _int(std_period)
    XMAD.XMALengthCheck('DPeriod', DPeriod)
    XMAD.XMALengthCheck('MPeriod', MPeriod)
    XMAD.XMAPhaseCheck('DPhase', DPhase, DSmoothMethod)
    ArrayResize(dXCCX, std_period)
    SetIndexBuffer(0, XCCXBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorXCCXBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, BearsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, BullsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    SmoothD = ""
    SmoothM = ""
    SmoothD = XMAD.GetString_MA_Method(DSmoothMethod)
    SmoothM = XMAD.GetString_MA_Method(MSmoothMethod)
    StringConcatenate(shortname, 'Commodity Chanel Index(', _str(DPeriod), ',', _str(MPeriod), ',', SmoothD, ',', SmoothM, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    xma = 0.0
    upccx = 0.0
    dnccx = 0.0
    xupccx = 0.0
    xdnccx = 0.0
    SMAdif = 0.0
    Sum = 0.0
    StDev = 0.0
    dstd = 0.0
    BEARS = 0.0
    BULLS = 0.0
    Filter = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        xma = XMAD.XMASeries(0, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, price, bar, False)
        upccx = price - xma
        dnccx = MathAbs(upccx)
        xupccx = XMAH.XMASeries(min_rates_D, prev_calculated, rates_total, MSmoothMethod, MPhase, MPeriod, upccx, bar, False)
        xdnccx = XMAL.XMASeries(min_rates_D, prev_calculated, rates_total, MSmoothMethod, MPhase, MPeriod, dnccx, bar, False)
        if xupccx:
            XCCXBuffer[bar] = _fdiv(100 * xupccx, xdnccx)
        else:
            XCCXBuffer[bar] = EMPTY_VALUE
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    bar = first
    for bar in range(bar, rates_total):
        ColorXCCXBuffer[bar] = 0.0
        if XCCXBuffer[bar - 1] < XCCXBuffer[bar]:
            ColorXCCXBuffer[bar] = 1.0
        if XCCXBuffer[bar - 1] > XCCXBuffer[bar]:
            ColorXCCXBuffer[bar] = 2.0
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first
    for bar in range(bar, rates_total):
        for iii in range(0, _int(std_period)):
            dXCCX[iii] = XCCXBuffer[bar - iii] - XCCXBuffer[bar - iii - 1]
        Sum = 0.0
        for iii in range(0, _int(std_period)):
            Sum += dXCCX[iii]
        SMAdif = Sum / std_period
        Sum = 0.0
        for iii in range(0, _int(std_period)):
            Sum += MathPow(dXCCX[iii] - SMAdif, 2)
        StDev = MathSqrt(Sum / std_period)
        dstd = NormalizeDouble(dXCCX[0], Digits() + 2)
        Filter = NormalizeDouble(dK * StDev, Digits() + 2)
        BEARS = EMPTY_VALUE
        BULLS = EMPTY_VALUE
        if dstd < (-Filter):
            BEARS = XCCXBuffer[bar]
        if dstd > Filter:
            BULLS = XCCXBuffer[bar]
        BullsBuffer[bar] = BULLS
        BearsBuffer[bar] = BEARS
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMAD = _alloc(CXMA)
XMAD.__init__()
XMAH = _alloc(CXMA)
XMAH.__init__()
XMAL = _alloc(CXMA)
XMAL.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XCCXStDev(_MQL5Indicator):
    name = 'XCCX_StDev'
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
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=6),  # ценовая константа
        'dK': 2.0,  # коэффициент для квадратичного фильтра
        'std_period': 9,  # период квадратичного фильтра
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

