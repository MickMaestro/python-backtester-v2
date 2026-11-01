"""Ozymandias_StDev — converted from MQL5: MQL5 Indicators/Ozymandias_StDev_HTF/Ozymandias_StDev.mq5

Copyright: Copyright © 2014, GoldnMoney; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, GoldnMoney', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 8, 2: 5, 3: 5}, 'colors': {1: [8421504, 16748574, 42495], 2: [255], 3: [10156544]}, 'widths': {1: 3, 2: 3, 3: 3}, 'styles': {1: 0}, 'labels': {1: 'Ozymandias', 2: 'Dn_Signal', 3: 'Up_Signal'}, 'levels': [], 'description': [], 'name': 'Ozymandias_StDev', 'source': 'MQL5 Indicators/Ozymandias_StDev_HTF/Ozymandias_StDev.mq5', 'folder': 'Ozymandias_StDev_HTF', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'dK', 'py': 'dK', 'param': 'dK', 'type': 'double', 'default': 2.0, 'label': 'коэффициент для квадратичного фильтра', 'sinput': False}, {'mql': 'std_period', 'py': 'std_period', 'param': 'std_period', 'type': 'uint', 'default': 9, 'label': 'период квадратичного фильтра', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 2)
MAType = _input('MAType', MODE_SMA)
dK = _input('dK', 2.0)  # коэффициент для квадратичного фильтра
std_period = _input('std_period', 9)  # период квадратичного фильтра
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
OzimBuffer = Arr(0, 0.0)
ColorOzimBuffer = Arr(0, 0.0)
BearsBuffer = Arr(0, 0.0)
BullsBuffer = Arr(0, 0.0)
Count = Arr(0, 0)
Smooth = Arr(0, 0.0)
dOzim = Arr(0, 0.0)
min_rates_1 = 0
min_rates_total = 0
HMA_Handle = 0
LMA_Handle = 0

def Recount_ArrayZeroPos(CoArr, Size):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def OnInit():
    global HMA_Handle, LMA_Handle, min_rates_1, min_rates_total
    min_rates_1 = _int(Length)
    min_rates_total = min_rates_1 + 1 + _int(std_period)
    ATR_Period = 100
    ArrayResize(dOzim, std_period)
    HMA_Handle = iMA(None, 0, Length, 0, MAType, PRICE_HIGH)
    if HMA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    LMA_Handle = iMA(None, 0, Length, 0, MAType, PRICE_LOW)
    if LMA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    SetIndexBuffer(0, OzimBuffer, INDICATOR_DATA)
    ArraySetAsSeries(OzimBuffer, True)
    SetIndexBuffer(1, ColorOzimBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorOzimBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(2, BearsBuffer, INDICATOR_DATA)
    ArraySetAsSeries(BearsBuffer, True)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 119)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(3, BullsBuffer, INDICATOR_DATA)
    ArraySetAsSeries(BullsBuffer, True)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 119)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    shortname = 'Ozymandias'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_maxl1, _s_OnCalculate_minh1, _s_OnCalculate_nexttrend1, _s_OnCalculate_trend1
    if (BarsCalculated(HMA_Handle) < rates_total or BarsCalculated(LMA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    trend0 = 0
    nexttrend0 = 0
    SMAdif = 0.0
    Sum = 0.0
    StDev = 0.0
    dstd = 0.0
    BEARS = 0.0
    BULLS = 0.0
    Filter = 0.0
    hh = 0.0
    ll = 0.0
    maxl0 = 0.0
    minh0 = 0.0
    lma = 0.0
    hma = 0.0
    HMA = Arr(0, 0.0)
    LMA = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_trend1 = 0
        _s_OnCalculate_nexttrend1 = 0
        _s_OnCalculate_maxl1 = 0.0
        _s_OnCalculate_minh1 = 9999999.0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(HMA_Handle, 0, 0, to_copy, HMA) <= 0:
        return 0
    if CopyBuffer(LMA_Handle, 0, 0, to_copy, LMA) <= 0:
        return 0
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(HMA, True)
    ArraySetAsSeries(LMA, True)
    nexttrend0 = _s_OnCalculate_nexttrend1
    maxl0 = _s_OnCalculate_maxl1
    minh0 = _s_OnCalculate_minh1
    for bar in range(limit, 0 - 1, -1):
        hh = high[ArrayMaximum(high, bar, Length)]
        ll = low[ArrayMinimum(low, bar, Length)]
        lma = LMA[bar]
        hma = HMA[bar]
        trend0 = _s_OnCalculate_trend1
        if nexttrend0 == 1:
            maxl0 = MathMax(ll, maxl0)
            if hma < maxl0 and close[bar] < low[bar + 1]:
                trend0 = 1
                nexttrend0 = 0
                minh0 = hh
        if nexttrend0 == 0:
            minh0 = MathMin(hh, minh0)
            if lma > minh0 and close[bar] > high[bar + 1]:
                trend0 = 0
                nexttrend0 = 1
                maxl0 = ll
        if trend0 == 0:
            if _s_OnCalculate_trend1 != 0.0:
                OzimBuffer[bar] = OzimBuffer[bar + 1]
                ColorOzimBuffer[bar] = 1.0
            else:
                OzimBuffer[bar] = MathMax(maxl0, OzimBuffer[bar + 1])
                ColorOzimBuffer[bar] = 1.0
        else:
            if _s_OnCalculate_trend1 != 1:
                OzimBuffer[bar] = OzimBuffer[bar + 1]
                ColorOzimBuffer[bar] = 0.0
            else:
                OzimBuffer[bar] = MathMin(minh0, OzimBuffer[bar + 1])
                ColorOzimBuffer[bar] = 0.0
        if bar:
            _s_OnCalculate_nexttrend1 = nexttrend0
            _s_OnCalculate_trend1 = trend0
            _s_OnCalculate_maxl1 = maxl0
            _s_OnCalculate_minh1 = minh0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    for bar in range(limit, 0 - 1, -1):
        ColorOzimBuffer[bar] = 0.0
        if OzimBuffer[bar + 1] < OzimBuffer[bar]:
            ColorOzimBuffer[bar] = 1.0
        if OzimBuffer[bar + 1] > OzimBuffer[bar]:
            ColorOzimBuffer[bar] = 2.0
        if OzimBuffer[bar + 1] == OzimBuffer[bar]:
            ColorOzimBuffer[bar] = ColorOzimBuffer[bar + 1]
    for bar in range(limit, 0 - 1, -1):
        for iii in range(0, _int(std_period)):
            dOzim[iii] = OzimBuffer[bar + iii] - OzimBuffer[bar + iii + 1]
        Sum = 0.0
        for iii in range(0, _int(std_period)):
            Sum += dOzim[iii]
        SMAdif = Sum / std_period
        Sum = 0.0
        for iii in range(0, _int(std_period)):
            Sum += MathPow(dOzim[iii] - SMAdif, 2)
        StDev = MathSqrt(Sum / std_period)
        dstd = NormalizeDouble(dOzim[0], Digits() + 2)
        Filter = NormalizeDouble(dK * StDev, Digits() + 2)
        BEARS = 0.0
        BULLS = 0.0
        if dstd < (-Filter):
            BEARS = OzimBuffer[bar]
        if dstd > Filter:
            BULLS = OzimBuffer[bar]
        BullsBuffer[bar] = BULLS
        BearsBuffer[bar] = BEARS
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1
_s_OnCalculate_trend1 = 0
_s_OnCalculate_nexttrend1 = 0
_s_OnCalculate_maxl1 = 0.0
_s_OnCalculate_minh1 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class OzymandiasStDev(_MQL5Indicator):
    name = 'Ozymandias_StDev'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Length': 2,
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'dK': 2.0,  # коэффициент для квадратичного фильтра
        'std_period': 9,  # период квадратичного фильтра
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

