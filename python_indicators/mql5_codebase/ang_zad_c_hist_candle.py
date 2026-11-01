"""Ang_Zad_C_Hist_Candle — converted from MQL5: MQL5 Indicators/Ang_Zad_C_Hist_Candle/Ang_Zad_C_Hist_Candle.mq5

Copyright: Copyright © 2018, ANG3110; Link: ANG3110@latchess.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, ANG3110', 'link': 'ANG3110@latchess.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16711680, 16748574, 8421504, 12695295, 16711935]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Ang_Zad_C_Hist_Open;Ang_Zad_C_Hist_High;Ang_Zad_C_Hist_Low;Ang_Zad_C_Hist_Close'}, 'levels': [], 'description': [], 'name': 'Ang_Zad_C_Hist_Candle', 'source': 'MQL5 Indicators/Ang_Zad_C_Hist_Candle/Ang_Zad_C_Hist_Candle.mq5', 'folder': 'Ang_Zad_C_Hist_Candle', 'inputs': [{'mql': 'ki', 'py': 'ki', 'param': 'ki', 'type': 'double', 'default': 4.000001, 'label': 'Коэффициент усреднения индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ki = _input('ki', 4.000001)  # Коэффициент усреднения индикатора
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorsBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorsBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    shortname = Box("")
    StringConcatenate(shortname, 'Ang_Zad_C_Hist_Candle(', DoubleToString(ki, 4), ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Cz2_prev, _s_OnCalculate_Cz_prev, _s_OnCalculate_Hz2_prev, _s_OnCalculate_Hz_prev, _s_OnCalculate_Lz2_prev, _s_OnCalculate_Lz_prev, _s_OnCalculate_Oz2_prev, _s_OnCalculate_Oz_prev
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    price = 0.0
    price_prev = 0.0
    Oz = 0.0
    Oz2 = 0.0
    Hz = 0.0
    Hz2 = 0.0
    Lz = 0.0
    Lz2 = 0.0
    Cz = 0.0
    Cz2 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
        _s_OnCalculate_Oz2_prev = open[first - 1]
        _s_OnCalculate_Oz_prev = _s_OnCalculate_Oz2_prev
        _s_OnCalculate_Hz2_prev = high[first - 1]
        _s_OnCalculate_Hz_prev = _s_OnCalculate_Hz2_prev
        _s_OnCalculate_Lz2_prev = low[first - 1]
        _s_OnCalculate_Lz_prev = _s_OnCalculate_Lz2_prev
        _s_OnCalculate_Cz2_prev = close[first - 1]
        _s_OnCalculate_Cz_prev = _s_OnCalculate_Cz2_prev
    else:
        first = prev_calculated - 1
    Oz = _s_OnCalculate_Oz_prev
    Oz2 = _s_OnCalculate_Oz2_prev
    Hz = _s_OnCalculate_Hz_prev
    Hz2 = _s_OnCalculate_Hz2_prev
    Lz = _s_OnCalculate_Lz_prev
    Lz2 = _s_OnCalculate_Lz2_prev
    Cz = _s_OnCalculate_Cz_prev
    Cz2 = _s_OnCalculate_Cz2_prev
    bar = first
    for bar in range(bar, rates_total):
        price = open[bar]
        price_prev = open[bar - 1]
        if price > Oz and price > price_prev:
            Oz = _s_OnCalculate_Oz_prev + ((price - _s_OnCalculate_Oz_prev) / ki)
        if price < Oz and price < price_prev:
            Oz = _s_OnCalculate_Oz_prev + ((price - _s_OnCalculate_Oz_prev) / ki)
        if price > Oz2 and price < price_prev:
            Oz2 = _s_OnCalculate_Lz2_prev + ((price - _s_OnCalculate_Oz2_prev) / ki)
        if price < Oz2 and price > price_prev:
            Oz2 = _s_OnCalculate_Cz2_prev + ((price - _s_OnCalculate_Oz2_prev) / ki)
        ExtOpenBuffer[bar] = _fdiv(Oz - Oz2, Point())
        price = high[bar]
        price_prev = high[bar - 1]
        if price > Hz and price > price_prev:
            Hz = _s_OnCalculate_Hz_prev + ((price - _s_OnCalculate_Hz_prev) / ki)
        if price < Hz and price < price_prev:
            Hz = _s_OnCalculate_Hz_prev + ((price - _s_OnCalculate_Hz_prev) / ki)
        if price > Hz2 and price < price_prev:
            Hz2 = _s_OnCalculate_Lz2_prev + ((price - _s_OnCalculate_Hz2_prev) / ki)
        if price < Hz2 and price > price_prev:
            Hz2 = _s_OnCalculate_Cz2_prev + ((price - _s_OnCalculate_Hz2_prev) / ki)
        ExtHighBuffer[bar] = _fdiv(Hz - Hz2, Point())
        price = low[bar]
        price_prev = low[bar - 1]
        if price > Lz and price > price_prev:
            Lz = _s_OnCalculate_Lz_prev + ((price - _s_OnCalculate_Lz_prev) / ki)
        if price < Lz and price < price_prev:
            Lz = _s_OnCalculate_Lz_prev + ((price - _s_OnCalculate_Lz_prev) / ki)
        if price > Lz2 and price < price_prev:
            Lz2 = _s_OnCalculate_Lz2_prev + ((price - _s_OnCalculate_Lz2_prev) / ki)
        if price < Lz2 and price > price_prev:
            Lz2 = _s_OnCalculate_Cz2_prev + ((price - _s_OnCalculate_Lz2_prev) / ki)
        ExtLowBuffer[bar] = _fdiv(Lz - Lz2, Point())
        price = close[bar]
        price_prev = close[bar - 1]
        if price > Cz and price > price_prev:
            Cz = _s_OnCalculate_Cz_prev + ((price - _s_OnCalculate_Cz_prev) / ki)
        if price < Cz and price < price_prev:
            Cz = _s_OnCalculate_Cz_prev + ((price - _s_OnCalculate_Cz_prev) / ki)
        if price > Cz2 and price < price_prev:
            Cz2 = _s_OnCalculate_Lz2_prev + ((price - _s_OnCalculate_Cz2_prev) / ki)
        if price < Cz2 and price > price_prev:
            Cz2 = _s_OnCalculate_Cz2_prev + ((price - _s_OnCalculate_Cz2_prev) / ki)
        ExtCloseBuffer[bar] = _fdiv(Cz - Cz2, Point())
        Max = MathMax(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        Min = MathMin(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        ExtHighBuffer[bar] = MathMax(Max, ExtHighBuffer[bar])
        ExtLowBuffer[bar] = MathMin(Min, ExtLowBuffer[bar])
        ExtColorsBuffer[bar] = 2.0
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            if ExtCloseBuffer[bar - 1] <= ExtCloseBuffer[bar]:
                ExtColorsBuffer[bar] = 0.0
            else:
                ExtColorsBuffer[bar] = 1.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            if ExtCloseBuffer[bar - 1] >= ExtCloseBuffer[bar]:
                ExtColorsBuffer[bar] = 4.0
            else:
                ExtColorsBuffer[bar] = 3.0
        if bar < (rates_total - 1):
            _s_OnCalculate_Oz_prev = Oz
            _s_OnCalculate_Oz2_prev = Oz2
            _s_OnCalculate_Hz_prev = Hz
            _s_OnCalculate_Hz2_prev = Hz2
            _s_OnCalculate_Lz_prev = Lz
            _s_OnCalculate_Lz2_prev = Lz2
            _s_OnCalculate_Cz_prev = Cz
            _s_OnCalculate_Cz2_prev = Cz2
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_Oz_prev = 0.0
_s_OnCalculate_Oz2_prev = 0.0
_s_OnCalculate_Hz_prev = 0.0
_s_OnCalculate_Hz2_prev = 0.0
_s_OnCalculate_Lz_prev = 0.0
_s_OnCalculate_Lz2_prev = 0.0
_s_OnCalculate_Cz_prev = 0.0
_s_OnCalculate_Cz2_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AngZadCHistCandle(_MQL5Indicator):
    name = 'Ang_Zad_C_Hist_Candle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ki': 4.000001,  # Коэффициент усреднения индикатора
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

