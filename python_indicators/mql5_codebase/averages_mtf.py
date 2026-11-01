"""averages_-_mtf — converted from MQL5: MQL5 Indicators/Averages MTF/averages_-_mtf.mq5

Copyright: mladen; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16760576, 9662683]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Label1'}, 'levels': [], 'description': [], 'name': 'averages_-_mtf', 'source': 'MQL5 Indicators/Averages MTF/averages_-_mtf.mq5', 'folder': 'Averages MTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': 'Time frame', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Apply to', 'sinput': False}, {'mql': 'AveragePeriod', 'py': 'AveragePeriod', 'param': 'AveragePeriod', 'type': 'int', 'default': 14, 'label': 'Calculation period', 'sinput': False}, {'mql': 'AverageType', 'py': 'AverageType', 'param': 'AverageType', 'type': 'int', 'default': 0, 'label': 'Calculation type', 'sinput': False}, {'mql': '_', 'py': '_', 'param': None, 'type': 'string', 'default': '', 'label': 'T3 parameters (used only if T3 chosen)', 'sinput': False}, {'mql': 'T3Hot', 'py': 'T3Hot', 'param': 'T3Hot', 'type': 'double', 'default': 0.7, 'label': 'T3 hot value', 'sinput': False}, {'mql': 'T3Original', 'py': 'T3Original', 'param': 'T3Original', 'type': 'bool', 'default': False, 'label': 'T3 original Tillson calculation?', 'sinput': False}, {'mql': '__', 'py': '__', 'param': None, 'type': 'string', 'default': '', 'label': 'Quantile parameters (used only if Quantiles chosen)', 'sinput': False}, {'mql': 'QuantPercent', 'py': 'QuantPercent', 'param': 'QuantPercent', 'type': 'double', 'default': 50.0, 'label': 'Quantile percent (50 == Median)', 'sinput': False}, {'mql': 'Multicolor', 'py': 'Multicolor', 'param': 'Multicolor', 'type': 'bool', 'default': True, 'label': 'Multi color mode?', 'sinput': False}, {'mql': 'Interpolate', 'py': 'Interpolate', 'param': 'Interpolate', 'type': 'bool', 'default': True, 'label': 'Interpolate mtf data ?', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_PATH = 0  # MQL5 constant unknown to the converter

# enum enumAveragesType
avgSma = 0
avgEma = 1
avgSmma = 2
avgLwma = 3
avgLsma = 4
avgTrima = 5
avgSwma = 6
avgHullma = 7
avgT3ma = 8
avgQuant = 9
_enum('enumAveragesType', {0: 'avgSma', 1: 'avgEma', 2: 'avgSmma', 3: 'avgLwma', 4: 'avgLsma', 5: 'avgTrima', 6: 'avgSwma', 7: 'avgHullma', 8: 'avgT3ma', 9: 'avgQuant'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_CURRENT)  # Time frame
Price = _input('Price', PRICE_CLOSE)  # Apply to
AveragePeriod = _input('AveragePeriod', 14)  # Calculation period
AverageType = _input('AverageType', 0)  # Calculation type
_ = _input('_', '')  # T3 parameters (used only if T3 chosen)
T3Hot = _input('T3Hot', 0.7)  # T3 hot value
T3Original = _input('T3Original', False)  # T3 original Tillson calculation?
__ = _input('__', '')  # Quantile parameters (used only if Quantiles chosen)
QuantPercent = _input('QuantPercent', 50.0)  # Quantile percent (50 == Median)
Multicolor = _input('Multicolor', True)  # Multi color mode?
Interpolate = _input('Interpolate', True)  # Interpolate mtf data ?
MaBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
CountBuffer = Arr(0, 0.0)
gAverageType = 0
timeFrame = 0
mtfHandle = 0
calculating = False
methodNames = Arr.of(['Simple MA', 'Eexponential MA', 'Smoothed MA', 'Liner weighted MA', 'Linear regression value', 'Triangular MA', 'Sine weighted MA', 'Hull MA', 'T3 MA', 'Quantile'], fill="")

class averages(MqlObject):
    _q_fields = ('aResultBuffer', 'aPricesBuffer', 't3c1', 't3c2', 't3c3', 't3c4', 't3period', 't3Original', 'quantPercent', 'T3Initialized', 'QuantInitialized')
    def __init__(self, *args):
        self.aResultBuffer = Arr(0, 0.0)
        self.aPricesBuffer = Arr(0, 0.0)
        self.t3c1 = 0.0
        self.t3c2 = 0.0
        self.t3c3 = 0.0
        self.t3c4 = 0.0
        self.t3period = 0.0
        self.t3Original = False
        self.quantPercent = 0.0
        self.T3Initialized = False
        self.QuantInitialized = False
    def averages(self):
        self.T3Initialized = False
        self.QuantInitialized = False
    def calc(self, symbol, period, cPeriod, cType, cPrice, i):
        if symbol == "":
            symbol = Symbol()
        if period == 0:
            period = Period()
        bars = Bars(symbol, period)
        if ArrayRange(self.aPricesBuffer, 0) != bars:
            ArrayResize(self.aPricesBuffer, bars)
        self.aPricesBuffer[i] = cPrice
        _sw1 = cType
        if _sw1 == avgSma:
            avg = 0.0
            k = 0
            k = 0
            while k < cPeriod and (i - k) >= 0:
                avg += self.aPricesBuffer[i - k]
                k += 1
            return _fdiv(avg, k)
        elif _sw1 == avgEma:
            if ArrayRange(self.aResultBuffer, 0) != bars:
                ArrayResize(self.aResultBuffer, bars)
            if i > 0:
                self.aResultBuffer[i] = self.aResultBuffer[i - 1] + (_fdiv(2, cPeriod + 1) * (cPrice - self.aResultBuffer[i - 1]))
            else:
                self.aResultBuffer[i] = self.aPricesBuffer[i]
            return self.aResultBuffer[i]
        elif _sw1 == avgSmma:
            if ArrayRange(self.aResultBuffer, 0) != bars:
                ArrayResize(self.aResultBuffer, bars)
            if i <= cPeriod:
                avg = 0.0
                k = 0
                k = 0
                while k < cPeriod and (i - k) >= 0:
                    avg += self.aPricesBuffer[i - k]
                    k += 1
                if k > 0:
                    self.aResultBuffer[i] = _fdiv(avg, k)
                else:
                    self.aResultBuffer[i] = self.aPricesBuffer[i]
            else:
                self.aResultBuffer[i] = _fdiv((self.aResultBuffer[i - 1] * (cPeriod - 1)) + self.aPricesBuffer[i], cPeriod)
            return self.aResultBuffer[i]
        elif _sw1 == avgLwma:
            sum_ = 0.0
            sumw = 0.0
            k = 0
            while k < cPeriod and (i - k) >= 0:
                weight = cPeriod - k
                sumw += weight
                sum_ += weight * self.aPricesBuffer[i - k]
                k += 1
            if sumw != 0:
                return _fdiv(sum_, sumw)
            else:
                return EMPTY_VALUE
        elif _sw1 == avgLsma:
            return (3 * _s_averages_calc_lwma.calc(symbol, period, cPeriod, avgLwma, cPrice, i)) - (2 * _s_averages_calc_sma.calc(symbol, period, cPeriod, avgSma, cPrice, i))
        elif _sw1 == avgTrima:
            half = (cPeriod + 1.0) / 2.0
            sum_ = 0.0
            sumw = 0.0
            k = 0
            while k < cPeriod and (i - k) >= 0:
                weight = cPeriod - k
                if weight > half:
                    weight = cPeriod - k
                sumw += weight
                sum_ += weight * self.aPricesBuffer[i - k]
                k += 1
            if sumw != 0:
                return _fdiv(sum_, sumw)
            else:
                return EMPTY_VALUE
        elif _sw1 == avgSwma:
            sum_ = 0.0
            sumw = 0.0
            k = 0
            while k < cPeriod and (i - k) >= 0:
                weight = MathSin(_fdiv(3.141592653589793 * (k + 1), cPeriod + 1))
                sumw += weight
                sum_ += weight * self.aPricesBuffer[i - k]
                k += 1
            if sumw != 0:
                return _fdiv(sum_, sumw)
            else:
                return EMPTY_VALUE
        elif _sw1 == avgHullma:
            HalfPeriod = _int(MathFloor(cPeriod / 2))
            HullPeriod = _int(MathFloor(MathSqrt(cPeriod)))
            price1 = (_s_averages_calc_lwma1.calc(symbol, period, HalfPeriod, avgLwma, cPrice, i) * 2) - _s_averages_calc_lwma2.calc(symbol, period, cPeriod, avgLwma, cPrice, i)
            return _s_averages_calc_lwma3.calc(symbol, period, HullPeriod, avgLwma, price1, i)
        elif _sw1 == avgQuant:
            if ArraySize(_s_averages_calc_quantileArray) != cPeriod:
                ArrayResize(_s_averages_calc_quantileArray, _int(cPeriod))
            k = 0
            while k < cPeriod and (i - k) >= 0:
                _s_averages_calc_quantileArray[k] = self.aPricesBuffer[i - k]
                k += 1
            ArraySort(_s_averages_calc_quantileArray)
            index = ((cPeriod - 1) * self.quantPercent) / 100.0
            ind = _int(index)
            delta = index - ind
            if ind == NormalizeDouble(index, 5):
                return _s_averages_calc_quantileArray[ind]
            else:
                return ((1.0 - delta) * _s_averages_calc_quantileArray[ind]) + (delta * _s_averages_calc_quantileArray[ind + 1])
        elif _sw1 == avgT3ma:
            price1 = _s_averages_calc_ema1.calc(symbol, period, self.t3period, avgEma, cPrice, i)
            price2 = _s_averages_calc_ema2.calc(symbol, period, self.t3period, avgEma, price1, i)
            price3 = _s_averages_calc_ema3.calc(symbol, period, self.t3period, avgEma, price2, i)
            price4 = _s_averages_calc_ema4.calc(symbol, period, self.t3period, avgEma, price3, i)
            price5 = _s_averages_calc_ema5.calc(symbol, period, self.t3period, avgEma, price4, i)
            price6 = _s_averages_calc_ema6.calc(symbol, period, self.t3period, avgEma, price5, i)
            return (self.t3c1 * price6) + (self.t3c2 * price5) + (self.t3c3 * price4) + (self.t3c4 * price3)
        return EMPTY_VALUE
    def setT3Parameters(self, cPeriod, cT3Hot, cT3Original):
        cT3Hot = MathMax(MathMin(cT3Hot, 1), 0.0001)
        a = cT3Hot
        self.t3c1 = (-a) * a * a
        self.t3c2 = 3 * ((a * a) + (a * a * a))
        self.t3c3 = -3 * ((2 * a * a) + a + (a * a * a))
        self.t3c4 = 1 + (3 * a) + (a * a * a) + (3 * a * a)
        self.t3period = cPeriod
        if not cT3Original:
            self.t3period = 1.0 + ((self.t3period - 1.0) / 2.0)
        self.T3Initialized = True
    def setQuantParameters(self, cPercent):
        self.quantPercent = MathMax(MathMin(cPercent, 100), 0)
        self.QuantInitialized = True

def OnInit():
    global calculating, gAverageType, mtfHandle, timeFrame
    SetIndexBuffer(0, MaBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, CountBuffer, INDICATOR_CALCULATIONS)
    gAverageType = AverageType
    timeFrame = MathMax(Period(), TimeFrame)
    calculating = timeFrame == Period()
    if not calculating:
        name = getIndicatorName()
        mtfHandle = iCustom(None, timeFrame, name, PERIOD_CURRENT, Price, AveragePeriod, AverageType, '', T3Hot, T3Original, '', QuantPercent, Multicolor)
    PlotIndexSetString(0, PLOT_LABEL, getAverageName(_GlobRef(globals(), 'gAverageType')) + ' (' + _str(AveragePeriod) + ')')
    IndicatorSetString(INDICATOR_SHORTNAME, getAverageName(_GlobRef(globals(), 'gAverageType')) + ' (' + _str(AveragePeriod) + ')')
    return 0

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    if calculating:
        if AverageType == avgT3ma and (not _s_OnCalculate_caverage.T3Initialized):
            _s_OnCalculate_caverage.setT3Parameters(AveragePeriod, T3Hot, T3Original)
        if AverageType == avgQuant and (not _s_OnCalculate_caverage.QuantInitialized):
            _s_OnCalculate_caverage.setQuantParameters(QuantPercent)
        for i in range(MathMax(prev_calculated - 1, 0), rates_total):
            price = getPrice(Price, rates_total - i - 1)
            MaBuffer[i] = _s_OnCalculate_caverage.calc("", 0, AveragePeriod, gAverageType, price, i)
            if Multicolor and i > 0:
                ColorBuffer[i] = ColorBuffer[i - 1]
                if MaBuffer[i] > MaBuffer[i - 1]:
                    ColorBuffer[i] = 0.0
                if MaBuffer[i] < MaBuffer[i - 1]:
                    ColorBuffer[i] = 1.0
            else:
                ColorBuffer[i] = 0.0
        CountBuffer[rates_total - 1] = MathMax(rates_total - prev_calculated + 1, 1)
        return rates_total
    times = Arr(0, 0)
    startTime = Time[0] - PeriodSeconds(timeFrame)
    endTime = Time[rates_total - 1]
    bars = CopyTime(None, timeFrame, _DT(startTime), _DT(endTime), times)
    if times[0] > Time[0] or bars < 1:
        return prev_calculated
    values = Arr(0, 0.0)
    CopyBuffer(mtfHandle, 0, 0, bars, values)
    colors = Arr(0, 0.0)
    CopyBuffer(mtfHandle, 1, 0, bars, colors)
    counts = Arr(0, 0.0)
    CopyBuffer(mtfHandle, 2, 0, bars, counts)
    maxb = _int(MathMax(MathMin(_fdiv(counts[bars - 1] * PeriodSeconds(timeFrame), PeriodSeconds(Period())), rates_total - 1), 1))
    for i in range(MathMax(prev_calculated - maxb, 0), rates_total):
        d = dateArrayBsearch(times, Time[i], bars)
        if d > -1 and d < bars:
            MaBuffer[i] = values[d]
            ColorBuffer[i] = colors[d]
        if not Interpolate:
            continue
        l = MathMin(i + 1, rates_total - 1)
        if d != dateArrayBsearch(times, Time[l], bars) or i == l:
            n = 0
            k = 0
            n = 1
            while (i - n) > 0 and Time[i - n] >= times[d]:
                n += 1
                continue
                n += 1
            k = 1
            while (i - k) >= 0 and k < n:
                MaBuffer[i - k] = MaBuffer[i] + _fdiv((MaBuffer[i - n] - MaBuffer[i]) * k, n)
                k += 1
    return rates_total

def getPrice(price, position):
    _rates = Arr(0, 0, factory=MqlRates)
    copyCount = CopyRates(Symbol(), Period(), position, 1, _rates)
    if copyCount == 1:
        _sw2 = price
        if _sw2 == PRICE_CLOSE:
            return _rates[0].close
        elif _sw2 == PRICE_HIGH:
            return _rates[0].high
        elif _sw2 == PRICE_LOW:
            return _rates[0].low
        elif _sw2 == PRICE_OPEN:
            return _rates[0].open
        elif _sw2 == PRICE_MEDIAN:
            return (_rates[0].high + _rates[0].low) / 2.0
        elif _sw2 == PRICE_TYPICAL:
            return (_rates[0].high + _rates[0].low + _rates[0].close) / 3.0
        elif _sw2 == PRICE_WEIGHTED:
            return (_rates[0].high + _rates[0].low + _rates[0].close + _rates[0].close) / 4.0
        else:
            return 0.0
    return 0.0

def dateArrayBsearch(times, toFind, total):
    mid = 0
    first = 0
    last = total - 1
    while last >= first:
        mid = (first + last) >> 1
        if toFind == times[mid] or ((mid < (total - 1) and toFind > times[mid]) and toFind < times[mid + 1]):
            break
        if toFind < times[mid]:
            last = mid - 1
        else:
            first = mid + 1
    return mid

def getIndicatorName():
    progPath = MQL5InfoString(MQL5_PROGRAM_PATH)
    terminalPath = TerminalInfoString(TERMINAL_PATH)
    startLength = StringLen(terminalPath) + 17
    progLength = StringLen(progPath)
    indicatorName = StringSubstr(progPath, startLength)
    indicatorName = StringSubstr(indicatorName, 0, StringLen(indicatorName) - 4)
    return indicatorName

def getAverageName(method):
    method.v = MathMax(MathMin(method.v, 10), 0)
    return methodNames[method.v]

# ---- static local variables
_s_averages_calc_lwma = averages()
_s_averages_calc_sma = averages()
_s_averages_calc_lwma1 = averages()
_s_averages_calc_lwma2 = averages()
_s_averages_calc_lwma3 = averages()
_s_averages_calc_quantileArray = Arr(0, 0.0)
_s_averages_calc_ema1 = averages()
_s_averages_calc_ema2 = averages()
_s_averages_calc_ema3 = averages()
_s_averages_calc_ema4 = averages()
_s_averages_calc_ema5 = averages()
_s_averages_calc_ema6 = averages()
_s_OnCalculate_caverage = averages()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AveragesMtf(_MQL5Indicator):
    name = 'averages_-_mtf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Time frame
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Apply to
        'AveragePeriod': 14,  # Calculation period
        'AverageType': _Choice({0: 'Simple moving average', 1: 'Exponential moving average', 2: 'Smoothed moving average', 3: 'Linear weighted moving average', 4: 'Linear regression value', 5: 'Triangular moving average', 6: 'Sine weighted moving average', 7: 'Hull moving average', 8: 'T3 moving average', 9: 'Qunatiles'}, default=0),  # Calculation type
        'T3Hot': 0.7,  # T3 hot value
        'T3Original': False,  # T3 original Tillson calculation?
        'QuantPercent': 50.0,  # Quantile percent (50 == Median)
        'Multicolor': True,  # Multi color mode?
        'Interpolate': True,  # Interpolate mtf data ?
    }

