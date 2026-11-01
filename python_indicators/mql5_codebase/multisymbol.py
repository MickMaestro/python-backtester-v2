"""MultiSymbol — converted from MQL5: MQL5 Indicators/Multi Symbol Chart/MultiSymbol.mq5

Multi Symbol
Copyright: Copyright 2018, pipPod.; Link: https://www.mql5.com/en/users/pippod; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, pipPod.', 'link': 'https://www.mql5.com/en/users/pippod', 'version': '1.10', 'window': 'separate', 'indicator_buffers': 20, 'indicator_plots': 4}, 'types': {1: 17, 2: 17, 3: 17, 4: 17}, 'colors': {1: [14772545, 3329330, 2237106], 2: [12632256, 3329330, 2237106], 3: [3329330, 2237106, 65535], 4: [3329330, 65535, 2237106]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Multi Symbol'], 'name': 'MultiSymbol', 'source': 'MQL5 Indicators/Multi Symbol Chart/MultiSymbol.mq5', 'folder': 'Multi Symbol Chart', 'inputs': [{'mql': 'Symbol1', 'py': 'Symbol1', 'param': None, 'type': 'string', 'default': 'EURUSD', 'label': 'Symbol 1', 'sinput': False}, {'mql': 'Symbol2', 'py': 'Symbol2', 'param': None, 'type': 'string', 'default': 'GBPUSD', 'label': 'Symbol 2', 'sinput': False}, {'mql': 'Symbol3', 'py': 'Symbol3', 'param': None, 'type': 'string', 'default': 'USDCHF', 'label': 'Symbol 3', 'sinput': False}, {'mql': 'Symbol4', 'py': 'Symbol4', 'param': None, 'type': 'string', 'default': 'USDJPY', 'label': 'Symbol 4', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

indicator_buffers = 20  # #property indicator_buffers
indicator_plots = 4  # #property indicator_plots

# ---- inputs and global variables
Symbol1 = _input('Symbol1', 'EURUSD')  # Symbol 1
Symbol2 = _input('Symbol2', 'GBPUSD')  # Symbol 2
Symbol3 = _input('Symbol3', 'USDCHF')  # Symbol 3
Symbol4 = _input('Symbol4', 'USDJPY')  # Symbol 4
symbol = Arr(indicator_plots, None, dyn=False)
chartID = 0
window = 0
toCopy = 0
Symbol_v = Arr(indicator_plots, "", dyn=False)

class CSymbol(MqlObject):
    _q_fields = ('m_handle', 'm_open', 'm_high', 'm_low', 'm_close', 'm_color')
    def __init__(self):
        self.m_handle = 0
        self.m_open = Arr(0, 0.0)
        self.m_high = Arr(0, 0.0)
        self.m_low = Arr(0, 0.0)
        self.m_close = Arr(0, 0.0)
        self.m_color = Arr(0, 0.0)
        self.m_handle = INVALID_HANDLE
        self.ArraySetAsSeries(True)
    def _q_dtor(self):
        IndicatorRelease(self.m_handle)
    def Handle(self, handle):
        return _setattr(self, 'm_handle', handle)
    def CopyBuffer(self, start, count):
        copied = 0
        if ((((copied := CopyBuffer(self.m_handle, 0, start, count, self.m_open)) < 1 or (copied := CopyBuffer(self.m_handle, 1, start, count, self.m_high)) < 1) or (copied := CopyBuffer(self.m_handle, 2, start, count, self.m_low)) < 1) or (copied := CopyBuffer(self.m_handle, 3, start, count, self.m_close)) < 1) or (copied := CopyBuffer(self.m_handle, 4, start, count, self.m_color)) < 1:
            return -1
        return copied
    def BarsCalculated(self):
        return self.BarsCalculated(self.m_handle)
    def SetIndexBuffer(self, index):
        return (((self.SetIndexBuffer(index, self.m_open) and self.SetIndexBuffer(index + 1, self.m_high)) and self.SetIndexBuffer(index + 2, self.m_low)) and self.SetIndexBuffer(index + 3, self.m_close)) and self.SetIndexBuffer(index + 4, self.m_color, INDICATOR_COLOR_INDEX)
    def ArraySetAsSeries(self, flag):
        return (((self.ArraySetAsSeries(_bool(self.m_open), flag) and self.ArraySetAsSeries(_bool(self.m_high), flag)) and self.ArraySetAsSeries(_bool(self.m_low), flag)) and self.ArraySetAsSeries(_bool(self.m_close), flag)) and self.ArraySetAsSeries(_bool(self.m_color), flag)
    def ArrayInitialize(self, value):
        return (((self.ArrayInitialize(self.m_open, value) and self.ArrayInitialize(self.m_high, value)) and self.ArrayInitialize(self.m_low, value)) and self.ArrayInitialize(self.m_close, value)) and self.ArrayInitialize(self.m_color, value)
    def ArrayFree(self):
        self.ArrayFree(self.m_open)
        self.ArrayFree(self.m_high)
        self.ArrayFree(self.m_low)
        self.ArrayFree(self.m_close)
        self.ArrayFree(self.m_color)

def OnInit():
    global chartID, window
    IndicatorSetInteger(0, INDICATOR_DIGITS, 4)
    chartID = ChartID()
    Symbol_v[0] = Symbol1
    Symbol_v[1] = Symbol2
    Symbol_v[2] = Symbol3
    Symbol_v[3] = Symbol4
    i = 0
    while i < indicator_plots:
        if not SymbolSelect(Symbol_v[i], True):
            Alert(Symbol_v[i], ' not available in Market Watch.\nInitialization Failed.')
            return INIT_FAILED
        PlotIndexSetString(i, PLOT_LABEL, Symbol_v[i] + ' Open;' + Symbol_v[i] + ' High;' + Symbol_v[i] + ' Low;' + Symbol_v[i] + ' Close;')
        if (not CheckPointer(_setitem(symbol, i, CSymbol()))) or symbol[i].Handle(iCustom(Symbol_v[i], PERIOD_CURRENT, 'PercentChange.ex5', chartID, i)) == INVALID_HANDLE:
            return INIT_FAILED
        i += 1
    shortName = 'Multi Symbol'
    IndicatorSetString(INDICATOR_SHORTNAME, shortName)
    window = _short(ChartWindowFind(chartID, shortName))
    CreateLabels()
    i = 0
    buf_num = 0
    while i < indicator_plots:
        symbol[i].SetIndexBuffer(buf_num)
        i += 1
        buf_num += 5
    i = 0
    while i < indicator_buffers:
        PlotIndexSetDouble(i, PLOT_EMPTY_VALUE, EMPTY_VALUE)
        i += 1
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    global toCopy
    limit = rates_total - prev_calculated
    if rates_total != prev_calculated:
        barsWindow = _int(ChartGetInteger(chartID, CHART_VISIBLE_BARS)) + 20
        if rates_total < barsWindow:
            return 0
        a = 0
        while a < indicator_plots:
            if (not CheckPointer(symbol[a])) or symbol[a].BarsCalculated() < barsWindow:
                return 0
            a += 1
        a = 0
        while a < indicator_plots:
            symbol[a].ArrayInitialize(EMPTY_VALUE)
            a += 1
        limit = barsWindow - 1
    else:
        return rates_total
    toCopy = limit + 1
    a = 0
    while a < indicator_plots:
        if OnTick(a, toCopy) < 1:
            return 0
        a += 1
    return rates_total

def OnDeinit(reason):
    ObjectsDeleteAll(chartID, window, OBJ_LABEL)
    a = 0
    while a < indicator_plots:
        if CheckPointer(symbol[a]):
            _delete(symbol[a])
        a += 1
    return

def OnTick(index, to_copy):
    if not CheckPointer(symbol[index]):
        return -1
    return symbol[index].CopyBuffer(0, to_copy)

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ >= CHARTEVENT_CUSTOM:
        OnTick(_int(lparam), (toCopy if _bool(dparam) else 1))

def CreateLabels():
    Label = Arr(indicator_plots * 2, "", dyn=False)
    Color = Arr.of([clrNONE], fill=0, dyn=False, size=indicator_plots * 2)
    i = 0
    j = 0
    k = 1
    while i < indicator_plots:
        Label[j] = StringSubstr(Symbol_v[i], 0, 3)
        Color[j] = _uint(PlotIndexGetInteger(i, PLOT_LINE_COLOR, 0))
        Label[k] = StringSubstr(Symbol_v[i], 3, 3)
        Color[k] = _uint(PlotIndexGetInteger(i, PLOT_LINE_COLOR, 1))
        i += 1
        j += 2
        k += 2
    xStart = 4
    xStart2 = 26
    xIncrement = 0
    yStart = 16
    yIncrement = 16
    i = 0
    k = 1
    while k < (indicator_plots * 2):
        name1 = _str(window + i)
        name2 = _str(window + k)
        ObjectCreate_u(name1, Label[i], xStart, yStart, Color[i])
        ObjectCreate_u(name2, Label[k], xStart2, yStart, Color[k])
        xStart += xIncrement
        yStart += yIncrement
        i += 2
        k += 2

def ObjectCreate_u(name, label, x, y, clr):
    ObjectCreate(chartID, name, OBJ_LABEL, window, 0, 0)
    ObjectSetString(chartID, name, OBJPROP_TEXT, label)
    ObjectSetString(chartID, name, OBJPROP_FONT, 'Arial Bold')
    ObjectSetInteger(chartID, name, OBJPROP_FONTSIZE, 8)
    ObjectSetInteger(chartID, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(chartID, name, OBJPROP_XDISTANCE, x)
    ObjectSetInteger(chartID, name, OBJPROP_YDISTANCE, y)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MultiSymbol(_MQL5Indicator):
    name = 'MultiSymbol'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

