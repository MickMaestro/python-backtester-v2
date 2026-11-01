"""chandelexit — converted from MQL5: MQL5 Indicators/ChandelExit_HTF/chandelexit.mq5

Copyright: MQLService; Link: scripts@mqlservice.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'MQLService', 'link': 'scripts@mqlservice.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [15631086, 65280]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'UpLoss Line'}, 'levels': [], 'description': [], 'name': 'chandelexit', 'source': 'MQL5 Indicators/ChandelExit_HTF/chandelexit.mq5', 'folder': 'ChandelExit_HTF', 'inputs': [{'mql': 'RangePeriod', 'py': 'RangePeriod', 'param': 'RangePeriod', 'type': 'int', 'default': 15, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'ATRPeriod', 'py': 'ATRPeriod', 'param': 'ATRPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'MultipleATR', 'py': 'MultipleATR', 'param': 'MultipleATR', 'type': 'int', 'default': 4, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RangePeriod = _input('RangePeriod', 15)
Shift = _input('Shift', 1)
ATRPeriod = _input('ATRPeriod', 14)
MultipleATR = _input('MultipleATR', 4)
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_total
    min_rates_total = MathMax(ATRPeriod, RangePeriod + Shift)
    ATR_Handle = iATR(None, 0, ATRPeriod)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(1, DnBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    shortname = Box("")
    StringConcatenate(shortname, 'ChandelExit(', RangePeriod, ', ', ATRPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_direction
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    ATR = Arr(0, 0.0)
    HH0 = 0.0
    LL0 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
        _s_OnCalculate_direction = 0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ATR[bar] *= MultipleATR
        HH0 = high[ArrayMaximum(high, bar + Shift, RangePeriod)] - ATR[bar]
        LL0 = low[ArrayMinimum(low, bar + Shift, RangePeriod)] + ATR[bar]
        if _s_OnCalculate_direction >= 0:
            if close[bar] < HH0:
                if bar:
                    _s_OnCalculate_direction = -1
                UpBuffer[bar] = LL0
                DnBuffer[bar] = HH0
            else:
                UpBuffer[bar] = HH0
                DnBuffer[bar] = LL0
        elif _s_OnCalculate_direction <= 0:
            if close[bar] > LL0:
                if bar:
                    _s_OnCalculate_direction = 1
                DnBuffer[bar] = LL0
                UpBuffer[bar] = HH0
            else:
                UpBuffer[bar] = LL0
                DnBuffer[bar] = HH0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_direction = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Chandelexit(_MQL5Indicator):
    name = 'chandelexit'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RangePeriod': 15,
        'Shift': 1,
        'ATRPeriod': 14,
        'MultipleATR': 4,
    }

