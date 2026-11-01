"""EhlersRoofingFilter — converted from MQL5: MQL5 Indicators/The Roofing Filter/EhlersRoofingFilter.mq5

Ehlers Roofing Filter:\\nJohn Ehlers, \\"Cycle Analytics for Traders\\", pg.80-82
Copyright: Copyright 2020, Andrei Novichkov.; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, Andrei Novichkov.', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 8, 2: 1}, 'colors': {1: [32768, 255, 3329330], 2: [9109504]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'rfilt', 2: 'trigger'}, 'levels': [], 'description': ['Ehlers Roofing Filter:\\nJohn Ehlers, \\"Cycle Analytics for Traders\\", pg.80-82'], 'name': 'EhlersRoofingFilter', 'source': 'MQL5 Indicators/The Roofing Filter/EhlersRoofingFilter.mq5', 'folder': 'The Roofing Filter', 'inputs': [{'mql': 'hpLength', 'py': 'hpLength', 'param': 'hpLength', 'type': 'int', 'default': 80, 'label': '', 'sinput': False}, {'mql': 'lpLength', 'py': 'lpLength', 'param': 'lpLength', 'type': 'int', 'default': 40, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
hpLength = _input('hpLength', 80)
lpLength = _input('lpLength', 40)
rb = Arr(0, 0.0)
rc = Arr(0, 0.0)
tb = Arr(0, 0.0)
hp = Arr(0, 0.0)
MINBAR = 5
c1 = 0.0
c2 = 0.0
c3 = 0.0
a1 = 0.0
t1 = 0.0
t2 = 0.0
t3 = 0.0

def OnInit():
    global a1, c1, c2, c3, t1, t2, t3
    SetIndexBuffer(0, rb, INDICATOR_DATA)
    SetIndexBuffer(1, rc, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, tb, INDICATOR_DATA)
    SetIndexBuffer(3, hp, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(rb, True)
    ArraySetAsSeries(rc, True)
    ArraySetAsSeries(tb, True)
    ArraySetAsSeries(hp, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'EhlersRoofingFilter')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    twoPiPrd = (M_SQRT1_2 * 2 * M_PI) / hpLength
    a1 = _fdiv(MathCos(twoPiPrd) + MathSin(twoPiPrd) - 1, MathCos(twoPiPrd))
    a2 = MathExp(((-M_SQRT2) * M_PI) / lpLength)
    beta = 2 * a2 * MathCos((M_SQRT2 * M_PI) / lpLength)
    c2 = beta
    c3 = (-a2) * a2
    c1 = 1 - c2 - c3
    t1 = MathPow(1 - (a1 / 2), 2)
    t2 = 1 - a1
    t3 = MathPow(t2, 2)
    t2 *= 2
    return INIT_SUCCEEDED

def GetValue(price, shift):
    hp[shift] = (t1 * (price[shift] - (2 * price[shift + 1]) + price[shift + 2])) + (t2 * hp[shift + 1]) - (t3 * hp[shift + 2])
    r1 = ZerroIfEmpty(rb[shift + 1])
    r2 = ZerroIfEmpty(rb[shift + 2])
    rb[shift] = (c1 * ((hp[shift] + hp[shift + 1]) / 2)) + (c2 * r1) + (c3 * r2)
    tb[shift] = r2
    if rb[shift] < 0:
        rc[shift] = 1.0
    elif rb[shift] > 0:
        rc[shift] = 2.0

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
        ArrayInitialize(tb, EMPTY_VALUE)
        ArrayInitialize(rc, 0)
        ArrayInitialize(hp, 0)
        limit = rates_total - MINBAR
        for i in range(limit, 1 - 1, -1):
            GetValue(price, i)
        return rates_total
    GetValue(price, 0)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EhlersRoofingFilter(_MQL5Indicator):
    name = 'EhlersRoofingFilter'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'hpLength': 80,
        'lpLength': 40,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

