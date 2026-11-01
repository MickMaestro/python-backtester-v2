"""Squeeze_RA_V1 — converted from MQL5: MQL5 Indicators/Squeeze_RA_V1/Squeeze_RA_V1.mq5

Copyright: Copyright © 2015, Ravish Anandaram; Link: aravishstocks@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2015, Ravish Anandaram', 'link': 'aravishstocks@gmail.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 6}, 'types': {1: 3, 2: 3, 3: 3, 4: 3, 5: 5, 6: 5}, 'colors': {1: [13434880], 2: [4678655], 3: [16748574], 4: [42495], 5: [65280], 6: [16711935]}, 'widths': {1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'SqzFiredLong', 2: 'SqzFiredShort', 3: 'SqzFiredLong_Weak', 4: 'SqzFiredShort_Weak', 5: 'Squeeze_Off', 6: 'Squeeze_On'}, 'levels': [], 'description': [], 'name': 'Squeeze_RA_V1', 'source': 'MQL5 Indicators/Squeeze_RA_V1/Squeeze_RA_V1.mq5', 'folder': 'Squeeze_RA_V1', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Bollinger_Period = 20
Bollinger_Deviation = 2.0
Keltner_Period = 20
Keltner_ATR = 1.5
Bollinger_MaMode = MODE_SMA
Keltner_MaMode = MODE_SMA
BarsToGoBack = 1000
LSmoothX = 1.0
LSmoothY = 1.0
LSmoothFactor_1 = 3.0
LSmoothFactor_2 = 3.0
Shift = 0  # сдвиг индикатора по горизонтали в барах
Squeeze_Off = Arr(0, 0.0)  # Green Dots on the zero line
Squeeze_On = Arr(0, 0.0)  # Red Dots on the zero line
SqzFiredLong_Strong = Arr(0, 0.0)  # Rising Positive Histograms
SqzFiredShort_Strong = Arr(0, 0.0)  # Falling Negative Histograms
SqzFiredLong_Weak = Arr(0, 0.0)  # Falling Positive Histograms
SqzFiredShort_Weak = Arr(0, 0.0)  # Rising Negative Histograms
min_rates_total = 0
Smooth_Factor = 0
ATR_Handle = 0
Std_Handle = 0
Ma1_Handle = 0
Ma2_Handle = 0
Ma3_Handle = 0
Ma4_Handle = 0

def IndInit(number, Array, shift, draw_begin, empty_value):
    SetIndexBuffer(number, Array, INDICATOR_DATA)
    PlotIndexSetInteger(number, PLOT_SHIFT, shift)
    PlotIndexSetInteger(number, PLOT_DRAW_BEGIN, draw_begin)
    PlotIndexSetDouble(number, PLOT_EMPTY_VALUE, empty_value)
    ArraySetAsSeries(Array, True)

def GetSmoothFactor(period):
    _sw1 = period
    if _sw1 == PERIOD_M1:
        return 300
    elif _sw1 == PERIOD_M2:
        return 230
    elif _sw1 == PERIOD_M4:
        return 150
    elif _sw1 == PERIOD_M5:
        return 100
    elif _sw1 == PERIOD_M6:
        return 80
    elif _sw1 == PERIOD_M10:
        return 65
    elif _sw1 == PERIOD_M15:
        return 50
    elif _sw1 == PERIOD_M20:
        return 50
    elif _sw1 == PERIOD_M30:
        return 50
    elif _sw1 == PERIOD_H1:
        return 30
    elif _sw1 == PERIOD_H2:
        return 20
    elif _sw1 == PERIOD_H3:
        return 12
    elif _sw1 == PERIOD_H4:
        return 8
    elif _sw1 == PERIOD_H6:
        return 7
    elif _sw1 == PERIOD_H8:
        return 6
    elif _sw1 == PERIOD_H12:
        return 5
    elif _sw1 == PERIOD_D1:
        return 6
    elif _sw1 == PERIOD_W1:
        return 4
    elif _sw1 == PERIOD_MN1:
        return 4
    return 300

def OnInit():
    global ATR_Handle, Ma1_Handle, Ma2_Handle, Ma3_Handle, Ma4_Handle, Smooth_Factor, Std_Handle, min_rates_total
    ATR_Handle = iATR(None, 0, Keltner_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    Std_Handle = iStdDev(None, 0, Bollinger_Period, 0, Bollinger_MaMode, PRICE_CLOSE)
    if Std_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iStdDev')
        return INIT_FAILED
    Ma1_Handle = iMA(None, 0, Keltner_Period, 0, MODE_SMA, PRICE_CLOSE)
    if Ma1_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA1')
        return INIT_FAILED
    Ma2_Handle = iMA(None, 0, Keltner_Period, 0, MODE_LWMA, PRICE_CLOSE)
    if Ma2_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA2')
        return INIT_FAILED
    Ma3_Handle = iMA(None, 0, Keltner_Period, 0, Keltner_MaMode, PRICE_CLOSE)
    if Ma3_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA3')
        return INIT_FAILED
    Ma4_Handle = iMA(None, 0, Bollinger_Period, 0, Bollinger_MaMode, PRICE_CLOSE)
    if Ma4_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA4')
        return INIT_FAILED
    min_rates_total = Keltner_Period + Bollinger_Period
    Smooth_Factor = GetSmoothFactor(Period())
    IndInit(0, SqzFiredLong_Strong, Shift, min_rates_total, EMPTY_VALUE)
    IndInit(1, SqzFiredShort_Strong, Shift, min_rates_total, EMPTY_VALUE)
    IndInit(2, SqzFiredLong_Weak, Shift, min_rates_total, EMPTY_VALUE)
    IndInit(3, SqzFiredShort_Weak, Shift, min_rates_total, EMPTY_VALUE)
    IndInit(4, Squeeze_Off, Shift, min_rates_total, EMPTY_VALUE)
    IndInit(5, Squeeze_On, Shift, min_rates_total, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Squeeze_RA_V1')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (((((BarsCalculated(ATR_Handle) < rates_total or BarsCalculated(Std_Handle) < rates_total) or BarsCalculated(Ma1_Handle) < rates_total) or BarsCalculated(Ma2_Handle) < rates_total) or BarsCalculated(Ma3_Handle) < rates_total) or BarsCalculated(Ma4_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    Std = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    MA1 = Arr(0, 0.0)
    MA2 = Arr(0, 0.0)
    MA3 = Arr(0, 0.0)
    MA4 = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(Std_Handle, 0, 0, to_copy, Std) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    if CopyBuffer(Ma1_Handle, 0, 0, to_copy, MA1) <= 0:
        return 0
    if CopyBuffer(Ma2_Handle, 0, 0, to_copy, MA2) <= 0:
        return 0
    if CopyBuffer(Ma3_Handle, 0, 0, to_copy, MA3) <= 0:
        return 0
    if CopyBuffer(Ma4_Handle, 0, 0, to_copy, MA4) <= 0:
        return 0
    ArraySetAsSeries(Std, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(MA1, True)
    ArraySetAsSeries(MA2, True)
    ArraySetAsSeries(MA3, True)
    ArraySetAsSeries(MA4, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Kelt_Mid_Band = MA3[bar]
        Kelt_Upper_Band = Kelt_Mid_Band + (ATR[bar] * Keltner_ATR)
        Kelt_Lower_Band = Kelt_Mid_Band - (ATR[bar] * Keltner_ATR)
        StdDev = Std[bar]
        Ma = MA4[bar]
        Boll_Upper_Band = Ma + (StdDev * Bollinger_Deviation)
        Boll_Lower_Band = Ma - (StdDev * Bollinger_Deviation)
        LSmooth1 = 0.0
        LSmooth2 = 0.0
        LSmoothVal = 0.0
        dLSmoothVal = 0.0
        LSmooth1 = LSmoothX * MA1[bar]
        LSmooth2 = _fdiv(MA2[bar], LSmoothY)
        LSmoothVal = (LSmoothFactor_1 * LSmooth2) - (LSmoothFactor_2 * LSmooth1)
        dLSmoothVal = LSmoothVal * Smooth_Factor
        if dLSmoothVal > 0:
            if (SqzFiredLong_Strong[bar + 1] and dLSmoothVal > SqzFiredLong_Strong[bar + 1]) or (SqzFiredLong_Weak[bar + 1] and dLSmoothVal > SqzFiredLong_Weak[bar + 1]):
                SqzFiredLong_Strong[bar] = dLSmoothVal
                SqzFiredLong_Weak[bar] = 0.0
            else:
                SqzFiredLong_Weak[bar] = dLSmoothVal
                SqzFiredLong_Strong[bar] = 0.0
            SqzFiredShort_Strong[bar] = 0.0
            SqzFiredShort_Weak[bar] = 0.0
        else:
            if (SqzFiredShort_Strong[bar + 1] and dLSmoothVal < SqzFiredShort_Strong[bar + 1]) or (SqzFiredShort_Weak[bar + 1] and dLSmoothVal < SqzFiredShort_Weak[bar + 1]):
                SqzFiredShort_Strong[bar] = dLSmoothVal
                SqzFiredShort_Weak[bar] = 0.0
            else:
                SqzFiredShort_Weak[bar] = dLSmoothVal
                SqzFiredShort_Strong[bar] = 0.0
            SqzFiredLong_Strong[bar] = 0.0
            SqzFiredLong_Weak[bar] = 0.0
        if Boll_Upper_Band < Kelt_Upper_Band and Boll_Lower_Band > Kelt_Lower_Band:
            Squeeze_On[bar] = 0.0
            Squeeze_Off[bar] = EMPTY_VALUE
        else:
            Squeeze_Off[bar] = 0.0
            Squeeze_On[bar] = EMPTY_VALUE
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SqueezeRAV1(_MQL5Indicator):
    name = 'Squeeze_RA_V1'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

