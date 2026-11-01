"""gfilter — converted from MQL5: MQL5 Indicators/GFilter/gfilter.mq5

This indicator calculates a filterline with the use of gaussian filtration
Copyright: Copyright © 2012, zzuegg; Link: http://when-money-makes-money.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, zzuegg', 'link': 'http://when-money-makes-money.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 8, 2: 5, 3: 5}, 'colors': {1: [8421376, 3937500], 2: [16711935], 3: [65280]}, 'widths': {1: 3, 2: 3, 3: 3}, 'styles': {1: 0}, 'labels': {1: 'GFilter', 2: 'Dn_Signal', 3: 'Up_Signal'}, 'levels': [], 'description': ['This indicator calculates a filterline with the use of gaussian filtration'], 'name': 'gfilter', 'source': 'MQL5 Indicators/GFilter/gfilter.mq5', 'folder': 'GFilter', 'inputs': [{'mql': 'FilterPeriod', 'py': 'FilterPeriod', 'param': 'FilterPeriod', 'type': 'uint', 'default': 12, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
FilterPeriod = _input('FilterPeriod', 12)  # Период индикатора
IPC = _input('IPC', PRICE_CLOSE_)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
BearsBuffer = Arr(0, 0.0)
BullsBuffer = Arr(0, 0.0)
fil_alfa = 0.0
dPriceShift = 0.0
min_rates_total = 0

def getAlfa(p):
    w = _fdiv(2 * 3.1415926535, p)
    beta = _fdiv(1 - MathCos(w), MathPow(1.414, 2.0 / 3) - 1)
    alfa = (-beta) + MathSqrt((beta * beta) + (2 * beta))
    return alfa

def GSMOOTH(price, arr, alfa, index):
    ret = (MathPow(alfa, 4) * price) + (4 * (1 - alfa) * arr[index - 1]) - (6 * MathPow(1 - alfa, 2) * arr[index - 2]) + (4 * MathPow(1 - alfa, 3) * arr[index - 3]) - (MathPow(1 - alfa, 4) * arr[index - 4])
    return ret

def OnInit():
    global dPriceShift, fil_alfa, min_rates_total
    min_rates_total = _int(FilterPeriod + 4)
    dPriceShift = Point() * PriceShift
    fil_alfa = getAlfa(FilterPeriod)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, BearsBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, BullsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, FilterPeriod)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, FilterPeriod)
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, FilterPeriod)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    shortname = Box("")
    StringConcatenate(shortname, 'GFilter( ', FilterPeriod, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    series = 0.0
    s1 = 0.0
    s2 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = _int(FilterPeriod) - 1
        IndBuffer[first - 1] = PriceSeries(IPC, first - 1, open, low, high, close)
        IndBuffer[first - 2] = PriceSeries(IPC, first - 2, open, low, high, close)
        IndBuffer[first - 3] = PriceSeries(IPC, first - 3, open, low, high, close)
        IndBuffer[first - 4] = PriceSeries(IPC, first - 4, open, low, high, close)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        BullsBuffer[bar] = 0.0
        BearsBuffer[bar] = 0.0
        series = PriceSeries(IPC, bar, open, low, high, close)
        IndBuffer[bar] = GSMOOTH(series, IndBuffer, fil_alfa, bar)
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        if IndBuffer[bar] < IndBuffer[bar - 1]:
            ColorIndBuffer[bar] = 1.0
        else:
            ColorIndBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        s2 = IndBuffer[bar - 2] - IndBuffer[bar - 1]
        s1 = IndBuffer[bar - 1] - IndBuffer[bar]
        if s1 < s2:
            BullsBuffer[bar] = IndBuffer[bar]
        if s1 > s2:
            BearsBuffer[bar] = IndBuffer[bar]
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
    elif _sw1 == 12:
        res = High[bar] + Low[bar] + Close[bar]
        if Close[bar] < Open[bar]:
            res = (res + Low[bar]) / 2
        if Close[bar] > Open[bar]:
            res = (res + High[bar]) / 2
        if Close[bar] == Open[bar]:
            res = (res + Close[bar]) / 2
        return (res - Low[bar] + (res - High[bar])) / 2
    else:
        return Close[bar]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Gfilter(_MQL5Indicator):
    name = 'gfilter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FilterPeriod': 12,  # Период индикатора
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
    }

