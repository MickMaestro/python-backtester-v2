"""linebreakonchart — converted from MQL5: MQL5 Indicators/LineBreakOnChart/linebreakonchart.mq5

Indicator of three-linear reversal on the main chart
Copyright: Copyright 2012, Rone.; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Unresolved names: operator
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, Rone.', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 0}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Series'}, 'levels': [], 'description': ['Indicator of three-linear reversal on the main chart'], 'name': 'linebreakonchart', 'source': 'MQL5 Indicators/LineBreakOnChart/linebreakonchart.mq5', 'folder': 'LineBreakOnChart', 'inputs': [{'mql': 'InpStartDate', 'py': 'InpStartDate', 'param': None, 'type': 'datetime', 'default': 1262304000, 'label': 'Date of calculation start', 'sinput': False}, {'mql': 'InpLines', 'py': 'InpLines', 'param': 'InpLines', 'type': 'int', 'default': 3, 'label': 'Number of reversal lines', 'sinput': False}, {'mql': 'InpMinBoxSize', 'py': 'InpMinBoxSize', 'param': 'InpMinBoxSize', 'type': 'int', 'default': 0, 'label': 'Min. box size', 'sinput': False}, {'mql': 'InpUpColor', 'py': 'InpUpColor', 'param': None, 'type': 'color', 'default': 11829830, 'label': 'Up-boxes color', 'sinput': False}, {'mql': 'InpDnColor', 'py': 'InpDnColor', 'param': None, 'type': 'color', 'default': 6053069, 'label': 'Down-boxes color', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpStartDate = _input('InpStartDate', 1262304000)  # Date of calculation start
InpLines = _input('InpLines', 3)  # Number of reversal lines
InpMinBoxSize = _input('InpMinBoxSize', 0)  # Min. box size
InpUpColor = _input('InpUpColor', clrSteelBlue)  # Up-boxes color
InpDnColor = _input('InpDnColor', clrIndianRed)  # Down-boxes color
SeriesBuffer = Arr(0, 0.0)
minBoxSize = 0.0
linesPrices = Arr(0, 0.0)
seriesData = Arr(0, 0)
startDate = 0
lines = 0

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
    def setPrice(self, p):
        self.price = p
    def setTime(self, t):
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
    global lines, minBoxSize, startDate
    startDate = InpStartDate
    if startDate < 978307200:
        startDate = 978307200
        Print('Incorrect date parameter. The indicator wil be calculated since ', startDate)
    lines = InpLines
    if lines < 1:
        lines = 3
        Print('Incorrect parameter of the reversal lines number. The indicator will be calculated with a value of  ', lines)
    if InpMinBoxSize < 0:
        minBoxSize = 0.0
        Print('Incorrect  parameter of the minimal box size. The indicator will be calculated with a value of  ', minBoxSize)
    else:
        minBoxSize = InpMinBoxSize * Point()
    SetIndexBuffer(0, SeriesBuffer, INDICATOR_DATA)
    ObjectsDeleteAll(0, 0, OBJ_RECTANGLE)
    ArrayResize(linesPrices, lines + 1)
    return 0

def OnDeinit(reason):
    ObjectsDeleteAll(0, 0, OBJ_RECTANGLE)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global curLeftPoint
    startBar = 0
    lastBar = 0
    objColor = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        startBar = rates_total - iBarShift_u(startDate)
        for bar in range(0, startBar):
            SeriesBuffer[bar] = 0.0
        for i in range(1, lines + 1):
            linesPrices[i] = close[startBar - 1]
        linesPrices[0] = close[startBar]
    else:
        startBar = prev_calculated - 1
    lastBar = rates_total - 1
    for bar in range(startBar, lastBar):
        prevBar = bar - 1
        seriesValue = _setitem(SeriesBuffer, bar, SeriesBuffer[prevBar])
        if seriesValue > 0.0:
            objColor = InpUpColor
            if close[bar] > (linesPrices[0] + minBoxSize):
                trendContinue(close[bar], time[bar], leftPoint, rightPoint)
                addNewLineToArray(close[bar])
                SeriesBuffer[bar] += 1
            elif close[bar] < linesPrices[lines]:
                trendReverse(close[bar], time[bar], leftPoint, rightPoint)
                objColor = InpDnColor
                SeriesBuffer[bar] = -1.0
            else:
                rightPoint.setTime(time[bar])
        elif seriesValue < 0.0:
            objColor = InpDnColor
            if close[bar] < (linesPrices[0] - minBoxSize):
                trendContinue(close[bar], time[bar], leftPoint, rightPoint)
                addNewLineToArray(close[bar])
                SeriesBuffer[bar] -= 1
            elif close[bar] > linesPrices[lines]:
                trendReverse(close[bar], time[bar], leftPoint, rightPoint)
                objColor = InpUpColor
                SeriesBuffer[bar] = 1.0
            else:
                rightPoint.setTime(time[bar])
        else:
            if close[bar] >= close[prevBar]:
                objColor = InpUpColor
                SeriesBuffer[bar] = 1.0
            else:
                objColor = InpDnColor
                SeriesBuffer[bar] = -1.0
            addNewLineToArray(close[bar])
            leftPoint.setPoint(close[prevBar], time[prevBar])
            rightPoint.setPoint(close[bar], time[bar])
        drawRectangle(TimeToString(leftPoint.getTime()), leftPoint, rightPoint, objColor)
    seriesValue = _setitem(SeriesBuffer, lastBar, SeriesBuffer[lastBar - 1])
    lastPrice = close[lastBar]
    if seriesValue > 0.0:
        objColor = InpUpColor
        if lastPrice > (linesPrices[0] + minBoxSize):
            _assign(curLeftPoint, rightPoint)
            curRightPoint.setPoint(lastPrice, time[lastBar])
            SeriesBuffer[lastBar] = SeriesBuffer[lastBar] + 1
        elif lastPrice < linesPrices[lines]:
            curLeftPoint.setPoint(leftPoint.getPrice(), rightPoint.getTime())
            curRightPoint.setPoint(lastPrice, time[lastBar])
            objColor = InpDnColor
            SeriesBuffer[lastBar] = -1.0
        else:
            curLeftPoint.setPoint(leftPoint.getPrice(), rightPoint.getTime())
            curRightPoint.setPoint(rightPoint.getPrice(), time[lastBar])
    else:
        objColor = InpDnColor
        if lastPrice < (linesPrices[0] - minBoxSize):
            _assign(curLeftPoint, rightPoint)
            curRightPoint.setPoint(lastPrice, time[lastBar])
            SeriesBuffer[lastBar] = SeriesBuffer[lastBar] - 1
        elif lastPrice > linesPrices[lines]:
            curLeftPoint.setPoint(leftPoint.getPrice(), rightPoint.getTime())
            curRightPoint.setPoint(lastPrice, time[lastBar])
            objColor = InpUpColor
            SeriesBuffer[lastBar] = 1.0
        else:
            curLeftPoint.setPoint(leftPoint.getPrice(), rightPoint.getTime())
            curRightPoint.setPoint(rightPoint.getPrice(), time[lastBar])
    drawRectangle('Current', curLeftPoint, curRightPoint, objColor)
    ChartRedraw()
    return rates_total

def iBarShift_u(startTime):
    if startTime < 0:
        return -1
    array = Arr(0, 0)
    curTime = 0
    CopyTime(Symbol(), Period(), 0, 1, array)
    curTime = array[0]
    if CopyTime(Symbol(), Period(), _DT(startTime), _DT(curTime), array) > 0:
        if ArraySize(array) > 2:
            return ArraySize(array)
    return -1

def addNewLineToArray(price):
    for i in range(lines, 1 - 1, -1):
        linesPrices[i] = linesPrices[i - 1]
    linesPrices[0] = price

def drawRectangle(name, left, right, clr):
    ObjectDelete(0, name)
    ObjectCreate(0, name, OBJ_RECTANGLE, 0, right.getTime(), right.getPrice(), left.getTime(), left.getPrice())
    ObjectSetInteger(0, name, OBJPROP_BACK, True)
    ObjectSetInteger(0, name, OBJPROP_FILL, True)
    ObjectSetInteger(0, name, OBJPROP_COLOR, clr)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, True)

def trendContinue(price, time, left, right):
    _assign(left, right)
    right.setPoint(price, time)

def trendReverse(price, time, left, right):
    left.setTime(right.getTime())
    right.setPoint(price, time)
    for i in range(1, lines + 1):
        linesPrices[i] = linesPrices[0]
    addNewLineToArray(price)

# ---- global variables initialised from expressions
leftPoint = _alloc(CPoint)
leftPoint.__init__()
rightPoint = _alloc(CPoint)
rightPoint.__init__()
prevLeftPoint = _alloc(CPoint)
prevLeftPoint.__init__()
prevRightPoint = _alloc(CPoint)
prevRightPoint.__init__()
curLeftPoint = _alloc(CPoint)
curLeftPoint.__init__()
curRightPoint = _alloc(CPoint)
curRightPoint.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Linebreakonchart(_MQL5Indicator):
    name = 'linebreakonchart'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpLines': 3,  # Number of reversal lines
        'InpMinBoxSize': 0,  # Min. box size
    }

