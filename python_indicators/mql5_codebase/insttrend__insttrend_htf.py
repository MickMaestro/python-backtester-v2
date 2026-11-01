"""InstTrend — converted from MQL5: MQL5 Indicators/InstTrend_HTF/InstTrend.mq5

Copyright: Coded by Witold Wozniak; Link: www.mqlsoft.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Coded by Witold Wozniak', 'link': 'www.mqlsoft.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [13850042, 16776960]}, 'widths': {}, 'styles': {}, 'labels': {1: 'InstTrend'}, 'levels': [], 'description': [], 'name': 'InstTrend', 'source': 'MQL5 Indicators/InstTrend_HTF/InstTrend.mq5', 'folder': 'InstTrend_HTF', 'inputs': [{'mql': 'Alpha', 'py': 'Alpha', 'param': 'Alpha', 'type': 'double', 'default': 0.07, 'label': 'коэффициент индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Alpha = _input('Alpha', 0.07)  # коэффициент индикатора
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
ITrendBuffer = Arr(0, 0.0)
TriggerBuffer = Arr(0, 0.0)
min_rates_total = 0
K0 = 0.0
K1 = 0.0
K2 = 0.0
K3 = 0.0
K4 = 0.0

def OnInit():
    global K0, K1, K2, K3, K4, min_rates_total
    min_rates_total = 8 + 3
    A2 = Alpha * Alpha
    K0 = Alpha - (A2 / 4.0)
    K1 = 0.5 * A2
    K2 = Alpha - (0.75 * A2)
    K3 = 2.0 * (1.0 - Alpha)
    K4 = MathPow(1.0 - Alpha, 2)
    SetIndexBuffer(0, ITrendBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, TriggerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 30)
    shortname = Box("")
    StringConcatenate(shortname, 'Instantaneous Trendline(', Alpha, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    price0 = 0.0
    price1 = 0.0
    price2 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 3
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price0 = (high[bar] + low[bar]) / 2.0
        price1 = (high[bar - 1] + low[bar - 1]) / 2.0
        price2 = (high[bar - 2] + low[bar - 2]) / 2.0
        if bar < min_rates_total:
            ITrendBuffer[bar] = (price0 + (2.0 * price1) + price2) / 4.0
        else:
            ITrendBuffer[bar] = (K0 * price0) + (K1 * price1) - (K2 * price2) + (K3 * ITrendBuffer[bar - 1]) - (K4 * ITrendBuffer[bar - 2])
        TriggerBuffer[bar] = (2.0 * ITrendBuffer[bar]) - ITrendBuffer[bar - 2]
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class InstTrend(_MQL5Indicator):
    name = 'InstTrend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Alpha': 0.07,  # коэффициент индикатора
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

