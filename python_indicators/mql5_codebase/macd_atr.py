"""macd_atr — converted from MQL5: MQL5 Indicators/iMACD±ATR/macd_atr.mq5

Copyright: Copyright © 2011, Svinozavr; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Svinozavr', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 10, 2: 1}, 'colors': {1: [8421504, 255, 65280], 2: [16711680]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'MACD', 2: 'ATR Line'}, 'levels': [], 'description': [], 'name': 'macd_atr', 'source': 'MQL5 Indicators/iMACD±ATR/macd_atr.mq5', 'folder': 'iMACD±ATR', 'inputs': [{'mql': 'FastEMA', 'py': 'FastEMA', 'param': 'FastEMA', 'type': 'uint', 'default': 12, 'label': 'Fast EMA period;', 'sinput': False}, {'mql': 'SlowEMA', 'py': 'SlowEMA', 'param': 'SlowEMA', 'type': 'uint', 'default': 26, 'label': 'Slow EMA period;', 'sinput': False}, {'mql': 'ATR_', 'py': 'ATR_', 'param': 'ATR_', 'type': 'int', 'default': 0, 'label': 'ATR period, if =0, then ATR=SlowEMA', 'sinput': False}, {'mql': 'AppliedPrice', 'py': 'AppliedPrice', 'param': 'AppliedPrice', 'type': 'int', 'default': 1, 'label': 'price constant', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FastEMA = _input('FastEMA', 12)  # Fast EMA period;
SlowEMA = _input('SlowEMA', 26)  # Slow EMA period;
ATR_ = _input('ATR_', 0)  # ATR period, if =0, then ATR=SlowEMA
AppliedPrice = _input('AppliedPrice', PRICE_CLOSE)  # price constant
ATRmin = 0.0  # noise threshold ??of ATR value in pp.
kATR = 1.0  # Scaling factor
min_rates_total = 0
ATR_Handle = 0
MACD_Handle = 0
MACDBuffer = Arr(0, 0.0)
ATRBuffer = Arr(0, 0.0)
ColorMACDBuffer = Arr(0, 0.0)

def OnInit():
    global ATR_Handle, ATRmin, MACD_Handle, min_rates_total
    if ATR_:
        min_rates_total = _int(MathMax(FastEMA, SlowEMA) + ATR_)
    else:
        min_rates_total = 2 * _int(MathMax(FastEMA, SlowEMA))
    ATR = 0
    if not ATR_:
        ATR = _int(SlowEMA)
    else:
        ATR = ATR_
    ATRmin *= Point()
    ATR_Handle = iATR(None, 0, ATR)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
    MACD_Handle = iMACD(None, 0, FastEMA, SlowEMA, 3, AppliedPrice)
    if MACD_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the MACD indicator')
    SetIndexBuffer(0, MACDBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(MACDBuffer, True)
    SetIndexBuffer(1, ColorMACDBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ColorMACDBuffer, True)
    SetIndexBuffer(2, ATRBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ATRBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'MACD(', FastEMA, ', ', SlowEMA, ', ', ATR, ', ', EnumToString(AppliedPrice, 'ENUM_APPLIED_PRICE'), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (rates_total < min_rates_total or BarsCalculated(ATR_Handle) < min_rates_total) or BarsCalculated(MACD_Handle) < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    atr = 0.0
    Atr = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(Atr, True)
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, Atr) <= 0:
        return 0
    if CopyBuffer(MACD_Handle, MAIN_LINE, 0, to_copy, MACDBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ColorMACDBuffer[bar] = 0.0
        atr = kATR * Atr[bar]
        atr = MathMax(atr, ATRmin)
        if MACDBuffer[bar] > 0:
            ATRBuffer[bar] = MACDBuffer[bar] - atr
        if MACDBuffer[bar] < 0:
            ATRBuffer[bar] = MACDBuffer[bar] + atr
        if (MACDBuffer[bar] > 0 and MACDBuffer[bar + 1] < MACDBuffer[bar]) and ATRBuffer[bar] >= 0:
            ColorMACDBuffer[bar] = 2.0
        if (MACDBuffer[bar] < 0 and MACDBuffer[bar + 1] > MACDBuffer[bar]) and ATRBuffer[bar] <= 0:
            ColorMACDBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MacdAtr(_MQL5Indicator):
    name = 'macd_atr'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastEMA': 12,  # Fast EMA period;
        'SlowEMA': 26,  # Slow EMA period;
        'ATR_': 0,  # ATR period, if =0, then ATR=SlowEMA
        'AppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # price constant
    }

