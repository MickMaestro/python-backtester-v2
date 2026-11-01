"""round_price_doc — converted from MQL5: MQL5 Indicators/Round Price/round_price_doc.mq5

Copyright: mladen; Link: mladenfx@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'mladen', 'link': 'mladenfx@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 7}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1}, 'colors': {1: [55295], 2: [16760576], 3: [16760576], 4: [16760576], 5: [9662683], 6: [9662683], 7: [9662683]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'round_price_doc', 'source': 'MQL5 Indicators/Round Price/round_price_doc.mq5', 'folder': 'Round Price', 'inputs': [{'mql': 'T3Period', 'py': 'T3Period', 'param': 'T3Period', 'type': 'int', 'default': 89, 'label': 'T3 Calculation period', 'sinput': False}, {'mql': 'T3Hot', 'py': 'T3Hot', 'param': 'T3Hot', 'type': 'double', 'default': 0.7, 'label': 'T3 hot value', 'sinput': False}, {'mql': 'T3Original', 'py': 'T3Original', 'param': 'T3Original', 'type': 'bool', 'default': False, 'label': 'T3 original Tillson calculation?', 'sinput': False}, {'mql': 'T3Price', 'py': 'T3Price', 'param': 'T3Price', 'type': 'int', 'default': 1, 'label': 'T3 price to use', 'sinput': False}, {'mql': 'Delta1', 'py': 'Delta1', 'param': 'Delta1', 'type': 'int', 'default': 89, 'label': 'Distance in points for first band', 'sinput': False}, {'mql': 'Delta2', 'py': 'Delta2', 'param': 'Delta2', 'type': 'int', 'default': 144, 'label': 'Distance in points for second band', 'sinput': False}, {'mql': 'Delta3', 'py': 'Delta3', 'param': 'Delta3', 'type': 'int', 'default': 233, 'label': 'Distance in points for third band', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
T3Period = _input('T3Period', 89)  # T3 Calculation period
T3Hot = _input('T3Hot', 0.7)  # T3 hot value
T3Original = _input('T3Original', False)  # T3 original Tillson calculation?
T3Price = _input('T3Price', PRICE_CLOSE)  # T3 price to use
Delta1 = _input('Delta1', 89)  # Distance in points for first band
Delta2 = _input('Delta2', 144)  # Distance in points for second band
Delta3 = _input('Delta3', 233)  # Distance in points for third band
t3 = Arr(0, 0.0)
t3Up1 = Arr(0, 0.0)
t3Up2 = Arr(0, 0.0)
t3Up3 = Arr(0, 0.0)
t3Dn1 = Arr(0, 0.0)
t3Dn2 = Arr(0, 0.0)
t3Dn3 = Arr(0, 0.0)
c1 = 0.0
c2 = 0.0
c3 = 0.0
c4 = 0.0
t3Alpha = 0.0
t3Values = Arr(0, 0.0, dims=(6,))

def OnInit():
    global c1, c2, c3, c4, t3Alpha
    SetIndexBuffer(0, t3, INDICATOR_DATA)
    SetIndexBuffer(1, t3Up1, INDICATOR_DATA)
    SetIndexBuffer(2, t3Up2, INDICATOR_DATA)
    SetIndexBuffer(3, t3Up3, INDICATOR_DATA)
    SetIndexBuffer(4, t3Dn1, INDICATOR_DATA)
    SetIndexBuffer(5, t3Dn2, INDICATOR_DATA)
    SetIndexBuffer(6, t3Dn3, INDICATOR_DATA)
    PlotIndexSetString(0, PLOT_LABEL, 'T3')
    for i in range(1, 4):
        PlotIndexSetString(i, PLOT_LABEL, 'T3 upper band ' + _str(i))
        PlotIndexSetString(i + 3, PLOT_LABEL, 'T3 lower band ' + _str(i))
    a = MathMax(MathMin(T3Hot, 1), 0.0001)
    c1 = (-a) * a * a
    c2 = 3 * ((a * a) + (a * a * a))
    c3 = -3 * ((2 * a * a) + a + (a * a * a))
    c4 = 1 + (3 * a) + (a * a * a) + (3 * a * a)
    t3period = T3Period
    if not T3Original:
        t3period = 1.0 + ((t3period - 1.0) / 2.0)
    t3Alpha = _fdiv(2.0, 1.0 + t3period)
    return 0

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    for i in range(MathMax(prev_calculated - 1, 0), rates_total):
        price = 0.0
        _sw1 = T3Price
        if _sw1 == PRICE_CLOSE:
            price = Close[i]
        elif _sw1 == PRICE_OPEN:
            price = Open[i]
        elif _sw1 == PRICE_HIGH:
            price = High[i]
        elif _sw1 == PRICE_LOW:
            price = Low[i]
        elif _sw1 == PRICE_MEDIAN:
            price = (High[i] + Low[i]) / 2.0
        elif _sw1 == PRICE_TYPICAL:
            price = (High[i] + Low[i] + Close[i]) / 3.0
        elif _sw1 == PRICE_WEIGHTED:
            price = (High[i] + Low[i] + Close[i] + Close[i]) / 4.0
        else:
            price = 0.0
        t3[i] = calcT3(price, i, rates_total)
        t3Up1[i] = t3[i] + (Delta1 * Point())
        t3Up2[i] = t3[i] + (Delta2 * Point())
        t3Up3[i] = t3[i] + (Delta3 * Point())
        t3Dn1[i] = t3[i] - (Delta1 * Point())
        t3Dn2[i] = t3[i] - (Delta2 * Point())
        t3Dn3[i] = t3[i] - (Delta3 * Point())
    return rates_total

def calcT3(price, r, bars, s=0):
    if ArrayRange(t3Values, 0) != bars:
        ArrayResize(t3Values, bars)
    if r < 2:
        t3Values[r][s + 0] = price
        t3Values[r][s + 1] = price
        t3Values[r][s + 2] = price
        t3Values[r][s + 3] = price
        t3Values[r][s + 4] = price
        t3Values[r][s + 5] = price
    else:
        t3Values[r][s + 0] = t3Values[r - 1][s + 0] + (t3Alpha * (price - t3Values[r - 1][s + 0]))
        t3Values[r][s + 1] = t3Values[r - 1][s + 1] + (t3Alpha * (t3Values[r][s + 0] - t3Values[r - 1][s + 1]))
        t3Values[r][s + 2] = t3Values[r - 1][s + 2] + (t3Alpha * (t3Values[r][s + 1] - t3Values[r - 1][s + 2]))
        t3Values[r][s + 3] = t3Values[r - 1][s + 3] + (t3Alpha * (t3Values[r][s + 2] - t3Values[r - 1][s + 3]))
        t3Values[r][s + 4] = t3Values[r - 1][s + 4] + (t3Alpha * (t3Values[r][s + 3] - t3Values[r - 1][s + 4]))
        t3Values[r][s + 5] = t3Values[r - 1][s + 5] + (t3Alpha * (t3Values[r][s + 4] - t3Values[r - 1][s + 5]))
    return (c1 * t3Values[r][s + 5]) + (c2 * t3Values[r][s + 4]) + (c3 * t3Values[r][s + 3]) + (c4 * t3Values[r][s + 2])


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RoundPriceDoc(_MQL5Indicator):
    name = 'round_price_doc'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'T3Period': 89,  # T3 Calculation period
        'T3Hot': 0.7,  # T3 hot value
        'T3Original': False,  # T3 original Tillson calculation?
        'T3Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # T3 price to use
        'Delta1': 89,  # Distance in points for first band
        'Delta2': 144,  # Distance in points for second band
        'Delta3': 233,  # Distance in points for third band
    }

