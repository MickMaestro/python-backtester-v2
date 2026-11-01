"""fractalsnoredraw — converted from MQL5: MQL5 Indicators/FractalsNoRedraw/fractalsnoredraw.mq5

Copyright: Tapochun; Link: https://login.mql5.com/ru/users/tapochun

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Tapochun', 'link': 'https://login.mql5.com/ru/users/tapochun', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16777215], 2: [16777215]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Fractal_nr Up', 2: 'Fractal_nr Dn'}, 'levels': [], 'description': [], 'name': 'fractalsnoredraw', 'source': 'MQL5 Indicators/FractalsNoRedraw/fractalsnoredraw.mq5', 'folder': 'FractalsNoRedraw', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_FRACTAL
UP = 0
DN = 1
_enum('ENUM_FRACTAL', {0: 'UP', 1: 'DN'})

# ---- inputs and global variables
ExtUpperBuffer = Arr(0, 0.0)
ExtLowerBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, ExtUpperBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtLowerBuffer, INDICATOR_DATA)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_ARROW, 217)
    PlotIndexSetInteger(1, PLOT_ARROW, 218)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_ARROW_SHIFT, -10)
    PlotIndexSetInteger(1, PLOT_ARROW_SHIFT, 10)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 5:
        return 0
    if prev_calculated <= 0:
        ArrayInitialize(ExtUpperBuffer, EMPTY_VALUE)
        ArrayInitialize(ExtLowerBuffer, EMPTY_VALUE)
        for i in range(2, rates_total - 3):
            CheckFractal(UP, i, ExtUpperBuffer, high)
            CheckFractal(DN, i, ExtLowerBuffer, low)
        return rates_total
    else:
        if rates_total > prev_calculated:
            ExtUpperBuffer[rates_total - 1] = EMPTY_VALUE
            ExtLowerBuffer[rates_total - 1] = EMPTY_VALUE
            CheckFractal(UP, rates_total - 4, ExtUpperBuffer, high)
            CheckFractal(DN, rates_total - 4, ExtLowerBuffer, low)
        return rates_total
    return rates_total

def CheckFractal(type_, i, buffer, price):
    p = price[i]
    pf_1 = price[i + 1]
    pf_2 = price[i + 2]
    pp_1 = price[i - 1]
    pp_2 = price[i - 2]
    if type_ == UP:
        if ((p > pf_1 and p > pf_2) and p >= pp_1) and p >= pp_2:
            ExtUpperBuffer[i] = price[i]
        return
    if type_ == DN:
        if ((p < pf_1 and p < pf_2) and p <= pp_1) and p <= pp_2:
            ExtLowerBuffer[i] = price[i]
        return
    Print('CheckFractal', ': ОШИБКА! Передан неизвестный тип фрактала: ' + EnumToString(type_, 'ENUM_FRACTAL'))
    return


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Fractalsnoredraw(_MQL5Indicator):
    name = 'fractalsnoredraw'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

