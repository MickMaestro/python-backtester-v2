"""bollingerbands_b — converted from MQL5: MQL5 Indicators/BollingerBands_b_HTF/bollingerbands_b.mq5

Copyright: Copyright © 2004, MetaQuotes Software Corp.; Link: http://www.metaquotes.net/; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2004, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net/', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [15624315]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Bollinger Bands% b'}, 'levels': [0.0], 'description': [], 'name': 'bollingerbands_b', 'source': 'MQL5 Indicators/BollingerBands_b_HTF/bollingerbands_b.mq5', 'folder': 'BollingerBands_b_HTF', 'inputs': [{'mql': 'BBPeriod', 'py': 'BBPeriod', 'param': 'BBPeriod', 'type': 'uint', 'default': 20, 'label': 'Период для расчета средней линии', 'sinput': False}, {'mql': 'StdDeviation', 'py': 'StdDeviation', 'param': 'StdDeviation', 'type': 'double', 'default': 2.0, 'label': 'Девиация', 'sinput': False}, {'mql': 'applied_price', 'py': 'applied_price', 'param': 'applied_price', 'type': 'int', 'default': 1, 'label': 'Тип цены', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BBPeriod = _input('BBPeriod', 20)  # Период для расчета средней линии
StdDeviation = _input('StdDeviation', 2.0)  # Девиация
applied_price = _input('applied_price', PRICE_CLOSE)  # Тип цены
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
Ind_Handle = 0
IndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global Ind_Handle, min_rates_total
    min_rates_total = _int(BBPeriod)
    Ind_Handle = iBands(None, 0, BBPeriod, 0, StdDeviation, applied_price)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iBands')
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Bollinger Bands% b', BBPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(Ind_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    UpBB = Arr(0, 0.0)
    DnBB = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Ind_Handle, UPPER_BAND, 0, to_copy, UpBB) <= 0:
        return 0
    if CopyBuffer(Ind_Handle, LOWER_BAND, 0, to_copy, DnBB) <= 0:
        return 0
    ArraySetAsSeries(UpBB, True)
    ArraySetAsSeries(DnBB, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IndBuffer[bar] = _fdiv(close[bar] - UpBB[bar], DnBB[bar] - UpBB[bar])
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BollingerbandsB(_MQL5Indicator):
    name = 'bollingerbands_b'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BBPeriod': 20,  # Период для расчета средней линии
        'StdDeviation': 2.0,  # Девиация
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Тип цены
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

