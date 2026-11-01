"""Hacking Objects — converted from MQL5: MQL5 Indicators/Hacking objects in an EX5/Hacking Objects.mq5

Modification of objects within an EX5 indicator
Copyright: Copyright 2024, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Modification of objects within an EX5 indicator'], 'name': 'Hacking Objects', 'source': 'MQL5 Indicators/Hacking objects in an EX5/Hacking Objects.mq5', 'folder': 'Hacking objects in an EX5', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
obj_prefix_1 = 'PZMDALS-diagonal'
obj_prefix_2 = 'PZMDALS-confluence'
handle = INVALID_HANDLE
indicatorShortName = ''

def OnInit():
    global indicatorShortName
    if handle == INVALID_HANDLE:
        if handle != INVALID_HANDLE:
            ChartIndicatorAdd(0, 0, handle)
    ModifyChartObjects(obj_prefix_1, 2)
    ModifyChartObjects(obj_prefix_2, 20)
    ChartRedraw(0)
    indicatorShortName = ChartIndicatorName(0, 0, 1)
    ChartIndicatorDelete(0, 0, indicatorShortName)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    IndicatorRelease(handle)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ModifyChartObjects(obj_prefix_1, 2)
    ModifyChartObjects(obj_prefix_2, 20)
    return rates_total

def LogChartObjectNames():
    total = ObjectsTotal(0)
    for i in range(0, total):
        name = ObjectName(0, i)
        Print('Chart Object Name: ', name)

def ModifyChartObjects(prefix, spared):
    totalObjects = ObjectsTotal(0)
    for i in range(totalObjects - 1 - spared, 0 - 1, -1):
        objName = ObjectName(0, i)
        currentCol = ObjectGetInteger(0, objName, OBJPROP_COLOR)
        if StringFind(objName, prefix) == 0 and currentCol != clrNONE:
            ObjectSetInteger(0, objName, OBJPROP_COLOR, clrNONE)
    for i in range(totalObjects - 1, totalObjects - spared - 1, -1):
        objName = ObjectName(0, i)
        currentWidth = ObjectGetInteger(0, objName, OBJPROP_WIDTH)
        if StringFind(objName, obj_prefix_1) == 0 and currentWidth != 3:
            ObjectSetInteger(0, objName, OBJPROP_WIDTH, 3)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HackingObjects(_MQL5Indicator):
    name = 'Hacking Objects'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

