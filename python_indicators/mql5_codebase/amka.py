"""amka — converted from MQL5: MQL5 Indicators/AMkA/amka.mq5

Copyright: Copyright © 2004, by GOODMAN & Mstera и AF; Link: http://forum.viac.ru/viewforum.php?f=7; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2004, by GOODMAN & Mstera и AF', 'link': 'http://forum.viac.ru/viewforum.php?f=7', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 5, 3: 5}, 'colors': {1: [14822282], 2: [255], 3: [65280]}, 'widths': {1: 3, 2: 2, 3: 2}, 'styles': {1: 0}, 'labels': {1: 'AMA', 2: 'Dn_Signal', 3: 'Up_Signal'}, 'levels': [], 'description': [], 'name': 'amka', 'source': 'MQL5 Indicators/AMkA/amka.mq5', 'folder': 'AMkA', 'inputs': [{'mql': 'ama_period', 'py': 'ama_period', 'param': 'ama_period', 'type': 'int', 'default': 9, 'label': 'Period of AMA', 'sinput': False}, {'mql': 'fast_ma_period', 'py': 'fast_ma_period', 'param': 'fast_ma_period', 'type': 'int', 'default': 2, 'label': 'Period of fast MA', 'sinput': False}, {'mql': 'slow_ma_period', 'py': 'slow_ma_period', 'param': 'slow_ma_period', 'type': 'int', 'default': 30, 'label': 'Period of slow MA', 'sinput': False}, {'mql': 'G', 'py': 'G', 'param': 'G', 'type': 'double', 'default': 2.0, 'label': 'The power the smoothing constant is raised to', 'sinput': False}, {'mql': 'AMAShift', 'py': 'AMAShift', 'param': 'AMAShift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'dK', 'py': 'dK', 'param': 'dK', 'type': 'double', 'default': 1.0, 'label': 'Coefficient for the filter', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ama_period = _input('ama_period', 9)  # Period of AMA
fast_ma_period = _input('fast_ma_period', 2)  # Period of fast MA
slow_ma_period = _input('slow_ma_period', 30)  # Period of slow MA
G = _input('G', 2.0)  # The power the smoothing constant is raised to
AMAShift = _input('AMAShift', 0)  # Horizontal shift of the indicator in bars
dK = _input('dK', 1.0)  # Coefficient for the filter
AMABuffer = Arr(0, 0.0)
BearsBuffer = Arr(0, 0.0)
BullsBuffer = Arr(0, 0.0)
dSC = 0.0
slowSC = 0.0
fastSC = 0.0
AMA_Handle = 0
dAMA_Handle = 0

def OnInit():
    global dSC, fastSC, slowSC
    SetIndexBuffer(0, AMABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, AMAShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ama_period + 1)
    PlotIndexSetString(0, PLOT_LABEL, 'AMA')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(1, BearsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, AMAShift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, ama_period + 2)
    PlotIndexSetString(1, PLOT_LABEL, 'DnSignal')
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(2, BullsBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, AMAShift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, ama_period + 2)
    PlotIndexSetString(2, PLOT_LABEL, 'UpSignal')
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    shortname = Box("")
    StringConcatenate(shortname, 'AMkA( ', ama_period, ', ', fast_ma_period, ', ', slow_ma_period, ' )')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    slowSC = 2.0 / (slow_ma_period + 1)
    fastSC = 2.0 / (fast_ma_period + 1)
    dSC = fastSC - slowSC

def OnCalculate(rates_total, prev_calculated, begin, price):
    global _s_OnCalculate_dama
    if rates_total < ((2 * ama_period) + 2 + begin):
        return 0
    first = 0
    bar = 0
    iii = 0
    noise = 0.0
    AMA = 0.0
    signal = 0.0
    ER = 0.0
    ERSC = 0.0
    SSC = 0.0
    price0 = 0.0
    price1 = 0.0
    Sum = 0.0
    SMAdif = 0.0
    StDev = 0.0
    BULLS = 0.0
    BEARS = 0.0
    Filter = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = ama_period + 2 + begin
        AMA = price[first - 1]
        if ArrayResize(_s_OnCalculate_dAMA, ama_period) != ama_period:
            return 0
        if begin > 0:
            PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ama_period + begin)
            PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, (2 * ama_period) + begin + 2)
            PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, (2 * ama_period) + begin + 2)
    else:
        first = prev_calculated - 1
        AMA = AMABuffer[first - 1]
    bar = first
    for bar in range(bar, rates_total):
        noise = Point() / 10000
        iii = 0
        for iii in range(iii, ama_period):
            price0 = price[bar - iii - 0]
            price1 = price[bar - iii - 1]
            noise += MathAbs(price0 - price1)
        else:
            iii = _range_end(iii, ama_period, 1)
        price0 = price[bar]
        price1 = price[bar - ama_period]
        signal = MathAbs(price0 - price1)
        ER = _fdiv(signal, noise)
        ERSC = ER * dSC
        SSC = ERSC + slowSC
        AMA = AMA + (MathPow(SSC, G) * (price0 - AMA))
        AMABuffer[bar] = AMA
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated == 0:
        first = (2 * ama_period) + 6 + begin
    bar = first
    for bar in range(bar, rates_total):
        iii = 0
        for iii in range(iii, ama_period):
            _s_OnCalculate_dAMA[iii] = AMABuffer[bar - iii - 0] - AMABuffer[bar - iii - 1]
        else:
            iii = _range_end(iii, ama_period, 1)
        Sum = 0.0
        iii = 0
        for iii in range(iii, ama_period):
            Sum += _s_OnCalculate_dAMA[iii]
        else:
            iii = _range_end(iii, ama_period, 1)
        SMAdif = Sum / ama_period
        Sum = 0.0
        iii = 0
        for iii in range(iii, ama_period):
            Sum += MathPow(_s_OnCalculate_dAMA[iii] - SMAdif, 2)
        else:
            iii = _range_end(iii, ama_period, 1)
        StDev = MathSqrt(Sum / ama_period)
        _s_OnCalculate_dama = NormalizeDouble(_s_OnCalculate_dAMA[0], Digits() + 2)
        Filter = NormalizeDouble(dK * StDev, Digits() + 2)
        BEARS = 0.0
        BULLS = 0.0
        if _s_OnCalculate_dama < (-Filter):
            BEARS = AMABuffer[bar]
        if _s_OnCalculate_dama > Filter:
            BULLS = AMABuffer[bar]
        BullsBuffer[bar] = BULLS
        BearsBuffer[bar] = BEARS
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_dAMA = Arr(0, 0.0)
_s_OnCalculate_dama = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Amka(_MQL5Indicator):
    name = 'amka'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ama_period': 9,  # Period of AMA
        'fast_ma_period': 2,  # Period of fast MA
        'slow_ma_period': 30,  # Period of slow MA
        'G': 2.0,  # The power the smoothing constant is raised to
        'AMAShift': 0,  # Horizontal shift of the indicator in bars
        'dK': 1.0,  # Coefficient for the filter
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

