"""ColorRSI_X20_Cloud — converted from MQL5: MQL5 Indicators/ColorRSI_X20_Cloud_HTF/ColorRSI_X20_Cloud.mq5

Двадцать индикаторов RSI в одном окне
Copyright: Copyright © 2010, Ivan Kornilov; Link: excelf@gmail.com; Version: 1.21

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Ivan Kornilov', 'link': 'excelf@gmail.com', 'version': '1.21', 'window': 'separate', 'indicator_buffers': 44, 'indicator_plots': 22}, 'types': {1: 7, 2: 7, 3: 8}, 'colors': {1: [16758711], 2: [16759295], 3: [8388352, 8421504, 255]}, 'widths': {3: 1}, 'styles': {3: 0}, 'labels': {1: 'Upper XFisher_org_v1', 2: 'Lower XFisher_org_v1'}, 'levels': [], 'description': ['Двадцать индикаторов RSI в одном окне'], 'name': 'ColorRSI_X20_Cloud', 'source': 'MQL5 Indicators/ColorRSI_X20_Cloud_HTF/ColorRSI_X20_Cloud.mq5', 'folder': 'ColorRSI_X20_Cloud_HTF', 'inputs': [{'mql': 'StartRSIPeriod', 'py': 'StartRSIPeriod', 'param': 'StartRSIPeriod', 'type': 'uint', 'default': 5, 'label': 'стартовый период', 'sinput': False}, {'mql': 'step', 'py': 'step', 'param': 'step', 'type': 'uint', 'default': 1, 'label': 'шаг периода', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': 'цена', 'sinput': False}, {'mql': 'HighLevelM', 'py': 'HighLevelM', 'param': 'HighLevelM', 'type': 'uint', 'default': 80, 'label': 'уровень максимальной перекупленности', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'uint', 'default': 60, 'label': 'уровень перекупленности', 'sinput': False}, {'mql': 'MidLevel', 'py': 'MidLevel', 'param': 'MidLevel', 'type': 'uint', 'default': 50, 'label': 'уровень середины', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'uint', 'default': 40, 'label': 'уровень перепроданности', 'sinput': False}, {'mql': 'LowLevelM', 'py': 'LowLevelM', 'param': 'LowLevelM', 'type': 'uint', 'default': 20, 'label': 'уровень минимальной перепроданности', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
StartRSIPeriod = _input('StartRSIPeriod', 5)  # стартовый период
step = _input('step', 1)  # шаг периода
RSIPrice = _input('RSIPrice', PRICE_CLOSE)  # цена
HighLevelM = _input('HighLevelM', 80)  # уровень максимальной перекупленности
HighLevel = _input('HighLevel', 60)  # уровень перекупленности
MidLevel = _input('MidLevel', 50)  # уровень середины
LowLevel = _input('LowLevel', 40)  # уровень перепроданности
LowLevelM = _input('LowLevelM', 20)  # уровень минимальной перепроданности
UpUpBuffer = Arr(0, 0.0)
UpDnBuffer = Arr(0, 0.0)
DnUpBuffer = Arr(0, 0.0)
DnDnBuffer = Arr(0, 0.0)
Ind_Handle = Arr(20, 0, dyn=False)
min_rates_total = 0

class CIndicatorsBuffers(MqlObject):
    _q_fields = ('IndBuffer', 'ColorIndBuffer')
    def __init__(self, *args):
        self.IndBuffer = Arr(0, 0.0)
        self.ColorIndBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = _int(StartRSIPeriod + (step * (20 - 1))) + 1
    Maxrange = StartRSIPeriod + (20 * (step - 1 + 1) * 2)
    IndInit(0, UpUpBuffer, INDICATOR_DATA)
    IndInit(1, UpDnBuffer, INDICATOR_DATA)
    PlotInit(0, EMPTY_VALUE, min_rates_total, 0)
    IndInit(2, DnUpBuffer, INDICATOR_DATA)
    IndInit(3, DnDnBuffer, INDICATOR_DATA)
    PlotInit(1, EMPTY_VALUE, min_rates_total, 0)
    period = StartRSIPeriod
    for numb in range(0, 20):
        period += step
        Ind_Handle[numb] = iRSI(Symbol(), 0, period, RSIPrice)
        if Ind_Handle[numb] == INVALID_HANDLE:
            Print(' Не удалось получить хендл индикатора iRSI ', numb)
        shortname = Box('')
        StringConcatenate(shortname, 'iRSI X', 20, '*', period, ')')
        numb1 = numb + 2
        PlotIndexSetString(numb1, PLOT_LABEL, shortname.v)
        PlotIndexSetDouble(numb1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
        PlotIndexSetInteger(numb1, PLOT_DRAW_BEGIN, min_rates_total)
        SetIndexBuffer((2 * numb) + 4, Ind[numb].IndBuffer, INDICATOR_DATA)
        ArraySetAsSeries(Ind[numb].IndBuffer, True)
        SetIndexBuffer((2 * numb) + 1 + 4, Ind[numb].ColorIndBuffer, INDICATOR_COLOR_INDEX)
        ArraySetAsSeries(Ind[numb].ColorIndBuffer, True)
        PlotIndexSetInteger(numb1, PLOT_DRAW_TYPE, PlotIndexGetInteger(2, PLOT_DRAW_TYPE))
        PlotIndexSetInteger(numb1, PLOT_LINE_STYLE, PlotIndexGetInteger(2, PLOT_LINE_STYLE))
        PlotIndexSetInteger(numb1, PLOT_LINE_WIDTH, PlotIndexGetInteger(2, PLOT_LINE_WIDTH))
        PlotIndexSetInteger(numb1, PLOT_COLOR_INDEXES, 3)
        PlotIndexSetInteger(numb1, PLOT_LINE_COLOR, 0, PlotIndexGetInteger(2, PLOT_LINE_COLOR, 0))
        PlotIndexSetInteger(numb1, PLOT_LINE_COLOR, 1, PlotIndexGetInteger(2, PLOT_LINE_COLOR, 1))
        PlotIndexSetInteger(numb1, PLOT_LINE_COLOR, 2, PlotIndexGetInteger(2, PLOT_LINE_COLOR, 2))
        PlotIndexSetInteger(numb1, PLOT_SHOW_DATA, False)
    shortname = Box("")
    StringConcatenate(shortname, 'iRSI X', 20, '_Cloud(', StartRSIPeriod, ',', step, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 5)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevelM)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, MidLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 3, LowLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 4, LowLevelM)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrDodgerBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrDodgerBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrBlueViolet)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 3, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 4, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_SOLID)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASH)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 3, STYLE_SOLID)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 4, STYLE_DASHDOTDOT)

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    PlotIndexSetInteger(Number, PLOT_SHOW_DATA, False)

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
        UpUpBuffer[bar] = float(HighLevelM)
        UpDnBuffer[bar] = float(HighLevel)
        DnUpBuffer[bar] = float(LowLevel)
        DnDnBuffer[bar] = float(LowLevelM)
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


class ColorRSIX20Cloud(_MQL5Indicator):
    name = 'ColorRSI_X20_Cloud'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'StartRSIPeriod': 5,  # стартовый период
        'step': 1,  # шаг периода
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # цена
        'HighLevelM': 80,  # уровень максимальной перекупленности
        'HighLevel': 60,  # уровень перекупленности
        'MidLevel': 50,  # уровень середины
        'LowLevel': 40,  # уровень перепроданности
        'LowLevelM': 20,  # уровень минимальной перепроданности
    }

