"""dynamicrs_3clines — converted from MQL5: MQL5 Indicators/DynamicRS_3CLines/dynamicrs_3clines.mq5

Copyright: Copyright © 2006, Renato P. dos Santos; Link: http://www.strategybuilderfx.com/forums/showthread.php?t=16086; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Renato P. dos Santos', 'link': 'http://www.strategybuilderfx.com/forums/showthread.php?t=16086', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [36095], 2: [14381203], 3: [65280]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Top', 2: 'ExtMap', 3: 'Bottom'}, 'levels': [], 'description': [''], 'name': 'dynamicrs_3clines', 'source': 'MQL5 Indicators/DynamicRS_3CLines/dynamicrs_3clines.mq5', 'folder': 'DynamicRS_3CLines', 'inputs': [{'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
Ind1Buffer = Arr(0, 0.0)
Ind2Buffer = Arr(0, 0.0)
Ind3Buffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, Ind1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Ind1Buffer, True)
    SetIndexBuffer(1, Ind2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Ind2Buffer, True)
    SetIndexBuffer(2, Ind3Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Ind3Buffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'DynamicRS_3CLines')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
        bar = limit + 1
        res = (high[bar] + low[bar]) / 2
        Ind1Buffer[bar] = res
        Ind2Buffer[bar] = res
        Ind3Buffer[bar] = res
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Ind1Buffer[bar] = Ind1Buffer[bar + 1]
        Ind2Buffer[bar] = Ind2Buffer[bar + 1]
        Ind3Buffer[bar] = Ind3Buffer[bar + 1]
        if high[bar] < high[bar + 1] and high[bar] < Ind2Buffer[bar + 1]:
            Ind2Buffer[bar] = high[bar]
            Ind3Buffer[bar] = high[bar]
            Ind1Buffer[bar] = Ind1Buffer[bar + 1]
        elif low[bar] > low[bar + 1] and low[bar] > Ind2Buffer[bar + 1]:
            Ind2Buffer[bar] = low[bar]
            Ind1Buffer[bar] = low[bar]
            Ind3Buffer[bar] = Ind3Buffer[bar + 1]
        else:
            Ind2Buffer[bar] = Ind2Buffer[bar + 1]
            if Ind2Buffer[bar + 1] == Ind1Buffer[bar + 1]:
                Ind1Buffer[bar] = Ind2Buffer[bar + 1]
                Ind3Buffer[bar] = Ind3Buffer[bar + 1]
            elif Ind2Buffer[bar + 1] == Ind3Buffer[bar + 1]:
                Ind3Buffer[bar] = Ind2Buffer[bar + 1]
                Ind1Buffer[bar] = Ind1Buffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dynamicrs3clines(_MQL5Indicator):
    name = 'dynamicrs_3clines'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

