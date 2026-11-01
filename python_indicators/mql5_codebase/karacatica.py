"""karacatica — converted from MQL5: MQL5 Indicators/Karacatica/karacatica.mq5

Copyright: Copyright © 2006, MetaQuotes Software Corp.; Link: http://www.metaquotes.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'Karacatica Sell', 2: 'Karacatica Buy'}, 'levels': [], 'description': [], 'name': 'karacatica', 'source': 'MQL5 Indicators/Karacatica/karacatica.mq5', 'folder': 'Karacatica', 'inputs': [{'mql': 'iPeriod', 'py': 'iPeriod', 'param': 'iPeriod', 'type': 'int', 'default': 70, 'label': 'ATR period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
iPeriod = _input('iPeriod', 70)  # ATR period
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
s = 0.0
StartBars = 0
ATR_Handle = 0
ADX_Handle = 0
ltr = 0
ltr_ = 0

def OnInit():
    global ADX_Handle, ATR_Handle, StartBars, s
    s = 1.5 / 2.0
    StartBars = iPeriod + 1
    ATR_Handle = iATR(None, 0, iPeriod)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
    ADX_Handle = iADX(None, 0, iPeriod)
    if ADX_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ADX indicator')
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(0, PLOT_LABEL, 'Karacatica Sell')
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(1, PLOT_LABEL, 'Karacatica Buy')
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Karacatica'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global ltr, ltr_
    if (BarsCalculated(ATR_Handle) < rates_total or BarsCalculated(ADX_Handle) < rates_total) or rates_total < StartBars:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    ADXP = Arr(0, 0.0)
    ADXM = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
        limit = rates_total - StartBars
    else:
        to_copy = rates_total - prev_calculated + 1
        limit = rates_total - prev_calculated
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    if CopyBuffer(ADX_Handle, 1, 0, to_copy, ADXP) <= 0:
        return 0
    if CopyBuffer(ADX_Handle, 2, 0, to_copy, ADXM) <= 0:
        return 0
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(ADXP, True)
    ArraySetAsSeries(ADXM, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ltr = ltr_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            ltr_ = ltr
        SellBuffer[bar] = 0.0
        BuyBuffer[bar] = 0.0
        if BuyBuffer[bar + 1] != 0 and BuyBuffer[bar + 1] != EMPTY_VALUE:
            ltr = 1
        if SellBuffer[bar + 1] != 0 and SellBuffer[bar + 1] != EMPTY_VALUE:
            ltr = 2
        if (close[bar] > close[bar + iPeriod] and ADXP[bar] > ADXM[bar]) and ltr != 1:
            BuyBuffer[bar] = low[bar] - (ATR[bar] * s)
        if (close[bar] < close[bar + iPeriod] and ADXP[bar] < ADXM[bar]) and ltr != 2:
            SellBuffer[bar] = high[bar] + (ATR[bar] * s)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Karacatica(_MQL5Indicator):
    name = 'karacatica'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iPeriod': 70,  # ATR period
    }

