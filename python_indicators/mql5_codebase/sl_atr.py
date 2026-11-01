"""sl_atr — converted from MQL5: MQL5 Indicators/SL_ATR/sl_atr.mq5

The indicator shows the best places for setting a stop-loss for current positions.
The indicator can be used for trailing stop operation.
Copyright: Copyright © 2011, Vladimir Hlystov; Link: cmillion@narod.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Vladimir Hlystov', 'link': 'cmillion@narod.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 7}, 'colors': {1: [9498256, 9498256], 2: [15631086, 15631086]}, 'widths': {}, 'styles': {}, 'labels': {1: 'StopLoss Sell Min/Max', 2: 'StopLoss Buy Min/Max'}, 'levels': [], 'description': ['The indicator shows the best places for setting a stop-loss for current positions.', 'The indicator can be used for trailing stop operation.'], 'name': 'sl_atr', 'source': 'MQL5 Indicators/SL_ATR/sl_atr.mq5', 'folder': 'SL_ATR', 'inputs': [{'mql': 'Period_ATR', 'py': 'Period_ATR', 'param': 'Period_ATR', 'type': 'int', 'default': 14, 'label': 'АТR period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Period_ATR = _input('Period_ATR', 14)  # АТR period
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
ExtLineBuffer4 = Arr(0, 0.0)
ATR_Handle = 0
StartBars = 0
StartBars1 = 0
StartBars2 = 0

def OnInit():
    global ATR_Handle, StartBars
    StartBars = Period_ATR
    ATR_Handle = iATR(None, 0, Period_ATR)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
    SetIndexBuffer(0, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, ExtLineBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLineBuffer3, INDICATOR_DATA)
    SetIndexBuffer(3, ExtLineBuffer4, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer1, True)
    ArraySetAsSeries(ExtLineBuffer2, True)
    ArraySetAsSeries(ExtLineBuffer3, True)
    ArraySetAsSeries(ExtLineBuffer4, True)
    shortname = Box("")
    StringConcatenate(shortname, 'SL_ATR(', Period_ATR, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < StartBars:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    Range = Arr(0, 0.0)
    ATR = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - StartBars
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, Range) <= 0:
        return 0
    ArraySetAsSeries(Range, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ATR = Range[bar]
        ExtLineBuffer1[bar] = NormalizeDouble(low[bar] + ATR, Digits())
        ExtLineBuffer2[bar] = NormalizeDouble(high[bar] + ATR, Digits())
        ExtLineBuffer3[bar] = NormalizeDouble(high[bar] - ATR, Digits())
        ExtLineBuffer4[bar] = NormalizeDouble(low[bar] - ATR, Digits())
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SlAtr(_MQL5Indicator):
    name = 'sl_atr'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period_ATR': 14,  # АТR period
    }

