"""XAng_Zad_C — converted from MQL5: MQL5 Indicators/XAng_Zad_C/XAng_Zad_C.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [65280, 42495]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Ang_Zad_C'}, 'levels': [], 'description': [], 'name': 'XAng_Zad_C', 'source': 'MQL5 Indicators/XAng_Zad_C/XAng_Zad_C.mq5', 'folder': 'XAng_Zad_C', 'inputs': [{'mql': 'ki', 'py': 'ki', 'param': 'ki', 'type': 'double', 'default': 4.000001, 'label': 'Коэффициент усреднения индикатора', 'sinput': False}, {'mql': 'MA_SMethod', 'py': 'MA_SMethod', 'param': 'MA_SMethod', 'type': 'int', 'default': 4, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'MA_Length', 'py': 'MA_Length', 'param': 'MA_Length', 'type': 'uint', 'default': 7, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'MA_Phase', 'py': 'MA_Phase', 'param': 'MA_Phase', 'type': 'int', 'default': 15, 'label': 'параметр первого сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора по вертикали в пунктах', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
MA_SMethod = _input('MA_SMethod', MODE_JJMA)  # Метод усреднения
MA_Length = _input('MA_Length', 7)  # Глубина сглаживания
MA_Phase = _input('MA_Phase', 15)  # параметр первого сглаживания,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
PriceShift = _input('PriceShift', 0)  # cдвиг индикатора по вертикали в пунктах
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
min_rates_1 = 0
min_rates_total = 0
dPriceShift = 0.0

def OnInit():
    global dPriceShift, min_rates_1, min_rates_total
    min_rates_1 = 2
    min_rates_total = min_rates_1 + GetStartBars(MA_SMethod, MA_Length, MA_Phase)
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, UpIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'XAng_Zad_C(', DoubleToString(ki, 4), ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
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
        first = min_rates_1
        DnIndBuffer[first - 1] = PriceSeries(IPC, first - 1, open, low, high, close) + dPriceShift
        UpIndBuffer[first - 1] = DnIndBuffer[first - 1]
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
        UpIndBuffer[bar] = XMA1.XMASeries(min_rates_1, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, z, bar, False)
        DnIndBuffer[bar] = XMA2.XMASeries(min_rates_1, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, z2, bar, False)
        UpIndBuffer[bar] += dPriceShift
        DnIndBuffer[bar] += dPriceShift
        if bar < (rates_total - 1):
            _s_OnCalculate_z_prev = z
            _s_OnCalculate_z2_prev = z2
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()

# ---- static local variables
_s_OnCalculate_z_prev = 0.0
_s_OnCalculate_z2_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XAngZadC(_MQL5Indicator):
    name = 'XAng_Zad_C'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ki': 4.000001,  # Коэффициент усреднения индикатора
        'MA_SMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод усреднения
        'MA_Length': 7,  # Глубина сглаживания
        'MA_Phase': 15,  # параметр первого сглаживания,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'PriceShift': 0,  # cдвиг индикатора по вертикали в пунктах
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

