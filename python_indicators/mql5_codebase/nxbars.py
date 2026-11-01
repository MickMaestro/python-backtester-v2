"""nxbars — converted from MQL5: MQL5 Indicators/NxBars/nxbars.mq5

Copyright: Copyright © 2006, EvgeniX; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, EvgeniX', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'NxBars Sell', 2: 'NxBars Buy'}, 'levels': [], 'description': [], 'name': 'nxbars', 'source': 'MQL5 Indicators/NxBars/nxbars.mq5', 'folder': 'NxBars', 'inputs': [{'mql': 'HowManyBars', 'py': 'HowManyBars', 'param': 'HowManyBars', 'type': 'uint', 'default': 5, 'label': 'Number of bars for analysis', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
HowManyBars = _input('HowManyBars', 5)  # Number of bars for analysis
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Period = 15
    min_rates_total = _int(MathMax(ATR_Period, (2 * HowManyBars) + 2))
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_ARROW, 218)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_ARROW, 217)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'NxBars(' + _str(HowManyBars) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    barX = 0
    ATR = Arr(0, 0.0)
    shigh = 0.0
    slow = 0.0
    sclose = 0.0
    fhigh = 0.0
    flow = 0.0
    fclose = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + _int(HowManyBars) + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        barX = bar + _int(HowManyBars)
        shigh = high[ArrayMaximum(high, bar, HowManyBars)]
        slow = low[ArrayMinimum(low, bar, HowManyBars)]
        sclose = close[bar]
        fhigh = high[ArrayMaximum(high, barX, HowManyBars)]
        flow = low[ArrayMinimum(low, barX, HowManyBars)]
        fclose = close[barX]
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        BuyBuffer[barX] = 0.0
        SellBuffer[barX] = 0.0
        if shigh > fhigh and sclose < flow:
            SellBuffer[barX] = high[barX] + ((ATR[barX] * 3) / 8)
        if slow < flow and sclose > fhigh:
            BuyBuffer[barX] = low[barX] - ((ATR[barX] * 3) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Nxbars(_MQL5Indicator):
    name = 'nxbars'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'HowManyBars': 5,  # Number of bars for analysis
    }

