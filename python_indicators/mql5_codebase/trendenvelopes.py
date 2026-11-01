"""trendenvelopes — converted from MQL5: MQL5 Indicators/TrendEnvelopes/trendenvelopes.mq5

Copyright: Copyright © 2006, TrendLaboratory Ltd.; Link: http://finance.groups.yahoo.com/group/TrendLaboratory; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, TrendLaboratory Ltd.', 'link': 'http://finance.groups.yahoo.com/group/TrendLaboratory', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 5, 4: 5}, 'colors': {1: [16711680], 2: [255], 3: [16760576], 4: [255]}, 'widths': {1: 2, 2: 2, 3: 4, 4: 4}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Upper TrendEnvelopes', 2: 'Lower TrendEnvelopes', 3: 'Buy TrendEnvelopes', 4: 'Sell TrendEnvelopes'}, 'levels': [], 'description': [], 'name': 'trendenvelopes', 'source': 'MQL5 Indicators/TrendEnvelopes/trendenvelopes.mq5', 'folder': 'TrendEnvelopes', 'inputs': [{'mql': 'MA_Period', 'py': 'MA_Period', 'param': 'MA_Period', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Applied_Price', 'py': 'Applied_Price', 'param': 'Applied_Price', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'Deviation_', 'py': 'Deviation_', 'param': 'Deviation_', 'type': 'double', 'default': 0.2, 'label': '', 'sinput': False}, {'mql': 'ATRPeriod', 'py': 'ATRPeriod', 'param': 'ATRPeriod', 'type': 'uint', 'default': 15, 'label': 'ATR indicator period', 'sinput': False}, {'mql': 'ATRSensitivity', 'py': 'ATRSensitivity', 'param': 'ATRSensitivity', 'type': 'double', 'default': 0.5, 'label': 'ATR shift sensitivity', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
MA_Period = _input('MA_Period', 14)
MA_Method = _input('MA_Method', MODE_EMA)
Applied_Price = _input('Applied_Price', PRICE_CLOSE)
Deviation_ = _input('Deviation_', 0.2)
ATRPeriod = _input('ATRPeriod', 15)  # ATR indicator period
ATRSensitivity = _input('ATRSensitivity', 0.5)  # ATR shift sensitivity
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
ExtMapBufferUp = Arr(0, 0.0)
ExtMapBufferDown = Arr(0, 0.0)
ExtMapBufferUp1 = Arr(0, 0.0)
ExtMapBufferDown1 = Arr(0, 0.0)
Deviation = 0.0
ATR_Handle = 0
MA_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, Deviation, MA_Handle, min_rates_total
    ATR_Handle = iATR(None, 0, ATRPeriod)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
        return 1
    MA_Handle = iMA(None, 0, MA_Period, 0, MA_Method, Applied_Price)
    if MA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
        return 1
    min_rates_total = _int(MathMax(ATRPeriod, MA_Period) + 1)
    Deviation = MathMax(Deviation_, 0.1)
    Deviation = MathMin(Deviation_, 100.0)
    SetIndexBuffer(0, ExtMapBufferUp, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferUp, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, ExtMapBufferDown, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferDown, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, ExtMapBufferUp1, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferUp1, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    SetIndexBuffer(3, ExtMapBufferDown1, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtMapBufferDown1, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TrendEnvelopes')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_smax, _s_OnCalculate_prev_smin, _s_OnCalculate_prev_trend
    if (BarsCalculated(ATR_Handle) < rates_total or BarsCalculated(MA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    trend = 0
    ATR = Arr(0, 0.0)
    MA = Arr(0, 0.0)
    smax = 0.0
    smin = 0.0
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(MA, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_prev_smax = 0.0
        _s_OnCalculate_prev_smin = 999999999.9
        _s_OnCalculate_prev_trend = 0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MA) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtMapBufferUp[bar] = EMPTY_VALUE
        ExtMapBufferDown[bar] = EMPTY_VALUE
        ExtMapBufferUp1[bar] = EMPTY_VALUE
        ExtMapBufferDown1[bar] = EMPTY_VALUE
        smax = (1 + (Deviation / 100)) * MA[bar]
        smin = (1 - (Deviation / 100)) * MA[bar]
        trend = _s_OnCalculate_prev_trend
        if close[bar] > _s_OnCalculate_prev_smax:
            trend = 1
        if close[bar] < _s_OnCalculate_prev_smin:
            trend = -1
        if trend > 0:
            if smin < _s_OnCalculate_prev_smin:
                smin = _s_OnCalculate_prev_smin
            ExtMapBufferUp[bar] = smin
            if _s_OnCalculate_prev_trend < 0:
                ExtMapBufferUp1[bar] = smin - (ATRSensitivity * ATR[bar])
        else:
            if smax > _s_OnCalculate_prev_smax:
                smax = _s_OnCalculate_prev_smax
            ExtMapBufferDown[bar] = smax
            if _s_OnCalculate_prev_trend > 0:
                ExtMapBufferDown1[bar] = smax + (ATRSensitivity * ATR[bar])
        if bar > 0:
            _s_OnCalculate_prev_smax = smax
            _s_OnCalculate_prev_smin = smin
            _s_OnCalculate_prev_trend = trend
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_prev_smax = 0.0
_s_OnCalculate_prev_smin = 0.0
_s_OnCalculate_prev_trend = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Trendenvelopes(_MQL5Indicator):
    name = 'trendenvelopes'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Period': 14,
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),
        'Applied_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'Deviation_': 0.2,
        'ATRPeriod': 15,  # ATR indicator period
        'ATRSensitivity': 0.5,  # ATR shift sensitivity
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

