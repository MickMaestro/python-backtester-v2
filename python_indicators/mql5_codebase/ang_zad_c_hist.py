"""Ang_Zad_C_Hist — converted from MQL5: MQL5 Indicators/Ang_Zad_C_Hist/Ang_Zad_C_Hist.mq5

Copyright: Copyright © 2018, ANG3110; Link: ANG3110@latchess.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, ANG3110', 'link': 'ANG3110@latchess.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [3329330, 42495]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'Ang_Zad_C_Hist'}, 'levels': [], 'description': [], 'name': 'Ang_Zad_C_Hist', 'source': 'MQL5 Indicators/Ang_Zad_C_Hist/Ang_Zad_C_Hist.mq5', 'folder': 'Ang_Zad_C_Hist', 'inputs': [{'mql': 'ki', 'py': 'ki', 'param': 'ki', 'type': 'double', 'default': 4.000001, 'label': 'Коэффициент усреднения индикатора', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
ki = _input('ki', 4.000001)  # Коэффициент усреднения индикатора
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    shortname = Box("")
    StringConcatenate(shortname, 'Ang_Zad_C_Hist(', DoubleToString(ki, 4), ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_z2_prev, _s_OnCalculate_z_prev
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    price = 0.0
    price_prev = 0.0
    z = 0.0
    z2 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
        _s_OnCalculate_z2_prev = PriceSeries(IPC, first, open, low, high, close)
        _s_OnCalculate_z_prev = _s_OnCalculate_z2_prev
    else:
        first = prev_calculated - 1
    z = _s_OnCalculate_z_prev
    z2 = _s_OnCalculate_z2_prev
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        price_prev = PriceSeries(IPC, bar - 1, open, low, high, close)
        if price > z and price > price_prev:
            z = _s_OnCalculate_z_prev + ((price - _s_OnCalculate_z_prev) / ki)
        if price < z and price < price_prev:
            z = _s_OnCalculate_z_prev + ((price - _s_OnCalculate_z_prev) / ki)
        if price > z2 and price < price_prev:
            z2 = _s_OnCalculate_z2_prev + ((price - _s_OnCalculate_z2_prev) / ki)
        if price < z2 and price > price_prev:
            z2 = _s_OnCalculate_z2_prev + ((price - _s_OnCalculate_z2_prev) / ki)
        IndBuffer[bar] = _fdiv(z - z2, Point())
        if IndBuffer[bar] < 0.0:
            ColorIndBuffer[bar] = 1.0
        else:
            ColorIndBuffer[bar] = 0.0
        if bar < (rates_total - 1):
            _s_OnCalculate_z_prev = z
            _s_OnCalculate_z2_prev = z2
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def PriceSeries(applied_price, bar, Open, Low, High, Close):
    _sw1 = applied_price
    if _sw1 == PRICE_CLOSE:
        return Close[bar]
    elif _sw1 == PRICE_OPEN:
        return Open[bar]
    elif _sw1 == PRICE_HIGH:
        return High[bar]
    elif _sw1 == PRICE_LOW:
        return Low[bar]
    elif _sw1 == PRICE_MEDIAN:
        return (High[bar] + Low[bar]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (Close[bar] + High[bar] + Low[bar]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return ((2 * Close[bar]) + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 8:
        return (Open[bar] + Close[bar]) / 2.0
    elif _sw1 == 9:
        return (Open[bar] + Close[bar] + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 10:
        if Close[bar] > Open[bar]:
            return High[bar]
        else:
            if Close[bar] < Open[bar]:
                return Low[bar]
            else:
                return Close[bar]
    elif _sw1 == 11:
        if Close[bar] > Open[bar]:
            return (High[bar] + Close[bar]) / 2.0
        else:
            if Close[bar] < Open[bar]:
                return (Low[bar] + Close[bar]) / 2.0
            else:
                return Close[bar]
    elif _sw1 == 12:
        res = High[bar] + Low[bar] + Close[bar]
        if Close[bar] < Open[bar]:
            res = (res + Low[bar]) / 2
        if Close[bar] > Open[bar]:
            res = (res + High[bar]) / 2
        if Close[bar] == Open[bar]:
            res = (res + Close[bar]) / 2
        return (res - Low[bar] + (res - High[bar])) / 2
    else:
        return Close[bar]

# ---- static local variables
_s_OnCalculate_z_prev = 0.0
_s_OnCalculate_z2_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AngZadCHist(_MQL5Indicator):
    name = 'Ang_Zad_C_Hist'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ki': 4.000001,  # Коэффициент усреднения индикатора
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

