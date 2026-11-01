"""correctedaverage — converted from MQL5: MQL5 Indicators/CorrectedAverage/correctedaverage.mq5

Copyright: Copyright © 2006, Alexander Piechotta; Link: http://onix-trade.net/forum/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Alexander Piechotta', 'link': 'http://onix-trade.net/forum/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [15624315]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'CorrectedAverage'}, 'levels': [], 'description': [], 'name': 'correctedaverage', 'source': 'MQL5 Indicators/CorrectedAverage/correctedaverage.mq5', 'folder': 'CorrectedAverage', 'inputs': [{'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 0, 'label': '/method of averaging', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 12, 'label': 'smoothing depth', 'sinput': False}, {'mql': 'Applied_price', 'py': 'Applied_price', 'param': 'Applied_price', 'type': 'int', 'default': 1, 'label': 'price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'vertical shift of the indicator in pointsх', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MA_Method = _input('MA_Method', MODE_SMA)  # /method of averaging
Length = _input('Length', 12)  # smoothing depth
Applied_price = _input('Applied_price', PRICE_CLOSE)  # price constant
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # vertical shift of the indicator in pointsх
MABuffer = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0
MA_Handle = 0
STD_Handle = 0

def OnInit():
    global MA_Handle, STD_Handle, dPriceShift, min_rates_total
    _sw1 = MA_Method
    if _sw1 == MODE_SMA:
        min_rates_total = _int(Length)
    elif _sw1 == MODE_EMA:
        min_rates_total = 2
    elif _sw1 == MODE_SMMA:
        min_rates_total = _int(Length)
    elif _sw1 == MODE_LWMA:
        min_rates_total = _int(Length) + 1
    min_rates_total += 1
    STD_Handle = iStdDev(None, PERIOD_CURRENT, Length, 0, MA_Method, Applied_price)
    if STD_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iStdDev indicator')
        return 1
    MA_Handle = iMA(None, PERIOD_CURRENT, Length, 0, MA_Method, Applied_price)
    if MA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
        return 1
    SetIndexBuffer(0, MABuffer, INDICATOR_DATA)
    ArraySetAsSeries(MABuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'CorrectedAverage( Length = ', Length, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    dPriceShift = Point() * PriceShift
    return 0

def OnCalculate(rates_total, prev_calculated, begin, price):
    if (BarsCalculated(STD_Handle) < rates_total or BarsCalculated(MA_Handle) < rates_total) or rates_total < (min_rates_total + begin):
        return 0
    limit = 0
    bar = 0
    to_copy = 0
    v1 = 0.0
    v2 = 0.0
    k = 0.0
    MA = Arr(0, 0.0)
    STD = Arr(0, 0.0)
    ArraySetAsSeries(MA, True)
    ArraySetAsSeries(STD, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        to_copy = limit + 2
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total + begin)
        bar = limit
        for bar in range(bar, 0 - 1, -1):
            MABuffer[bar] = EMPTY_VALUE
        else:
            bar = _range_end(bar, 0 - 1, -1)
    else:
        limit = rates_total - prev_calculated
        to_copy = limit + 1
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MA) <= 0:
        return 0
    if CopyBuffer(STD_Handle, 0, 0, to_copy, STD) <= 0:
        return 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        MABuffer[limit + 1] = MA[limit + 1]
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        v1 = MathPow(STD[bar], 2)
        v2 = MathPow(MABuffer[bar + 1] - MA[bar], 2)
        if v2 < v1 or (not v2):
            k = 0.0
        else:
            k = 1 - _fdiv(v1, v2)
        MABuffer[bar] = MABuffer[bar + 1] + (k * (MA[bar] - MABuffer[bar + 1]))
        MABuffer[bar] += dPriceShift
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Correctedaverage(_MQL5Indicator):
    name = 'correctedaverage'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # /method of averaging
        'Length': 12,  # smoothing depth
        'Applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # price constant
        'Shift': 0,  # horizontal shift of the indicator in bars
        'PriceShift': 0,  # vertical shift of the indicator in pointsх
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

