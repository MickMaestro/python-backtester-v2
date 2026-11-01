"""kalmanfilter — converted from MQL5: MQL5 Indicators/KalmanFilterCandle/kalmanfilter.mq5

Copyright: Copyright © 2010, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [42495, 13688896]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'KalmanFilter'}, 'levels': [], 'description': [], 'name': 'kalmanfilter', 'source': 'MQL5 Indicators/KalmanFilterCandle/kalmanfilter.mq5', 'folder': 'KalmanFilterCandle', 'inputs': [{'mql': 'K', 'py': 'K', 'param': 'K', 'type': 'double', 'default': 1.0, 'label': 'Коэффициент сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 7, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Signal', 'py': 'Signal', 'param': 'Signal', 'type': 'int', 'default': 1, 'label': 'Метод изменения окраски линии', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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

# enum Signal_mode
Trend = 0
Kalman = 1
_enum('Signal_mode', {0: 'Trend', 1: 'Kalman'})

# ---- inputs and global variables
K = _input('K', 1.0)  # Коэффициент сглаживания
IPC = _input('IPC', PRICE_WEIGHTED)  # Ценовая константа
Signal = _input('Signal', Kalman)  # Метод изменения окраски линии
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
IndBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
dPriceShift = 0.0
Sqrt100 = 0.0
K100 = 0.0
min_rates_total = 0

def OnInit():
    global K100, Sqrt100, dPriceShift, min_rates_total
    min_rates_total = 2
    Sqrt100 = MathSqrt(K / 100)
    K100 = K / 100.0
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 31)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = Box("")
    StringConcatenate(shortname, 'KalmanFilter(', DoubleToString(K, 2), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Velocity_
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    Velocity = 0.0
    Distance = 0.0
    Error = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
        IndBuffer[first - 1] = PriceSeries(IPC, first - 1, open, low, high, close)
        _s_OnCalculate_Velocity_ = 0.0
    else:
        first = prev_calculated - 1
    Velocity = _s_OnCalculate_Velocity_
    bar = first
    for bar in range(bar, rates_total):
        if rates_total != prev_calculated and bar == (rates_total - 1):
            _s_OnCalculate_Velocity_ = Velocity
        Distance = PriceSeries(IPC, bar, open, low, high, close) - IndBuffer[bar - 1]
        Error = IndBuffer[bar - 1] + (Distance * Sqrt100)
        Velocity += Distance * K100
        IndBuffer[bar] = Error + Velocity + dPriceShift
        if Signal == Trend:
            if IndBuffer[bar - 1] > IndBuffer[bar]:
                ColorBuffer[bar] = 0.0
            else:
                ColorBuffer[bar] = 1.0
        else:
            if Velocity > 0:
                ColorBuffer[bar] = 1.0
            else:
                ColorBuffer[bar] = 0.0
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
    else:
        return Close[bar]

# ---- static local variables
_s_OnCalculate_Velocity_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Kalmanfilter(_MQL5Indicator):
    name = 'kalmanfilter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'K': 1.0,  # Коэффициент сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=7),  # Ценовая константа
        'Signal': _Choice({0: 'по тренду', 1: 'по Кальману'}, default=1),  # Метод изменения окраски линии
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
    }

