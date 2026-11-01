"""colorj2jma — converted from MQL5: MQL5 Indicators/J2JMA/colorj2jma.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [8421504, 16711680, 255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'J2JMA'}, 'levels': [], 'description': [], 'name': 'colorj2jma', 'source': 'MQL5 Indicators/J2JMA/colorj2jma.mq5', 'folder': 'J2JMA', 'inputs': [{'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'double', 'default': 5.0, 'label': 'Depth of the first smoothing', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'double', 'default': 5.0, 'label': 'Depth of the second smoothing', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'double', 'default': 100.0, 'label': 'First smoothing parameter,', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'double', 'default': 100.0, 'label': 'Second smoothing parameter,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Vertical shift of the indicator in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
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
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
Length1 = _input('Length1', 5.0)  # Depth of the first smoothing
Length2 = _input('Length2', 5.0)  # Depth of the second smoothing
Phase1 = _input('Phase1', 100.0)  # First smoothing parameter,
Phase2 = _input('Phase2', 100.0)  # Second smoothing parameter,
IPC = _input('IPC', PRICE_CLOSE_)  # Price constant
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # Vertical shift of the indicator in points
J2JMA = Arr(0, 0.0)
ColorJ2JMA = Arr(0, 0.0)
dPriceShift = 0.0

def OnInit():
    global dPriceShift
    SetIndexBuffer(0, J2JMA, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, 62)
    PlotIndexSetString(0, PLOT_LABEL, 'J2JMA')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ColorJ2JMA, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, 62)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    shortname = Box("")
    StringConcatenate(shortname, 'J2JMA( Length1 = ', Length1, ', Length2 = ', Length2, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    JMA = CJJMA()
    JMA.JJMALengthCheck('Length1', _int(Length1))
    JMA.JJMALengthCheck('Length2', _int(Length2))
    JMA.JJMAPhaseCheck('Phase1', _int(Phase1))
    JMA.JJMAPhaseCheck('Phase2', _int(Phase2))
    dPriceShift = Point() * PriceShift

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < 60:
        return 0
    price_ = 0.0
    j1jma = 0.0
    j2jma = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        j1jma = _s_OnCalculate_JMA1.JJMASeries(0, prev_calculated, rates_total, 0, Phase1, Length1, price_, bar, False)
        j2jma = _s_OnCalculate_JMA2.JJMASeries(30, prev_calculated, rates_total, 0, Phase2, Length2, j1jma, bar, False)
        J2JMA[bar] = j2jma + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        ColorJ2JMA[bar] = 0.0
        if J2JMA[bar - 1] < J2JMA[bar]:
            ColorJ2JMA[bar] = 1.0
        if J2JMA[bar - 1] > J2JMA[bar]:
            ColorJ2JMA[bar] = 2.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_JMA1 = CJJMA()
_s_OnCalculate_JMA2 = CJJMA()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorj2jma(_MQL5Indicator):
    name = 'colorj2jma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length1': 5.0,  # Depth of the first smoothing
        'Length2': 5.0,  # Depth of the second smoothing
        'Phase1': 100.0,  # First smoothing parameter,
        'Phase2': 100.0,  # Second smoothing parameter,
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'}, default=1),  # Price constant
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'PriceShift': 0,  # Vertical shift of the indicator in points
    }

