"""pchannel3 — converted from MQL5: MQL5 Indicators/PChannel3Cloud/pchannel3.mq5

Copyright: Copyright © 2005, Xaoc; Link: http://forex.xcd.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Xaoc', 'link': 'http://forex.xcd.ru/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [3329330], 2: [16711680], 3: [255]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'TOPBAND', 2: 'MIDBAND', 3: 'BOTBAND'}, 'levels': [], 'description': [], 'name': 'pchannel3', 'source': 'MQL5 Indicators/PChannel3Cloud/pchannel3.mq5', 'folder': 'PChannel3Cloud', 'inputs': [{'mql': 'PCPeriod', 'py': 'PCPeriod', 'param': 'PCPeriod', 'type': 'uint', 'default': 55, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
PCPeriod = _input('PCPeriod', 55)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
min_rates_total = 0
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
ExtCBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = _int(PCPeriod)
    SetIndexBuffer(0, ExtABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ExtABuffer, True)
    SetIndexBuffer(1, ExtBBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ExtBBuffer, True)
    SetIndexBuffer(2, ExtCBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ExtCBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'PChannel3(' + _str(PCPeriod) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    for bar in range(limit, 0 - 1, -1):
        ExtABuffer[bar] = High[ArrayMaximum(High, bar, PCPeriod)]
        ExtCBuffer[bar] = Low[ArrayMinimum(Low, bar, PCPeriod)]
        ExtBBuffer[bar] = (ExtABuffer[bar] + ExtCBuffer[bar]) / 2.0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Pchannel3(_MQL5Indicator):
    name = 'pchannel3'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PCPeriod': 55,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

