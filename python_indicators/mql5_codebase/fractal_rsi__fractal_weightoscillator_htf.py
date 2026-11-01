"""Fractal_RSI — converted from MQL5: MQL5 Indicators/Fractal_WeightOscillator_HTF/Fractal_RSI.mq5

Фрактальный RSI
Copyright: Copyright © 2008, jppoton@yahoo.com; Link: http://fractalfinance.blogspot.com/; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, jppoton@yahoo.com', 'link': 'http://fractalfinance.blogspot.com/', 'version': '1.01', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [13458026]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Fractal_RSI'}, 'levels': [70.0, 30.0], 'description': ['Фрактальный RSI'], 'name': 'Fractal_RSI', 'source': 'MQL5 Indicators/Fractal_WeightOscillator_HTF/Fractal_RSI.mq5', 'folder': 'Fractal_WeightOscillator_HTF', 'inputs': [{'mql': 'e_period', 'py': 'e_period', 'param': 'e_period', 'type': 'uint', 'default': 30, 'label': 'глубина  усреднения', 'sinput': False}, {'mql': 'normal_speed', 'py': 'normal_speed', 'param': 'normal_speed', 'type': 'uint', 'default': 30, 'label': '', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_APPLIED_PRICE_
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
_enum('ENUM_APPLIED_PRICE_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
e_period = _input('e_period', 30)  # глубина  усреднения
normal_speed = _input('normal_speed', 30)
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
ExtLineBuffer0 = Arr(0, 0.0)
ExtLineBuffer1 = Arr(0, 0.0)
LOG_2 = 0.0
min_rates_total = 0
g_period_minus_1 = 0

def OnInit():
    global LOG_2, g_period_minus_1, min_rates_total
    min_rates_total = _int(MathMax(e_period, normal_speed))
    g_period_minus_1 = _int(e_period - 1)
    LOG_2 = MathLog(2.0)
    SetIndexBuffer(0, ExtLineBuffer0, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    SetIndexBuffer(1, ExtLineBuffer1, INDICATOR_CALCULATIONS)
    shortname = Box('')
    StringConcatenate(shortname, 'Fractal_RSI(', e_period, ', ', normal_speed, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        ExtLineBuffer1[bar] = PriceSeries(IPC, bar, open, low, high, close)
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    FRACTAL_RSI(first, rates_total)
    return rates_total

def FRACTAL_RSI(lastBar, Rates_Total):
    diff = 0.0
    priorDiff = 0.0
    length = 0.0
    priceMax = 0.0
    priceMin = 0.0
    fdi = 0.0
    trail_dim = 0.0
    beta = 0.0
    hurst = 0.0
    speed = 0
    for index in range(lastBar, Rates_Total):
        priceMax = _highest(e_period, index, ExtLineBuffer1)
        priceMin = _lowest(e_period, index, ExtLineBuffer1)
        length = 0.0
        priorDiff = 0.0
        for kkk in range(0, g_period_minus_1 + 1):
            if (priceMax - priceMin) > 0.0:
                diff = _fdiv(ExtLineBuffer1[index - kkk] - priceMin, priceMax - priceMin)
                if kkk > 0:
                    length += MathSqrt(MathPow(diff - priorDiff, 2.0) + _fdiv(1.0, MathPow(e_period, 2.0)))
                priorDiff = diff
        if length > 0.0:
            fdi = 1.0 + _fdiv(MathLog(length) + LOG_2, MathLog(2 * g_period_minus_1))
        else:
            fdi = 0.0
        hurst = 2 - fdi
        trail_dim = _fdiv(1, hurst)
        beta = trail_dim / 2
        speed = _int(MathRound(normal_speed * beta))
        ExtLineBuffer0[index] = GetRSI(speed, index, ExtLineBuffer1)

def _highest(n, index, inputData):
    highest = 0.0
    for i in range(index - n + 1, index + 1):
        if inputData[i] > highest:
            highest = inputData[i]
    return highest

def _lowest(n, index, inputData):
    lowest = 9999999999.0
    for i in range(index - n + 1, index + 1):
        if inputData[i] < lowest:
            lowest = inputData[i]
    return lowest

def GetRSI(period, index, InputData):
    if index < period:
        return EMPTY_VALUE
    RSI = 50.0
    SumP = 0.0
    SumN = 0.0
    for iii in range(0, period):
        diff = InputData[index - iii] - InputData[index - iii - 1]
        SumP += (diff if (diff > 0) else 0)
        SumN += ((-diff) if (diff < 0) else 0)
    Pos = _fdiv(SumP, period)
    Neg = _fdiv(SumN, period)
    if Neg:
        RSI = 100.0 - _fdiv(100.0, 1.0 + _fdiv(Pos, Neg))
    else:
        if Pos:
            RSI = 100.0
        else:
            RSI = 50.0
    return RSI

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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FractalRSI(_MQL5Indicator):
    name = 'Fractal_RSI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'e_period': 30,  # глубина  усреднения
        'normal_speed': 30,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

