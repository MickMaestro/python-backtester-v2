"""i-spectranalysis_obv — converted from MQL5: MQL5 Indicators/i-SpectrAnalysis_OBV/i-spectranalysis_obv.mq5

FFT for MQL5
Copyright: Copyright © 2006, klot; Link: http://alglib.sources.ru/fft/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.dt_fft import *  # #include dt_fft.mqh

MQL5_META = {'props': {'copyright': 'Copyright © 2006, klot', 'link': 'http://alglib.sources.ru/fft/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [15624315]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'i-SpectrAnalysis_OBV'}, 'levels': [], 'description': ['FFT for MQL5'], 'name': 'i-spectranalysis_obv', 'source': 'MQL5 Indicators/i-SpectrAnalysis_OBV/i-spectranalysis_obv.mq5', 'folder': 'i-SpectrAnalysis_OBV', 'inputs': [{'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'Объем', 'sinput': False}, {'mql': 'N', 'py': 'N', 'param': 'N', 'type': 'uint', 'default': 7, 'label': 'Длина ряда', 'sinput': False}, {'mql': 'SS', 'py': 'SS', 'param': 'SS', 'type': 'uint', 'default': 20, 'label': 'Коэффициент сглаживания', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['dt_fft.mqh']}

# ---- inputs and global variables
VolumeType = _input('VolumeType', VOLUME_TICK)  # Объем
N = _input('N', 7)  # Длина ряда
SS = _input('SS', 20)  # Коэффициент сглаживания
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
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
    Ind_Handle = iOBV(Symbol(), PERIOD_CURRENT, VolumeType)
    if Ind_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iOBV')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(IndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'i-SpectrAnalysis_OBV')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total or BarsCalculated(Ind_Handle) < rates_total:
        return 0
    for bar in range(rates_total - 1, prev_calculated - 1, -1):
        IndBuffer[bar] = 0.0
    if CopyBuffer(Ind_Handle, 0, 0, M, aa) <= 0:
        return 0
    end = M - 1
    fastcosinetransform(aa, tnn1, False)
    for kkk in range(0, end + 1):
        if kkk >= ss:
            aa[kkk] = 0.0
    fastcosinetransform(aa, tnn1, True)
    for rrr in range(0, end + 1):
        IndBuffer[rrr] = aa[rrr]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ISpectranalysisObv(_MQL5Indicator):
    name = 'i-spectranalysis_obv'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Объем
        'N': 7,  # Длина ряда
        'SS': 20,  # Коэффициент сглаживания
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

