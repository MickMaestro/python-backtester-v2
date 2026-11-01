"""exvol — converted from MQL5: MQL5 Indicators/ExVol/exvol.mq5

Copyright: Copyright © 2006, Alex Sidd (Executer); Link: mailto:work_st@mail.ru; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Alex Sidd (Executer)', 'link': 'mailto:work_st@mail.ru', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [255, 8036607, 8421504, 15453831, 16711680]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'ExVol'}, 'levels': [], 'description': [], 'name': 'exvol', 'source': 'MQL5 Indicators/ExVol/exvol.mq5', 'folder': 'ExVol', 'inputs': [{'mql': 'ExPeriod', 'py': 'ExPeriod', 'param': 'ExPeriod', 'type': 'uint', 'default': 15, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExPeriod = _input('ExPeriod', 15)
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = _int(ExPeriod)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ExVol(' + _str(ExPeriod) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        negative = 0.0
        positive = 0.0
        kkk = _int(bar - ExPeriod + 1)
        while kkk <= bar:
            res = _fdiv(close[kkk] - open[kkk], Point())
            if res > 0:
                positive += res
            if res < 0:
                negative -= res
            kkk += 1
        IndBuffer[bar] = (positive - negative) / ExPeriod
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        clr = 0
        if IndBuffer[bar] > 0:
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                clr = 4
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                clr = 3
        if IndBuffer[bar] < 0:
            if IndBuffer[bar] < IndBuffer[bar - 1]:
                clr = 0
            if IndBuffer[bar] > IndBuffer[bar - 1]:
                clr = 1
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Exvol(_MQL5Indicator):
    name = 'exvol'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ExPeriod': 15,
    }

