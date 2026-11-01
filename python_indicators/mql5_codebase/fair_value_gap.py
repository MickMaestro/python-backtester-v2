"""Fair_Value_Gap — converted from MQL5: MQL5 Indicators/Fair Value Gap/Fair_Value_Gap.mq5

Copyright: Copyright 2024, Rajesh Kumar Nait; Link: https://www.mql5.com/en/users/rajeshnait/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, Rajesh Kumar Nait', 'link': 'https://www.mql5.com/en/users/rajeshnait/seller', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Fair_Value_Gap', 'source': 'MQL5 Indicators/Fair Value Gap/Fair_Value_Gap.mq5', 'folder': 'Fair Value Gap', 'inputs': [{'mql': 'InpColorToUP', 'py': 'InpColorToUP', 'param': None, 'type': 'color', 'default': 65280, 'label': 'Color of the gap up', 'sinput': False}, {'mql': 'InpColorToDN', 'py': 'InpColorToDN', 'param': None, 'type': 'color', 'default': 9639167, 'label': 'Color of the gap down', 'sinput': False}, {'mql': 'maxbars', 'py': 'maxbars', 'param': 'maxbars', 'type': 'int', 'default': 300, 'label': 'how many bars to Look back', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpColorToUP = _input('InpColorToUP', clrLime)  # Color of the gap up
InpColorToDN = _input('InpColorToDN', clrDeepPink)  # Color of the gap down
maxbars = _input('maxbars', 300)  # how many bars to Look back
prefix = ""
price = 0.0

def OnInit():
    global prefix
    prefix = MQLInfoString(MQL_PROGRAM_NAME) + '_'
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, prefix)
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global price
    if rates_total < 4:
        return 0
    price = close[0]
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 5
    for i in range(maxbars, 0 - 1, -1):
        if (low[i] - high[i + 2]) >= Point():
            up = fmin(high[i], low[i])
            dn = fmax(high[i + 2], low[i + 2])
            DrawArea(i, up, dn, time, InpColorToUP, 1)
        if (low[i + 2] - high[i]) >= Point():
            up = fmin(high[i + 2], low[i + 2])
            dn = fmax(high[i], low[i])
            DrawArea(i, up, dn, time, InpColorToDN, 0)
    return rates_total

def DrawArea(index, price_up, price_dn, time, color_area, dir):
    name = prefix + ('up_' if (dir > 0) else 'dn_') + TimeToString(time[index])
    if ObjectFind(0, name) < 0:
        ObjectCreate(0, name, OBJ_RECTANGLE, 0, 0, 0, 0)
    ObjectSetInteger(0, name, OBJPROP_SELECTABLE, False)
    ObjectSetInteger(0, name, OBJPROP_HIDDEN, True)
    ObjectSetInteger(0, name, OBJPROP_FILL, True)
    ObjectSetInteger(0, name, OBJPROP_BACK, True)
    ObjectSetString(0, name, OBJPROP_TOOLTIP, '\n')
    ObjectSetInteger(0, name, OBJPROP_COLOR, color_area)
    ObjectSetInteger(0, name, OBJPROP_TIME, 0, time[index + 2])
    ObjectSetInteger(0, name, OBJPROP_TIME, 1, time[index])
    ObjectSetDouble(0, name, OBJPROP_PRICE, 0, price_up)
    ObjectSetDouble(0, name, OBJPROP_PRICE, 1, price_dn)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FairValueGap(_MQL5Indicator):
    name = 'Fair_Value_Gap'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'maxbars': 300,  # how many bars to Look back
    }

