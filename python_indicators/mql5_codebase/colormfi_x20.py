"""ColorMFI_X20 — converted from MQL5: MQL5 Indicators/ColorMFI_X20/ColorMFI_X20.mq5

Двадцать индикаторов MFI в одном окне
Copyright: Copyright © 2010, Ivan Kornilov; Link: excelf@gmail.com; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Ivan Kornilov', 'link': 'excelf@gmail.com', 'version': '1.02', 'window': 'separate', 'indicator_buffers': 40, 'indicator_plots': 0}, 'types': {1: 8}, 'colors': {1: [16748574, 8421504, 255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': ['Двадцать индикаторов MFI в одном окне'], 'name': 'ColorMFI_X20', 'source': 'MQL5 Indicators/ColorMFI_X20/ColorMFI_X20.mq5', 'folder': 'ColorMFI_X20', 'inputs': [{'mql': 'StartMFIPeriod', 'py': 'StartMFIPeriod', 'param': 'StartMFIPeriod', 'type': 'uint', 'default': 5, 'label': 'стартовый период', 'sinput': False}, {'mql': 'step', 'py': 'step', 'param': 'step', 'type': 'uint', 'default': 1, 'label': 'шаг периода', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'объём', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'uint', 'default': 60, 'label': 'уровень перекупленности', 'sinput': False}, {'mql': 'MidLevel', 'py': 'MidLevel', 'param': 'MidLevel', 'type': 'uint', 'default': 50, 'label': 'уровень середины', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'uint', 'default': 40, 'label': 'уровень перепроданности', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
StartMFIPeriod = _input('StartMFIPeriod', 5)  # стартовый период
step = _input('step', 1)  # шаг периода
VolumeType = _input('VolumeType', VOLUME_TICK)  # объём
HighLevel = _input('HighLevel', 60)  # уровень перекупленности
MidLevel = _input('MidLevel', 50)  # уровень середины
LowLevel = _input('LowLevel', 40)  # уровень перепроданности
Ind_Handle = Arr(20, 0, dyn=False)
min_rates_total = 0

class CIndicatorsBuffers(MqlObject):
    _q_fields = ('IndBuffer', 'ColorIndBuffer')
    def __init__(self, *args):
        self.IndBuffer = Arr(0, 0.0)
        self.ColorIndBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = _int(StartMFIPeriod + (step * (20 - 1))) + 1
    Maxrange = StartMFIPeriod + (20 * (step - 1 + 1) * 2)
    period = StartMFIPeriod
    for numb in range(0, 20):
        period += step
        Ind_Handle[numb] = iMFI(Symbol(), 0, period, VolumeType)
        if Ind_Handle[numb] == INVALID_HANDLE:
            Print(' Не удалось получить хендл индикатора iMFI ', numb)
        shortname = Box('')
        StringConcatenate(shortname, 'iMFI X', 20, '*', period, ')')
        PlotIndexSetString(numb, PLOT_LABEL, shortname.v)
        PlotIndexSetDouble(numb, PLOT_EMPTY_VALUE, EMPTY_VALUE)
        PlotIndexSetInteger(numb, PLOT_DRAW_BEGIN, min_rates_total)
        SetIndexBuffer(2 * numb, Ind[numb].IndBuffer, INDICATOR_DATA)
        ArraySetAsSeries(Ind[numb].IndBuffer, True)
        SetIndexBuffer((2 * numb) + 1, Ind[numb].ColorIndBuffer, INDICATOR_COLOR_INDEX)
        ArraySetAsSeries(Ind[numb].ColorIndBuffer, True)
        PlotIndexSetInteger(numb, PLOT_DRAW_TYPE, PlotIndexGetInteger(0, PLOT_DRAW_TYPE))
        PlotIndexSetInteger(numb, PLOT_LINE_STYLE, PlotIndexGetInteger(0, PLOT_LINE_STYLE))
        PlotIndexSetInteger(numb, PLOT_LINE_WIDTH, PlotIndexGetInteger(0, PLOT_LINE_WIDTH))
        PlotIndexSetInteger(numb, PLOT_COLOR_INDEXES, 3)
        PlotIndexSetInteger(numb, PLOT_LINE_COLOR, 0, PlotIndexGetInteger(0, PLOT_LINE_COLOR, 0))
        PlotIndexSetInteger(numb, PLOT_LINE_COLOR, 1, PlotIndexGetInteger(0, PLOT_LINE_COLOR, 1))
        PlotIndexSetInteger(numb, PLOT_LINE_COLOR, 2, PlotIndexGetInteger(0, PLOT_LINE_COLOR, 2))
        PlotIndexSetInteger(numb, PLOT_SHOW_DATA, False)
    shortname = Box("")
    StringConcatenate(shortname, 'iMFI X', 20, '(', StartMFIPeriod, ',', step, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, MidLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrLimeGreen)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_SOLID)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASH)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_SOLID)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    for numb in range(0, 20):
        if BarsCalculated(Ind_Handle[numb]) < min_rates_total:
            return 0
    for numb in range(0, 20):
        if BarsCalculated(Ind_Handle[numb]) < rates_total:
            return 0
    to_copy = 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    for numb in range(0, 20):
        if CopyBuffer(Ind_Handle[numb], 0, 0, to_copy, Ind[numb].IndBuffer) <= 0:
            return 0
    for bar in range(limit, 0 - 1, -1):
        for numb in range(0, 20):
            clr = _int(1.0)
            if Ind[numb].IndBuffer[bar] > HighLevel:
                clr = _int(0.0)
            elif Ind[numb].IndBuffer[bar] < LowLevel:
                clr = _int(2.0)
            Ind[numb].ColorIndBuffer[bar] = clr
    return rates_total

# ---- global variables initialised from expressions
Ind = Arr(20, 0, dyn=False, factory=CIndicatorsBuffers)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorMFIX20(_MQL5Indicator):
    name = 'ColorMFI_X20'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'StartMFIPeriod': 5,  # стартовый период
        'step': 1,  # шаг периода
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём
        'HighLevel': 60,  # уровень перекупленности
        'MidLevel': 50,  # уровень середины
        'LowLevel': 40,  # уровень перепроданности
    }

