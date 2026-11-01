"""cronex_impulse_macd — converted from MQL5: MQL5 Indicators/Cronex_Impulse_MACD_HTF/cronex_impulse_macd.mq5

Copyright: Copyright © 2008, Cronex; Link: http://www.metaquotes.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, Cronex', 'link': 'http://www.metaquotes.net/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 7, 2: 10}, 'colors': {1: [65280, 255], 2: [8721863, 15631086, 8421504, 16760576, 16711680]}, 'widths': {2: 2}, 'styles': {2: 0}, 'labels': {1: 'Cronex_Impulse_MACD Signal', 2: 'Cronex_Impulse_MACD'}, 'levels': [], 'description': [], 'name': 'cronex_impulse_macd', 'source': 'MQL5 Indicators/Cronex_Impulse_MACD_HTF/cronex_impulse_macd.mq5', 'folder': 'Cronex_Impulse_MACD_HTF', 'inputs': [{'mql': 'Master_MA', 'py': 'Master_MA', 'param': 'Master_MA', 'type': 'uint', 'default': 34, 'label': 'Период усреднения MACD', 'sinput': False}, {'mql': 'Signal_MA', 'py': 'Signal_MA', 'param': 'Signal_MA', 'type': 'uint', 'default': 9, 'label': 'Период сигнальной линии', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Master_MA = _input('Master_MA', 34)  # Период усреднения MACD
Signal_MA = _input('Signal_MA', 9)  # Период сигнальной линии
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
MAh_Handle = 0
MAl_Handle = 0
MAw_Handle = 0
min_rates_total = 0
min_rates_1 = 0

def OnInit():
    global MAh_Handle, MAl_Handle, MAw_Handle, min_rates_1, min_rates_total
    min_rates_1 = _int(Master_MA + 1)
    min_rates_total = _int(min_rates_1 + Signal_MA + 1)
    MAh_Handle = iMA(None, 0, Master_MA, 0, MODE_SMMA, PRICE_HIGH)
    if MAh_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA 1')
        return INIT_FAILED
    MAl_Handle = iMA(None, 0, Master_MA, 0, MODE_SMMA, PRICE_LOW)
    if MAl_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA 2')
        return INIT_FAILED
    MAw_Handle = iMA(None, 0, Master_MA, 0, MODE_SMA, PRICE_WEIGHTED)
    if MAw_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA 3')
        return INIT_FAILED
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnBuffer, True)
    SetIndexBuffer(2, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(3, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    shortname = Box("")
    StringConcatenate(shortname, 'Cronex_Impulse_MACD(', Master_MA, ', ', Signal_MA, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((BarsCalculated(MAh_Handle) < rates_total or BarsCalculated(MAl_Handle) < rates_total) or BarsCalculated(MAw_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    MAh = Arr(0, 0.0)
    MAl = Arr(0, 0.0)
    MAw = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_1 - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(MAh_Handle, 0, 0, to_copy, MAh) <= 0:
        return 0
    if CopyBuffer(MAl_Handle, 0, 0, to_copy, MAl) <= 0:
        return 0
    if CopyBuffer(MAw_Handle, 0, 0, to_copy, MAw) <= 0:
        return 0
    ArraySetAsSeries(MAh, True)
    ArraySetAsSeries(MAl, True)
    ArraySetAsSeries(MAw, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IndBuffer[bar] = 0.0
        if MAw[bar] > MAh[bar]:
            IndBuffer[bar] = MAw[bar] - MAh[bar]
        if MAw[bar] < MAl[bar]:
            IndBuffer[bar] = MAw[bar] - MAl[bar]
        IndBuffer[bar] = _fdiv(IndBuffer[bar], Point())
        UpBuffer[bar] = IndBuffer[bar]
        Sum = 0.0
        if IndBuffer[bar]:
            for iii in range(0, _int(Signal_MA)):
                Sum += IndBuffer[MathMin(bar + iii, rates_total - 1)]
            DnBuffer[bar] = Sum / Signal_MA
        else:
            UpBuffer[bar] = UpBuffer[bar + 1]
            DnBuffer[bar] = UpBuffer[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        clr = 2
        if IndBuffer[bar] > 0:
            if IndBuffer[bar] > IndBuffer[bar + 1]:
                clr = 4
            if IndBuffer[bar] < IndBuffer[bar + 1]:
                clr = 3
        if IndBuffer[bar] < 0:
            if IndBuffer[bar] < IndBuffer[bar + 1]:
                clr = 0
            if IndBuffer[bar] > IndBuffer[bar + 1]:
                clr = 1
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CronexImpulseMacd(_MQL5Indicator):
    name = 'cronex_impulse_macd'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Master_MA': 34,  # Период усреднения MACD
        'Signal_MA': 9,  # Период сигнальной линии
    }

