"""MACD (sr) — converted from MQL5: MQL5 Indicators/MACD with on-chart SR levels/MACD (sr).mq5

MACD with support and resistance levels 
Copyright: © mladen, 2019; Link: mladenfx@gmail.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2019', 'link': 'mladenfx@gmail.com', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [11119017, 16760576, 8036607], 2: [8421504]}, 'widths': {1: 2}, 'styles': {2: 2}, 'labels': {1: 'MACD', 2: 'Signal'}, 'levels': [], 'description': ['MACD with support and resistance levels '], 'name': 'MACD (sr)', 'source': 'MQL5 Indicators/MACD with on-chart SR levels/MACD (sr).mq5', 'folder': 'MACD with on-chart SR levels', 'inputs': [{'mql': 'inpPeriodFast', 'py': 'inpPeriodFast', 'param': 'inpPeriodFast', 'type': 'int', 'default': 12, 'label': 'Fast MACD period', 'sinput': False}, {'mql': 'inpPeriodSlow', 'py': 'inpPeriodSlow', 'param': 'inpPeriodSlow', 'type': 'int', 'default': 26, 'label': 'Slow MACD period', 'sinput': False}, {'mql': 'inpPeriodSign', 'py': 'inpPeriodSign', 'param': 'inpPeriodSign', 'type': 'int', 'default': 9, 'label': 'Signal period', 'sinput': False}, {'mql': 'inpPrice', 'py': 'inpPrice', 'param': 'inpPrice', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'inpColorOn', 'py': 'inpColorOn', 'param': 'inpColorOn', 'type': 'int', 'default': 2, 'label': 'Color change mode', 'sinput': False}, {'mql': 'inpUniqueID', 'py': 'inpUniqueID', 'param': None, 'type': 'string', 'default': 'MacdLevels1', 'label': 'Unique ID for on chart objects', 'sinput': False}, {'mql': 'inpColorUp', 'py': 'inpColorUp', 'param': None, 'type': 'color', 'default': 16760576, 'label': 'Color for upper level broken line', 'sinput': False}, {'mql': 'inpColorDown', 'py': 'inpColorDown', 'param': None, 'type': 'color', 'default': 8036607, 'label': 'Color for lower level broken line', 'sinput': False}, {'mql': 'inpLinesWidth', 'py': 'inpLinesWidth', 'param': 'inpLinesWidth', 'type': 'int', 'default': 2, 'label': 'Lines width', 'sinput': False}, {'mql': 'inpLinesStyle', 'py': 'inpLinesStyle', 'param': 'inpLinesStyle', 'type': 'int', 'default': 0, 'label': 'Lines style', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum enColorOn
col_onSlope = 0
col_onZero = 1
col_onSignal = 2
_enum('enColorOn', {0: 'col_onSlope', 1: 'col_onZero', 2: 'col_onSignal'})

# ---- inputs and global variables
inpPeriodFast = _input('inpPeriodFast', 12)  # Fast MACD period
inpPeriodSlow = _input('inpPeriodSlow', 26)  # Slow MACD period
inpPeriodSign = _input('inpPeriodSign', 9)  # Signal period
inpPrice = _input('inpPrice', PRICE_CLOSE)  # Price
inpColorOn = _input('inpColorOn', col_onSignal)  # Color change mode
inpUniqueID = _input('inpUniqueID', 'MacdLevels1')  # Unique ID for on chart objects
inpColorUp = _input('inpColorUp', clrDeepSkyBlue)  # Color for upper level broken line
inpColorDown = _input('inpColorDown', clrLightSalmon)  # Color for lower level broken line
inpLinesWidth = _input('inpLinesWidth', 2)  # Lines width
inpLinesStyle = _input('inpLinesStyle', STYLE_SOLID)  # Lines style
val = Arr(0, 0.0)
valc = Arr(0, 0.0)
vals = Arr(0, 0.0)
ª_indHandle = 0

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
    global ª_indHandle
    SetIndexBuffer(0, val, INDICATOR_DATA)
    SetIndexBuffer(1, valc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, vals, INDICATOR_DATA)
    ª_indHandle = iMACD(Symbol(), 0, inpPeriodFast, inpPeriodSlow, inpPeriodSign, inpPrice)
    if not _checkHandle(ª_indHandle, 'MACD'):
        return INIT_FAILED
    _srHandler.setUniqueID(inpUniqueID)
    _srHandler.setLinesStyle(inpLinesStyle)
    _srHandler.setLinesWidth(inpLinesWidth)
    _srHandler.setSupportColor(inpColorDown)
    _srHandler.setResistanceColor(inpColorUp)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MACD with SR levels (' + _str(inpPeriodFast) + ',' + _str(inpPeriodSlow) + ',' + _str(inpPeriodSign) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    _copyCount = rates_total - prev_calculated + 1
    if _copyCount > rates_total:
        _copyCount = rates_total
    if CopyBuffer(ª_indHandle, 0, 0, _copyCount, val) != _copyCount:
        return prev_calculated
    if CopyBuffer(ª_indHandle, 1, 0, _copyCount, vals) != _copyCount:
        return prev_calculated
    i = ((prev_calculated - 1) if (prev_calculated > 0) else 0)
    while i < rates_total:
        _sw1 = inpColorOn
        if _sw1 == col_onZero:
            valc[i] = (1 if (val[i] > 0) else 2 if (val[i] < 0) else 0)
        elif _sw1 == col_onSlope:
            valc[i] = ((1 if (val[i] > val[i - 1]) else 2 if (val[i] < val[i - 1]) else valc[i - 1]) if (i > 0) else 0)
        elif _sw1 == col_onSignal:
            valc[i] = (1 if (val[i] > vals[i]) else 2 if (val[i] < vals[i]) else 0)
        _srHandler.update(close[i], time[i], valc[i], i, rates_total)
        i += 1
    return i

def _checkHandle(_handle, _description):
    _size = ArraySize(_s__checkHandle__handles)
    _answer = _handle != INVALID_HANDLE
    if _answer:
        ArrayResize(_s__checkHandle__handles, _size + 1)
        _s__checkHandle__handles[_size] = _handle
    else:
        for i in range(_size - 1, 0 - 1, -1):
            IndicatorRelease(_s__checkHandle__handles[i])
        ArrayResize(_s__checkHandle__handles, 0)
        Alert(_description + ' initialization failed')
    return _answer

# ---- global variables initialised from expressions
_srHandler = _alloc(COnChartSR)
_srHandler.__init__()

# ---- static local variables
_s__checkHandle__handles = Arr(0, 0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MACDSr(_MQL5Indicator):
    name = 'MACD (sr)'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpPeriodFast': 12,  # Fast MACD period
        'inpPeriodSlow': 26,  # Slow MACD period
        'inpPeriodSign': 9,  # Signal period
        'inpPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'inpColorOn': _Choice({0: 'Change color on macd slope change', 1: 'Change color on zero cross', 2: 'Change color on signal line cross'}, default=2),  # Color change mode
        'inpLinesWidth': 2,  # Lines width
        'inpLinesStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Lines style
    }

