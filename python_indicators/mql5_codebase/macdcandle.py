"""macdcandle — converted from MQL5: MQL5 Indicators/MACDCandle/macdcandle.mq5

MACDCandle Smoothed
Copyright: Copyright © 2013, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2013, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [9639167, 16711680, 8421376]}, 'widths': {}, 'styles': {}, 'labels': {1: 'MACDCandle Open;MACDCandle High;MACDCandle Low;MACDCandle Close'}, 'levels': [], 'description': ['MACDCandle Smoothed'], 'name': 'macdcandle', 'source': 'MQL5 Indicators/MACDCandle/macdcandle.mq5', 'folder': 'MACDCandle', 'inputs': [{'mql': 'fast_ema_period', 'py': 'fast_ema_period', 'param': 'fast_ema_period', 'type': 'uint', 'default': 12, 'label': 'Период быстрой средней', 'sinput': False}, {'mql': 'slow_ema_period', 'py': 'slow_ema_period', 'param': 'slow_ema_period', 'type': 'uint', 'default': 26, 'label': 'Период медленной средней', 'sinput': False}, {'mql': 'signal_period', 'py': 'signal_period', 'param': 'signal_period', 'type': 'uint', 'default': 9, 'label': 'Период усреднения разности', 'sinput': False}, {'mql': 'mode', 'py': 'mode', 'param': 'mode', 'type': 'int', 'default': 1, 'label': 'Источник даных для расчета', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum MODE
MODE_HISTOGRAM = 0
MODE_SIGNAL_LINE = 1
_enum('MODE', {0: 'MODE_HISTOGRAM', 1: 'MODE_SIGNAL_LINE'})

# ---- inputs and global variables
fast_ema_period = _input('fast_ema_period', 12)  # Период быстрой средней
slow_ema_period = _input('slow_ema_period', 26)  # Период медленной средней
signal_period = _input('signal_period', 9)  # Период усреднения разности
mode = _input('mode', MODE_SIGNAL_LINE)  # Источник даных для расчета
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
MACD_Handle = Arr(4, 0, dyn=False)

def OnInit():
    global min_rates_total
    min_rates_total = _int(MathMax(fast_ema_period, slow_ema_period))
    if mode == MODE_SIGNAL_LINE:
        min_rates_total += _int(signal_period)
    MACD_Handle[0] = iMACD(None, 0, fast_ema_period, slow_ema_period, signal_period, PRICE_OPEN)
    if MACD_Handle[0] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMACD[' + _str(0) + ']!')
        return INIT_FAILED
    MACD_Handle[1] = iMACD(None, 0, fast_ema_period, slow_ema_period, signal_period, PRICE_HIGH)
    if MACD_Handle[1] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMACD[' + _str(1) + ']!')
        return INIT_FAILED
    MACD_Handle[2] = iMACD(None, 0, fast_ema_period, slow_ema_period, signal_period, PRICE_LOW)
    if MACD_Handle[2] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMACD[' + _str(2) + ']!')
        return INIT_FAILED
    MACD_Handle[3] = iMACD(None, 0, fast_ema_period, slow_ema_period, signal_period, PRICE_CLOSE)
    if MACD_Handle[3] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMACD[' + _str(3) + ']!')
        return INIT_FAILED
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    short_name = 'MACDCandl'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (((BarsCalculated(MACD_Handle[0]) < rates_total or BarsCalculated(MACD_Handle[1]) < rates_total) or BarsCalculated(MACD_Handle[2]) < rates_total) or BarsCalculated(MACD_Handle[3]) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(MACD_Handle[0], mode, 0, to_copy, ExtOpenBuffer) <= 0:
        return 0
    if CopyBuffer(MACD_Handle[1], mode, 0, to_copy, ExtHighBuffer) <= 0:
        return 0
    if CopyBuffer(MACD_Handle[2], mode, 0, to_copy, ExtLowBuffer) <= 0:
        return 0
    if CopyBuffer(MACD_Handle[3], mode, 0, to_copy, ExtCloseBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Max = MathMax(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        Min = MathMin(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        ExtHighBuffer[bar] = _fdiv(MathMax(Max, ExtHighBuffer[bar]), Point())
        ExtLowBuffer[bar] = _fdiv(MathMin(Min, ExtLowBuffer[bar]), Point())
        ExtOpenBuffer[bar] = _fdiv(ExtOpenBuffer[bar], Point())
        ExtCloseBuffer[bar] = _fdiv(ExtCloseBuffer[bar], Point())
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 2.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Macdcandle(_MQL5Indicator):
    name = 'macdcandle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'fast_ema_period': 12,  # Период быстрой средней
        'slow_ema_period': 26,  # Период медленной средней
        'signal_period': 9,  # Период усреднения разности
        'mode': _Choice({0: 'Гистограмма', 1: 'Сигнальная линия'}, default=1),  # Источник даных для расчета
    }

