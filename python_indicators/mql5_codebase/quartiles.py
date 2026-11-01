"""quartiles — converted from MQL5: MQL5 Indicators/Quartiles/quartiles.mq5

Copyright: Copyright © 2010, LeMan.; Link: b-market@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, LeMan.', 'link': 'b-market@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [8421376], 2: [16711680], 3: [42495]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Upper Quartile', 2: 'Middle Quartile', 3: 'Lower Quartile'}, 'levels': [], 'description': [], 'name': 'quartiles', 'source': 'MQL5 Indicators/Quartiles/quartiles.mq5', 'folder': 'Quartiles', 'inputs': [{'mql': 'N', 'py': 'N', 'param': 'N', 'type': 'int', 'default': 20, 'label': '', 'sinput': False}, {'mql': 'p1', 'py': 'p1', 'param': 'p1', 'type': 'double', 'default': 0.25, 'label': '', 'sinput': False}, {'mql': 'p3', 'py': 'p3', 'param': 'p3', 'type': 'double', 'default': 0.75, 'label': '', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_APPLIED_PRICE_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('ENUM_APPLIED_PRICE_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
N = _input('N', 20)
p1 = _input('p1', 0.25)
p3 = _input('p3', 0.75)
IPC = _input('IPC', PRICE_CLOSE)  # Applied price
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
q1Buffer = Arr(0, 0.0)
q2Buffer = Arr(0, 0.0)
q3Buffer = Arr(0, 0.0)
n1 = 0
n2t = 0
n2f = 0
n3 = 0
PriceArray = Arr(0, 0.0)
min_rates_total = 0
N_ = 0

def OnInit():
    global N_, min_rates_total, n1, n2f, n2t, n3
    P1 = p1
    if p1 > 1:
        P1 = 1.0
        Print('p1 parameter cannot be above 1! Default value equal to 1 will be used!')
    if p1 < 0:
        P1 = 0.0
        Print('p1 parameter cannot be less than 0! Default value equal to 0 will be used!')
    P3 = p3
    if p3 > 1:
        P3 = 1.0
        Print('p3 parameter cannot be above 1! Default value equal to 1 will be used!')
    if p3 < 0:
        P3 = 0.0
        Print('p3 parameter cannot be less than 0! Default value equal to 0 will be used!')
    N_ = N
    if N_ < 3:
        N_ = 3
        Print('N parameter cannot be less than 3! Default value equal to 3 will be used!')
    min_rates_total = N_
    n1 = _int(MathRound(N_ * P1))
    if not n1:
        n1 = 1
    n2t = _idiv(N_ + 1, 2)
    n2f = _idiv(N_, 2)
    n3 = _int(MathRound(N_ * P3))
    if not n3:
        n3 = 1
    if ArrayResize(PriceArray, N_) < N_:
        Print('Failed to distribute the memory for PriceArray[] array')
    SetIndexBuffer(0, q3Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, q2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, q1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = 'Quartiles'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    q1 = 0.0
    q2 = 0.0
    q3 = 0.0
    if prev_calculated == 0:
        first = min_rates_total - 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        kkk = 0
        while kkk < N_:
            PriceArray[kkk] = PriceSeries(IPC, bar - kkk, open, low, high, close)
            kkk += 1
        ArraySort(PriceArray)
        if _imod(N_, 2) > 0:
            q2 = PriceArray[n2t - 1]
        else:
            q2 = (PriceArray[n2f - 1] + PriceArray[n2f]) / 2
        q1 = PriceArray[n1 - 1]
        q3 = PriceArray[n3 - 1]
        q1Buffer[bar] = NormalizeDouble(q1, Digits())
        q2Buffer[bar] = NormalizeDouble(q2, Digits())
        q3Buffer[bar] = NormalizeDouble(q3, Digits())
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def PriceSeries(applied_price, bar, Open, Low, High, Close):
    _sw1 = applied_price
    if _sw1 == PRICE_CLOSE:
        return Close[bar]
    elif _sw1 == PRICE_OPEN:
        return Open[bar]
    elif _sw1 == PRICE_HIGH:
        return High[bar]
    elif _sw1 == PRICE_LOW:
        return Low[bar]
    elif _sw1 == PRICE_MEDIAN:
        return (High[bar] + Low[bar]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (Close[bar] + High[bar] + Low[bar]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return ((2 * Close[bar]) + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 8:
        return (Open[bar] + Close[bar]) / 2.0
    elif _sw1 == 9:
        return (Open[bar] + Close[bar] + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 10:
        if Close[bar] > Open[bar]:
            return High[bar]
        else:
            if Close[bar] < Open[bar]:
                return Low[bar]
            else:
                return Close[bar]
    elif _sw1 == 11:
        if Close[bar] > Open[bar]:
            return (High[bar] + Close[bar]) / 2.0
        else:
            if Close[bar] < Open[bar]:
                return (Low[bar] + Close[bar]) / 2.0
            else:
                return Close[bar]
    else:
        return Close[bar]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Quartiles(_MQL5Indicator):
    name = 'quartiles'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'N': 20,
        'p1': 0.25,
        'p3': 0.75,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Applied price
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

