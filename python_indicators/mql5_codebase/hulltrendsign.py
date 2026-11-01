"""hulltrendsign — converted from MQL5: MQL5 Indicators/HullTrendSign/hulltrendsign.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [3329330]}, 'widths': {1: 2, 2: 2}, 'styles': {}, 'labels': {1: 'HullTrendSign Sell', 2: 'HullTrendSign Buy'}, 'levels': [], 'description': [], 'name': 'hulltrendsign', 'source': 'MQL5 Indicators/HullTrendSign/hulltrendsign.mq5', 'folder': 'HullTrendSign', 'inputs': [{'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 20, 'label': 'период индикатора', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'цена индикатора', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 3, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр усреднения,', 'sinput': False}, {'mql': 'XLength1', 'py': 'XLength1', 'param': 'XLength1', 'type': 'uint', 'default': 5, 'label': 'период сглаживания индикатора', 'sinput': False}, {'mql': 'XMA_Method1', 'py': 'XMA_Method1', 'param': 'XMA_Method1', 'type': 'int', 'default': 4, 'label': 'метод сглаживания', 'sinput': False}, {'mql': 'XPhase1', 'py': 'XPhase1', 'param': 'XPhase1', 'type': 'int', 'default': 100, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
XLength = _input('XLength', 20)  # период индикатора
IPC = _input('IPC', PRICE_CLOSE)  # цена индикатора
XMA_Method = _input('XMA_Method', MODE_LWMA)  # метод усреднения
XPhase = _input('XPhase', 15)  # параметр усреднения,
XLength1 = _input('XLength1', 5)  # период сглаживания индикатора
XMA_Method1 = _input('XMA_Method1', MODE_JJMA)  # метод сглаживания
XPhase1 = _input('XPhase1', 100)  # параметр сглаживания,
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_1 = 0
min_rates_2 = 0
min_rates_total = 0
ATR_Handle = 0
XLength2 = 0
SqrXLength = 0

def OnInit():
    global ATR_Handle, SqrXLength, XLength2, min_rates_1, min_rates_2, min_rates_total
    XLength2 = _int(_idiv(XLength, 2))
    SqrXLength = _int(MathFloor(MathSqrt(XLength)))
    min_rates_1 = XMA1.GetStartBars(XMA_Method, XLength, XPhase)
    min_rates_2 = min_rates_1 + XMA1.GetStartBars(XMA_Method, SqrXLength, XPhase)
    min_rates_total = min_rates_2 + XMA1.GetStartBars(XMA_Method1, XLength1, XPhase1) + 1
    ATR_Period = 10
    min_rates_total = MathMax(min_rates_total, ATR_Period)
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 84)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 84)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    IndicatorSetString(INDICATOR_SHORTNAME, 'HullTrendSign')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_trend1, _s_OnCalculate_xosma1
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    price = 0.0
    xma = 0.0
    xma2 = 0.0
    hma = 0.0
    xhma = 0.0
    osma = 0.0
    xosma = 0.0
    trend = 0.0
    ATR = Arr(1, 0.0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        _s_OnCalculate_trend1 = 0.0
        _s_OnCalculate_xosma1 = 0.0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        xma2 = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength2, price, bar, False)
        xma = XMA2.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, price, bar, False)
        hma = (2 * xma2) - xma
        xhma = XMA3.XMASeries(min_rates_1, prev_calculated, rates_total, XMA_Method, XPhase, SqrXLength, hma, bar, False)
        osma = hma - xhma
        xosma = XMA4.XMASeries(min_rates_2, prev_calculated, rates_total, XMA_Method1, XPhase1, XLength1, osma, bar, False)
        trend = xosma - _s_OnCalculate_xosma1
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if _s_OnCalculate_trend1 <= 0 and trend > 0:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            BuyBuffer[bar] = low[bar] - ((ATR[0] * 3) / 8)
        if _s_OnCalculate_trend1 >= 0 and trend < 0:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            SellBuffer[bar] = high[bar] + ((ATR[0] * 3) / 8)
        if bar < (rates_total - 1):
            _s_OnCalculate_trend1 = trend
            _s_OnCalculate_xosma1 = xosma
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

# ---- static local variables
_s_OnCalculate_xosma1 = 0.0
_s_OnCalculate_trend1 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Hulltrendsign(_MQL5Indicator):
    name = 'hulltrendsign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XLength': 20,  # период индикатора
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # цена индикатора
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # метод усреднения
        'XPhase': 15,  # параметр усреднения,
        'XLength1': 5,  # период сглаживания индикатора
        'XMA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод сглаживания
        'XPhase1': 100,  # параметр сглаживания,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

