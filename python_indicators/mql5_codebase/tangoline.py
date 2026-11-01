"""tangoline — converted from MQL5: MQL5 Indicators/TangoLine_HTF/tangoline.mq5

Copyright: Copyright © 2015, fxborg; Link: http://fxborg-labo.hateblo.jp/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, fxborg', 'link': 'http://fxborg-labo.hateblo.jp/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [14822282], 2: [3329330], 3: [255]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'TangoLine', 2: 'Upper', 3: 'Lower'}, 'levels': [], 'description': [''], 'name': 'tangoline', 'source': 'MQL5 Indicators/TangoLine_HTF/tangoline.mq5', 'folder': 'TangoLine_HTF', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'MinSpread', 'py': 'MinSpread', 'param': 'MinSpread', 'type': 'double', 'default': 5.0, 'label': 'Min Spread', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 20)  # Period
MinSpread = _input('MinSpread', 5.0)  # Min Spread
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
LineBuffer = Arr(0, 0.0)
HighesBuffer = Arr(0, 0.0)
LowesBuffer = Arr(0, 0.0)
HighBuffer = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)
dMinSpread = 0.0
min_rates_total = 0

def OnInit():
    global dMinSpread, min_rates_total
    min_rates_total = InpPeriod + 3
    dMinSpread = MinSpread * Point()
    SetIndexBuffer(0, LineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, HighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, LowBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(3, HighesBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, LowesBuffer, INDICATOR_CALCULATIONS)
    shortname = Box("")
    StringConcatenate(shortname, 'TangoLine(', InpPeriod, ', ', MinSpread, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_btm_bar, _s_OnCalculate_top_bar
    if rates_total < min_rates_total:
        return 0
    dmin = 0.0
    dmax = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        _s_OnCalculate_top_bar = 0
        _s_OnCalculate_btm_bar = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        LowesBuffer[bar] = 0.0
        HighesBuffer[bar] = 0.0
        HighBuffer[bar] = 0.0
        LowBuffer[bar] = 0.0
        LineBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    bar = first
    for bar in range(bar, rates_total):
        dmin = 1000000.0
        dmax = -1000000.0
        for kkk in range(bar - InpPeriod + 1, bar + 1):
            if dmin > low[kkk]:
                dmin = low[kkk]
            if dmax < high[kkk]:
                dmax = high[kkk]
        if (LowesBuffer[bar - 2] - dMinSpread) > LowesBuffer[bar - 1] and LowesBuffer[bar - 1] == dmin:
            _s_OnCalculate_top_bar = bar - 1
            _s_OnCalculate_btm_bar = bar - 1
        if (HighesBuffer[bar - 2] + dMinSpread) < HighesBuffer[bar - 1] and HighesBuffer[bar - 1] == dmax:
            _s_OnCalculate_btm_bar = bar - 1
            _s_OnCalculate_top_bar = bar - 1
        LowesBuffer[bar] = dmin
        HighesBuffer[bar] = dmax
        if MathMax(_s_OnCalculate_top_bar, _s_OnCalculate_btm_bar) > (bar - InpPeriod + 1):
            dmin = 1000000.0
            dmax = -1000000.0
            for kkk in range(bar - InpPeriod + 1, bar + 1):
                if kkk >= _s_OnCalculate_btm_bar and dmin > low[kkk]:
                    dmin = low[kkk]
                if kkk >= _s_OnCalculate_top_bar and dmax < high[kkk]:
                    dmax = high[kkk]
        LowBuffer[bar] = dmin
        HighBuffer[bar] = dmax
        LineBuffer[bar] = (dmax + dmin) / 2
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_top_bar = 0
_s_OnCalculate_btm_bar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Tangoline(_MQL5Indicator):
    name = 'tangoline'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 20,  # Period
        'MinSpread': 5.0,  # Min Spread
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

