"""forexline_htf — converted from MQL5: MQL5 Indicators/ForexLine_HTF/forexline_htf.mq5

Copyright: Copyright © 2016, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [3329330, 8421504, 16711935]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'ForexLine'}, 'levels': [], 'description': [], 'name': 'forexline_htf', 'source': 'MQL5 Indicators/ForexLine_HTF/forexline_htf.mq5', 'folder': 'ForexLine_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16388, 'label': 'Период графика', 'sinput': False}, {'mql': 'MA_Method11', 'py': 'MA_Method11', 'param': 'MA_Method11', 'type': 'int', 'default': 3, 'label': 'Метод усреднения первого сглаживания мувинга 1', 'sinput': False}, {'mql': 'Length11', 'py': 'Length11', 'param': 'Length11', 'type': 'int', 'default': 5, 'label': 'Глубина  первого сглаживания мувинга 1', 'sinput': False}, {'mql': 'Phase11', 'py': 'Phase11', 'param': 'Phase11', 'type': 'int', 'default': 15, 'label': 'Параметр первого сглаживания', 'sinput': False}, {'mql': 'MA_Method12', 'py': 'MA_Method12', 'param': 'MA_Method12', 'type': 'int', 'default': 3, 'label': 'Метод усреднения второго сглаживания', 'sinput': False}, {'mql': 'Length12', 'py': 'Length12', 'param': 'Length12', 'type': 'int', 'default': 10, 'label': 'Глубина  второго сглаживания  мувинга 1', 'sinput': False}, {'mql': 'Phase12', 'py': 'Phase12', 'param': 'Phase12', 'type': 'int', 'default': 15, 'label': 'Параметр второго сглаживания  мувинга 1', 'sinput': False}, {'mql': 'IPC1', 'py': 'IPC1', 'param': 'IPC1', 'type': 'int', 'default': 1, 'label': 'Ценовая константа мувинга 1', 'sinput': False}, {'mql': 'MA_Method21', 'py': 'MA_Method21', 'param': 'MA_Method21', 'type': 'int', 'default': 3, 'label': 'Метод усреднения первого сглаживания мувинга 2', 'sinput': False}, {'mql': 'Length21', 'py': 'Length21', 'param': 'Length21', 'type': 'int', 'default': 20, 'label': 'Глубина  первого сглаживания мувинга 2', 'sinput': False}, {'mql': 'Phase21', 'py': 'Phase21', 'param': 'Phase21', 'type': 'int', 'default': 15, 'label': 'Параметр первого сглаживания мувинга 2,', 'sinput': False}, {'mql': 'MA_Method22', 'py': 'MA_Method22', 'param': 'MA_Method22', 'type': 'int', 'default': 3, 'label': 'Метод усреднения второго сглаживания мувинга 2', 'sinput': False}, {'mql': 'Length22', 'py': 'Length22', 'param': 'Length22', 'type': 'int', 'default': 20, 'label': 'Глубина  второго сглаживания мувинга 2', 'sinput': False}, {'mql': 'Phase22', 'py': 'Phase22', 'param': 'Phase22', 'type': 'int', 'default': 15, 'label': 'Параметр второго сглаживания', 'sinput': False}, {'mql': 'IPC2', 'py': 'IPC2', 'param': 'IPC2', 'type': 'int', 'default': 1, 'label': 'Ценовая константа мувинга 2', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}, {'mql': 'ReDraw', 'py': 'ReDraw', 'param': 'ReDraw', 'type': 'bool', 'default': True, 'label': 'Повтор отображения инфомации на пустых барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum Smooth_Method
MODE_SMA_ = 0
MODE_EMA_ = 1
MODE_SMMA_ = 2
MODE_LWMA_ = 3
MODE_JJMA = 4
MODE_JurX = 5
MODE_ParMA = 6
MODE_T3 = 7
MODE_VIDYA = 8
MODE_AMA = 9
_enum('Smooth_Method', {0: 'MODE_SMA_', 1: 'MODE_EMA_', 2: 'MODE_SMMA_', 3: 'MODE_LWMA_', 4: 'MODE_JJMA', 5: 'MODE_JurX', 6: 'MODE_ParMA', 7: 'MODE_T3', 8: 'MODE_VIDYA', 9: 'MODE_AMA'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H4)  # Период графика
MA_Method11 = _input('MA_Method11', MODE_LWMA)  # Метод усреднения первого сглаживания мувинга 1
Length11 = _input('Length11', 5)  # Глубина  первого сглаживания мувинга 1
Phase11 = _input('Phase11', 15)  # Параметр первого сглаживания
MA_Method12 = _input('MA_Method12', MODE_LWMA)  # Метод усреднения второго сглаживания
Length12 = _input('Length12', 10)  # Глубина  второго сглаживания  мувинга 1
Phase12 = _input('Phase12', 15)  # Параметр второго сглаживания  мувинга 1
IPC1 = _input('IPC1', PRICE_CLOSE)  # Ценовая константа мувинга 1
MA_Method21 = _input('MA_Method21', MODE_LWMA)  # Метод усреднения первого сглаживания мувинга 2
Length21 = _input('Length21', 20)  # Глубина  первого сглаживания мувинга 2
Phase21 = _input('Phase21', 15)  # Параметр первого сглаживания мувинга 2,
MA_Method22 = _input('MA_Method22', MODE_LWMA)  # Метод усреднения второго сглаживания мувинга 2
Length22 = _input('Length22', 20)  # Глубина  второго сглаживания мувинга 2
Phase22 = _input('Phase22', 15)  # Параметр второго сглаживания
IPC2 = _input('IPC2', PRICE_CLOSE)  # Ценовая константа мувинга 2
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
ReDraw = _input('ReDraw', True)  # Повтор отображения инфомации на пустых барах
min_rates_total = 0
Ind_Handle = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global Ind_Handle, min_rates_total
    min_rates_total = 3
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора ForexLine не может быть меньше периода текущего графика')
        return INIT_FAILED
    Ind_Handle = iCustom(Symbol(), TimeFrame, 'ForexLine', MA_Method11, Length11, Phase11, MA_Method12, Length12, Phase12, IPC1, MA_Method21, Length21, Phase21, MA_Method22, Length22, Phase22, IPC2, 0, PriceShift)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ForexLine')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'ForexLine HTF( ', GetStringTimeframe(TimeFrame), ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
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
        if ReDraw:
            if IndBuffer[bar + 1] != EMPTY_VALUE and IndBuffer[bar] == EMPTY_VALUE:
                IndBuffer[bar] = IndBuffer[bar + 1]
                ColorIndBuffer[bar] = ColorIndBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ForexlineHtf(_MQL5Indicator):
    name = 'forexline_htf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16388),  # Период графика
        'MA_Method11': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # Метод усреднения первого сглаживания мувинга 1
        'Length11': 5,  # Глубина  первого сглаживания мувинга 1
        'Phase11': 15,  # Параметр первого сглаживания
        'MA_Method12': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # Метод усреднения второго сглаживания
        'Length12': 10,  # Глубина  второго сглаживания  мувинга 1
        'Phase12': 15,  # Параметр второго сглаживания  мувинга 1
        'IPC1': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа мувинга 1
        'MA_Method21': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # Метод усреднения первого сглаживания мувинга 2
        'Length21': 20,  # Глубина  первого сглаживания мувинга 2
        'Phase21': 15,  # Параметр первого сглаживания мувинга 2,
        'MA_Method22': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # Метод усреднения второго сглаживания мувинга 2
        'Length22': 20,  # Глубина  второго сглаживания мувинга 2
        'Phase22': 15,  # Параметр второго сглаживания
        'IPC2': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа мувинга 2
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
        'ReDraw': True,  # Повтор отображения инфомации на пустых барах
    }

