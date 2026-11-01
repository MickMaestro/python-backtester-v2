"""MinMax SR — converted from MQL5: MQL5 Indicators/Minimum _ maximum support resistance zones/MinMax SR.mq5

Copyright: © mladen, 2020; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2020', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'MinMax SR', 'source': 'MQL5 Indicators/Minimum _ maximum support resistance zones/MinMax SR.mq5', 'folder': 'Minimum _ maximum support resistance zones', 'inputs': [{'mql': 'inpStartFrom', 'py': 'inpStartFrom', 'param': 'inpStartFrom', 'type': 'int', 'default': 10, 'label': 'Start from', 'sinput': False}, {'mql': 'inpStep', 'py': 'inpStep', 'param': 'inpStep', 'type': 'int', 'default': 5, 'label': 'Step size', 'sinput': False}, {'mql': 'inpLineStyle', 'py': 'inpLineStyle', 'param': 'inpLineStyle', 'type': 'int', 'default': 2, 'label': 'Lines style', 'sinput': False}, {'mql': 'inpStartColor', 'py': 'inpStartColor', 'param': None, 'type': 'color', 'default': 32768, 'label': 'Start color', 'sinput': False}, {'mql': 'inpEndColor', 'py': 'inpEndColor', 'param': None, 'type': 'color', 'default': 9639167, 'label': 'End color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpStartFrom = _input('inpStartFrom', 10)  # Start from
inpStep = _input('inpStep', 5)  # Step size
inpLineStyle = _input('inpLineStyle', STYLE_DOT)  # Lines style
inpStartColor = _input('inpStartColor', clrGreen)  # Start color
inpEndColor = _input('inpEndColor', clrDeepPink)  # End color

class sSimpleBuffer(MqlObject):
    _q_fields = ('buffer', 'period')
    def __init__(self, *args):
        self.buffer = Arr(0, 0.0)
        self.period = 0

class sWorkStruct(MqlObject):
    _q_fields = ('min', 'max')
    def __init__(self, *args):
        self.min = Arr(10, 0.0, dyn=False)
        self.max = Arr(10, 0.0, dyn=False)

def OnInit():
    _startFrom = (inpStartFrom if (inpStartFrom > 0) else 1)
    _stepSize = (inpStep if (inpStep > 0) else 1)
    for i in range(0, 10):
        SetIndexBuffer(i, buffers[i].buffer, INDICATOR_DATA)
        PlotIndexSetInteger(i, PLOT_DRAW_TYPE, DRAW_LINE)
        PlotIndexSetInteger(i, PLOT_LINE_STYLE, (inpLineStyle if (i < (10 - 1)) else STYLE_SOLID))
        PlotIndexSetInteger(i, PLOT_LINE_COLOR, gradientColor(i, 10 + 1, inpStartColor, inpEndColor))
        buffers[i].period = _startFrom + (i * _stepSize)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_m_workSize
    limit = prev_calculated - 1
    if limit < 0:
        limit = 0
    if _s_OnCalculate_m_workSize < rates_total:
        _s_OnCalculate_m_workSize = ArrayResize(_s_OnCalculate_m_work, rates_total + 500, 2000)
    for i in range(limit, rates_total):
        for k in range(0, 10):
            _period = buffers[k].period
            _start = i - _period
            if _start < 0:
                _start = 0
                _period = i + 1
            _s_OnCalculate_m_work[i].min[k] = close[ArrayMinimum(close, _start, _period)]
            _s_OnCalculate_m_work[i].max[k] = close[ArrayMaximum(close, _start, _period)]
            buffers[k].buffer[i] = (_s_OnCalculate_m_work[i].max[k] + _s_OnCalculate_m_work[i].min[k]) / 2.0
    return rates_total

def getColor(stepNo, totalSteps, from_, to):
    stes = float(totalSteps) - 1.0
    step = _fdiv(from_ - to, stes)
    return _uint(round(from_ - (step * stepNo)))

def gradientColor(step, totalSteps, from_, to):
    newBlue = getColor(step, totalSteps, (from_ & 0XFF0000) >> 16, (to & 0XFF0000) >> 16) << 16
    newGreen = getColor(step, totalSteps, (from_ & 0X00FF00) >> 8, (to & 0X00FF00) >> 8) << 8
    newRed = getColor(step, totalSteps, from_ & 0X0000FF, to & 0X0000FF)
    return newBlue + newGreen + newRed

# ---- global variables initialised from expressions
buffers = Arr(10, 0, dyn=False, factory=sSimpleBuffer)

# ---- static local variables
_s_OnCalculate_m_work = Arr(0, 0, factory=sWorkStruct)
_s_OnCalculate_m_workSize = -1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MinMaxSR(_MQL5Indicator):
    name = 'MinMax SR'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpStartFrom': 10,  # Start from
        'inpStep': 5,  # Step size
        'inpLineStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),  # Lines style
    }

