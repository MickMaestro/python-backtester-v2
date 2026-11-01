"""Rj_RMA — converted from MQL5: MQL5 Indicators/Rj_RMA/Rj_RMA.mq5

Copyright: Copyright © 2011,RJ Rjabkov Alexander; Link: rj-a@mail.ru; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011,RJ Rjabkov Alexander', 'link': 'rj-a@mail.ru', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [8421504, 16748574, 16711935]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Rj_RMA'}, 'levels': [], 'description': [], 'name': 'Rj_RMA', 'source': 'MQL5 Indicators/Rj_RMA/Rj_RMA.mq5', 'folder': 'Rj_RMA', 'inputs': [{'mql': 'CalcPeriodRange', 'py': 'CalcPeriodRange', 'param': 'CalcPeriodRange', 'type': 'uint', 'default': 13, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CalcPeriodRange = _input('CalcPeriodRange', 13)  # Период индикатора
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0

def OnInit():
    global dPriceShift, min_rates_total
    min_rates_total = _int(CalcPeriodRange + 1)
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Rj_RMA(', CalcPeriodRange, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    b1 = 0.0
    b2 = 0.0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    for bar in range(limit, 0 - 1, -1):
        b1 = 0.0
        b2 = 0.0
        for iii in range(0, _int(CalcPeriodRange)):
            b1 += high[ArrayMaximum(high, bar + iii, CalcPeriodRange)]
            b2 += low[ArrayMinimum(low, bar + iii, CalcPeriodRange)]
        IndBuffer[bar] = NormalizeDouble(_fdiv(b1 + b2, CalcPeriodRange * 2.0), Digits())
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    for bar in range(limit, 0 - 1, -1):
        ColorIndBuffer[bar] = 0.0
        if IndBuffer[bar + 1] < IndBuffer[bar]:
            ColorIndBuffer[bar] = 1.0
        if IndBuffer[bar + 1] > IndBuffer[bar]:
            ColorIndBuffer[bar] = 2.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RjRMA(_MQL5Indicator):
    name = 'Rj_RMA'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CalcPeriodRange': 13,  # Период индикатора
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
    }

