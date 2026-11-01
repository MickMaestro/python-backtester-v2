"""i4_GoldenLionTrend_v3 — converted from MQL5: MQL5 Indicators/i4_GoldenLionTrend_v3/i4_GoldenLionTrend_v3.mq5

Индикатор силы тренда с использованием значений двух каналов Боллинджера
Copyright: Copyright © 2006, goldenlion@ukr.net; Link: http://GlobeInvestFund.com/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, goldenlion@ukr.net', 'link': 'http://GlobeInvestFund.com/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 11}, 'colors': {1: [65280, 8421376, 8388736, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'i4_GoldenLionTrend_v3'}, 'levels': [], 'description': ['Индикатор силы тренда с использованием значений двух каналов Боллинджера'], 'name': 'i4_GoldenLionTrend_v3', 'source': 'MQL5 Indicators/i4_GoldenLionTrend_v3/i4_GoldenLionTrend_v3.mq5', 'folder': 'i4_GoldenLionTrend_v3', 'inputs': [{'mql': 'BBPeriod', 'py': 'BBPeriod', 'param': 'BBPeriod', 'type': 'uint', 'default': 20, 'label': 'период для расчета средней линии', 'sinput': False}, {'mql': 'StdDeviation1', 'py': 'StdDeviation1', 'param': 'StdDeviation1', 'type': 'double', 'default': 1.0001, 'label': 'девиация 1', 'sinput': False}, {'mql': 'StdDeviation2', 'py': 'StdDeviation2', 'param': 'StdDeviation2', 'type': 'double', 'default': 2.0001, 'label': 'девиация 2', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 1, 'label': 'тип цены', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BBPeriod = _input('BBPeriod', 20)  # период для расчета средней линии
StdDeviation1 = _input('StdDeviation1', 1.0001)  # девиация 1
StdDeviation2 = _input('StdDeviation2', 2.0001)  # девиация 2
applied_price = _input('applied_price', PRICE_CLOSE)  # тип цены
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
Ind_Handle1 = 0
Ind_Handle2 = 0
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global Ind_Handle1, Ind_Handle2, min_rates_total
    min_rates_total = _int(BBPeriod)
    if StdDeviation1 >= StdDeviation2:
        Print('Девиация 1 должна быть больше, чем Девиация 2!')
        Print('Откорректируйте значения входных параметров!')
        return INIT_FAILED
    Ind_Handle1 = iBands(None, 0, BBPeriod, 0, StdDeviation1, applied_price)
    if Ind_Handle1 == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iBands1')
        return INIT_FAILED
    Ind_Handle2 = iBands(None, 0, BBPeriod, 0, StdDeviation2, applied_price)
    if Ind_Handle2 == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iBands2')
        return INIT_FAILED
    SetIndexBuffer(0, UpIndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpIndBuffer, True)
    SetIndexBuffer(1, DnIndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnIndBuffer, True)
    SetIndexBuffer(2, ColorIndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    shortname = Box("")
    StringConcatenate(shortname, 'i4_GoldenLionTrend_v3', BBPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(Ind_Handle1) < rates_total or BarsCalculated(Ind_Handle2) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    UpBB1 = Arr(0, 0.0)
    DnBB1 = Arr(0, 0.0)
    UpBB2 = Arr(0, 0.0)
    DnBB2 = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ind_Handle1, UPPER_BAND, 0, to_copy, UpBB1) <= 0:
        return 0
    if CopyBuffer(Ind_Handle1, LOWER_BAND, 0, to_copy, DnBB1) <= 0:
        return 0
    if CopyBuffer(Ind_Handle2, UPPER_BAND, 0, to_copy, UpBB2) <= 0:
        return 0
    if CopyBuffer(Ind_Handle2, LOWER_BAND, 0, to_copy, DnBB2) <= 0:
        return 0
    ArraySetAsSeries(UpBB1, True)
    ArraySetAsSeries(DnBB1, True)
    ArraySetAsSeries(UpBB2, True)
    ArraySetAsSeries(DnBB2, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if close[bar] < UpBB1[bar] and close[bar] > DnBB1[bar]:
            UpIndBuffer[bar] = 0.0
            DnIndBuffer[bar] = 0.0
            continue
        UpIndBuffer[bar] = high[bar]
        DnIndBuffer[bar] = low[bar]
        if close[bar] >= UpBB2[bar]:
            ColorIndBuffer[bar] = 0.0
        elif close[bar] >= UpBB1[bar]:
            ColorIndBuffer[bar] = 1.0
        elif close[bar] <= DnBB2[bar]:
            ColorIndBuffer[bar] = 3.0
        elif close[bar] <= DnBB1[bar]:
            ColorIndBuffer[bar] = 2.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class I4GoldenLionTrendV3(_MQL5Indicator):
    name = 'i4_GoldenLionTrend_v3'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BBPeriod': 20,  # период для расчета средней линии
        'StdDeviation1': 1.0001,  # девиация 1
        'StdDeviation2': 2.0001,  # девиация 2
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # тип цены
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

