"""tsi_macd — converted from MQL5: MQL5 Indicators/TSI_MACD_HTF/tsi_macd.mq5

TSI_MACD
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [13749760, 15631086]}, 'widths': {}, 'styles': {}, 'labels': {1: 'TSI_MACD'}, 'levels': [50.0, 0.0, -50.0], 'description': ['TSI_MACD'], 'name': 'tsi_macd', 'source': 'MQL5 Indicators/TSI_MACD_HTF/tsi_macd.mq5', 'folder': 'TSI_MACD_HTF', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 1, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XFast', 'py': 'XFast', 'param': 'XFast', 'type': 'uint', 'default': 8, 'label': 'Быстрое усреднение цены', 'sinput': False}, {'mql': 'XSlow', 'py': 'XSlow', 'param': 'XSlow', 'type': 'uint', 'default': 21, 'label': 'Медленное усреднение цены', 'sinput': False}, {'mql': 'MomPeriod', 'py': 'MomPeriod', 'param': 'MomPeriod', 'type': 'uint', 'default': 1, 'label': 'Период моментума', 'sinput': False}, {'mql': 'XLength1', 'py': 'XLength1', 'param': 'XLength1', 'type': 'uint', 'default': 5, 'label': 'Глубина первого усреднения', 'sinput': False}, {'mql': 'XLength2', 'py': 'XLength2', 'param': 'XLength2', 'type': 'uint', 'default': 8, 'label': 'Глубина второго усреднения', 'sinput': False}, {'mql': 'XLength3', 'py': 'XLength3', 'param': 'XLength3', 'type': 'uint', 'default': 5, 'label': 'Глубина усреднения сигнальной линии', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XMA_Method = _input('XMA_Method', MODE_EMA)  # Метод усреднения
XFast = _input('XFast', 8)  # Быстрое усреднение цены
XSlow = _input('XSlow', 21)  # Медленное усреднение цены
MomPeriod = _input('MomPeriod', 1)  # Период моментума
XLength1 = _input('XLength1', 5)  # Глубина первого усреднения
XLength2 = _input('XLength2', 8)  # Глубина второго усреднения
XLength3 = _input('XLength3', 5)  # Глубина усреднения сигнальной линии
XPhase = _input('XPhase', 15)  # Параметр сглаживания
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
min_rates_3 = 0
min_rates_4 = 0

def OnInit():
    global min_rates_1, min_rates_2, min_rates_3, min_rates_4, min_rates_total
    min_rates_1 = MathMax(XMA1.GetStartBars(XMA_Method, XFast, XPhase), XMA1.GetStartBars(XMA_Method, XSlow, XPhase))
    min_rates_2 = _int(MomPeriod)
    min_rates_3 = min_rates_2 + XMA1.GetStartBars(XMA_Method, XLength1, XPhase)
    min_rates_4 = min_rates_3 + XMA1.GetStartBars(XMA_Method, XLength2, XPhase)
    min_rates_total = min_rates_4 + XMA1.GetStartBars(XMA_Method, XLength3, XPhase)
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TSI_MACD')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    fast = 0.0
    slow = 0.0
    macd = 0.0
    mtm = 0.0
    xmtm = 0.0
    xxmtm = 0.0
    absmtm = 0.0
    xabsmtm = 0.0
    xxabsmtm = 0.0
    tsi = 0.0
    xtsi = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        fast = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XFast, price, bar, False)
        slow = XMA2.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XSlow, price, bar, False)
        macd = fast - slow
        mtm = Mom.MomentumSeries(min_rates_1, prev_calculated, rates_total, MomPeriod, macd, bar, False)
        absmtm = MathAbs(mtm)
        xmtm = XMA3.XMASeries(min_rates_2, prev_calculated, rates_total, XMA_Method, XPhase, XLength1, mtm, bar, False)
        xabsmtm = XMA4.XMASeries(min_rates_2, prev_calculated, rates_total, XMA_Method, XPhase, XLength1, absmtm, bar, False)
        xxmtm = XMA5.XMASeries(min_rates_3, prev_calculated, rates_total, XMA_Method, XPhase, XLength2, xmtm, bar, False)
        xxabsmtm = XMA6.XMASeries(min_rates_3, prev_calculated, rates_total, XMA_Method, XPhase, XLength2, xabsmtm, bar, False)
        if xxabsmtm:
            tsi = _fdiv(100 * xxmtm, xxabsmtm)
        else:
            tsi = 0.0
        if not tsi:
            tsi = 1e-09
        xtsi = XMA7.XMASeries(min_rates_4, prev_calculated, rates_total, XMA_Method, XPhase, XLength3, tsi, bar, False)
        if not xtsi:
            xtsi = 1e-09
        UpBuffer[bar] = tsi
        DnBuffer[bar] = xtsi
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
XMA7 = _alloc(CXMA)
XMA7.__init__()
Mom = _alloc(CMomentum)
Mom.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TsiMacd(_MQL5Indicator):
    name = 'tsi_macd'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Метод усреднения
        'XFast': 8,  # Быстрое усреднение цены
        'XSlow': 21,  # Медленное усреднение цены
        'MomPeriod': 1,  # Период моментума
        'XLength1': 5,  # Глубина первого усреднения
        'XLength2': 8,  # Глубина второго усреднения
        'XLength3': 5,  # Глубина усреднения сигнальной линии
        'XPhase': 15,  # Параметр сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
    }

