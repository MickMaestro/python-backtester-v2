"""MaChannel — converted from MQL5: MQL5 Indicators/MaChannel/MaChannel.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [16711680], 2: [255], 3: [16748574], 4: [16711935]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'MaChannel Up', 2: 'MaChannel Down', 3: 'Buy MaChannel signal', 4: 'Sell MaChannel signal'}, 'levels': [], 'description': [], 'name': 'MaChannel', 'source': 'MQL5 Indicators/MaChannel/MaChannel.mq5', 'folder': 'MaChannel', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'uint', 'default': 12, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'Renge', 'py': 'Renge', 'param': 'Renge', 'type': 'uint', 'default': 600, 'label': 'Ценовой размах мувинга в пунктах', 'sinput': False}, {'mql': 'oneWay', 'py': 'oneWay', 'param': 'oneWay', 'type': 'bool', 'default': True, 'label': 'одностороннее движение индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_SMA_)  # метод усреднения
XLength = _input('XLength', 12)  # глубина сглаживания
XPhase = _input('XPhase', 15)  # параметр сглаживания,
Renge = _input('Renge', 600)  # Ценовой размах мувинга в пунктах
oneWay = _input('oneWay', True)  # одностороннее движение индикатора
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали
TrendUp = Arr(0, 0.0)
TrendDown = Arr(0, 0.0)
SignUp = Arr(0, 0.0)
SignDown = Arr(0, 0.0)
dRenge = 0.0
min_rates_total = 0

def OnInit():
    global dRenge, min_rates_total
    min_rates_total = GetStartBars(XMA_Method, XLength, XPhase) + 2
    XMA1.XMALengthCheck('XLength', XLength)
    XMA1.XMAPhaseCheck('XPhase', XPhase, XMA_Method)
    dRenge = Point() * Renge
    SetIndexBuffer(0, TrendUp, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_ARROW, 119)
    SetIndexBuffer(1, TrendDown, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_ARROW, 119)
    SetIndexBuffer(2, SignUp, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(2, PLOT_ARROW, 117)
    SetIndexBuffer(3, SignDown, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(3, PLOT_ARROW, 117)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MaChannel')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_down_prev, _s_OnCalculate_trend_prev, _s_OnCalculate_up_prev
    if rates_total < min_rates_total:
        return 0
    up = 0.0
    down = 0.0
    first = 0
    bar = 0
    trend = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        _s_OnCalculate_trend_prev = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        TrendUp[bar] = 0.0
        TrendDown[bar] = 0.0
        SignUp[bar] = 0.0
        SignDown[bar] = 0.0
        trend = _s_OnCalculate_trend_prev
        up = XMA1.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, high[bar], bar, False) + dRenge
        down = XMA2.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, low[bar], bar, False) + dRenge
        if oneWay:
            if _s_OnCalculate_trend_prev == 1:
                if down < _s_OnCalculate_down_prev and _s_OnCalculate_down_prev:
                    down = _s_OnCalculate_down_prev
            elif _s_OnCalculate_trend_prev == -1:
                if up > _s_OnCalculate_up_prev and _s_OnCalculate_up_prev:
                    up = _s_OnCalculate_up_prev
        if high[bar] > up:
            trend = 1
        elif low[bar] < down:
            trend = -1
        if trend == -1.0:
            TrendDown[bar] = up
        elif trend == 1.0:
            TrendUp[bar] = down
        if _s_OnCalculate_trend_prev <= 0 and trend > 0:
            SignUp[bar] = TrendUp[bar]
        if _s_OnCalculate_trend_prev >= 0 and trend < 0:
            SignDown[bar] = TrendDown[bar]
        if bar < (rates_total - 1):
            _s_OnCalculate_up_prev = up
            _s_OnCalculate_down_prev = down
            _s_OnCalculate_trend_prev = trend
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()

# ---- static local variables
_s_OnCalculate_up_prev = 0.0
_s_OnCalculate_down_prev = 0.0
_s_OnCalculate_trend_prev = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MaChannel(_MQL5Indicator):
    name = 'MaChannel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения
        'XLength': 12,  # глубина сглаживания
        'XPhase': 15,  # параметр сглаживания,
        'Renge': 600,  # Ценовой размах мувинга в пунктах
        'oneWay': True,  # одностороннее движение индикатора
        'Shift': 0,  # сдвиг индикатора по горизонтали
    }

