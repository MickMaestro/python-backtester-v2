"""Pivot oscillator extended — converted from MQL5: MQL5 Indicators/Pivot Oscillator Extended/Pivot oscillator extended.mq5

Pivot oscillator extended 
Copyright: © mladen, 2018; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '© mladen, 2018', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 9, 'indicator_plots': 8}, 'types': {8: 1}, 'colors': {8: [6908265]}, 'widths': {8: 2}, 'styles': {}, 'labels': {8: 'Price'}, 'levels': [], 'description': ['Pivot oscillator extended '], 'name': 'Pivot oscillator extended', 'source': 'MQL5 Indicators/Pivot Oscillator Extended/Pivot oscillator extended.mq5', 'folder': 'Pivot Oscillator Extended', 'inputs': [{'mql': 'inpTimeFrame', 'py': 'inpTimeFrame', 'param': 'inpTimeFrame', 'type': 'int', 'default': 16408, 'label': 'Time frame', 'sinput': False}, {'mql': 'inpPivotType', 'py': 'inpPivotType', 'param': 'inpPivotType', 'type': 'int', 'default': 0, 'label': 'Pivot calculated as', 'sinput': False}, {'mql': 'inpPivotCalculate', 'py': 'inpPivotCalculate', 'param': 'inpPivotCalculate', 'type': 'int', 'default': 0, 'label': 'Calculation method', 'sinput': False}, {'mql': 'inpColorSup', 'py': 'inpColorSup', 'param': None, 'type': 'color', 'default': 3329330, 'label': 'Support lines color', 'sinput': False}, {'mql': 'inpColorRes', 'py': 'inpColorRes', 'param': None, 'type': 'color', 'default': 255, 'label': 'Resistance lines color', 'sinput': False}, {'mql': 'inpColorPiv', 'py': 'inpColorPiv', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'Pivot line color', 'sinput': False}, {'mql': 'inpSaRStyle', 'py': 'inpSaRStyle', 'param': 'inpSaRStyle', 'type': 'int', 'default': 2, 'label': 'Pivot, support and resistance lines style', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_PATH = 0  # MQL5 constant unknown to the converter

# enum enTimeFrames
tf_cu = 0
tf_m1 = 1
tf_m2 = 2
tf_m3 = 3
tf_m4 = 4
tf_m5 = 5
tf_m6 = 6
tf_m10 = 10
tf_m12 = 12
tf_m15 = 15
tf_m20 = 20
tf_m30 = 30
tf_h1 = 16385
tf_h2 = 16386
tf_h3 = 16387
tf_h4 = 16388
tf_h6 = 16390
tf_h8 = 16392
tf_h12 = 16396
tf_d1 = 16408
tf_w1 = 32769
tf_mn = 49153
tf_cp1 = -1
tf_cp2 = -2
tf_cp3 = -3
tf_cp4 = -4
_enum('enTimeFrames', {0: 'tf_cu', 1: 'tf_m1', 2: 'tf_m2', 3: 'tf_m3', 4: 'tf_m4', 5: 'tf_m5', 6: 'tf_m6', 10: 'tf_m10', 12: 'tf_m12', 15: 'tf_m15', 20: 'tf_m20', 30: 'tf_m30', 16385: 'tf_h1', 16386: 'tf_h2', 16387: 'tf_h3', 16388: 'tf_h4', 16390: 'tf_h6', 16392: 'tf_h8', 16396: 'tf_h12', 16408: 'tf_d1', 32769: 'tf_w1', 49153: 'tf_mn', -1: 'tf_cp1', -2: 'tf_cp2', -3: 'tf_cp3', -4: 'tf_cp4'})

# enum ePivotTypes
ptHLC = 0
ptHLCC = 1
ptHLOC = 2
ptHLOO = 3
_enum('ePivotTypes', {0: 'ptHLC', 1: 'ptHLCC', 2: 'ptHLOC', 3: 'ptHLOO'})

# enum eCalculation
ecOriginal = 0
ecAlternate = 1
_enum('eCalculation', {0: 'ecOriginal', 1: 'ecAlternate'})

# ---- inputs and global variables
inpTimeFrame = _input('inpTimeFrame', tf_d1)  # Time frame
inpPivotType = _input('inpPivotType', ptHLC)  # Pivot calculated as
inpPivotCalculate = _input('inpPivotCalculate', ecOriginal)  # Calculation method
inpColorSup = _input('inpColorSup', clrLimeGreen)  # Support lines color
inpColorRes = _input('inpColorRes', clrRed)  # Resistance lines color
inpColorPiv = _input('inpColorPiv', clrGray)  # Pivot line color
inpSaRStyle = _input('inpSaRStyle', STYLE_DOT)  # Pivot, support and resistance lines style
PBuffer = Arr(0, 0.0)
S1Buffer = Arr(0, 0.0)
R1Buffer = Arr(0, 0.0)
S2Buffer = Arr(0, 0.0)
R2Buffer = Arr(0, 0.0)
S3Buffer = Arr(0, 0.0)
R3Buffer = Arr(0, 0.0)
Price = Arr(0, 0.0)
count = Arr(0, 0.0)
_mtfHandle = INVALID_HANDLE
_indicatorTimeFrame = 0
_indicatorName = ""
_pivotDescriptions = Arr.of(['(high+low+close)/3', '(high+low+close+close)/4', '(high+low+close+open)/4', '(high+low+open+open)/4'], fill="")
_tfsPer = Arr.of([PERIOD_M1, PERIOD_M2, PERIOD_M3, PERIOD_M4, PERIOD_M5, PERIOD_M6, PERIOD_M10, PERIOD_M12, PERIOD_M15, PERIOD_M20, PERIOD_M30, PERIOD_H1, PERIOD_H2, PERIOD_H3, PERIOD_H4, PERIOD_H6, PERIOD_H8, PERIOD_H12, PERIOD_D1, PERIOD_W1, PERIOD_MN1], fill=0)
_tfsStr = Arr.of(['1 minute', '2 minutes', '3 minutes', '4 minutes', '5 minutes', '6 minutes', '10 minutes', '12 minutes', '15 minutes', '20 minutes', '30 minutes', '1 hour', '2 hours', '3 hours', '4 hours', '6 hours', '8 hours', '12 hours', 'daily', 'weekly', 'monthly'], fill="")

def OnInit():
    global _indicatorName, _indicatorTimeFrame, _mtfHandle
    SetIndexBuffer(0, PBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_LINE_COLOR, inpColorPiv)
    SetIndexBuffer(1, S1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_LINE_COLOR, inpColorSup)
    SetIndexBuffer(2, R1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_LINE_COLOR, inpColorRes)
    SetIndexBuffer(3, S2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_LINE_COLOR, inpColorSup)
    SetIndexBuffer(4, R2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_LINE_COLOR, inpColorRes)
    SetIndexBuffer(5, S3Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_LINE_COLOR, inpColorSup)
    SetIndexBuffer(6, R3Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(6, PLOT_LINE_COLOR, inpColorRes)
    SetIndexBuffer(7, Price, INDICATOR_DATA)
    SetIndexBuffer(8, count, INDICATOR_CALCULATIONS)
    for i in range(0, 7):
        PlotIndexSetInteger(i, PLOT_DRAW_TYPE, DRAW_LINE)
        PlotIndexSetInteger(i, PLOT_LINE_STYLE, inpSaRStyle)
    _indicatorTimeFrame = MathMax(timeFrameGet(inpTimeFrame), Period())
    _indicatorName = getIndicatorName()
    if _indicatorTimeFrame != Period():
        _mtfHandle = iCustom(Symbol(), _indicatorTimeFrame, _indicatorName, 0)
        if _mtfHandle == INVALID_HANDLE:
            return INIT_FAILED
    IndicatorSetString(INDICATOR_SHORTNAME, 'Pivot ' + _pivotDescriptions[inpPivotType] + ' oscillator (' + timeFrameToString(_indicatorTimeFrame) + ')')
    return INIT_SUCCEEDED

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Bars(Symbol(), Period()) < rates_total:
        return prev_calculated
    _prevMark = 0
    _tfSeconds = PeriodSeconds(_indicatorTimeFrame)
    i = MathMax(prev_calculated - 1, 0)
    P = 0.0
    R1 = 0.0
    S1 = 0.0
    R2 = 0.0
    S2 = 0.0
    R3 = 0.0
    S3 = 0.0
    if _mtfHandle != INVALID_HANDLE:
        result = Arr(1, 0.0, dyn=False)
        if BarsCalculated(_mtfHandle) < 0:
            return prev_calculated
        if CopyBuffer(_mtfHandle, 8, 0, 1, result) != 1:
            return prev_calculated
        i = MathMin(MathMax(prev_calculated - 1, 0), MathMax(rates_total - _int(_fdiv(result[0] * float(PeriodSeconds(_indicatorTimeFrame)), PeriodSeconds(Period()))) - 1, 0))
    while i < rates_total:
        _currMark = _int(float(_idiv(time[i], _tfSeconds)))
        if _currMark != _prevMark:
            _rates = Arr(0, 0, factory=MqlRates)
            _ratesCopied = CopyRates(Symbol(), _indicatorTimeFrame, _DT(time[i]), 2, _rates)
            LastHigh = (_rates[0].high if (_ratesCopied == 2) else 0)
            LastLow = (_rates[0].low if (_ratesCopied == 2) else 0)
            LastClose = (_rates[0].close if (_ratesCopied == 2) else 0)
            LastOpen = (_rates[0].open if (_ratesCopied == 2) else 0)
            if _ratesCopied == 2:
                P = 0.0
                _sw1 = inpPivotType
                if _sw1 == ptHLC:
                    P = (LastHigh + LastLow + LastClose) / 3.0
                elif _sw1 == ptHLCC:
                    P = (LastHigh + LastLow + LastClose + LastClose) / 4.0
                elif _sw1 == ptHLOC:
                    P = (LastHigh + LastLow + LastClose + LastOpen) / 4.0
                elif _sw1 == ptHLOO:
                    P = (LastHigh + LastLow + LastOpen + LastOpen) / 4.0
                if inpPivotCalculate == ecOriginal:
                    R1 = P + (P - LastLow)
                    S1 = P - (LastHigh - P)
                    R2 = P + (LastHigh - LastLow)
                    S2 = P - (LastHigh - LastLow)
                    R3 = P + ((LastHigh - LastLow) * 2.0)
                    S3 = P - ((LastHigh - LastLow) * 2.0)
                else:
                    R1 = (P * 2.0) - LastLow
                    S1 = (P * 2.0) - LastHigh
                    R2 = P + (LastHigh - LastLow)
                    S2 = P - (LastHigh - LastLow)
                    R3 = (P * 2.0) + (LastHigh - (2.0 * LastLow))
                    S3 = (P * 2.0) - ((2.0 * LastHigh) - LastLow)
        lower = S3
        range_ = R3 - S3
        if range_ != 0:
            R3Buffer[i] = 1.0
            S3Buffer[i] = -1.0
            R1Buffer[i] = 2.0 * (_fdiv(R1 - lower, range_) - 0.5)
            S1Buffer[i] = 2.0 * (_fdiv(S1 - lower, range_) - 0.5)
            R2Buffer[i] = 2.0 * (_fdiv(R2 - lower, range_) - 0.5)
            S2Buffer[i] = 2.0 * (_fdiv(S2 - lower, range_) - 0.5)
            PBuffer[i] = 2.0 * (_fdiv(P - lower, range_) - 0.5)
            Price[i] = 2.0 * (_fdiv(close[i] - lower, range_) - 0.5)
        i += 1
    return rates_total

def timeFrameToString(period):
    if period == PERIOD_CURRENT:
        period = Period()
    i = 0
    i = 0
    for i in range(i, ArraySize(_tfsPer)):
        if period == _tfsPer[i]:
            break
    else:
        i = _range_end(i, ArraySize(_tfsPer), 1)
    return _tfsStr[i]

def timeFrameGet(period):
    _shift = (MathAbs(period) if (period < 0) else 0)
    if _shift > 0 or period == tf_cu:
        period = Period()
    i = 0
    i = 0
    for i in range(i, ArraySize(_tfsPer)):
        if period == _tfsPer[i]:
            break
    else:
        i = _range_end(i, ArraySize(_tfsPer), 1)
    return _tfsPer[MathMin(i + _shift, ArraySize(_tfsPer) - 1)]

def getIndicatorName():
    _path = Box(MQL5InfoString(MQL5_PROGRAM_PATH))
    StringToLower(_path)
    _partsA = Arr(0, "")
    _partsS = StringGetCharacter('\\', 0)
    _partsN = StringSplit(_path.v, _partsS, _partsA)
    name = _partsA[_partsN - 1]
    n = _partsN - 2
    while n >= 0 and _partsA[n] != 'indicators':
        name = _partsA[n] + '\\' + name
        n -= 1
    return name


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PivotOscillatorExtended(_MQL5Indicator):
    name = 'Pivot oscillator extended'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'inpTimeFrame': _Choice({0: 'Current time frame', 1: '1 minute', 2: '2 minutes', 3: '3 minutes', 4: '4 minutes', 5: '5 minutes', 6: '6 minutes', 10: '10 minutes', 12: '12 minutes', 15: '15 minutes', 20: '20 minutes', 30: '30 minutes', 16385: '1 hour', 16386: '2 hours', 16387: '3 hours', 16388: '4 hours', 16390: '6 hours', 16392: '8 hours', 16396: '12 hours', 16408: 'daily', 32769: 'weekly', 49153: 'monthly', -1: 'Next higher time frame', -2: 'Second higher time frame', -3: 'Third higher time frame', -4: 'Fourth higher time frame'}, default=16408),  # Time frame
        'inpPivotType': _Choice({0: '(high+low+close)/3', 1: '(high+low+close+close)/4', 2: '(high+low+close+open)/4', 3: '(high+low+open+open)/4'}, default=0),  # Pivot calculated as
        'inpPivotCalculate': _Choice({0: 'Calculate pivot the original way', 1: 'Calculate pivot the "alternate" way'}, default=0),  # Calculation method
        'inpSaRStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=2),  # Pivot, support and resistance lines style
    }

