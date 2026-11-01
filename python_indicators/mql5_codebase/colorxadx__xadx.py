"""colorxadx — converted from MQL5: MQL5 Indicators/XADX/colorxadx.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 12}, 'colors': {1: [65280, 255], 2: [8421504], 3: [8421504, 16711680, 16711935, 255]}, 'widths': {2: 1, 3: 3}, 'styles': {2: 0, 3: 0}, 'labels': {1: 'XDi', 2: 'XADX Line', 3: 'XADX'}, 'levels': [], 'description': [], 'name': 'colorxadx', 'source': 'MQL5 Indicators/XADX/colorxadx.mq5', 'folder': 'XADX', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 7, 'label': 'Histogram smoothing method', 'sinput': False}, {'mql': 'ADX_Period', 'py': 'ADX_Period', 'param': 'ADX_Period', 'type': 'int', 'default': 14, 'label': 'XMA smoothing period', 'sinput': False}, {'mql': 'ADX_Phase', 'py': 'ADX_Phase', 'param': 'ADX_Phase', 'type': 'int', 'default': 100, 'label': 'XMA smoothing period [-100...+100]', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'ExtraHighLevel', 'py': 'ExtraHighLevel', 'param': 'ExtraHighLevel', 'type': 'int', 'default': 60, 'label': 'Maximum trend level', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 40, 'label': 'Strong trend level', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': 20, 'label': 'Weak trend level', 'sinput': False}, {'mql': 'LevelStyle', 'py': 'LevelStyle', 'param': 'LevelStyle', 'type': 'int', 'default': 4, 'label': 'Levels lines style', 'sinput': False}, {'mql': 'LevelColor', 'py': 'LevelColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Levels color', 'sinput': False}, {'mql': 'LevelWidth', 'py': 'LevelWidth', 'param': 'LevelWidth', 'type': 'int', 'default': 1, 'label': 'Levels width', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

Blue = 0xFF0000  # MQL4 colour name

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# enum ENUM_WIDTH
w_1 = 1
w_2 = 2
w_3 = 3
w_4 = 4
w_5 = 5
_enum('ENUM_WIDTH', {1: 'w_1', 2: 'w_2', 3: 'w_3', 4: 'w_4', 5: 'w_5'})

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_T3)  # Histogram smoothing method
ADX_Period = _input('ADX_Period', 14)  # XMA smoothing period
ADX_Phase = _input('ADX_Phase', 100)  # XMA smoothing period [-100...+100]
IPC = _input('IPC', PRICE_CLOSE_)  # Applied price
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
ExtraHighLevel = _input('ExtraHighLevel', 60)  # Maximum trend level
HighLevel = _input('HighLevel', 40)  # Strong trend level
LowLevel = _input('LowLevel', 20)  # Weak trend level
LevelStyle = _input('LevelStyle', STYLE_DASHDOTDOT)  # Levels lines style
LevelWidth = _input('LevelWidth', w_1)  # Levels width
DiPlusBuffer = Arr(0, 0.0)
DiMinusBuffer = Arr(0, 0.0)
ADXBuffer = Arr(0, 0.0)
ADXLineBuffer = Arr(0, 0.0)
ColorADXBuffer = Arr(0, 0.0)
min_rates_di = 0
min_rates_total = 0

def OnInit():
    global min_rates_di, min_rates_total
    min_rates_di = XADX.GetStartBars(XMA_Method, ADX_Period, ADX_Phase)
    min_rates_total = (2 * min_rates_di) + 1
    min_rates_di += 1
    SetIndexBuffer(0, DiPlusBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_di)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    SetIndexBuffer(1, DiMinusBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_di)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    SetIndexBuffer(2, ADXLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    SetIndexBuffer(3, ADXBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    SetIndexBuffer(4, ColorADXBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total + 1)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    shortname = Box("")
    Smooth = XADX.GetString_MA_Method(XMA_Method)
    StringConcatenate(shortname, 'XADX( ', Smooth, ', ', ADX_Period, ', ', ADX_Phase, ', ', EnumToString(IPC, 'Applied_price_'), ', ', Shift, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, ExtraHighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, LevelColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, LevelStyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 0, LevelWidth)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, LevelColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, LevelStyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 1, LevelWidth)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, LevelColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, LevelStyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 2, LevelWidth)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    DiPlus = 0.0
    DiMinus = 0.0
    Hi = 0.0
    Lo = 0.0
    prevHi = 0.0
    prevLo = 0.0
    prevCl = 0.0
    dTmpP = 0.0
    dTmpN = 0.0
    tr = 0.0
    dTmp = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        Hi = high[bar]
        prevHi = high[bar - 1]
        Lo = low[bar]
        prevLo = low[bar - 1]
        prevCl = close[bar - 1]
        dTmpP = Hi - prevHi
        dTmpN = prevLo - Lo
        if dTmpP < 0.0:
            dTmpP = 0.0
        if dTmpN < 0.0:
            dTmpN = 0.0
        if dTmpP > dTmpN:
            dTmpN = 0.0
        else:
            if dTmpP < dTmpN:
                dTmpP = 0.0
            else:
                dTmpP = 0.0
                dTmpN = 0.0
        tr = MathMax(MathMax(MathAbs(Hi - Lo), MathAbs(Hi - prevCl)), MathAbs(Lo - prevCl))
        if tr != 0.0:
            DiPlus = _fdiv(100.0 * dTmpP, tr)
            DiMinus = _fdiv(100.0 * dTmpN, tr)
        else:
            DiPlus = 0.0
            DiMinus = 0.0
        DiPlusBuffer[bar] = XDIP.XMASeries(1, prev_calculated, rates_total, XMA_Method, ADX_Phase, ADX_Period, DiPlus, bar, False)
        DiMinusBuffer[bar] = XDIM.XMASeries(1, prev_calculated, rates_total, XMA_Method, ADX_Phase, ADX_Period, DiMinus, bar, False)
        dTmp = DiPlusBuffer[bar] + DiMinusBuffer[bar]
        if dTmp != 0.0:
            dTmp = 100.0 * MathAbs(_fdiv(DiPlusBuffer[bar] - DiMinusBuffer[bar], dTmp))
        else:
            dTmp = 0.0
        ADXBuffer[bar] = XADX.XMASeries(min_rates_di, prev_calculated, rates_total, XMA_Method, ADX_Phase, ADX_Period, dTmp, bar, False)
        ADXLineBuffer[bar] = ADXBuffer[bar]
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first
    for bar in range(bar, rates_total):
        ColorADXBuffer[bar] = 1.0
        if ADXBuffer[bar] > ExtraHighLevel:
            ColorADXBuffer[bar] = 3.0
        elif ADXBuffer[bar] > HighLevel:
            ColorADXBuffer[bar] = 2.0
        elif ADXBuffer[bar] < LowLevel:
            ColorADXBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XDIP = _alloc(CXMA)
XDIP.__init__()
XDIM = _alloc(CXMA)
XDIM.__init__()
XADX = _alloc(CXMA)
XADX.__init__()
LevelColor = _input('LevelColor', _uint(Blue))  # Levels color


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorxadx(_MQL5Indicator):
    name = 'colorxadx'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # Histogram smoothing method
        'ADX_Period': 14,  # XMA smoothing period
        'ADX_Phase': 100,  # XMA smoothing period [-100...+100]
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Applied price
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'ExtraHighLevel': 60,  # Maximum trend level
        'HighLevel': 40,  # Strong trend level
        'LowLevel': 20,  # Weak trend level
        'LevelStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=4),  # Levels lines style
        'LevelWidth': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Levels width
    }

