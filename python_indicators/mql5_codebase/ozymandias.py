"""ozymandias — converted from MQL5: MQL5 Indicators/Ozymandias/ozymandias.mq5

Copyright: Copyright © 2014, GoldnMoney; Link: http://www.mql5.com; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, GoldnMoney', 'link': 'http://www.mql5.com', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 8, 2: 1, 3: 1}, 'colors': {1: [9639167, 16748574], 2: [9408444], 3: [9408444]}, 'widths': {1: 3, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Ozymandias', 2: 'Upper Ozymandias', 3: 'Lower Ozymandias'}, 'levels': [], 'description': [], 'name': 'ozymandias', 'source': 'MQL5 Indicators/Ozymandias/ozymandias.mq5', 'folder': 'Ozymandias', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 2)
MAType = _input('MAType', MODE_SMA)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
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
    SetIndexBuffer(2, UpBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpBuffer, True)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(3, DnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    shortname = 'Ozymandias'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_maxl1, _s_OnCalculate_minh1, _s_OnCalculate_nexttrend1, _s_OnCalculate_trend1
    if ((BarsCalculated(ATR_Handle) < rates_total or BarsCalculated(HMA_Handle) < rates_total) or BarsCalculated(LMA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    trend0 = 0
    nexttrend0 = 0
    hh = 0.0
    ll = 0.0
    maxl0 = 0.0
    minh0 = 0.0
    lma = 0.0
    hma = 0.0
    atr = 0.0
    ATR = Arr(0, 0.0)
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
    nexttrend0 = _s_OnCalculate_nexttrend1
    maxl0 = _s_OnCalculate_maxl1
    minh0 = _s_OnCalculate_minh1
    for bar in range(limit, 0 - 1, -1):
        hh = high[ArrayMaximum(high, bar, Length)]
        ll = low[ArrayMinimum(low, bar, Length)]
        lma = LMA[bar]
        hma = HMA[bar]
        atr = ATR[bar] / 2
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
                IndBuffer[bar] = IndBuffer[bar + 1]
                ColorIndBuffer[bar] = 1.0
            else:
                IndBuffer[bar] = MathMax(maxl0, IndBuffer[bar + 1])
                ColorIndBuffer[bar] = 1.0
            UpBuffer[bar] = IndBuffer[bar] + atr
            DnBuffer[bar] = IndBuffer[bar] - atr
        else:
            if _s_OnCalculate_trend1 != 1:
                IndBuffer[bar] = IndBuffer[bar + 1]
                ColorIndBuffer[bar] = 0.0
            else:
                IndBuffer[bar] = MathMin(minh0, IndBuffer[bar + 1])
                ColorIndBuffer[bar] = 0.0
            UpBuffer[bar] = IndBuffer[bar] + atr
            DnBuffer[bar] = IndBuffer[bar] - atr
        if bar:
            _s_OnCalculate_nexttrend1 = nexttrend0
            _s_OnCalculate_trend1 = trend0
            _s_OnCalculate_maxl1 = maxl0
            _s_OnCalculate_minh1 = minh0
    return rates_total

# ---- static local variables
_s_OnCalculate_trend1 = 0
_s_OnCalculate_nexttrend1 = 0
_s_OnCalculate_maxl1 = 0.0
_s_OnCalculate_minh1 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ozymandias(_MQL5Indicator):
    name = 'ozymandias'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 2,
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

