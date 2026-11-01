"""sfx_tor — converted from MQL5: MQL5 Indicators/SFX_TOR_HTF/sfx_tor.mq5

Copyright: Copyright © 2007, MetaQuotes Software Corp.; Link: http://www.metaquotes.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [3329330], 2: [16711935], 3: [16748574]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'ATR', 2: 'StdDev', 3: 'StdDev MA'}, 'levels': [], 'description': [], 'name': 'sfx_tor', 'source': 'MQL5 Indicators/SFX_TOR_HTF/sfx_tor.mq5', 'folder': 'SFX_TOR_HTF', 'inputs': [{'mql': 'ATR_period', 'py': 'ATR_period', 'param': 'ATR_period', 'type': 'uint', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'Std_period', 'py': 'Std_period', 'param': 'Std_period', 'type': 'uint', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'Std_method', 'py': 'Std_method', 'param': 'Std_method', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Std_price', 'py': 'Std_price', 'param': 'Std_price', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MAPeriod', 'py': 'MAPeriod', 'param': 'MAPeriod', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'MAType', 'py': 'MAType', 'param': 'MAType', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ATR_period = _input('ATR_period', 12)
Std_period = _input('Std_period', 12)
Std_method = _input('Std_method', MODE_EMA)
Std_price = _input('Std_price', PRICE_CLOSE)
MAPeriod = _input('MAPeriod', 3)
MAType = _input('MAType', MODE_SMMA)
ATRBuffer = Arr(0, 0.0)
StdBuffer = Arr(0, 0.0)
MABuffer = Arr(0, 0.0)
ATR_Handle = 0
Std_Handle = 0
MA_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, MA_Handle, Std_Handle, min_rates_total
    ATR_Handle = iATR(None, PERIOD_CURRENT, ATR_period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    Std_Handle = iStdDev(None, 0, Std_period, 0, Std_method, Std_price)
    if Std_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iStdDev')
        return INIT_FAILED
    MA_Handle = iMA(None, 0, MAPeriod, 0, MAType, Std_Handle)
    if MA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    min_rates_total = _int(MathMax(ATR_period, Std_period + MAPeriod))
    SetIndexBuffer(0, ATRBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ATRBuffer, True)
    SetIndexBuffer(1, StdBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(StdBuffer, True)
    SetIndexBuffer(2, MABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(MABuffer, True)
    shortname = 'SFX_TOR'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((BarsCalculated(ATR_Handle) < rates_total or BarsCalculated(Std_Handle) < rates_total) or BarsCalculated(MA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATRBuffer) <= 0:
        return 0
    if CopyBuffer(Std_Handle, 0, 0, to_copy, StdBuffer) <= 0:
        return 0
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MABuffer) <= 0:
        return 0
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SfxTor(_MQL5Indicator):
    name = 'sfx_tor'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ATR_period': 12,
        'Std_period': 12,
        'Std_method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'Std_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'MAPeriod': 3,
        'MAType': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=2),
    }

