"""ATR_Volatility — converted from MQL5: MQL5 Indicators/ATR_Volatility/ATR_Volatility.mq5

ATR Volatility oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 10}, 'colors': {1: [32768, 255, 16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'AATR'}, 'levels': [], 'description': ['ATR Volatility oscillator'], 'name': 'ATR_Volatility', 'source': 'MQL5 Indicators/ATR_Volatility/ATR_Volatility.mq5', 'folder': 'ATR_Volatility', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 12, 'label': 'ATR period', 'sinput': False}, {'mql': 'InpLevelH', 'py': 'InpLevelH', 'param': 'InpLevelH', 'type': 'double', 'default': 300.0, 'label': 'Higher level', 'sinput': False}, {'mql': 'InpLevelL', 'py': 'InpLevelL', 'param': 'InpLevelL', 'type': 'double', 'default': 200.0, 'label': 'Lower level', 'sinput': False}, {'mql': 'InpMode', 'py': 'InpMode', 'param': 'InpMode', 'type': 'int', 'default': 0, 'label': 'Calculation mode', 'sinput': False}, {'mql': 'InpMaxBars', 'py': 'InpMaxBars', 'param': 'InpMaxBars', 'type': 'uint', 'default': 1000, 'label': 'Maximum bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_MODE
MODE_POINTS = 0
MODE_PERCENT = 1
_enum('ENUM_MODE', {0: 'MODE_POINTS', 1: 'MODE_PERCENT'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 12)  # ATR period
InpLevelH = _input('InpLevelH', 300.0)  # Higher level
InpLevelL = _input('InpLevelL', 200.0)  # Lower level
InpMode = _input('InpMode', MODE_POINTS)  # Calculation mode
InpMaxBars = _input('InpMaxBars', _uint(1000.0))  # Maximum bars
BufferAATR = Arr(0, 0.0)
BufferColors = Arr(0, 0.0)
level_h = 0.0
level_l = 0.0
last_top = 0.0
last_bottom = 0.0
period_atr = 0
max_bars = 0
handle_atr = 0

def OnInit():
    global handle_atr, last_bottom, last_top, level_h, level_l, period_atr
    period_atr = (1 if (InpPeriod < 1) else InpPeriod)
    level_h = InpLevelH
    level_l = InpLevelL
    last_top = 0.0
    last_bottom = 0.0
    SetIndexBuffer(0, BufferAATR, INDICATOR_DATA)
    SetIndexBuffer(1, BufferColors, INDICATOR_COLOR_INDEX)
    pf = ('%' if (InpMode == MODE_PERCENT) else '')
    IndicatorSetString(INDICATOR_SHORTNAME, 'ATR Volatility (' + _str(period_atr) + ',' + DoubleToString(level_h, 1) + pf + ',' + DoubleToString(level_l, 1) + pf + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_LEVELS, 2)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrDodgerBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrOrangeRed)
    ArraySetAsSeries(BufferAATR, True)
    ArraySetAsSeries(BufferColors, True)
    ResetLastError()
    handle_atr = iATR(None, PERIOD_CURRENT, period_atr)
    if handle_atr == INVALID_HANDLE:
        Print('The iATR(', _str(period_atr), ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global last_bottom, last_top
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if rates_total < 4 or Point() == 0:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferAATR, EMPTY_VALUE)
    count = (rates_total if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_atr, 0, 0, count, BufferAATR)
    if copied != count:
        return 0
    bars = rates_total - period_atr - 1
    count_bars = (bars if (InpMaxBars == 0) else bars if (_int(InpMaxBars) > bars) else InpMaxBars)
    bl = ArrayMinimum(BufferAATR, 0, count_bars)
    bh = ArrayMaximum(BufferAATR, 0, count_bars)
    if bl == WRONG_VALUE or bh == WRONG_VALUE:
        return 0
    min_ = BufferAATR[bl]
    max_ = BufferAATR[bh]
    top = 0.0
    bottom = 0.0
    percentage = 0.0
    if InpMode == MODE_POINTS:
        top = level_h * Point()
        bottom = level_l * Point()
    else:
        percentage = (max_ - min_) / 100.0
        top = min_ + (level_h * percentage)
        bottom = min_ + (level_l * percentage)
    if last_top != top:
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, top)
        last_top = top
    if last_bottom != bottom:
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, bottom)
        last_bottom = bottom
    for i in range(limit, 0 - 1, -1):
        BufferColors[i] = (0 if (BufferAATR[i] > top) else 1 if (BufferAATR[i] < bottom) else 2)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ATRVolatility(_MQL5Indicator):
    name = 'ATR_Volatility'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 12,  # ATR period
        'InpLevelH': 300.0,  # Higher level
        'InpLevelL': 200.0,  # Lower level
        'InpMode': _Choice({0: 'In points', 1: 'In percents'}, default=0),  # Calculation mode
        'InpMaxBars': 1000,  # Maximum bars
    }

