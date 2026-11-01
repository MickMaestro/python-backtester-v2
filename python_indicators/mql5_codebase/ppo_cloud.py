"""PPO_Cloud — converted from MQL5: MQL5 Indicators/BackgroundCandle_PPO_Cloud_HTF/PPO_Cloud.mq5

This is a momentum indicator.
Signal line is EMA of PPO.
Follows formula: PPO=(FastEMA-SlowEMA)/SlowEMA
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16748574, 8388736]}, 'widths': {}, 'styles': {}, 'labels': {1: 'PPO_Cloud'}, 'levels': [0.0], 'description': ['This is a momentum indicator.', 'Signal line is EMA of PPO.', 'Follows formula: PPO=(FastEMA-SlowEMA)/SlowEMA'], 'name': 'PPO_Cloud', 'source': 'MQL5 Indicators/BackgroundCandle_PPO_Cloud_HTF/PPO_Cloud.mq5', 'folder': 'BackgroundCandle_PPO_Cloud_HTF', 'inputs': [{'mql': 'FastMethod', 'py': 'FastMethod', 'param': 'FastMethod', 'type': 'int', 'default': 1, 'label': 'метод быстрого усреднения', 'sinput': False}, {'mql': 'FastLength', 'py': 'FastLength', 'param': 'FastLength', 'type': 'uint', 'default': 12, 'label': 'глубина быстрого усреднения', 'sinput': False}, {'mql': 'FastPhase', 'py': 'FastPhase', 'param': 'FastPhase', 'type': 'int', 'default': 15, 'label': 'параметр быстрого усреднения,', 'sinput': False}, {'mql': 'SlowMethod', 'py': 'SlowMethod', 'param': 'SlowMethod', 'type': 'int', 'default': 1, 'label': 'метод медленного усреднения', 'sinput': False}, {'mql': 'SlowLength', 'py': 'SlowLength', 'param': 'SlowLength', 'type': 'uint', 'default': 26, 'label': 'глубина медленного усреднения', 'sinput': False}, {'mql': 'SlowPhase', 'py': 'SlowPhase', 'param': 'SlowPhase', 'type': 'int', 'default': 15, 'label': 'параметр медленного усреднения,', 'sinput': False}, {'mql': 'SignMethod', 'py': 'SignMethod', 'param': 'SignMethod', 'type': 'int', 'default': 1, 'label': 'метод сглаживания', 'sinput': False}, {'mql': 'SignLength', 'py': 'SignLength', 'param': 'SignLength', 'type': 'uint', 'default': 9, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'SignPhase', 'py': 'SignPhase', 'param': 'SignPhase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
FastMethod = _input('FastMethod', MODE_EMA_)  # метод быстрого усреднения
FastLength = _input('FastLength', 12)  # глубина быстрого усреднения
FastPhase = _input('FastPhase', 15)  # параметр быстрого усреднения,
SlowMethod = _input('SlowMethod', MODE_EMA_)  # метод медленного усреднения
SlowLength = _input('SlowLength', 26)  # глубина медленного усреднения
SlowPhase = _input('SlowPhase', 15)  # параметр медленного усреднения,
SignMethod = _input('SignMethod', MODE_EMA_)  # метод сглаживания
SignLength = _input('SignLength', 9)  # глубина сглаживания
SignPhase = _input('SignPhase', 15)  # параметр сглаживания,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
PPOBuffer = Arr(0, 0.0)
SignBuffer = Arr(0, 0.0)
min_rates_ = 0
min_rates_total = 0

def OnInit():
    global min_rates_, min_rates_total
    min_rates_ = MathMax(XMA1.GetStartBars(FastMethod, FastLength, FastPhase), XMA1.GetStartBars(SlowMethod, SlowLength, SlowPhase))
    min_rates_total = min_rates_ + XMA1.GetStartBars(SignMethod, SignLength, SignPhase)
    SetIndexBuffer(0, PPOBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SignBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'PPO_Cloud')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    for bar in range(first, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        fast = XMA1.XMASeries(0, prev_calculated, rates_total, FastMethod, FastPhase, FastLength, price, bar, False)
        slow = XMA2.XMASeries(0, prev_calculated, rates_total, SlowMethod, SlowPhase, SlowLength, price, bar, False)
        if not slow:
            slow = 1.0
        ppo = _fdiv(fast - slow, slow)
        PPOBuffer[bar] = ppo
        SignBuffer[bar] = XMA3.XMASeries(min_rates_, prev_calculated, rates_total, SignMethod, SignPhase, SignLength, ppo, bar, False)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()
XMA3 = _alloc(CXMA)
XMA3.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PPOCloud(_MQL5Indicator):
    name = 'PPO_Cloud'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # метод быстрого усреднения
        'FastLength': 12,  # глубина быстрого усреднения
        'FastPhase': 15,  # параметр быстрого усреднения,
        'SlowMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # метод медленного усреднения
        'SlowLength': 26,  # глубина медленного усреднения
        'SlowPhase': 15,  # параметр медленного усреднения,
        'SignMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # метод сглаживания
        'SignLength': 9,  # глубина сглаживания
        'SignPhase': 15,  # параметр сглаживания,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

