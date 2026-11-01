"""EMAVFS_StDev — converted from MQL5: MQL5 Indicators/EMAVFS_StDev/EMAVFS_StDev.mq5

Экспоненциальная скользящая средняя с переменным фактором сглаживания
Copyright: Copyright © 2018, Станислав Булашев; Link: http://stan.okis.ru/file/stan/EMAVFS.pdf

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Станислав Булашев', 'link': 'http://stan.okis.ru/file/stan/EMAVFS.pdf', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 5}, 'types': {1: 8, 2: 5, 3: 5, 4: 5, 5: 5}, 'colors': {1: [16711935, 8421504, 16748574], 2: [255], 3: [16776960], 4: [255], 5: [16776960]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 4, 5: 4}, 'styles': {1: 0}, 'labels': {1: 'EMAVFS', 2: 'Dn_Signal 1', 3: 'Up_Signal 1', 4: 'Dn_Signal 2', 5: 'Up_Signal 2'}, 'levels': [], 'description': ['Экспоненциальная скользящая средняя с переменным фактором сглаживания'], 'name': 'EMAVFS_StDev', 'source': 'MQL5 Indicators/EMAVFS_StDev/EMAVFS_StDev.mq5', 'folder': 'EMAVFS_StDev', 'inputs': [{'mql': 'Wmin', 'py': 'Wmin', 'param': 'Wmin', 'type': 'double', 'default': 0.0, 'label': 'минимальная чувствительность', 'sinput': False}, {'mql': 'Wmax', 'py': 'Wmax', 'param': 'Wmax', 'type': 'double', 'default': 5.0, 'label': 'максимальная чувствительность', 'sinput': False}, {'mql': 'Efactor', 'py': 'Efactor', 'param': 'Efactor', 'type': 'double', 'default': 1.01, 'label': 'коэффициент E (менять значение около единицы на десятые и сотые доли)', 'sinput': False}, {'mql': 'Afactor', 'py': 'Afactor', 'param': 'Afactor', 'type': 'double', 'default': 1.001, 'label': 'степень A (менять значение около единицы на десятые и сотые доли)', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг по вертикали в пунктах', 'sinput': False}, {'mql': 'dK1', 'py': 'dK1', 'param': 'dK1', 'type': 'double', 'default': 2.001, 'label': 'коэффициент 1 для квадратичного фильтра', 'sinput': False}, {'mql': 'dK2', 'py': 'dK2', 'param': 'dK2', 'type': 'double', 'default': 4.001, 'label': 'коэффициент 2 для квадратичного фильтра', 'sinput': False}, {'mql': 'std_period', 'py': 'std_period', 'param': 'std_period', 'type': 'uint', 'default': 9, 'label': 'период квадратичного фильтра', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# ---- inputs and global variables
Wmin = _input('Wmin', 0.0)  # минимальная чувствительность
Wmax = _input('Wmax', 5.0)  # максимальная чувствительность
Efactor = _input('Efactor', 1.01)  # коэффициент E (менять значение около единицы на десятые и сотые доли)
Afactor = _input('Afactor', 1.001)  # степень A (менять значение около единицы на десятые и сотые доли)
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
PriceShift = _input('PriceShift', 0)  # cдвиг по вертикали в пунктах
dK1 = _input('dK1', 2.001)  # коэффициент 1 для квадратичного фильтра
dK2 = _input('dK2', 4.001)  # коэффициент 2 для квадратичного фильтра
std_period = _input('std_period', 9)  # период квадратичного фильтра
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
ExtLineBuffer = Arr(0, 0.0)
ColorExtLineBuffer = Arr(0, 0.0)
BearsBuffer1 = Arr(0, 0.0)
BullsBuffer1 = Arr(0, 0.0)
BearsBuffer2 = Arr(0, 0.0)
BullsBuffer2 = Arr(0, 0.0)
start = 0
dPriceShift = 0.0
dEMAVFS = Arr(0, 0.0)

def OnInit():
    global dPriceShift, start
    if dK1 >= dK2:
        Print(' Некрректные значения входных параметров для коэффициентов 1 и 2 для квадратичного фильтра!')
        return INIT_FAILED
    start = 2 + _int(std_period)
    ArrayResize(dEMAVFS, std_period)
    shortname = 'EMAVFS_StDev'
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    SetIndexBuffer(1, ColorExtLineBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, BearsBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, start)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, BullsBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, start)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(4, BearsBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, start)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(5, BullsBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, start)
    PlotIndexSetInteger(4, PLOT_ARROW, 159)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    dPriceShift = Point() * PriceShift
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_wema_prew
    if rates_total < start:
        return 0
    first = 0
    bar = 0
    clr = 0
    series = 0.0
    wema = 0.0
    w = 0.0
    SMAdif = 0.0
    Sum = 0.0
    StDev = 0.0
    dstd = 0.0
    BEARS1 = 0.0
    BULLS1 = 0.0
    BEARS2 = 0.0
    BULLS2 = 0.0
    Filter1 = 0.0
    Filter2 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
        _s_OnCalculate_wema_prew = PriceSeries(IPC, first - 1, open, low, high, close)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        series = PriceSeries(IPC, bar, open, low, high, close)
        w = Wmin + ((Wmax - Wmin) * (1.0 - MathExp(-MathPow(MathAbs(series - (_s_OnCalculate_wema_prew / Efactor)), Afactor))))
        wema = _s_OnCalculate_wema_prew + (w * (series - _s_OnCalculate_wema_prew))
        ExtLineBuffer[bar] = wema + dPriceShift
        if bar < (rates_total - 1):
            _s_OnCalculate_wema_prew = wema
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        clr = 1
        if ExtLineBuffer[bar - 1] < ExtLineBuffer[bar]:
            clr = 2
        if ExtLineBuffer[bar - 1] > ExtLineBuffer[bar]:
            clr = 0
        ColorExtLineBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = start
    bar = first
    for bar in range(bar, rates_total):
        for iii in range(0, _int(std_period)):
            dEMAVFS[iii] = ExtLineBuffer[bar - iii] - ExtLineBuffer[bar - iii - 1]
        Sum = 0.0
        for iii in range(0, _int(std_period)):
            Sum += dEMAVFS[iii]
        SMAdif = Sum / std_period
        Sum = 0.0
        for iii in range(0, _int(std_period)):
            Sum += MathPow(dEMAVFS[iii] - SMAdif, 2)
        StDev = MathSqrt(Sum / std_period)
        dstd = NormalizeDouble(dEMAVFS[0], Digits() + 2)
        Filter1 = NormalizeDouble(dK1 * StDev, Digits() + 2)
        Filter2 = NormalizeDouble(dK2 * StDev, Digits() + 2)
        BEARS1 = EMPTY_VALUE
        BULLS1 = EMPTY_VALUE
        BEARS2 = EMPTY_VALUE
        BULLS2 = EMPTY_VALUE
        wema = ExtLineBuffer[bar]
        if dstd < (-Filter1) and dstd >= (-Filter2):
            BEARS1 = wema
        if dstd < (-Filter2):
            BEARS2 = wema
        if dstd > Filter1 and dstd <= Filter2:
            BULLS1 = wema
        if dstd > Filter2:
            BULLS2 = wema
        BullsBuffer1[bar] = BULLS1
        BearsBuffer1[bar] = BEARS1
        BullsBuffer2[bar] = BULLS2
        BearsBuffer2[bar] = BEARS2
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def PriceSeries(applied_price, bar, dOpen, dLow, dHigh, dClose):
    _sw1 = applied_price
    if _sw1 == PRICE_CLOSE:
        return dClose[bar]
    elif _sw1 == PRICE_OPEN:
        return dOpen[bar]
    elif _sw1 == PRICE_HIGH:
        return dHigh[bar]
    elif _sw1 == PRICE_LOW:
        return dLow[bar]
    elif _sw1 == PRICE_MEDIAN:
        return (dHigh[bar] + dLow[bar]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (dClose[bar] + dHigh[bar] + dLow[bar]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return ((2 * dClose[bar]) + dHigh[bar] + dLow[bar]) / 4.0
    elif _sw1 == 8:
        return (dOpen[bar] + dClose[bar]) / 2.0
    elif _sw1 == 9:
        return (dOpen[bar] + dClose[bar] + dHigh[bar] + dLow[bar]) / 4.0
    elif _sw1 == 10:
        if dClose[bar] > dOpen[bar]:
            return dHigh[bar]
        else:
            if dClose[bar] < dOpen[bar]:
                return dLow[bar]
            else:
                return dClose[bar]
    elif _sw1 == 11:
        if dClose[bar] > dOpen[bar]:
            return (dHigh[bar] + dClose[bar]) / 2.0
        else:
            if dClose[bar] < dOpen[bar]:
                return (dLow[bar] + dClose[bar]) / 2.0
            else:
                return dClose[bar]
    elif _sw1 == 12:
        res = dHigh[bar] + dLow[bar] + dClose[bar]
        if dClose[bar] < dOpen[bar]:
            res = (res + dLow[bar]) / 2
        if dClose[bar] > dOpen[bar]:
            res = (res + dHigh[bar]) / 2
        if dClose[bar] == dOpen[bar]:
            res = (res + dClose[bar]) / 2
        return (res - dLow[bar] + (res - dHigh[bar])) / 2
    else:
        return dClose[bar]

# ---- static local variables
_s_OnCalculate_wema_prew = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EMAVFSStDev(_MQL5Indicator):
    name = 'EMAVFS_StDev'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Wmin': 0.0,  # минимальная чувствительность
        'Wmax': 5.0,  # максимальная чувствительность
        'Efactor': 1.01,  # коэффициент E (менять значение около единицы на десятые и сотые доли)
        'Afactor': 1.001,  # степень A (менять значение около единицы на десятые и сотые доли)
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'PriceShift': 0,  # cдвиг по вертикали в пунктах
        'dK1': 2.001,  # коэффициент 1 для квадратичного фильтра
        'dK2': 4.001,  # коэффициент 2 для квадратичного фильтра
        'std_period': 9,  # период квадратичного фильтра
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

