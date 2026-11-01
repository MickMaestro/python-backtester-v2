"""multitrend_signal_kvn — converted from MQL5: MQL5 Indicators/MultiTrend_Signal_KVN/multitrend_signal_kvn.mq5

Copyright: Copyright © 2007, Vladimir Korykin; Link: koryvladimir@inbox.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Vladimir Korykin', 'link': 'koryvladimir@inbox.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [8421376], 2: [16711935]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 4, 2: 4}, 'labels': {1: 'Buy MultiTrend_Signal_KVN', 2: 'Sell MultiTrend_Signal_KVN'}, 'levels': [], 'description': [], 'name': 'multitrend_signal_kvn', 'source': 'MQL5 Indicators/MultiTrend_Signal_KVN/multitrend_signal_kvn.mq5', 'folder': 'MultiTrend_Signal_KVN', 'inputs': [{'mql': 'K', 'py': 'K', 'param': 'K', 'type': 'uint', 'default': 48, 'label': '', 'sinput': False}, {'mql': 'Kstop', 'py': 'Kstop', 'param': 'Kstop', 'type': 'double', 'default': 0.5, 'label': '', 'sinput': False}, {'mql': 'Kperiod', 'py': 'Kperiod', 'param': 'Kperiod', 'type': 'uint', 'default': 150, 'label': '', 'sinput': False}, {'mql': 'PerADX', 'py': 'PerADX', 'param': 'PerADX', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
K = _input('K', 48)
Kstop = _input('Kstop', 0.5)
Kperiod = _input('Kperiod', 150)
PerADX = _input('PerADX', 14)
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
BuyBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
K100 = 0.0
ADX_Handle = 0
min_rates_total = 0

def OnInit():
    global ADX_Handle, K100, min_rates_total
    min_rates_total = _int(Kperiod + PerADX + 1)
    K100 = _idiv(K, 50)
    ADX_Handle = iADX(None, PERIOD_CURRENT, PerADX)
    if ADX_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iADX indicator')
    SetIndexBuffer(0, BuyBuffer, INDICATOR_DATA)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_ARROW, 217)
    SetIndexBuffer(1, SellBuffer, INDICATOR_DATA)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_ARROW, 218)
    IndicatorSetString(INDICATOR_SHORTNAME, 'MultiTrend_Signal_KVN')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_prev_Trend
    if BarsCalculated(ADX_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    ADX = Arr(0, 0.0)
    Range = 0.0
    AvgRange = 0.0
    Swing = 0.0
    smin = 0.0
    smax = 0.0
    SsMax = 0.0
    SsMin = 0.0
    val1 = 0.0
    val2 = 0.0
    to_copy = 0
    limit = 0
    bar = 0
    SSP = 0
    Trend = 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(ADX, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1 - min_rates_total
        _s_OnCalculate_prev_Trend = 0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ADX_Handle, MAIN_LINE, 0, to_copy, ADX) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        SSP = _int(MathCeil(_fdiv(Kperiod, ADX[bar])))
        SSP = MathMax(1, SSP)
        Range = 0.0
        AvgRange = 0.0
        for i1 in range(bar + SSP - 1, bar - 1, -1):
            AvgRange += MathAbs(high[i1] - low[i1])
        Range = _fdiv(AvgRange, SSP)
        SsMax = high[ArrayMaximum(high, bar, SSP)]
        SsMin = low[ArrayMinimum(low, bar, SSP)]
        Swing = ((SsMax - SsMin) * K) / 100
        smin = SsMin + Swing
        smax = SsMax - Swing
        Trend = _s_OnCalculate_prev_Trend
        val1 = 0.0
        val2 = 0.0
        if close[bar] < smin:
            Trend = -1
            if _s_OnCalculate_prev_Trend > -1:
                val1 = high[bar] + (Range * Kstop)
        if close[bar] > smax:
            Trend = 1
            if _s_OnCalculate_prev_Trend < 1:
                val2 = low[bar] - (Range * Kstop)
        BuyBuffer[bar] = val2
        SellBuffer[bar] = val1
        if bar:
            _s_OnCalculate_prev_Trend = Trend
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_prev_Trend = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MultitrendSignalKvn(_MQL5Indicator):
    name = 'multitrend_signal_kvn'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'K': 48,
        'Kstop': 0.5,
        'Kperiod': 150,
        'PerADX': 14,
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

