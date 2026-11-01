"""ind_amu — converted from MQL5: MQL5 Indicators/ind_aMU/ind_amu.mq5

Индикатор указывает на трендовые и боковые (флет) движения цены
Copyright: Copyright © 2012, Yuriy Tokman (YTG); Link: yuriytokman@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Yuriy Tokman (YTG)', 'link': 'yuriytokman@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 6}, 'colors': {1: [14822282]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'ind_aMU'}, 'levels': [], 'description': ['Индикатор указывает на трендовые и боковые (флет) движения цены'], 'name': 'ind_amu', 'source': 'MQL5 Indicators/ind_aMU/ind_amu.mq5', 'folder': 'ind_aMU', 'inputs': [{'mql': 'FastPeriod', 'py': 'FastPeriod', 'param': 'FastPeriod', 'type': 'uint', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'SlowPeriod', 'py': 'SlowPeriod', 'param': 'SlowPeriod', 'type': 'uint', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FastPeriod = _input('FastPeriod', 12)
SlowPeriod = _input('SlowPeriod', 21)
MAType = _input('MAType', MODE_EMA)
MAPrice = _input('MAPrice', PRICE_CLOSE)
SlowBuffer = Arr(0, 0.0)
FastBuffer = Arr(0, 0.0)
min_rates_total = 0
FsMA_Handle = 0
SlMA_Handle = 0

def OnInit():
    global FsMA_Handle, SlMA_Handle, min_rates_total
    min_rates_total = _int(MathMax(FastPeriod, SlowPeriod))
    SlMA_Handle = iMA(Symbol(), PERIOD_CURRENT, FastPeriod, 0, MAType, MAPrice)
    if SlMA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Fast iMA')
        return INIT_FAILED
    FsMA_Handle = iMA(Symbol(), PERIOD_CURRENT, SlowPeriod, 0, MAType, MAPrice)
    if FsMA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Slow iMA')
        return INIT_FAILED
    SetIndexBuffer(0, FastBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SlowBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(FastBuffer, True)
    ArraySetAsSeries(SlowBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    shortname = Box("")
    StringConcatenate(shortname, 'ind_aMU(', FastPeriod, ',', SlowPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(FsMA_Handle) < rates_total or BarsCalculated(SlMA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total - min_rates_total + 1
    else:
        to_copy = rates_total - prev_calculated + 1
    if CopyBuffer(FsMA_Handle, 0, 0, to_copy, FastBuffer) <= 0:
        return 0
    if CopyBuffer(SlMA_Handle, 0, 0, to_copy, SlowBuffer) <= 0:
        return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IndAmu(_MQL5Indicator):
    name = 'ind_amu'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastPeriod': 12,
        'SlowPeriod': 21,
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
    }

