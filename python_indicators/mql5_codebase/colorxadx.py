"""colorxadx — converted from MQL5: MQL5 Indicators/ColorXADX_HTF/colorxadx.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 12}, 'colors': {1: [65280, 255], 2: [8421504], 3: [8421504, 16711680, 16711935, 255]}, 'widths': {2: 1, 3: 3}, 'styles': {2: 0, 3: 0}, 'labels': {1: 'XDi', 2: 'XADX Line', 3: 'XADX'}, 'levels': [], 'description': [], 'name': 'colorxadx', 'source': 'MQL5 Indicators/ColorXADX_HTF/colorxadx.mq5', 'folder': 'ColorXADX_HTF', 'inputs': [{'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 7, 'label': 'Метод усреднения гистограммы', 'sinput': False}, {'mql': 'ADX_Period', 'py': 'ADX_Period', 'param': 'ADX_Period', 'type': 'uint', 'default': 14, 'label': 'Период XMA усреднения', 'sinput': False}, {'mql': 'ADX_Phase', 'py': 'ADX_Phase', 'param': 'ADX_Phase', 'type': 'int', 'default': 100, 'label': 'Параметр XMA усреднения', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'ExtraHighLevel', 'py': 'ExtraHighLevel', 'param': 'ExtraHighLevel', 'type': 'uint', 'default': 60, 'label': 'Уровень максимального тренда', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'uint', 'default': 40, 'label': 'Уровень сильного тренда', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'uint', 'default': 20, 'label': 'Уровень слабого тренда', 'sinput': False}, {'mql': 'LevelStyle', 'py': 'LevelStyle', 'param': 'LevelStyle', 'type': 'int', 'default': 4, 'label': 'Стиль линий уровней', 'sinput': False}, {'mql': 'LevelColor', 'py': 'LevelColor', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Цвет уровней', 'sinput': False}, {'mql': 'LevelWidth', 'py': 'LevelWidth', 'param': 'LevelWidth', 'type': 'int', 'default': 0, 'label': 'Толщина уровней', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# enum ENUM_WIDTH
w_1 = 0
w_2 = 1
w_3 = 2
w_4 = 3
w_5 = 4
_enum('ENUM_WIDTH', {0: 'w_1', 1: 'w_2', 2: 'w_3', 3: 'w_4', 4: 'w_5'})

# ---- inputs and global variables
XMA_Method = _input('XMA_Method', MODE_T3)  # Метод усреднения гистограммы
ADX_Period = _input('ADX_Period', 14)  # Период XMA усреднения
ADX_Phase = _input('ADX_Phase', 100)  # Параметр XMA усреднения
IPC = _input('IPC', PRICE_CLOSE_)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtraHighLevel = _input('ExtraHighLevel', 60)  # Уровень максимального тренда
HighLevel = _input('HighLevel', 40)  # Уровень сильного тренда
LowLevel = _input('LowLevel', 20)  # Уровень слабого тренда
LevelStyle = _input('LevelStyle', STYLE_DASHDOTDOT)  # Стиль линий уровней
LevelColor = _input('LevelColor', clrBlue)  # Цвет уровней
LevelWidth = _input('LevelWidth', w_1)  # Толщина уровней
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
    SetIndexBuffer(1, DiMinusBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ADXLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ADXBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ColorADXBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_di)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_di)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
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
        bar1 = bar - 1
        Hi = high[bar]
        prevHi = high[bar1]
        Lo = low[bar]
        prevLo = low[bar1]
        prevCl = close[bar1]
        dTmpP = Hi - prevHi
        dTmpN = prevLo - Lo
        dTmpP = MathMax(0.0, dTmpP)
        dTmpN = MathMax(0.0, dTmpN)
        if dTmpP > dTmpN:
            dTmpN = 0.0
        else:
            if dTmpP < dTmpN:
                dTmpP = 0.0
            else:
                dTmpP = 0.0
                dTmpN = 0.0
        tr = MathMax(MathMax(MathAbs(Hi - Lo), MathAbs(Hi - prevCl)), MathAbs(Lo - prevCl))
        if tr:
            DiPlus = _fdiv(100.0 * dTmpP, tr)
            DiMinus = _fdiv(100.0 * dTmpN, tr)
        else:
            DiPlus = 0.0
            DiMinus = 0.0
        DiPlusBuffer[bar] = XDIP.XMASeries(1, prev_calculated, rates_total, XMA_Method, ADX_Phase, ADX_Period, DiPlus, bar, False)
        DiMinusBuffer[bar] = XDIM.XMASeries(1, prev_calculated, rates_total, XMA_Method, ADX_Phase, ADX_Period, DiMinus, bar, False)
        dTmp = DiPlusBuffer[bar] + DiMinusBuffer[bar]
        if dTmp:
            dTmp = 100.0 * MathAbs(_fdiv(DiPlusBuffer[bar] - DiMinusBuffer[bar], dTmp))
        else:
            dTmp = 0.0
        ADXBuffer[bar] = XADX.XMASeries(min_rates_di, prev_calculated, rates_total, XMA_Method, ADX_Phase, ADX_Period, dTmp, bar, False)
        ADXLineBuffer[bar] = ADXBuffer[bar]
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first
    for bar in range(bar, rates_total):
        clr = 1
        if ADXBuffer[bar] > ExtraHighLevel:
            clr = 3
        elif ADXBuffer[bar] > HighLevel:
            clr = 2
        elif ADXBuffer[bar] < LowLevel:
            clr = 0
        ColorADXBuffer[bar] = clr
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorxadx(_MQL5Indicator):
    name = 'colorxadx'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # Метод усреднения гистограммы
        'ADX_Period': 14,  # Период XMA усреднения
        'ADX_Phase': 100,  # Параметр XMA усреднения
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'ExtraHighLevel': 60,  # Уровень максимального тренда
        'HighLevel': 40,  # Уровень сильного тренда
        'LowLevel': 20,  # Уровень слабого тренда
        'LevelStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=4),  # Стиль линий уровней
        'LevelWidth': _Choice({0: '1', 1: '2', 2: '3', 3: '4', 4: '5'}, default=0),  # Толщина уровней
    }

