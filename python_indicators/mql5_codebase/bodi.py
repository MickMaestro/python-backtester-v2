"""BoDi — converted from MQL5: MQL5 Indicators/BoDi/BoDi.mq5

Copyright: Copyright © 2011, paladin80; Link: forevex@mail.ru; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, paladin80', 'link': 'forevex@mail.ru', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [9639167, 8421504, 16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'BoDi'}, 'levels': [], 'description': [], 'name': 'BoDi', 'source': 'MQL5 Indicators/BoDi/BoDi.mq5', 'folder': 'BoDi', 'inputs': [{'mql': 'BBPeriod', 'py': 'BBPeriod', 'param': 'BBPeriod', 'type': 'uint', 'default': 20, 'label': 'Период для расчета средней линии', 'sinput': False}, {'mql': 'StdDeviation', 'py': 'StdDeviation', 'param': 'StdDeviation', 'type': 'double', 'default': 2.0, 'label': 'Кол-во отклонений', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 1, 'label': 'Тип цены', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BBPeriod = _input('BBPeriod', 20)  # Период для расчета средней линии
StdDeviation = _input('StdDeviation', 2.0)  # Кол-во отклонений
applied_price = _input('applied_price', PRICE_CLOSE)  # Тип цены
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
Ind_Handle = 0

def OnInit():
    global Ind_Handle, min_rates_total
    min_rates_total = _int(BBPeriod + 1)
    Ind_Handle = iBands(Symbol(), PERIOD_CURRENT, BBPeriod, 0, StdDeviation, applied_price)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iBands')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'BoDi')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(Ind_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    UpBB = Arr(0, 0.0)
    DnBB = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 2
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ind_Handle, UPPER_BAND, 0, to_copy, UpBB) <= 0:
        return 0
    if CopyBuffer(Ind_Handle, LOWER_BAND, 0, to_copy, DnBB) <= 0:
        return 0
    ArraySetAsSeries(UpBB, True)
    ArraySetAsSeries(DnBB, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IndBuffer[bar] = _fdiv(UpBB[bar] - DnBB[bar], Point())
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ColorIndBuffer[bar] = 1.0
        if IndBuffer[bar] > IndBuffer[bar + 1]:
            ColorIndBuffer[bar] = 2.0
        if IndBuffer[bar] < IndBuffer[bar + 1]:
            ColorIndBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BoDi(_MQL5Indicator):
    name = 'BoDi'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BBPeriod': 20,  # Период для расчета средней линии
        'StdDeviation': 2.0,  # Кол-во отклонений
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Тип цены
    }

