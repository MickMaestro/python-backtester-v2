"""UltraAbsolutelyNoLagLwma — converted from MQL5: MQL5 Indicators/UltraAbsolutelyNoLagLwma/UltraAbsolutelyNoLagLwma.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 11}, 'colors': {1: [8421504, 16711935, 11823615, 255, 2763429, 3329330, 8421376, 65280, 10025880]}, 'widths': {1: 4}, 'styles': {}, 'labels': {1: 'Ultra AbsolutelyNoLagLwma'}, 'levels': [], 'description': [], 'name': 'UltraAbsolutelyNoLagLwma', 'source': 'MQL5 Indicators/UltraAbsolutelyNoLagLwma/UltraAbsolutelyNoLagLwma.mq5', 'folder': 'UltraAbsolutelyNoLagLwma', 'inputs': [{'mql': 'FLength', 'py': 'FLength', 'param': 'FLength', 'type': 'uint', 'default': 7, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'W_Method', 'py': 'W_Method', 'param': 'W_Method', 'type': 'int', 'default': 4, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'StartLength', 'py': 'StartLength', 'param': 'StartLength', 'type': 'int', 'default': 3, 'label': 'Стартовый период усреднения', 'sinput': False}, {'mql': 'WPhase', 'py': 'WPhase', 'param': 'WPhase', 'type': 'int', 'default': 100, 'label': 'Параметр усреднения', 'sinput': False}, {'mql': 'Step', 'py': 'Step', 'param': 'Step', 'type': 'uint', 'default': 5, 'label': 'Шаг изменения периода', 'sinput': False}, {'mql': 'StepsTotal', 'py': 'StepsTotal', 'param': 'StepsTotal', 'type': 'uint', 'default': 10, 'label': 'Количество изменений периода', 'sinput': False}, {'mql': 'SmoothMethod', 'py': 'SmoothMethod', 'param': 'SmoothMethod', 'type': 'int', 'default': 4, 'label': 'Метод сглаживания', 'sinput': False}, {'mql': 'SmoothLength', 'py': 'SmoothLength', 'param': 'SmoothLength', 'type': 'int', 'default': 3, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'SmoothPhase', 'py': 'SmoothPhase', 'param': 'SmoothPhase', 'type': 'int', 'default': 100, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'UpLevel', 'py': 'UpLevel', 'param': 'UpLevel', 'type': 'uint', 'default': 80, 'label': 'Уровень перекупленности в %%', 'sinput': False}, {'mql': 'DnLevel', 'py': 'DnLevel', 'param': 'DnLevel', 'type': 'uint', 'default': 20, 'label': 'Уровень перепроданности в %%', 'sinput': False}, {'mql': 'UpLevelsColor', 'py': 'UpLevelsColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Цвет уровня перекупленности', 'sinput': False}, {'mql': 'DnLevelsColor', 'py': 'DnLevelsColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Цвет уровня перепроданности', 'sinput': False}, {'mql': 'Levelstyle', 'py': 'Levelstyle', 'param': 'Levelstyle', 'type': 'int', 'default': 1, 'label': 'Стиль уровней', 'sinput': False}, {'mql': 'LevelsWidth', 'py': 'LevelsWidth', 'param': 'LevelsWidth', 'type': 'int', 'default': 1, 'label': 'Толщина уровней', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

Blue = 0xFF0000  # MQL4 colour name

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

# enum WIDTH
Width_1 = 1
Width_2 = 2
Width_3 = 3
Width_4 = 4
Width_5 = 5
_enum('WIDTH', {1: 'Width_1', 2: 'Width_2', 3: 'Width_3', 4: 'Width_4', 5: 'Width_5'})

# enum STYLE
SOLID_ = 0
DASH_ = 1
DOT_ = 2
DASHDOT_ = 3
DASHDOTDOT_ = 4
_enum('STYLE', {0: 'SOLID_', 1: 'DASH_', 2: 'DOT_', 3: 'DASHDOT_', 4: 'DASHDOTDOT_'})

# ---- inputs and global variables
FLength = _input('FLength', 7)  # глубина сглаживания
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
W_Method = _input('W_Method', MODE_JJMA)  # Метод усреднения
StartLength = _input('StartLength', 3)  # Стартовый период усреднения
WPhase = _input('WPhase', 100)  # Параметр усреднения
Step = _input('Step', 5)  # Шаг изменения периода
StepsTotal = _input('StepsTotal', 10)  # Количество изменений периода
SmoothMethod = _input('SmoothMethod', MODE_JJMA)  # Метод сглаживания
SmoothLength = _input('SmoothLength', 3)  # Глубина сглаживания
SmoothPhase = _input('SmoothPhase', 100)  # Параметр сглаживания
UpLevel = _input('UpLevel', 80)  # Уровень перекупленности в %%
DnLevel = _input('DnLevel', 20)  # Уровень перепроданности в %%
Levelstyle = _input('Levelstyle', DASH_)  # Стиль уровней
LevelsWidth = _input('LevelsWidth', Width_1)  # Толщина уровней
BullsBuffer = Arr(0, 0.0)
BearsBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
period = Arr(0, 0)
invelue0 = Arr(0, 0.0)
invelue1 = Arr(0, 0.0)
dUpLevel = 0.0
dDnLevel = 0.0
StTot1 = 0
StTot2 = 0
min_rates_total = 0
min_rates_lwma2 = 0
min_rates_xma = 0
Count = Arr(0, 0)
Price = Arr(0, 0.0)
Lwma = Arr(0, 0.0)

def Recount_ArrayZeroPos(CoArr, Size):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def OnInit():
    global StTot1, StTot2, dDnLevel, dUpLevel, min_rates_total, min_rates_xma
    size = _int(StepsTotal + 3)
    if ArrayResize(XMA, size) < size:
        Print('Не удалось распределить память под массив XMA[]')
    size -= 2
    if ArrayResize(invelue0, size) < size:
        Print('Не удалось распределить память под массив invelue0[]')
    if ArrayResize(invelue1, size) < size:
        Print('Не удалось распределить память под массив invelue1[]')
    if ArrayResize(period, size) < size:
        Print('Не удалось распределить память под массив period[]')
    ZeroMemory(invelue0)
    ZeroMemory(invelue1)
    ZeroMemory(period)
    for sm in range(_int(StepsTotal), 0 - 1, -1):
        period[sm] = _int(StartLength + (sm * Step))
    dUpLevel = (StepsTotal * UpLevel) / 100.0
    dDnLevel = (StepsTotal * DnLevel) / 100.0
    XMA[0].XMALengthCheck('StartLength', StartLength)
    XMA[0].XMAPhaseCheck('WPhase', WPhase, W_Method)
    XMA[0].XMALengthCheck('SmoothLength', SmoothLength)
    XMA[0].XMAPhaseCheck('SmoothPhase', SmoothPhase, SmoothMethod)
    min_rates_total = _int(FLength * 2.0)
    min_rates_xma = min_rates_lwma2 + XMA[0].GetStartBars(W_Method, StartLength + (Step * StepsTotal), WPhase) + 1
    min_rates_total = min_rates_xma + XMA[0].GetStartBars(SmoothMethod, SmoothLength, SmoothPhase)
    StTot1 = StepsTotal + 1
    StTot2 = StepsTotal + 2
    ArrayResize(Count, FLength)
    ArrayResize(Price, FLength)
    ArrayResize(Lwma, FLength)
    SetIndexBuffer(0, BullsBuffer, INDICATOR_DATA)
    ArraySetAsSeries(BullsBuffer, True)
    SetIndexBuffer(1, BearsBuffer, INDICATOR_DATA)
    ArraySetAsSeries(BearsBuffer, True)
    SetIndexBuffer(2, ColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = 'Ultra AbsolutelyNoLagLwma'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, dUpLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, UpLevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, Levelstyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 0, LevelsWidth)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, dDnLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, DnLevelsColor)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, Levelstyle)
    IndicatorSetInteger(INDICATOR_LEVELWIDTH, 1, LevelsWidth)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    maxbar0 = 0
    maxbar1 = 0
    maxbar2 = 0
    weight = 0
    upsch = 0.0
    dnsch = 0.0
    sum_ = 0.0
    sumw = 0.0
    lwma2 = 0.0
    maxbar0 = rates_total - 1
    maxbar1 = maxbar0 - min_rates_lwma2
    maxbar2 = maxbar0 - min_rates_xma
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar0
        ArrayInitialize(Count, 0)
        ArrayInitialize(Price, 0.0)
        ArrayInitialize(Lwma, 0.0)
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Price[Count[0]] = PriceSeries(IPC, bar, open, low, high, close)
        sum_ = 0.0
        sumw = 0.0
        for kkk in range(0, _int(FLength)):
            weight = _int(FLength) - kkk
            sumw += weight
            sum_ += weight * Price[Count[kkk]]
        if sumw:
            Lwma[Count[0]] = _fdiv(sum_, sumw)
        else:
            Lwma[Count[0]] = 0.0
        sum_ = 0.0
        sumw = 0.0
        for kkk in range(0, _int(FLength)):
            weight = _int(FLength) - kkk
            sumw += weight
            sum_ += weight * Lwma[Count[kkk]]
        if sumw:
            lwma2 = _fdiv(sum_, sumw)
        else:
            lwma2 = 0.0
        if bar < (rates_total - 1):
            Recount_ArrayZeroPos(Count, FLength)
        for sm in range(_int(StepsTotal), 0 - 1, -1):
            invelue0[sm] = XMA[sm].XMASeries(maxbar1, prev_calculated, rates_total, W_Method, WPhase, period[sm], lwma2, bar, True)
        if bar > maxbar2:
            if bar:
                ArrayCopy(invelue1, invelue0, 0, 0, WHOLE_ARRAY)
            continue
        upsch = 0.0
        dnsch = 0.0
        for sm in range(_int(StepsTotal), 0 - 1, -1):
            if invelue0[sm] > invelue1[sm]:
                upsch += 1
            else:
                dnsch += 1
        BullsBuffer[bar] = XMA[StTot1].XMASeries(maxbar2, prev_calculated, rates_total, SmoothMethod, SmoothPhase, SmoothLength, upsch, bar, True)
        BearsBuffer[bar] = XMA[StTot2].XMASeries(maxbar2, prev_calculated, rates_total, SmoothMethod, SmoothPhase, SmoothLength, dnsch, bar, True)
        if bar:
            ArrayCopy(invelue1, invelue0, 0, 0, WHOLE_ARRAY)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ColorBuffer[bar] = 0.0
        if BullsBuffer[bar] > BearsBuffer[bar]:
            if BullsBuffer[bar] > dUpLevel or BearsBuffer[bar] < dDnLevel:
                if BullsBuffer[bar + 1] <= BullsBuffer[bar]:
                    ColorBuffer[bar] = 7.0
                else:
                    ColorBuffer[bar] = 8.0
            else:
                if BullsBuffer[bar + 1] <= BullsBuffer[bar]:
                    ColorBuffer[bar] = 5.0
                else:
                    ColorBuffer[bar] = 6.0
        if BullsBuffer[bar] < BearsBuffer[bar]:
            if BullsBuffer[bar] < dDnLevel or BearsBuffer[bar] > dUpLevel:
                if BearsBuffer[bar + 1] <= BearsBuffer[bar]:
                    ColorBuffer[bar] = 1.0
                else:
                    ColorBuffer[bar] = 2.0
            else:
                if BearsBuffer[bar + 1] <= BearsBuffer[bar]:
                    ColorBuffer[bar] = 3.0
                else:
                    ColorBuffer[bar] = 4.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA = Arr(0, 0, factory=CXMA)
UpLevelsColor = _input('UpLevelsColor', _uint(Blue))  # Цвет уровня перекупленности
DnLevelsColor = _input('DnLevelsColor', _uint(Blue))  # Цвет уровня перепроданности

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class UltraAbsolutelyNoLagLwma(_MQL5Indicator):
    name = 'UltraAbsolutelyNoLagLwma'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FLength': 7,  # глубина сглаживания
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'W_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод усреднения
        'StartLength': 3,  # Стартовый период усреднения
        'WPhase': 100,  # Параметр усреднения
        'Step': 5,  # Шаг изменения периода
        'StepsTotal': 10,  # Количество изменений периода
        'SmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод сглаживания
        'SmoothLength': 3,  # Глубина сглаживания
        'SmoothPhase': 100,  # Параметр сглаживания
        'UpLevel': 80,  # Уровень перекупленности в %%
        'DnLevel': 20,  # Уровень перепроданности в %%
        'Levelstyle': _Choice({0: 'Сплошная линия', 1: 'Штриховая линия', 2: 'Пунктирная линия', 3: 'Штрих-пунктирная линия', 4: 'Штрих-пунктирная линия с двойными точками'}, default=1),  # Стиль уровней
        'LevelsWidth': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=1),  # Толщина уровней
    }

