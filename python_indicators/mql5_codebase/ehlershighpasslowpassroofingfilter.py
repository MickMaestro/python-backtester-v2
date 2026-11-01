"""EhlersHighPassLowPassRoofingFilter — converted from MQL5: MQL5 Indicators/The HighPass - LowPass Roofing Filter/EhlersHighPassLowPassRoofingFilter.mq5

Telegram Channel: https://t.me/fxstill\\n
The HighPass-LowPass Roofing Filter:\\nJohn Ehlers, \\"Cycle Analytics For Traders\\", pg.78
Copyright: Copyright 2020, Andrei Novichkov.; Link: http://fxstill.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, Andrei Novichkov.', 'link': 'http://fxstill.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [32768, 255, 3329330]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'RB'}, 'levels': [], 'description': ['Telegram Channel: https://t.me/fxstill\\n', 'The HighPass-LowPass Roofing Filter:\\nJohn Ehlers, \\"Cycle Analytics For Traders\\", pg.78'], 'name': 'EhlersHighPassLowPassRoofingFilter', 'source': 'MQL5 Indicators/The HighPass - LowPass Roofing Filter/EhlersHighPassLowPassRoofingFilter.mq5', 'folder': 'The HighPass - LowPass Roofing Filter', 'inputs': [{'mql': 'HPLength', 'py': 'HPLength', 'param': 'HPLength', 'type': 'int', 'default': 48, 'label': '', 'sinput': False}, {'mql': 'SSFLength', 'py': 'SSFLength', 'param': 'SSFLength', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
HPLength = _input('HPLength', 48)
SSFLength = _input('SSFLength', 10)
rb = Arr(0, 0.0)
rc = Arr(0, 0.0)
hb = Arr(0, 0.0)
MINBAR = 5
a1 = 0.0
a2 = 0.0
c1 = 0.0
c2 = 0.0
c3 = 0.0

def OnInit():
    global a1, a2, c1, c2, c3
    SetIndexBuffer(0, rb, INDICATOR_DATA)
    SetIndexBuffer(1, rc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, hb, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(rb, True)
    ArraySetAsSeries(rc, True)
    ArraySetAsSeries(hb, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EhlersHighPassLowPassRoofingFilter')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    twoPiPrd = (2 * M_PI) / HPLength
    alpha1 = _fdiv(MathCos(twoPiPrd) + MathSin(twoPiPrd) - 1, MathCos(twoPiPrd))
    alpha2 = MathExp(((-M_SQRT2) * M_PI) / SSFLength)
    beta = 2 * alpha2 * MathCos((M_SQRT2 * M_PI) / SSFLength)
    c2 = beta
    c3 = -MathPow(alpha2, 2)
    c1 = 1 - c2 - c3
    a1 = 1 - (alpha1 / 2)
    a2 = 1 - alpha1
    return INIT__SUCCEEDED()

def GetValue(price, shift):
    hb[shift] = (a1 * (price[shift] - price[shift + 1])) + (a2 * hb[shift + 1])
    r1 = ZerroIfEmpty(rb[shift + 1])
    r2 = ZerroIfEmpty(rb[shift + 2])
    rb[shift] = ((c1 * (hb[shift] + hb[shift + 1])) / 2) + (c2 * r1) + (c3 * r2)
    if rb[shift] < 0:
        rc[shift] = 1.0
    elif rb[shift] > 0:
        rc[shift] = 2.0

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

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total <= MINBAR:
        return 0
    ArraySetAsSeries(price, True)
    limit = rates_total - prev_calculated
    if limit == 0:
        pass
    elif limit == 1:
        GetValue(price, 1)
        return rates_total
    elif limit > 1:
        ArrayInitialize(rb, EMPTY_VALUE)
        ArrayInitialize(rc, 0)
        ArrayInitialize(hb, 0)
        limit = rates_total - MINBAR
        for i in range(limit, 1 - 1, -1):
            GetValue(price, i)
        return rates_total
    GetValue(price, 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EhlersHighPassLowPassRoofingFilter(_MQL5Indicator):
    name = 'EhlersHighPassLowPassRoofingFilter'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'HPLength': 48,
        'SSFLength': 10,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

