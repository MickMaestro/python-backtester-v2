"""Auto TrendLine — converted from MQL5: MQL5 Indicators/AutoTrendLines Indicator for MQL5/Auto TrendLine.mq5

Automatic trend lines
Copyright: Copyright 2012, Rone.; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Unresolved names: operator
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, Rone.', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Automatic trend lines'], 'name': 'Auto TrendLine', 'source': 'MQL5 Indicators/AutoTrendLines Indicator for MQL5/Auto TrendLine.mq5', 'folder': 'AutoTrendLines Indicator for MQL5', 'inputs': [{'mql': 'InpLineType', 'py': 'InpLineType', 'param': 'InpLineType', 'type': 'int', 'default': 1, 'label': 'Line type', 'sinput': False}, {'mql': 'InpLeftExmSide', 'py': 'InpLeftExmSide', 'param': 'InpLeftExmSide', 'type': 'int', 'default': 20, 'label': 'Left extremum side (Type 1, 2)', 'sinput': False}, {'mql': 'InpRightExmSide', 'py': 'InpRightExmSide', 'param': 'InpRightExmSide', 'type': 'int', 'default': 3, 'label': 'Right extremum side (Type 1)', 'sinput': False}, {'mql': 'InpFromCurrent', 'py': 'InpFromCurrent', 'param': 'InpFromCurrent', 'type': 'int', 'default': 3, 'label': 'Offset from the current bar� (Type 2)', 'sinput': False}, {'mql': 'InpPrevExmBar', 'py': 'InpPrevExmBar', 'param': 'InpPrevExmBar', 'type': 'bool', 'default': False, 'label': 'Account for the bar before the extremum (Type 2)', 'sinput': False}, {'mql': 'InpLinesWidth', 'py': 'InpLinesWidth', 'param': 'InpLinesWidth', 'type': 'int', 'default': 1, 'label': 'lines width', 'sinput': False}, {'mql': 'InpSupColor', 'py': 'InpSupColor', 'param': None, 'type': 'color', 'default': 12745215, 'label': 'Support line color', 'sinput': False}, {'mql': 'InpResColor', 'py': 'InpResColor', 'param': None, 'type': 'color', 'default': 16765254, 'label': 'Resistance line color', 'sinput': False}, {'mql': 'InstanceName', 'py': 'InstanceName', 'param': None, 'type': 'string', 'default': 'AutoTrendLines1', 'label': 'Instance name', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_LINE_TYPE
EXM_EXM = 0
EXM_DELTA = 1
_enum('ENUM_LINE_TYPE', {0: 'EXM_EXM', 1: 'EXM_DELTA'})

# ---- inputs and global variables
InpLineType = _input('InpLineType', EXM_DELTA)  # Line type
InpLeftExmSide = _input('InpLeftExmSide', 20)  # Left extremum side (Type 1, 2)
InpRightExmSide = _input('InpRightExmSide', 3)  # Right extremum side (Type 1)
InpFromCurrent = _input('InpFromCurrent', 3)  # Offset from the current bar� (Type 2)
InpPrevExmBar = _input('InpPrevExmBar', False)  # Account for the bar before the extremum (Type 2)
InpLinesWidth = _input('InpLinesWidth', 1)  # lines width
InpSupColor = _input('InpSupColor', 0xC279FF)  # Support line color
InpResColor = _input('InpResColor', 0xFFD146)  # Resistance line color
InstanceName = _input('InstanceName', 'AutoTrendLines1')  # Instance name
minRequiredBars = 0

class CPoint(MqlObject):
    _q_fields = ('price', 'time')
    def _q_ctor1(self):
        self.price = 0.0
        self.time = 0
        self.price = 0.0
        self.time = 0
    def _q_ctor2(self, p, t):
        self.price = 0.0
        self.time = 0
        self.price = p
        self.time = t
    def __init__(self, *args):
        if 0 <= len(args) <= 0:
            self._q_ctor1(*args)
            return
        if 2 <= len(args) <= 2 and (len(args) == 0 or isinstance(args[0], float)):
            self._q_ctor2(*args)
            return
        self._q_ctor1(*args)
    def _q_dtor(self):
        pass
    def setPoint(self, p, t):
        self.price = p
        self.time = t
    def __eq__(self, other):
        return self.price == other.price and self.time == other.time
    __hash__ = MqlObject.__hash__
    def __ne__(self, other):
        return (not operator) == other
    def _q_assign(self, other):
        self.price = other.price
        self.time = other.time
    def getPrice(self):
        return self.price
    def getTime(self):
        return self.time

def OnInit():
    global minRequiredBars
    minRequiredBars = (InpLeftExmSide * 2) + (MathMax(InpRightExmSide, InpFromCurrent) * 2)
    return 0

def OnDeinit(reason):
    ObjectsDeleteAll(0, InstanceName)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    leftIndex = 0
    rightIndex = 0
    delta = 0.0
    tmpDelta = 0.0
    if rates_total < minRequiredBars:
        Print('Not enough data to calculate')
        return 0
    if prev_calculated != rates_total:
        _sw1 = InpLineType
        if _sw1 == EXM_DELTA:
            leftIndex = rates_total - InpLeftExmSide - 2
            while (not isLowestLow(leftIndex, InpLeftExmSide, low)) and leftIndex > minRequiredBars:
                pass
                leftIndex -= 1
            curLeftSup.setPoint(low[leftIndex], time[leftIndex])
            rightIndex = rates_total - InpFromCurrent - 2
            delta = _fdiv(low[rightIndex] - low[leftIndex], rightIndex - leftIndex)
            if not InpPrevExmBar:
                leftIndex += 1
            for tmpIndex in range(rightIndex - 1, leftIndex, -1):
                tmpDelta = _fdiv(low[tmpIndex] - curLeftSup.getPrice(), tmpIndex - leftIndex)
                if tmpDelta < delta:
                    delta = tmpDelta
                    rightIndex = tmpIndex
            curRightSup.setPoint(low[rightIndex], time[rightIndex])
            leftIndex = rates_total - InpLeftExmSide - 2
            while (not isHighestHigh(leftIndex, InpLeftExmSide, high)) and leftIndex > minRequiredBars:
                pass
                leftIndex -= 1
            curLeftRes.setPoint(high[leftIndex], time[leftIndex])
            rightIndex = rates_total - InpFromCurrent - 2
            delta = _fdiv(high[leftIndex] - high[rightIndex], rightIndex - leftIndex)
            if not InpPrevExmBar:
                leftIndex += 1
            for tmpIndex in range(rightIndex - 1, leftIndex, -1):
                tmpDelta = _fdiv(curLeftRes.getPrice() - high[tmpIndex], tmpIndex - leftIndex)
                if tmpDelta < delta:
                    delta = tmpDelta
                    rightIndex = tmpIndex
            curRightRes.setPoint(high[rightIndex], time[rightIndex])
        else:
            rightIndex = rates_total - InpRightExmSide - 2
            while (not isLowestLow(rightIndex, InpRightExmSide, low)) and rightIndex > minRequiredBars:
                pass
                rightIndex -= 1
            curRightSup.setPoint(low[rightIndex], time[rightIndex])
            leftIndex = rightIndex - InpRightExmSide
            while (not isLowestLow(leftIndex, InpLeftExmSide, low)) and leftIndex > minRequiredBars:
                pass
                leftIndex -= 1
            curLeftSup.setPoint(low[leftIndex], time[leftIndex])
            rightIndex = rates_total - InpRightExmSide - 2
            while (not isHighestHigh(rightIndex, InpRightExmSide, high)) and rightIndex > minRequiredBars:
                pass
                rightIndex -= 1
            curRightRes.setPoint(high[rightIndex], time[rightIndex])
            leftIndex = rightIndex - InpRightExmSide
            while (not isHighestHigh(leftIndex, InpLeftExmSide, high)) and leftIndex > minRequiredBars:
                pass
                leftIndex -= 1
            curLeftRes.setPoint(high[leftIndex], time[leftIndex])
        if curLeftSup != nullPoint and curRightSup != nullPoint:
            drawLine('Current_Support', curRightSup, curLeftSup, InpSupColor)
        if curLeftRes != nullPoint and curRightRes != nullPoint:
            drawLine('Current_Resistance', curRightRes, curLeftRes, InpResColor)
    return rates_total

def isLowestLow(bar, side, Low):
    for i in range(1, side + 1):
        if Low[bar] > Low[bar - i] or Low[bar] > Low[bar + i]:
            return False
    return True

def isHighestHigh(bar, side, High):
    for i in range(1, side + 1):
        if High[bar] < High[bar - i] or High[bar] < High[bar + i]:
            return False
    return True

def drawLine(name, right, left, clr):
    name = InstanceName + '-' + name
    ObjectDelete(0, name)
    ObjectCreate(0, name, OBJ_TREND, 0, right.getTime(), right.getPrice(), left.getTime(), left.getPrice())
    ObjectSetInteger(0, name, OBJPROP_WIDTH, InpLinesWidth)
    ObjectSetInteger(0, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(0, name, OBJPROP_RAY_LEFT, True)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, True)

# ---- global variables initialised from expressions
curLeftSup = _alloc(CPoint)
curLeftSup.__init__()
curRightSup = _alloc(CPoint)
curRightSup.__init__()
curLeftRes = _alloc(CPoint)
curLeftRes.__init__()
curRightRes = _alloc(CPoint)
curRightRes.__init__()
nullPoint = _alloc(CPoint)
nullPoint.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AutoTrendLine(_MQL5Indicator):
    name = 'Auto TrendLine'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpLineType': _Choice({0: '1: By 2 extremums', 1: '2: Extremum and delta'}, default=1),  # Line type
        'InpLeftExmSide': 20,  # Left extremum side (Type 1, 2)
        'InpRightExmSide': 3,  # Right extremum side (Type 1)
        'InpFromCurrent': 3,  # Offset from the current bar� (Type 2)
        'InpPrevExmBar': False,  # Account for the bar before the extremum (Type 2)
        'InpLinesWidth': 1,  # lines width
    }

