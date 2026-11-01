"""chandelexitsign — converted from MQL5: MQL5 Indicators/ChandelExitSign/chandelexitsign.mq5

Copyright: MQLService; Link: scripts@mqlservice.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'MQLService', 'link': 'scripts@mqlservice.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'BullsBears Sell', 2: 'BullsBears Buy'}, 'levels': [], 'description': [], 'name': 'chandelexitsign', 'source': 'MQL5 Indicators/ChandelExitSign/chandelexitsign.mq5', 'folder': 'ChandelExitSign', 'inputs': [{'mql': 'RangePeriod', 'py': 'RangePeriod', 'param': 'RangePeriod', 'type': 'uint', 'default': 15, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'uint', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'ATRPeriod', 'py': 'ATRPeriod', 'param': 'ATRPeriod', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'MultipleATR', 'py': 'MultipleATR', 'param': 'MultipleATR', 'type': 'uint', 'default': 4, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RangePeriod = _input('RangePeriod', 15)
Shift = _input('Shift', 1)
ATRPeriod = _input('ATRPeriod', 14)
MultipleATR = _input('MultipleATR', 4)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
ATR1_Handle = 0
ATR2_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR1_Handle, ATR2_Handle, min_rates_total
    ATR2Period = 12
    min_rates_total = _int(MathMax(MathMax(ATRPeriod, RangePeriod + Shift) + 1, ATR2Period))
    ATR1_Handle = iATR(None, 0, ATRPeriod)
    if ATR1_Handle == INVALID_HANDLE:
        Print('Не удалось получить хендл индикатора ATR1')
        return INIT_FAILED
    ATR2_Handle = iATR(None, 0, ATR2Period)
    if ATR2_Handle == INVALID_HANDLE:
        Print('Не удалось получить хендл индикатора ATR2')
        return INIT_FAILED
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 163)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 163)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    ArraySetAsSeries(BuyBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'ChandelExit(', RangePeriod, ', ', ATRPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Dn1, _s_OnCalculate_Up1, _s_OnCalculate_direction
    if (BarsCalculated(ATR1_Handle) < rates_total or BarsCalculated(ATR2_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    ATR1 = Arr(0, 0.0)
    ATR2 = Arr(0, 0.0)
    HH0 = 0.0
    LL0 = 0.0
    Up = 0.0
    Dn = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
        _s_OnCalculate_direction = 0
        _s_OnCalculate_Up1 = 0.0
        Up = _s_OnCalculate_Up1
        _s_OnCalculate_Dn1 = 0.0
        Dn = _s_OnCalculate_Dn1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR1_Handle, 0, 0, to_copy, ATR1) <= 0:
        return 0
    if CopyBuffer(ATR2_Handle, 0, 0, to_copy, ATR2) <= 0:
        return 0
    ArraySetAsSeries(ATR1, True)
    ArraySetAsSeries(ATR2, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ATR1[bar] *= MultipleATR
        HH0 = high[ArrayMaximum(high, bar + Shift, RangePeriod)] - ATR1[bar]
        LL0 = low[ArrayMinimum(low, bar + Shift, RangePeriod)] + ATR1[bar]
        if _s_OnCalculate_direction >= 0:
            if close[bar] < HH0:
                if bar:
                    _s_OnCalculate_direction = -1
                Up = LL0
                Dn = HH0
            else:
                Up = HH0
                Dn = LL0
        elif _s_OnCalculate_direction <= 0:
            if close[bar] > LL0:
                if bar:
                    _s_OnCalculate_direction = 1
                Dn = LL0
                Up = HH0
            else:
                Up = LL0
                Dn = HH0
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        if _s_OnCalculate_Dn1 <= _s_OnCalculate_Up1 and Dn > Up:
            BuyBuffer[bar] = low[bar] - ((ATR1[bar] * 3) / 8)
        if _s_OnCalculate_Dn1 >= _s_OnCalculate_Up1 and Dn < Up:
            SellBuffer[bar] = high[bar] + ((ATR1[bar] * 3) / 8)
        if bar:
            _s_OnCalculate_Up1 = Up
            _s_OnCalculate_Dn1 = Dn
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_direction = 0
_s_OnCalculate_Up1 = 0.0
_s_OnCalculate_Dn1 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Chandelexitsign(_MQL5Indicator):
    name = 'chandelexitsign'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RangePeriod': 15,
        'Shift': 1,
        'ATRPeriod': 14,
        'MultipleATR': 4,
    }

