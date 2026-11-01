"""i-SpectrAnalysis_RVI — converted from MQL5: MQL5 Indicators/i-SpectrAnalysis_RVI/i-SpectrAnalysis_RVI.mq5

FFT for MQL5
Copyright: Copyright © 2006, klot; Link: http://alglib.sources.ru/fft/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.dt_fft import *  # #include dt_fft.mqh

MQL5_META = {'props': {'copyright': 'Copyright © 2006, klot', 'link': 'http://alglib.sources.ru/fft/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16748574, 13828244]}, 'widths': {}, 'styles': {}, 'labels': {1: 'i-SpectrAnalysis_RVI'}, 'levels': [0.0], 'description': ['FFT for MQL5'], 'name': 'i-SpectrAnalysis_RVI', 'source': 'MQL5 Indicators/i-SpectrAnalysis_RVI/i-SpectrAnalysis_RVI.mq5', 'folder': 'i-SpectrAnalysis_RVI', 'inputs': [{'mql': 'RVIPeriod', 'py': 'RVIPeriod', 'param': 'RVIPeriod', 'type': 'uint', 'default': 14, 'label': 'averaging period', 'sinput': False}, {'mql': 'N', 'py': 'N', 'param': 'N', 'type': 'uint', 'default': 7, 'label': 'number Length', 'sinput': False}, {'mql': 'SS', 'py': 'SS', 'param': 'SS', 'type': 'uint', 'default': 20, 'label': 'smoothing factor', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'The shift indicator in the horizontal bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['dt_fft.mqh']}

# ---- inputs and global variables
RVIPeriod = _input('RVIPeriod', 14)  # averaging period
N = _input('N', 7)  # number Length
SS = _input('SS', 20)  # smoothing factor
Shift = _input('Shift', 0)  # The shift indicator in the horizontal bars
RVIBuffer = Arr(0, 0.0)
SignBuffer = Arr(0, 0.0)
M = 0
tnn1 = 0
ss = 0
aa = Arr(0, 0.0)
min_rates_total = 0
Ind_Handle = 0

def OnInit():
    global Ind_Handle, M, min_rates_total, ss, tnn1
    tnn1 = _int(MathPow(2, N))
    M = ArrayResize(aa, tnn1 + 1)
    ArraySetAsSeries(aa, True)
    ss = _int(MathMin(SS, M))
    min_rates_total = M
    Ind_Handle = iRVI(Symbol(), PERIOD_CURRENT, RVIPeriod)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRVI')
        return INIT_FAILED
    SetIndexBuffer(0, RVIBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, SignBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(RVIBuffer, True)
    ArraySetAsSeries(SignBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'i-SpectrAnalysis_RVI')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total or BarsCalculated(Ind_Handle) < rates_total:
        return 0
    end = M - 1
    drawbegin = rates_total - end
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, drawbegin)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, drawbegin)
    if CopyBuffer(Ind_Handle, 0, 0, M, aa) <= 0:
        return 0
    fastcosinetransform(aa, tnn1, False)
    for kkk in range(0, end + 1):
        if kkk >= ss:
            aa[kkk] = 0.0
    fastcosinetransform(aa, tnn1, True)
    for rrr in range(0, end + 1):
        RVIBuffer[rrr] = aa[rrr]
    if CopyBuffer(Ind_Handle, 1, 0, M, aa) <= 0:
        return 0
    fastcosinetransform(aa, tnn1, False)
    for kkk in range(0, end + 1):
        if kkk >= ss:
            aa[kkk] = 0.0
    fastcosinetransform(aa, tnn1, True)
    for rrr in range(0, end + 1):
        SignBuffer[rrr] = aa[rrr]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ISpectrAnalysisRVI(_MQL5Indicator):
    name = 'i-SpectrAnalysis_RVI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'RVIPeriod': 14,  # averaging period
        'N': 7,  # number Length
        'SS': 20,  # smoothing factor
        'Shift': 0,  # The shift indicator in the horizontal bars
    }

