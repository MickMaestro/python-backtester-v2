"""ccmx — converted from MQL5: MQL5 Indicators/CCMx_HTF/ccmx.mq5

Copyright: Copyright © 2004, MetaQuotes Software Corp.; Link: http://www.metaquotes.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2004, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [1993170]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'CCMx'}, 'levels': [], 'description': [], 'name': 'ccmx', 'source': 'MQL5 Indicators/CCMx_HTF/ccmx.mq5', 'folder': 'CCMx_HTF', 'inputs': [{'mql': 'F', 'py': 'F', 'param': 'F', 'type': 'uint', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'k', 'py': 'k', 'param': 'k', 'type': 'double', 'default': 1.682, 'label': '', 'sinput': False}, {'mql': 'L_adx', 'py': 'L_adx', 'param': 'L_adx', 'type': 'double', 'default': 18.0, 'label': '', 'sinput': False}, {'mql': 'PriceMACD', 'py': 'PriceMACD', 'param': 'PriceMACD', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Level1', 'py': 'Level1', 'param': 'Level1', 'type': 'double', 'default': 423.6, 'label': 'Уровень 1', 'sinput': False}, {'mql': 'Level2', 'py': 'Level2', 'param': 'Level2', 'type': 'double', 'default': 261.8, 'label': 'Уровень 2', 'sinput': False}, {'mql': 'Level3', 'py': 'Level3', 'param': 'Level3', 'type': 'double', 'default': 161.8, 'label': 'Уровень 3', 'sinput': False}, {'mql': 'Level4', 'py': 'Level4', 'param': 'Level4', 'type': 'double', 'default': 61.8, 'label': 'Уровень 4', 'sinput': False}, {'mql': 'Level5', 'py': 'Level5', 'param': 'Level5', 'type': 'double', 'default': 0.0, 'label': 'Уровень 5', 'sinput': False}, {'mql': 'Level6', 'py': 'Level6', 'param': 'Level6', 'type': 'double', 'default': -61.8, 'label': 'Уровень 6', 'sinput': False}, {'mql': 'Level7', 'py': 'Level7', 'param': 'Level7', 'type': 'double', 'default': -161.8, 'label': 'Уровень 7', 'sinput': False}, {'mql': 'Level8', 'py': 'Level8', 'param': 'Level8', 'type': 'double', 'default': -261.8, 'label': 'Уровень 8', 'sinput': False}, {'mql': 'Level9', 'py': 'Level9', 'param': 'Level9', 'type': 'double', 'default': -423.6, 'label': 'Уровень 9', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
F = _input('F', 12)
k = _input('k', 1.682)
L_adx = _input('L_adx', 18.0)
PriceMACD = _input('PriceMACD', PRICE_CLOSE)
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
MACD_Handle = 0
ADX_Handle = 0
CCI_Handle = 0
min_rates_total = 0

def OnInit():
    global ADX_Handle, CCI_Handle, L_adxk, MACD_Handle, min_rates_total
    Fk = _int(MathRound(MathAbs(F * k)))
    min_rates_total = _int(MathMax(F, Fk))
    min_rates_total *= 2
    L_adxk = L_adx * k
    MACD_Handle = iMACD(None, 0, F, Fk, 5, PriceMACD)
    if MACD_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMACD')
        return INIT_FAILED
    CCI_Handle = iCCI(Symbol(), PERIOD_CURRENT, Fk, MACD_Handle)
    if CCI_Handle == INVALID_HANDLE:
        Print('Не удалось получить хендл индикатора iCCI')
        return INIT_FAILED
    ADX_Handle = iADX(Symbol(), PERIOD_CURRENT, F)
    if ADX_Handle == INVALID_HANDLE:
        Print('Не удалось получить хендл индикатора iADX')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'CCMx(', F, ', ', DoubleToString(k, 4), ', ', DoubleToString(L_adx, 2), ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
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
    if ((rates_total < min_rates_total or BarsCalculated(MACD_Handle) < rates_total) or BarsCalculated(ADX_Handle) < rates_total) or BarsCalculated(CCI_Handle) < rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    CCI = Arr(0, 0.0)
    ADX = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
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


class Ccmx(_MQL5Indicator):
    name = 'ccmx'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'F': 12,
        'k': 1.682,
        'L_adx': 18.0,
        'PriceMACD': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
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

