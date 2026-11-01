"""WATR — converted from MQL5: MQL5 Indicators/WATR_HTF_Signal/WATR.mq5

Copyright: Written WizardSerg under article konkop in <Modern trading> #4/2001; Link: http://www.wizardserg.inweb.ru; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Written WizardSerg under article konkop in <Modern trading> #4/2001', 'link': 'http://www.wizardserg.inweb.ru', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [16748574], 2: [5275647], 3: [16776960], 4: [16711935]}, 'widths': {1: 2, 2: 2, 3: 4, 4: 4}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Upper WATR', 2: 'Lower WATR', 3: 'Upper WATR', 4: 'Lower WATR'}, 'levels': [], 'description': [], 'name': 'WATR', 'source': 'MQL5 Indicators/WATR_HTF_Signal/WATR.mq5', 'folder': 'WATR_HTF_Signal', 'inputs': [{'mql': 'WATR_K', 'py': 'WATR_K', 'param': 'WATR_K', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'WATR_M', 'py': 'WATR_M', 'param': 'WATR_M', 'type': 'double', 'default': 4.0, 'label': '', 'sinput': False}, {'mql': 'ATR', 'py': 'ATR', 'param': 'ATR', 'type': 'int', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
WATR_K = _input('WATR_K', 10)
WATR_M = _input('WATR_M', 4.0)
ATR = _input('ATR', 21)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
ExtMapBufferUp = Arr(0, 0.0)
ExtMapBufferDown = Arr(0, 0.0)
ExtMapBufferUp1 = Arr(0, 0.0)
ExtMapBufferDown1 = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0

def AntiTrendBar(Open, Close, bar):
    res = (TrendUp(Close, bar) and Close[bar] < Open[bar]) or ((not TrendUp(Close, bar)) and Close[bar] > Open[bar])
    return res

def CalcIndicValue(ATRArray, Close, bar, trend):
    res = Close[bar]
    if trend:
        res -= (WATR_K * Point()) + (WATR_M * ATRArray[bar])
    else:
        res += (WATR_K * Point()) + (WATR_M * ATRArray[bar])
    return res

def TrendUp(Close, bar):
    return Close[bar + 1] > ExtMapBufferUp[bar + 1] and ExtMapBufferUp[bar + 1] != EMPTY_VALUE

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Handle = iATR(None, 0, ATR)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
    min_rates_total = ATR
    SetIndexBuffer(0, ExtMapBufferUp, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(0, PLOT_LABEL, 'Upper WATR')
    ArraySetAsSeries(ExtMapBufferUp, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ExtMapBufferDown, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(1, PLOT_LABEL, 'Lower WATR')
    ArraySetAsSeries(ExtMapBufferDown, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, ExtMapBufferUp1, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(2, PLOT_LABEL, 'Upper WATR')
    ArraySetAsSeries(ExtMapBufferUp1, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_ARROW, 108)
    SetIndexBuffer(3, ExtMapBufferDown1, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(3, PLOT_LABEL, 'Lower WATR')
    ArraySetAsSeries(ExtMapBufferDown1, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_ARROW, 108)
    shortname = Box("")
    StringConcatenate(shortname, 'WATR(', WATR_K, ', ', WATR_M, ', ', ATR, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    iATR_ = Arr(0, 0.0)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(iATR_, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        to_copy = rates_total
        ExtMapBufferUp[limit + 1] = close[limit + 1] - (WATR_K * Point())
    else:
        limit = rates_total - prev_calculated
        to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, iATR_) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if AntiTrendBar(open, close, bar):
            ExtMapBufferUp[bar] = ExtMapBufferUp[bar + 1]
            ExtMapBufferDown[bar] = ExtMapBufferDown[bar + 1]
        else:
            if TrendUp(close, bar):
                ExtMapBufferUp[bar] = CalcIndicValue(iATR_, close, bar, True)
                if ExtMapBufferUp[bar] < ExtMapBufferUp[bar + 1]:
                    ExtMapBufferUp[bar] = ExtMapBufferUp[bar + 1]
                ExtMapBufferDown[bar] = EMPTY_VALUE
            else:
                ExtMapBufferDown[bar] = CalcIndicValue(iATR_, close, bar, False)
                ExtMapBufferDown1[bar] = ExtMapBufferDown[bar]
                if ExtMapBufferDown[bar] > ExtMapBufferDown[bar + 1]:
                    ExtMapBufferDown[bar] = ExtMapBufferDown[bar + 1]
                ExtMapBufferUp[bar] = EMPTY_VALUE
        if TrendUp(close, bar) and close[bar] < ExtMapBufferUp[bar]:
            ExtMapBufferDown[bar] = CalcIndicValue(iATR_, close, bar, False)
            ExtMapBufferUp[bar] = EMPTY_VALUE
        if (not TrendUp(close, bar)) and close[bar] > ExtMapBufferDown[bar]:
            ExtMapBufferUp[bar] = CalcIndicValue(iATR_, close, bar, True)
            ExtMapBufferDown[bar] = EMPTY_VALUE
        ExtMapBufferUp1[bar] = EMPTY_VALUE
        ExtMapBufferDown1[bar] = EMPTY_VALUE
        if ExtMapBufferUp[bar + 1] == EMPTY_VALUE and ExtMapBufferUp[bar] != EMPTY_VALUE:
            ExtMapBufferUp1[bar] = ExtMapBufferUp[bar]
        if ExtMapBufferDown[bar + 1] == EMPTY_VALUE and ExtMapBufferDown[bar] != EMPTY_VALUE:
            ExtMapBufferDown1[bar] = ExtMapBufferDown[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WATR(_MQL5Indicator):
    name = 'WATR'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'WATR_K': 10,
        'WATR_M': 4.0,
        'ATR': 21,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

