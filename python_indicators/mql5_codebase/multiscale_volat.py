"""multiscale_volat — converted from MQL5: MQL5 Indicators/multi-scale volatility/multiscale_volat.mq5

Copyright: Copyright 2021, Yossy Nakata; Link: https://www.mql5.com/ja/users/yossy_nkt; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2021, Yossy Nakata', 'link': 'https://www.mql5.com/ja/users/yossy_nkt', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 15, 'indicator_plots': 8}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'colors': {1: [255], 2: [17919], 3: [36095], 4: [755384], 5: [32768], 6: [13688896], 7: [16748574], 8: [16711680]}, 'widths': {1: 3, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'styles': {}, 'labels': {1: 'Multi-scale volatility', 2: 'lag-3', 3: 'lag-4', 4: 'lag-5', 5: 'lag-6', 6: 'lag-8', 7: 'lag-10', 8: 'lag-13'}, 'levels': [], 'description': [], 'name': 'multiscale_volat', 'source': 'MQL5 Indicators/multi-scale volatility/multiscale_volat.mq5', 'folder': 'multi-scale volatility', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'int', 'default': 14, 'label': 'Smoothing Period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # Smoothing Period
df3 = Arr(0, 0.0)
df4 = Arr(0, 0.0)
df5 = Arr(0, 0.0)
df6 = Arr(0, 0.0)
df8 = Arr(0, 0.0)
df10 = Arr(0, 0.0)
df13 = Arr(0, 0.0)
adf3 = Arr(0, 0.0)
adf4 = Arr(0, 0.0)
adf5 = Arr(0, 0.0)
adf6 = Arr(0, 0.0)
adf8 = Arr(0, 0.0)
adf10 = Arr(0, 0.0)
adf13 = Arr(0, 0.0)
adf = Arr(0, 0.0)

def OnInit():
    SetIndexBuffer(0, adf, INDICATOR_DATA)
    SetIndexBuffer(1, adf3, INDICATOR_DATA)
    SetIndexBuffer(2, adf4, INDICATOR_DATA)
    SetIndexBuffer(3, adf5, INDICATOR_DATA)
    SetIndexBuffer(4, adf6, INDICATOR_DATA)
    SetIndexBuffer(5, adf8, INDICATOR_DATA)
    SetIndexBuffer(6, adf10, INDICATOR_DATA)
    SetIndexBuffer(7, adf13, INDICATOR_DATA)
    SetIndexBuffer(8, df3, INDICATOR_CALCULATIONS)
    SetIndexBuffer(9, df4, INDICATOR_CALCULATIONS)
    SetIndexBuffer(10, df5, INDICATOR_CALCULATIONS)
    SetIndexBuffer(11, df6, INDICATOR_CALCULATIONS)
    SetIndexBuffer(12, df8, INDICATOR_CALCULATIONS)
    SetIndexBuffer(13, df10, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, df13, INDICATOR_CALCULATIONS)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(7, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(8, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(9, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(10, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(11, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(12, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(13, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(14, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    limit = rates_total - prev_calculated
    if limit > 1:
        ArrayInitialize(adf, EMPTY_VALUE)
        ArrayInitialize(adf3, EMPTY_VALUE)
        ArrayInitialize(adf4, EMPTY_VALUE)
        ArrayInitialize(adf5, EMPTY_VALUE)
        ArrayInitialize(adf6, EMPTY_VALUE)
        ArrayInitialize(adf8, EMPTY_VALUE)
        ArrayInitialize(adf10, EMPTY_VALUE)
        ArrayInitialize(adf13, EMPTY_VALUE)
        ArrayInitialize(df3, EMPTY_VALUE)
        ArrayInitialize(df4, EMPTY_VALUE)
        ArrayInitialize(df5, EMPTY_VALUE)
        ArrayInitialize(df6, EMPTY_VALUE)
        ArrayInitialize(df8, EMPTY_VALUE)
        ArrayInitialize(df10, EMPTY_VALUE)
        ArrayInitialize(df13, EMPTY_VALUE)
    i = 0
    pos = 0
    pos = MathMax(prev_calculated - 1, 0)
    i = pos
    for i in range(i, rates_total):
        diff(i, 3, Sqrt3, close, df3)
        diff(i, 4, Sqrt4, close, df4)
        diff(i, 5, Sqrt5, close, df5)
        diff(i, 6, Sqrt6, close, df6)
        diff(i, 8, Sqrt8, close, df8)
        diff(i, 10, Sqrt10, close, df10)
        diff(i, 13, Sqrt13, close, df13)
        if i > 2:
            total = 0.0
            n = 0
            ema(i, Alpha, df3, adf3)
            ema(i, Alpha, df4, adf4)
            ema(i, Alpha, df5, adf5)
            ema(i, Alpha, df6, adf6)
            ema(i, Alpha, df8, adf8)
            ema(i, Alpha, df10, adf10)
            ema(i, Alpha, df13, adf13)
        if i > (InpPeriod + 13):
            total = adf3[i] + adf4[i] + adf5[i] + adf6[i] + adf8[i] + adf10[i] + adf13[i]
            adf[i] = total / 7.0
        else:
            adf[i] = EMPTY_VALUE
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total

def diff(i, lag, w, close, buf):
    if i <= lag:
        buf[i] = EMPTY_VALUE
    else:
        buf[i] = _fdiv(MathAbs(close[i - lag] - close[i]), w)

def ema(i, alpha, buf, ema_):
    if buf[i - 1] != EMPTY_VALUE and buf[i] != EMPTY_VALUE:
        if ema_[i - 1] == EMPTY_VALUE:
            ema_[i - 1] = buf[i - 1]
        ema_[i] = (alpha * buf[i]) + ((1.0 - alpha) * ema_[i - 1])
    else:
        ema_[i] = EMPTY_VALUE

# ---- global variables initialised from expressions
Alpha = _fdiv(2.0, InpPeriod + 1.0)
Sqrt3 = sqrt(3)
Sqrt4 = sqrt(4)
Sqrt5 = sqrt(5)
Sqrt6 = sqrt(6)
Sqrt8 = sqrt(8)
Sqrt10 = sqrt(10)
Sqrt13 = sqrt(13)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MultiscaleVolat(_MQL5Indicator):
    name = 'multiscale_volat'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # Smoothing Period
    }

