"""gainlossinfo — converted from MQL5: MQL5 Indicators/GainLossInfo/gainlossinfo.mq5

Shows percentage and pip gain/loss for a candle.
Can calculate gain/loss compared either to the previous Close or to the current Open.
Copyright: Copyright © 2013, Andriy Moraru; Link: http://www.earnforex.com; Version: 1.0

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2013, Andriy Moraru', 'link': 'http://www.earnforex.com', 'version': '1.0', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Shows percentage and pip gain/loss for a candle.', 'Can calculate gain/loss compared either to the previous Close or to the current Open.'], 'name': 'gainlossinfo', 'source': 'MQL5 Indicators/GainLossInfo/gainlossinfo.mq5', 'folder': 'GainLossInfo', 'inputs': [{'mql': 'PercentageLimit', 'py': 'PercentageLimit', 'param': 'PercentageLimit', 'type': 'double', 'default': 1.0, 'label': 'PercentageLimit - Will not display number if percentage gain/loss is below limit.', 'sinput': False}, {'mql': 'PipsLimit', 'py': 'PipsLimit', 'param': 'PipsLimit', 'type': 'int', 'default': 1000, 'label': 'PipsLimit - Will not display number if pips gain/loss is below limit.', 'sinput': False}, {'mql': 'CloseToClose', 'py': 'CloseToClose', 'param': 'CloseToClose', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'DisplayLossColor', 'py': 'DisplayLossColor', 'param': None, 'type': 'color', 'default': 255, 'label': '', 'sinput': False}, {'mql': 'DisplayGainColor', 'py': 'DisplayGainColor', 'param': None, 'type': 'color', 'default': 3329330, 'label': '', 'sinput': False}, {'mql': 'DisplayDistance', 'py': 'DisplayDistance', 'param': 'DisplayDistance', 'type': 'int', 'default': 100, 'label': 'DisplayDistance - Distance in pips from High/Low to percentage display.', 'sinput': False}, {'mql': 'MaxBars', 'py': 'MaxBars', 'param': 'MaxBars', 'type': 'int', 'default': 100, 'label': 'MaxBars: More bars - more objects - more lag and memory usage.', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
PercentageLimit = _input('PercentageLimit', 1.0)  # PercentageLimit - Will not display number if percentage gain/loss is below limit.
PipsLimit = _input('PipsLimit', 1000)  # PipsLimit - Will not display number if pips gain/loss is below limit.
CloseToClose = _input('CloseToClose', True)
DisplayLossColor = _input('DisplayLossColor', clrRed)
DisplayGainColor = _input('DisplayGainColor', clrLimeGreen)
DisplayDistance = _input('DisplayDistance', 100)  # DisplayDistance - Distance in pips from High/Low to percentage display.
MaxBars = _input('MaxBars', 100)  # MaxBars: More bars - more objects - more lag and memory usage.

def OnInit():
    pass

def OnDeinit(reason):
    ObjectsDeleteAll(0, 0, OBJ_TEXT)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, tick_volume, volume, spread):
    name = ""
    perc = ""
    pips = ""
    index = rates_total - 1
    start = 0.0
    counted_bars = prev_calculated
    if counted_bars > 0:
        counted_bars -= 1
    limit = counted_bars
    if (rates_total - counted_bars) > MaxBars:
        limit = rates_total - MaxBars
    for i in range(rates_total - 1, limit - 1, -1):
        if CloseToClose and i > 0:
            start = Close[i - 1]
        else:
            start = Open[i]
        if (_fdiv(Close[i] - start, start) * 100) >= PercentageLimit:
            name = 'RedPercent-' + TimeToString(Time[i], TIME_DATE | TIME_MINUTES)
            perc = DoubleToString(_fdiv(Close[i] - start, start) * 100, 1) + '%'
            if ObjectFind(0, name) != -1:
                ObjectDelete(0, name)
            ObjectCreate(0, name, OBJ_TEXT, 0, Time[i], High[i] + (DisplayDistance * Point()))
            ObjectSetString(0, name, OBJPROP_TEXT, perc)
            ObjectSetInteger(0, name, OBJPROP_FONTSIZE, 10)
            ObjectSetString(0, name, OBJPROP_FONT, 'Verdana')
            ObjectSetInteger(0, name, OBJPROP_COLOR, DisplayGainColor)
        elif (_fdiv(start - Close[i], start) * 100) >= PercentageLimit:
            name = 'GreenPercent-' + TimeToString(Time[i], TIME_DATE | TIME_MINUTES)
            perc = DoubleToString(_fdiv(start - Close[i], start) * 100, 1) + '%'
            if ObjectFind(0, name) != -1:
                ObjectDelete(0, name)
            ObjectCreate(0, name, OBJ_TEXT, 0, Time[i], High[i] + (DisplayDistance * Point()))
            ObjectSetString(0, name, OBJPROP_TEXT, perc)
            ObjectSetInteger(0, name, OBJPROP_FONTSIZE, 10)
            ObjectSetString(0, name, OBJPROP_FONT, 'Verdana')
            ObjectSetInteger(0, name, OBJPROP_COLOR, DisplayLossColor)
        if _fdiv(Close[i] - start, Point()) >= PipsLimit:
            name = 'RedPips-' + TimeToString(Time[i], TIME_DATE | TIME_MINUTES)
            pips = DoubleToString(_fdiv(Close[i] - start, Point()), 0)
            if ObjectFind(0, name) != -1:
                ObjectDelete(0, name)
            ObjectCreate(0, name, OBJ_TEXT, 0, Time[i], Low[i])
            ObjectSetString(0, name, OBJPROP_TEXT, pips)
            ObjectSetInteger(0, name, OBJPROP_FONTSIZE, 10)
            ObjectSetString(0, name, OBJPROP_FONT, 'Verdana')
            ObjectSetInteger(0, name, OBJPROP_COLOR, DisplayGainColor)
        elif _fdiv(start - Close[i], Point()) >= PipsLimit:
            name = 'GreenPips-' + TimeToString(Time[i], TIME_DATE | TIME_MINUTES)
            pips = DoubleToString(_fdiv(start - Close[i], Point()), 0)
            if ObjectFind(0, name) != -1:
                ObjectDelete(0, name)
            ObjectCreate(0, name, OBJ_TEXT, 0, Time[i], Low[i])
            ObjectSetString(0, name, OBJPROP_TEXT, pips)
            ObjectSetInteger(0, name, OBJPROP_FONTSIZE, 10)
            ObjectSetString(0, name, OBJPROP_FONT, 'Verdana')
            ObjectSetInteger(0, name, OBJPROP_COLOR, DisplayLossColor)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Gainlossinfo(_MQL5Indicator):
    name = 'gainlossinfo'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PercentageLimit': 1.0,  # PercentageLimit - Will not display number if percentage gain/loss is below limit.
        'PipsLimit': 1000,  # PipsLimit - Will not display number if pips gain/loss is below limit.
        'CloseToClose': True,
        'DisplayDistance': 100,  # DisplayDistance - Distance in pips from High/Low to percentage display.
        'MaxBars': 100,  # MaxBars: More bars - more objects - more lag and memory usage.
    }

