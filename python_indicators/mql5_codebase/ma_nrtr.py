"""ma_nrtr — converted from MQL5: MQL5 Indicators/MA_NRTR/ma_nrtr.mq5

Copyright: Copyright © 2012, Ivan Kornilov; Link: excelf@gmail.com; Version: 7.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Ivan Kornilov', 'link': 'excelf@gmail.com', 'version': '7.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [9639167], 2: [8421376], 3: [8388352], 4: [255]}, 'widths': {1: 2, 2: 2, 3: 4, 4: 4}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Upper MA NRTR', 2: 'Lower MA NRTR', 3: ' MA NRTR Buy', 4: ' MA NRTR Sell'}, 'levels': [], 'description': [], 'name': 'ma_nrtr', 'source': 'MQL5 Indicators/MA_NRTR/ma_nrtr.mq5', 'folder': 'MA_NRTR', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 12, 'label': 'indicator period', 'sinput': False}, {'mql': 'MAShift', 'py': 'MAShift', 'param': 'MAShift', 'type': 'int', 'default': 150, 'label': 'vertical shift of MA in points', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 0, 'label': 'smoothing method', 'sinput': False}, {'mql': 'OneWay', 'py': 'OneWay', 'param': 'OneWay', 'type': 'bool', 'default': True, 'label': 'indicator movement without a rollback', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 12)  # indicator period
MAShift = _input('MAShift', 150)  # vertical shift of MA in points
MA_Method = _input('MA_Method', MODE_SMA)  # smoothing method
OneWay = _input('OneWay', True)  # indicator movement without a rollback
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
MAShift_ = 0.0
MAH_Handle = 0
MAL_Handle = 0
min_rates_total = 0

def OnInit():
    global MAH_Handle, MAL_Handle, MAShift_, min_rates_total
    min_rates_total = Length + 1
    MAShift_ = MAShift * Point()
    MAH_Handle = iMA(None, 0, Length, 0, MA_Method, PRICE_HIGH)
    if MAH_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
        return 1
    MAL_Handle = iMA(None, 0, Length, 0, MA_Method, PRICE_LOW)
    if MAL_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
        return 1
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(UpBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(2, PLOT_ARROW, 164)
    SetIndexBuffer(3, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(3, PLOT_ARROW, 164)
    shortname = Box("")
    StringConcatenate(shortname, 'StepMA NRTR (', Length, ', ', MAShift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_down1, _s_OnCalculate_trend1, _s_OnCalculate_up1
    if (BarsCalculated(MAH_Handle) < rates_total or BarsCalculated(MAL_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    up0 = 0.0
    down0 = 0.0
    trend0 = 0.0
    MAH = Arr(0, 0.0)
    MAL = Arr(0, 0.0)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(MAH, True)
    ArraySetAsSeries(MAL, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        _s_OnCalculate_trend1 = 0.0
        _s_OnCalculate_up1 = 999999999.9999
        _s_OnCalculate_down1 = 0.0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(MAH_Handle, 0, 0, to_copy, MAH) <= 0:
        return 0
    if CopyBuffer(MAL_Handle, 0, 0, to_copy, MAL) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        UpBuffer[bar] = 0.0
        DnBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        BuyBuffer[bar] = 0.0
        trend0 = _s_OnCalculate_trend1
        up0 = MAH[bar + 1] + MAShift_
        down0 = MAL[bar + 1] - MAShift_
        if OneWay:
            if _s_OnCalculate_trend1 == 1 and down0 < _s_OnCalculate_down1:
                down0 = _s_OnCalculate_down1
            if _s_OnCalculate_trend1 == -1 and up0 > _s_OnCalculate_up1:
                up0 = _s_OnCalculate_up1
        if high[bar] > up0:
            trend0 = 1.0
        if low[bar] < down0:
            trend0 = -1.0
        if trend0 == -1.0:
            UpBuffer[bar] = up0
        if trend0 == 1.0:
            DnBuffer[bar] = down0
        if (not DnBuffer[bar + 1]) and DnBuffer[bar]:
            BuyBuffer[bar] = DnBuffer[bar]
        if (not UpBuffer[bar + 1]) and UpBuffer[bar]:
            SellBuffer[bar] = UpBuffer[bar]
        if bar:
            _s_OnCalculate_up1 = up0
            _s_OnCalculate_down1 = down0
            _s_OnCalculate_trend1 = trend0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_up1 = 0.0
_s_OnCalculate_down1 = 0.0
_s_OnCalculate_trend1 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MaNrtr(_MQL5Indicator):
    name = 'ma_nrtr'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 12,  # indicator period
        'MAShift': 150,  # vertical shift of MA in points
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # smoothing method
        'OneWay': True,  # indicator movement without a rollback
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

