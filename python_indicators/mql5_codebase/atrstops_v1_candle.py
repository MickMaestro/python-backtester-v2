"""ATRStops_v1_Candle — converted from MQL5: MQL5 Indicators/ATRStops_v1_Candle/ATRStops_v1_Candle.mq5

Copyright: Copyright © 2006, Forex-TSD.com ; Link: http://www.forex-tsd.com/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Forex-TSD.com ', 'link': 'http://www.forex-tsd.com/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [65280, 8421376, 8421504, 128, 9639167]}, 'widths': {}, 'styles': {}, 'labels': {1: 'ATRStops_v1_Open;ATRStops_v1_High;ATRStops_v1_Low;ATRStops_v1_Close'}, 'levels': [], 'description': [], 'name': 'ATRStops_v1_Candle', 'source': 'MQL5 Indicators/ATRStops_v1_Candle/ATRStops_v1_Candle.mq5', 'folder': 'ATRStops_v1_Candle', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 10, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'ATRPeriod', 'py': 'ATRPeriod', 'param': 'ATRPeriod', 'type': 'uint', 'default': 5, 'label': 'Период индикатора ATR', 'sinput': False}, {'mql': 'Kv', 'py': 'Kv', 'param': 'Kv', 'type': 'double', 'default': 2.5, 'label': 'Волатильность по ATR', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 10)  # Период индикатора
ATRPeriod = _input('ATRPeriod', 5)  # Период индикатора ATR
Kv = _input('Kv', 2.5)  # Волатильность по ATR
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorsBuffer = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Handle = iATR(None, 0, ATRPeriod)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    min_rates_total = _int(ATRPeriod + Length)
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorsBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorsBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'ATRStops_v1_Candle(', Length, ', ', ATRPeriod, ', ', DoubleToString(Kv, 4), ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_smax1, _s_OnCalculate_smin1, _s_OnCalculate_trend1
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    ATR = Arr(0, 0.0)
    smin0 = 0.0
    smax0 = 0.0
    limit = 0
    to_copy = 0
    bar = 0
    trend0 = 0
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(ATR, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_trend1 = 0
        _s_OnCalculate_smin1 = -DBL_MAX
        _s_OnCalculate_smax1 = DBL_MAX
    else:
        limit = rates_total - prev_calculated
    to_copy = _int(limit + Length)
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtOpenBuffer[bar] = open[bar]
        ExtHighBuffer[bar] = high[bar]
        ExtLowBuffer[bar] = low[bar]
        ExtCloseBuffer[bar] = close[bar]
        smin0 = -DBL_MAX
        smax0 = DBL_MAX
        for iii in range(0, _int(Length)):
            barx = bar + iii
            res = Kv * ATR[barx]
            smin0 = MathMax(smin0, high[barx] - res)
            smax0 = MathMin(smax0, low[barx] + res)
        trend0 = _s_OnCalculate_trend1
        if close[bar] > _s_OnCalculate_smax1:
            trend0 = 1
        if close[bar] < _s_OnCalculate_smin1:
            trend0 = -1
        if trend0 > 0:
            if smin0 < _s_OnCalculate_smin1:
                smin0 = _s_OnCalculate_smin1
            if open[bar] <= close[bar]:
                ExtColorsBuffer[bar] = 0.0
            else:
                ExtColorsBuffer[bar] = 1.0
        if trend0 < 0:
            if smax0 > _s_OnCalculate_smax1:
                smax0 = _s_OnCalculate_smax1
            if open[bar] >= close[bar]:
                ExtColorsBuffer[bar] = 4.0
            else:
                ExtColorsBuffer[bar] = 3.0
        if bar > 0:
            _s_OnCalculate_smin1 = smin0
            _s_OnCalculate_smax1 = smax0
            _s_OnCalculate_trend1 = trend0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_smin1 = 0.0
_s_OnCalculate_smax1 = 0.0
_s_OnCalculate_trend1 = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ATRStopsV1Candle(_MQL5Indicator):
    name = 'ATRStops_v1_Candle'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 10,  # Период индикатора
        'ATRPeriod': 5,  # Период индикатора ATR
        'Kv': 2.5,  # Волатильность по ATR
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

