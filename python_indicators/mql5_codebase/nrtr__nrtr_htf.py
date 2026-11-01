"""NRTR — converted from MQL5: MQL5 Indicators/NRTR_HTF/NRTR.mq5

Copyright: Copyright © 2005, Ramdass; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Ramdass', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [65280], 2: [255], 3: [13422920], 4: [36095]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'NRTR Up', 2: 'NRTR Down', 3: 'Buy NRTR signal', 4: 'Sell NRTR signal'}, 'levels': [], 'description': [], 'name': 'NRTR', 'source': 'MQL5 Indicators/NRTR_HTF/NRTR.mq5', 'folder': 'NRTR_HTF', 'inputs': [{'mql': 'iPeriod', 'py': 'iPeriod', 'param': 'iPeriod', 'type': 'uint', 'default': 10, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'iDig', 'py': 'iDig', 'param': 'iDig', 'type': 'int', 'default': 0, 'label': 'Разряд', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
iPeriod = _input('iPeriod', 10)  # Период индикатора
iDig = _input('iDig', 0)  # Разряд
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
TrendUp = Arr(0, 0.0)
TrendDown = Arr(0, 0.0)
SignUp = Arr(0, 0.0)
SignDown = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(iPeriod)
    shortname = Box("")
    StringConcatenate(shortname, 'NRTR(', _str(iPeriod), ', ', _str(Shift), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, TrendUp, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(TrendUp, True)
    SetIndexBuffer(1, TrendDown, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(TrendDown, True)
    SetIndexBuffer(2, SignUp, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SignUp, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(2, PLOT_ARROW, 108)
    SetIndexBuffer(3, SignDown, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SignDown, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(3, PLOT_ARROW, 108)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_price_prev, _s_OnCalculate_trend_prev, _s_OnCalculate_value_prev
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    value = 0.0
    dK = 0.0
    limit = 0
    bar = 0
    trend = 0
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_trend_prev = 0
        _s_OnCalculate_value_prev = close[limit]
        _s_OnCalculate_price_prev = _s_OnCalculate_value_prev
    else:
        limit = rates_total - prev_calculated
    trend = _s_OnCalculate_trend_prev
    price = _s_OnCalculate_price_prev
    value = _s_OnCalculate_value_prev
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        TrendUp[bar] = 0.0
        TrendDown[bar] = 0.0
        SignUp[bar] = 0.0
        SignDown[bar] = 0.0
        AvgRange = 0.0
        for iii in range(0, _int(iPeriod)):
            AvgRange += MathAbs(high[bar + iii] - low[bar + iii])
        dK = _fdiv(AvgRange / iPeriod, MathPow(10, SymbolInfoInteger('EURUSD', SYMBOL_DIGITS) - Digits() - iDig))
        if trend >= 0:
            price = MathMax(price, close[bar])
            value = MathMax(value, price * (1.0 - dK))
            if close[bar] < value:
                price = close[bar]
                value = price * (1.0 + dK)
                trend = -1
        elif trend <= 0:
            price = MathMin(price, close[bar])
            value = MathMin(value, price * (1.0 + dK))
            if close[bar] > value:
                price = close[bar]
                value = price * (1.0 - dK)
                trend = 1
        if trend > 0:
            TrendUp[bar] = value
        if trend < 0:
            TrendDown[bar] = value
        if _s_OnCalculate_trend_prev < 0 and trend > 0:
            SignUp[bar] = TrendUp[bar]
        if _s_OnCalculate_trend_prev > 0 and trend < 0:
            SignDown[bar] = TrendDown[bar]
        if bar:
            _s_OnCalculate_trend_prev = trend
            _s_OnCalculate_price_prev = price
            _s_OnCalculate_value_prev = value
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_price_prev = 0.0
_s_OnCalculate_value_prev = 0.0
_s_OnCalculate_trend_prev = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NRTR(_MQL5Indicator):
    name = 'NRTR'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iPeriod': 10,  # Период индикатора
        'iDig': 0,  # Разряд
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

