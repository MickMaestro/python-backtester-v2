"""trendmanageropen — converted from MQL5: MQL5 Indicators/TrendManagerOpen/trendmanageropen.mq5

Copyright: Copyright © 2007, Matt Kennel; Link: mbkennel@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Matt Kennel', 'link': 'mbkennel@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 7, 2: 1, 3: 1}, 'colors': {1: [10025880, 16711935], 2: [13434880], 3: [13434880]}, 'widths': {2: 1, 3: 1}, 'styles': {}, 'labels': {1: 'TrendManagerOpen', 2: 'TrendManagerOpen Line1', 3: 'TrendManagerOpen Line2'}, 'levels': [], 'description': [], 'name': 'trendmanageropen', 'source': 'MQL5 Indicators/TrendManagerOpen/trendmanageropen.mq5', 'folder': 'TrendManagerOpen', 'inputs': [{'mql': 'TM_Period_1', 'py': 'TM_Period_1', 'param': 'TM_Period_1', 'type': 'int', 'default': 7, 'label': '', 'sinput': False}, {'mql': 'TM_Shift_1', 'py': 'TM_Shift_1', 'param': 'TM_Shift_1', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'TM_Period_2', 'py': 'TM_Period_2', 'param': 'TM_Period_2', 'type': 'int', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'TM_Shift_2', 'py': 'TM_Shift_2', 'param': 'TM_Shift_2', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TM_Period_1 = _input('TM_Period_1', 7)
TM_Shift_1 = _input('TM_Shift_1', 2)
TM_Period_2 = _input('TM_Period_2', 13)
TM_Shift_2 = _input('TM_Shift_2', 1)
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
min_rates_total = 0
UpBuffer1 = Arr(0, 0.0)
DnBuffer1 = Arr(0, 0.0)
UpBuffer2 = Arr(0, 0.0)
DnBuffer2 = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = MathMax(TM_Period_1 + TM_Shift_1, TM_Period_2 + TM_Shift_2)
    SetIndexBuffer(0, UpBuffer1, INDICATOR_DATA)
    ArraySetAsSeries(UpBuffer1, True)
    SetIndexBuffer(1, DnBuffer1, INDICATOR_DATA)
    ArraySetAsSeries(DnBuffer1, True)
    SetIndexBuffer(2, UpBuffer2, INDICATOR_DATA)
    ArraySetAsSeries(UpBuffer2, True)
    SetIndexBuffer(3, DnBuffer2, INDICATOR_DATA)
    ArraySetAsSeries(DnBuffer2, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TrendManagerOpen')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if rates_total < min_rates_total:
        return 0
    M1 = 0.0
    M1b = 0.0
    M2 = 0.0
    M2b = 0.0
    diff1 = 0.0
    diff2 = 0.0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    for bar in range(limit, 0 - 1, -1):
        M1 = Get_MiddlePrice(TM_Period_1, bar, High, Low)
        M1b = Get_MiddlePrice(TM_Period_1, bar + TM_Shift_1, High, Low)
        M2 = Get_MiddlePrice(TM_Period_2, bar, High, Low)
        M2b = Get_MiddlePrice(TM_Period_2, bar + TM_Shift_2, High, Low)
        diff1 = M1 - M1b
        diff2 = M2 - M2b
        if (diff1 * diff2) <= 0.0:
            UpBuffer1[bar] = (M1 + M2) * 0.5
            UpBuffer2[bar] = UpBuffer1[bar]
            DnBuffer1[bar] = UpBuffer1[bar]
            DnBuffer2[bar] = DnBuffer1[bar]
        else:
            UpBuffer1[bar] = (M1 + M2) * 0.5
            UpBuffer2[bar] = UpBuffer1[bar]
            DnBuffer1[bar] = (M1b + M2b) * 0.5
            DnBuffer2[bar] = DnBuffer1[bar]
    return rates_total

def Get_MiddlePrice(period, shift, high, low):
    HH = high[ArrayMaximum(high, shift, period)]
    LL = low[ArrayMinimum(low, shift, period)]
    return (HH + LL) / 2.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Trendmanageropen(_MQL5Indicator):
    name = 'trendmanageropen'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TM_Period_1': 7,
        'TM_Shift_1': 2,
        'TM_Period_2': 13,
        'TM_Shift_2': 1,
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

