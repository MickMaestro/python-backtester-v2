"""Dominant — converted from MQL5: MQL5 Indicators/Dominant Candle/Dominant.mq5

Copyright: Copyright 2024, Rajesh Kumar Nait; Link: https://www.mql5.com/en/users/rajeshnait/seller; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2024, Rajesh Kumar Nait', 'link': 'https://www.mql5.com/en/users/rajeshnait/seller', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'Dominant', 'source': 'MQL5 Indicators/Dominant Candle/Dominant.mq5', 'folder': 'Dominant Candle', 'inputs': [{'mql': 'total', 'py': 'total', 'param': 'total', 'type': 'int', 'default': 1000, 'label': 'Number of Bars', 'sinput': False}, {'mql': 'clr', 'py': 'clr', 'param': None, 'type': 'color', 'default': 16448255, 'label': 'Adjust color as required', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
prefix = 'c_'
total = _input('total', 1000)  # Number of Bars
clr = _input('clr', clrSnow)  # Adjust color as required

def OnInit():
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, prefix)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    if rates_total < total:
        Print('Required Bars not available')
        return rates_total
    for i in range(1, total):
        if (((open[i] < close[i] and open[i + 1] < close[i + 1]) and open[i] >= close[i + 1]) and low[i] < close[i + 1]) and high[i + 1] > open[i]:
            crearFlecha(prefix + 'Bull_Dominanat' + IntegerToString(i), time[i], low[i + 1], clr, 225, ANCHOR_TOP)
        if (((open[i] > close[i] and open[i + 1] > close[i + 1]) and open[i] <= close[i + 1]) and high[i] > close[i + 1]) and low[i + 1] < open[i]:
            crearFlecha(prefix + 'Bear_Dominanat' + IntegerToString(i), time[i], high[i + 1], clr, 226, ANCHOR_BOTTOM)
    return rates_total

def crearFlecha(nameAux, timeAux, priceAux, clrAux, code, anchorAux):
    chart_ID = 0
    name = nameAux
    sub_window = 0
    time = timeAux
    price = priceAux
    arrow_code = code
    anchor = anchorAux
    clr_ = clrAux
    style = STYLE_SOLID
    width = 1
    back = True
    selection = False
    hidden = True
    z_order = 0
    ObjectCreate(chart_ID, name, OBJ_ARROW, sub_window, time, price)
    ObjectSetInteger(chart_ID, name, OBJPROP_ARROWCODE, arrow_code)
    ObjectSetInteger(chart_ID, name, OBJPROP_ANCHOR, anchorAux)
    ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr_)
    ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
    ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
    ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
    ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dominant(_MQL5Indicator):
    name = 'Dominant'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'total': 1000,  # Number of Bars
    }

