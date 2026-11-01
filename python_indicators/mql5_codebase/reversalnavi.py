"""reversalnavi — converted from MQL5: MQL5 Indicators/ReversalNavi/reversalnavi.mq5

Copyright: Copyright © 2015, fxborg; Link: http://blog.livedoor.jp/fxborg/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, fxborg', 'link': 'http://blog.livedoor.jp/fxborg/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 6}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 1, 6: 1}, 'colors': {1: [255], 2: [16748574], 3: [255], 4: [16748574], 5: [255], 6: [16748574]}, 'widths': {1: 4, 2: 4, 3: 4, 4: 4, 5: 2, 6: 2}, 'styles': {5: 0, 6: 0}, 'labels': {1: 'Sell Reversal Bar Mark', 2: 'Buy Reversal Bar Mark', 3: 'Sell Reversal Bar', 4: 'Buy Reversal Bar', 5: 'Sell Reversal Bar Line', 6: 'Buy Reversal Bar Line'}, 'levels': [], 'description': [], 'name': 'reversalnavi', 'source': 'MQL5 Indicators/ReversalNavi/reversalnavi.mq5', 'folder': 'ReversalNavi', 'inputs': [{'mql': 'InpHiLoPeriod', 'py': 'InpHiLoPeriod', 'param': 'InpHiLoPeriod', 'type': 'int', 'default': 8, 'label': 'High Low Period', 'sinput': False}, {'mql': 'InpStanbyBars', 'py': 'InpStanbyBars', 'param': 'InpStanbyBars', 'type': 'int', 'default': 8, 'label': 'Stanby Bars', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpHiLoPeriod = _input('InpHiLoPeriod', 8)  # High Low Period
InpStanbyBars = _input('InpStanbyBars', 8)  # Stanby Bars
CalcBarCount = 4  # Calc Bar Count
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtTopBuffer = Arr(0, 0.0)
ExtBtmBuffer = Arr(0, 0.0)
ExtSellStandbyBuffer = Arr(0, 0.0)
ExtBuyStandbyBuffer = Arr(0, 0.0)
ExtSellLineBuffer = Arr(0, 0.0)
ExtBuyLineBuffer = Arr(0, 0.0)
ExtHighesBuffer = Arr(0, 0.0)
ExtLowesBuffer = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Period = 10
    min_rates_total = MathMax(InpHiLoPeriod + InpStanbyBars + CalcBarCount, ATR_Period)
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, ExtTopBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 218)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, ExtBtmBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 217)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(2, ExtSellStandbyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(3, ExtBuyStandbyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(4, ExtSellLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(5, ExtBuyLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(5, PLOT_SHIFT, Shift)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(6, ExtHighesBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(7, ExtLowesBuffer, INDICATOR_CALCULATIONS)
    shortname = Box("")
    StringConcatenate(shortname, 'ReversalNavi(', InpHiLoPeriod, ', ', InpStanbyBars, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    dmin = 0.0
    dmax = 0.0
    entry_point = 0.0
    range_lo = 0.0
    range_hi = 0.0
    ATR = Arr(1, 0.0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        dmin = 1000000.0
        dmax = -1000000.0
        for iii in range(bar - InpHiLoPeriod + 1, bar + 1):
            if dmin > low[iii]:
                dmin = low[iii]
            if dmax < high[iii]:
                dmax = high[iii]
        ExtLowesBuffer[bar] = dmin
        ExtHighesBuffer[bar] = dmax
        ExtBuyStandbyBuffer[bar] = 0.0
        ExtSellStandbyBuffer[bar] = 0.0
        ExtBuyLineBuffer[bar] = 0.0
        ExtSellLineBuffer[bar] = 0.0
        ExtTopBuffer[bar] = 0.0
        ExtBtmBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first
    for bar in range(bar, rates_total):
        btm_pos = bar - 1
        for iii in range(bar - 1, 1, -1):
            if ExtLowesBuffer[iii - 2] > ExtLowesBuffer[iii - 1] and ExtLowesBuffer[iii - 1] == ExtLowesBuffer[iii]:
                btm_pos = iii - 1
                break
        setup = 0
        for iii in range(btm_pos, bar - 1 + 1):
            if ExtBuyStandbyBuffer[iii]:
                setup = iii
                break
        entry_point = 0.0
        range_lo = 1000000.0
        range_hi = -1000000.0
        if (not setup) or (bar - setup) <= InpStanbyBars:
            for iii in range(btm_pos, bar - 1 + 1):
                if range_hi < high[iii]:
                    range_hi = high[iii]
                if range_lo > low[iii]:
                    range_lo = low[iii]
            entry_point = (range_hi + range_lo) / 2
            ExtBuyLineBuffer[bar] = entry_point
        if MathMin(low[bar - 4], MathMin(low[bar - 3], low[bar - 2])) < low[bar - 1]:
            if not setup:
                if CopyBuffer(ATR_Handle, 0, _DT(time[btm_pos]), 1, ATR) <= 0:
                    return 0
                ExtBtmBuffer[btm_pos] = low[btm_pos] - MathMax((ATR[0] * 3) / 8, 5 * Point())
                ExtBuyStandbyBuffer[bar] = entry_point
        top_pos = bar - 1
        for iii in range(bar - 1, 1, -1):
            if ExtHighesBuffer[iii - 2] < ExtHighesBuffer[iii - 1] and ExtHighesBuffer[iii - 1] == ExtHighesBuffer[iii]:
                top_pos = iii - 1
                break
        setup = 0
        for iii in range(top_pos, bar - 1 + 1):
            if ExtSellStandbyBuffer[iii]:
                setup = iii
                break
        entry_point = 0.0
        range_lo = 1000000.0
        range_hi = -1000000.0
        if (not setup) or (bar - setup) <= InpStanbyBars:
            for iii in range(top_pos, bar - 1 + 1):
                if range_hi < high[iii]:
                    range_hi = high[iii]
                if range_lo > low[iii]:
                    range_lo = low[iii]
            entry_point = (range_hi + range_lo) / 2
            ExtSellLineBuffer[bar] = entry_point
        if MathMax(high[bar - 4], MathMax(high[bar - 3], high[bar - 2])) > high[bar - 1]:
            if not setup:
                if CopyBuffer(ATR_Handle, 0, _DT(time[top_pos]), 1, ATR) <= 0:
                    return 0
                ExtTopBuffer[top_pos] = high[top_pos] + MathMax((ATR[0] * 3) / 8, 5 * Point())
                ExtSellStandbyBuffer[bar] = entry_point
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Reversalnavi(_MQL5Indicator):
    name = 'reversalnavi'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpHiLoPeriod': 8,  # High Low Period
        'InpStanbyBars': 8,  # Stanby Bars
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

