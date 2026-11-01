"""trendpower — converted from MQL5: MQL5 Indicators/TrendPower/trendpower.mq5

Copyright: Copyright © 2007, mandorr; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, mandorr', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 5, 5: 5}, 'colors': {1: [8421504], 2: [16711680], 3: [8721863], 4: [16760576], 5: [255]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 4, 5: 4}, 'styles': {1: 0, 2: 4, 3: 4}, 'labels': {1: 'Lower TrendPower', 2: 'Upper TrendPower', 3: 'Lower TrendPower', 4: 'Buy TrendPower', 5: 'Sell TrendPower'}, 'levels': [], 'description': [], 'name': 'trendpower', 'source': 'MQL5 Indicators/TrendPower/trendpower.mq5', 'folder': 'TrendPower', 'inputs': [{'mql': 'PeriodStep', 'py': 'PeriodStep', 'param': 'PeriodStep', 'type': 'uint', 'default': 10, 'label': 'Moving averages period step;', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 1, 'label': 'smoothing method', 'sinput': False}, {'mql': 'MAPrice', 'py': 'MAPrice', 'param': 'MAPrice', 'type': 'int', 'default': 1, 'label': 'type of price', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
PeriodStep = _input('PeriodStep', 10)  # Moving averages period step;
MAType = _input('MAType', MODE_EMA)  # smoothing method
MAPrice = _input('MAPrice', PRICE_CLOSE)  # type of price
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
ExtMapBufferUp = Arr(0, 0.0)
ExtMapBufferDown = Arr(0, 0.0)
ExtMapBufferUp1 = Arr(0, 0.0)
ExtMapBufferDown1 = Arr(0, 0.0)
ExtMapLineBuffer = Arr(0, 0.0)
MA_Handle = Arr(6, 0, dyn=False)
min_rates_total = 0

def OnInit():
    global min_rates_total
    for numb in range(0, 6):
        MA_Handle[numb] = iMA(None, 0, (numb + 1) * PeriodStep, 0, MAType, MAPrice)
        if MA_Handle[numb] == INVALID_HANDLE:
            Print(' Failed to get handle of the MA indicator')
            return 1
    min_rates_total = _int(PeriodStep * 6)
    SetIndexBuffer(0, ExtMapLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapLineBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ExtMapBufferUp, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferUp, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, ExtMapBufferDown, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferDown, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, ExtMapBufferUp1, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferUp1, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(4, ExtMapBufferDown1, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferDown1, True)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'TrendPower(', PeriodStep, ', ', EnumToString(MAType, 'ENUM_MA_METHOD'), ', ', EnumToString(MAPrice, 'ENUM_APPLIED_PRICE'), ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    for numb in range(0, 6):
        if BarsCalculated(MA_Handle[numb]) < rates_total:
            return 0
    if rates_total < min_rates_total:
        return 0
    MA1 = Arr(0, 0.0)
    MA2 = Arr(0, 0.0)
    MA3 = Arr(0, 0.0)
    MA4 = Arr(0, 0.0)
    MA5 = Arr(0, 0.0)
    MA6 = Arr(0, 0.0)
    h = 0.0
    l = 0.0
    limit = 0
    to_copy = 0
    bar = 0
    trend = 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(MA1, True)
    ArraySetAsSeries(MA2, True)
    ArraySetAsSeries(MA3, True)
    ArraySetAsSeries(MA4, True)
    ArraySetAsSeries(MA5, True)
    ArraySetAsSeries(MA6, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(MA_Handle[0], 0, 0, to_copy, MA1) <= 0:
        return 0
    if CopyBuffer(MA_Handle[1], 0, 0, to_copy, MA2) <= 0:
        return 0
    if CopyBuffer(MA_Handle[2], 0, 0, to_copy, MA3) <= 0:
        return 0
    if CopyBuffer(MA_Handle[3], 0, 0, to_copy, MA4) <= 0:
        return 0
    if CopyBuffer(MA_Handle[4], 0, 0, to_copy, MA5) <= 0:
        return 0
    if CopyBuffer(MA_Handle[5], 0, 0, to_copy, MA6) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtMapBufferUp[bar] = EMPTY_VALUE
        ExtMapBufferDown[bar] = EMPTY_VALUE
        ExtMapBufferUp1[bar] = EMPTY_VALUE
        ExtMapBufferDown1[bar] = EMPTY_VALUE
        h = MA1[bar]
        l = MA1[bar]
        if h < MA2[bar]:
            h = MA2[bar]
        if h < MA3[bar]:
            h = MA3[bar]
        if h < MA4[bar]:
            h = MA4[bar]
        if h < MA5[bar]:
            h = MA5[bar]
        if h < MA6[bar]:
            h = MA6[bar]
        if h > MA2[bar]:
            h = MA2[bar]
        if h > MA3[bar]:
            h = MA3[bar]
        if h > MA4[bar]:
            h = MA4[bar]
        if h > MA5[bar]:
            h = MA5[bar]
        if h > MA6[bar]:
            h = MA6[bar]
        if high[bar] > h:
            trend = 1
        if low[bar] < l:
            trend = -1
        if high[bar] > h and low[bar] < l:
            trend = 0
        if trend < 0:
            ExtMapBufferDown[bar] = h
        if trend > 0:
            ExtMapBufferUp[bar] = l
        ExtMapLineBuffer[bar] = (h + l) / 2
        if ExtMapBufferUp[bar + 1] == EMPTY_VALUE and ExtMapBufferUp[bar] != EMPTY_VALUE:
            ExtMapBufferUp1[bar] = ExtMapBufferUp[bar]
        if ExtMapBufferDown[bar + 1] == EMPTY_VALUE and ExtMapBufferDown[bar] != EMPTY_VALUE:
            ExtMapBufferDown1[bar] = ExtMapBufferDown[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Trendpower(_MQL5Indicator):
    name = 'trendpower'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PeriodStep': 10,  # Moving averages period step;
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # smoothing method
        'MAPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # type of price
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

