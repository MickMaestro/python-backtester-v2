"""2mohlc_ — converted from MQL5: MQL5 Indicators/2MoHLC/2mohlc_.mq5

2 Medians of High-Low Channels
Copyright: Copyright © 2010, Ilya Filatov; Link: ilya-filatov@ya.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Ilya Filatov', 'link': 'ilya-filatov@ya.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [16760576, 11823615], 2: [9470064], 3: [9470064]}, 'widths': {2: 2, 3: 2}, 'styles': {2: 0, 3: 0}, 'labels': {1: '2MoHLC', 2: 'HLC-M1', 3: 'HLC-M2'}, 'levels': [], 'description': ['2 Medians of High-Low Channels'], 'name': '2mohlc_', 'source': 'MQL5 Indicators/2MoHLC/2mohlc_.mq5', 'folder': '2MoHLC', 'inputs': [{'mql': 'Period1', 'py': 'Period1', 'param': 'Period1', 'type': 'int', 'default': 24, 'label': 'Period 1', 'sinput': False}, {'mql': 'Period2', 'py': 'Period2', 'param': 'Period2', 'type': 'int', 'default': 48, 'label': 'Period 2', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Period1 = _input('Period1', 24)  # Period 1
Period2 = _input('Period2', 48)  # Period 2
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
min_rates_total = 0
Ext1Buffer = Arr(0, 0.0)
Ext2Buffer = Arr(0, 0.0)
Ext1_Buffer = Arr(0, 0.0)
Ext2_Buffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = MathMax(Period1, Period2)
    SetIndexBuffer(0, Ext1Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Ext1Buffer, True)
    SetIndexBuffer(1, Ext2Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Ext2Buffer, True)
    SetIndexBuffer(2, Ext1_Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Ext1_Buffer, True)
    SetIndexBuffer(3, Ext2_Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Ext2_Buffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    IndicatorSetString(INDICATOR_SHORTNAME, '2MoHLC(' + _str(Period1) + ',' + _str(Period2) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if rates_total < min_rates_total:
        return 0
    HH = 0.0
    LL = 0.0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    for bar in range(limit, 0 - 1, -1):
        HH = High[ArrayMaximum(High, bar, Period1)]
        LL = Low[ArrayMinimum(Low, bar, Period1)]
        Ext1Buffer[bar] = (HH + LL) / 2.0
        Ext1_Buffer[bar] = Ext1Buffer[bar]
        HH = High[ArrayMaximum(High, bar, Period2)]
        LL = Low[ArrayMinimum(Low, bar, Period2)]
        Ext2Buffer[bar] = (HH + LL) / 2.0
        Ext2_Buffer[bar] = Ext2Buffer[bar]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ind2mohlc(_MQL5Indicator):
    name = '2mohlc_'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period1': 24,  # Period 1
        'Period2': 48,  # Period 2
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

