"""taf — converted from MQL5: MQL5 Indicators/Taf/taf.mq5

Copyright: Copyright © 2004, Poul_Trade_Forum; Link: http://forex.kbpauk.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2004, Poul_Trade_Forum', 'link': 'http://forex.kbpauk.ru/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 2, 2: 2}, 'colors': {1: [16748574], 2: [16711935]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'TafHigh', 2: 'TafLow'}, 'levels': [], 'description': [], 'name': 'taf', 'source': 'MQL5 Indicators/Taf/taf.mq5', 'folder': 'Taf', 'inputs': [{'mql': 'BQUALIFY', 'py': 'BQUALIFY', 'param': 'BQUALIFY', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BQUALIFY = _input('BQUALIFY', 2)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
min_rates_total = 0
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = _int(BQUALIFY)
    SetIndexBuffer(0, ExtHighBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ExtHighBuffer, True)
    SetIndexBuffer(1, ExtLowBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ExtLowBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Taf(' + _str(BQUALIFY) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    global _s_OnCalculate_VALUE1_prev, _s_OnCalculate_VALUE2_prev
    if rates_total < min_rates_total:
        return 0
    limit = 0
    VALUE1 = 0
    VALUE2 = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_VALUE1_prev = 0
        _s_OnCalculate_VALUE2_prev = 0
    else:
        limit = rates_total - prev_calculated
    VALUE1 = _s_OnCalculate_VALUE1_prev
    VALUE2 = _s_OnCalculate_VALUE2_prev
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    for bar in range(limit, 0 - 1, -1):
        ExtLowBuffer[bar] = 0.0
        ExtHighBuffer[bar] = 0.0
        if High[bar] >= High[bar + 1] and Low[bar] >= Low[bar + 1]:
            if VALUE2 >= BQUALIFY:
                ExtLowBuffer[bar] = Low[bar + 1]
            VALUE1 += 1
            VALUE2 = 0
        if Low[bar] <= Low[bar + 1] and High[bar] <= High[bar + 1]:
            if VALUE1 >= BQUALIFY:
                ExtHighBuffer[bar] = High[bar + 1]
            VALUE2 += 1
            VALUE1 = 0
        if bar:
            _s_OnCalculate_VALUE1_prev = VALUE1
            _s_OnCalculate_VALUE2_prev = VALUE2
    return rates_total

# ---- static local variables
_s_OnCalculate_VALUE1_prev = 0
_s_OnCalculate_VALUE2_prev = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Taf(_MQL5Indicator):
    name = 'taf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BQUALIFY': 2,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

