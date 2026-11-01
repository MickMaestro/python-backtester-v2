"""XRSXCandleKeltner — converted from MQL5: MQL5 Indicators/XRSXCandleKeltner/XRSXCandleKeltner.mq5

XRSXCandle
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 2}, 'types': {1: 17, 2: 7}, 'colors': {1: [255, 8421504, 16760576], 2: [16443110]}, 'widths': {}, 'styles': {}, 'labels': {1: 'XRSXCandle Open;XRSXCandle High;XRSXCandle Low;XRSXCandle Close', 2: 'Channels'}, 'levels': [-50.0, 50.0], 'description': ['XRSXCandle'], 'name': 'XRSXCandleKeltner', 'source': 'MQL5 Indicators/XRSXCandleKeltner/XRSXCandleKeltner.mq5', 'folder': 'XRSXCandleKeltner', 'inputs': [{'mql': 'DSmoothMethod', 'py': 'DSmoothMethod', 'param': 'DSmoothMethod', 'type': 'int', 'default': 4, 'label': 'метод усреднения цены', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'int', 'default': 15, 'label': 'период мувинга', 'sinput': False}, {'mql': 'DPhase', 'py': 'DPhase', 'param': 'DPhase', 'type': 'int', 'default': 100, 'label': 'параметр усреднения мувинга,', 'sinput': False}, {'mql': 'SSmoothMethod', 'py': 'SSmoothMethod', 'param': 'SSmoothMethod', 'type': 'int', 'default': 5, 'label': 'метод сглаживания индикатора', 'sinput': False}, {'mql': 'SPeriod', 'py': 'SPeriod', 'param': 'SPeriod', 'type': 'int', 'default': 7, 'label': 'период сглаживания индикатора', 'sinput': False}, {'mql': 'SPhase', 'py': 'SPhase', 'param': 'SPhase', 'type': 'int', 'default': 100, 'label': 'параметр сглаживания индикатора,', 'sinput': False}, {'mql': 'KeltnerPeriod', 'py': 'KeltnerPeriod', 'param': 'KeltnerPeriod', 'type': 'uint', 'default': 100, 'label': 'период усреднения Кёлтнера', 'sinput': False}, {'mql': 'Ratio', 'py': 'Ratio', 'param': 'Ratio', 'type': 'double', 'default': 4.01, 'label': 'девиация канала', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг канала по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
DSmoothMethod = _input('DSmoothMethod', MODE_JJMA)  # метод усреднения цены
DPeriod = _input('DPeriod', 15)  # период мувинга
DPhase = _input('DPhase', 100)  # параметр усреднения мувинга,
SSmoothMethod = _input('SSmoothMethod', MODE_JurX)  # метод сглаживания индикатора
SPeriod = _input('SPeriod', 7)  # период сглаживания индикатора
SPhase = _input('SPhase', 100)  # параметр сглаживания индикатора,
KeltnerPeriod = _input('KeltnerPeriod', 100)  # период усреднения Кёлтнера
Ratio = _input('Ratio', 4.01)  # девиация канала
Shift = _input('Shift', 0)  # сдвиг канала по горизонтали в барах
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
    min_rates_2 = min_rates_1 + GetStartBars(SSmoothMethod, SPeriod, SPhase)
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
    short_name = 'XRSXCandleKeltner'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    MA = 0.0
    dprice = 0.0
    absdprice = 0.0
    up_xrsx = 0.0
    dn_xrsx = 0.0
    xrsx = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        dprice = open[bar] - open[bar - 1]
        absdprice = MathAbs(dprice)
        up_xrsx = OUPXRSX.XMASeries(1, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, dprice, bar, False)
        dn_xrsx = ODNXRSX.XMASeries(1, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, absdprice, bar, False)
        if not dn_xrsx:
            xrsx = EMPTY_VALUE
        else:
            xrsx = _fdiv(up_xrsx, dn_xrsx)
            if xrsx > 1:
                xrsx = 1.0
            if xrsx < -1:
                xrsx = -1.0
        ExtOpenBuffer[bar] = 100 * OXSIGN.XMASeries(min_rates_1, prev_calculated, rates_total, SSmoothMethod, SPhase, SPeriod, xrsx, bar, False)
        dprice = close[bar] - close[bar - 1]
        absdprice = MathAbs(dprice)
        up_xrsx = CUPXRSX.XMASeries(1, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, dprice, bar, False)
        dn_xrsx = CDNXRSX.XMASeries(1, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, absdprice, bar, False)
        if not dn_xrsx:
            xrsx = EMPTY_VALUE
        else:
            xrsx = _fdiv(up_xrsx, dn_xrsx)
            if xrsx > 1:
                xrsx = 1.0
            if xrsx < -1:
                xrsx = -1.0
        ExtCloseBuffer[bar] = 100 * CXSIGN.XMASeries(min_rates_1, prev_calculated, rates_total, SSmoothMethod, SPhase, SPeriod, xrsx, bar, False)
        dprice = high[bar] - high[bar - 1]
        absdprice = MathAbs(dprice)
        up_xrsx = HUPXRSX.XMASeries(1, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, dprice, bar, False)
        dn_xrsx = HDNXRSX.XMASeries(1, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, absdprice, bar, False)
        if not dn_xrsx:
            xrsx = EMPTY_VALUE
        else:
            xrsx = _fdiv(up_xrsx, dn_xrsx)
            if xrsx > 1:
                xrsx = 1.0
            if xrsx < -1:
                xrsx = -1.0
        ExtHighBuffer[bar] = 100 * HXSIGN.XMASeries(min_rates_1, prev_calculated, rates_total, SSmoothMethod, SPhase, SPeriod, xrsx, bar, False)
        dprice = low[bar] - low[bar - 1]
        absdprice = MathAbs(dprice)
        up_xrsx = LUPXRSX.XMASeries(1, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, dprice, bar, False)
        dn_xrsx = LDNXRSX.XMASeries(1, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, absdprice, bar, False)
        if not dn_xrsx:
            xrsx = EMPTY_VALUE
        else:
            xrsx = _fdiv(up_xrsx, dn_xrsx)
            if xrsx > 1:
                xrsx = 1.0
            if xrsx < -1:
                xrsx = -1.0
        ExtLowBuffer[bar] = 100 * LXSIGN.XMASeries(min_rates_1, prev_calculated, rates_total, SSmoothMethod, SPhase, SPeriod, xrsx, bar, False)
        Max = MathMax(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        Min = MathMin(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        ExtHighBuffer[bar] = MathMax(Max, ExtHighBuffer[bar])
        ExtLowBuffer[bar] = MathMin(Min, ExtLowBuffer[bar])
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 2.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_2
    bar = first
    for bar in range(bar, rates_total):
        MA = XXMA.XMASeries(min_rates_2, prev_calculated, rates_total, MODE_SMA_, 0, KeltnerPeriod, ExtCloseBuffer[bar], bar, False)
        if bar < min_rates_total:
            continue
        Keltner = Ratio * GetKeltner(KeltnerPeriod, bar, ExtHighBuffer, ExtLowBuffer)
        BorderTopBuffer[bar] = MA + Keltner
        BorderBotBuffer[bar] = MA - Keltner
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
OUPXRSX = _alloc(CXMA)
OUPXRSX.__init__()
ODNXRSX = _alloc(CXMA)
ODNXRSX.__init__()
OXSIGN = _alloc(CXMA)
OXSIGN.__init__()
HUPXRSX = _alloc(CXMA)
HUPXRSX.__init__()
HDNXRSX = _alloc(CXMA)
HDNXRSX.__init__()
HXSIGN = _alloc(CXMA)
HXSIGN.__init__()
LUPXRSX = _alloc(CXMA)
LUPXRSX.__init__()
LDNXRSX = _alloc(CXMA)
LDNXRSX.__init__()
LXSIGN = _alloc(CXMA)
LXSIGN.__init__()
CUPXRSX = _alloc(CXMA)
CUPXRSX.__init__()
CDNXRSX = _alloc(CXMA)
CDNXRSX.__init__()
CXSIGN = _alloc(CXMA)
CXSIGN.__init__()
XXMA = _alloc(CXMA)
XXMA.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XRSXCandleKeltner(_MQL5Indicator):
    name = 'XRSXCandleKeltner'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'DSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения цены
        'DPeriod': 15,  # период мувинга
        'DPhase': 100,  # параметр усреднения мувинга,
        'SSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=5),  # метод сглаживания индикатора
        'SPeriod': 7,  # период сглаживания индикатора
        'SPhase': 100,  # параметр сглаживания индикатора,
        'KeltnerPeriod': 100,  # период усреднения Кёлтнера
        'Ratio': 4.01,  # девиация канала
        'Shift': 0,  # сдвиг канала по горизонтали в барах
    }

