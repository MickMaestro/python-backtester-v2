"""cmx — converted from MQL5: MQL5 Indicators/CMx_HTF/cmx.mq5

Copyright: Copyright © 2005, Alexandr; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Alexandr', 'link': '', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [3329330]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'CMx'}, 'levels': [], 'description': [], 'name': 'cmx', 'source': 'MQL5 Indicators/CMx_HTF/cmx.mq5', 'folder': 'CMx_HTF', 'inputs': [{'mql': 'F', 'py': 'F', 'param': 'F', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'k', 'py': 'k', 'param': 'k', 'type': 'double', 'default': 1.682, 'label': '', 'sinput': False}, {'mql': 'L_adx', 'py': 'L_adx', 'param': 'L_adx', 'type': 'double', 'default': 18.0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Level1', 'py': 'Level1', 'param': 'Level1', 'type': 'double', 'default': 423.6, 'label': 'Уровень 1', 'sinput': False}, {'mql': 'Level2', 'py': 'Level2', 'param': 'Level2', 'type': 'double', 'default': 261.8, 'label': 'Уровень 2', 'sinput': False}, {'mql': 'Level3', 'py': 'Level3', 'param': 'Level3', 'type': 'double', 'default': 161.8, 'label': 'Уровень 3', 'sinput': False}, {'mql': 'Level4', 'py': 'Level4', 'param': 'Level4', 'type': 'double', 'default': 61.8, 'label': 'Уровень 4', 'sinput': False}, {'mql': 'Level5', 'py': 'Level5', 'param': 'Level5', 'type': 'double', 'default': 0.0, 'label': 'Уровень 5', 'sinput': False}, {'mql': 'Level6', 'py': 'Level6', 'param': 'Level6', 'type': 'double', 'default': -61.8, 'label': 'Уровень 6', 'sinput': False}, {'mql': 'Level7', 'py': 'Level7', 'param': 'Level7', 'type': 'double', 'default': -161.8, 'label': 'Уровень 7', 'sinput': False}, {'mql': 'Level8', 'py': 'Level8', 'param': 'Level8', 'type': 'double', 'default': -261.8, 'label': 'Уровень 8', 'sinput': False}, {'mql': 'Level9', 'py': 'Level9', 'param': 'Level9', 'type': 'double', 'default': -423.6, 'label': 'Уровень 9', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
F = _input('F', 12)
k = _input('k', 1.682)
L_adx = _input('L_adx', 18.0)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
Level1 = _input('Level1', 423.6)  # Уровень 1
Level2 = _input('Level2', 261.8)  # Уровень 2
Level3 = _input('Level3', 161.8)  # Уровень 3
Level4 = _input('Level4', 61.8)  # Уровень 4
Level5 = _input('Level5', 0.0)  # Уровень 5
Level6 = _input('Level6', -61.8)  # Уровень 6
Level7 = _input('Level7', -161.8)  # Уровень 7
Level8 = _input('Level8', -261.8)  # Уровень 8
Level9 = _input('Level9', -423.6)  # Уровень 9
IndBuffer = Arr(0, 0.0)
L_adxk = 0.0
MA1_Handle = 0
MA2_Handle = 0
Ind_Handle = 0
ADX_Handle = 0
CCI_Handle = 0
min_rates_total = 0

def OnInit():
    global ADX_Handle, CCI_Handle, Ind_Handle, L_adxk, MA1_Handle, MA2_Handle, min_rates_total
    Fk = _int(MathRound(MathAbs(F * k)))
    min_rates_total = MathMax(F, Fk)
    if F > 0:
        min_rates_total *= 2
    if F < 0:
        MA1_Handle = iMA(Symbol(), PERIOD_CURRENT, -F, 0, MODE_EMA, PRICE_CLOSE)
        if MA1_Handle == INVALID_HANDLE:
            Print('Не удалось получить хендл индикатора iMA 1')
            return INIT_FAILED
        MA2_Handle = iMA(Symbol(), PERIOD_CURRENT, Fk, 0, MODE_EMA, PRICE_CLOSE)
        if MA2_Handle == INVALID_HANDLE:
            Print('Не удалось получить хендл индикатора iMA 2')
            return INIT_FAILED
    elif F > 0:
        L_adxk = L_adx * k
        IndName = MQLInfoString(MQL_PROGRAM_NAME)
        Ind_Handle = iCustom(Symbol(), PERIOD_CURRENT, IndName, -F, k, L_adx, 0)
        if Ind_Handle == INVALID_HANDLE:
            Print('Не удалось получить хендл индикатора CMx')
            return INIT_FAILED
        CCI_Handle = iCCI(Symbol(), PERIOD_CURRENT, Fk, Ind_Handle)
        if CCI_Handle == INVALID_HANDLE:
            Print('Не удалось получить хендл индикатора iCCI')
            return INIT_FAILED
        ADX_Handle = iADX(Symbol(), PERIOD_CURRENT, F)
        if ADX_Handle == INVALID_HANDLE:
            Print('Не удалось получить хендл индикатора iADX')
            return INIT_FAILED
    else:
        Print('Период индикатора не может быть меньше единицы!')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'CMx(', F, ', ', DoubleToString(k, 4), ', ', DoubleToString(L_adx, 2), ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetInteger(INDICATOR_LEVELS, 9)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, Level1)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, Level2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, Level3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, Level4)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 4, Level5)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 5, Level6)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 6, Level7)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 7, Level8)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 8, Level9)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 3, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 4, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 5, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 6, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 7, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 8, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 3, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 4, STYLE_DASH)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 5, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 6, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 7, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 8, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    if F < 0:
        if BarsCalculated(MA1_Handle) < rates_total or BarsCalculated(MA2_Handle) < rates_total:
            return 0
    else:
        if (BarsCalculated(Ind_Handle) < rates_total or BarsCalculated(ADX_Handle) < rates_total) or BarsCalculated(CCI_Handle) < rates_total:
            return 0
    to_copy = 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if F < 0:
        Ma1 = Arr(0, 0.0)
        Ma2 = Arr(0, 0.0)
        ArraySetAsSeries(Ma1, True)
        ArraySetAsSeries(Ma2, True)
        if CopyBuffer(MA1_Handle, 0, 0, to_copy, Ma1) <= 0:
            return 0
        if CopyBuffer(MA2_Handle, 0, 0, to_copy, Ma2) <= 0:
            return 0
        bar = limit
        for bar in range(bar, 0 - 1, -1):
            IndBuffer[bar] = Ma1[bar] - Ma2[bar]
        else:
            bar = _range_end(bar, 0 - 1, -1)
    else:
        CCI = Arr(0, 0.0)
        ADX = Arr(0, 0.0)
        ArraySetAsSeries(CCI, True)
        ArraySetAsSeries(ADX, True)
        if CopyBuffer(CCI_Handle, 0, 0, to_copy, CCI) <= 0:
            return 0
        if CopyBuffer(ADX_Handle, 0, 0, to_copy, ADX) <= 0:
            return 0
        bar = limit
        for bar in range(bar, 0 - 1, -1):
            IndBuffer[bar] = _fdiv(CCI[bar] * ADX[bar], L_adxk)
        else:
            bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Cmx(_MQL5Indicator):
    name = 'cmx'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'F': 12,
        'k': 1.682,
        'L_adx': 18.0,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'Level1': 423.6,  # Уровень 1
        'Level2': 261.8,  # Уровень 2
        'Level3': 161.8,  # Уровень 3
        'Level4': 61.8,  # Уровень 4
        'Level5': 0.0,  # Уровень 5
        'Level6': -61.8,  # Уровень 6
        'Level7': -161.8,  # Уровень 7
        'Level8': -261.8,  # Уровень 8
        'Level9': -423.6,  # Уровень 9
    }

