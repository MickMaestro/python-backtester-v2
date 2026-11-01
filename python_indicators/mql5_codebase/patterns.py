"""Patterns — converted from MQL5: MQL5 Indicators/Patterns/Patterns.mq5

Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 31, 'indicator_plots': 30}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 5, 11: 5, 12: 5, 13: 5, 14: 5, 15: 5, 16: 5, 17: 5, 18: 5, 19: 5, 20: 5, 21: 5, 22: 5, 23: 5, 24: 5, 25: 5, 26: 5, 27: 5, 28: 5, 29: 5, 30: 5}, 'colors': {1: [255], 2: [255], 3: [255], 4: [255], 5: [255], 6: [255], 7: [255], 8: [255], 9: [255], 10: [255], 11: [255], 12: [255], 13: [255], 14: [255], 15: [255], 16: [255], 17: [255], 18: [255], 19: [255], 20: [255], 21: [255], 22: [255], 23: [255], 24: [255], 25: [255], 26: [255], 27: [255], 28: [255], 29: [255], 30: [255]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0, 25: 0, 26: 0, 27: 0, 28: 0, 29: 0, 30: 0}, 'labels': {1: 'Double inside', 2: 'Inside', 3: 'Outside', 4: 'Pin up', 5: 'Pin down', 6: 'Pivot Point Reversal Up', 7: 'Pivot Point Reversal Down', 8: 'Double Bar Low With A Higher Close', 9: 'Double Bar High With A Lower Close', 10: 'Close Price Reversal Up', 11: 'Close Price Reversal Down', 12: 'Neutral Bar', 13: 'Force Bar Up', 14: 'Force Bar Down', 15: 'Mirror Bar', 16: 'Hammer Pattern', 17: 'Shooting Star', 18: 'Evening Star', 19: 'Morning Star', 20: 'Bearish Harami', 21: 'Bearish Harami Cross', 22: 'Bullish Harami', 23: 'Bullish Harami Cross', 24: 'Dark Cloud Cover', 25: 'Doji Star', 26: 'Engulfing Bearish Line', 27: 'Engulfing Bullish Line', 28: 'Evening Doji Star', 29: 'Morning Doji Star', 30: 'Two Neutral Bars'}, 'levels': [], 'description': [], 'name': 'Patterns', 'source': 'MQL5 Indicators/Patterns/Patterns.mq5', 'folder': 'Patterns', 'inputs': [{'mql': 'InpEnableOneBarPatterns', 'py': 'InpEnableOneBarPatterns', 'param': 'InpEnableOneBarPatterns', 'type': 'int', 'default': 1, 'label': 'Enable One-bar patterns:', 'sinput': False}, {'mql': 'InpEnableTwoBarPatterns', 'py': 'InpEnableTwoBarPatterns', 'param': 'InpEnableTwoBarPatterns', 'type': 'int', 'default': 1, 'label': 'Enable Two-bar patterns:', 'sinput': False}, {'mql': 'InpEnableThreeBarPatterns', 'py': 'InpEnableThreeBarPatterns', 'param': 'InpEnableThreeBarPatterns', 'type': 'int', 'default': 1, 'label': 'Enable Three-bar patterns:', 'sinput': False}, {'mql': 'InpEQ', 'py': 'InpEQ', 'param': 'InpEQ', 'type': 'uint', 'default': 1, 'label': 'Maximum of pips distance between equal prices', 'sinput': False}, {'mql': 'InpShowPatternDescript', 'py': 'InpShowPatternDescript', 'param': 'InpShowPatternDescript', 'type': 'int', 'default': 1, 'label': 'Show Pattern Descriptions', 'sinput': False}, {'mql': 'InpFontSize', 'py': 'InpFontSize', 'param': 'InpFontSize', 'type': 'uint', 'default': 8, 'label': 'Font size', 'sinput': False}, {'mql': 'InpFontColor', 'py': 'InpFontColor', 'param': None, 'type': 'color', 'default': 8421504, 'label': 'Texts color', 'sinput': False}, {'mql': 'InpFontName', 'py': 'InpFontName', 'param': None, 'type': 'string', 'default': 'Calibri', 'label': 'Font name', 'sinput': False}, {'mql': 'InpEnablePAT_DOUBLE_INSIDE', 'py': 'InpEnablePAT_DOUBLE_INSIDE', 'param': 'InpEnablePAT_DOUBLE_INSIDE', 'type': 'int', 'default': 1, 'label': '<Double inside> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_INSIDE', 'py': 'InpEnablePAT_INSIDE', 'param': 'InpEnablePAT_INSIDE', 'type': 'int', 'default': 1, 'label': '<Inside> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_OUTSIDE', 'py': 'InpEnablePAT_OUTSIDE', 'param': 'InpEnablePAT_OUTSIDE', 'type': 'int', 'default': 1, 'label': '<Outside> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_PINUP', 'py': 'InpEnablePAT_PINUP', 'param': 'InpEnablePAT_PINUP', 'type': 'int', 'default': 1, 'label': '<Pin up> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_PINDOWN', 'py': 'InpEnablePAT_PINDOWN', 'param': 'InpEnablePAT_PINDOWN', 'type': 'int', 'default': 1, 'label': '<Pin down> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_PPRUP', 'py': 'InpEnablePAT_PPRUP', 'param': 'InpEnablePAT_PPRUP', 'type': 'int', 'default': 1, 'label': '<Pivot Point Reversal Up> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_PPRDN', 'py': 'InpEnablePAT_PPRDN', 'param': 'InpEnablePAT_PPRDN', 'type': 'int', 'default': 1, 'label': '<Pivot Point Reversal Down> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_DBLHC', 'py': 'InpEnablePAT_DBLHC', 'param': 'InpEnablePAT_DBLHC', 'type': 'int', 'default': 1, 'label': '<Double Bar Low With A Higher Close> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_DBHLC', 'py': 'InpEnablePAT_DBHLC', 'param': 'InpEnablePAT_DBHLC', 'type': 'int', 'default': 1, 'label': '<Double Bar High With A Lower Close> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_CPRU', 'py': 'InpEnablePAT_CPRU', 'param': 'InpEnablePAT_CPRU', 'type': 'int', 'default': 1, 'label': '<Close Price Reversal Up> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_CPRD', 'py': 'InpEnablePAT_CPRD', 'param': 'InpEnablePAT_CPRD', 'type': 'int', 'default': 1, 'label': '<Close Price Reversal Down> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_NB', 'py': 'InpEnablePAT_NB', 'param': 'InpEnablePAT_NB', 'type': 'int', 'default': 1, 'label': '<Neutral Bar> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_FBU', 'py': 'InpEnablePAT_FBU', 'param': 'InpEnablePAT_FBU', 'type': 'int', 'default': 1, 'label': '<Force Bar Up> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_FBD', 'py': 'InpEnablePAT_FBD', 'param': 'InpEnablePAT_FBD', 'type': 'int', 'default': 1, 'label': '<Force Bar Down> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_MB', 'py': 'InpEnablePAT_MB', 'param': 'InpEnablePAT_MB', 'type': 'int', 'default': 1, 'label': '<Mirror Bar> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_HAMMER', 'py': 'InpEnablePAT_HAMMER', 'param': 'InpEnablePAT_HAMMER', 'type': 'int', 'default': 1, 'label': '<Hammer Pattern> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_SHOOTSTAR', 'py': 'InpEnablePAT_SHOOTSTAR', 'param': 'InpEnablePAT_SHOOTSTAR', 'type': 'int', 'default': 1, 'label': '<Shooting Star> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_EVSTAR', 'py': 'InpEnablePAT_EVSTAR', 'param': 'InpEnablePAT_EVSTAR', 'type': 'int', 'default': 1, 'label': '<Evening Star> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_MORNSTAR', 'py': 'InpEnablePAT_MORNSTAR', 'param': 'InpEnablePAT_MORNSTAR', 'type': 'int', 'default': 1, 'label': '<Morning Star> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_BEARHARAMI', 'py': 'InpEnablePAT_BEARHARAMI', 'param': 'InpEnablePAT_BEARHARAMI', 'type': 'int', 'default': 1, 'label': '<Bearish Harami> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_BEARHARAMICROSS', 'py': 'InpEnablePAT_BEARHARAMICROSS', 'param': 'InpEnablePAT_BEARHARAMICROSS', 'type': 'int', 'default': 1, 'label': '<Bearish Harami Cross> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_BULLHARAMI', 'py': 'InpEnablePAT_BULLHARAMI', 'param': 'InpEnablePAT_BULLHARAMI', 'type': 'int', 'default': 1, 'label': '<Bullish Harami> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_BULLHARAMICROSS', 'py': 'InpEnablePAT_BULLHARAMICROSS', 'param': 'InpEnablePAT_BULLHARAMICROSS', 'type': 'int', 'default': 1, 'label': '<Bullish Harami Cross> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_DARKCLOUD', 'py': 'InpEnablePAT_DARKCLOUD', 'param': 'InpEnablePAT_DARKCLOUD', 'type': 'int', 'default': 1, 'label': '<Dark Cloud Cover> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_DOJISTAR', 'py': 'InpEnablePAT_DOJISTAR', 'param': 'InpEnablePAT_DOJISTAR', 'type': 'int', 'default': 1, 'label': '<Doji Star> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_ENGBEARLINE', 'py': 'InpEnablePAT_ENGBEARLINE', 'param': 'InpEnablePAT_ENGBEARLINE', 'type': 'int', 'default': 1, 'label': '<Engulfing Bearish Line> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_ENGBULLLINE', 'py': 'InpEnablePAT_ENGBULLLINE', 'param': 'InpEnablePAT_ENGBULLLINE', 'type': 'int', 'default': 1, 'label': '<Engulfing Bullish Line> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_EVDJSTAR', 'py': 'InpEnablePAT_EVDJSTAR', 'param': 'InpEnablePAT_EVDJSTAR', 'type': 'int', 'default': 1, 'label': '<Evening Doji Star> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_MORNDJSTAR', 'py': 'InpEnablePAT_MORNDJSTAR', 'param': 'InpEnablePAT_MORNDJSTAR', 'type': 'int', 'default': 1, 'label': '<Morning Doji Star> pattern', 'sinput': False}, {'mql': 'InpEnablePAT_NB2', 'py': 'InpEnablePAT_NB2', 'param': 'InpEnablePAT_NB2', 'type': 'int', 'default': 1, 'label': '<Two Neutral Bars> pattern', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_ON_OFF
INPUT_ON = 1
INPUT_OFF = 0
_enum('ENUM_INPUT_ON_OFF', {1: 'INPUT_ON', 0: 'INPUT_OFF'})

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# enum ENUM_PATTERN_TYPE
PATTERN_TYPE_DOUBLE_INSIDE = 0
PATTERN_TYPE_INSIDE = 1
PATTERN_TYPE_OUTSIDE = 2
PATTERN_TYPE_PINUP = 3
PATTERN_TYPE_PINDOWN = 4
PATTERN_TYPE_PPRUP = 5
PATTERN_TYPE_PPRDN = 6
PATTERN_TYPE_DBLHC = 7
PATTERN_TYPE_DBHLC = 8
PATTERN_TYPE_CPRU = 9
PATTERN_TYPE_CPRD = 10
PATTERN_TYPE_NB = 11
PATTERN_TYPE_FBU = 12
PATTERN_TYPE_FBD = 13
PATTERN_TYPE_MB = 14
PATTERN_TYPE_HAMMER = 15
PATTERN_TYPE_SHOOTSTAR = 16
PATTERN_TYPE_EVSTAR = 17
PATTERN_TYPE_MORNSTAR = 18
PATTERN_TYPE_BEARHARAMI = 19
PATTERN_TYPE_BEARHARAMICROSS = 20
PATTERN_TYPE_BULLHARAMI = 21
PATTERN_TYPE_BULLHARAMICROSS = 22
PATTERN_TYPE_DARKCLOUD = 23
PATTERN_TYPE_DOJISTAR = 24
PATTERN_TYPE_ENGBEARLINE = 25
PATTERN_TYPE_ENGBULLLINE = 26
PATTERN_TYPE_EVDJSTAR = 27
PATTERN_TYPE_MORNDJSTAR = 28
PATTERN_TYPE_NB2 = 29
_enum('ENUM_PATTERN_TYPE', {0: 'PATTERN_TYPE_DOUBLE_INSIDE', 1: 'PATTERN_TYPE_INSIDE', 2: 'PATTERN_TYPE_OUTSIDE', 3: 'PATTERN_TYPE_PINUP', 4: 'PATTERN_TYPE_PINDOWN', 5: 'PATTERN_TYPE_PPRUP', 6: 'PATTERN_TYPE_PPRDN', 7: 'PATTERN_TYPE_DBLHC', 8: 'PATTERN_TYPE_DBHLC', 9: 'PATTERN_TYPE_CPRU', 10: 'PATTERN_TYPE_CPRD', 11: 'PATTERN_TYPE_NB', 12: 'PATTERN_TYPE_FBU', 13: 'PATTERN_TYPE_FBD', 14: 'PATTERN_TYPE_MB', 15: 'PATTERN_TYPE_HAMMER', 16: 'PATTERN_TYPE_SHOOTSTAR', 17: 'PATTERN_TYPE_EVSTAR', 18: 'PATTERN_TYPE_MORNSTAR', 19: 'PATTERN_TYPE_BEARHARAMI', 20: 'PATTERN_TYPE_BEARHARAMICROSS', 21: 'PATTERN_TYPE_BULLHARAMI', 22: 'PATTERN_TYPE_BULLHARAMICROSS', 23: 'PATTERN_TYPE_DARKCLOUD', 24: 'PATTERN_TYPE_DOJISTAR', 25: 'PATTERN_TYPE_ENGBEARLINE', 26: 'PATTERN_TYPE_ENGBULLLINE', 27: 'PATTERN_TYPE_EVDJSTAR', 28: 'PATTERN_TYPE_MORNDJSTAR', 29: 'PATTERN_TYPE_NB2'})

# ---- inputs and global variables
BufferATR = Arr(0, 0.0)
InpEnableOneBarPatterns = _input('InpEnableOneBarPatterns', INPUT_ON)  # Enable One-bar patterns:
InpEnableTwoBarPatterns = _input('InpEnableTwoBarPatterns', INPUT_ON)  # Enable Two-bar patterns:
InpEnableThreeBarPatterns = _input('InpEnableThreeBarPatterns', INPUT_ON)  # Enable Three-bar patterns:
InpEQ = _input('InpEQ', 1)  # Maximum of pips distance between equal prices
InpShowPatternDescript = _input('InpShowPatternDescript', INPUT_YES)  # Show Pattern Descriptions
InpFontSize = _input('InpFontSize', 8)  # Font size
InpFontColor = _input('InpFontColor', clrGray)  # Texts color
InpFontName = _input('InpFontName', 'Calibri')  # Font name
InpEnablePAT_DOUBLE_INSIDE = _input('InpEnablePAT_DOUBLE_INSIDE', INPUT_ON)  # <Double inside> pattern
InpEnablePAT_INSIDE = _input('InpEnablePAT_INSIDE', INPUT_ON)  # <Inside> pattern
InpEnablePAT_OUTSIDE = _input('InpEnablePAT_OUTSIDE', INPUT_ON)  # <Outside> pattern
InpEnablePAT_PINUP = _input('InpEnablePAT_PINUP', INPUT_ON)  # <Pin up> pattern
InpEnablePAT_PINDOWN = _input('InpEnablePAT_PINDOWN', INPUT_ON)  # <Pin down> pattern
InpEnablePAT_PPRUP = _input('InpEnablePAT_PPRUP', INPUT_ON)  # <Pivot Point Reversal Up> pattern
InpEnablePAT_PPRDN = _input('InpEnablePAT_PPRDN', INPUT_ON)  # <Pivot Point Reversal Down> pattern
InpEnablePAT_DBLHC = _input('InpEnablePAT_DBLHC', INPUT_ON)  # <Double Bar Low With A Higher Close> pattern
InpEnablePAT_DBHLC = _input('InpEnablePAT_DBHLC', INPUT_ON)  # <Double Bar High With A Lower Close> pattern
InpEnablePAT_CPRU = _input('InpEnablePAT_CPRU', INPUT_ON)  # <Close Price Reversal Up> pattern
InpEnablePAT_CPRD = _input('InpEnablePAT_CPRD', INPUT_ON)  # <Close Price Reversal Down> pattern
InpEnablePAT_NB = _input('InpEnablePAT_NB', INPUT_ON)  # <Neutral Bar> pattern
InpEnablePAT_FBU = _input('InpEnablePAT_FBU', INPUT_ON)  # <Force Bar Up> pattern
InpEnablePAT_FBD = _input('InpEnablePAT_FBD', INPUT_ON)  # <Force Bar Down> pattern
InpEnablePAT_MB = _input('InpEnablePAT_MB', INPUT_ON)  # <Mirror Bar> pattern
InpEnablePAT_HAMMER = _input('InpEnablePAT_HAMMER', INPUT_ON)  # <Hammer Pattern> pattern
InpEnablePAT_SHOOTSTAR = _input('InpEnablePAT_SHOOTSTAR', INPUT_ON)  # <Shooting Star> pattern
InpEnablePAT_EVSTAR = _input('InpEnablePAT_EVSTAR', INPUT_ON)  # <Evening Star> pattern
InpEnablePAT_MORNSTAR = _input('InpEnablePAT_MORNSTAR', INPUT_ON)  # <Morning Star> pattern
InpEnablePAT_BEARHARAMI = _input('InpEnablePAT_BEARHARAMI', INPUT_ON)  # <Bearish Harami> pattern
InpEnablePAT_BEARHARAMICROSS = _input('InpEnablePAT_BEARHARAMICROSS', INPUT_ON)  # <Bearish Harami Cross> pattern
InpEnablePAT_BULLHARAMI = _input('InpEnablePAT_BULLHARAMI', INPUT_ON)  # <Bullish Harami> pattern
InpEnablePAT_BULLHARAMICROSS = _input('InpEnablePAT_BULLHARAMICROSS', INPUT_ON)  # <Bullish Harami Cross> pattern
InpEnablePAT_DARKCLOUD = _input('InpEnablePAT_DARKCLOUD', INPUT_ON)  # <Dark Cloud Cover> pattern
InpEnablePAT_DOJISTAR = _input('InpEnablePAT_DOJISTAR', INPUT_ON)  # <Doji Star> pattern
InpEnablePAT_ENGBEARLINE = _input('InpEnablePAT_ENGBEARLINE', INPUT_ON)  # <Engulfing Bearish Line> pattern
InpEnablePAT_ENGBULLLINE = _input('InpEnablePAT_ENGBULLLINE', INPUT_ON)  # <Engulfing Bullish Line> pattern
InpEnablePAT_EVDJSTAR = _input('InpEnablePAT_EVDJSTAR', INPUT_ON)  # <Evening Doji Star> pattern
InpEnablePAT_MORNDJSTAR = _input('InpEnablePAT_MORNDJSTAR', INPUT_ON)  # <Morning Doji Star> pattern
InpEnablePAT_NB2 = _input('InpEnablePAT_NB2', INPUT_ON)  # <Two Neutral Bars> pattern
handle_atr = 0
eq_pp = 0.0
prefix = ""
font_name = ""
ArrayNames = Arr.of([['Double inside', 'DBLIN'], ['Inside Bar', 'IN'], ['Outside Bar', 'OUT'], ['Pin Bar up', 'PINUP'], ['Pin Bar down', 'PINDOWN'], ['Pivot Point Reversal Up', 'PPRUP'], ['Pivot Point Reversal Down', 'PPRDN'], ['Double Bar Low With A Higher Close', 'DBLHC'], ['Double Bar High With A Lower Close', 'DBHLC'], ['Close Price Reversal Up', 'CPRU'], ['Close Price Reversal Down', 'CPRD'], ['Neutral Bar', 'NB'], ['Force Bar Up', 'FBU'], ['Force Bar Down', 'FBD'], ['Mirror Bar', 'MB'], ['Hammer', 'HAMMER'], ['Shooting Star', 'SHOOTSTAR'], ['Evening Star', 'EVSTAR'], ['Morning Star', 'MORNSTAR'], ['Bearish Harami', 'BEARHARAMI'], ['Bearish Harami Cross', 'BEARHARAMICROSS'], ['Bullish Harami', 'BULLHARAMI'], ['Bullish Harami Cross', 'BULLHARAMICROSS'], ['Dark Cloud Cover', 'DARKCLOUD'], ['Doji Star', 'DOJISTAR'], ['Engulfing Bearish Line', 'ENGBEARLINE'], ['Engulfing Bullish Line', 'ENGBULLLINE'], ['Evening Doji Star', 'EVDJSTAR'], ['Morning Doji Star', 'MORNDJSTAR'], ['Two Neutral Bars', 'NB2']], fill="", dims=(2,))

class SDataBuffers(MqlObject):
    _q_fields = ('Buffer', 'type_pattern')
    def __init__(self, *args):
        self.Buffer = Arr(0, 0.0)
        self.type_pattern = 0
    def Description(self):
        return DescriptionPattern_2(self.type_pattern)

def OnInit():
    global eq_pp, font_name, handle_atr, prefix
    if Point() == 0:
        Print('Error. Unable to get the value of points on ', Symbol())
        return INIT_FAILED
    eq_pp = InpEQ * Point()
    prefix = 'Patterns_'
    font_name = ('Calibri' if (InpFontName == '') else InpFontName)
    ArraySetAsSeries(BufferATR, True)
    total = ArrayRange(ArrayNames, 0)
    ArrayResize(Pattern, total)
    ZeroMemory(Pattern)
    for i in range(0, total):
        SetIndexBuffer(i, Pattern[i].Buffer, INDICATOR_DATA)
        PlotIndexSetInteger(i, PLOT_ARROW, 159)
        Pattern[i].type_pattern = i
        ArraySetAsSeries(Pattern[i].Buffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Patterns')
    ResetLastError()
    handle_atr = iATR(Symbol(), PERIOD_CURRENT, 14)
    if handle_atr == INVALID_HANDLE:
        Print('The iATR object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, prefix)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 4:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 5
        total = ArraySize(Pattern)
        for i in range(0, total):
            ArrayInitialize(Pattern[i].Buffer, EMPTY_VALUE)
    copied = 0
    count = (1 if (limit == 0) else rates_total)
    copied = CopyBuffer(handle_atr, 0, 0, count, BufferATR)
    if copied != count:
        return 0
    for i in range(limit, 0, -1):
        CheckPatterns(i, open, high, low, close, time)
    return rates_total

def CheckPatterns(index, open, high, low, close, time):
    total = ArraySize(Pattern)
    for i in range(0, total):
        Pattern[i].Buffer[index] = EMPTY_VALUE
    min_dev = fmax(eq_pp, Point())
    min_dev4 = fmax(eq_pp * 4, Point() * 4)
    open_0 = open[index]
    close_0 = close[index]
    low_0 = low[index]
    high_0 = high[index]
    body_top_0 = fmax(open_0, close_0)
    body_bottom_0 = fmin(open_0, close_0)
    body_size_0 = body_top_0 - body_bottom_0
    shadow_upper_0 = high_0 - body_top_0
    shadow_lower_0 = body_bottom_0 - low_0
    open_1 = open[index + 1]
    close_1 = close[index + 1]
    low_1 = low[index + 1]
    high_1 = high[index + 1]
    body_top_1 = fmax(open_1, close_1)
    body_bottom_1 = fmin(open_1, close_1)
    body_size_1 = body_top_1 - body_bottom_1
    shadow_upper_1 = high_1 - body_top_1
    shadow_lower_1 = body_bottom_1 - low_1
    open_2 = open[index + 2]
    close_2 = close[index + 2]
    low_2 = low[index + 2]
    high_2 = high[index + 2]
    body_top_2 = fmax(open_2, close_2)
    body_bottom_2 = fmin(open_2, close_2)
    body_size_2 = body_top_2 - body_bottom_2
    shadow_upper_2 = high_2 - body_top_2
    shadow_lower_2 = body_bottom_2 - low_2
    if InpEnableOneBarPatterns:
        if (Cmp(open_0, close_0) == 0 and shadow_upper_0 > min_dev4) and shadow_lower_0 > min_dev4:
            if InpEnablePAT_NB:
                DrawPattern(index, PATTERN_TYPE_NB, high, low, time)
        if close_0 == high_0:
            if InpEnablePAT_FBU:
                DrawPattern(index, PATTERN_TYPE_FBU, high, low, time)
        if close_0 == low_0:
            if InpEnablePAT_FBD:
                DrawPattern(index, PATTERN_TYPE_FBD, high, low, time)
        if shadow_upper_0 <= min_dev and shadow_lower_0 > (2 * body_size_0):
            if InpEnablePAT_HAMMER:
                DrawPattern(index, PATTERN_TYPE_HAMMER, high, low, time)
        if shadow_lower_0 <= min_dev and shadow_upper_0 > (2 * body_size_0):
            if InpEnablePAT_SHOOTSTAR:
                DrawPattern(index, PATTERN_TYPE_SHOOTSTAR, high, low, time)
    if InpEnableTwoBarPatterns:
        if Cmp(high_0, high_1) < 0 and Cmp(low_0, low_1) > 0:
            if InpEnablePAT_INSIDE:
                DrawPattern(index, PATTERN_TYPE_INSIDE, high, low, time)
        if Cmp(high_0, high_1) > 0 and Cmp(low_0, low_1) < 0:
            if InpEnablePAT_OUTSIDE:
                DrawPattern(index, PATTERN_TYPE_OUTSIDE, high, low, time)
        if (Cmp(high_0, high_1) == 0 and Cmp(close_0, close_1) < 0) and Cmp(low_0, low_1) <= 0:
            if InpEnablePAT_DBHLC:
                DrawPattern(index, PATTERN_TYPE_DBHLC, high, low, time)
        if (Cmp(low_0, low_1) == 0 and Cmp(close_0, close_1) > 0) and Cmp(high_0, high_1) >= 0:
            if InpEnablePAT_DBLHC:
                DrawPattern(index, PATTERN_TYPE_DBLHC, high, low, time)
        if Cmp(body_size_1, body_size_0) == 0 and Cmp(open_1, close_0) == 0:
            if InpEnablePAT_MB:
                DrawPattern(index, PATTERN_TYPE_MB, high, low, time)
        if (((((Cmp(high_0, high_1) < 0 and Cmp(low_0, low_1) > 0) and Cmp(close_1, open_1) > 0) and Cmp(close_0, open_0) < 0) and Cmp(body_size_1, body_size_0) > 0) and Cmp(close_1, open_0) > 0) and Cmp(open_1, close_0) < 0:
            if InpEnablePAT_BEARHARAMI:
                DrawPattern(index, PATTERN_TYPE_BEARHARAMI, high, low, time)
        if (((((Cmp(high_0, high_1) < 0 and Cmp(low_0, low_1) > 0) and Cmp(close_1, open_1) > 0) and Cmp(open_0, close_0) == 0) and Cmp(body_size_1, body_size_0) > 0) and Cmp(close_1, open_0) > 0) and Cmp(open_1, close_0) < 0:
            if InpEnablePAT_BEARHARAMICROSS:
                DrawPattern(index, PATTERN_TYPE_BEARHARAMICROSS, high, low, time)
        if (((((Cmp(high_0, high_1) < 0 and Cmp(low_0, low_1) > 0) and Cmp(close_1, open_1) < 0) and Cmp(close_0, open_0) > 0) and Cmp(body_size_1, body_size_0) > 0) and Cmp(close_1, open_0) < 0) and Cmp(open_1, close_0) > 0:
            if InpEnablePAT_BULLHARAMI:
                DrawPattern(index, PATTERN_TYPE_BULLHARAMI, high, low, time)
        if (((((Cmp(high_0, high_1) < 0 and Cmp(low_0, low_1) > 0) and Cmp(close_1, open_1) < 0) and Cmp(open_0, close_0) == 0) and Cmp(body_size_1, body_size_0) > 0) and Cmp(close_1, open_0) < 0) and Cmp(open_1, close_0) > 0:
            if InpEnablePAT_BULLHARAMICROSS:
                DrawPattern(index, PATTERN_TYPE_BULLHARAMICROSS, high, low, time)
        if (((Cmp(close_1, open_1) > 0 and Cmp(close_0, open_0) < 0) and Cmp(high_1, open_0) < 0) and Cmp(close_0, close_1) < 0) and Cmp(close_0, open_1) > 0:
            if InpEnablePAT_DARKCLOUD:
                DrawPattern(index, PATTERN_TYPE_DARKCLOUD, high, low, time)
        if (((Cmp(open_0, close_0) == 0 and Cmp(close_1, open_1) > 0) and Cmp(open_0, high_1) > 0) and Cmp(close_1, open_1) < 0) and Cmp(open_0, low_1) < 0:
            if InpEnablePAT_DOJISTAR:
                DrawPattern(index, PATTERN_TYPE_DOJISTAR, high, low, time)
        if ((Cmp(close_1, open_1) > 0 and Cmp(close_0, open_0) < 0) and Cmp(open_0, close_1) > 0) and Cmp(close_0, open_1) < 0:
            if InpEnablePAT_ENGBEARLINE:
                DrawPattern(index, PATTERN_TYPE_ENGBEARLINE, high, low, time)
        if ((Cmp(close_1, open_1) < 0 and Cmp(close_0, open_0) > 0) and Cmp(open_0, close_1) < 0) and Cmp(close_0, open_1) > 0:
            if InpEnablePAT_ENGBULLLINE:
                DrawPattern(index, PATTERN_TYPE_ENGBULLLINE, high, low, time)
        if ((((Cmp(open_0, close_0) == 0 and shadow_upper_0 > min_dev4) and shadow_lower_0 > min_dev4) and Cmp(open_1, close_1) == 0) and shadow_upper_1 > min_dev4) and shadow_lower_1 > min_dev4:
            if InpEnablePAT_NB2:
                DrawPattern(index, PATTERN_TYPE_NB2, high, low, time)
    if InpEnableThreeBarPatterns:
        if ((Cmp(high_0, high_1) < 0 and Cmp(low_0, low_1) > 0) and Cmp(high_1, high_2) < 0) and Cmp(low_1, low_2) > 0:
            if InpEnablePAT_DOUBLE_INSIDE:
                DrawPattern(index, PATTERN_TYPE_DOUBLE_INSIDE, high, low, time)
        if (((Cmp(high_1, high_2) > 0 and Cmp(high_1, high_0) > 0) and Cmp(low_1, low_2) > 0) and Cmp(low_1, low_0) > 0) and (body_size_1 * 2) < shadow_upper_1:
            if InpEnablePAT_PINUP:
                DrawPattern(index, PATTERN_TYPE_PINUP, high, low, time)
        if (((Cmp(high_1, high_2) < 0 and Cmp(high_1, high_0) < 0) and Cmp(low_1, low_2) < 0) and Cmp(low_1, low_0) < 0) and (body_size_1 * 2) < shadow_lower_1:
            if InpEnablePAT_PINDOWN:
                DrawPattern(index, PATTERN_TYPE_PINDOWN, high, low, time)
        if (((Cmp(high_1, high_2) > 0 and Cmp(high_1, high_0) > 0) and Cmp(low_1, low_2) > 0) and Cmp(low_1, low_0) > 0) and Cmp(close_0, low_1) < 0:
            if InpEnablePAT_PPRDN:
                DrawPattern(index, PATTERN_TYPE_PPRDN, high, low, time)
        if (((Cmp(high_1, high_2) < 0 and Cmp(high_1, high_0) < 0) and Cmp(low_1, low_2) < 0) and Cmp(low_1, low_0) < 0) and Cmp(close_0, high_1) > 0:
            if InpEnablePAT_PPRUP:
                DrawPattern(index, PATTERN_TYPE_PPRUP, high, low, time)
        if ((((Cmp(high_1, high_2) < 0 and Cmp(low_1, low_2) < 0) and Cmp(high_0, high_1) < 0) and Cmp(low_0, low_1) < 0) and Cmp(close_0, close_1) > 0) and Cmp(open_0, close_0) < 0:
            if InpEnablePAT_CPRU:
                DrawPattern(index, PATTERN_TYPE_CPRU, high, low, time)
        if ((((Cmp(high_1, high_2) > 0 and Cmp(low_1, low_2) > 0) and Cmp(high_0, high_1) > 0) and Cmp(low_0, low_1) > 0) and Cmp(close_0, close_1) < 0) and Cmp(open_0, close_0) > 0:
            if InpEnablePAT_CPRD:
                DrawPattern(index, PATTERN_TYPE_CPRD, high, low, time)
        if ((((((Cmp(close_2, open_2) > 0 and Cmp(close_1, open_1) > 0) and Cmp(close_0, open_0) < 0) and Cmp(close_2, open_1) < 0) and Cmp(body_size_2, body_size_1) > 0) and Cmp(body_size_1, body_size_0) < 0) and Cmp(close_0, open_2) > 0) and Cmp(close_0, close_2) < 0:
            if InpEnablePAT_EVSTAR:
                DrawPattern(index, PATTERN_TYPE_EVSTAR, high, low, time)
        if ((((((Cmp(close_2, open_2) < 0 and Cmp(close_1, open_1) > 0) and Cmp(close_0, open_0) > 0) and Cmp(close_2, open_1) > 0) and Cmp(body_size_2, body_size_1) > 0) and Cmp(body_size_1, body_size_0) < 0) and Cmp(close_0, close_2) > 0) and Cmp(close_0, open_2) < 0:
            if InpEnablePAT_MORNSTAR:
                DrawPattern(index, PATTERN_TYPE_MORNSTAR, high, low, time)
        if ((((((Cmp(close_2, open_2) > 0 and Cmp(close_1, open_1) == 0) and Cmp(close_0, open_0) < 0) and Cmp(close_2, open_1) < 0) and Cmp(body_size_2, body_size_1) > 0) and Cmp(body_size_1, body_size_0) < 0) and Cmp(close_0, open_2) > 0) and Cmp(close_0, close_2) < 0:
            if InpEnablePAT_EVDJSTAR:
                DrawPattern(index, PATTERN_TYPE_EVDJSTAR, high, low, time)
        if ((((((Cmp(close_2, open_2) < 0 and Cmp(close_1, open_1) == 0) and Cmp(close_0, open_0) > 0) and Cmp(close_2, open_1) > 0) and Cmp(body_size_2, body_size_1) > 0) and Cmp(body_size_1, body_size_0) < 0) and Cmp(close_0, close_2) > 0) and Cmp(close_0, open_2) < 0:
            if InpEnablePAT_MORNDJSTAR:
                DrawPattern(index, PATTERN_TYPE_MORNDJSTAR, high, low, time)

def DrawPattern(index, pattern_type, high, low, time):
    up = True
    length = 1
    price = 0.0
    if pattern_type == PATTERN_TYPE_NB:
        up = True
        length = 1
    if pattern_type == PATTERN_TYPE_FBU:
        up = False
        length = 1
    if pattern_type == PATTERN_TYPE_FBD:
        up = True
        length = 1
    if pattern_type == PATTERN_TYPE_HAMMER:
        up = True
        length = 1
    if pattern_type == PATTERN_TYPE_SHOOTSTAR:
        up = True
        length = 1
    if pattern_type == PATTERN_TYPE_INSIDE:
        up = True
        length = 2
    if pattern_type == PATTERN_TYPE_OUTSIDE:
        up = True
        length = 2
    if pattern_type == PATTERN_TYPE_DBHLC:
        up = True
        length = 2
    if pattern_type == PATTERN_TYPE_DBLHC:
        up = False
        length = 2
    if pattern_type == PATTERN_TYPE_MB:
        up = True
        length = 2
    if pattern_type == PATTERN_TYPE_BEARHARAMI:
        up = True
        length = 2
    if pattern_type == PATTERN_TYPE_BEARHARAMICROSS:
        up = True
        length = 2
    if pattern_type == PATTERN_TYPE_BULLHARAMI:
        up = True
        length = 2
    if pattern_type == PATTERN_TYPE_BULLHARAMICROSS:
        up = True
        length = 2
    if pattern_type == PATTERN_TYPE_DARKCLOUD:
        up = True
        length = 2
    if pattern_type == PATTERN_TYPE_DOJISTAR:
        up = True
        length = 2
    if pattern_type == PATTERN_TYPE_ENGBEARLINE:
        up = True
        length = 2
    if pattern_type == PATTERN_TYPE_ENGBULLLINE:
        up = True
        length = 2
    if pattern_type == PATTERN_TYPE_NB2:
        up = True
        length = 2
    if pattern_type == PATTERN_TYPE_DOUBLE_INSIDE:
        up = True
        length = 3
    if pattern_type == PATTERN_TYPE_PINUP:
        up = True
        length = 3
    if pattern_type == PATTERN_TYPE_PINDOWN:
        up = False
        length = 3
    if pattern_type == PATTERN_TYPE_PPRDN:
        up = True
        length = 3
    if pattern_type == PATTERN_TYPE_PPRUP:
        up = False
        length = 3
    if pattern_type == PATTERN_TYPE_CPRU:
        up = False
        length = 3
    if pattern_type == PATTERN_TYPE_CPRD:
        up = True
        length = 3
    if pattern_type == PATTERN_TYPE_EVSTAR:
        up = True
        length = 3
    if pattern_type == PATTERN_TYPE_MORNSTAR:
        up = True
        length = 3
    if pattern_type == PATTERN_TYPE_EVDJSTAR:
        up = True
        length = 3
    if pattern_type == PATTERN_TYPE_MORNDJSTAR:
        up = True
        length = 3
    price = ((high[Highest("", PERIOD_CURRENT, length, index)] + BufferATR[index]) if up else (low[Lowest("", PERIOD_CURRENT, length, index)] - BufferATR[index]))
    Pattern[pattern_type].Buffer[index] = price
    Pattern[pattern_type].type_pattern = pattern_type
    if InpShowPatternDescript:
        DrawLabel(pattern_type, price, index, high, low, time, up)

def DrawLabel(type_pattern, price, index, high, low, time, upper):
    tm = TimeToString(time[index])
    name = prefix + DescrShortPattern_2(type_pattern) + '_' + _str(index) + '_' + tm
    ObjectCreate(0, name, OBJ_TEXT, 0, time[index], price)
    ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
    ObjectSetString(0, name, OBJPROP_TEXT, DescriptionPattern_2(type_pattern))
    ObjectSetInteger(0, name, OBJPROP_FONTSIZE, InpFontSize)
    ObjectSetString(0, name, OBJPROP_FONT, font_name)
    ObjectSetInteger(0, name, OBJPROP_COLOR, InpFontColor)
    ObjectSetString(0, name, OBJPROP_TOOLTIP, 'Pattern on ' + NameTimeframe() + ':\n' + DescriptionPattern_2(type_pattern) + '\n' + tm)
    ObjectSetInteger(0, name, OBJPROP_ANCHOR, (ANCHOR_LEFT_LOWER if upper else ANCHOR_LEFT_UPPER))
    name = prefix + DescrShortPattern_2(type_pattern) + '_vl_' + _str(index) + '_' + tm
    ObjectCreate(0, name, OBJ_TREND, 0, 0, 0, 0, 0)
    ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, name, OBJPROP_COLOR, clrRed)
    ObjectSetInteger(0, name, OBJPROP_WIDTH, 0)
    ObjectSetInteger(0, name, OBJPROP_STYLE, STYLE_DOT)
    ObjectSetInteger(0, name, OBJPROP_RAY, False)
    ObjectSetString(0, name, OBJPROP_TOOLTIP, '\n')
    ObjectSetInteger(0, name, OBJPROP_TIME, 0, time[index])
    ObjectSetInteger(0, name, OBJPROP_TIME, 1, time[index])
    ObjectSetDouble(0, name, OBJPROP_PRICE, 0, (high[index] if upper else low[index]))
    ObjectSetDouble(0, name, OBJPROP_PRICE, 1, price)

def DescriptionPattern_1(index):
    return ArrayNames[index][0]

def DescriptionPattern_2(pattern):
    return ArrayNames[pattern][0]

def DescrShortPattern_1(index):
    return ArrayNames[index][1]

def DescrShortPattern_2(pattern):
    return ArrayNames[pattern][1]

def Highest(symbol_name, timeframe, count, start):
    symb = (Symbol() if (symbol_name == "" or symbol_name == '') else symbol_name)
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyHigh(symb, timeframe, start, count, array) == count:
        return ArrayMaximum(array) + start
    return WRONG_VALUE

def Lowest(symbol_name, timeframe, count, start):
    symb = (Symbol() if (symbol_name == "" or symbol_name == '') else symbol_name)
    array = Arr(0, 0.0)
    ArraySetAsSeries(array, True)
    if CopyLow(symb, timeframe, start, count, array) == count:
        return ArrayMinimum(array) + start
    return WRONG_VALUE

def Cmp(price1, price2):
    return (0 if (fabs(price1 - price2) < eq_pp) else 1 if (price1 > price2) else -1)

def NameTimeframe(timeframe=PERIOD_CURRENT):
    if timeframe == PERIOD_CURRENT:
        timeframe = Period()
    _sw1 = timeframe
    if _sw1 == 1:
        return 'M1'
    elif _sw1 == 2:
        return 'M2'
    elif _sw1 == 3:
        return 'M3'
    elif _sw1 == 4:
        return 'M4'
    elif _sw1 == 5:
        return 'M5'
    elif _sw1 == 6:
        return 'M6'
    elif _sw1 == 10:
        return 'M10'
    elif _sw1 == 12:
        return 'M12'
    elif _sw1 == 15:
        return 'M15'
    elif _sw1 == 20:
        return 'M20'
    elif _sw1 == 30:
        return 'M30'
    elif _sw1 == 16385:
        return 'H1'
    elif _sw1 == 16386:
        return 'H2'
    elif _sw1 == 16387:
        return 'H3'
    elif _sw1 == 16388:
        return 'H4'
    elif _sw1 == 16390:
        return 'H6'
    elif _sw1 == 16392:
        return 'H8'
    elif _sw1 == 16396:
        return 'H12'
    elif _sw1 == 16408:
        return 'D1'
    elif _sw1 == 32769:
        return 'W1'
    elif _sw1 == 49153:
        return 'MN1'
    else:
        return _str(Period())

# ---- global variables initialised from expressions
Pattern = Arr(0, 0, factory=SDataBuffers)  # Структура данных паттернов


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Patterns(_MQL5Indicator):
    name = 'Patterns'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpEnableOneBarPatterns': _Choice({1: 'On', 0: 'Off'}, default=1),  # Enable One-bar patterns:
        'InpEnableTwoBarPatterns': _Choice({1: 'On', 0: 'Off'}, default=1),  # Enable Two-bar patterns:
        'InpEnableThreeBarPatterns': _Choice({1: 'On', 0: 'Off'}, default=1),  # Enable Three-bar patterns:
        'InpEQ': 1,  # Maximum of pips distance between equal prices
        'InpShowPatternDescript': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show Pattern Descriptions
        'InpFontSize': 8,  # Font size
        'InpEnablePAT_DOUBLE_INSIDE': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Double inside> pattern
        'InpEnablePAT_INSIDE': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Inside> pattern
        'InpEnablePAT_OUTSIDE': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Outside> pattern
        'InpEnablePAT_PINUP': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Pin up> pattern
        'InpEnablePAT_PINDOWN': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Pin down> pattern
        'InpEnablePAT_PPRUP': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Pivot Point Reversal Up> pattern
        'InpEnablePAT_PPRDN': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Pivot Point Reversal Down> pattern
        'InpEnablePAT_DBLHC': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Double Bar Low With A Higher Close> pattern
        'InpEnablePAT_DBHLC': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Double Bar High With A Lower Close> pattern
        'InpEnablePAT_CPRU': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Close Price Reversal Up> pattern
        'InpEnablePAT_CPRD': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Close Price Reversal Down> pattern
        'InpEnablePAT_NB': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Neutral Bar> pattern
        'InpEnablePAT_FBU': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Force Bar Up> pattern
        'InpEnablePAT_FBD': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Force Bar Down> pattern
        'InpEnablePAT_MB': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Mirror Bar> pattern
        'InpEnablePAT_HAMMER': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Hammer Pattern> pattern
        'InpEnablePAT_SHOOTSTAR': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Shooting Star> pattern
        'InpEnablePAT_EVSTAR': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Evening Star> pattern
        'InpEnablePAT_MORNSTAR': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Morning Star> pattern
        'InpEnablePAT_BEARHARAMI': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Bearish Harami> pattern
        'InpEnablePAT_BEARHARAMICROSS': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Bearish Harami Cross> pattern
        'InpEnablePAT_BULLHARAMI': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Bullish Harami> pattern
        'InpEnablePAT_BULLHARAMICROSS': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Bullish Harami Cross> pattern
        'InpEnablePAT_DARKCLOUD': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Dark Cloud Cover> pattern
        'InpEnablePAT_DOJISTAR': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Doji Star> pattern
        'InpEnablePAT_ENGBEARLINE': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Engulfing Bearish Line> pattern
        'InpEnablePAT_ENGBULLLINE': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Engulfing Bullish Line> pattern
        'InpEnablePAT_EVDJSTAR': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Evening Doji Star> pattern
        'InpEnablePAT_MORNDJSTAR': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Morning Doji Star> pattern
        'InpEnablePAT_NB2': _Choice({1: 'On', 0: 'Off'}, default=1),  # <Two Neutral Bars> pattern
    }

