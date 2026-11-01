"""Fractal_Levels — converted from MQL5: MQL5 Indicators/Fractal_Levels/Fractal_Levels.mq5

Copyright: Copyright © 2008, lotos4u; Link: lotos4u@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, lotos4u', 'link': 'lotos4u@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [16748574], 2: [14053594], 3: [65280], 4: [255]}, 'widths': {1: 2, 2: 2, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Фрактальное сопротивление', 2: 'Фрактальная поддержка', 3: 'Фрактал ВЕРХ', 4: 'Фрактал ВНИЗ'}, 'levels': [], 'description': [], 'name': 'Fractal_Levels', 'source': 'MQL5 Indicators/Fractal_Levels/Fractal_Levels.mq5', 'folder': 'Fractal_Levels', 'inputs': [{'mql': 'LeftBars', 'py': 'LeftBars', 'param': 'LeftBars', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'RightBars', 'py': 'RightBars', 'param': 'RightBars', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
LeftBars = _input('LeftBars', 3)
RightBars = _input('RightBars', 3)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
LineUp = Arr(0, 0.0)
LineDown = Arr(0, 0.0)
SignUp = Arr(0, 0.0)
SignDown = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(LeftBars + RightBars)
    shortname = Box("")
    StringConcatenate(shortname, 'Fractal_Levels(', _str(LeftBars), ', ', _str(RightBars), ', ', _str(Shift), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, LineUp, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(LineUp, True)
    SetIndexBuffer(1, LineDown, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(LineDown, True)
    SetIndexBuffer(2, SignUp, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SignUp, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(2, PLOT_ARROW, 167)
    SetIndexBuffer(3, SignDown, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SignDown, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(3, PLOT_ARROW, 167)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        SignUp[bar] = isFractalUp(bar, LeftBars, RightBars, rates_total, high)
        SignDown[bar] = isFractalDown(bar, LeftBars, RightBars, rates_total, low)
        if SignUp[bar]:
            LineUp[bar] = SignUp[bar]
        else:
            LineUp[bar] = LineUp[bar + 1]
        if SignDown[bar]:
            LineDown[bar] = SignDown[bar]
        else:
            LineDown[bar] = LineDown[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def isFractalUp(index, lBars, rBars, Rates_Total, High):
    left = MathMin(Rates_Total - 1, index + lBars)
    right = MathMax(0, index - rBars)
    max_ = High[index]
    for iii in range(right, left + 1):
        if max_ <= High[iii] and iii != index:
            if max_ < High[iii]:
                return 0.0
            if MathAbs(iii - index) > 1:
                return 0.0
    return max_

def isFractalDown(index, lBars, rBars, Rates_Total, Low):
    left = MathMin(Rates_Total - 1, index + lBars)
    right = MathMax(0, index - rBars)
    min_ = Low[index]
    for iii in range(right, left + 1):
        if min_ >= Low[iii] and iii != index:
            if min_ > Low[iii]:
                return 0.0
            if MathAbs(iii - index) > 1:
                return 0.0
    return min_


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FractalLevels(_MQL5Indicator):
    name = 'Fractal_Levels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'LeftBars': 3,
        'RightBars': 3,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

