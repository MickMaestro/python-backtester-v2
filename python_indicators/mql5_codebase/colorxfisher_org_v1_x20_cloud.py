"""ColorXFisher_org_v1_X20_Cloud — converted from MQL5: MQL5 Indicators/ColorXFisher_org_v1_X20_Cloud/ColorXFisher_org_v1_X20_Cloud.mq5

ColorXFisher_org_v1_X20
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 44, 'indicator_plots': 22}, 'types': {1: 7, 2: 7, 3: 8}, 'colors': {1: [14417815], 2: [16759295], 3: [16748574, 8421504, 16711935]}, 'widths': {3: 1}, 'styles': {3: 0}, 'labels': {1: 'Upper XFisher_org_v1', 2: 'Lower XFisher_org_v1'}, 'levels': [], 'description': ['ColorXFisher_org_v1_X20'], 'name': 'ColorXFisher_org_v1_X20_Cloud', 'source': 'MQL5 Indicators/ColorXFisher_org_v1_X20_Cloud/ColorXFisher_org_v1_X20_Cloud.mq5', 'folder': 'ColorXFisher_org_v1_X20_Cloud', 'inputs': [{'mql': 'FLength', 'py': 'FLength', 'param': 'FLength', 'type': 'uint', 'default': 3, 'label': 'стартовая глубина усреднения', 'sinput': False}, {'mql': 'step', 'py': 'step', 'param': 'step', 'type': 'uint', 'default': 1, 'label': 'шаг изменения глубины усреднения', 'sinput': False}, {'mql': 'MA_SMethod', 'py': 'MA_SMethod', 'param': 'MA_SMethod', 'type': 'int', 'default': 4, 'label': 'Метод сглаживания', 'sinput': False}, {'mql': 'MA_Length', 'py': 'MA_Length', 'param': 'MA_Length', 'type': 'uint', 'default': 3, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'MA_Phase', 'py': 'MA_Phase', 'param': 'MA_Phase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'HighLevelM', 'py': 'HighLevelM', 'param': 'HighLevelM', 'type': 'double', 'default': 2.30001, 'label': 'уровень максимальной перекупленности', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'double', 'default': 1.0001, 'label': 'уровень перекупленности', 'sinput': False}, {'mql': 'MidLevel', 'py': 'MidLevel', 'param': 'MidLevel', 'type': 'double', 'default': 0.0, 'label': 'уровень середины', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'double', 'default': -1.0001, 'label': 'уровень перепроданности', 'sinput': False}, {'mql': 'LowLevelM', 'py': 'LowLevelM', 'param': 'LowLevelM', 'type': 'double', 'default': -2.3001, 'label': 'уровень минимальной перепроданности', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum ENUM_APPLIED_PRICE_
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
_enum('ENUM_APPLIED_PRICE_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
FLength = _input('FLength', 3)  # стартовая глубина усреднения
step = _input('step', 1)  # шаг изменения глубины усреднения
MA_SMethod = _input('MA_SMethod', MODE_JJMA)  # Метод сглаживания
MA_Length = _input('MA_Length', 3)  # Глубина сглаживания
MA_Phase = _input('MA_Phase', 15)  # параметр сглаживания,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
HighLevelM = _input('HighLevelM', 2.30001)  # уровень максимальной перекупленности
HighLevel = _input('HighLevel', 1.0001)  # уровень перекупленности
MidLevel = _input('MidLevel', 0.0)  # уровень середины
LowLevel = _input('LowLevel', -1.0001)  # уровень перепроданности
LowLevelM = _input('LowLevelM', -2.3001)  # уровень минимальной перепроданности
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
    min_rates_total = _int(FLength + (step * (20 - 1))) + 1
    min_rates_total += GetStartBars(MA_SMethod, MA_Length, MA_Phase)
    IndInit(0, UpUpBuffer, INDICATOR_DATA)
    IndInit(1, UpDnBuffer, INDICATOR_DATA)
    PlotInit(0, EMPTY_VALUE, min_rates_total, 0)
    IndInit(2, DnUpBuffer, INDICATOR_DATA)
    IndInit(3, DnDnBuffer, INDICATOR_DATA)
    PlotInit(1, EMPTY_VALUE, min_rates_total, 0)
    period = FLength
    for numb in range(0, 20):
        period += step
        Ind_Handle[numb] = iCustom(None, 0, 'XFisher_org_v1', period, MA_SMethod, MA_Length, MA_Phase, IPC, 0)
        if Ind_Handle[numb] == INVALID_HANDLE:
            Print(' Не удалось получить хендл индикатора XFisher_org_v1 ', numb)
        shortname = Box('')
        StringConcatenate(shortname, 'Fisher_org_v1 X', 20, '*', period, ')')
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
    StringConcatenate(shortname, 'ColorXFisher_org_v1 X', 20, '*', FLength, '(', step, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, MidLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrMediumSeaGreen)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrRed)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_SOLID)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_SOLID)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_SOLID)

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
        UpUpBuffer[bar] = HighLevelM
        UpDnBuffer[bar] = HighLevel
        DnUpBuffer[bar] = LowLevel
        DnDnBuffer[bar] = LowLevelM
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


class ColorXFisherOrgV1X20Cloud(_MQL5Indicator):
    name = 'ColorXFisher_org_v1_X20_Cloud'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FLength': 3,  # стартовая глубина усреднения
        'step': 1,  # шаг изменения глубины усреднения
        'MA_SMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод сглаживания
        'MA_Length': 3,  # Глубина сглаживания
        'MA_Phase': 15,  # параметр сглаживания,
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'HighLevelM': 2.30001,  # уровень максимальной перекупленности
        'HighLevel': 1.0001,  # уровень перекупленности
        'MidLevel': 0.0,  # уровень середины
        'LowLevel': -1.0001,  # уровень перепроданности
        'LowLevelM': -2.3001,  # уровень минимальной перепроданности
    }

