"""ozfx_d1_indaes_v1e0 — converted from MQL5: MQL5 Indicators/OzFX_D1_IndAES_v1.0/ozfx_d1_indaes_v1e0.mq5

Copyright: Copyright © 2008, DGC; Link: http://www.ozfx.com.au/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, DGC', 'link': 'http://www.ozfx.com.au/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 3}, 'types': {1: 10, 2: 10, 3: 1}, 'colors': {1: [16711935, 8421504, 8421376], 2: [255, 8421504, 16711680], 3: [55295]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'OzFX Signals', 2: 'AES Signals', 3: 'SMA Filter'}, 'levels': [], 'description': [], 'name': 'ozfx_d1_indaes_v1e0', 'source': 'MQL5 Indicators/OzFX_D1_IndAES_v1.0/ozfx_d1_indaes_v1e0.mq5', 'folder': 'OzFX_D1_IndAES_v1.0', 'inputs': [{'mql': 'SMA_Filter_Period', 'py': 'SMA_Filter_Period', 'param': 'SMA_Filter_Period', 'type': 'uint', 'default': 200, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SMA_Filter_Period = _input('SMA_Filter_Period', 200)
IndBuffer1 = Arr(0, 0.0)
IndBuffer2 = Arr(0, 0.0)
IndBuffer3 = Arr(0, 0.0)
ColorIndBuffer1 = Arr(0, 0.0)
ColorIndBuffer2 = Arr(0, 0.0)
ColorIndBuffer3 = Arr(0, 0.0)
min_rates_total = 0
KPer = 0
DPer = 0
Slow = 0
ACLim = 0
MA_Handle = 0
AC_Handle = 0
STO_Handle = 0

def OnInit():
    global ACLim, AC_Handle, DPer, KPer, MA_Handle, STO_Handle, Slow, min_rates_total
    KPer = 5
    DPer = 3
    Slow = 3
    ACLim = 37
    min_rates_total = _int(MathMax(MathMax(ACLim, KPer + DPer + Slow), SMA_Filter_Period))
    STO_Handle = iStochastic(None, 0, KPer, DPer, Slow, MODE_SMA, STO_LOWHIGH)
    if STO_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iStochastic indicator')
    MA_Handle = iMA(None, 0, SMA_Filter_Period, 0, MODE_SMA, PRICE_CLOSE)
    if MA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iMA indicator')
    AC_Handle = iAC(None, 0)
    if AC_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the Accelerator Oscillator indicator')
    SetIndexBuffer(0, IndBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer1, True)
    SetIndexBuffer(1, ColorIndBuffer1, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer1, True)
    SetIndexBuffer(2, IndBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer2, True)
    SetIndexBuffer(3, ColorIndBuffer2, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer2, True)
    SetIndexBuffer(4, IndBuffer3, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(IndBuffer3, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'OzFX_D1_IndAES_v1.0')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_trend1, _s_OnCalculate_trend2
    if ((BarsCalculated(STO_Handle) < rates_total or BarsCalculated(AC_Handle) < rates_total) or BarsCalculated(MA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    to_copy = 0
    Stoc = Arr(0, 0.0)
    Main = Arr(0, 0.0)
    AC = Arr(0, 0.0)
    MA = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_trend1 = 0
        _s_OnCalculate_trend2 = 0
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(Stoc, True)
    ArraySetAsSeries(Main, True)
    ArraySetAsSeries(AC, True)
    ArraySetAsSeries(MA, True)
    ArraySetAsSeries(close, True)
    to_copy = limit + 1
    if CopyBuffer(STO_Handle, MAIN_LINE, 0, to_copy, Stoc) <= 0:
        return 0
    if CopyBuffer(STO_Handle, SIGNAL_LINE, 0, to_copy, Main) <= 0:
        return 0
    if CopyBuffer(AC_Handle, 0, 0, to_copy + 1, AC) <= 0:
        return 0
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MA) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        IndBuffer1[bar] = 0.0
        ColorIndBuffer1[bar] = 1.0
        if (AC[bar] > 0 and AC[bar] > AC[bar + 1]) and Stoc[bar] > 50:
            if _s_OnCalculate_trend1 != 1:
                IndBuffer1[bar] = 2.0
                ColorIndBuffer1[bar] = 2.0
            if bar:
                _s_OnCalculate_trend1 = 1
        if (AC[bar] < 0 and AC[bar] < AC[bar + 1]) and Stoc[bar] < 50:
            if _s_OnCalculate_trend1 != -1:
                IndBuffer1[bar] = -2.0
                ColorIndBuffer1[bar] = 0.0
            if bar:
                _s_OnCalculate_trend1 = -1
        IndBuffer2[bar] = 0.0
        ColorIndBuffer2[bar] = 1.0
        if AC[bar] > AC[bar + 1] and Stoc[bar] > Main[bar]:
            if _s_OnCalculate_trend2 != 1:
                IndBuffer2[bar] = 1.0
                ColorIndBuffer2[bar] = 2.0
            if bar:
                _s_OnCalculate_trend2 = 1
        if AC[bar] < AC[bar + 1] and Stoc[bar] < Main[bar]:
            if _s_OnCalculate_trend2 != -1:
                IndBuffer2[bar] = -1.0
                ColorIndBuffer2[bar] = 0.0
            if bar:
                _s_OnCalculate_trend2 = -1
        IndBuffer3[bar] = 0.0
        if close[bar] > MA[bar]:
            IndBuffer3[bar] = 2.0
        if close[bar] <= MA[bar]:
            IndBuffer3[bar] = -2.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_trend1 = 0
_s_OnCalculate_trend2 = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class OzfxD1IndaesV1e0(_MQL5Indicator):
    name = 'ozfx_d1_indaes_v1e0'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'SMA_Filter_Period': 200,
    }

