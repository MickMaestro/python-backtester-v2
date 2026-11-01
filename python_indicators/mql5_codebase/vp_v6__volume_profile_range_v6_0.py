"""VP-v6 — converted from MQL5: MQL5 Indicators/Volume Profile + Range v6.0/VP-v6.mq5

Copyright: VP: Volume Profile v6.0. © FXcoder; Link: http://fxcoder.blogspot.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'VP: Volume Profile v6.0. © FXcoder', 'link': 'http://fxcoder.blogspot.com', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'VP-v6', 'source': 'MQL5 Indicators/Volume Profile + Range v6.0/VP-v6.mq5', 'folder': 'Volume Profile + Range v6.0', 'inputs': [{'mql': 'RangePeriod', 'py': 'RangePeriod', 'param': 'RangePeriod', 'type': 'int', 'default': 16408, 'label': 'Range period', 'sinput': False}, {'mql': 'RangeCount', 'py': 'RangeCount', 'param': 'RangeCount', 'type': 'int', 'default': 20, 'label': 'Range count', 'sinput': False}, {'mql': 'TimeShift', 'py': 'TimeShift', 'param': 'TimeShift', 'type': 'int', 'default': 0, 'label': 'Time shift', 'sinput': False}, {'mql': 'ModeStep', 'py': 'ModeStep', 'param': 'ModeStep', 'type': 'int', 'default': 100, 'label': 'Mode step (points)', 'sinput': False}, {'mql': 'HgPointScale', 'py': 'HgPointScale', 'param': 'HgPointScale', 'type': 'int', 'default': 10, 'label': 'Point scale', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'Volume type', 'sinput': False}, {'mql': 'DataSource', 'py': 'DataSource', 'param': 'DataSource', 'type': 'int', 'default': 1, 'label': 'Data source', 'sinput': False}, {'mql': 'HgBarStyle', 'py': 'HgBarStyle', 'param': 'HgBarStyle', 'type': 'int', 'default': 0, 'label': 'Bar style', 'sinput': False}, {'mql': 'DrawDirection', 'py': 'DrawDirection', 'param': 'DrawDirection', 'type': 'int', 'default': 1, 'label': 'Draw direction', 'sinput': False}, {'mql': 'HgColor', 'py': 'HgColor', 'param': None, 'type': 'color', 'default': 12624000, 'label': 'Color 1', 'sinput': False}, {'mql': 'HgColor2', 'py': 'HgColor2', 'param': None, 'type': 'color', 'default': 12624000, 'label': 'Color 2', 'sinput': False}, {'mql': 'HgLineWidth', 'py': 'HgLineWidth', 'param': 'HgLineWidth', 'type': 'int', 'default': 1, 'label': 'Line width', 'sinput': False}, {'mql': 'ModeColor', 'py': 'ModeColor', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Mode color', 'sinput': False}, {'mql': 'MaxColor', 'py': 'MaxColor', 'param': None, 'type': 'color', 'default': 4294967295, 'label': 'Maximum color', 'sinput': False}, {'mql': 'MedianColor', 'py': 'MedianColor', 'param': None, 'type': 'color', 'default': 4294967295, 'label': 'Median color', 'sinput': False}, {'mql': 'VwapColor', 'py': 'VwapColor', 'param': None, 'type': 'color', 'default': 4294967295, 'label': 'VWAP color', 'sinput': False}, {'mql': 'ModeLineWidth', 'py': 'ModeLineWidth', 'param': 'ModeLineWidth', 'type': 'int', 'default': 1, 'label': 'Mode line width', 'sinput': False}, {'mql': 'StatLineStyle', 'py': 'StatLineStyle', 'param': 'StatLineStyle', 'type': 'int', 'default': 2, 'label': 'Median & VWAP line style', 'sinput': False}, {'mql': 'Id', 'py': 'Id', 'param': None, 'type': 'string', 'default': '+vp', 'label': 'Identifier', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

COPY_TICKS_INFO = 0  # MQL5 constant unknown to the converter
COPY_TICKS_TRADE = 0  # MQL5 constant unknown to the converter
Red = 0x0000FF  # MQL4 colour name

# enum ENUM_POINT_SCALE
POINT_SCALE_1 = 1
POINT_SCALE_10 = 10
POINT_SCALE_100 = 100
_enum('ENUM_POINT_SCALE', {1: 'POINT_SCALE_1', 10: 'POINT_SCALE_10', 100: 'POINT_SCALE_100'})

# enum ENUM_VP_BAR_STYLE
VP_BAR_STYLE_LINE = 0
VP_BAR_STYLE_BAR = 1
VP_BAR_STYLE_FILLED = 2
VP_BAR_STYLE_OUTLINE = 3
VP_BAR_STYLE_COLOR = 4
_enum('ENUM_VP_BAR_STYLE', {0: 'VP_BAR_STYLE_LINE', 1: 'VP_BAR_STYLE_BAR', 2: 'VP_BAR_STYLE_FILLED', 3: 'VP_BAR_STYLE_OUTLINE', 4: 'VP_BAR_STYLE_COLOR'})

# enum ENUM_HG_DIRECTION
HG_DIRECTION_LEFT = 0
HG_DIRECTION_RIGHT = 1
_enum('ENUM_HG_DIRECTION', {0: 'HG_DIRECTION_LEFT', 1: 'HG_DIRECTION_RIGHT'})

# enum ENUM_VP_SOURCE
VP_SOURCE_TICKS = 0
VP_SOURCE_M1 = 1
VP_SOURCE_M5 = 5
VP_SOURCE_M15 = 15
VP_SOURCE_M30 = 30
_enum('ENUM_VP_SOURCE', {0: 'VP_SOURCE_TICKS', 1: 'VP_SOURCE_M1', 5: 'VP_SOURCE_M5', 15: 'VP_SOURCE_M15', 30: 'VP_SOURCE_M30'})

# enum ENUM_TIME_SHIFT
TIME_SHIFT_PLUS_720 = 720
TIME_SHIFT_PLUS_660 = 660
TIME_SHIFT_PLUS_600 = 600
TIME_SHIFT_PLUS_540 = 540
TIME_SHIFT_PLUS_480 = 480
TIME_SHIFT_PLUS_420 = 420
TIME_SHIFT_PLUS_360 = 360
TIME_SHIFT_PLUS_300 = 300
TIME_SHIFT_PLUS_240 = 240
TIME_SHIFT_PLUS_180 = 180
TIME_SHIFT_PLUS_120 = 120
TIME_SHIFT_PLUS_60 = 60
TIME_SHIFT_0 = 0
TIME_SHIFT_MINUS_60 = -60
TIME_SHIFT_MINUS_120 = -120
TIME_SHIFT_MINUS_180 = -180
TIME_SHIFT_MINUS_240 = -240
TIME_SHIFT_MINUS_300 = -300
TIME_SHIFT_MINUS_360 = -360
TIME_SHIFT_MINUS_420 = -420
TIME_SHIFT_MINUS_480 = -480
TIME_SHIFT_MINUS_540 = -540
TIME_SHIFT_MINUS_600 = -600
TIME_SHIFT_MINUS_660 = -660
TIME_SHIFT_MINUS_720 = -720
_enum('ENUM_TIME_SHIFT', {720: 'TIME_SHIFT_PLUS_720', 660: 'TIME_SHIFT_PLUS_660', 600: 'TIME_SHIFT_PLUS_600', 540: 'TIME_SHIFT_PLUS_540', 480: 'TIME_SHIFT_PLUS_480', 420: 'TIME_SHIFT_PLUS_420', 360: 'TIME_SHIFT_PLUS_360', 300: 'TIME_SHIFT_PLUS_300', 240: 'TIME_SHIFT_PLUS_240', 180: 'TIME_SHIFT_PLUS_180', 120: 'TIME_SHIFT_PLUS_120', 60: 'TIME_SHIFT_PLUS_60', 0: 'TIME_SHIFT_0', -60: 'TIME_SHIFT_MINUS_60', -120: 'TIME_SHIFT_MINUS_120', -180: 'TIME_SHIFT_MINUS_180', -240: 'TIME_SHIFT_MINUS_240', -300: 'TIME_SHIFT_MINUS_300', -360: 'TIME_SHIFT_MINUS_360', -420: 'TIME_SHIFT_MINUS_420', -480: 'TIME_SHIFT_MINUS_480', -540: 'TIME_SHIFT_MINUS_540', -600: 'TIME_SHIFT_MINUS_600', -660: 'TIME_SHIFT_MINUS_660', -720: 'TIME_SHIFT_MINUS_720'})

# ---- inputs and global variables
RangePeriod = _input('RangePeriod', PERIOD_D1)  # Range period
RangeCount = _input('RangeCount', 20)  # Range count
TimeShift = _input('TimeShift', TIME_SHIFT_0)  # Time shift
ModeStep = _input('ModeStep', 100)  # Mode step (points)
HgPointScale = _input('HgPointScale', POINT_SCALE_10)  # Point scale
VolumeType = _input('VolumeType', VOLUME_TICK)  # Volume type
DataSource = _input('DataSource', VP_SOURCE_M1)  # Data source
HgBarStyle = _input('HgBarStyle', VP_BAR_STYLE_LINE)  # Bar style
DrawDirection = _input('DrawDirection', HG_DIRECTION_RIGHT)  # Draw direction
HgColor = _input('HgColor', 0xC0A080)  # Color 1
HgColor2 = _input('HgColor2', 0xC0A080)  # Color 2
HgLineWidth = _input('HgLineWidth', 1)  # Line width
ModeColor = _input('ModeColor', clrBlue)  # Mode color
MaxColor = _input('MaxColor', clrNONE)  # Maximum color
MedianColor = _input('MedianColor', clrNONE)  # Median color
VwapColor = _input('VwapColor', clrNONE)  # VWAP color
ModeLineWidth = _input('ModeLineWidth', 1)  # Mode line width
StatLineStyle = _input('StatLineStyle', STYLE_DOT)  # Median & VWAP line style
Id = _input('Id', '+vp')  # Identifier
ShowHorizon = True  # Show data horizon
Zoom = 0.0  # Zoom (0=auto)
WaitMilliseconds = 1000  # Wait milliseconds
RangeLength = 0  # Range length (0=Range period) // не реализовано
_prefix = ""
_tfn = ""
_ttn = ""
_drawHistory = Arr(0, 0)
_lastOK = False
_modeStep = 0
_prevBackgroundColor = clrNONE
_rangeCount = 0
_hgBarStyle = 0
_hgPoint = 0.0
_hgPointDigits = 0
_defaultHgColor1 = 0
_defaultHgColor2 = 0
_hgColor1 = 0
_hgColor2 = 0
_hgLineWidth = 0
_modeColor = 0
_maxColor = 0
_medianColor = 0
_vwapColor = 0
_modeLineWidth = 0
_statLineStyle = 0
_modeLevelColor = 0
_modeLevelStyle = 0
_modeLevelWidth = 0
_showHg = False
_showModes = False
_showMax = False
_showMedian = False
_showVwap = False
_showModeLevel = False
_zoom = 0.0
_firstVisibleBar = 0
_lastVisibleBar = 0
_updateTimer = None
_isTimeframeEnabled = False
_timeShiftSeconds = 0
_dataPeriod = 0

class MillisecondTimer(MqlObject):
    _q_fields = ('_milliseconds', '_lastTick')
    def __init__(self, *args):
        self._milliseconds = 0
        self._lastTick = 0
    def MillisecondTimer(self, milliseconds, reset=True):
        self._milliseconds = milliseconds
        if reset:
            self.Reset()
        else:
            self._lastTick = 0
    def Check(self):
        now = self.getCurrentTick()
        stop = now >= (self._lastTick + self._milliseconds)
        if stop:
            self._lastTick = now
        return stop
    def Reset(self):
        self._lastTick = self.getCurrentTick()
    def getCurrentTick(self):
        return GetTickCount()

def OnInit():
    global _dataPeriod, _defaultHgColor1, _defaultHgColor2, _hgBarStyle, _hgLineWidth, _hgPoint, _hgPointDigits, _maxColor, _medianColor, _modeColor, _modeLineWidth, _modeStep, _prefix, _rangeCount, _showHg, _showMax, _showMedian, _showModes, _showVwap, _statLineStyle, _timeShiftSeconds, _updateTimer, _vwapColor, _zoom
    _prefix = Id + ' ' + IntegerToString(RangePeriod) + ' '
    _rangeCount = (RangeCount if (RangeCount > 0) else 1)
    _hgPoint = Point() * HgPointScale
    _modeStep = _idiv(ModeStep, HgPointScale)
    ArrayFree(_drawHistory)
    _hgBarStyle = HgBarStyle
    _hgPointDigits = GetPointDigits_1(_hgPoint)
    _defaultHgColor1 = HgColor
    _defaultHgColor2 = HgColor2
    _hgLineWidth = HgLineWidth
    _modeColor = ModeColor
    _maxColor = MaxColor
    _medianColor = MedianColor
    _vwapColor = VwapColor
    _modeLineWidth = ModeLineWidth
    _statLineStyle = StatLineStyle
    _showHg = not (ColorIsNone(_hgColor1) and ColorIsNone(_hgColor2))
    _showModes = not ColorIsNone(_modeColor)
    _showMax = not ColorIsNone(_maxColor)
    _showMedian = not ColorIsNone(_medianColor)
    _showVwap = not ColorIsNone(_vwapColor)
    _zoom = MathAbs(Zoom)
    _updateTimer = MillisecondTimer(WaitMilliseconds, False)
    _timeShiftSeconds = _imod(TimeShift * 60, PeriodSeconds(RangePeriod))
    if _timeShiftSeconds < 0:
        _timeShiftSeconds += PeriodSeconds(RangePeriod)
    _dataPeriod = GetDataPeriod(DataSource)

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ == CHARTEVENT_CHART_CHANGE:
        if UpdateAutoColors():
            ArrayFree(_drawHistory)
            CheckTimer()

def OnCalculate(ratesTotal, prevCalculated, time, open, high, low, close, tickVolume, volume, spread):
    if UpdateAutoColors():
        ArrayFree(_drawHistory)
    CheckTimer()
    return 0

def OnTimer():
    CheckTimer()

def OnDeinit(reason):
    ObjectsDeleteAll(0, _prefix)
    _delete(_updateTimer)

def CheckTimer():
    global _lastOK
    EventKillTimer()
    if _updateTimer.Check() or (not _lastOK):
        _lastOK = Update()
        if not _lastOK:
            EventSetTimer(3)
        ChartRedraw()
        _updateTimer.Reset()
    else:
        EventSetTimer(3)

def Update():
    ranges = Arr(0, 0)
    ArraySetAsSeries(ranges, True)
    ArrayResize(ranges, _rangeCount)
    if CopyTime(Symbol(), RangePeriod, 0, _rangeCount, ranges) != _rangeCount:
        return False
    if RangePeriod == PERIOD_W1:
        for i in range(0, _rangeCount):
            ranges[i] += 1440 * 60
    rangeLengthSeconds = (PeriodSeconds(RangePeriod) if (RangeLength == 0) else (_int(RangeLength) * 60))
    dataRates = Arr(0, 0)
    rangesStart = ranges[_rangeCount - 1] + _timeShiftSeconds
    rangesEnd = ranges[0] + rangeLengthSeconds - 1 + _timeShiftSeconds
    if CopyTime(Symbol(), _dataPeriod, _DT(rangesStart), _DT(rangesEnd), dataRates) <= 0:
        return False
    tick = MqlTick()
    if not SymbolInfoTick(Symbol(), tick):
        return False
    lastTickTime = tick.time
    if ShowHorizon:
        horizon = GetHorizon(DataSource, _dataPeriod)
        DrawHorizon(_prefix + 'hz', horizon)
    modes = Arr(0, 0)
    volumes = Arr(0, 0.0)
    lowPrice = Box(0.0)
    totalResult = True
    i = 0
    while i < _rangeCount:
        rangeStart = ranges[i] + _timeShiftSeconds
        if TimeDayOfWeek_u(rangeStart) == SUNDAY:
            rangeStart -= 2 * 1440 * 60
        if i != 0 and ArrayIndexOf(_drawHistory, rangeStart) != -1:
            i += 1
            continue
        rangeEnd = 0
        if i == 0:
            rangeEnd = ranges[i] + _timeShiftSeconds + rangeLengthSeconds - 1
        else:
            rangeEnd = ranges[i - 1] + _timeShiftSeconds - 1
            if TimeDayOfWeek_u(rangeEnd) == SUNDAY:
                rangeEnd -= 2 * 1440 * 60
        barFrom = Box(0)
        barTo = Box(0)
        if not GetRangeBars(rangeStart, rangeEnd, barFrom, barTo):
            totalResult = False
            i += 1
            continue
        count = 0
        if DataSource == VP_SOURCE_TICKS:
            count = GetHgByTicks(rangeStart, rangeEnd, _hgPoint, _dataPeriod, VolumeType, lowPrice, volumes)
        else:
            count = GetHg(rangeStart, rangeEnd, _hgPoint, _dataPeriod, VolumeType, lowPrice, volumes)
        if count <= 0:
            totalResult = False
            i += 1
            continue
        if rangeEnd < lastTickTime:
            ArrayAdd(_drawHistory, rangeStart, True)
        modeCount = (HgModes(volumes, _modeStep, modes) if _showModes else -1)
        maxPos = (ArrayMax(volumes) if _showMax else -1)
        medianPos = (ArrayMedian(volumes) if _showMedian else -1)
        vwapPos = (HgVwap(volumes, lowPrice.v, _hgPoint) if _showVwap else -1)
        prefix = _prefix + _str(_idiv(_int(rangeStart), PeriodSeconds(RangePeriod))) + ' '
        maxVolume = volumes[ArrayMaximum(volumes)]
        if maxVolume == 0:
            maxVolume = 1.0
        zoom = (_zoom if (_zoom > 0) else _fdiv(barFrom.v - barTo.v, maxVolume))
        if DrawDirection == HG_DIRECTION_LEFT:
            Swap(barFrom, barTo)
        ObjectsDeleteAll(0, prefix)
        DrawHg(prefix, lowPrice.v, volumes, barFrom.v, barTo.v, zoom, modes, maxPos, medianPos, vwapPos)
        i += 1
    return totalResult

def TimeDayOfWeek_u(time):
    timeStruct = MqlDateTime()
    TimeToStruct(time, timeStruct)
    return timeStruct.day_of_week

def ArrayIndexOf(arr, value, startingFrom=0):
    size = ArraySize(arr)
    for i in range(startingFrom, size):
        if arr[i] == value:
            return i
    return -1

def ArrayAdd(arr, value, checkUnique=False, reserveSize=100):
    i = 0
    if checkUnique:
        i = ArrayIndexOf(arr, value)
        if i != -1:
            return i
    i = ArrayResize(arr, ArraySize(arr) + 1, reserveSize)
    if i == -1:
        return -1
    i -= 1
    arr[i] = value
    return i

def ArrayCheckRange(arr, start, count):
    size = ArraySize(arr)
    if size <= 0:
        return False
    if count.v == 0:
        return False
    if start.v > (size - 1) or start.v < 0:
        return False
    if count.v < 0:
        count.v = size - start.v
    elif count.v > (size - start.v):
        count.v = size - start.v
    return True

def ArrayMedian(values):
    size = ArraySize(values)
    halfVolume = Sum(values) / 2.0
    v = 0.0
    for i in range(0, size):
        v += values[i]
        if v >= halfVolume:
            return i
    return -1

def TrimRight(s, ch):
    len_ = StringLen(s)
    cut = len_
    for i in range(len_ - 1, 0 - 1, -1):
        if StringGetCharacter(s, i) == ch:
            cut -= 1
        else:
            break
    if cut != len_:
        if cut == 0:
            s = ''
        else:
            s = StringSubstr(s, 0, cut)
    return s

def DoubleToString_u(d, digits, separator):
    s = Box(DoubleToString(d, digits) + '')
    if separator != 46:
        p = StringFind(s.v, '.')
        if p != -1:
            StringSetCharacter(s, p, separator)
    return s.v

def DoubleToCompactString(d, digits=8, separator=46):
    s = DoubleToString_u(d, digits, separator)
    if StringFind(s, CharToString(separator)) != -1:
        s = TrimRight(s, 48)
        s = TrimRight(s, 46)
    return s

def MathRound_u(value, error):
    return (value if (error == 0) else (MathRound(_fdiv(value, error)) * error))

def Swap(value1, value2):
    tmp = value1.v
    value1.v = value2.v
    value2.v = tmp

def Sum(arr, start=0, count=-1):
    start = Box(start)
    count = Box(count)
    if not ArrayCheckRange(arr, start, count):
        return None
    sum_ = None
    i = start.v
    end = start.v + count.v
    while i < end:
        sum_ += arr[i]
        i += 1
    return sum_

def GetPointDigits_1(point):
    if point == 0:
        return Digits()
    return GetPointDigits_2(point, Digits())

def GetPointDigits_2(point, maxDigits):
    if point == 0:
        return maxDigits
    pointString = DoubleToCompactString(point, maxDigits)
    pointStringLen = StringLen(pointString)
    dotPos = StringFind(pointString, '.')
    return ((StringLen(TrimRight(pointString, 48)) - pointStringLen) if (dotPos < 0) else (pointStringLen - dotPos - 1))

def ArrayMax(array, start=0, count=WHOLE_ARRAY):
    return ArrayMaximum(array, start, count)

def HgModes(values, modeStep, modes):
    modeCount = 0
    ArrayFree(modes)
    i = modeStep
    count = ArraySize(values) - modeStep
    while i < count:
        maxFrom = i - modeStep
        maxRange = (2 * modeStep) + 1
        maxTo = maxFrom + maxRange - 1
        k = ArrayMax(values, maxFrom, maxRange)
        if k != i:
            i += 1
            continue
        for j in range(i - modeStep, i + modeStep + 1):
            if values[j] != values[k]:
                continue
            modeCount += 1
            ArrayResize(modes, modeCount, count)
            modes[modeCount - 1] = j
        i += 1
    return modeCount

def HgVwap(volumes, low, step):
    if step == 0:
        return -1
    vwap = 0.0
    totalVolume = 0.0
    size = ArraySize(volumes)
    for i in range(0, size):
        price = low + (i * step)
        volume = volumes[i]
        vwap += price * volume
        totalVolume += volume
    if totalVolume == 0:
        return -1
    vwap = _fdiv(vwap, totalVolume)
    return _int(_fdiv(vwap - low, step) + 0.5)

def iBarShift_u(symbol, timeframe, time, exact=False):
    if time < 0:
        return -1
    arr = Arr(0, 0)
    time1 = 0
    CopyTime(symbol, timeframe, 0, 1, arr)
    time1 = arr[0]
    if CopyTime(symbol, timeframe, _DT(time), _DT(time1), arr) <= 0:
        return -1
    if ArraySize(arr) > 2:
        return ArraySize(arr) - 1
    return (1 if (time < time1) else 0)

def iTime_u(symbol, timeframe, index):
    if index < 0:
        return -1
    arr = Arr(0, 0)
    if CopyTime(symbol, timeframe, index, 1, arr) <= 0:
        return -1
    return arr[0]

def GetHgByTicks(timeFrom, timeTo, point, dataPeriod, appliedVolume, low, volumes):
    tickVolumes = Arr(0, 0)
    tickVolumeCount = CopyTickVolume(Symbol(), dataPeriod, _DT(timeFrom), _DT(timeTo), tickVolumes)
    if tickVolumeCount <= 0:
        return 0
    tickVolumesTotal = _long(Sum(tickVolumes))
    ticks = Arr(0, 0, factory=MqlTick)
    tickCount = CopyTicks(Symbol(), ticks, COPY_TICKS_TRADE, timeFrom * 1000, _uint(tickVolumesTotal))
    if tickCount <= 0:
        return 0
    tick = _copy(ticks[0])
    low.v = _int(_fdiv(tick.last, point) + 0.5) * point
    high = low.v
    timeToMs = timeTo * 1000
    i = 1
    while i < tickCount:
        _assign(tick, ticks[i])
        if tick.time_msc > timeToMs:
            tickCount = i
            break
        tickLast = _int(_fdiv(tick.last, point) + 0.5) * point
        if tickLast < low.v:
            low.v = tickLast
        if tickLast > high:
            high = tickLast
        i += 1
    lowIndex = _int(_fdiv(low.v, point) + 0.5)
    highIndex = _int(_fdiv(high, point) + 0.5)
    hgSize = highIndex - lowIndex + 1
    ArrayResize(volumes, hgSize)
    ArrayInitialize(volumes, 0)
    pri = 0
    for j in range(0, tickCount):
        _assign(tick, ticks[j])
        pri = _int(_fdiv(tick.last, point) + 0.5) - lowIndex
        volumes[pri] += (float(tick.volume) if (appliedVolume == VOLUME_REAL) else 1)
    return hgSize

def GetHg(timeFrom, timeTo, point, dataPeriod, appliedVolume, low, volumes):
    rates = Arr(0, 0, factory=MqlRates)
    rateCount = CopyRates(Symbol(), dataPeriod, _DT(timeFrom), _DT(timeTo), rates)
    if rateCount <= 0:
        return 0
    rate = _copy(rates[0])
    low.v = _int(_fdiv(rate.low, point) + 0.5) * point
    high = _int(_fdiv(rate.high, point) + 0.5) * point
    for i in range(1, rateCount):
        _assign(rate, rates[i])
        rateHigh = _int(_fdiv(rate.high, point) + 0.5) * point
        rateLow = _int(_fdiv(rate.low, point) + 0.5) * point
        if rateLow < low.v:
            low.v = rateLow
        if rateHigh > high:
            high = rateHigh
    lowIndex = _int(_fdiv(low.v, point) + 0.5)
    highIndex = _int(_fdiv(high, point) + 0.5)
    hgSize = highIndex - lowIndex + 1
    ArrayResize(volumes, hgSize)
    ArrayInitialize(volumes, 0)
    pri = 0
    oi = 0
    hi = 0
    li = 0
    ci = 0
    dv = 0.0
    v = 0.0
    for j in range(0, rateCount):
        _assign(rate, rates[j])
        oi = _int(_fdiv(rate.open, point) + 0.5) - lowIndex
        hi = _int(_fdiv(rate.high, point) + 0.5) - lowIndex
        li = _int(_fdiv(rate.low, point) + 0.5) - lowIndex
        ci = _int(_fdiv(rate.close, point) + 0.5) - lowIndex
        v = (float(rate.real_volume) if (appliedVolume == VOLUME_REAL) else float(rate.tick_volume))
        if ci >= oi:
            dv = _fdiv(v, oi - li + hi - li + hi - ci + 1.0)
            pri = oi
            for pri in range(pri, li - 1, -1):
                volumes[pri] += dv
            else:
                pri = _range_end(pri, li - 1, -1)
            pri = li + 1
            for pri in range(pri, hi + 1):
                volumes[pri] += dv
            else:
                pri = _range_end(pri, hi + 1, 1)
            pri = hi - 1
            for pri in range(pri, ci - 1, -1):
                volumes[pri] += dv
            else:
                pri = _range_end(pri, ci - 1, -1)
        else:
            dv = _fdiv(v, hi - oi + hi - li + ci - li + 1.0)
            pri = oi
            for pri in range(pri, hi + 1):
                volumes[pri] += dv
            else:
                pri = _range_end(pri, hi + 1, 1)
            pri = hi - 1
            for pri in range(pri, li - 1, -1):
                volumes[pri] += dv
            else:
                pri = _range_end(pri, li - 1, -1)
            pri = li + 1
            for pri in range(pri, ci + 1):
                volumes[pri] += dv
            else:
                pri = _range_end(pri, ci + 1, 1)
    return hgSize

def GetHorizon(dataSource, dataPeriod):
    if dataSource == VP_SOURCE_TICKS:
        ticks = Arr(0, 0, factory=MqlTick)
        tickCount = CopyTicks(Symbol(), ticks, COPY_TICKS_INFO, 1, 1)
        if tickCount <= 0:
            return SymbolInfoInteger(Symbol(), SYMBOL_TIME) + 1
        return ticks[0].time
    return iTime_u(Symbol(), dataPeriod, Bars(Symbol(), dataPeriod) - 1)

def GetDataPeriod(dataSource):
    _sw1 = dataSource
    if _sw1 == VP_SOURCE_TICKS:
        return PERIOD_M1
    elif _sw1 == VP_SOURCE_M1:
        return PERIOD_M1
    elif _sw1 == VP_SOURCE_M5:
        return PERIOD_M5
    elif _sw1 == VP_SOURCE_M15:
        return PERIOD_M15
    elif _sw1 == VP_SOURCE_M30:
        return PERIOD_M30
    else:
        return PERIOD_M1

def ColorToRGB(c, r, g, b):
    if (c >> 24) != 0:
        return False
    b.v = (c & 0xFF0000) >> 16
    g.v = (c & 0x00FF00) >> 8
    r.v = c & 0x0000FF
    return True

def MixColors(color1, color2, mix, step=16.0):
    step = (step if (255.0 < 1.0) else 1.0 if (step < 1.0) else 255.0 if (step > 255.0) else step)
    mix = (mix if (1.0 < 0.0) else 0.0 if (mix < 0.0) else 1.0 if (mix > 1.0) else mix)
    r1 = Box(0)
    g1 = Box(0)
    b1 = Box(0)
    r2 = Box(0)
    g2 = Box(0)
    b2 = Box(0)
    ColorToRGB(color1, r1, g1, b1)
    ColorToRGB(color2, r2, g2, b2)
    r = (_int(MathRound_u(r1.v + (mix * (r2.v - r1.v)), step)) if (255 < 0) else 0 if (_int(MathRound_u(r1.v + (mix * (r2.v - r1.v)), step)) < 0) else 255 if (_int(MathRound_u(r1.v + (mix * (r2.v - r1.v)), step)) > 255) else _int(MathRound_u(r1.v + (mix * (r2.v - r1.v)), step)))
    g = (_int(MathRound_u(g1.v + (mix * (g2.v - g1.v)), step)) if (255 < 0) else 0 if (_int(MathRound_u(g1.v + (mix * (g2.v - g1.v)), step)) < 0) else 255 if (_int(MathRound_u(g1.v + (mix * (g2.v - g1.v)), step)) > 255) else _int(MathRound_u(g1.v + (mix * (g2.v - g1.v)), step)))
    b = (_int(MathRound_u(b1.v + (mix * (b2.v - b1.v)), step)) if (255 < 0) else 0 if (_int(MathRound_u(b1.v + (mix * (b2.v - b1.v)), step)) < 0) else 255 if (_int(MathRound_u(b1.v + (mix * (b2.v - b1.v)), step)) > 255) else _int(MathRound_u(b1.v + (mix * (b2.v - b1.v)), step)))
    return _uint(_int((b & 0x0000FF) << 16) + _int((g & 0x0000FF) << 8) + (r & 0x0000FF))

def ColorIsNone(c):
    return (c >> 24) != 0

def ObjectDisable(chartId, name):
    ObjectSetInteger(chartId, name, OBJPROP_HIDDEN, True)
    ObjectSetInteger(chartId, name, OBJPROP_SELECTABLE, False)

def GetTimeBarRight(time, period=PERIOD_CURRENT):
    bar = iBarShift_u(Symbol(), period, time)
    t = iTime_u(Symbol(), period, bar)
    if t != time and bar == 0:
        bar = _int(_idiv(iTime_u(Symbol(), period, 0) - time, PeriodSeconds(period)))
    else:
        if t < time:
            bar -= 1
    return bar

def GetBarTime(shift, period=PERIOD_CURRENT):
    if shift >= 0:
        return iTime_u(Symbol(), period, shift)
    else:
        return iTime_u(Symbol(), period, 0) - (shift * PeriodSeconds(period))

def DrawHorizon(lineName, time):
    DrawVLine(lineName, time, _uint(Red), 1, STYLE_DOT, False)
    ObjectDisable(0, lineName)

def DrawVLine(name, time1, lineColor, width, style, back):
    if ObjectFind(0, name) >= 0:
        ObjectDelete(0, name)
    ObjectCreate(0, name, OBJ_VLINE, 0, time1, 0)
    ObjectSetInteger(0, name, OBJPROP_COLOR, lineColor)
    ObjectSetInteger(0, name, OBJPROP_BACK, back)
    ObjectSetInteger(0, name, OBJPROP_STYLE, style)
    ObjectSetInteger(0, name, OBJPROP_WIDTH, width)

def DrawBar(name, time1, time2, price, lineColor, width, barStyle, lineStyle, back):
    ObjectDelete(0, name)
    if barStyle == VP_BAR_STYLE_BAR:
        ObjectCreate(0, name, OBJ_RECTANGLE, 0, time1, price - (_hgPoint / 2.0), time2, price + (_hgPoint / 2.0))
    elif barStyle == VP_BAR_STYLE_FILLED or barStyle == VP_BAR_STYLE_COLOR:
        ObjectCreate(0, name, OBJ_RECTANGLE, 0, time1, price - (_hgPoint / 2.0), time2, price + (_hgPoint / 2.0))
    elif barStyle == VP_BAR_STYLE_OUTLINE:
        ObjectCreate(0, name, OBJ_TREND, 0, time1, price, time2, price + _hgPoint)
    else:
        ObjectCreate(0, name, OBJ_TREND, 0, time1, price, time2, price)
    SetBarStyle(name, lineColor, width, barStyle, lineStyle, back)

def SetBarStyle(name, lineColor, width, barStyle, lineStyle, back):
    ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, name, OBJPROP_COLOR, lineColor)
    ObjectSetInteger(0, name, OBJPROP_STYLE, lineStyle)
    ObjectSetInteger(0, name, OBJPROP_WIDTH, (width if (lineStyle == STYLE_SOLID) else 1))
    ObjectSetInteger(0, name, OBJPROP_RAY_LEFT, False)
    ObjectSetInteger(0, name, OBJPROP_RAY_RIGHT, False)
    ObjectSetInteger(0, name, OBJPROP_BACK, back)
    ObjectSetInteger(0, name, OBJPROP_FILL, barStyle == VP_BAR_STYLE_FILLED or barStyle == VP_BAR_STYLE_COLOR)

def DrawLevel(name, price):
    ObjectDelete(0, name)
    ObjectCreate(0, name, OBJ_HLINE, 0, 0, price)
    ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, name, OBJPROP_COLOR, _modeLevelColor)
    ObjectSetInteger(0, name, OBJPROP_STYLE, _modeLevelStyle)
    ObjectSetInteger(0, name, OBJPROP_WIDTH, (_modeLevelWidth if (_modeLevelStyle == STYLE_SOLID) else 1))
    ObjectSetInteger(0, name, OBJPROP_BACK, False)

def DrawHg(prefix, lowPrice, volumes, barFrom, barTo, zoom, modes, max_=-1, median=-1, vwap=-1):
    if ArraySize(volumes) == 0:
        return
    if barFrom > barTo:
        zoom = -zoom
    cl = _hgColor1
    maxValue = volumes[ArrayMaximum(volumes)]
    if maxValue == 0:
        maxValue = 1.0
    volume = 0.0
    nextVolume = 0.0
    isOutline = _hgBarStyle == VP_BAR_STYLE_OUTLINE
    bar1 = barFrom
    bar2 = barTo
    modeBar2 = barTo
    i = 0
    size = ArraySize(volumes)
    while i < size:
        price = NormalizeDouble(lowPrice + (i * _hgPoint), _hgPointDigits)
        priceString = DoubleToString(price, _hgPointDigits)
        name = prefix + priceString
        volume = volumes[i]
        if isOutline:
            if i < (size - 1):
                nextVolume = volumes[i + 1]
                bar1 = _int(barFrom + (volume * zoom))
                bar2 = _int(barFrom + (nextVolume * zoom))
                modeBar2 = bar1
        elif _hgBarStyle != VP_BAR_STYLE_COLOR:
            bar2 = _int(barFrom + (volume * zoom))
            modeBar2 = bar2
        timeFrom = GetBarTime(barFrom)
        timeTo = GetBarTime(barTo)
        t1 = GetBarTime(bar1)
        t2 = GetBarTime(bar2)
        mt2 = GetBarTime(modeBar2)
        if _showModeLevel and ArrayIndexOf(modes, i) != -1:
            DrawLevel(name + ' level', price)
        if _showHg and (not (isOutline and i == (size - 1))):
            if _hgColor1 != _hgColor2:
                cl = MixColors(_hgColor1, _hgColor2, _fdiv((MathMax(volume, nextVolume) if isOutline else volume), maxValue), 8.0)
            DrawBar(name, t1, t2, price, cl, _hgLineWidth, _hgBarStyle, STYLE_SOLID, True)
        if _showMedian and i == median:
            DrawBar(name + ' median', timeFrom, timeTo, price, _medianColor, _modeLineWidth, VP_BAR_STYLE_LINE, _statLineStyle, False)
        elif _showVwap and i == vwap:
            DrawBar(name + ' vwap', timeFrom, timeTo, price, _vwapColor, _modeLineWidth, VP_BAR_STYLE_LINE, _statLineStyle, False)
        elif (_showMax and i == max_) or (_showModes and ArrayIndexOf(modes, i) != -1):
            modeColor = (_maxColor if (_showMax and i == max_) else _modeColor)
            if _hgBarStyle == VP_BAR_STYLE_LINE:
                DrawBar(name, timeFrom, mt2, price, modeColor, _modeLineWidth, VP_BAR_STYLE_LINE, STYLE_SOLID, False)
            elif _hgBarStyle == VP_BAR_STYLE_BAR:
                DrawBar(name, timeFrom, mt2, price, modeColor, _modeLineWidth, VP_BAR_STYLE_BAR, STYLE_SOLID, False)
            elif _hgBarStyle == VP_BAR_STYLE_FILLED:
                DrawBar(name, timeFrom, mt2, price, modeColor, _modeLineWidth, VP_BAR_STYLE_FILLED, STYLE_SOLID, False)
            elif _hgBarStyle == VP_BAR_STYLE_OUTLINE:
                DrawBar(name + '+', timeFrom, mt2, price, modeColor, _modeLineWidth, VP_BAR_STYLE_LINE, STYLE_SOLID, False)
            elif _hgBarStyle == VP_BAR_STYLE_COLOR:
                DrawBar(name, timeFrom, mt2, price, modeColor, _modeLineWidth, VP_BAR_STYLE_FILLED, STYLE_SOLID, False)
        i += 1

def GetRangeBars(timeFrom, timeTo, barFrom, barTo):
    barFrom.v = GetTimeBarRight(timeFrom)
    barTo.v = GetTimeBarRight(timeTo)
    return True

def UpdateAutoColors():
    global _hgColor1, _hgColor2, _prevBackgroundColor
    if not _showHg:
        return False
    isNone1 = ColorIsNone(_defaultHgColor1)
    isNone2 = ColorIsNone(_defaultHgColor2)
    if isNone1 and isNone2:
        return False
    newBgColor = _uint(ChartGetInteger(0, CHART_COLOR_BACKGROUND))
    if newBgColor == _prevBackgroundColor:
        return False
    _hgColor1 = (newBgColor if isNone1 else _defaultHgColor1)
    _hgColor2 = (newBgColor if isNone2 else _defaultHgColor2)
    _prevBackgroundColor = newBgColor
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VPV6(_MQL5Indicator):
    name = 'VP-v6'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RangePeriod': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Range period
        'RangeCount': 20,  # Range count
        'TimeShift': _Choice({720: '+12:00', 660: '+11:00', 600: '+10:00', 540: '+9:00', 480: '+8:00', 420: '+7:00', 360: '+6:00', 300: '+5:00', 240: '+4:00', 180: '+3:00', 120: '+2:00', 60: '+1:00', 0: '0:00 (no shift)', -60: '-1:00', -120: '-2:00', -180: '-3:00', -240: '-4:00', -300: '-5:00', -360: '-6:00', -420: '-7:00', -480: '-8:00', -540: '-9:00', -600: '-10:00', -660: '-11:00', -720: '-12:00'}, default=0),  # Time shift
        'ModeStep': 100,  # Mode step (points)
        'HgPointScale': _Choice({1: '*1', 10: '*10', 100: '*100'}, default=10),  # Point scale
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volume type
        'DataSource': _Choice({0: 'Ticks', 1: 'M1 bars', 5: 'M5 bars', 15: 'M15 bars', 30: 'M30 bars'}, default=1),  # Data source
        'HgBarStyle': _Choice({0: 'Line', 1: 'Empty bar', 2: 'Filled bar', 3: 'Outline', 4: 'Color'}, default=0),  # Bar style
        'DrawDirection': _Choice({0: 'Right to left', 1: 'Left to right'}, default=1),  # Draw direction
        'HgLineWidth': 1,  # Line width
        'ModeLineWidth': 1,  # Mode line width
        'StatLineStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),  # Median & VWAP line style
    }

