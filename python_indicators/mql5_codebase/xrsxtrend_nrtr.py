"""XRSXTrend_NRTR — converted from MQL5: MQL5 Indicators/XRSXTrend_NRTR/XRSXTrend_NRTR.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 5, 4: 5, 5: 5, 6: 5}, 'colors': {1: [16776960], 2: [55295], 3: [16748574], 4: [36095], 5: [16711680], 6: [16711935]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2, 5: 5, 6: 5}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'NRTR Line Up', 2: 'NRTR Line Down', 3: 'NRTR Up', 4: 'NRTR Down', 5: 'Buy XRSXTrend signal', 6: 'Sell XRSXTrend signal'}, 'levels': [], 'description': [], 'name': 'XRSXTrend_NRTR', 'source': 'MQL5 Indicators/XRSXTrend_NRTR/XRSXTrend_NRTR.mq5', 'folder': 'XRSXTrend_NRTR', 'inputs': [{'mql': 'RISK', 'py': 'RISK', 'param': 'RISK', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'DSmoothMethod', 'py': 'DSmoothMethod', 'param': 'DSmoothMethod', 'type': 'int', 'default': 4, 'label': 'метод усреднения цены', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'int', 'default': 12, 'label': 'период мувинга', 'sinput': False}, {'mql': 'DPhase', 'py': 'DPhase', 'param': 'DPhase', 'type': 'int', 'default': 100, 'label': 'параметр усреднения мувинга,', 'sinput': False}, {'mql': 'SSmoothMethod', 'py': 'SSmoothMethod', 'param': 'SSmoothMethod', 'type': 'int', 'default': 4, 'label': 'метод усреднения сигнальной линии', 'sinput': False}, {'mql': 'SPeriod', 'py': 'SPeriod', 'param': 'SPeriod', 'type': 'int', 'default': 7, 'label': 'период сигнальной линии', 'sinput': False}, {'mql': 'SPhase', 'py': 'SPhase', 'param': 'SPhase', 'type': 'int', 'default': 100, 'label': 'параметр сигнальной линии,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'AtrRatio', 'py': 'AtrRatio', 'param': 'AtrRatio', 'type': 'double', 'default': 0.375, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
RISK = _input('RISK', 2)
DSmoothMethod = _input('DSmoothMethod', MODE_JJMA)  # метод усреднения цены
DPeriod = _input('DPeriod', 12)  # период мувинга
DPhase = _input('DPhase', 100)  # параметр усреднения мувинга,
SSmoothMethod = _input('SSmoothMethod', MODE_JJMA)  # метод усреднения сигнальной линии
SPeriod = _input('SPeriod', 7)  # период сигнальной линии
SPhase = _input('SPhase', 100)  # параметр сигнальной линии,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
AtrRatio = _input('AtrRatio', 0.375)
UpBuffer1 = Arr(0, 0.0)
DnBuffer1 = Arr(0, 0.0)
UpBuffer2 = Arr(0, 0.0)
DnBuffer2 = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
Kx = 0
ATR_Handle = 0
min_rates_total = 0
min_rates_D = 0
min_rates_S = 0

def OnInit():
    global ATR_Handle, Kx, min_rates_D, min_rates_S, min_rates_total
    Kx = 33 - _int(RISK)
    ATR_Period = 15
    min_rates_D = GetStartBars(DSmoothMethod, DPeriod, DPhase) + 1
    min_rates_S = min_rates_D + GetStartBars(SSmoothMethod, SPeriod, SPhase)
    min_rates_total = MathMax(min_rates_S, ATR_Period) + 1
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, UpBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(UpBuffer1, True)
    SetIndexBuffer(1, DnBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(DnBuffer1, True)
    SetIndexBuffer(2, UpBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(UpBuffer2, True)
    SetIndexBuffer(3, DnBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(DnBuffer2, True)
    SetIndexBuffer(4, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_ARROW, 175)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(BuyBuffer, True)
    SetIndexBuffer(5, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(5, PLOT_ARROW, 175)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(SellBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'XRSXTrend_NRTR'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_oldtrend
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    trend = 0
    maxbar = 0
    ATR = Arr(0, 0.0)
    range_ = 0.0
    stop = 0.0
    dprice = 0.0
    absdprice = 0.0
    up_xrsx = 0.0
    dn_xrsx = 0.0
    xrsx = 0.0
    xxrsx = 0.0
    maxbar = rates_total - 2
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
        _s_OnCalculate_oldtrend = 0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        dprice = PriceSeries(IPC, bar, open, low, high, close) - PriceSeries(IPC, bar + 1, open, low, high, close)
        absdprice = MathAbs(dprice)
        up_xrsx = UPXRSX.XMASeries(maxbar, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, dprice, bar, True)
        dn_xrsx = DNXRSX.XMASeries(maxbar, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, absdprice, bar, True)
        if not dn_xrsx:
            xrsx = 1.0
        else:
            xrsx = _fdiv(up_xrsx, dn_xrsx)
            if xrsx > 1:
                xrsx = 1.0
            if xrsx < -1:
                xrsx = -1.0
        xrsx *= 100
        xxrsx = XSIGN.XMASeries(maxbar - min_rates_D, prev_calculated, rates_total, SSmoothMethod, SPhase, SPeriod, xrsx, bar, True)
        xxrsx += 100
        xxrsx = xxrsx / 2
        DnBuffer2[bar] = 0.0
        UpBuffer2[bar] = DnBuffer2[bar]
        DnBuffer1[bar] = UpBuffer2[bar]
        UpBuffer1[bar] = DnBuffer1[bar]
        SellBuffer[bar] = UpBuffer1[bar]
        BuyBuffer[bar] = SellBuffer[bar]
        trend = _s_OnCalculate_oldtrend
        if xxrsx < Kx:
            trend = -1
        if xxrsx > (100 - Kx):
            trend = 1
        range_ = AtrRatio * ATR[bar]
        if _s_OnCalculate_oldtrend < 0 and trend > 0:
            BuyBuffer[bar] = low[bar] - range_
        if _s_OnCalculate_oldtrend > 0 and trend < 0:
            SellBuffer[bar] = high[bar] + range_
        if trend > 0:
            if BuyBuffer[bar]:
                UpBuffer2[bar] = BuyBuffer[bar]
                UpBuffer1[bar] = UpBuffer2[bar]
                DnBuffer1[bar] = DnBuffer1[bar + 1]
            else:
                stop = low[bar] - range_
                if stop < UpBuffer1[bar + 1]:
                    stop = UpBuffer1[bar + 1]
                UpBuffer2[bar] = stop
                UpBuffer1[bar] = UpBuffer2[bar]
        if trend < 0:
            if SellBuffer[bar]:
                DnBuffer2[bar] = SellBuffer[bar]
                DnBuffer1[bar] = DnBuffer2[bar]
                UpBuffer1[bar] = UpBuffer1[bar + 1]
            else:
                stop = high[bar] + range_
                if stop > DnBuffer1[bar + 1]:
                    stop = DnBuffer1[bar + 1]
                DnBuffer2[bar] = stop
                DnBuffer1[bar] = DnBuffer2[bar]
        if bar:
            _s_OnCalculate_oldtrend = trend
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
UPXRSX = _alloc(CXMA)
UPXRSX.__init__()
DNXRSX = _alloc(CXMA)
DNXRSX.__init__()
XSIGN = _alloc(CXMA)
XSIGN.__init__()

# ---- static local variables
_s_OnCalculate_oldtrend = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XRSXTrendNRTR(_MQL5Indicator):
    name = 'XRSXTrend_NRTR'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RISK': 2,
        'DSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения цены
        'DPeriod': 12,  # период мувинга
        'DPhase': 100,  # параметр усреднения мувинга,
        'SSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения сигнальной линии
        'SPeriod': 7,  # период сигнальной линии
        'SPhase': 100,  # параметр сигнальной линии,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'AtrRatio': 0.375,
    }

