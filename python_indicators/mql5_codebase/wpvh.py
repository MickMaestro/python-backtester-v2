"""WPVH — converted from MQL5: MQL5 Indicators/WPVH/WPVH.mq5

Wyckoff PV Histogram oscillator
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 3}, 'colors': {1: [32768], 2: [255], 3: [15570276]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Fast', 2: 'Slow', 3: 'Hist'}, 'levels': [], 'description': ['Wyckoff PV Histogram oscillator'], 'name': 'WPVH', 'source': 'MQL5 Indicators/WPVH/WPVH.mq5', 'folder': 'WPVH', 'inputs': [{'mql': 'InpPeriodFast', 'py': 'InpPeriodFast', 'param': 'InpPeriodFast', 'type': 'uint', 'default': 5, 'label': 'Fast period', 'sinput': False}, {'mql': 'InpPeriodSlow', 'py': 'InpPeriodSlow', 'param': 'InpPeriodSlow', 'type': 'uint', 'default': 15, 'label': 'Slow period', 'sinput': False}, {'mql': 'InpShowHistogram', 'py': 'InpShowHistogram', 'param': 'InpShowHistogram', 'type': 'int', 'default': 0, 'label': 'Show histogram', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriodFast = _input('InpPeriodFast', 5)  # Fast period
InpPeriodSlow = _input('InpPeriodSlow', 15)  # Slow period
InpShowHistogram = _input('InpShowHistogram', INPUT_NO)  # Show histogram
BufferFast = Arr(0, 0.0)
BufferSlow = Arr(0, 0.0)
BufferHist = Arr(0, 0.0)
BufferRAW = Arr(0, 0.0)
period_fast = 0
period_slow = 0

def OnInit():
    global period_fast, period_slow
    period_fast = (1 if (InpPeriodFast < 1) else InpPeriodFast)
    period_slow = (1 if (InpPeriodSlow < 1) else InpPeriodSlow)
    SetIndexBuffer(0, BufferFast, INDICATOR_DATA)
    SetIndexBuffer(1, BufferSlow, INDICATOR_DATA)
    SetIndexBuffer(2, BufferHist, INDICATOR_DATA)
    SetIndexBuffer(3, BufferRAW, INDICATOR_CALCULATIONS)
    IndicatorSetString(INDICATOR_SHORTNAME, 'WPVH (' + _str(period_fast) + ',' + _str(period_slow) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    if InpShowHistogram:
        PlotIndexSetInteger(2, PLOT_DRAW_TYPE, DRAW_HISTOGRAM)
        PlotIndexSetInteger(2, PLOT_SHOW_DATA, True)
    else:
        PlotIndexSetInteger(2, PLOT_DRAW_TYPE, DRAW_NONE)
        PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(BufferFast, True)
    ArraySetAsSeries(BufferSlow, True)
    ArraySetAsSeries(BufferHist, True)
    ArraySetAsSeries(BufferRAW, True)
    ChartRedraw()
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(tick_volume, True)
    if rates_total < 4:
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 2
        ArrayInitialize(BufferFast, EMPTY_VALUE)
        ArrayInitialize(BufferSlow, EMPTY_VALUE)
        ArrayInitialize(BufferHist, EMPTY_VALUE)
        ArrayInitialize(BufferRAW, 0)
    for i in range(limit, 0 - 1, -1):
        UDPC = (True if (close[i] >= (((high[i] - low[i]) / 2.0) + low[i]) and close[i] > close[i + 1]) else False)
        UDNC = (True if (close[i] < (((high[i] - low[i]) / 2.0) + low[i]) and close[i] > close[i + 1]) else False)
        DDPC = (True if (close[i] >= (((high[i] - low[i]) / 2.0) + low[i]) and close[i] < close[i + 1]) else False)
        DDNC = (True if (close[i] < (((high[i] - low[i]) / 2.0) + low[i]) and close[i] < close[i + 1]) else False)
        HVWS = (True if ((high[i] - low[i]) >= (high[i + 1] - low[i + 1]) and tick_volume[i] > tick_volume[i + 1]) else False)
        HVNS = (True if ((high[i] - low[i]) < (high[i + 1] - low[i + 1]) and tick_volume[i] > tick_volume[i + 1]) else False)
        LVWS = (True if ((high[i] - low[i]) >= (high[i + 1] - low[i + 1]) and tick_volume[i] < tick_volume[i + 1]) else False)
        LVNS = (True if ((high[i] - low[i]) < (high[i + 1] - low[i + 1]) and tick_volume[i] < tick_volume[i + 1]) else False)
        BufferRAW[i] = (8 if (UDPC and LVWS) else 7 if (UDPC and HVWS) else 6 if (UDPC and HVNS) else 5 if (UDPC and LVNS) else 4 if (UDNC and LVWS) else 3 if (UDNC and HVWS) else 2 if (UDNC and HVNS) else 1 if (UDNC and LVNS) else -1 if (DDPC and LVNS) else -2 if (DDPC and HVNS) else -3 if (DDPC and HVWS) else -4 if (DDPC and LVWS) else -5 if (DDNC and LVNS) else -6 if (DDNC and HVNS) else -7 if (DDNC and HVWS) else -8 if (DDNC and LVWS) else 0)
        BufferSlow[i] = GetSMA(rates_total, i, period_slow, BufferRAW)
        BufferFast[i] = GetSMA(rates_total, i, period_fast, BufferRAW)
        BufferHist[i] = (EMPTY_VALUE if (not InpShowHistogram) else (BufferRAW[i] - BufferRAW[i + 1]))
    return rates_total

def GetSMA(rates_total, index, period, price, as_series=True):
    result = 0.0
    check_index = ((index <= (rates_total - period - 1)) if as_series else (index >= (period - 1)))
    if period < 1 or (not check_index):
        return 0.0
    for i in range(0, period):
        result = result + (price[index + i] if as_series else price[index - i])
    return _fdiv(result, period)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WPVH(_MQL5Indicator):
    name = 'WPVH'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriodFast': 5,  # Fast period
        'InpPeriodSlow': 15,  # Slow period
        'InpShowHistogram': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Show histogram
    }

