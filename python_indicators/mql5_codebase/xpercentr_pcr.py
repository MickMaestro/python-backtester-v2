"""xpercentr-pcr — converted from MQL5: MQL5 Indicators/XPercentR-PCR/xpercentr-pcr.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [8421376, 9639167]}, 'widths': {}, 'styles': {}, 'labels': {1: 'XPercentR-PCR'}, 'levels': [], 'description': [], 'name': 'xpercentr-pcr', 'source': 'MQL5 Indicators/XPercentR-PCR/xpercentr-pcr.mq5', 'folder': 'XPercentR-PCR', 'inputs': [{'mql': 'HL_Period', 'py': 'HL_Period', 'param': 'HL_Period', 'type': 'uint', 'default': 55, 'label': '', 'sinput': False}, {'mql': 'SmoothMethod', 'py': 'SmoothMethod', 'param': 'SmoothMethod', 'type': 'int', 'default': 4, 'label': 'smoothing method', 'sinput': False}, {'mql': 'SmoothLength', 'py': 'SmoothLength', 'param': 'SmoothLength', 'type': 'uint', 'default': 3, 'label': 'smoothing depth', 'sinput': False}, {'mql': 'SmoothPhase', 'py': 'SmoothPhase', 'param': 'SmoothPhase', 'type': 'int', 'default': 100, 'label': 'smoothing parameter,', 'sinput': False}, {'mql': 'UpLevel', 'py': 'UpLevel', 'param': 'UpLevel', 'type': 'uint', 'default': 80, 'label': 'overbought level', 'sinput': False}, {'mql': 'DnLevel', 'py': 'DnLevel', 'param': 'DnLevel', 'type': 'uint', 'default': 20, 'label': 'oversold level', 'sinput': False}, {'mql': 'UpLevelsColor', 'py': 'UpLevelsColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'overbought level color', 'sinput': False}, {'mql': 'DnLevelsColor', 'py': 'DnLevelsColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'oversold level color', 'sinput': False}, {'mql': 'Levelstyle', 'py': 'Levelstyle', 'param': 'Levelstyle', 'type': 'int', 'default': 1, 'label': 'levels style', 'sinput': False}, {'mql': 'LevelsWidth', 'py': 'LevelsWidth', 'param': 'LevelsWidth', 'type': 'int', 'default': 1, 'label': 'levels width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

Purple = 0x800080  # MQL4 colour name

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# enum WIDTH
Width_1 = 1
Width_2 = 2
Width_3 = 3
Width_4 = 4
Width_5 = 5
_enum('WIDTH', {1: 'Width_1', 2: 'Width_2', 3: 'Width_3', 4: 'Width_4', 5: 'Width_5'})

# enum STYLE
SOLID_ = 0
DASH_ = 1
DOT_ = 2
DASHDOT_ = 3
DASHDOTDOT_ = 4
_enum('STYLE', {0: 'SOLID_', 1: 'DASH_', 2: 'DOT_', 3: 'DASHDOT_', 4: 'DASHDOTDOT_'})

# ---- inputs and global variables
HL_Period = _input('HL_Period', 55)
SmoothMethod = _input('SmoothMethod', MODE_JJMA)  # smoothing method
SmoothLength = _input('SmoothLength', 3)  # smoothing depth
SmoothPhase = _input('SmoothPhase', 100)  # smoothing parameter,
UpLevel = _input('UpLevel', 80)  # overbought level
DnLevel = _input('DnLevel', 20)  # oversold level
Levelstyle = _input('Levelstyle', DASH_)  # levels style
LevelsWidth = _input('LevelsWidth', Width_1)  # levels width
BullsBuffer = Arr(0, 0.0)
BearsBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_ = 0

def OnInit():
    global min_rates_, min_rates_total
    UpXMA.XMALengthCheck('SmoothLength', SmoothLength)
    UpXMA.XMAPhaseCheck('SmoothPhase', SmoothPhase, SmoothMethod)
    min_rates_ = _int(HL_Period)
    min_rates_total = min_rates_ + UpXMA.GetStartBars(SmoothMethod, SmoothLength, SmoothPhase)
    SetIndexBuffer(0, BullsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(BullsBuffer, True)
    SetIndexBuffer(1, BearsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(BearsBuffer, True)
    shortname = 'XPercentR-PCRA'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, UpLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, UpLevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, Levelstyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 0, LevelsWidth)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, DnLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, DnLevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, Levelstyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 1, LevelsWidth)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    bar1 = 0
    maxbar = 0
    h = 0.0
    l = 0.0
    p = 0.0
    Up = 0.0
    Dn = 0.0
    d = 0.0
    maxbar = rates_total - 1 - min_rates_
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        bar1 = bar + 1
        p = close[bar]
        h = high[ArrayMaximum(high, bar1, HL_Period)]
        l = low[ArrayMinimum(low, bar1, HL_Period)]
        d = h - l
        if d:
            Dn = _fdiv(h - p, d) * 100
            Up = _fdiv(p - l, d) * 100
        else:
            Up = 0.0
            Dn = 0.0
        BullsBuffer[bar] = UpXMA.XMASeries(maxbar, prev_calculated, rates_total, SmoothMethod, SmoothPhase, SmoothLength, Up, bar, True)
        BearsBuffer[bar] = DnXMA.XMASeries(maxbar, prev_calculated, rates_total, SmoothMethod, SmoothPhase, SmoothLength, Dn, bar, True)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
UpXMA = _alloc(CXMA)
UpXMA.__init__()
DnXMA = _alloc(CXMA)
DnXMA.__init__()
UpLevelsColor = _input('UpLevelsColor', _uint(Purple))  # overbought level color
DnLevelsColor = _input('DnLevelsColor', _uint(Purple))  # oversold level color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XpercentrPcr(_MQL5Indicator):
    name = 'xpercentr-pcr'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'HL_Period': 55,
        'SmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # smoothing method
        'SmoothLength': 3,  # smoothing depth
        'SmoothPhase': 100,  # smoothing parameter,
        'UpLevel': 80,  # overbought level
        'DnLevel': 20,  # oversold level
        'Levelstyle': _Choice({0: 'Solid line', 1: 'Dashed line', 2: 'Dotted line', 3: 'Dot-dash line', 4: 'Dot-dash line with double dots'}, default=1),  # levels style
        'LevelsWidth': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # levels width
    }

