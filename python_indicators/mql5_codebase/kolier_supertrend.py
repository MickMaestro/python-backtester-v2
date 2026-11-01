"""kolier_supertrend — converted from MQL5: MQL5 Indicators/Kolier_SuperTrend/kolier_supertrend.mq5

Copyright: Copyright 2010, KoliEr Li.; Link: http://kolier.li; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2010, KoliEr Li.', 'link': 'http://kolier.li', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [11186720], 2: [9639167], 3: [65280], 4: [255]}, 'widths': {1: 1, 2: 1, 3: 4, 4: 4}, 'styles': {1: 1, 2: 1}, 'labels': {1: 'Upper SuperTrend', 2: 'Lower SuperTrend', 3: 'Buy SuperTrend', 4: 'Sell SuperTrend'}, 'levels': [], 'description': [], 'name': 'kolier_supertrend', 'source': 'MQL5 Indicators/Kolier_SuperTrend/kolier_supertrend.mq5', 'folder': 'Kolier_SuperTrend', 'inputs': [{'mql': 'TrendMode', 'py': 'TrendMode', 'param': 'TrendMode', 'type': 'int', 'default': 1, 'label': 'Display option', 'sinput': False}, {'mql': 'ATR_Period', 'py': 'ATR_Period', 'param': 'ATR_Period', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'ATR_Multiplier', 'py': 'ATR_Multiplier', 'param': 'ATR_Multiplier', 'type': 'double', 'default': 3.0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Mode
SuperTrend = 0
NewWay = 1
Visual = 2
ExpertSignal = 3
_enum('Mode', {0: 'SuperTrend', 1: 'NewWay', 2: 'Visual', 3: 'ExpertSignal'})

# ---- inputs and global variables
TrendMode = _input('TrendMode', NewWay)  # Display option
ATR_Period = _input('ATR_Period', 10)
ATR_Multiplier = _input('ATR_Multiplier', 3.0)
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
        return 1
    min_rates_total = _int(ATR_Period + 3)
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(UpBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(2, PLOT_ARROW, 167)
    SetIndexBuffer(3, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(3, PLOT_ARROW, 167)
    shortname = Box("")
    StringConcatenate(shortname, 'SuperTrend(', ATR_Period, ', ', ATR_Multiplier, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_phase_
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    ATR = Arr(0, 0.0)
    atr = 0.0
    band_upper = 0.0
    band_lower = 0.0
    limit = 0
    to_copy = 0
    bar = 0
    phase = 0
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(ATR, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_phase_ = 0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    phase = _s_OnCalculate_phase_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        mediane = (high[bar] + low[bar]) / 2
        atr = ATR[bar]
        atr *= ATR_Multiplier
        band_upper = mediane + atr
        band_lower = mediane - atr
        UpBuffer[bar] = 0.0
        DnBuffer[bar] = 0.0
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if phase == 0:
            UpBuffer[bar] = mediane
            DnBuffer[bar] = mediane
        if (phase != 1 and close[bar] > DnBuffer[bar + 1]) and DnBuffer[bar + 1]:
            phase = 1
            UpBuffer[bar] = band_lower
            if TrendMode < Visual:
                UpBuffer[bar + 1] = DnBuffer[bar + 1]
            elif TrendMode == Visual:
                DnBuffer[bar] = DnBuffer[bar + 1]
        if (phase != -1 and close[bar] < UpBuffer[bar + 1]) and UpBuffer[bar + 1]:
            phase = -1
            DnBuffer[bar] = band_upper
            if TrendMode < Visual:
                DnBuffer[bar + 1] = UpBuffer[bar + 1]
            elif TrendMode == Visual:
                UpBuffer[bar] = UpBuffer[bar + 1]
        if phase == 1 and ((TrendMode == SuperTrend and UpBuffer[bar + 2]) or TrendMode > SuperTrend):
            if band_lower > UpBuffer[bar + 1] or (UpBuffer[bar] and TrendMode > NewWay):
                UpBuffer[bar] = band_lower
            else:
                UpBuffer[bar] = UpBuffer[bar + 1]
        if phase == -1 and ((TrendMode == SuperTrend and DnBuffer[bar + 2]) or TrendMode > SuperTrend):
            if band_upper < DnBuffer[bar + 1] or (DnBuffer[bar] and TrendMode > NewWay):
                DnBuffer[bar] = band_upper
            else:
                DnBuffer[bar] = DnBuffer[bar + 1]
        if TrendMode != Visual:
            if DnBuffer[bar + 1] and UpBuffer[bar]:
                BuyBuffer[bar] = UpBuffer[bar]
            if UpBuffer[bar + 1] and DnBuffer[bar]:
                SellBuffer[bar] = DnBuffer[bar]
        else:
            if (not UpBuffer[bar + 1]) and UpBuffer[bar]:
                BuyBuffer[bar] = UpBuffer[bar]
            if (not DnBuffer[bar + 1]) and DnBuffer[bar]:
                SellBuffer[bar] = DnBuffer[bar]
        if bar == 1:
            _s_OnCalculate_phase_ = phase
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_phase_ = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KolierSupertrend(_MQL5Indicator):
    name = 'kolier_supertrend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TrendMode': _Choice({0: 'Display as SuperTrend', 1: 'Display as NeWay', 2: 'Display for the visual trading', 3: 'Display for the automated trading'}, default=1),  # Display option
        'ATR_Period': 10,
        'ATR_Multiplier': 3.0,
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

