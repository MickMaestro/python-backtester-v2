"""MurreyMathFixPeriod_Lv — converted from MQL5: MQL5 Indicators/MurreyMathFixPeriod_Lv/MurreyMathFixPeriod_Lv.mq5

Copyright: 2011,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.getfontname import *  # #include getfontname.mqh

MQL5_META = {'props': {'copyright': '2011,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 41, 'indicator_plots': 40}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 40: 4}, 'colors': {1: [16711680], 2: [13828244], 3: [16776960], 4: [4163021], 5: [255], 6: [65280], 7: [11119017], 8: [65280], 9: [255], 10: [4163021], 11: [16776960], 12: [13828244], 13: [16711680], 40: [12632256]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 40: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 40: 1}, 'labels': {40: 'Вертикальный разделитель периодов индикатора'}, 'levels': [], 'description': [], 'name': 'MurreyMathFixPeriod_Lv', 'source': 'MQL5 Indicators/MurreyMathFixPeriod_Lv/MurreyMathFixPeriod_Lv.mq5', 'folder': 'MurreyMathFixPeriod_Lv', 'inputs': [{'mql': 'Timeframe', 'py': 'Timeframe', 'param': 'Timeframe', 'type': 'int', 'default': 16408, 'label': 'Таймфрейм индикатора для расчёта уровней', 'sinput': False}, {'mql': 'CalculationPeriod', 'py': 'CalculationPeriod', 'param': 'CalculationPeriod', 'type': 'int', 'default': 64, 'label': 'Период расчета P', 'sinput': False}, {'mql': 'StepBack', 'py': 'StepBack', 'param': 'StepBack', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 8, 'label': 'размер шрифта', 'sinput': False}, {'mql': 'FontType', 'py': 'FontType', 'param': 'FontType', 'type': 'int', 'default': 7, 'label': 'тип шрифта', 'sinput': False}, {'mql': 'LableSirname', 'py': 'LableSirname', 'param': None, 'type': 'string', 'default': 'Murrey_Math_Lv', 'label': 'Первая часть имени графических объектов', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['getfontname.mqh']}

# ---- inputs and global variables
Timeframe = _input('Timeframe', PERIOD_D1)  # Таймфрейм индикатора для расчёта уровней
CalculationPeriod = _input('CalculationPeriod', 64)  # Период расчета P
StepBack = _input('StepBack', 0)
FontSize = _input('FontSize', 8)  # размер шрифта
FontType = _input('FontType', Font7)  # тип шрифта
LableSirname = _input('LableSirname', 'Murrey_Math_Lv')  # Первая часть имени графических объектов
LinesNames = Arr.of(['Вращение, разворот [-2/8]', 'Слабая остановка и разворот [-1/8]', 'Окончательное сопротивление [0/8]', 'Слабая остановка и разворот [1/8]', 'Вращение, разворот [2/8]', 'Дно торгового диапазона [3/8]', 'Главные сопротивление/поддержка [4/8]', 'Верх торгового диапазона [5/8]', 'Вращение, разворот [6/8]', 'Слабая остановка и разворот [7/8]', 'Окончательное сопротивление [8/8]', 'Слабая остановка и разворот [+1/8]', 'Вращение, разворот [+2/8]'], fill="", dyn=False, size=13)
Init = False
ShiftBarsForward = 0
Murrey_Handle = 0
min_rates_total = 0
Murrey_Calculated = 0

class CIndicatorsBuffers(MqlObject):
    _q_fields = ('IndBuffer',)
    def __init__(self, *args):
        self.IndBuffer = Arr(0, 0.0)

def GetMurreyLevels(Array, Time):
    Murrey = Arr(1, 0.0, dyn=False)
    for i in range(0, 13):
        if CopyBuffer(Murrey_Handle, i, _DT(Time), 1, Murrey) <= 0:
            return (0 != 0)
        Array[i] = Murrey[0]
    return True

def CheckMurreyLevels(Array):
    for iii in range(0, 13):
        if Array[iii] != _s_CheckMurreyLevels_OldMurrey[iii]:
            for kkk in range(0, 13):
                _s_CheckMurreyLevels_OldMurrey[kkk] = Array[kkk]
            return True
    return False

def OnInit():
    global Init, Murrey_Calculated, Murrey_Handle, min_rates_total
    Murrey_Calculated = CalculationPeriod + StepBack + 3
    min_rates_total = _idiv(Murrey_Calculated * PeriodSeconds(Timeframe), PeriodSeconds(PERIOD_CURRENT))
    Init = True
    if Timeframe < Period() and Timeframe != PERIOD_CURRENT:
        Print('Период графика для индикатора MurreyMath не может быть меньше периода текущего графика')
        Init = False
        return
    Murrey_Handle = iCustom(None, Timeframe, 'Murrey_Math_Lv', CalculationPeriod, StepBack, True, FontSize, FontType, LableSirname)
    if Murrey_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора MurreyMath_Lv')
    for kkk in range(0, 3):
        for iii in range(0, 13):
            SetIndexBuffer((13 * kkk) + iii, Ind[kkk][iii].IndBuffer, INDICATOR_DATA)
            PlotIndexSetDouble((13 * kkk) + iii, PLOT_EMPTY_VALUE, EMPTY_VALUE)
            PlotIndexSetString((13 * kkk) + iii, PLOT_LABEL, LinesNames[iii])
    SetIndexBuffer(39, Ind1[0].IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(40, Ind1[1].IndBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(39, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    for fff in range(1, 3):
        for iii in range(0, 13):
            PlotIndexSetInteger((13 * fff) + iii, PLOT_DRAW_TYPE, PlotIndexGetInteger(iii, PLOT_DRAW_TYPE))
            PlotIndexSetInteger((13 * fff) + iii, PLOT_LINE_STYLE, PlotIndexGetInteger(iii, PLOT_LINE_STYLE))
            PlotIndexSetInteger((13 * fff) + iii, PLOT_LINE_WIDTH, PlotIndexGetInteger(iii, PLOT_LINE_WIDTH))
            PlotIndexSetInteger((13 * fff) + iii, PLOT_LINE_COLOR, PlotIndexGetInteger(iii, PLOT_LINE_COLOR))
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'Murrey_LvMath_Lv(' + EnumToString(Timeframe, 'ENUM_TIMEFRAMES') + ', ' + _str(CalculationPeriod) + ', ' + _str(StepBack) + ')')
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_bar1, _s_OnCalculate_count
    if (BarsCalculated(Murrey_Handle) < (10 * Murrey_Calculated) or rates_total < min_rates_total) or (not Init):
        return 0
    if prev_calculated == rates_total:
        return rates_total
    first = 0
    oldcount = 0
    val = Arr(26, 0.0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
        _s_OnCalculate_bar1 = first
        for kkk in range(0, 3):
            for iii in range(0, 13):
                for bar in range(0, min_rates_total):
                    _s_OnCalculate_count = 0
    else:
        first = prev_calculated - 1
    for bar in range(first, rates_total):
        if not GetMurreyLevels(_s_OnCalculate_Murrey, time[bar]):
            return 0
        if CheckMurreyLevels(_s_OnCalculate_Murrey):
            _s_OnCalculate_count += 1
            if _s_OnCalculate_count > 2:
                _s_OnCalculate_count = 0
            _s_OnCalculate_bar1 = bar - 1
            for iii in range(0, 13):
                Ind[_s_OnCalculate_count][iii].IndBuffer[_s_OnCalculate_bar1] = _s_OnCalculate_Murrey[iii]
        for kkk in range(0, 3):
            for iii in range(0, 13):
                Ind[kkk][iii].IndBuffer[bar] = EMPTY_VALUE
        for iii in range(0, 13):
            Ind[_s_OnCalculate_count][iii].IndBuffer[bar] = _s_OnCalculate_Murrey[iii]
        Ind1[0].IndBuffer[bar] = EMPTY_VALUE
        Ind1[1].IndBuffer[bar] = EMPTY_VALUE
        ArrayInitialize(val, None)
        oldcount = _s_OnCalculate_count - 1
        if oldcount < 0:
            oldcount = 2
        for iii in range(0, 13):
            val[iii] = Ind[oldcount][iii].IndBuffer[_s_OnCalculate_bar1]
            val[iii + 13] = Ind[_s_OnCalculate_count][iii].IndBuffer[bar]
        Ind1[0].IndBuffer[_s_OnCalculate_bar1] = 5 * val[25 - ArrayMaximum(val)]
        Ind1[1].IndBuffer[_s_OnCalculate_bar1] = val[25 - ArrayMinimum(val)] / 5
    return rates_total

# ---- global variables initialised from expressions
Ind = Arr(3, 0, dyn=False, factory=CIndicatorsBuffers, dims=(13,))
Ind1 = Arr(2, 0, dyn=False, factory=CIndicatorsBuffers)

# ---- static local variables
_s_CheckMurreyLevels_OldMurrey = Arr(13, 0.0, dyn=False)
_s_OnCalculate_count = 0
_s_OnCalculate_bar1 = 0
_s_OnCalculate_Murrey = Arr(13, 0.0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MurreyMathFixPeriodLv(_MQL5Indicator):
    name = 'MurreyMathFixPeriod_Lv'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Timeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Таймфрейм индикатора для расчёта уровней
        'CalculationPeriod': 64,  # Период расчета P
        'StepBack': 0,
        'FontSize': 8,  # размер шрифта
        'FontType': _Choice({0: 'Arial', 1: 'Arial Black', 2: 'Arial Bold', 3: 'Arial Bold Italic', 4: 'Arial Italic', 5: 'Comic Sans MS Bold', 6: 'Courier', 7: 'Courier New', 8: 'Courier New Bold', 9: 'Courier New Bold Italic', 10: 'Courier New Italic', 11: 'Estrangelo Edessa', 12: 'Franklin Gothic Medium', 13: 'Gautami', 14: 'Georgia', 15: 'Georgia Bold', 16: 'Georgia Bold Italic', 17: 'Georgia Italic', 18: 'Georgia Italic Impact', 19: 'Latha', 20: 'Lucida Console', 21: 'Lucida Sans Unicode', 22: 'Modern MS Sans Serif', 23: 'MS Sans Serif', 24: 'Mv Boli', 25: 'Palatino Linotype', 26: 'Palatino Linotype Bold', 27: 'Palatino Linotype Italic', 28: 'Roman', 29: 'Script', 30: 'Small Fonts', 31: 'Symbol', 32: 'Tahoma', 33: 'Tahoma Bold', 34: 'Times New Roman', 35: 'Times New Roman Bold', 36: 'Times New Roman Bold Italic', 37: 'Times New Roman Italic', 38: 'Trebuchet MS', 39: 'Trebuchet MS Bold', 40: 'Trebuchet MS Bold Italic', 41: 'Trebuchet MS Italic', 42: 'Tunga', 43: 'Verdana', 44: 'Verdana Bold', 45: 'Verdana Bold Italic', 46: 'Verdana Italic', 47: 'Webdings', 48: 'Westminster', 49: 'Wingdings', 50: 'WST_Czech', 51: 'WST_Engl', 52: 'WST_Fren', 53: 'WST_Germ', 54: 'WST_Ital', 55: 'WST_Span', 56: 'WST_Swed'}, default=7),  # тип шрифта
    }

