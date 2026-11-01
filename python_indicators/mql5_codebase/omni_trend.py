"""Omni_Trend — converted from MQL5: MQL5 Indicators/Omni_Trend/Omni_Trend.mq5

Copyright: Copyright © 2005,  ; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005,  ', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [16711680], 2: [36095], 3: [16748574], 4: [55295]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Omni_Trend Up', 2: 'Omni_Trend Down', 3: 'Buy Omni_Trend signal', 4: 'Sell Omni_Trend signal'}, 'levels': [], 'description': [], 'name': 'Omni_Trend', 'source': 'MQL5 Indicators/Omni_Trend/Omni_Trend.mq5', 'folder': 'Omni_Trend', 'inputs': [{'mql': 'MA_Length', 'py': 'MA_Length', 'param': 'MA_Length', 'type': 'uint', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'MA_Type', 'py': 'MA_Type', 'param': 'MA_Type', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MA_Price', 'py': 'MA_Price', 'param': 'MA_Price', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'ATR_Length', 'py': 'ATR_Length', 'param': 'ATR_Length', 'type': 'int', 'default': 11, 'label': "ATR's Period", 'sinput': False}, {'mql': 'Kv', 'py': 'Kv', 'param': 'Kv', 'type': 'double', 'default': 1.3, 'label': "Volatility's Factor or Multiplier", 'sinput': False}, {'mql': 'MoneyRisk', 'py': 'MoneyRisk', 'param': 'MoneyRisk', 'type': 'double', 'default': 0.15, 'label': 'Offset Factor', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MA_Length = _input('MA_Length', 13)
MA_Type = _input('MA_Type', MODE_EMA)
MA_Price = _input('MA_Price', PRICE_CLOSE)
ATR_Length = _input('ATR_Length', 11)  # ATR's Period
Kv = _input('Kv', 1.3)  # Volatility's Factor or Multiplier
MoneyRisk = _input('MoneyRisk', 0.15)  # Offset Factor
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
TrendUp = Arr(0, 0.0)
TrendDown = Arr(0, 0.0)
SignUp = Arr(0, 0.0)
SignDown = Arr(0, 0.0)
min_rates_total = 0
MA_Handle = 0
ATR_Handle = 0

def OnInit():
    global ATR_Handle, MA_Handle, min_rates_total
    min_rates_total = _int(MathMax(ATR_Length, MA_Length))
    MA_Handle = iMA(None, 0, MA_Length, 0, MA_Type, MA_Price)
    if MA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    ATR_Handle = iATR(None, 0, ATR_Length)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    shortname = Box("")
    StringConcatenate(shortname, 'Omni_Trend(', _str(MA_Length), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, TrendUp, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(TrendUp, True)
    SetIndexBuffer(1, TrendDown, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(TrendDown, True)
    SetIndexBuffer(2, SignUp, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SignUp, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(2, PLOT_ARROW, 108)
    SetIndexBuffer(3, SignDown, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SignDown, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(3, PLOT_ARROW, 108)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_smax_prev, _s_OnCalculate_smin_prev, _s_OnCalculate_trend_prev
    if (BarsCalculated(MA_Handle) < rates_total or BarsCalculated(ATR_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    MA = Arr(0, 0.0)
    ATR = Arr(0, 0.0)
    smin = 0.0
    smax = 0.0
    limit = 0
    to_copy = 0
    bar = 0
    trend = 0
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(MA, True)
    ArraySetAsSeries(ATR, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_trend_prev = 0
        _s_OnCalculate_smax_prev = close[limit]
        _s_OnCalculate_smin_prev = _s_OnCalculate_smax_prev
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MA) <= 0:
        return 0
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        TrendUp[bar] = 0.0
        TrendDown[bar] = 0.0
        SignUp[bar] = 0.0
        SignDown[bar] = 0.0
        bprice = MA[bar]
        sprice = MA[bar]
        smax = bprice + (Kv * ATR[bar])
        smin = sprice - (Kv * ATR[bar])
        trend = _s_OnCalculate_trend_prev
        if high[bar] > _s_OnCalculate_smax_prev:
            trend = 1
        if low[bar] < _s_OnCalculate_smin_prev:
            trend = -1
        if trend > 0:
            if smin < _s_OnCalculate_smin_prev:
                smin = _s_OnCalculate_smin_prev
            TrendUp[bar] = smin - ((MoneyRisk - 1) * ATR[bar])
            if TrendUp[bar] < TrendUp[bar + 1] and TrendUp[bar + 1]:
                TrendUp[bar] = TrendUp[bar + 1]
        if trend < 0:
            if smax > _s_OnCalculate_smax_prev:
                smax = _s_OnCalculate_smax_prev
            TrendDown[bar] = smax + ((MoneyRisk - 1) * ATR[bar])
            if TrendDown[bar] > TrendDown[bar + 1] and TrendDown[bar + 1]:
                TrendDown[bar] = TrendDown[bar + 1]
        if _s_OnCalculate_trend_prev <= 0 and trend > 0:
            SignUp[bar] = TrendUp[bar]
        if _s_OnCalculate_trend_prev >= 0 and trend < 0:
            SignDown[bar] = TrendDown[bar]
        if bar:
            _s_OnCalculate_trend_prev = trend
            _s_OnCalculate_smin_prev = smin
            _s_OnCalculate_smax_prev = smax
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_smin_prev = 0.0
_s_OnCalculate_smax_prev = 0.0
_s_OnCalculate_trend_prev = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class OmniTrend(_MQL5Indicator):
    name = 'Omni_Trend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Length': 13,
        'MA_Type': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'MA_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'ATR_Length': 11,  # ATR's Period
        'Kv': 1.3,  # Volatility's Factor or Multiplier
        'MoneyRisk': 0.15,  # Offset Factor
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

