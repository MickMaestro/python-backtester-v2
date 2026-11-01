"""arrows_curves — converted from MQL5: MQL5 Indicators/Arrows&Curves/arrows_curves.mq5

Copyright: Copyright © 2007, Victor G. Lukashuck aka lukas1; Link: lukas1@ngs.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Victor G. Lukashuck aka lukas1', 'link': 'lukas1@ngs.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 8}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 1, 6: 1, 7: 1, 8: 1}, 'colors': {1: [16711935], 2: [65280], 3: [16711935], 4: [65280], 5: [42495], 6: [7451452], 7: [7451452], 8: [42495]}, 'widths': {1: 4, 2: 4, 3: 4, 4: 4, 5: 1, 6: 1, 7: 1, 8: 1}, 'styles': {5: 4, 6: 4, 7: 4, 8: 4}, 'labels': {1: 'Sell', 2: 'Buy', 3: 'SellStop', 4: 'BuyStop', 5: 'BUY from here', 6: 'BuyStop', 7: 'SellStop', 8: 'SELL from here'}, 'levels': [], 'description': [], 'name': 'arrows_curves', 'source': 'MQL5 Indicators/Arrows&Curves/arrows_curves.mq5', 'folder': 'Arrows&Curves', 'inputs': [{'mql': 'SSP', 'py': 'SSP', 'param': 'SSP', 'type': 'int', 'default': 20, 'label': 'reversal period', 'sinput': False}, {'mql': 'Channel', 'py': 'Channel', 'param': 'Channel', 'type': 'int', 'default': 0, 'label': 'Channel', 'sinput': False}, {'mql': 'Ch_Stop', 'py': 'Ch_Stop', 'param': 'Ch_Stop', 'type': 'int', 'default': 30, 'label': 'Stop Channel', 'sinput': False}, {'mql': 'relay', 'py': 'relay', 'param': 'relay', 'type': 'int', 'default': 10, 'label': 'shift', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SSP = _input('SSP', 20)  # reversal period
Channel = _input('Channel', 0)  # Channel
Ch_Stop = _input('Ch_Stop', 30)  # Stop Channel
relay = _input('relay', 10)  # shift
BuyBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
HBuffer = Arr(0, 0.0)
LBuffer = Arr(0, 0.0)
HSBuffer = Arr(0, 0.0)
LSBuffer = Arr(0, 0.0)
BuyStopBuffer = Arr(0, 0.0)
SellStopBuffer = Arr(0, 0.0)
StartBars = 0
uptrend_ = False
old_ = False
uptrend2_ = False
old2_ = False

def OnInit():
    global StartBars
    StartBars = SSP + 1 + relay
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(0, PLOT_LABEL, 'Sell')
    PlotIndexSetInteger(0, PLOT_ARROW, 108)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(1, PLOT_LABEL, 'Buy')
    PlotIndexSetInteger(1, PLOT_ARROW, 108)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, SellStopBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(2, PLOT_LABEL, 'SellStop')
    PlotIndexSetInteger(2, PLOT_ARROW, 251)
    ArraySetAsSeries(SellStopBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(3, BuyStopBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(3, PLOT_LABEL, 'BuyStop')
    PlotIndexSetInteger(3, PLOT_ARROW, 251)
    ArraySetAsSeries(BuyStopBuffer, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(4, HBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, HSBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, LSBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, LBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(7, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(4, PLOT_LABEL, 'BUY from here')
    PlotIndexSetString(5, PLOT_LABEL, 'BuyStop')
    PlotIndexSetString(6, PLOT_LABEL, 'SellStop')
    PlotIndexSetString(7, PLOT_LABEL, 'SELL from here')
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetDouble(7, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(HBuffer, True)
    ArraySetAsSeries(HSBuffer, True)
    ArraySetAsSeries(LSBuffer, True)
    ArraySetAsSeries(LBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Arrows&Curves'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_old, _s_OnCalculate_old2, _s_OnCalculate_uptrend, _s_OnCalculate_uptrend2, old2_, old_, uptrend2_, uptrend_
    if rates_total < StartBars:
        return 0
    limit = 0
    bar = 0
    High = 0.0
    Low = 0.0
    smin = 0.0
    smax = 0.0
    smin2 = 0.0
    smax2 = 0.0
    Close = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - StartBars
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    _s_OnCalculate_uptrend = uptrend_
    _s_OnCalculate_uptrend2 = uptrend2_
    _s_OnCalculate_old = old_
    _s_OnCalculate_old2 = old2_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            uptrend_ = _s_OnCalculate_uptrend
            uptrend2_ = _s_OnCalculate_uptrend2
            old_ = _s_OnCalculate_old
            old2_ = _s_OnCalculate_old2
        Close = close[bar]
        High = high[iHighest_u(high, SSP, bar + relay)]
        Low = low[iLowest_u(low, SSP, bar + relay)]
        smax = High - (((Low - High) * Channel) / 100)
        smin = Low + (((High - Low) * Channel) / 100)
        smax2 = High - (((High - Low) * (Channel + Ch_Stop)) / 100)
        smin2 = Low + (((High - Low) * (Channel + Ch_Stop)) / 100)
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        BuyStopBuffer[bar] = 0.0
        SellStopBuffer[bar] = 0.0
        if ((Close < smin and Close < smax) and _s_OnCalculate_uptrend2 == True) and bar != 0:
            _s_OnCalculate_uptrend = False
        if ((Close > smax and Close > smin) and _s_OnCalculate_uptrend2 == False) and bar != 0:
            _s_OnCalculate_uptrend = True
        if ((Close > smax2 or Close > smin2) and _s_OnCalculate_uptrend == False) and bar != 0:
            _s_OnCalculate_uptrend2 = False
        if ((Close < smin2 or Close < smax2) and _s_OnCalculate_uptrend == True) and bar != 0:
            _s_OnCalculate_uptrend2 = True
        if ((close[bar] < smin and close[bar] < smax) and _s_OnCalculate_uptrend2 == False) and bar != 0:
            SellBuffer[bar] = Low
            _s_OnCalculate_uptrend2 = True
        if ((Close > smax and Close > smin) and _s_OnCalculate_uptrend2 == True) and bar != 0:
            BuyBuffer[bar] = High
            _s_OnCalculate_uptrend2 = False
        if _s_OnCalculate_uptrend != _s_OnCalculate_old and _s_OnCalculate_uptrend == False:
            SellBuffer[bar] = Low
        if _s_OnCalculate_uptrend != _s_OnCalculate_old and _s_OnCalculate_uptrend == True:
            BuyBuffer[bar] = High
        if _s_OnCalculate_uptrend2 != _s_OnCalculate_old2 and _s_OnCalculate_uptrend2 == True:
            BuyStopBuffer[bar] = smax2
        if _s_OnCalculate_uptrend2 != _s_OnCalculate_old2 and _s_OnCalculate_uptrend2 == False:
            SellStopBuffer[bar] = smin2
        _s_OnCalculate_old = _s_OnCalculate_uptrend
        _s_OnCalculate_old2 = _s_OnCalculate_uptrend2
        HBuffer[bar] = smax
        LBuffer[bar] = smin
        HSBuffer[bar] = smax2
        LSBuffer[bar] = smin2
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def iHighest_u(array, count, startPos):
    index = startPos
    if startPos < 0:
        Print('Incorrect starting position in iHighest, startPos = ', startPos)
        return 0
    max_ = array[startPos]
    for i in range(startPos, startPos + count):
        if array[i] > max_:
            index = i
            max_ = array[i]
    return index

def iLowest_u(array, count, startPos):
    index = startPos
    if startPos < 0:
        Print('Incorrect starting position in iLowest, startPos = ', startPos)
        return 0
    min_ = array[startPos]
    for i in range(startPos, startPos + count):
        if array[i] < min_:
            index = i
            min_ = array[i]
    return index

# ---- static local variables
_s_OnCalculate_uptrend = False
_s_OnCalculate_old = False
_s_OnCalculate_uptrend2 = False
_s_OnCalculate_old2 = False


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ArrowsCurves(_MQL5Indicator):
    name = 'arrows_curves'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SSP': 20,  # reversal period
        'Channel': 0,  # Channel
        'Ch_Stop': 30,  # Stop Channel
        'relay': 10,  # shift
    }

