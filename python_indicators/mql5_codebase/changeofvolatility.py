"""changeofvolatility — converted from MQL5: MQL5 Indicators/Change Of Volatility/changeofvolatility.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 8388736, 255, 55295]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Change of Volatility'}, 'levels': [], 'description': [], 'name': 'changeofvolatility', 'source': 'MQL5 Indicators/Change Of Volatility/changeofvolatility.mq5', 'folder': 'Change Of Volatility', 'inputs': [{'mql': 'MPeriod', 'py': 'MPeriod', 'param': 'MPeriod', 'type': 'uint', 'default': 1, 'label': 'Momentum period', 'sinput': False}, {'mql': 'Short', 'py': 'Short', 'param': 'Short', 'type': 'uint', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'Long', 'py': 'Long', 'param': 'Long', 'type': 'uint', 'default': 100, 'label': '', 'sinput': False}, {'mql': 'MaxTrendLevel', 'py': 'MaxTrendLevel', 'param': 'MaxTrendLevel', 'type': 'uint', 'default': 80, 'label': 'Maximum trend level', 'sinput': False}, {'mql': 'MiddLeTrendLevel', 'py': 'MiddLeTrendLevel', 'param': 'MiddLeTrendLevel', 'type': 'uint', 'default': 50, 'label': 'Middle trend level', 'sinput': False}, {'mql': 'FlatLevel', 'py': 'FlatLevel', 'param': 'FlatLevel', 'type': 'uint', 'default': 30, 'label': 'Flat level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

Blue = 0xFF0000  # MQL4 colour name
Gray = 0x808080  # MQL4 colour name
Magenta = 0xFF00FF  # MQL4 colour name

# ---- inputs and global variables
MPeriod = _input('MPeriod', 1)  # Momentum period
Short = _input('Short', 6)
Long = _input('Long', 100)
MaxTrendLevel = _input('MaxTrendLevel', 80)  # Maximum trend level
MiddLeTrendLevel = _input('MiddLeTrendLevel', 50)  # Middle trend level
FlatLevel = _input('FlatLevel', 30)  # Flat level
StdDevBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(MPeriod + MathMax(Short, Long))
    SetIndexBuffer(0, StdDevBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = Box("")
    StringConcatenate(shortname, 'Change of Volatility( ', MPeriod, ', ', Short, ', ', Long, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, MaxTrendLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, MiddLeTrendLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, FlatLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, Magenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, Blue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, Gray)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    stdl = 0.0
    stds = 0.0
    smal = 0.0
    smas = 0.0
    momentum = 0.0
    if prev_calculated == 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        momentum = _s_OnCalculate_Mom.MomentumSeries(0, prev_calculated, rates_total, MPeriod, close[bar], bar, False)
        momentum = _fdiv(momentum, Point())
        smal = _s_OnCalculate_SMAL.SMASeries(MPeriod, prev_calculated, rates_total, Long, momentum, bar, False)
        stdl = _s_OnCalculate_STDL.StdDevSeries(MPeriod, prev_calculated, rates_total, Long, 2.0, momentum, smal, bar, False)
        smas = _s_OnCalculate_SMAS.SMASeries(MPeriod, prev_calculated, rates_total, Short, momentum, bar, False)
        stds = _s_OnCalculate_STDS.StdDevSeries(MPeriod, prev_calculated, rates_total, Short, 2.0, momentum, smas, bar, False)
        if stdl:
            StdDevBuffer[bar] = _fdiv(100 * stds, stdl)
        else:
            StdDevBuffer[bar] = 0.0
        ColorBuffer[bar] = 0.0
        if StdDevBuffer[bar] > MaxTrendLevel:
            ColorBuffer[bar] = 3.0
        elif StdDevBuffer[bar] > MiddLeTrendLevel:
            ColorBuffer[bar] = 2.0
        elif StdDevBuffer[bar] > FlatLevel:
            ColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_Mom = CMomentum()
_s_OnCalculate_STDL = CStdDeviation()
_s_OnCalculate_STDS = CStdDeviation()
_s_OnCalculate_SMAL = CMoving_Average()
_s_OnCalculate_SMAS = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Changeofvolatility(_MQL5Indicator):
    name = 'changeofvolatility'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MPeriod': 1,  # Momentum period
        'Short': 6,
        'Long': 100,
        'MaxTrendLevel': 80,  # Maximum trend level
        'MiddLeTrendLevel': 50,  # Middle trend level
        'FlatLevel': 30,  # Flat level
    }

