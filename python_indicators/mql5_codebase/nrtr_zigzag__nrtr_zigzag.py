"""NRTR_ZigZag — converted from MQL5: MQL5 Indicators/NRTR_ZigZag/NRTR_ZigZag.mq5

Copyright: Copyright © 2005, Ramdass; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Ramdass', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 1}, 'types': {1: 6}, 'colors': {1: [14053594]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'NRTR_ZigZag'}, 'levels': [], 'description': [], 'name': 'NRTR_ZigZag', 'source': 'MQL5 Indicators/NRTR_ZigZag/NRTR_ZigZag.mq5', 'folder': 'NRTR_ZigZag', 'inputs': [{'mql': 'iPeriod', 'py': 'iPeriod', 'param': 'iPeriod', 'type': 'uint', 'default': 10, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'iDig', 'py': 'iDig', 'param': 'iDig', 'type': 'int', 'default': 0, 'label': 'Разряд', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
iPeriod = _input('iPeriod', 10)  # Период индикатора
iDig = _input('iDig', 0)  # Разряд
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
TrendUp = Arr(0, 0.0)
TrendDown = Arr(0, 0.0)
SignUp = Arr(0, 0.0)
SignDown = Arr(0, 0.0)
HighestBuffer = Arr(0, 0.0)
LowestBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(iPeriod)
    shortname = Box("")
    StringConcatenate(shortname, 'NRTR_ZigZag(', _str(iPeriod), ', ', _str(Shift), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(0, LowestBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, HighestBuffer, INDICATOR_DATA)
    ArraySetAsSeries(LowestBuffer, True)
    ArraySetAsSeries(HighestBuffer, True)
    SetIndexBuffer(2, TrendUp, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(TrendUp, True)
    SetIndexBuffer(3, TrendDown, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(TrendDown, True)
    SetIndexBuffer(4, SignUp, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(SignUp, True)
    SetIndexBuffer(5, SignDown, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(SignDown, True)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_lasthigh, _s_OnCalculate_lasthighpos, _s_OnCalculate_lastlow, _s_OnCalculate_lastlowpos, _s_OnCalculate_price_prev, _s_OnCalculate_trend_prev, _s_OnCalculate_value_prev
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
        _s_OnCalculate_lastlow = 999999999.99999
        _s_OnCalculate_lasthigh = 0.0
        _s_OnCalculate_lasthighpos = 0
        _s_OnCalculate_lastlowpos = _s_OnCalculate_lasthighpos
    else:
        limit = rates_total - prev_calculated
    trend = _s_OnCalculate_trend_prev
    price = _s_OnCalculate_price_prev
    value = _s_OnCalculate_value_prev
    _s_OnCalculate_lastlowpos += limit
    _s_OnCalculate_lasthighpos += limit
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        TrendUp[bar] = 0.0
        TrendDown[bar] = 0.0
        SignUp[bar] = 0.0
        SignDown[bar] = 0.0
        HighestBuffer[bar] = 0.0
        LowestBuffer[bar] = 0.0
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
            SignUp[bar] = value
        if _s_OnCalculate_trend_prev > 0 and trend < 0:
            SignDown[bar] = value
        if trend > 0:
            if TrendUp[bar + 1]:
                if high[bar] > _s_OnCalculate_lasthigh:
                    _s_OnCalculate_lasthigh = high[bar]
                    HighestBuffer[bar] = _s_OnCalculate_lasthigh
                    HighestBuffer[_s_OnCalculate_lasthighpos] = 0.0
                    _s_OnCalculate_lasthighpos = bar
            else:
                _s_OnCalculate_lasthigh = high[bar]
                HighestBuffer[bar] = _s_OnCalculate_lasthigh
                _s_OnCalculate_lasthighpos = bar
        if trend < 0:
            if TrendDown[bar + 1]:
                if low[bar] < _s_OnCalculate_lastlow:
                    _s_OnCalculate_lastlow = low[bar]
                    LowestBuffer[bar] = _s_OnCalculate_lastlow
                    LowestBuffer[_s_OnCalculate_lastlowpos] = 0.0
                    _s_OnCalculate_lastlowpos = bar
            else:
                _s_OnCalculate_lastlow = low[bar]
                LowestBuffer[bar] = _s_OnCalculate_lastlow
                _s_OnCalculate_lastlowpos = bar
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
_s_OnCalculate_lastlow = 0.0
_s_OnCalculate_lasthigh = 0.0
_s_OnCalculate_trend_prev = 0
_s_OnCalculate_lastlowpos = 0
_s_OnCalculate_lasthighpos = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class NRTRZigZag(_MQL5Indicator):
    name = 'NRTR_ZigZag'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'iPeriod': 10,  # Период индикатора
        'iDig': 0,  # Разряд
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

