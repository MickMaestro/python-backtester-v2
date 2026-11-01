"""Heiken_Ashi_Smoothed_Volatility_Volume — converted from MQL5: MQL5 Indicators/Heiken_Ashi_Smoothed_Volatility_Volume_HTF/Heiken_Ashi_Smoothed_Volatility_Volume.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 3}, 'colors': {1: [13458026]}, 'widths': {1: 4}, 'styles': {1: 0}, 'labels': {1: 'Heiken_Ashi_Smoothed_VolatilityStep'}, 'levels': [], 'description': [], 'name': 'Heiken_Ashi_Smoothed_Volatility_Volume', 'source': 'MQL5 Indicators/Heiken_Ashi_Smoothed_Volatility_Volume_HTF/Heiken_Ashi_Smoothed_Volatility_Volume.mq5', 'folder': 'Heiken_Ashi_Smoothed_Volatility_Volume_HTF', 'inputs': [{'mql': 'HMA_Method', 'py': 'HMA_Method', 'param': 'HMA_Method', 'type': 'int', 'default': 7, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'HLength', 'py': 'HLength', 'param': 'HLength', 'type': 'uint', 'default': 12, 'label': 'Глубина  усреднения', 'sinput': False}, {'mql': 'HPhase', 'py': 'HPhase', 'param': 'HPhase', 'type': 'int', 'default': 100, 'label': 'Параметр усреднения,', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'объём', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
HMA_Method = _input('HMA_Method', MODE_T3)  # Метод усреднения
HLength = _input('HLength', 12)  # Глубина  усреднения
HPhase = _input('HPhase', 100)  # Параметр усреднения,
VolumeType = _input('VolumeType', VOLUME_TICK)  # объём
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = GetStartBars(HMA_Method, HLength, HPhase) + 1
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = 'Heiken_Ashi_Smoothed_Volatility_Volume(' + _str(HLength) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_HAC_prev, _s_OnCalculate_HAO_prev
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    XmaOpen = 0.0
    XmaHigh = 0.0
    XmaLow = 0.0
    XmaClose = 0.0
    XVolume = 0.0
    Volatility = 0.0
    O = 0.0
    H = 0.0
    L = 0.0
    C = 0.0
    V = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        _s_OnCalculate_HAO_prev = (open[first] + close[first]) / 2
        _s_OnCalculate_HAC_prev = (open[first] + high[first] + low[first] + close[first]) / 4
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        IndBuffer[bar] = 0.0
        XmaOpen = XMAO.XMASeries(0, prev_calculated, rates_total, HMA_Method, HPhase, HLength, open[bar], bar, False)
        XmaClose = XMAC.XMASeries(0, prev_calculated, rates_total, HMA_Method, HPhase, HLength, close[bar], bar, False)
        XmaHigh = XMAH.XMASeries(0, prev_calculated, rates_total, HMA_Method, HPhase, HLength, high[bar], bar, False)
        XmaLow = XMAL.XMASeries(0, prev_calculated, rates_total, HMA_Method, HPhase, HLength, low[bar], bar, False)
        if VolumeType == VOLUME_TICK:
            V = float(tick_volume[bar])
        else:
            V = float(volume[bar])
        XVolume = XMAV.XMASeries(0, prev_calculated, rates_total, HMA_Method, HPhase, HLength, V, bar, False)
        if bar < min_rates_total:
            continue
        O = (_s_OnCalculate_HAO_prev + _s_OnCalculate_HAC_prev) / 2
        C = (XmaOpen + XmaHigh + XmaLow + XmaClose) / 4
        H = MathMax(XmaHigh, MathMax(O, C))
        L = MathMin(XmaLow, MathMin(O, C))
        Volatility = _fdiv(H - L, Point())
        IndBuffer[bar] = Volatility * XVolume
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMAO = _alloc(CXMA)
XMAO.__init__()
XMAL = _alloc(CXMA)
XMAL.__init__()
XMAH = _alloc(CXMA)
XMAH.__init__()
XMAC = _alloc(CXMA)
XMAC.__init__()
XMAV = _alloc(CXMA)
XMAV.__init__()

# ---- static local variables
_s_OnCalculate_HAO_prev = 0.0
_s_OnCalculate_HAC_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HeikenAshiSmoothedVolatilityVolume(_MQL5Indicator):
    name = 'Heiken_Ashi_Smoothed_Volatility_Volume'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'HMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # Метод усреднения
        'HLength': 12,  # Глубина  усреднения
        'HPhase': 100,  # Параметр усреднения,
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

