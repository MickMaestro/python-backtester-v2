"""pchannel3cloud — converted from MQL5: MQL5 Indicators/PChannel3Cloud/pchannel3cloud.mq5

Copyright: Copyright © 2005, Xaoc; Link: http://forex.xcd.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Xaoc', 'link': 'http://forex.xcd.ru/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 5}, 'types': {1: 7, 2: 1, 3: 1, 4: 1, 5: 7}, 'colors': {1: [10025880], 2: [8421376], 3: [16711680], 4: [255], 5: [13353215]}, 'widths': {2: 2, 3: 2, 4: 2}, 'styles': {2: 0, 3: 0, 4: 0}, 'labels': {1: 'Upper Cloud', 2: 'TOPBAND', 3: 'MIDBAND', 4: 'BOTBAND', 5: 'Upper Cloud'}, 'levels': [], 'description': [], 'name': 'pchannel3cloud', 'source': 'MQL5 Indicators/PChannel3Cloud/pchannel3cloud.mq5', 'folder': 'PChannel3Cloud', 'inputs': [{'mql': 'PCPeriod', 'py': 'PCPeriod', 'param': 'PCPeriod', 'type': 'uint', 'default': 55, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
PCPeriod = _input('PCPeriod', 55)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
min_rates_total = 0
ExtUp1Buffer = Arr(0, 0.0)
ExtUp2Buffer = Arr(0, 0.0)
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
ExtCBuffer = Arr(0, 0.0)
ExtDn1Buffer = Arr(0, 0.0)
ExtDn2Buffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = _int(PCPeriod)
    SetIndexBuffer(0, ExtUp1Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtUp2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ExtUp1Buffer, True)
    ArraySetAsSeries(ExtUp2Buffer, True)
    SetIndexBuffer(2, ExtABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ExtABuffer, True)
    SetIndexBuffer(3, ExtBBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ExtBBuffer, True)
    SetIndexBuffer(4, ExtCBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ExtCBuffer, True)
    SetIndexBuffer(5, ExtDn1Buffer, INDICATOR_DATA)
    SetIndexBuffer(6, ExtDn2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ExtDn1Buffer, True)
    ArraySetAsSeries(ExtDn2Buffer, True)
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
        ExtUp1Buffer[bar] = ExtABuffer[bar]
        ExtUp2Buffer[bar] = ExtBBuffer[bar]
        ExtDn1Buffer[bar] = ExtBBuffer[bar]
        ExtDn2Buffer[bar] = ExtCBuffer[bar]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Pchannel3cloud(_MQL5Indicator):
    name = 'pchannel3cloud'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PCPeriod': 55,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

