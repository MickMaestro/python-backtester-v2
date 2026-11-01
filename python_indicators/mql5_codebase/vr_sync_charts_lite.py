"""VR-Sync-Charts-Lite — converted from MQL5: MQL5 Indicators/VR Sync Chart Lite MT 5/VR-Sync-Charts-Lite.mq5

Indicator for synchronizing graphical objects on different charts
Synchronizes all properties of objects and their location.
For maximum efficiency, place the indicator on open charts.
Copyright: Copyright 2020, Trading-go Project.; Link: https://trading-go.ru; Version: 20.052

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, Trading-go Project.', 'link': 'https://trading-go.ru', 'version': '20.052', 'window': 'chart', 'indicator_plots': 0, 'indicator_buffers': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Indicator for synchronizing graphical objects on different charts', 'Synchronizes all properties of objects and their location.', 'For maximum efficiency, place the indicator on open charts.'], 'name': 'VR-Sync-Charts-Lite', 'source': 'MQL5 Indicators/VR Sync Chart Lite MT 5/VR-Sync-Charts-Lite.mq5', 'folder': 'VR Sync Chart Lite MT 5', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
names = ''

class CCore(MqlObject):
    _q_fields = ('window',)
    def __init__(self, *args):
        self.window = Arr(0, 0, factory=CHART)
    def GetAllCharts(self, chart):
        i = 0
        prevChart = ChartFirst()
        ArrayResize(chart, i + 1, 1000)
        chart[i].id = prevChart
        chart[i].sy = ChartSymbol(prevChart)
        chart[i].tf = ChartPeriod(prevChart)
        while i < 30:
            i += 1
            if (prevChart := ChartNext(prevChart)) < 0:
                ResetLastError()
                return i
            ArrayResize(chart, i + 1, 1000)
            chart[i].id = prevChart
            chart[i].sy = ChartSymbol(prevChart)
            chart[i].tf = ChartPeriod(prevChart)
        return i
    def SetObjects(self, aName):
        global back, color_1, fill, price_1, price_2, style, time_1, time_2, width
        chart_ID = ChartID()
        xType = ObjectGetInteger(chart_ID, aName, OBJPROP_TYPE)
        name = aName
        sy = Symbol()
        if xType == OBJ_RECTANGLE:
            price_1 = ObjectGetDouble(chart_ID, name, OBJPROP_PRICE, 0)
            price_2 = ObjectGetDouble(chart_ID, name, OBJPROP_PRICE, 1)
            time_1 = ObjectGetInteger(chart_ID, name, OBJPROP_TIME, 0)
            time_2 = ObjectGetInteger(chart_ID, name, OBJPROP_TIME, 1)
            color_1 = _uint(ObjectGetInteger(chart_ID, name, OBJPROP_COLOR))
            back = (ObjectGetInteger(chart_ID, name, OBJPROP_BACK) != 0)
            style = ObjectGetInteger(chart_ID, name, OBJPROP_STYLE)
            width = ObjectGetInteger(chart_ID, name, OBJPROP_WIDTH)
            fill = (ObjectGetInteger(chart_ID, name, OBJPROP_FILL) != 0)
            if ((time_1 != 0 and price_1 != 0) and price_2 != 0) and time_2 != 0:
                for i in range(0, ArraySize(core.window)):
                    if core.window[i].sy == sy:
                        dt = _int(SymbolInfoInteger(core.window[i].sy, SYMBOL_DIGITS))
                        price_1 = NormalizeDouble(price_1, dt)
                        price_2 = NormalizeDouble(price_2, dt)
                        if ObjectFind(core.window[i].id, name) != 0:
                            ObjectCreate(core.window[i].id, name, xType, 0, time_1, price_1, time_2, price_2)
                        else:
                            ObjectSetDouble(core.window[i].id, name, OBJPROP_PRICE, 0, price_1)
                            ObjectSetDouble(core.window[i].id, name, OBJPROP_PRICE, 1, price_2)
                            ObjectSetInteger(core.window[i].id, name, OBJPROP_TIME, 0, time_1)
                            ObjectSetInteger(core.window[i].id, name, OBJPROP_TIME, 1, time_2)
                            ObjectSetInteger(core.window[i].id, name, OBJPROP_COLOR, color_1)
                            ObjectSetInteger(core.window[i].id, name, OBJPROP_BACK, back)
                            ObjectSetInteger(core.window[i].id, name, OBJPROP_STYLE, style)
                            ObjectSetInteger(core.window[i].id, name, OBJPROP_WIDTH, width)
                            ObjectSetInteger(core.window[i].id, name, OBJPROP_FILL, fill)
                            ObjectSetInteger(core.window[i].id, name, OBJPROP_SELECTABLE, True)
                        ChartRedraw(core.window[i].id)
        return False
    def SetDeleteObject(self, aName, aWindow):
        if ObjectDelete(aWindow, aName):
            ChartRedraw(aWindow)
            return True
        return False

class CHART(MqlObject):
    _q_fields = ('id', 'sy', 'tf')
    def __init__(self, *args):
        self.id = 0
        self.sy = ""
        self.tf = 0

def OnInit():
    Comment('')
    ChartSetInteger(ChartID(), CHART_EVENT_MOUSE_MOVE, True)
    ChartSetInteger(ChartID(), CHART_EVENT_OBJECT_CREATE, True)
    ChartSetInteger(ChartID(), CHART_EVENT_OBJECT_DELETE, True)
    core.GetAllCharts(core.window)
    return INIT_SUCCEEDED

def OnChartEvent(id_, lparam, dparam, sparam):
    global names
    if id_ == CHARTEVENT_OBJECT_CLICK:
        names = sparam
        core.SetObjects(sparam)
    if id_ == CHARTEVENT_OBJECT_CREATE:
        names = sparam
        core.SetObjects(names)
    if id_ == CHARTEVENT_OBJECT_CHANGE:
        core.SetObjects(sparam)
    if id_ == CHARTEVENT_OBJECT_DRAG:
        core.SetObjects(sparam)
    if id_ == CHARTEVENT_MOUSE_MOVE:
        core.SetObjects(names)
    if id_ == CHARTEVENT_OBJECT_DELETE:
        for i in range(0, ArraySize(core.window)):
            if ObjectDelete(core.window[i].id, sparam):
                ChartRedraw(core.window[i].id)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def OnDeinit(reason):
    pass

# ---- global variables initialised from expressions
time_1 = 0
time_2 = 0
price_1 = 0.0
price_2 = 0.0
color_1 = 0
back = False
fill = False
style = 0
width = 0
core = _alloc(CCore)
core.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VRSyncChartsLite(_MQL5Indicator):
    name = 'VR-Sync-Charts-Lite'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

