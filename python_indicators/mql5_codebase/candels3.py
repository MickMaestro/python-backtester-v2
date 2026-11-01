"""candels3 — converted from MQL5: MQL5 Indicators/Crash Spike Trade Pattern/candels3.mq5

Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'window': 'chart', 'version': '1.0'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'candels3', 'source': 'MQL5 Indicators/Crash Spike Trade Pattern/candels3.mq5', 'folder': 'Crash Spike Trade Pattern', 'inputs': [{'mql': 'BoxColor', 'py': 'BoxColor', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'LineColor', 'py': 'LineColor', 'param': None, 'type': 'color', 'default': 16748574, 'label': '', 'sinput': False}, {'mql': 'BoxWidth', 'py': 'BoxWidth', 'param': 'BoxWidth', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'LineWidth', 'py': 'LineWidth', 'param': 'LineWidth', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'BoxStyle', 'py': 'BoxStyle', 'param': 'BoxStyle', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'LineStyle', 'py': 'LineStyle', 'param': 'LineStyle', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BoxColor = _input('BoxColor', clrRed)
LineColor = _input('LineColor', clrDodgerBlue)
BoxWidth = _input('BoxWidth', 2)
LineWidth = _input('LineWidth', 1)
BoxStyle = _input('BoxStyle', STYLE_SOLID)
LineStyle = _input('LineStyle', STYLE_SOLID)
zoneCount = 0
lastProcessedTime = 0

class Zone(MqlObject):
    _q_fields = ('boxTime', 'entryPrice', 'lineName', 'mitigated')
    def __init__(self, *args):
        self.boxTime = 0
        self.entryPrice = 0.0
        self.lineName = ""
        self.mitigated = False

def OnInit():
    global lastProcessedTime, zoneCount
    zoneCount = 0
    lastProcessedTime = 0
    ObjectsDeleteAll(0, 'Box_')
    ObjectsDeleteAll(0, 'Line_')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, 'Box_')
    ObjectsDeleteAll(0, 'Line_')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global lastProcessedTime
    if prev_calculated == 0 or rates_total > prev_calculated:
        ProcessHistory(rates_total, time, open, high, low, close)
    if TimeCurrent() > lastProcessedTime:
        ProcessRealtime()
        lastProcessedTime = TimeCurrent()
    return rates_total

def ProcessHistory(rates_total, time, open, high, low, close):
    if rates_total < 10:
        return
    for i in range(rates_total - 4, 2 - 1, -1):
        if time[i + 2] <= lastProcessedTime:
            continue
        body1 = MathAbs(open[i] - close[i])
        wick1 = high[i] - low[i]
        isRedSpike1 = close[i] < open[i] and body1 > (0.7 * wick1)
        isGreenMid = close[i + 1] > open[i + 1]
        body3 = MathAbs(open[i + 2] - close[i + 2])
        wick3 = high[i + 2] - low[i + 2]
        isRedSpike2 = close[i + 2] < open[i + 2] and body3 > (0.7 * wick3)
        if (isRedSpike1 and isGreenMid) and isRedSpike2:
            CreateZone(time[i], time[i + 2], high[i], high[i + 1], high[i + 2], low[i], low[i + 1], low[i + 2], open[i + 1])
    CheckMitigationHistory(rates_total, time, low, high)

def ProcessRealtime():
    rt = Arr(0, 0, factory=MqlRates)
    CopyRates(None, 0, 0, 4, rt)
    if ArraySize(rt) < 4:
        return
    if (TimeCurrent() - rt[0].time) < PeriodSeconds():
        return
    for i in range(3, 2 - 1, -1):
        if rt[i].time <= lastProcessedTime:
            continue
        body1 = MathAbs(rt[i - 2].open - rt[i - 2].close)
        wick1 = rt[i - 2].high - rt[i - 2].low
        isRedSpike1 = rt[i - 2].close < rt[i - 2].open and body1 > (0.7 * wick1)
        isGreenMid = rt[i - 1].close > rt[i - 1].open
        body3 = MathAbs(rt[i].open - rt[i].close)
        wick3 = rt[i].high - rt[i].low
        isRedSpike2 = rt[i].close < rt[i].open and body3 > (0.7 * wick3)
        if (isRedSpike1 and isGreenMid) and isRedSpike2:
            CreateZone(rt[i - 2].time, rt[i].time, rt[i - 2].high, rt[i - 1].high, rt[i].high, rt[i - 2].low, rt[i - 1].low, rt[i].low, rt[i - 1].open)
    CheckMitigationRealtime()

def CreateZone(startTime, endTime, high1, high2, high3, low1, low2, low3, entryPrice):
    global zoneCount
    exists = False
    for j in range(0, zoneCount):
        if zones[j].boxTime == endTime:
            exists = True
            break
    if (not exists) and zoneCount < ArraySize(zones):
        top = MathMax(MathMax(high1, high2), high3)
        bottom = MathMin(MathMin(low1, low2), low3)
        boxName = 'Box_' + IntegerToString(_int(endTime))
        ObjectCreate(0, boxName, OBJ_RECTANGLE, 0, startTime, top, endTime, bottom)
        ObjectSetInteger(0, boxName, OBJPROP_COLOR, BoxColor)
        ObjectSetInteger(0, boxName, OBJPROP_WIDTH, BoxWidth)
        ObjectSetInteger(0, boxName, OBJPROP_STYLE, BoxStyle)
        ObjectSetInteger(0, boxName, OBJPROP_BACK, True)
        futureTime = TimeCurrent() + (PeriodSeconds() * 100)
        lineName = 'Line_' + IntegerToString(_int(endTime))
        ObjectCreate(0, lineName, OBJ_TREND, 0, endTime, entryPrice, futureTime, entryPrice)
        ObjectSetInteger(0, lineName, OBJPROP_COLOR, LineColor)
        ObjectSetInteger(0, lineName, OBJPROP_WIDTH, LineWidth)
        ObjectSetInteger(0, lineName, OBJPROP_STYLE, LineStyle)
        zones[zoneCount].boxTime = endTime
        zones[zoneCount].entryPrice = entryPrice
        zones[zoneCount].lineName = lineName
        zones[zoneCount].mitigated = False
        zoneCount += 1

def CheckMitigationHistory(rates_total, time, low, high):
    j = 0
    while j < zoneCount:
        if zones[j].mitigated:
            j += 1
            continue
        for i in range(1, rates_total):
            if time[i] <= zones[j].boxTime:
                continue
            if low[i] <= zones[j].entryPrice and high[i] >= zones[j].entryPrice:
                MitigateZone(j, time[i])
                break
        j += 1

def CheckMitigationRealtime():
    current = Arr(0, 0, factory=MqlRates)
    CopyRates(None, 0, 0, 1, current)
    if ArraySize(current) < 1:
        return
    j = 0
    while j < zoneCount:
        if zones[j].mitigated:
            j += 1
            continue
        if current[0].low <= zones[j].entryPrice and current[0].high >= zones[j].entryPrice:
            MitigateZone(j, current[0].time)
        j += 1

def MitigateZone(zoneIndex, mitigationTime):
    if ObjectFind(0, zones[zoneIndex].lineName) >= 0:
        ObjectDelete(0, zones[zoneIndex].lineName)
    fixedName = zones[zoneIndex].lineName + '_Fixed'
    ObjectCreate(0, fixedName, OBJ_TREND, 0, zones[zoneIndex].boxTime, zones[zoneIndex].entryPrice, mitigationTime, zones[zoneIndex].entryPrice)
    ObjectSetInteger(0, fixedName, OBJPROP_COLOR, LineColor)
    ObjectSetInteger(0, fixedName, OBJPROP_WIDTH, LineWidth)
    ObjectSetInteger(0, fixedName, OBJPROP_STYLE, LineStyle)
    zones[zoneIndex].mitigated = True

# ---- global variables initialised from expressions
zones = Arr(100, 0, dyn=False, factory=Zone)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Candels3(_MQL5Indicator):
    name = 'candels3'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BoxWidth': 2,
        'LineWidth': 1,
        'BoxStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),
        'LineStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),
    }

