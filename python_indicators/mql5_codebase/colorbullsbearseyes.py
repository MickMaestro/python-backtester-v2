"""colorbullsbearseyes — converted from MQL5: MQL5 Indicators/ColorBullsBearsEyes_HTF/colorbullsbearseyes.mq5

BullsBearsEyes
Copyright: Copyright © 2007, EmeraldKing, transport_david; Link: http://finance.groups.yahoo.com/group/MetaTrader_Experts_and_Indicators/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, EmeraldKing, transport_david', 'link': 'http://finance.groups.yahoo.com/group/MetaTrader_Experts_and_Indicators/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16711680, 255, 65280]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'BullsBearsEyes'}, 'levels': [0.0], 'description': ['BullsBearsEyes'], 'name': 'colorbullsbearseyes', 'source': 'MQL5 Indicators/ColorBullsBearsEyes_HTF/colorbullsbearseyes.mq5', 'folder': 'ColorBullsBearsEyes_HTF', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'int', 'default': 13, 'label': 'Период усреднения индикатора', 'sinput': False}, {'mql': 'gamma', 'py': 'gamma', 'param': 'gamma', 'type': 'double', 'default': 0.6, 'label': 'Коэффициент сглаживания индикатора', 'sinput': False}, {'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 2, 'label': 'Алгоритм расчета сигнала входа', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'uint', 'default': 75, 'label': 'Уровень перекупленности', 'sinput': False}, {'mql': 'MiddleLevel', 'py': 'MiddleLevel', 'param': 'MiddleLevel', 'type': 'uint', 'default': 50, 'label': 'Уровень середины', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'uint', 'default': 25, 'label': 'Уровень перепроданности', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum AlgMode
twist = 0
breakdown1 = 1
breakdown2 = 2
breakdown3 = 3
_enum('AlgMode', {0: 'twist', 1: 'breakdown1', 2: 'breakdown2', 3: 'breakdown3'})

# ---- inputs and global variables
period = _input('period', 13)  # Период усреднения индикатора
gamma = _input('gamma', 0.6)  # Коэффициент сглаживания индикатора
Mode = _input('Mode', breakdown2)  # Алгоритм расчета сигнала входа
HighLevel = _input('HighLevel', 75)  # Уровень перекупленности
MiddleLevel = _input('MiddleLevel', 50)  # Уровень середины
LowLevel = _input('LowLevel', 25)  # Уровень перепроданности
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
BullsBearsEyes = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
SignBuffer = Arr(0, 0.0)
Bears_Handle = 0
Bulls_Handle = 0
min_rates_total = 0

def OnInit():
    global Bears_Handle, Bulls_Handle, min_rates_total
    min_rates_total = period + 4
    Bears_Handle = iBearsPower(None, 0, period)
    if Bears_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iBearsPower')
    Bulls_Handle = iBullsPower(None, 0, period)
    if Bulls_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iBullsPower')
    SetIndexBuffer(0, BullsBearsEyes, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(BullsBearsEyes, True)
    SetIndexBuffer(1, ColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorBuffer, True)
    SetIndexBuffer(2, SignBuffer, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(SignBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'BullsBearsEyes(', period, ', ', gamma, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 5)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, 100)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, MiddleLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, LowLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 4, 0)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrLimeGreen)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 3, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 4, clrLimeGreen)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASH)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 3, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 4, STYLE_DASH)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_L0_, _s_OnCalculate_L1_, _s_OnCalculate_L2_, _s_OnCalculate_L3_, _s_OnCalculate_trend_
    if (BarsCalculated(Bears_Handle) < rates_total or BarsCalculated(Bulls_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    result = 0.0
    Bears = Arr(0, 0.0)
    Bulls = Arr(0, 0.0)
    CU = 0.0
    CD = 0.0
    L0 = 0.0
    L1 = 0.0
    L2 = 0.0
    L3 = 0.0
    L0A = 0.0
    L1A = 0.0
    L2A = 0.0
    L3A = 0.0
    limit = 0
    bar = 0
    to_copy = 0
    trend = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - period - 1
        _s_OnCalculate_trend_ = 0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(Bears, True)
    ArraySetAsSeries(Bulls, True)
    if CopyBuffer(Bears_Handle, 0, 0, to_copy, Bears) <= 0:
        return 0
    if CopyBuffer(Bulls_Handle, 0, 0, to_copy, Bulls) <= 0:
        return 0
    L0 = _s_OnCalculate_L0_
    L1 = _s_OnCalculate_L1_
    L2 = _s_OnCalculate_L2_
    L3 = _s_OnCalculate_L3_
    if Mode == breakdown3:
        trend = _s_OnCalculate_trend_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            _s_OnCalculate_L0_ = L0
            _s_OnCalculate_L1_ = L1
            _s_OnCalculate_L2_ = L2
            _s_OnCalculate_L3_ = L3
        L0A = L0
        L1A = L1
        L2A = L2
        L3A = L3
        L0 = ((1.0 - gamma) * (Bears[bar] + Bulls[bar])) + (gamma * L0A)
        L1 = ((-gamma) * L0) + L0A + (gamma * L1A)
        L2 = ((-gamma) * L1) + L1A + (gamma * L2A)
        L3 = ((-gamma) * L2) + L2A + (gamma * L3A)
        CU = 0.0
        CD = 0.0
        result = 0.0
        if L0 >= L1:
            CU = L0 - L1
        else:
            CD = L1 - L0
        if L1 >= L2:
            CU += L1 - L2
        else:
            CD += L2 - L1
        if L2 >= L3:
            CU += L2 - L3
        else:
            CD += L3 - L2
        if (CU + CD) != 0:
            result = _fdiv(CU, CU + CD)
        result *= 100
        BullsBearsEyes[bar] = result
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= min_rates_total
    _sw1 = Mode
    if _sw1 == twist:
        bar = limit
        for bar in range(bar, 0 - 1, -1):
            bar1 = bar + 1
            ColorBuffer[bar] = 0.0
            if BullsBearsEyes[bar1] > BullsBearsEyes[bar]:
                ColorBuffer[bar] = 1.0
            if BullsBearsEyes[bar1] < BullsBearsEyes[bar]:
                ColorBuffer[bar] = 2.0
        else:
            bar = _range_end(bar, 0 - 1, -1)
    elif _sw1 == breakdown1:
        bar = limit
        for bar in range(bar, 0 - 1, -1):
            ColorBuffer[bar] = 0.0
            if BullsBearsEyes[bar] < MiddleLevel:
                ColorBuffer[bar] = 1.0
            if BullsBearsEyes[bar] > MiddleLevel:
                ColorBuffer[bar] = 2.0
        else:
            bar = _range_end(bar, 0 - 1, -1)
    elif _sw1 == breakdown2:
        bar = limit
        for bar in range(bar, 0 - 1, -1):
            ColorBuffer[bar] = 0.0
            if BullsBearsEyes[bar] < LowLevel:
                ColorBuffer[bar] = 1.0
            if BullsBearsEyes[bar] > HighLevel:
                ColorBuffer[bar] = 2.0
        else:
            bar = _range_end(bar, 0 - 1, -1)
    elif _sw1 == breakdown3:
        bar = limit
        for bar in range(bar, 0 - 1, -1):
            bar1 = bar + 1
            if BullsBearsEyes[bar1] >= HighLevel and BullsBearsEyes[bar] < HighLevel:
                trend = -1
            if BullsBearsEyes[bar1] >= LowLevel and BullsBearsEyes[bar] < LowLevel:
                trend = -1
            if BullsBearsEyes[bar1] <= LowLevel and BullsBearsEyes[bar] > LowLevel:
                trend = 1
            if BullsBearsEyes[bar1] <= HighLevel and BullsBearsEyes[bar] > HighLevel:
                trend = 1
            if bar == 1:
                _s_OnCalculate_trend_ = trend
            ColorBuffer[bar] = 0.0
            if trend < 0:
                ColorBuffer[bar] = 1.0
            if trend > 0:
                ColorBuffer[bar] = 2.0
        else:
            bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        SignBuffer[bar] = 0.0
        bar1 = bar + 1
        if SignBuffer[bar1] > 0 and ColorBuffer[bar] == 1:
            SignBuffer[bar] = -2.0
        elif (SignBuffer[bar1] <= 0 and ColorBuffer[bar] == 1) or (SignBuffer[bar + 1] < 0 and (not ColorBuffer[bar])):
            SignBuffer[bar] = -1.0
        if SignBuffer[bar + 1] < 0 and ColorBuffer[bar] == 2:
            SignBuffer[bar] = 2.0
        elif (SignBuffer[bar1] >= 0 and ColorBuffer[bar] == 2) or (SignBuffer[bar1] > 0 and (not ColorBuffer[bar])):
            SignBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_L0_ = 0.0
_s_OnCalculate_L1_ = 0.0
_s_OnCalculate_L2_ = 0.0
_s_OnCalculate_L3_ = 0.0
_s_OnCalculate_trend_ = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorbullsbearseyes(_MQL5Indicator):
    name = 'colorbullsbearseyes'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'period': 13,  # Период усреднения индикатора
        'gamma': 0.6,  # Коэффициент сглаживания индикатора
        'Mode': _Choice({0: 'изменение направления', 1: 'пробой средней линии', 2: 'пробой уровней перезакупа и перепроданности', 3: 'выход из зон перекупленности и перепроданности + пробой уровней перезакупа и перепроданности'}, default=2),  # Алгоритм расчета сигнала входа
        'HighLevel': 75,  # Уровень перекупленности
        'MiddleLevel': 50,  # Уровень середины
        'LowLevel': 25,  # Уровень перепроданности
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

