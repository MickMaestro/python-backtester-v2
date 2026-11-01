"""candel 2 — converted from MQL5: MQL5 Indicators/Boom Index Spike Pattern/candel 2.mq5

Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'window': 'chart', 'version': '1.0'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'candel 2', 'source': 'MQL5 Indicators/Boom Index Spike Pattern/candel 2.mq5', 'folder': 'Boom Index Spike Pattern', 'inputs': [{'mql': 'BoxColor', 'py': 'BoxColor', 'param': None, 'type': 'color', 'default': 16711680, 'label': '', 'sinput': False}, {'mql': 'LineColor', 'py': 'LineColor', 'param': None, 'type': 'color', 'default': 3329330, 'label': '', 'sinput': False}, {'mql': 'BoxWidth', 'py': 'BoxWidth', 'param': 'BoxWidth', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'LineWidth', 'py': 'LineWidth', 'param': 'LineWidth', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'BoxStyle', 'py': 'BoxStyle', 'param': 'BoxStyle', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'LineStyle', 'py': 'LineStyle', 'param': 'LineStyle', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BoxColor = _input('BoxColor', clrBlue)
LineColor = _input('LineColor', clrLimeGreen)
BoxWidth = _input('BoxWidth', 2)
LineWidth = _input('LineWidth', 1)
BoxStyle = _input('BoxStyle', STYLE_SOLID)
LineStyle = _input('LineStyle', STYLE_SOLID)
zoneCount = 0

class Zone(MqlObject):
    _q_fields = ('boxTime', 'entryPrice', 'lineName', 'mitigated')
    def __init__(self, *args):
        self.boxTime = 0
        self.entryPrice = 0.0
        self.lineName = ""
        self.mitigated = False

def OnInit():
    global zoneCount
    zoneCount = 0
    ObjectsDeleteAll(0, 'Box_')
    ObjectsDeleteAll(0, 'Line_')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, 'Box_')
    ObjectsDeleteAll(0, 'Line_')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global zoneCount
    if rates_total < 10:
        return prev_calculated
    for i in range(rates_total - 4, 2 - 1, -1):
        body1 = MathAbs(open[i] - close[i])
        wick1 = high[i] - low[i]
        isGreenSpike1 = close[i] > open[i] and body1 > (0.7 * wick1)
        isRedMid = close[i + 1] < open[i + 1]
        body3 = MathAbs(open[i + 2] - close[i + 2])
        wick3 = high[i + 2] - low[i + 2]
        isGreenSpike2 = close[i + 2] > open[i + 2] and body3 > (0.7 * wick3)
        if (isGreenSpike1 and isRedMid) and isGreenSpike2:
            boxTime = time[i + 2]
            entryPrice = open[i + 1]
            exists = False
            for j in range(0, zoneCount):
                if zones[j].boxTime == boxTime:
                    exists = True
                    break
            if (not exists) and zoneCount < ArraySize(zones):
                top = MathMax(MathMax(high[i], high[i + 1]), high[i + 2])
                bottom = MathMin(MathMin(low[i], low[i + 1]), low[i + 2])
                boxName = 'Box_' + IntegerToString(_int(boxTime))
                ObjectCreate(0, boxName, OBJ_RECTANGLE, 0, time[i], top, boxTime, bottom)
                ObjectSetInteger(0, boxName, OBJPROP_COLOR, BoxColor)
                ObjectSetInteger(0, boxName, OBJPROP_WIDTH, BoxWidth)
                ObjectSetInteger(0, boxName, OBJPROP_STYLE, BoxStyle)
                ObjectSetInteger(0, boxName, OBJPROP_BACK, True)
                futureTime = TimeCurrent() + (PeriodSeconds() * 100)
                lineName = 'Line_' + IntegerToString(_int(boxTime))
                ObjectCreate(0, lineName, OBJ_TREND, 0, boxTime, entryPrice, futureTime, entryPrice)
                ObjectSetInteger(0, lineName, OBJPROP_COLOR, LineColor)
                ObjectSetInteger(0, lineName, OBJPROP_WIDTH, LineWidth)
                ObjectSetInteger(0, lineName, OBJPROP_STYLE, LineStyle)
                zones[zoneCount].boxTime = boxTime
                zones[zoneCount].entryPrice = entryPrice
                zones[zoneCount].lineName = lineName
                zones[zoneCount].mitigated = False
                zoneCount += 1
    for j in range(0, zoneCount):
        if zones[j].mitigated:
            continue
        for i in range(1, rates_total):
            if time[i] <= zones[j].boxTime:
                continue
            if low[i] <= zones[j].entryPrice and high[i] >= zones[j].entryPrice:
                if ObjectFind(0, zones[j].lineName) >= 0:
                    ObjectDelete(0, zones[j].lineName)
                fixedName = zones[j].lineName + '_Fixed'
                ObjectCreate(0, fixedName, OBJ_TREND, 0, zones[j].boxTime, zones[j].entryPrice, time[i], zones[j].entryPrice)
                ObjectSetInteger(0, fixedName, OBJPROP_COLOR, LineColor)
                ObjectSetInteger(0, fixedName, OBJPROP_WIDTH, LineWidth)
                ObjectSetInteger(0, fixedName, OBJPROP_STYLE, LineStyle)
                zones[j].mitigated = True
                break
    return rates_total

# ---- global variables initialised from expressions
zones = Arr(100, 0, dyn=False, factory=Zone)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Candel2(_MQL5Indicator):
    name = 'candel 2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BoxWidth': 2,
        'LineWidth': 1,
        'BoxStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),
        'LineStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),
    }

