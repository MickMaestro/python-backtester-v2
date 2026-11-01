"""tema_customcandle — converted from MQL5: MQL5 Indicators/TEMA_CUSTOMCandle/tema_customcandle.mq5

TEMA_CUSTOMCandle
Copyright: Copyright © 2015, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [9639167, 8421504, 16711680]}, 'widths': {}, 'styles': {}, 'labels': {1: 'TEMA_CUSTOM Open;TEMA_CUSTOM High;TEMA_CUSTOM Low;TEMA_CUSTOM Close'}, 'levels': [], 'description': ['TEMA_CUSTOMCandle'], 'name': 'tema_customcandle', 'source': 'MQL5 Indicators/TEMA_CUSTOMCandle/tema_customcandle.mq5', 'folder': 'TEMA_CUSTOMCandle', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 1, 'label': 'Метод усреднения первого сглаживания', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'int', 'default': 12, 'label': 'Глубина  первого сглаживания', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'Параметр первого сглаживания', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 1, 'label': 'Метод усреднения второго сглаживания', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'int', 'default': 5, 'label': 'Глубина  второго сглаживания', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 15, 'label': 'Параметр второго сглаживания', 'sinput': False}, {'mql': 'MA_Method3', 'py': 'MA_Method3', 'param': 'MA_Method3', 'type': 'int', 'default': 1, 'label': 'Метод усреднения третьего сглаживания', 'sinput': False}, {'mql': 'Length3', 'py': 'Length3', 'param': 'Length3', 'type': 'int', 'default': 5, 'label': 'Глубина третьего сглаживания', 'sinput': False}, {'mql': 'Phase3', 'py': 'Phase3', 'param': 'Phase3', 'type': 'int', 'default': 15, 'label': 'Параметр третьего сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 5, 'label': 'Ценовая константа, по которой производится расчет индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
MA_Method1 = _input('MA_Method1', MODE_EMA_)  # Метод усреднения первого сглаживания
Length1 = _input('Length1', 12)  # Глубина  первого сглаживания
Phase1 = _input('Phase1', 15)  # Параметр первого сглаживания
MA_Method2 = _input('MA_Method2', MODE_EMA)  # Метод усреднения второго сглаживания
Length2 = _input('Length2', 5)  # Глубина  второго сглаживания
Phase2 = _input('Phase2', 15)  # Параметр второго сглаживания
MA_Method3 = _input('MA_Method3', MODE_EMA)  # Метод усреднения третьего сглаживания
Length3 = _input('Length3', 5)  # Глубина третьего сглаживания
Phase3 = _input('Phase3', 15)  # Параметр третьего сглаживания
IPC = _input('IPC', PRICE_MEDIAN)  # Ценовая константа, по которой производится расчет индикатора
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = Arr(4, 0, dyn=False)

def OnInit():
    global min_rates_total
    min_rates_total = 30
    Ind_Handle[0] = iCustom(None, 0, 'TEMA_CUSTOM', MA_Method1, Length1, Phase1, MA_Method2, Length2, Phase2, MA_Method3, Length3, Phase3, PRICE_OPEN_, 0, PriceShift)
    if Ind_Handle[0] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iTEMA_CUSTOM[' + _str(0) + ']!')
        return INIT_FAILED
    Ind_Handle[1] = iCustom(None, 0, 'TEMA_CUSTOM', MA_Method1, Length1, Phase1, MA_Method2, Length2, Phase2, MA_Method3, Length3, Phase3, PRICE_HIGH_, 0, PriceShift)
    if Ind_Handle[1] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iTEMA_CUSTOM[' + _str(1) + ']!')
        return INIT_FAILED
    Ind_Handle[2] = iCustom(None, 0, 'TEMA_CUSTOM', MA_Method1, Length1, Phase1, MA_Method2, Length2, Phase2, MA_Method3, Length3, Phase3, PRICE_LOW_, 0, PriceShift)
    if Ind_Handle[2] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iTEMA_CUSTOM[' + _str(2) + ']!')
        return INIT_FAILED
    Ind_Handle[3] = iCustom(None, 0, 'TEMA_CUSTOM', MA_Method1, Length1, Phase1, MA_Method2, Length2, Phase2, MA_Method3, Length3, Phase3, PRICE_CLOSE_, 0, PriceShift)
    if Ind_Handle[3] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iTEMA_CUSTOM[' + _str(3) + ']!')
        return INIT_FAILED
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'TEMA_CUSTOMCandle'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (((BarsCalculated(Ind_Handle[0]) < rates_total or BarsCalculated(Ind_Handle[1]) < rates_total) or BarsCalculated(Ind_Handle[2]) < rates_total) or BarsCalculated(Ind_Handle[3]) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ind_Handle[0], 0, 0, to_copy, ExtOpenBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[1], 0, 0, to_copy, ExtHighBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[2], 0, 0, to_copy, ExtLowBuffer) <= 0:
        return 0
    if CopyBuffer(Ind_Handle[3], 0, 0, to_copy, ExtCloseBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Max = MathMax(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        Min = MathMin(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        ExtHighBuffer[bar] = MathMax(Max, ExtHighBuffer[bar])
        ExtLowBuffer[bar] = MathMin(Min, ExtLowBuffer[bar])
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 2.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TemaCustomcandle(_MQL5Indicator):
    name = 'tema_customcandle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Метод усреднения первого сглаживания
        'Length1': 12,  # Глубина  первого сглаживания
        'Phase1': 15,  # Параметр первого сглаживания
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Метод усреднения второго сглаживания
        'Length2': 5,  # Глубина  второго сглаживания
        'Phase2': 15,  # Параметр второго сглаживания
        'MA_Method3': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=1),  # Метод усреднения третьего сглаживания
        'Length3': 5,  # Глубина третьего сглаживания
        'Phase3': 15,  # Параметр третьего сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=5),  # Ценовая константа, по которой производится расчет индикатора
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
    }

