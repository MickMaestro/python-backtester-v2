"""trendtriggermod — converted from MQL5: MQL5 Indicators/TrendTriggerMod/trendtriggermod.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [8421504, 16711935, 8388352]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'Trend Trigger Mod'}, 'levels': [], 'description': [], 'name': 'trendtriggermod', 'source': 'MQL5 Indicators/TrendTriggerMod/trendtriggermod.mq5', 'folder': 'TrendTriggerMod', 'inputs': [{'mql': 'Regress', 'py': 'Regress', 'param': 'Regress', 'type': 'uint', 'default': 15, 'label': 'Extremums searching period', 'sinput': False}, {'mql': 'TLength', 'py': 'TLength', 'param': 'TLength', 'type': 'uint', 'default': 5, 'label': 'JMA smoothing depth', 'sinput': False}, {'mql': 'TPhase', 'py': 'TPhase', 'param': 'TPhase', 'type': 'int', 'default': -100, 'label': 'JMA smoothing parameter', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'UpTriggerLevel', 'py': 'UpTriggerLevel', 'param': 'UpTriggerLevel', 'type': 'int', 'default': 50, 'label': 'Overbought level', 'sinput': False}, {'mql': 'DnTriggerLevel', 'py': 'DnTriggerLevel', 'param': 'DnTriggerLevel', 'type': 'int', 'default': -50, 'label': 'Oversold level', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

Blue = 0xFF0000  # MQL4 colour name
Brown = 0x2A2AA5  # MQL4 colour name

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
Regress = _input('Regress', 15)  # Extremums searching period
TLength = _input('TLength', 5)  # JMA smoothing depth
TPhase = _input('TPhase', -100)  # JMA smoothing parameter
IPC = _input('IPC', PRICE_CLOSE_)  # Applied price
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
UpTriggerLevel = _input('UpTriggerLevel', 50)  # Overbought level
DnTriggerLevel = _input('DnTriggerLevel', -50)  # Oversold level
ExtLineBuffer = Arr(0, 0.0)
ColorExtLineBuffer = Arr(0, 0.0)
min_rates_r = 0
min_rates_total = 0

def OnInit():
    global min_rates_r, min_rates_total
    min_rates_r = _int(Regress + Regress + 1)
    min_rates_total = min_rates_r + 30
    SetIndexBuffer(0, ExtLineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(ExtLineBuffer, True)
    SetIndexBuffer(1, ColorExtLineBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ColorExtLineBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'Trend Trigger Mod(', TLength, ' ,', TPhase, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    JMA = CJJMA()
    JMA.JJMALengthCheck('TLength', TLength)
    JMA.JJMAPhaseCheck('TPhase', TPhase)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, UpTriggerLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, DnTriggerLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, 0)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, Blue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, Blue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, Brown)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    maxbar = 0
    HHR = 0.0
    LLR = 0.0
    HHO = 0.0
    LLO = 0.0
    BuyPower = 0.0
    SellPower = 0.0
    TTF = 0.0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    maxbar = rates_total - min_rates_r - 1
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_r - 1
    else:
        limit = rates_total - prev_calculated
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        HHR = high[ArrayMaximum(high, bar, Regress)]
        HHO = high[ArrayMaximum(high, bar + Regress, Regress)]
        LLR = low[ArrayMinimum(low, bar, Regress)]
        LLO = low[ArrayMinimum(low, bar + Regress, Regress)]
        BuyPower = HHR - LLO
        SellPower = HHO - LLR
        TTF = _fdiv(100 * (BuyPower - SellPower) * 2, BuyPower + SellPower)
        ExtLineBuffer[bar] = _s_OnCalculate_JMA.JJMASeries(maxbar, prev_calculated, rates_total, 0, TPhase, TLength, TTF, bar, True)
        ColorExtLineBuffer[bar] = 0.0
        if ExtLineBuffer[bar] > UpTriggerLevel:
            ColorExtLineBuffer[bar] = 2.0
        if ExtLineBuffer[bar] < DnTriggerLevel:
            ColorExtLineBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_JMA = CJJMA()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Trendtriggermod(_MQL5Indicator):
    name = 'trendtriggermod'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Regress': 15,  # Extremums searching period
        'TLength': 5,  # JMA smoothing depth
        'TPhase': -100,  # JMA smoothing parameter
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Applied price
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'UpTriggerLevel': 50,  # Overbought level
        'DnTriggerLevel': -50,  # Oversold level
    }

