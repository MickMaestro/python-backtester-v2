"""ColorRSI_X20_Cloud_HTF — converted from MQL5: MQL5 Indicators/ColorRSI_X20_Cloud_HTF/ColorRSI_X20_Cloud_HTF.mq5

ColorRSI_X20_Cloud с фиксированным во входных параметрах таймфреймом
Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'separate', 'indicator_buffers': 44, 'indicator_plots': 22}, 'types': {1: 7, 2: 7, 3: 8}, 'colors': {1: [16758711], 2: [16759295], 3: [8388352, 8421504, 255]}, 'widths': {3: 2}, 'styles': {3: 0}, 'labels': {1: 'Upper XFisher_org_v1', 2: 'Lower XFisher_org_v1'}, 'levels': [], 'description': ['ColorRSI_X20_Cloud с фиксированным во входных параметрах таймфреймом'], 'name': 'ColorRSI_X20_Cloud_HTF', 'source': 'MQL5 Indicators/ColorRSI_X20_Cloud_HTF/ColorRSI_X20_Cloud_HTF.mq5', 'folder': 'ColorRSI_X20_Cloud_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика индикатора', 'sinput': False}, {'mql': 'StartRSIPeriod', 'py': 'StartRSIPeriod', 'param': 'StartRSIPeriod', 'type': 'uint', 'default': 5, 'label': 'стартовый период', 'sinput': False}, {'mql': 'step', 'py': 'step', 'param': 'step', 'type': 'uint', 'default': 1, 'label': 'шаг периода', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': 'цена', 'sinput': False}, {'mql': 'HighLevelM', 'py': 'HighLevelM', 'param': 'HighLevelM', 'type': 'uint', 'default': 80, 'label': 'уровень максимальной перекупленности', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'uint', 'default': 60, 'label': 'уровень перекупленности', 'sinput': False}, {'mql': 'MidLevel', 'py': 'MidLevel', 'param': 'MidLevel', 'type': 'uint', 'default': 50, 'label': 'уровень середины', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'uint', 'default': 40, 'label': 'уровень перепроданности', 'sinput': False}, {'mql': 'LowLevelM', 'py': 'LowLevelM', 'param': 'LowLevelM', 'type': 'uint', 'default': 20, 'label': 'уровень минимальной перепроданности', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика индикатора
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
min_rates_total = 0
Ind_Handle = 0

class CIndicatorsBuffers(MqlObject):
    _q_fields = ('IndBuffer', 'ColorIndBuffer')
    def __init__(self, *args):
        self.IndBuffer = Arr(0, 0.0)
        self.ColorIndBuffer = Arr(0, 0.0)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    min_rates_total = 2
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'ColorRSI_X20_Cloud', StartRSIPeriod, step, RSIPrice, HighLevelM, HighLevel, MidLevel, LowLevel, LowLevelM)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ColorRSI_X20_Cloud')
        return INIT_FAILED
    IndInit(0, UpUpBuffer, INDICATOR_DATA)
    IndInit(1, UpDnBuffer, INDICATOR_DATA)
    PlotInit(0, 0.0, min_rates_total, 0)
    IndInit(2, DnUpBuffer, INDICATOR_DATA)
    IndInit(3, DnDnBuffer, INDICATOR_DATA)
    PlotInit(1, 0.0, min_rates_total, 0)
    period = StartRSIPeriod
    for numb in range(0, 20):
        period += step
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
    StringConcatenate(shortname, 'ColorRSI_X20_Cloud', '(', GetStringTimeframe(TimeFrame), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
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
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Comment('')
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if not TimeFramesCheck('ColorRSI_X20_Cloud', TimeFrame):
        return 0
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    ArraySetAsSeries(time, True)
    for numb in range(0, 20):
        count = 4 + (2 * numb)
        if not CountIndicator(count, "", TimeFrame, Ind_Handle, count, Ind[numb].IndBuffer, time, rates_total, prev_calculated, min_rates_total):
            return 0
        if not CountIndicator(count + 1, "", TimeFrame, Ind_Handle, count + 1, Ind[numb].ColorIndBuffer, time, rates_total, prev_calculated, min_rates_total):
            return 0
    if not CountIndicator(0, "", TimeFrame, Ind_Handle, 0, UpUpBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(1, "", TimeFrame, Ind_Handle, 1, UpDnBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(2, "", TimeFrame, Ind_Handle, 2, DnUpBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    if not CountIndicator(3, "", TimeFrame, Ind_Handle, 3, DnDnBuffer, time, rates_total, prev_calculated, min_rates_total):
        return 0
    return rates_total

def IndInit(Number, Buffer, Type):
    SetIndexBuffer(Number, Buffer, Type)
    ArraySetAsSeries(Buffer, True)

def PlotInit(Number, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(Number, PLOT_SHIFT, nShift)
    PlotIndexSetInteger(Number, PLOT_SHOW_DATA, False)

def CountIndicator(Numb, Symb, TFrame, IndHandle, BuffNumb, IndBuf, Time, Rates_Total, Prev_Calculated, Min_Rates_Total):
    IndTime = Arr(1, 0, dyn=False)
    limit = 0
    if Prev_Calculated > Rates_Total or Prev_Calculated <= 0:
        limit = Rates_Total - Min_Rates_Total - 1
        _s_CountIndicator_LastCountBar[Numb] = limit
    else:
        limit = _s_CountIndicator_LastCountBar[Numb] + Rates_Total - Prev_Calculated
    for bar in range(limit, 0 - 1, -1):
        if CopyTime(Symbol(), TFrame, _DT(Time[bar]), 1, IndTime) <= 0:
            return (0 != 0)
        if Time[bar] >= IndTime[0] and Time[bar + 1] < IndTime[0]:
            _s_CountIndicator_LastCountBar[Numb] = bar
            Arr_ = Arr(1, 0.0, dyn=False)
            if CopyBuffer(IndHandle, BuffNumb, _DT(Time[bar]), 1, Arr_) <= 0:
                return (0 != 0)
            IndBuf[bar] = Arr_[0]
        else:
            IndBuf[bar] = IndBuf[bar + 1]
    return True

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Comment('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика! \n Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- global variables initialised from expressions
Ind = Arr(20, 0, dyn=False, factory=CIndicatorsBuffers)

# ---- static local variables
_s_CountIndicator_LastCountBar = Arr(44, 0, dyn=False)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorRSIX20CloudHTF(_MQL5Indicator):
    name = 'ColorRSI_X20_Cloud_HTF'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика индикатора
        'StartRSIPeriod': 5,  # стартовый период
        'step': 1,  # шаг периода
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # цена
        'HighLevelM': 80,  # уровень максимальной перекупленности
        'HighLevel': 60,  # уровень перекупленности
        'MidLevel': 50,  # уровень середины
        'LowLevel': 40,  # уровень перепроданности
        'LowLevelM': 20,  # уровень минимальной перепроданности
    }

