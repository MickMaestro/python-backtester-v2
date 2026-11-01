"""ForexLineSign — converted from MQL5: MQL5 Indicators/ForexLineSign/ForexLineSign.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [9639167], 2: [3329330]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'NRatioSign Sell', 2: 'NRatioSign Buy'}, 'levels': [], 'description': [], 'name': 'ForexLineSign', 'source': 'MQL5 Indicators/ForexLineSign/ForexLineSign.mq5', 'folder': 'ForexLineSign', 'inputs': [{'mql': 'MA_Method11', 'py': 'MA_Method11', 'param': 'MA_Method11', 'type': 'int', 'default': 3, 'label': 'Метод усреднения первого сглаживания мувинга 1', 'sinput': False}, {'mql': 'Length11', 'py': 'Length11', 'param': 'Length11', 'type': 'int', 'default': 5, 'label': 'Глубина  первого сглаживания  мувинга 1', 'sinput': False}, {'mql': 'Phase11', 'py': 'Phase11', 'param': 'Phase11', 'type': 'int', 'default': 15, 'label': 'Параметр первого сглаживания,', 'sinput': False}, {'mql': 'MA_Method12', 'py': 'MA_Method12', 'param': 'MA_Method12', 'type': 'int', 'default': 3, 'label': 'Метод усреднения второго сглаживания', 'sinput': False}, {'mql': 'Length12', 'py': 'Length12', 'param': 'Length12', 'type': 'int', 'default': 10, 'label': 'Глубина  второго сглаживания  мувинга 1', 'sinput': False}, {'mql': 'Phase12', 'py': 'Phase12', 'param': 'Phase12', 'type': 'int', 'default': 15, 'label': 'Параметр второго сглаживания  мувинга 1,', 'sinput': False}, {'mql': 'IPC1', 'py': 'IPC1', 'param': 'IPC1', 'type': 'int', 'default': 1, 'label': 'Ценовая константа мувинга 1', 'sinput': False}, {'mql': 'MA_Method21', 'py': 'MA_Method21', 'param': 'MA_Method21', 'type': 'int', 'default': 3, 'label': 'Метод усреднения первого сглаживания мувинга 2', 'sinput': False}, {'mql': 'Length21', 'py': 'Length21', 'param': 'Length21', 'type': 'int', 'default': 20, 'label': 'Глубина  первого сглаживания мувинга 2', 'sinput': False}, {'mql': 'Phase21', 'py': 'Phase21', 'param': 'Phase21', 'type': 'int', 'default': 15, 'label': 'Параметр первого сглаживания мувинга 2,', 'sinput': False}, {'mql': 'MA_Method22', 'py': 'MA_Method22', 'param': 'MA_Method22', 'type': 'int', 'default': 3, 'label': 'Метод усреднения второго сглаживания мувинга 2', 'sinput': False}, {'mql': 'Length22', 'py': 'Length22', 'param': 'Length22', 'type': 'int', 'default': 20, 'label': 'Глубина  второго сглаживания мувинга 2', 'sinput': False}, {'mql': 'Phase22', 'py': 'Phase22', 'param': 'Phase22', 'type': 'int', 'default': 15, 'label': 'Параметр второго сглаживания,', 'sinput': False}, {'mql': 'IPC2', 'py': 'IPC2', 'param': 'IPC2', 'type': 'int', 'default': 1, 'label': 'Ценовая константа мувинга 2', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
MA_Method11 = _input('MA_Method11', MODE_LWMA)  # Метод усреднения первого сглаживания мувинга 1
Length11 = _input('Length11', 5)  # Глубина  первого сглаживания  мувинга 1
Phase11 = _input('Phase11', 15)  # Параметр первого сглаживания,
MA_Method12 = _input('MA_Method12', MODE_LWMA)  # Метод усреднения второго сглаживания
Length12 = _input('Length12', 10)  # Глубина  второго сглаживания  мувинга 1
Phase12 = _input('Phase12', 15)  # Параметр второго сглаживания  мувинга 1,
IPC1 = _input('IPC1', PRICE_CLOSE)  # Ценовая константа мувинга 1
MA_Method21 = _input('MA_Method21', MODE_LWMA)  # Метод усреднения первого сглаживания мувинга 2
Length21 = _input('Length21', 20)  # Глубина  первого сглаживания мувинга 2
Phase21 = _input('Phase21', 15)  # Параметр первого сглаживания мувинга 2,
MA_Method22 = _input('MA_Method22', MODE_LWMA)  # Метод усреднения второго сглаживания мувинга 2
Length22 = _input('Length22', 20)  # Глубина  второго сглаживания мувинга 2
Phase22 = _input('Phase22', 15)  # Параметр второго сглаживания,
IPC2 = _input('IPC2', PRICE_CLOSE)  # Ценовая константа мувинга 2
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
dF = 0.0
ATR_Handle = 0
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0

def OnInit():
    global ATR_Handle, min_rates_1, min_rates_2, min_rates_total
    min_rates_1 = GetStartBars(MA_Method11, Length11, Phase11)
    min_rates_2 = GetStartBars(MA_Method21, Length21, Phase21)
    min_rates_12 = GetStartBars(MA_Method12, Length12, Phase12)
    min_rates_22 = GetStartBars(MA_Method22, Length22, Phase22)
    min_rates_total = MathMax(min_rates_1 + min_rates_12, min_rates_2 + min_rates_22)
    ATR_Period = 10
    min_rates_total = MathMax(min_rates_total, ATR_Period)
    XMA1.XMALengthCheck('Length11', Length11)
    XMA2.XMALengthCheck('Length12', Length12)
    XMA3.XMALengthCheck('Length21', Length21)
    XMA4.XMALengthCheck('Length22', Length22)
    XMA1.XMAPhaseCheck('Phase11', Phase11, MA_Method11)
    XMA2.XMAPhaseCheck('Phase12', Phase12, MA_Method12)
    XMA3.XMAPhaseCheck('Phase21', Phase21, MA_Method21)
    XMA4.XMAPhaseCheck('Phase22', Phase22, MA_Method22)
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 175)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 175)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    shortname = Box("")
    StringConcatenate(shortname, 'ForexLineSign(', Length11, ', ', Length12, ', ', Length21, ', ', Length21, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_trend
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    price = 0.0
    x1xma = 0.0
    x2xma = 0.0
    x3xma = 0.0
    x4xma = 0.0
    trend = 0.0
    ATR = Arr(1, 0.0, dyn=False)
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        _s_OnCalculate_prev_trend = 0.0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC1, bar, open, low, high, close)
        x1xma = XMA1.XMASeries(0, prev_calculated, rates_total, MA_Method11, Phase11, Length11, price, bar, False)
        x2xma = XMA2.XMASeries(min_rates_1, prev_calculated, rates_total, MA_Method12, Phase12, Length12, x1xma, bar, False)
        price = PriceSeries(IPC2, bar, open, low, high, close)
        x3xma = XMA3.XMASeries(0, prev_calculated, rates_total, MA_Method21, Phase21, Length21, price, bar, False)
        x4xma = XMA4.XMASeries(min_rates_2, prev_calculated, rates_total, MA_Method22, Phase22, Length22, x3xma, bar, False)
        trend = x2xma - x4xma
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if _s_OnCalculate_prev_trend < 0 and trend > 0.0:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            BuyBuffer[bar] = low[bar] - ((ATR[0] * 3) / 8)
        if _s_OnCalculate_prev_trend > 0 and trend < 0.0:
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            SellBuffer[bar] = high[bar] + ((ATR[0] * 3) / 8)
        if bar < (rates_total - 1) and trend:
            _s_OnCalculate_prev_trend = trend
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
_s_OnCalculate_prev_trend = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ForexLineSign(_MQL5Indicator):
    name = 'ForexLineSign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method11': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # Метод усреднения первого сглаживания мувинга 1
        'Length11': 5,  # Глубина  первого сглаживания  мувинга 1
        'Phase11': 15,  # Параметр первого сглаживания,
        'MA_Method12': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # Метод усреднения второго сглаживания
        'Length12': 10,  # Глубина  второго сглаживания  мувинга 1
        'Phase12': 15,  # Параметр второго сглаживания  мувинга 1,
        'IPC1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа мувинга 1
        'MA_Method21': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # Метод усреднения первого сглаживания мувинга 2
        'Length21': 20,  # Глубина  первого сглаживания мувинга 2
        'Phase21': 15,  # Параметр первого сглаживания мувинга 2,
        'MA_Method22': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # Метод усреднения второго сглаживания мувинга 2
        'Length22': 20,  # Глубина  второго сглаживания мувинга 2
        'Phase22': 15,  # Параметр второго сглаживания,
        'IPC2': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа мувинга 2
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
    }

