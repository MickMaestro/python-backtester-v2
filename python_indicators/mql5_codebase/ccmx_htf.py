"""ccmx_htf — converted from MQL5: MQL5 Indicators/CCMx_HTF/ccmx_htf.mq5

CCMx с возможностью изменения таймфрейма во входных параметрах
Copyright: Copyright © 2014, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [1993170]}, 'widths': {1: 4}, 'styles': {1: 0}, 'labels': {1: 'INDICATOR_NAME'}, 'levels': [], 'description': ['CCMx с возможностью изменения таймфрейма во входных параметрах'], 'name': 'ccmx_htf', 'source': 'MQL5 Indicators/CCMx_HTF/ccmx_htf.mq5', 'folder': 'CCMx_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора', 'sinput': False}, {'mql': 'F', 'py': 'F', 'param': 'F', 'type': 'uint', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'k', 'py': 'k', 'param': 'k', 'type': 'double', 'default': 1.682, 'label': '', 'sinput': False}, {'mql': 'L_adx', 'py': 'L_adx', 'param': 'L_adx', 'type': 'double', 'default': 18.0, 'label': '', 'sinput': False}, {'mql': 'PriceMACD', 'py': 'PriceMACD', 'param': 'PriceMACD', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Level1', 'py': 'Level1', 'param': 'Level1', 'type': 'double', 'default': 423.6, 'label': 'Уровень 1', 'sinput': False}, {'mql': 'Level2', 'py': 'Level2', 'param': 'Level2', 'type': 'double', 'default': 261.8, 'label': 'Уровень 2', 'sinput': False}, {'mql': 'Level3', 'py': 'Level3', 'param': 'Level3', 'type': 'double', 'default': 161.8, 'label': 'Уровень 3', 'sinput': False}, {'mql': 'Level4', 'py': 'Level4', 'param': 'Level4', 'type': 'double', 'default': 61.8, 'label': 'Уровень 4', 'sinput': False}, {'mql': 'Level5', 'py': 'Level5', 'param': 'Level5', 'type': 'double', 'default': 0.0, 'label': 'Уровень 5', 'sinput': False}, {'mql': 'Level6', 'py': 'Level6', 'param': 'Level6', 'type': 'double', 'default': -61.8, 'label': 'Уровень 6', 'sinput': False}, {'mql': 'Level7', 'py': 'Level7', 'param': 'Level7', 'type': 'double', 'default': -161.8, 'label': 'Уровень 7', 'sinput': False}, {'mql': 'Level8', 'py': 'Level8', 'param': 'Level8', 'type': 'double', 'default': -261.8, 'label': 'Уровень 8', 'sinput': False}, {'mql': 'Level9', 'py': 'Level9', 'param': 'Level9', 'type': 'double', 'default': -423.6, 'label': 'Уровень 9', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора
F = _input('F', 12)
k = _input('k', 1.682)
L_adx = _input('L_adx', 18.0)
PriceMACD = _input('PriceMACD', PRICE_CLOSE)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
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
ColorIndBuffer = Arr(0, 0.0)
Symbol_ = ""
Word = ""
min_rates_total = 0
Ind_Handle = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, Symbol_, Word, min_rates_total
    if not TimeFramesCheck('CCMx', TimeFrame):
        return INIT_FAILED
    min_rates_total = 2
    Symbol_ = Symbol()
    Word = 'CCMx' + ' индикатор: ' + Symbol_ + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1)
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'CCMx', F, k, L_adx, PriceMACD, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора CCMx')
        return INIT_FAILED
    IndInit(0, IndBuffer, 0.0, min_rates_total, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'CCMx', '(', GetStringTimeframe(TimeFrame), ')')
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
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(time, True)
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, IndBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Empty_Value, Draw_Begin, nShift):
    SetIndexBuffer(Number, Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    ArraySetAsSeries(Buffer, True)

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb, IndBuf, iTime_, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        IndBuf[bar] = 0.0
        if CopyTime(Symbol_, TFrame, _DT(iTime_[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if iTime_[bar] >= IndTime[0] and iTime_[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            Arr_ = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb, _DT(iTime_[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf[bar] = Arr_[0]
        else:
            IndBuf[bar] = IndBuf[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика!')
        Print('Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(1, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CcmxHtf(_MQL5Indicator):
    name = 'ccmx_htf'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора
        'F': 12,
        'k': 1.682,
        'L_adx': 18.0,
        'PriceMACD': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
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

