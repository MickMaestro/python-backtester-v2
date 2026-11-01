"""NRTR_Sign — converted from MQL5: MQL5 Indicators/NRTR_Sign/NRTR_Sign.mq5

Copyright: Copyright © 2005, Ramdass; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Ramdass', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [65280], 2: [255]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Buy NRTR signal', 2: 'Sell NRTR signal'}, 'levels': [], 'description': [], 'name': 'NRTR_Sign', 'source': 'MQL5 Indicators/NRTR_Sign/NRTR_Sign.mq5', 'folder': 'NRTR_Sign', 'inputs': [{'mql': 'iPeriod', 'py': 'iPeriod', 'param': 'iPeriod', 'type': 'uint', 'default': 10, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'iDig', 'py': 'iDig', 'param': 'iDig', 'type': 'int', 'default': 0, 'label': 'Разряд', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
iPeriod = _input('iPeriod', 10)  # Период индикатора
iDig = _input('iDig', 0)  # Разряд
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
SignUp = Arr(0, 0.0)
SignDown = Arr(0, 0.0)
min_rates_total = 0
ATR_Handle = 0

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Period = 15
    min_rates_total = _int(MathMax(iPeriod, ATR_Period)) + 1
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    shortname = Box("")
    StringConcatenate(shortname, 'NRTR Sign(', _str(iPeriod), ', ', _str(Shift), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, SignUp, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(SignUp, True)
    PlotIndexSetInteger(0, PLOT_ARROW, 110)
    SetIndexBuffer(1, SignDown, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(SignDown, True)
    PlotIndexSetInteger(1, PLOT_ARROW, 110)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_price_prev, _s_OnCalculate_trend_prev, _s_OnCalculate_value_prev
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    price = 0.0
    value = 0.0
    dK = 0.0
    ATR = Arr(0, 0.0)
    to_copy = 0
    limit = 0
    bar = 0
    trend = 0
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(ATR, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_trend_prev = 0
        _s_OnCalculate_value_prev = close[limit]
        _s_OnCalculate_price_prev = _s_OnCalculate_value_prev
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    trend = _s_OnCalculate_trend_prev
    price = _s_OnCalculate_price_prev
    value = _s_OnCalculate_value_prev
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
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
        if _s_OnCalculate_trend_prev < 0 and trend > 0:
            SignUp[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if _s_OnCalculate_trend_prev > 0 and trend < 0:
            SignDown[bar] = high[bar] + ((ATR[bar] * 3) / 8)
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


class NRTRSign(_MQL5Indicator):
    name = 'NRTR_Sign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iPeriod': 10,  # Период индикатора
        'iDig': 0,  # Разряд
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

