"""Support_and_Resistance — converted from MQL5: MQL5 Indicators/Support_and_Resistance_HTF/Support_and_Resistance.mq5

Copyright: Copyright © 2006, MetaQuotes Software Corp.; Link: http://www.metaquotes.net/; Version: 1.12

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net/', 'version': '1.12', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Support', 2: 'Resistance'}, 'levels': [], 'description': [], 'name': 'Support_and_Resistance', 'source': 'MQL5 Indicators/Support_and_Resistance_HTF/Support_and_Resistance.mq5', 'folder': 'Support_and_Resistance_HTF', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
StartBars = 0
FRA_Handle = 0

def OnInit():
    global FRA_Handle, StartBars
    StartBars = 6
    FRA_Handle = iFractals(None, 0)
    if FRA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iFractals')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(0, PLOT_LABEL, 'Support')
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(1, PLOT_LABEL, 'Resistance')
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Support & Resistance'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(FRA_Handle) < rates_total or rates_total < StartBars:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    FRAUp = Arr(0, 0.0)
    FRALo = Arr(0, 0.0)
    upVel = 0.0
    loVel = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
        limit = rates_total - StartBars - 1
    else:
        to_copy = rates_total - prev_calculated + 3
        limit = rates_total - prev_calculated + 2
    ArraySetAsSeries(FRAUp, True)
    ArraySetAsSeries(FRALo, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    if CopyBuffer(FRA_Handle, 0, 0, to_copy, FRAUp) <= 0:
        return 0
    if CopyBuffer(FRA_Handle, 1, 0, to_copy, FRALo) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        upVel = FRAUp[bar]
        loVel = FRALo[bar]
        if upVel and upVel != EMPTY_VALUE:
            BuyBuffer[bar] = high[bar]
        else:
            BuyBuffer[bar] = BuyBuffer[bar + 1]
        if loVel and loVel != EMPTY_VALUE:
            SellBuffer[bar] = low[bar]
        else:
            SellBuffer[bar] = SellBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SupportAndResistance(_MQL5Indicator):
    name = 'Support_and_Resistance'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

