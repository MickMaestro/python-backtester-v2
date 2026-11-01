"""RiskSpread — converted from MQL5: MQL5 Indicators/RiskSpread/RiskSpread.mq5

Copyright: Copyright © 2007, VadimVP; Link: poluyan@fxmail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, VadimVP', 'link': 'poluyan@fxmail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16443110]}, 'widths': {}, 'styles': {}, 'labels': {1: 'RiskSpread'}, 'levels': [], 'description': [], 'name': 'RiskSpread', 'source': 'MQL5 Indicators/RiskSpread/RiskSpread.mq5', 'folder': 'RiskSpread', 'inputs': [{'mql': 'K_Spread', 'py': 'K_Spread', 'param': 'K_Spread', 'type': 'uint', 'default': 10, 'label': 'количество спредов', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
K_Spread = _input('K_Spread', 10)  # количество спредов
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 1
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    shortname = Box("")
    StringConcatenate(shortname, 'RiskSpread(', K_Spread, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    DxSpread = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 3
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        DxSpread = Point() * K_Spread * spread[bar]
        UpBuffer[bar] = close[bar] + DxSpread
        DnBuffer[bar] = close[bar] - (Point() * spread[bar]) - DxSpread
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RiskSpread(_MQL5Indicator):
    name = 'RiskSpread'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'K_Spread': 10,  # количество спредов
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

