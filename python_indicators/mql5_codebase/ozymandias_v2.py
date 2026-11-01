"""ozymandias_v2 — converted from MQL5: MQL5 Indicators/Ozymandias_v2/ozymandias_v2.mq5

Copyright: Copyright © 2014, GoldnMoney; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, GoldnMoney', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 8, 2: 8}, 'colors': {1: [42495, 65407], 2: [42495, 3329330]}, 'widths': {1: 3, 2: 1}, 'styles': {1: 0, 2: 3}, 'labels': {1: 'Line', 2: 'Signal'}, 'levels': [], 'description': [], 'name': 'ozymandias_v2', 'source': 'MQL5 Indicators/Ozymandias_v2/ozymandias_v2.mq5', 'folder': 'Ozymandias_v2', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 2)
MAType = _input('MAType', MODE_SMA)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
SigBuffer = Arr(0, 0.0)
ColorSigBuffer = Arr(0, 0.0)
min_rates_total = 0
ATR_Handle = 0
HMA_Handle = 0
LMA_Handle = 0

def OnInit():
    global ATR_Handle, HMA_Handle, LMA_Handle, min_rates_total
    min_rates_total = _int(Length)
    ATR_Period = 100
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    HMA_Handle = iMA(None, 0, Length, 0, MAType, PRICE_HIGH)
    if HMA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    LMA_Handle = iMA(None, 0, Length, 0, MAType, PRICE_LOW)
    if LMA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(2, SigBuffer, INDICATOR_DATA)
    ArraySetAsSeries(SigBuffer, True)
    SetIndexBuffer(3, ColorSigBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorSigBuffer, True)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    shortname = 'Ozymandias_v2'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_map1, _s_OnCalculate_maxlo1, _s_OnCalculate_minhi1
    if ((BarsCalculated(ATR_Handle) < rates_total or BarsCalculated(HMA_Handle) < rates_total) or BarsCalculated(LMA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    highprice = 0.0
    lowprice = 0.0
    maxlo = 0.0
    zone = 0.0
    minhi = 0.0
    map0 = 0.0
    lowma = 0.0
    highma = 0.0
    ATR = Arr(0, 0.0)
    HMA = Arr(0, 0.0)
    LMA = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_map1 = 0.0
        _s_OnCalculate_minhi1 = 99999999.0
        _s_OnCalculate_maxlo1 = 1.0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    if CopyBuffer(HMA_Handle, 0, 0, to_copy, HMA) <= 0:
        return 0
    if CopyBuffer(LMA_Handle, 0, 0, to_copy, LMA) <= 0:
        return 0
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(HMA, True)
    ArraySetAsSeries(LMA, True)
    maxlo = _s_OnCalculate_maxlo1
    minhi = _s_OnCalculate_minhi1
    for bar in range(limit, 0 - 1, -1):
        highprice = high[ArrayMaximum(high, bar, Length)]
        lowprice = low[ArrayMinimum(low, bar, Length)]
        lowma = LMA[bar]
        highma = HMA[bar]
        zone = ATR[bar] / 2
        maxlo = MathMax(lowprice, maxlo)
        minhi = MathMin(highprice, minhi)
        map0 = _s_OnCalculate_map1
        if highma < maxlo and close[bar] < low[bar + 1]:
            map0 = -1.0
            maxlo = lowprice
        if lowma > minhi and close[bar] > high[bar + 1]:
            map0 = 1.0
            minhi = highprice
        if map0 > 0 and _s_OnCalculate_map1 < 0:
            IndBuffer[bar] = IndBuffer[bar + 1]
            ColorIndBuffer[bar] = 1.0
            SigBuffer[bar] = SigBuffer[bar + 1]
            ColorSigBuffer[bar] = 1.0
        if map0 > 0 and _s_OnCalculate_map1 > 0:
            IndBuffer[bar] = MathMax(maxlo, IndBuffer[bar + 1])
            ColorIndBuffer[bar] = 1.0
            SigBuffer[bar] = IndBuffer[bar] - zone
            ColorSigBuffer[bar] = 1.0
        if map0 < 0 and _s_OnCalculate_map1 > 0:
            IndBuffer[bar] = IndBuffer[bar + 1]
            ColorIndBuffer[bar] = 0.0
            SigBuffer[bar] = SigBuffer[bar + 1]
            ColorSigBuffer[bar] = 0.0
        if map0 < 0 and _s_OnCalculate_map1 < 0:
            IndBuffer[bar] = MathMin(minhi, IndBuffer[bar + 1])
            ColorIndBuffer[bar] = 0.0
            SigBuffer[bar] = IndBuffer[bar] + zone
            ColorSigBuffer[bar] = 0.0
        if bar:
            _s_OnCalculate_map1 = map0
            _s_OnCalculate_maxlo1 = maxlo
            _s_OnCalculate_minhi1 = minhi
    return rates_total

# ---- static local variables
_s_OnCalculate_map1 = 0.0
_s_OnCalculate_maxlo1 = 0.0
_s_OnCalculate_minhi1 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class OzymandiasV2(_MQL5Indicator):
    name = 'ozymandias_v2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 2,
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

