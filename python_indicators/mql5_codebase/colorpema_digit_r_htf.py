"""ColorPEMA_Digit_r_HTF — converted from MQL5: MQL5 Indicators/ColorPEMA_Digit_r_HTF/ColorPEMA_Digit_r_HTF.mq5

Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [16711935, 8421504, 16748574]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'ColorPEMA_Digit_r'}, 'levels': [], 'description': [], 'name': 'ColorPEMA_Digit_r_HTF', 'source': 'MQL5 Indicators/ColorPEMA_Digit_r_HTF/ColorPEMA_Digit_r_HTF.mq5', 'folder': 'ColorPEMA_Digit_r_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'период графика', 'sinput': False}, {'mql': 'EmaLength', 'py': 'EmaLength', 'param': 'EmaLength', 'type': 'double', 'default': 50.01, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора по вертикали в пунктах', 'sinput': False}, {'mql': 'Digit', 'py': 'Digit', 'param': 'Digit', 'type': 'uint', 'default': 2, 'label': 'количество разрядов округления', 'sinput': False}, {'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'ColorPEMA_Digit_r', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': 'показывать ценовую метку', 'sinput': False}, {'mql': 'RecountMode', 'py': 'RecountMode', 'param': 'RecountMode', 'type': 'int', 'default': 3, 'label': 'Способ ограничения расчётов индикатора', 'sinput': False}, {'mql': 'CountBars', 'py': 'CountBars', 'param': 'CountBars', 'type': 'uint', 'default': 500, 'label': 'количество баров для расчёта индикатора', 'sinput': False}, {'mql': 'ReCountTime', 'py': 'ReCountTime', 'param': 'ReCountTime', 'type': 'uint', 'default': 60, 'label': 'время в секундах между расчётами индикатора', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum ENUM_RECOUNT_MODE
ONLY_BARS_RECOUNT = 1
ONLY_TIME_RECOUNT = 2
FULL_RECOUNT = 3
_enum('ENUM_RECOUNT_MODE', {1: 'ONLY_BARS_RECOUNT', 2: 'ONLY_TIME_RECOUNT', 3: 'FULL_RECOUNT'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # период графика
EmaLength = _input('EmaLength', 50.01)  # глубина сглаживания
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # cдвиг индикатора по вертикали в пунктах
Digit = _input('Digit', 2)  # количество разрядов округления
SirName = _input('SirName', 'ColorPEMA_Digit_r')  # Первая часть имени графических объектов
ShowPrice = _input('ShowPrice', True)  # показывать ценовую метку
RecountMode = _input('RecountMode', FULL_RECOUNT)  # Способ ограничения расчётов индикатора
CountBars = _input('CountBars', 500)  # количество баров для расчёта индикатора
ReCountTime = _input('ReCountTime', 60)  # время в секундах между расчётами индикатора
min_rates_total = 0
count_bars = 0
Ind_Handle = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, count_bars, min_rates_total
    min_rates_total = 3
    count_bars = _int(MathMax(CountBars, min_rates_total))
    CountBars_htf = 10 + _int(_idiv(CountBars * PeriodSeconds(PERIOD_CURRENT), PeriodSeconds(TimeFrame)))
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'ColorPEMA_Digit_r', EmaLength, IPC, 0, PriceShift, Digit, SirName, ShowPrice, RecountMode, CountBars_htf, ReCountTime)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ColorPEMA_Digit_r')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'ColorPEMA_Digit_r HTF( ', GetStringTimeframe(TimeFrame), ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar, _s_OnCalculate_recount_time
    if not TimeFramesCheck('ColorPEMA_Digit_r_HTF', TimeFrame):
        return 0
    if (prev_calculated > rates_total or prev_calculated <= 0) or prev_calculated != rates_total:
        _s_OnCalculate_recount_time = 0
    _sw1 = RecountMode
    if _sw1 == ONLY_BARS_RECOUNT:
        pass
    else:
        if (TimeCurrent() - _s_OnCalculate_recount_time) < _int(ReCountTime):
            return rates_total
        else:
            _s_OnCalculate_recount_time = TimeCurrent()
    if rates_total < min_rates_total:
        return 0
    if BarsCalculated(Ind_Handle) < Bars(Symbol(), TimeFrame):
        return prev_calculated
    limit = 0
    bar = 0
    Ind = Arr(1, 0.0, dyn=False)
    Col = Arr(1, 0.0, dyn=False)
    IndTime = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    _sw2 = RecountMode
    if _sw2 == ONLY_TIME_RECOUNT:
        pass
    else:
        barx = count_bars
        limit = MathMin(limit, barx)
        barx = rates_total - 1 - barx
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, barx)
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IndBuffer[bar] = EMPTY_VALUE
        ColorIndBuffer[bar] = 1.0
        if CopyTime(Symbol(), TimeFrame, _DT(time[bar]), 1, IndTime) <= 0:
            return 0
        if time[bar] >= IndTime[0] and time[bar + 1] < IndTime[0]:
            _s_OnCalculate_LastCountBar = bar
            if CopyBuffer(Ind_Handle, 0, _DT(time[bar]), 1, Ind) <= 0:
                return 0
            if CopyBuffer(Ind_Handle, 1, _DT(time[bar]), 1, Col) <= 0:
                return 0
            IndBuffer[bar] = Ind[0]
            ColorIndBuffer[bar] = Col[0]
        if IndBuffer[bar + 1] != EMPTY_VALUE and IndBuffer[bar] == EMPTY_VALUE:
            IndBuffer[bar] = IndBuffer[bar + 1]
            ColorIndBuffer[bar] = ColorIndBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def TimeFramesCheck(IndName, TFrame):
    if TFrame < Period() and TFrame != PERIOD_CURRENT:
        Comment('Период графика для индикатора ' + IndName + ' не может быть меньше периода текущего графика! \n Следует изменить входные параметры индикатора!')
        return (0 != 0)
    return True

# ---- static local variables
_s_OnCalculate_recount_time = 0
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorPEMADigitRHTF(_MQL5Indicator):
    name = 'ColorPEMA_Digit_r_HTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # период графика
        'EmaLength': 50.01,  # глубина сглаживания
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # cдвиг индикатора по вертикали в пунктах
        'Digit': 2,  # количество разрядов округления
        'ShowPrice': True,  # показывать ценовую метку
        'RecountMode': _Choice({1: 'Обрезаем только пересчёт баров', 2: 'Обрезаем только пересчёт во времени', 3: 'Полная оптимизация пересчётов'}, default=3),  # Способ ограничения расчётов индикатора
        'CountBars': 500,  # количество баров для расчёта индикатора
        'ReCountTime': 60,  # время в секундах между расчётами индикатора
    }

