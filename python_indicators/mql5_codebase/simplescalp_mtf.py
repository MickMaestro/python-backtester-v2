"""simplescalp_mtf — converted from MQL5: MQL5 Indicators/SimpleScalp_MTF/simplescalp_mtf.mq5

Индикатор направленного тренда
Copyright: Copyright © 2011, MetaQuotes Software Corp.; Link: http://www.mql4.com/ru/users/kontra; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, MetaQuotes Software Corp.', 'link': 'http://www.mql4.com/ru/users/kontra', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [4678655], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'SimpleScalp_MTF Sell', 2: 'SimpleScalp_MTF Buy'}, 'levels': [], 'description': ['Индикатор направленного тренда'], 'name': 'simplescalp_mtf', 'source': 'MQL5 Indicators/SimpleScalp_MTF/simplescalp_mtf.mq5', 'folder': 'SimpleScalp_MTF', 'inputs': [{'mql': 'TimeFrame1', 'py': 'TimeFrame1', 'param': 'TimeFrame1', 'type': 'int', 'default': 16385, 'label': 'Период графика 1', 'sinput': False}, {'mql': 'TimeFrame2', 'py': 'TimeFrame2', 'param': 'TimeFrame2', 'type': 'int', 'default': 30, 'label': 'Период графика 2', 'sinput': False}, {'mql': 'TimeFrame3', 'py': 'TimeFrame3', 'param': 'TimeFrame3', 'type': 'int', 'default': 15, 'label': 'Период графика 3', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame1 = _input('TimeFrame1', PERIOD_H1)  # Период графика 1
TimeFrame2 = _input('TimeFrame2', PERIOD_M30)  # Период графика 2
TimeFrame3 = _input('TimeFrame3', PERIOD_M15)  # Период графика 3
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
ATR_Handle = 0

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Period = 15
    min_rates_total = 2
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    if TimeFrame1 <= Period():
        Alert('Период графика 1 должен быть больше периода текущего графика!')
    if TimeFrame2 <= Period():
        Alert('Период графика 2 должен быть больше периода текущего графика!')
    if TimeFrame3 <= Period():
        Alert('Период графика 3 должен быть больше периода текущего графика!')
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 178)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 178)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'SimpleScalp_MTF'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (((Bars(Symbol(), TimeFrame1) < min_rates_total or Bars(Symbol(), TimeFrame2) < min_rates_total) or Bars(Symbol(), TimeFrame3) < min_rates_total) or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    iClose1 = Arr(0, 0.0)
    iClose2 = Arr(0, 0.0)
    iClose3 = Arr(0, 0.0)
    iOpen1 = Arr(0, 0.0)
    iOpen2 = Arr(0, 0.0)
    iOpen3 = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(iClose1, True)
    ArraySetAsSeries(iClose2, True)
    ArraySetAsSeries(iClose3, True)
    ArraySetAsSeries(iOpen1, True)
    ArraySetAsSeries(iOpen2, True)
    ArraySetAsSeries(iOpen3, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(ATR, True)
    for bar in range(limit, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if CopyClose(Symbol(), TimeFrame1, _DT(time[bar]), min_rates_total, iClose1) <= 0:
            return 0
        if CopyClose(Symbol(), TimeFrame2, _DT(time[bar]), min_rates_total, iClose2) <= 0:
            return 0
        if CopyClose(Symbol(), TimeFrame3, _DT(time[bar]), min_rates_total, iClose3) <= 0:
            return 0
        if CopyOpen(Symbol(), TimeFrame1, _DT(time[bar]), min_rates_total, iOpen1) <= 0:
            return 0
        if CopyOpen(Symbol(), TimeFrame2, _DT(time[bar]), min_rates_total, iOpen2) <= 0:
            return 0
        if CopyOpen(Symbol(), TimeFrame3, _DT(time[bar]), min_rates_total, iOpen3) <= 0:
            return 0
        if (((iClose1[1] - iOpen1[1]) > 0 and (iClose2[1] - iOpen2[1]) > 0) and (iClose3[1] - iOpen3[1]) > 0) and (close[bar + 1] - open[bar + 1]) > 0:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if (((iClose1[1] - iOpen1[1]) < 0 and (iClose2[1] - iOpen2[1]) < 0) and (iClose3[1] - iOpen3[1]) < 0) and (close[bar + 1] - open[bar + 1]) < 0:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SimplescalpMtf(_MQL5Indicator):
    name = 'simplescalp_mtf'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame1': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # Период графика 1
        'TimeFrame2': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=30),  # Период графика 2
        'TimeFrame3': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=15),  # Период графика 3
    }

