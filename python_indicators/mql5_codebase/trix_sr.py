"""TRiX (sr) — converted from MQL5: MQL5 Indicators/Trix oscillator with support _ resistance lines on chart/TRiX (sr).mq5

Trix with support and resistance levels 
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [12632256, 16748574, 6333684]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'TRiX'}, 'levels': [], 'description': ['Trix with support and resistance levels '], 'name': 'TRiX (sr)', 'source': 'MQL5 Indicators/Trix oscillator with support _ resistance lines on chart/TRiX (sr).mq5', 'folder': 'Trix oscillator with support _ resistance lines on chart', 'inputs': [{'mql': 'inpPeriod', 'py': 'inpPeriod', 'param': 'inpPeriod', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpColorOn', 'py': 'inpColorOn', 'param': 'inpColorOn', 'type': 'int', 'default': 1, 'label': 'Color change mode', 'sinput': False}, {'mql': 'inpUniqueID', 'py': 'inpUniqueID', 'param': None, 'type': 'string', 'default': 'TrixLevels1', 'label': 'Unique ID for on chart objects', 'sinput': False}, {'mql': 'inpColorUp', 'py': 'inpColorUp', 'param': None, 'type': 'color', 'default': 16760576, 'label': 'Color for upper level broken line', 'sinput': False}, {'mql': 'inpColorDown', 'py': 'inpColorDown', 'param': None, 'type': 'color', 'default': 8036607, 'label': 'Color for lower level broken line', 'sinput': False}, {'mql': 'inpLinesWidth', 'py': 'inpLinesWidth', 'param': 'inpLinesWidth', 'type': 'int', 'default': 2, 'label': 'Lines width', 'sinput': False}, {'mql': 'inpLinesStyle', 'py': 'inpLinesStyle', 'param': 'inpLinesStyle', 'type': 'int', 'default': 0, 'label': 'Lines style', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorOn
on_slope = 0
on_zero = 1
_enum('enColorOn', {0: 'on_slope', 1: 'on_zero'})

# ---- inputs and global variables
inpPeriod = _input('inpPeriod', 14)  # Period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpColorOn = _input('inpColorOn', on_zero)  # Color change mode
inpUniqueID = _input('inpUniqueID', 'TrixLevels1')  # Unique ID for on chart objects
inpColorUp = _input('inpColorUp', clrDeepSkyBlue)  # Color for upper level broken line
inpColorDown = _input('inpColorDown', clrLightSalmon)  # Color for lower level broken line
inpLinesWidth = _input('inpLinesWidth', 2)  # Lines width
inpLinesStyle = _input('inpLinesStyle', STYLE_SOLID)  # Lines style
val = Arr(0, 0.0)
valc = Arr(0, 0.0)

class CTrix(MqlObject):
    _q_fields = ('m_period', 'm_alpha', 'm_arraySize', 'm_array')
    def __init__(self):
        self.m_period = 0.0
        self.m_alpha = 0.0
        self.m_arraySize = 0
        self.m_array = Arr(0, 0, factory=sTrixStruct)
        self.m_arraySize = -1
        self.m_alpha = 1.0
    def _q_dtor(self):
        ArrayFree(self.m_array)
    def init(self, period):
        self.m_period = (period if (period > 1) else 1)
        self.m_alpha = _fdiv(2.0, 1.0 + self.m_period)
        return True
    def calculate(self, price, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                return 0.0
        if i > 0:
            self.m_array[i].ema1 = self.m_array[i - 1].ema1 + (self.m_alpha * (price - self.m_array[i - 1].ema1))
            self.m_array[i].ema2 = self.m_array[i - 1].ema2 + (self.m_alpha * (self.m_array[i].ema1 - self.m_array[i - 1].ema2))
            self.m_array[i].ema3 = self.m_array[i - 1].ema3 + (self.m_alpha * (self.m_array[i].ema2 - self.m_array[i - 1].ema3))
            return _fdiv(self.m_array[i].ema3 - self.m_array[i - 1].ema3, self.m_array[i].ema3)
        else:
            self.m_array[i].ema3 = price
            self.m_array[i].ema2 = self.m_array[i].ema3
            self.m_array[i].ema1 = self.m_array[i].ema2
        return 0.0

class sTrixStruct(MqlObject):
    _q_fields = ('price', 'ema1', 'ema2', 'ema3')
    def __init__(self, *args):
        self.price = 0.0
        self.ema1 = 0.0
        self.ema2 = 0.0
        self.ema3 = 0.0

class COnChartSR(MqlObject):
    _q_fields = ('m_uniqueID', 'm_colorSup', 'm_colorRes', 'm_linesWidth', 'm_linesStyle', 'm_arraySize', 'm_array')
    def __init__(self):
        self.m_uniqueID = ""
        self.m_colorSup = 0
        self.m_colorRes = 0
        self.m_linesWidth = 0
        self.m_linesStyle = 0
        self.m_arraySize = 0
        self.m_array = Arr(0, 0, factory=sOnChartSRStruct)
        self.m_colorSup = clrOrangeRed
        self.m_colorRes = clrMediumSeaGreen
        self.m_linesWidth = 1
        self.m_linesStyle = STYLE_SOLID
        self.m_arraySize = -1
        return
    def _q_dtor(self):
        ObjectsDeleteAll(0, self.m_uniqueID + ':')
        ChartRedraw(0)
        return
    def setUniqueID(self, _id):
        self.m_uniqueID = _id
        return
    def setSupportColor(self, _color):
        self.m_colorSup = _color
        return
    def setResistanceColor(self, _color):
        self.m_colorRes = _color
        return
    def setLinesWidth(self, _width):
        self.m_linesWidth = _width
        return
    def setLinesStyle(self, _style):
        self.m_linesStyle = _style
        return
    def update(self, price, time, state, i, bars):
        if self.m_arraySize < bars:
            self.m_arraySize = ArrayResize(self.m_array, bars + 500)
            if self.m_arraySize < bars:
                return
        self.m_array[i].state = state
        if state == 0:
            self.m_array[i].time = time
            _name = self.m_uniqueID + ':' + _str(self.m_array[i].time)
            if ObjectFind(0, _name) >= 0:
                ObjectDelete(0, _name)
        elif i > 0:
            if self.m_array[i].state != self.m_array[i - 1].state:
                self.m_array[i].time = time
                _name = self.m_uniqueID + ':' + _str(time)
                ObjectCreate(0, _name, OBJ_TREND, 0, 0, 0)
                ObjectSetInteger(0, _name, OBJPROP_WIDTH, self.m_linesWidth)
                ObjectSetInteger(0, _name, OBJPROP_STYLE, self.m_linesStyle)
                ObjectSetInteger(0, _name, OBJPROP_COLOR, (self.m_colorRes if (state == 1) else self.m_colorSup))
                ObjectSetInteger(0, _name, OBJPROP_HIDDEN, True)
                ObjectSetInteger(0, _name, OBJPROP_BACK, True)
                ObjectSetInteger(0, _name, OBJPROP_SELECTABLE, False)
                ObjectSetInteger(0, _name, OBJPROP_RAY, False)
                ObjectSetInteger(0, _name, OBJPROP_TIME, 0, time)
                ObjectSetInteger(0, _name, OBJPROP_TIME, 1, time + PeriodSeconds(Period()))
                ObjectSetDouble(0, _name, OBJPROP_PRICE, 0, price)
                ObjectSetDouble(0, _name, OBJPROP_PRICE, 1, price)
            else:
                self.m_array[i].time = self.m_array[i - 1].time
                _name = self.m_uniqueID + ':' + _str(self.m_array[i].time)
                ObjectSetInteger(0, _name, OBJPROP_TIME, 1, time + PeriodSeconds(Period()))
        else:
            self.m_array[i].time = time

class sOnChartSRStruct(MqlObject):
    _q_fields = ('time', 'state')
    def __init__(self, *args):
        self.time = 0
        self.state = 0.0

def OnInit():
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    iTrix.init(inpPeriod)
    _srHandler.setUniqueID(inpUniqueID)
    _srHandler.setLinesStyle(inpLinesStyle)
    _srHandler.setLinesWidth(inpLinesWidth)
    _srHandler.setSupportColor(inpColorDown)
    _srHandler.setResistanceColor(inpColorUp)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TRiX with SR(' + _str(inpPeriod) + ')')
    return INIT_SUCCEEDED

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
        val[i] = iTrix.calculate(_price, i, rates_total)
        if inpColorOn == on_slope:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        else:
            valc[i] = (1 if (val[i] > 0) else 2 if (val[i] < 0) else 0)
        _srHandler.update(close[i], time[i], valc[i], i, rates_total)
        i += 1
    return i

# ---- global variables initialised from expressions
iTrix = _alloc(CTrix)
iTrix.__init__()
_srHandler = _alloc(COnChartSR)
_srHandler.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TRiXSr(_MQL5Indicator):
    name = 'TRiX (sr)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriod': 14,  # Period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpColorOn': _Choice({0: 'Change color on slope change', 1: 'Change color on zero cross'}, default=1),  # Color change mode
        'inpLinesWidth': 2,  # Lines width
        'inpLinesStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Lines style
    }

