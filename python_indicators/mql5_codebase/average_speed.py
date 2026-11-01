"""average_speed — converted from MQL5: MQL5 Indicators/Average Speed/average_speed.mq5

Copyright: Copyright 2013, Totom Sukopratomo; Link: https://login.mql5.com/en/users/tomsuk001; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2013, Totom Sukopratomo', 'link': 'https://login.mql5.com/en/users/tomsuk001', 'version': '2.00', 'window': 'separate', 'indicator_minimum': 0.0, 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 3}, 'colors': {1: [32768]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Output'}, 'levels': [], 'description': [], 'name': 'average_speed', 'source': 'MQL5 Indicators/Average Speed/average_speed.mq5', 'folder': 'Average Speed', 'inputs': [{'mql': 'n', 'py': 'n', 'param': 'n', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'price', 'py': 'price', 'param': 'price', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
n = _input('n', 3)
price = _input('price', PRICE_CLOSE)
OutputBuffer = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, OutputBuffer, INDICATOR_DATA)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = 0
    if prev_calculated == 0:
        limit = n
    else:
        limit = prev_calculated - 1
    for i in range(limit, rates_total):
        v = 0.0
        d = 0.0
        t = GetMinute()
        sumv = 0.0
        for j in range(i - n + 1, i + 1):
            _sw1 = price
            if _sw1 == PRICE_CLOSE:
                d = _fdiv(MathAbs(close[j] - close[j - 1]), Point())
                v = _fdiv(d, t)
                sumv += v
            elif _sw1 == PRICE_HIGH:
                d = _fdiv(MathAbs(high[j] - high[j - 1]), Point())
                v = _fdiv(d, t)
                sumv += v
            elif _sw1 == PRICE_LOW:
                d = _fdiv(MathAbs(low[j] - low[j - 1]), Point())
                v = _fdiv(d, t)
                sumv += v
            elif _sw1 == PRICE_MEDIAN:
                d = _fdiv(MathAbs(((high[j] + low[j]) / 2) - ((high[j - 1] + low[j - 1]) / 2)), Point())
                v = _fdiv(d, t)
                sumv += v
            elif _sw1 == PRICE_OPEN:
                d = _fdiv(MathAbs(open[j] - open[j - 1]), Point())
                v = _fdiv(d, t)
                sumv += v
            elif _sw1 == PRICE_TYPICAL:
                d = _fdiv(MathAbs(((high[j] + low[j] + close[j]) / 3) - ((high[j - 1] + low[j - 1] + close[j - 1]) / 3)), Point())
                v = _fdiv(d, t)
                sumv += v
            elif _sw1 == PRICE_WEIGHTED:
                d = _fdiv(MathAbs(((high[j] + low[j] + close[j] + close[j]) / 4) - ((high[j - 1] + low[j - 1] + close[j - 1] + close[j - 1]) / 4)), Point())
                v = _fdiv(d, t)
                sumv += v
        A = (1.0 / n) * sumv
        OutputBuffer[i] = A
    return rates_total

def GetMinute():
    _sw2 = Period()
    if _sw2 == PERIOD_M1:
        return 1
    elif _sw2 == PERIOD_M2:
        return 2
    elif _sw2 == PERIOD_M3:
        return 3
    elif _sw2 == PERIOD_M4:
        return 4
    elif _sw2 == PERIOD_M5:
        return 5
    elif _sw2 == PERIOD_M6:
        return 6
    elif _sw2 == PERIOD_M10:
        return 10
    elif _sw2 == PERIOD_M12:
        return 12
    elif _sw2 == PERIOD_M15:
        return 15
    elif _sw2 == PERIOD_M20:
        return 20
    elif _sw2 == PERIOD_M30:
        return 30
    elif _sw2 == PERIOD_H1:
        return 60
    elif _sw2 == PERIOD_H2:
        return 120
    elif _sw2 == PERIOD_H3:
        return 180
    elif _sw2 == PERIOD_H4:
        return 240
    elif _sw2 == PERIOD_H6:
        return 360
    elif _sw2 == PERIOD_H8:
        return 480
    elif _sw2 == PERIOD_H12:
        return 720
    elif _sw2 == PERIOD_D1:
        return 1440
    elif _sw2 == PERIOD_W1:
        return 10080
    elif _sw2 == PERIOD_MN1:
        return 43200
    return 1


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AverageSpeed(_MQL5Indicator):
    name = 'average_speed'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'n': 3,
        'price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
    }

