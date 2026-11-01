"""EhlersHurstCoefficient — converted from MQL5: MQL5 Indicators/The Hurst Coefficient Indicator/EhlersHurstCoefficient.mq5

Telegram Channel: https://t.me/fxstill\\n
The Hurst Coefficient:\\nJohn Ehlers, \\"Cycle Analytics For Traders\\", pg.67-68
Copyright: Copyright 2020, Andrei Novichkov.; Link: http://fxstill.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, Andrei Novichkov.', 'link': 'http://fxstill.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [32768, 255, 3329330]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': ['Telegram Channel: https://t.me/fxstill\\n', 'The Hurst Coefficient:\\nJohn Ehlers, \\"Cycle Analytics For Traders\\", pg.67-68'], 'name': 'EhlersHurstCoefficient', 'source': 'MQL5 Indicators/The Hurst Coefficient Indicator/EhlersHurstCoefficient.mq5', 'folder': 'The Hurst Coefficient Indicator', 'inputs': [{'mql': 'length', 'py': 'length', 'param': 'length', 'type': 'int', 'default': 30, 'label': 'Length', 'sinput': False}, {'mql': 'ssflength', 'py': 'ssflength', 'param': 'ssflength', 'type': 'int', 'default': 20, 'label': 'SuperSmoother filter Length', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
length = _input('length', 30)  # Length
ssflength = _input('ssflength', 20)  # SuperSmoother filter Length
a = 0.0
b = 0.0
c1 = 0.0
c2 = 0.0
c3 = 0.0
hl = 0
smoothHurst = Arr(0, 0.0)
hurst = Arr(0, 0.0)
cf = Arr(0, 0.0)
dimen = Arr(0, 0.0)
MINBAR = length

def OnInit():
    global a, b, c1, c2, c3, hl
    SetIndexBuffer(0, smoothHurst, INDICATOR_DATA)
    SetIndexBuffer(1, cf, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, hurst, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, dimen, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(smoothHurst, True)
    ArraySetAsSeries(cf, True)
    ArraySetAsSeries(hurst, True)
    ArraySetAsSeries(dimen, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EhlersHurstCoefficient')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    a = MathExp(((-M_SQRT2) * M_PI) / ssflength)
    b = 2 * a * MathCos((M_SQRT2 * M_PI) / ssflength)
    c2 = b
    c3 = -MathPow(a, 2)
    c1 = 1 - c2 - c3
    hl = _int(MathCeil(_idiv(length, 2)))
    return INIT__SUCCEEDED()

def GetValue(price, shift):
    ih = iHighest(None, 0, MODE_CLOSE, length, shift)
    il = iLowest(None, 0, MODE_CLOSE, length, shift)
    if ih == -1 or il == -1:
        return
    n3 = (price[ih] - price[il]) / length
    hh = price[shift]
    ll = price[shift]
    for i in range(shift, shift + hl):
        if price[i] > hh:
            hh = price[i]
        if price[i] < ll:
            ll = price[i]
    n1 = _fdiv(hh - ll, hl)
    hh = price[shift + hl]
    ll = price[shift + hl]
    for i in range(shift + hl, shift + length):
        if price[i] > hh:
            hh = price[i]
        if price[i] < ll:
            ll = price[i]
    n2 = _fdiv(hh - ll, hl)
    dimen[shift] = ((0.5 * (_fdiv(log(n1 + n2) - log(n3), log(2)) + dimen[shift + 1])) if ((n1 > 0 and n2 > 0) and n3 > 0) else 0)
    hurst[shift] = 2 - dimen[shift]
    s1 = ZerroIfEmpty(smoothHurst[shift + 1])
    s2 = ZerroIfEmpty(smoothHurst[shift + 2])
    smoothHurst[shift] = ((c1 * (hurst[shift] + hurst[shift + 1])) / 2) + (c2 * s1) + (c3 * s2)
    if smoothHurst[shift] < 0.5:
        cf[shift] = 1.0
    elif smoothHurst[shift] > 0.5:
        cf[shift] = 2.0

def INIT__SUCCEEDED():
    PlaySound('ok.wav')
    cm = 'Subscribe! https://t.me/fxstill'
    Print(cm)
    Comment('\n' + cm)
    return INIT_SUCCEEDED

def ZerroIfEmpty(value):
    if value >= EMPTY_VALUE or value <= (-EMPTY_VALUE):
        return 0.0
    return value

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total <= MINBAR:
        return 0
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    limit = rates_total - prev_calculated
    if limit == 0:
        pass
    elif limit == 1:
        GetValue(close, 1)
        return rates_total
    elif limit > 1:
        ArrayInitialize(smoothHurst, EMPTY_VALUE)
        ArrayInitialize(cf, 0)
        ArrayInitialize(hurst, 0)
        ArrayInitialize(dimen, 0)
        limit = rates_total - MINBAR
        for i in range(limit, 1 - 1, -1):
            GetValue(close, i)
        return rates_total
    GetValue(close, 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EhlersHurstCoefficient(_MQL5Indicator):
    name = 'EhlersHurstCoefficient'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'length': 30,  # Length
        'ssflength': 20,  # SuperSmoother filter Length
    }

