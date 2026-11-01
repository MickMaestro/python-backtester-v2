"""ChandelierExit_Candle — converted from MQL5: MQL5 Indicators/ChandelierExit_Candle/ChandelierExit_Candle.mq5

Copyright: Copyright © 2009, MQLService; Link: scripts@mqlservice.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, MQLService', 'link': 'scripts@mqlservice.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16711935, 2763429, 2263842, 13749760]}, 'widths': {}, 'styles': {}, 'labels': {1: 'ChandelierExitOpen;ChandelierExitHigh;ChandelierExitLow;ChandelierExitClose'}, 'levels': [], 'description': [], 'name': 'ChandelierExit_Candle', 'source': 'MQL5 Indicators/ChandelierExit_Candle/ChandelierExit_Candle.mq5', 'folder': 'ChandelierExit_Candle', 'inputs': [{'mql': 'RangePeriod', 'py': 'RangePeriod', 'param': 'RangePeriod', 'type': 'int', 'default': 15, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'ATRPeriod', 'py': 'ATRPeriod', 'param': 'ATRPeriod', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'MultipleATR', 'py': 'MultipleATR', 'param': 'MultipleATR', 'type': 'int', 'default': 4, 'label': '', 'sinput': False}, {'mql': 'PriceMode', 'py': 'PriceMode', 'param': 'PriceMode', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_PRICE_MODE
CLOSE_CLOSE = 1
HIGH_LOW = 2
_enum('ENUM_PRICE_MODE', {1: 'CLOSE_CLOSE', 2: 'HIGH_LOW'})

# ---- inputs and global variables
RangePeriod = _input('RangePeriod', 15)
Shift = _input('Shift', 1)
ATRPeriod = _input('ATRPeriod', 14)
MultipleATR = _input('MultipleATR', 4)
PriceMode = _input('PriceMode', CLOSE_CLOSE)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_total
    min_rates_total = MathMax(ATRPeriod, RangePeriod + Shift)
    ATR_Handle = iATR(None, 0, ATRPeriod)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'ChandelierExit(', RangePeriod, ', ', ATRPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_HH1, _s_OnCalculate_LL1, _s_OnCalculate_direction
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    ATR = Arr(0, 0.0)
    HH0 = 0.0
    LL0 = 0.0
    hi = 0.0
    lo = 0.0
    stop = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
        _s_OnCalculate_direction = 0
        _s_OnCalculate_HH1 = 0.0
        _s_OnCalculate_LL1 = 999999999.0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtOpenBuffer[bar] = open[bar]
        ExtHighBuffer[bar] = high[bar]
        ExtLowBuffer[bar] = low[bar]
        ExtCloseBuffer[bar] = close[bar]
        ATR[bar] *= MultipleATR
        HH0 = high[ArrayMaximum(high, bar + Shift, RangePeriod)] - ATR[bar]
        LL0 = low[ArrayMinimum(low, bar + Shift, RangePeriod)] + ATR[bar]
        stop = close[bar]
        if PriceMode == CLOSE_CLOSE:
            hi = close[bar + 1]
            lo = close[bar + 1]
        else:
            hi = high[bar + 1]
            lo = low[bar + 1]
        if _s_OnCalculate_direction >= 0:
            if hi < _s_OnCalculate_HH1:
                if bar:
                    _s_OnCalculate_direction = -1
                stop = LL0
            else:
                stop = HH0
        elif _s_OnCalculate_direction <= 0:
            if lo > _s_OnCalculate_LL1:
                if bar:
                    _s_OnCalculate_direction = 1
                stop = HH0
            else:
                stop = LL0
        if stop <= close[bar]:
            if close[bar] >= open[bar]:
                ExtColorBuffer[bar] = 3.0
            else:
                ExtColorBuffer[bar] = 2.0
        if stop >= close[bar]:
            if close[bar] <= open[bar]:
                ExtColorBuffer[bar] = 0.0
            else:
                ExtColorBuffer[bar] = 1.0
        if bar:
            _s_OnCalculate_HH1 = HH0
            _s_OnCalculate_LL1 = LL0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_direction = 0
_s_OnCalculate_HH1 = 0.0
_s_OnCalculate_LL1 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ChandelierExitCandle(_MQL5Indicator):
    name = 'ChandelierExit_Candle'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RangePeriod': 15,
        'Shift': 1,
        'ATRPeriod': 14,
        'MultipleATR': 4,
        'PriceMode': _Choice({1: 'Close/Close', 2: 'High/low'}, default=1),
    }

