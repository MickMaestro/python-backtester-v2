"""i-amma — converted from MQL5: MQL5 Indicators/i-AMMA_HTF/i-amma.mq5

Copyright: Copyright © 2007, RickD; Link: www.e2e-fx.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, RickD', 'link': 'www.e2e-fx.net', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [42495]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'i-AMMA'}, 'levels': [], 'description': [], 'name': 'i-amma', 'source': 'MQL5 Indicators/i-AMMA_HTF/i-amma.mq5', 'folder': 'i-AMMA_HTF', 'inputs': [{'mql': 'MA_Period', 'py': 'MA_Period', 'param': 'MA_Period', 'type': 'uint', 'default': 25, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MA_Period = _input('MA_Period', 25)  # Глубина сглаживания
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
IndBuffer = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0

def OnInit():
    global dPriceShift, min_rates_total
    min_rates_total = 2
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'i-AMMA(', MA_Period, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (min_rates_total + begin):
        return 0
    first = 0
    bar = 0
    AMMA = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total + begin
        IndBuffer[first - 1] = price[first - 1]
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + begin)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        AMMA = (((MA_Period - 1) * (IndBuffer[bar - 1] - dPriceShift)) + price[bar]) / MA_Period
        IndBuffer[bar] = AMMA + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IAmma(_MQL5Indicator):
    name = 'i-amma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Period': 25,  # Глубина сглаживания
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

