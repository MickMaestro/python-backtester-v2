"""Smoother rainbow — converted from MQL5: MQL5 Indicators/Smoother rainbow/Smoother rainbow.mq5

Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'chart', 'indicator_buffers': 40, 'indicator_plots': 20}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Smoother rainbow', 'source': 'MQL5 Indicators/Smoother rainbow/Smoother rainbow.mq5', 'folder': 'Smoother rainbow', 'inputs': [{'mql': 'inpStep', 'py': 'inpStep', 'param': 'inpStep', 'type': 'double', 'default': 5.0, 'label': 'Step', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpColorUp', 'py': 'inpColorUp', 'param': None, 'type': 'color', 'default': 7451452, 'label': 'Up slope color', 'sinput': False}, {'mql': 'inpColorDn', 'py': 'inpColorDn', 'param': None, 'type': 'color', 'default': 6333684, 'label': 'Down slope color', 'sinput': False}, {'mql': 'inpLinesWidth', 'py': 'inpLinesWidth', 'param': 'inpLinesWidth', 'type': 'int', 'default': 0, 'label': 'Lines width', 'sinput': False}, {'mql': 'inpLinesStyle', 'py': 'inpLinesStyle', 'param': 'inpLinesStyle', 'type': 'int', 'default': 0, 'label': 'Lines style', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
inpStep = _input('inpStep', 5.0)  # Step
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpColorUp = _input('inpColorUp', clrMediumSeaGreen)  # Up slope color
inpColorDn = _input('inpColorDn', clrSandyBrown)  # Down slope color
inpLinesWidth = _input('inpLinesWidth', 0)  # Lines width
inpLinesStyle = _input('inpLinesStyle', STYLE_SOLID)  # Lines style

class simpleBuff(MqlObject):
    _q_fields = ('buffer', 'bufferColor')
    def __init__(self, *args):
        self.buffer = Arr(0, 0.0)
        self.bufferColor = Arr(0, 0.0)

class CSmoother(MqlObject):
    _q_fields = ('m_period', 'm_alpha', 'm_beta', 'm_arraySize', 'm_array')
    def __init__(self):
        self.m_period = 0.0
        self.m_alpha = 0.0
        self.m_beta = 0.0
        self.m_arraySize = 0
        self.m_array = Arr(0, 0, factory=CSmootherStruct)
        self.m_arraySize = -1
        self.m_alpha = 1.0
        self.m_beta = 1.0
    def _q_dtor(self):
        pass
    def init(self, period):
        self.m_period = (period if (period > 1) else 1)
        self.m_beta = _fdiv(0.45 * (self.m_period - 1.0), (0.45 * (self.m_period - 1)) + 2.0)
        self.m_alpha = self.m_beta * self.m_beta * self.m_beta
        return True
    def calculate(self, value, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        if i > 0:
            self.m_array[i].l0 = ((1.0 - self.m_alpha) * value) + (self.m_alpha * self.m_array[i - 1].l0)
            self.m_array[i].l1 = ((value - self.m_array[i].l0) * (1 - self.m_beta)) + (self.m_beta * self.m_array[i - 1].l1)
            self.m_array[i].l2 = self.m_array[i].l0 + self.m_array[i].l1
            self.m_array[i].l3 = ((self.m_array[i].l2 - self.m_array[i - 1].l4) * (1.0 - self.m_alpha) * (1.0 - self.m_alpha)) + (self.m_alpha * self.m_alpha * self.m_array[i - 1].l3)
            self.m_array[i].l4 = self.m_array[i - 1].l4 + self.m_array[i].l3
        else:
            self.m_array[i].l4 = value
            self.m_array[i].l1 = self.m_array[i].l4
            self.m_array[i].l0 = self.m_array[i].l1
            self.m_array[i].l3 = 0.0
            self.m_array[i].l2 = self.m_array[i].l3
        return self.m_array[i].l4

class CSmootherStruct(MqlObject):
    _q_fields = ('l0', 'l1', 'l2', 'l3', 'l4')
    def __init__(self, *args):
        self.l0 = 0.0
        self.l1 = 0.0
        self.l2 = 0.0
        self.l3 = 0.0
        self.l4 = 0.0

def OnInit():
    _step = (inpStep if (inpStep > 1) else 1.1)
    for i in range(0, 20):
        SetIndexBuffer(i * 2, wbuffer[i].buffer, INDICATOR_DATA)
        SetIndexBuffer((i * 2) + 1, wbuffer[i].bufferColor, INDICATOR_COLOR_INDEX)
        PlotIndexSetInteger(i, PLOT_DRAW_TYPE, DRAW_COLOR_LINE)
        PlotIndexSetInteger(i, PLOT_COLOR_INDEXES, 2)
        PlotIndexSetInteger(i, PLOT_LINE_COLOR, 0, inpColorUp)
        PlotIndexSetInteger(i, PLOT_LINE_COLOR, 1, inpColorDn)
        PlotIndexSetInteger(i, PLOT_LINE_WIDTH, inpLinesWidth)
        PlotIndexSetInteger(i, PLOT_LINE_STYLE, inpLinesStyle)
        PlotIndexSetString(i, PLOT_LABEL, 'Smoother (' + _str((i + 1) * _step) + ')')
        iSmoother[i].init((i + 1) * _step)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Smoother rainbow, step (' + _str(_step) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = prev_calculated - 1
    if i < 0:
        i = 0
    while i < rates_total:
        _price = 0.0
        _sw1 = inpPrice
        if _sw1 == PRICE_CLOSE:
            _price = close[i]
        elif _sw1 == PRICE_OPEN:
            _price = open[i]
        elif _sw1 == PRICE_HIGH:
            _price = high[i]
        elif _sw1 == PRICE_LOW:
            _price = low[i]
        elif _sw1 == PRICE_MEDIAN:
            _price = (high[i] + low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            _price = (high[i] + low[i] + close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            _price = (high[i] + low[i] + close[i] + close[i]) / 4.0
        else:
            _price = 0.0
        for k in range(0, 20):
            wbuffer[k].buffer[i] = iSmoother[k].calculate(_price, i, rates_total)
            wbuffer[k].bufferColor[i] = ((0 if (wbuffer[k].buffer[i] > wbuffer[k].buffer[i - 1]) else 1 if (wbuffer[k].buffer[i] < wbuffer[k].buffer[i - 1]) else wbuffer[k].bufferColor[i - 1]) if (i > 0) else 0)
        i += 1
    return i

# ---- global variables initialised from expressions
wbuffer = Arr(20, 0, dyn=False, factory=simpleBuff)
iSmoother = Arr(20, 0, dyn=False, factory=CSmoother)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SmootherRainbow(_MQL5Indicator):
    name = 'Smoother rainbow'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'inpStep': 5.0,  # Step
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpLinesWidth': 0,  # Lines width
        'inpLinesStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Lines style
    }

