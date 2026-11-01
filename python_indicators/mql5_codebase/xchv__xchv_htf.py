"""XCHV — converted from MQL5: MQL5 Indicators/XCHV_HTF/XCHV.mq5

Chaikin Volatility
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [13458026]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'XCHV'}, 'levels': [], 'description': ['Chaikin Volatility'], 'name': 'XCHV', 'source': 'MQL5 Indicators/XCHV_HTF/XCHV.mq5', 'folder': 'XCHV_HTF', 'inputs': [{'mql': 'SmoothPeriod', 'py': 'SmoothPeriod', 'param': 'SmoothPeriod', 'type': 'int', 'default': 10, 'label': 'период усреднения', 'sinput': False}, {'mql': 'Phase_', 'py': 'Phase_', 'param': 'Phase_', 'type': 'int', 'default': 15, 'label': 'параметр усреднения,', 'sinput': False}, {'mql': 'CHVPeriod', 'py': 'CHVPeriod', 'param': 'CHVPeriod', 'type': 'int', 'default': 10, 'label': 'CHV период', 'sinput': False}, {'mql': 'SmoothMethod', 'py': 'SmoothMethod', 'param': 'SmoothMethod', 'type': 'int', 'default': 7, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
SmoothPeriod = _input('SmoothPeriod', 10)  # период усреднения
Phase_ = _input('Phase_', 15)  # параметр усреднения,
CHVPeriod = _input('CHVPeriod', 10)  # CHV период
SmoothMethod = _input('SmoothMethod', MODE_T3)  # метод усреднения
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
XCHV = Arr(0, 0.0)
StartBars = 0

def OnInit():
    global StartBars
    StartBars = CHVPeriod + XMA.GetStartBars(SmoothMethod, SmoothPeriod, Phase_)
    XMA.XMALengthCheck('SmoothPeriod', SmoothPeriod)
    XMA.XMALengthCheck('CHVPeriod', CHVPeriod)
    XMA.XMAPhaseCheck('Phase_', Phase_, SmoothMethod)
    SetIndexBuffer(0, XCHV, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(0, PLOT_LABEL, 'XCHV')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    Smooth = XMA.GetString_MA_Method(SmoothMethod)
    StringConcatenate(shortname, 'Chaikin Volatility(', _str(SmoothPeriod), ',', _str(CHVPeriod), ',', Smooth, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBars:
        return 0
    velue = 0.0
    xvelue = 0.0
    mom = 0.0
    dmom = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        velue = high[bar] - low[bar]
        xvelue = XMA.XMASeries(0, prev_calculated, rates_total, SmoothMethod, Phase_, SmoothPeriod, velue, bar, False)
        mom = MOM.MomentumSeries(SmoothPeriod, prev_calculated, rates_total, CHVPeriod, xvelue, bar, False)
        dmom = xvelue - mom
        if bar < StartBars:
            XCHV[bar] = EMPTY_VALUE
            continue
        elif dmom != 0.0:
            XCHV[bar] = _fdiv(100.0 * mom, dmom)
        else:
            XCHV[bar] = EMPTY_VALUE
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA = _alloc(CXMA)
XMA.__init__()
MOM = _alloc(CMomentum)
MOM.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XCHVIndicator(_MQL5Indicator):
    name = 'XCHV'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SmoothPeriod': 10,  # период усреднения
        'Phase_': 15,  # параметр усреднения,
        'CHVPeriod': 10,  # CHV период
        'SmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # метод усреднения
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

