"""universaloscillator — converted from MQL5: MQL5 Indicators/Universal Oscillator/universaloscillator.mq5

1) Includes Bears Power, Bulls Power, CCI, DeMarker, MACD, Momentum, RSI, Stochastic, WPR.
2) Has three draw mode: a) Line, b) Filling, c) Color Histogram.
3) Has three levels mode: a) constant levels, b) dynamic levels based on MA, c) dynamic levels 
based on Bollinger Bands.
Copyright: Copyright 2013, Rone.; Link: rone.sergey@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2013, Rone.', 'link': 'rone.sergey@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 1, 4: 1}, 'colors': {1: [16711680, 255], 2: [11119017], 3: [11119017], 4: [11119017]}, 'widths': {1: 2, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Value1;Value2', 2: 'Middle', 3: 'OverBought', 4: 'OverSold'}, 'levels': [], 'description': ['1) Includes Bears Power, Bulls Power, CCI, DeMarker, MACD, Momentum, RSI, Stochastic, WPR.', '2) Has three draw mode: a) Line, b) Filling, c) Color Histogram.', '3) Has three levels mode: a) constant levels, b) dynamic levels based on MA, c) dynamic levels ', 'based on Bollinger Bands.'], 'name': 'universaloscillator', 'source': 'MQL5 Indicators/Universal Oscillator/universaloscillator.mq5', 'folder': 'Universal Oscillator', 'inputs': [{'mql': 'InpOscillator', 'py': 'InpOscillator', 'param': 'InpOscillator', 'type': 'int', 'default': 6, 'label': 'Oscillator', 'sinput': False}, {'mql': 'InpOscPeriod1', 'py': 'InpOscPeriod1', 'param': 'InpOscPeriod1', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'InpDrawMode', 'py': 'InpDrawMode', 'param': 'InpDrawMode', 'type': 'int', 'default': 1, 'label': 'Draw Mode', 'sinput': False}, {'mql': 'InpLevelsMode', 'py': 'InpLevelsMode', 'param': 'InpLevelsMode', 'type': 'int', 'default': 2, 'label': 'Levels Mode', 'sinput': False}, {'mql': 'InpLevelsPeriod', 'py': 'InpLevelsPeriod', 'param': 'InpLevelsPeriod', 'type': 'int', 'default': 50, 'label': 'Levels Period', 'sinput': False}, {'mql': 'InpLevelsIndent', 'py': 'InpLevelsIndent', 'param': 'InpLevelsIndent', 'type': 'double', 'default': 2.0, 'label': 'Levels Indent / Deviation', 'sinput': False}, {'mql': 'InpIndentAutoCorrection', 'py': 'InpIndentAutoCorrection', 'param': 'InpIndentAutoCorrection', 'type': 'bool', 'default': True, 'label': 'Levels Auto Correction', 'sinput': False}, {'mql': 'InpDivider', 'py': 'InpDivider', 'param': None, 'type': 'string', 'default': '---For Stochastic or MACD---', 'label': 'Just Divider NOT Parameter', 'sinput': False}, {'mql': 'InpOscPeriod2', 'py': 'InpOscPeriod2', 'param': 'InpOscPeriod2', 'type': 'int', 'default': 3, 'label': 'Stoch %D / MACD Slow EMA', 'sinput': False}, {'mql': 'InpOscPeriod3', 'py': 'InpOscPeriod3', 'param': 'InpOscPeriod3', 'type': 'int', 'default': 3, 'label': 'Stoch Slowing / MACD Signal', 'sinput': False}, {'mql': 'InpStochPrice', 'py': 'InpStochPrice', 'param': 'InpStochPrice', 'type': 'int', 'default': 0, 'label': 'Stochastic Price', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# enum OSCILLATOR_NAME
BEARS = 0
BULLS = 1
CCI = 2
DEMARKER = 3
MACD = 4
MOMENTUM = 5
RSI = 6
STOCHASTIC = 7
WPR = 8
_enum('OSCILLATOR_NAME', {0: 'BEARS', 1: 'BULLS', 2: 'CCI', 3: 'DEMARKER', 4: 'MACD', 5: 'MOMENTUM', 6: 'RSI', 7: 'STOCHASTIC', 8: 'WPR'})

# enum LEVEL_MODE
CONST_VALUE_MODE = 0
MA_MODE = 1
BB_MODE = 2
_enum('LEVEL_MODE', {0: 'CONST_VALUE_MODE', 1: 'MA_MODE', 2: 'BB_MODE'})

# enum DRAW_MODE
LINE = 0
FILLING = 1
HISTOGRAM = 2
_enum('DRAW_MODE', {0: 'LINE', 1: 'FILLING', 2: 'HISTOGRAM'})

# ---- inputs and global variables
InpOscillator = _input('InpOscillator', RSI)  # Oscillator
InpOscPeriod1 = _input('InpOscPeriod1', 14)  # Period
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # Applied price
InpDrawMode = _input('InpDrawMode', FILLING)  # Draw Mode
InpLevelsMode = _input('InpLevelsMode', BB_MODE)  # Levels Mode
InpLevelsPeriod = _input('InpLevelsPeriod', 50)  # Levels Period
InpLevelsIndent = _input('InpLevelsIndent', 2.0)  # Levels Indent / Deviation
InpIndentAutoCorrection = _input('InpIndentAutoCorrection', True)  # Levels Auto Correction
InpDivider = _input('InpDivider', '---For Stochastic or MACD---')  # Just Divider NOT Parameter
InpOscPeriod2 = _input('InpOscPeriod2', 3)  # Stoch %D / MACD Slow EMA
InpOscPeriod3 = _input('InpOscPeriod3', 3)  # Stoch Slowing / MACD Signal
InpStochPrice = _input('InpStochPrice', STO_LOWHIGH)  # Stochastic Price
ExtBuffer1 = Arr(0, 0.0)
ExtBuffer2 = Arr(0, 0.0)
ExtBuffer3 = Arr(0, 0.0)
ExtBuffer4 = Arr(0, 0.0)
ExtBuffer5 = Arr(0, 0.0)
ExtBuffer6 = Arr(0, 0.0)
oscPeriod1 = 0
levelsPeriod = 0
minRequiredBars = 0
oscHandle = 0
oscPeriod2 = 0
oscPeriod3 = 0
midValue = 0.0
addValue = 0.0
levelsIndent = 0.0

def OnInit():
    global levelsIndent, levelsPeriod, midValue, minRequiredBars, oscHandle, oscPeriod1, oscPeriod2, oscPeriod3
    if InpOscPeriod1 < 1:
        oscPeriod1 = 14
        printf('Incorrected input parameter InpOscPeriod1 = %d. Indicator will use value %d.', InpOscPeriod1, oscPeriod1)
    else:
        oscPeriod1 = InpOscPeriod1
    if InpLevelsPeriod < 1:
        levelsPeriod = 10
        printf('Incorrected input parameter InpLevelsPeriod = %d. Indicator will use value %d.', InpLevelsPeriod, levelsPeriod)
    else:
        levelsPeriod = InpLevelsPeriod
    if InpOscPeriod2 < 1:
        oscPeriod2 = 3
        printf('Incorrected input parameter InpOscPeriod2 = %d. Indicator will use value %d.', InpOscPeriod2, oscPeriod2)
    else:
        oscPeriod2 = InpOscPeriod2
    if InpOscPeriod3 < 1:
        oscPeriod3 = 3
        printf('Incorrected input parameter InpOscPeriod3 = %d. Indicator will use value %d.', InpOscPeriod3, oscPeriod3)
    else:
        oscPeriod3 = InpOscPeriod3
    levelsIndent = MathAbs(InpLevelsIndent)
    minRequiredBars = oscPeriod1 + oscPeriod2 + oscPeriod3 + levelsPeriod - 1
    SetIndexBuffer(0, ExtBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ExtBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, ExtBuffer3, INDICATOR_DATA)
    SetIndexBuffer(3, ExtBuffer4, INDICATOR_DATA)
    SetIndexBuffer(4, ExtBuffer5, INDICATOR_DATA)
    SetIndexBuffer(5, ExtBuffer6, INDICATOR_DATA)
    shortname = 'UniOsc: '
    _sw1 = InpOscillator
    if _sw1 == BEARS:
        oscHandle = iBearsPower(Symbol(), Period(), oscPeriod1)
        midValue = 0.0
        shortname += 'Bears Power (' + _str(oscPeriod1) + ')'
    elif _sw1 == BULLS:
        oscHandle = iBullsPower(Symbol(), Period(), oscPeriod1)
        midValue = 0.0
        shortname += 'Bulls Power (' + _str(oscPeriod1) + ')'
    elif _sw1 == CCI:
        oscHandle = iCCI(Symbol(), Period(), oscPeriod1, InpAppliedPrice)
        midValue = 0.0
        levelsAutoCorrect(30.0, 300.0, 200.0)
        shortname += 'CCI (' + _str(oscPeriod1) + ')'
    elif _sw1 == DEMARKER:
        oscHandle = iDeMarker(Symbol(), Period(), oscPeriod1)
        midValue = 0.5
        levelsAutoCorrect(0.05, 0.5, 0.3)
        shortname += 'DeMarker (' + _str(oscPeriod1) + ')'
    elif _sw1 == MACD:
        oscHandle = iMACD(Symbol(), Period(), oscPeriod1, oscPeriod2, oscPeriod3, InpAppliedPrice)
        midValue = 0.0
        shortname += 'MACD (' + _str(oscPeriod1) + ', ' + _str(oscPeriod2) + ', ' + _str(oscPeriod3) + ')'
    elif _sw1 == MOMENTUM:
        oscHandle = iMomentum(Symbol(), Period(), oscPeriod1, InpAppliedPrice)
        midValue = 100.0
        levelsAutoCorrect(0.03, 5.0, 0.5)
        shortname += 'Momentum (' + _str(oscPeriod1) + ')'
    elif _sw1 == RSI:
        oscHandle = iRSI(Symbol(), Period(), oscPeriod1, InpAppliedPrice)
        midValue = 50.0
        levelsAutoCorrect(5.0, 50.0, 20.0)
        shortname += 'RSI (' + _str(oscPeriod1) + ')'
    elif _sw1 == STOCHASTIC:
        oscHandle = iStochastic(Symbol(), Period(), oscPeriod1, oscPeriod2, oscPeriod3, MODE_SMA, InpStochPrice)
        midValue = 50.0
        levelsAutoCorrect(5.0, 50.0, 30.0)
        shortname += 'Stochastic (' + _str(oscPeriod1) + ', ' + _str(oscPeriod2) + ', ' + _str(oscPeriod3) + ')'
    elif _sw1 == WPR:
        oscHandle = iWPR(Symbol(), Period(), oscPeriod1)
        midValue = -50.0
        levelsAutoCorrect(5.0, 50.0, 30.0)
        shortname += 'WPR (' + _str(oscPeriod1) + ')'
    else:
        oscHandle = INVALID_HANDLE
        Print('Unknown Oscillator!')
        return -1
    _sw2 = InpDrawMode
    if _sw2 == FILLING:
        SetIndexBuffer(2, ExtBuffer3, INDICATOR_DATA)
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_FILLING)
    elif _sw2 == HISTOGRAM:
        SetIndexBuffer(2, ExtBuffer3, INDICATOR_COLOR_INDEX)
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_COLOR_HISTOGRAM2)
    else:
        SetIndexBuffer(2, ExtBuffer3, INDICATOR_DATA)
        PlotIndexSetInteger(0, PLOT_DRAW_TYPE, DRAW_LINE)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    return 0

def levelsAutoCorrect(minIndent, maxIndent, correctIndent):
    global levelsIndent
    if InpLevelsMode == BB_MODE:
        if levelsIndent > 4.0:
            levelsIndent = 2.0
            printf('Incorrected deviation input parameter InpLevelsIndent = %f. Indicator will use value %f.', InpLevelsIndent, levelsIndent)
    else:
        if levelsIndent < minIndent or levelsIndent > maxIndent:
            levelsIndent = correctIndent
            printf('Incorrected indent input parameter InpLevelsIndent = %f. Indicator will use value %f.', InpLevelsIndent, levelsIndent)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    startBar = 0
    calculated = 0
    toCopy = 0
    if rates_total < minRequiredBars:
        Print('Not enough bars for calculation.')
        return 0
    calculated = BarsCalculated(oscHandle)
    if calculated < rates_total:
        Print('Not all data of oscHandle is calculated (', calculated, ' bars. Error #', GetLastError())
        return 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        startBar = minRequiredBars
        toCopy = rates_total
    else:
        startBar = prev_calculated - 1
        toCopy = rates_total - prev_calculated
        if prev_calculated > 0:
            toCopy += 1
    if CopyBuffer(oscHandle, 0, 0, toCopy, ExtBuffer1) <= 0:
        Print('Getting Oscillator is failed. Error #', GetLastError())
        return 0
    if InpLevelsMode != CONST_VALUE_MODE:
        SimpleMAOnBuffer(rates_total, prev_calculated, oscPeriod1 + levelsPeriod, levelsPeriod, ExtBuffer1, ExtBuffer2)
    for bar in range(startBar, rates_total):
        value = 0.0
        sum_ = 0.0
        middleLine = 0.0
        indent = 0.0
        _sw3 = InpLevelsMode
        if _sw3 == MA_MODE:
            middleLine = ExtBuffer2[bar]
            indent = levelsIndent
        elif _sw3 == BB_MODE:
            value = ExtBuffer2[bar]
            middleLine = value
            for i in range(bar - levelsPeriod + 1, bar + 1):
                sum_ += MathPow(ExtBuffer1[i] - value, 2)
            indent = levelsIndent * MathSqrt(_fdiv(sum_, levelsPeriod))
        else:
            ExtBuffer2[bar] = midValue
            middleLine = ExtBuffer2[bar]
            indent = levelsIndent
        _sw4 = InpDrawMode
        if _sw4 == LINE:
            ExtBuffer3[bar] = middleLine + indent
            ExtBuffer4[bar] = middleLine - indent
        elif _sw4 == FILLING:
            ExtBuffer3[bar] = middleLine
            ExtBuffer4[bar] = middleLine + indent
            ExtBuffer5[bar] = middleLine - indent
        elif _sw4 == HISTOGRAM:
            if ExtBuffer1[bar] >= ExtBuffer2[bar]:
                ExtBuffer3[bar] = 0.0
            else:
                ExtBuffer3[bar] = 1.0
            ExtBuffer4[bar] = middleLine
            ExtBuffer5[bar] = middleLine + indent
            ExtBuffer6[bar] = middleLine - indent
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Universaloscillator(_MQL5Indicator):
    name = 'universaloscillator'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpOscillator': _Choice({0: 'Bears Power', 1: 'Bulls Power', 2: 'CCI', 3: 'DeMarker', 4: 'MACD', 5: 'Momentum', 6: 'RSI', 7: 'Stochastic', 8: 'Williams Percent Range'}, default=6),  # Oscillator
        'InpOscPeriod1': 14,  # Period
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied price
        'InpDrawMode': _Choice({0: 'Line', 1: 'Filling', 2: 'Histogram'}, default=1),  # Draw Mode
        'InpLevelsMode': _Choice({0: 'Constant level value mode', 1: 'Moving Average mode', 2: 'Bollinger Bands Mode'}, default=2),  # Levels Mode
        'InpLevelsPeriod': 50,  # Levels Period
        'InpLevelsIndent': 2.0,  # Levels Indent / Deviation
        'InpIndentAutoCorrection': True,  # Levels Auto Correction
        'InpOscPeriod2': 3,  # Stoch %D / MACD Slow EMA
        'InpOscPeriod3': 3,  # Stoch Slowing / MACD Signal
        'InpStochPrice': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Stochastic Price
    }

