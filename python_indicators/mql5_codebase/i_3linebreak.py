"""3linebreak — converted from MQL5: MQL5 Indicators/3LineBreak/3linebreak.mq5

Copyright:  Copyright © 2004, Poul_Trade_Forum; Link:  http://forex.kbpauk.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': ' Copyright © 2004, Poul_Trade_Forum', 'link': ' http://forex.kbpauk.ru/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 11}, 'colors': {1: [16711680, 255]}, 'widths': {1: 2}, 'styles': {}, 'labels': {1: 'UpTend; DownTrend;'}, 'levels': [], 'description': [], 'name': '3linebreak', 'source': 'MQL5 Indicators/3LineBreak/3linebreak.mq5', 'folder': '3LineBreak', 'inputs': [{'mql': 'Lines_Break', 'py': 'Lines_Break', 'param': 'Lines_Break', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Lines_Break = _input('Lines_Break', 3)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtColorsBuffer = Arr(0, 0.0)
Swing_ = False
StartBars = 0

def OnInit():
    global StartBars
    StartBars = Lines_Break
    SetIndexBuffer(0, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtColorsBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtColorsBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = '3LineBreak'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global Swing_
    if rates_total < StartBars:
        return 0
    limit = 0
    bar = 0
    VALUE1 = 0.0
    VALUE2 = 0.0
    OLDSwing = False
    Swing = False
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - StartBars
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    Swing = Swing_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            Swing_ = Swing
        OLDSwing = Swing
        VALUE1 = high[ArrayMaximum(high, bar + 1, Lines_Break)]
        VALUE2 = low[ArrayMinimum(low, bar + 1, Lines_Break)]
        if OLDSwing and low[bar] < VALUE2:
            Swing = False
        if (not OLDSwing) and high[bar] > VALUE1:
            Swing = True
        ExtHighBuffer[bar] = high[bar]
        ExtLowBuffer[bar] = low[bar]
        if Swing:
            ExtColorsBuffer[bar] = 0.0
        else:
            ExtColorsBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ind3linebreak(_MQL5Indicator):
    name = '3linebreak'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Lines_Break': 3,
    }

