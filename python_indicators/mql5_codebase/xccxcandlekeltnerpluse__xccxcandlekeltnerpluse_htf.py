"""XCCXCandleKeltnerPluse — converted from MQL5: MQL5 Indicators/XCCXCandleKeltnerPluse_HTF/XCCXCandleKeltnerPluse.mq5

XCCXCandle
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 2}, 'types': {1: 17, 2: 7}, 'colors': {1: [255, 11823615, 8421504, 8421376, 65280], 2: [16443110]}, 'widths': {}, 'styles': {}, 'labels': {1: 'XCCXCandle Open;XCCXCandle High;XCCXCandle Low;XCCXCandle Close', 2: 'Channels'}, 'levels': [], 'description': ['XCCXCandle'], 'name': 'XCCXCandleKeltnerPluse', 'source': 'MQL5 Indicators/XCCXCandleKeltnerPluse_HTF/XCCXCandleKeltnerPluse.mq5', 'folder': 'XCCXCandleKeltnerPluse_HTF', 'inputs': [{'mql': 'DSmoothMethod', 'py': 'DSmoothMethod', 'param': 'DSmoothMethod', 'type': 'int', 'default': 4, 'label': 'метод усреднения цены', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'int', 'default': 15, 'label': 'период мувинга', 'sinput': False}, {'mql': 'DPhase', 'py': 'DPhase', 'param': 'DPhase', 'type': 'int', 'default': 15, 'label': 'параметр усреднения мувинга,', 'sinput': False}, {'mql': 'MSmoothMethod', 'py': 'MSmoothMethod', 'param': 'MSmoothMethod', 'type': 'int', 'default': 7, 'label': 'метод усреднения отклонения', 'sinput': False}, {'mql': 'MPeriod', 'py': 'MPeriod', 'param': 'MPeriod', 'type': 'int', 'default': 15, 'label': 'период среднего отклонения', 'sinput': False}, {'mql': 'MPhase', 'py': 'MPhase', 'param': 'MPhase', 'type': 'int', 'default': 15, 'label': 'среднего отклонения,', 'sinput': False}, {'mql': 'KeltnerPeriod', 'py': 'KeltnerPeriod', 'param': 'KeltnerPeriod', 'type': 'uint', 'default': 100, 'label': 'период усреднения Келтнера', 'sinput': False}, {'mql': 'Ratio', 'py': 'Ratio', 'param': 'Ratio', 'type': 'double', 'default': 4.01, 'label': 'девиация канала', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг канала по горизонтали в барах', 'sinput': False}, {'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 1, 'label': 'метод индикации пробоя', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 50, 'label': '', 'sinput': False}, {'mql': 'MiddleLevel', 'py': 'MiddleLevel', 'param': 'MiddleLevel', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': -50, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum ENUM_COLOR_MODE
ENUM_LEVELES = 1
ENUM__CHANELS = 2
_enum('ENUM_COLOR_MODE', {1: 'ENUM_LEVELES', 2: 'ENUM__CHANELS'})

# ---- inputs and global variables
DSmoothMethod = _input('DSmoothMethod', MODE_JJMA)  # метод усреднения цены
DPeriod = _input('DPeriod', 15)  # период мувинга
DPhase = _input('DPhase', 15)  # параметр усреднения мувинга,
MSmoothMethod = _input('MSmoothMethod', MODE_T3)  # метод усреднения отклонения
MPeriod = _input('MPeriod', 15)  # период среднего отклонения
MPhase = _input('MPhase', 15)  # среднего отклонения,
KeltnerPeriod = _input('KeltnerPeriod', 100)  # период усреднения Келтнера
Ratio = _input('Ratio', 4.01)  # девиация канала
Shift = _input('Shift', 0)  # сдвиг канала по горизонтали в барах
Mode = _input('Mode', ENUM_LEVELES)  # метод индикации пробоя
HighLevel = _input('HighLevel', 50)
MiddleLevel = _input('MiddleLevel', 0)
LowLevel = _input('LowLevel', -50)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
BorderTopBuffer = Arr(0, 0.0)
BorderBotBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0

def OnInit():
    global min_rates_1, min_rates_2, min_rates_total
    min_rates_1 = GetStartBars(DSmoothMethod, DPeriod, DPhase) + 1
    min_rates_2 = min_rates_1 + GetStartBars(MSmoothMethod, MPeriod, MPhase)
    min_rates_total = min_rates_2 + _int(KeltnerPeriod)
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, BorderTopBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, BorderBotBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    short_name = 'XCCXCandleKeltner'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, MiddleLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrGreen)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrBrown)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    MA = 0.0
    price = 0.0
    xma = 0.0
    upccx = 0.0
    dnccx = 0.0
    xupccx = 0.0
    xdnccx = 0.0
    xccx = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = open[bar]
        xma = OXXMA.XMASeries(0, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, price, bar, False)
        upccx = price - xma
        dnccx = MathAbs(upccx)
        xupccx = OUPXCCX.XMASeries(min_rates_1, prev_calculated, rates_total, MSmoothMethod, MPhase, MPeriod, upccx, bar, False)
        xdnccx = ODNXCCX.XMASeries(min_rates_1, prev_calculated, rates_total, MSmoothMethod, MPhase, MPeriod, dnccx, bar, False)
        if xupccx:
            xccx = _fdiv(100 * xupccx, xdnccx)
        else:
            xccx = EMPTY_VALUE
        ExtOpenBuffer[bar] = xccx
        price = close[bar]
        xma = CXXMA.XMASeries(0, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, price, bar, False)
        upccx = price - xma
        dnccx = MathAbs(upccx)
        xupccx = CUPXCCX.XMASeries(min_rates_1, prev_calculated, rates_total, MSmoothMethod, MPhase, MPeriod, upccx, bar, False)
        xdnccx = CDNXCCX.XMASeries(min_rates_1, prev_calculated, rates_total, MSmoothMethod, MPhase, MPeriod, dnccx, bar, False)
        if xupccx:
            xccx = _fdiv(100 * xupccx, xdnccx)
        else:
            xccx = EMPTY_VALUE
        ExtCloseBuffer[bar] = xccx
        price = high[bar]
        xma = HXXMA.XMASeries(0, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, price, bar, False)
        upccx = price - xma
        dnccx = MathAbs(upccx)
        xupccx = HUPXCCX.XMASeries(min_rates_1, prev_calculated, rates_total, MSmoothMethod, MPhase, MPeriod, upccx, bar, False)
        xdnccx = HDNXCCX.XMASeries(min_rates_1, prev_calculated, rates_total, MSmoothMethod, MPhase, MPeriod, dnccx, bar, False)
        if xupccx:
            xccx = _fdiv(100 * xupccx, xdnccx)
        else:
            xccx = EMPTY_VALUE
        ExtHighBuffer[bar] = xccx
        price = low[bar]
        xma = LXXMA.XMASeries(0, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, price, bar, False)
        upccx = price - xma
        dnccx = MathAbs(upccx)
        xupccx = LUPXCCX.XMASeries(min_rates_1, prev_calculated, rates_total, MSmoothMethod, MPhase, MPeriod, upccx, bar, False)
        xdnccx = LDNXCCX.XMASeries(min_rates_1, prev_calculated, rates_total, MSmoothMethod, MPhase, MPeriod, dnccx, bar, False)
        if xupccx:
            xccx = _fdiv(100 * xupccx, xdnccx)
        else:
            xccx = EMPTY_VALUE
        ExtLowBuffer[bar] = xccx
        Max = MathMax(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        Min = MathMin(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        ExtHighBuffer[bar] = MathMax(Max, ExtHighBuffer[bar])
        ExtLowBuffer[bar] = MathMin(Min, ExtLowBuffer[bar])
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 3.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 1.0
        else:
            ExtColorBuffer[bar] = 2.0
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_2
    bar = first
    for bar in range(bar, rates_total):
        MA = XMA.XMASeries(min_rates_2, prev_calculated, rates_total, MODE_SMA_, 0, KeltnerPeriod, ExtCloseBuffer[bar], bar, False)
        if bar < min_rates_total:
            continue
        Keltner = Ratio * GetKeltner(KeltnerPeriod, bar, ExtHighBuffer, ExtLowBuffer)
        BorderTopBuffer[bar] = MA + Keltner
        BorderBotBuffer[bar] = MA - Keltner
    else:
        bar = _range_end(bar, rates_total, 1)
    if Mode == ENUM_LEVELES:
        bar = first
        for bar in range(bar, rates_total):
            if ExtCloseBuffer[bar] > HighLevel:
                ExtColorBuffer[bar] = 4.0
            elif ExtCloseBuffer[bar] < LowLevel:
                ExtColorBuffer[bar] = 0.0
        else:
            bar = _range_end(bar, rates_total, 1)
    else:
        bar = first
        for bar in range(bar, rates_total):
            if ExtCloseBuffer[bar] > BorderTopBuffer[bar]:
                ExtColorBuffer[bar] = 4.0
            elif ExtCloseBuffer[bar] < BorderBotBuffer[bar]:
                ExtColorBuffer[bar] = 0.0
        else:
            bar = _range_end(bar, rates_total, 1)
    return rates_total

def GetKeltner(period, bar, High, Low):
    Resalt = 0.0
    sum_ = 0.0
    for iii in range(0, period):
        sum_ += High[bar - iii] - Low[bar - iii]
    Resalt = _fdiv(sum_, period)
    return Resalt

# ---- global variables initialised from expressions
OUPXCCX = _alloc(CXMA)
OUPXCCX.__init__()
ODNXCCX = _alloc(CXMA)
ODNXCCX.__init__()
OXXMA = _alloc(CXMA)
OXXMA.__init__()
HUPXCCX = _alloc(CXMA)
HUPXCCX.__init__()
HDNXCCX = _alloc(CXMA)
HDNXCCX.__init__()
HXXMA = _alloc(CXMA)
HXXMA.__init__()
LUPXCCX = _alloc(CXMA)
LUPXCCX.__init__()
LDNXCCX = _alloc(CXMA)
LDNXCCX.__init__()
LXXMA = _alloc(CXMA)
LXXMA.__init__()
CUPXCCX = _alloc(CXMA)
CUPXCCX.__init__()
CDNXCCX = _alloc(CXMA)
CDNXCCX.__init__()
CXXMA = _alloc(CXMA)
CXXMA.__init__()
XMA = _alloc(CXMA)
XMA.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XCCXCandleKeltnerPluse(_MQL5Indicator):
    name = 'XCCXCandleKeltnerPluse'
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
        'KeltnerPeriod': 100,  # период усреднения Келтнера
        'Ratio': 4.01,  # девиация канала
        'Shift': 0,  # сдвиг канала по горизонтали в барах
        'Mode': _Choice({1: 'по уровням перекупленности/перепроданности', 2: 'по границам канала Келтнера'}, default=1),  # метод индикации пробоя
        'HighLevel': 50,
        'MiddleLevel': 0,
        'LowLevel': -50,
    }

