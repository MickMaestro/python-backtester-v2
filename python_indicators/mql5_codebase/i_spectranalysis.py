"""i-spectranalysis — converted from MQL5: MQL5 Indicators/i-SpectrAnalysis/i-spectranalysis.mq5

FFT for MQL5
Copyright: Copyright © 2006, klot; Link: http://alglib.sources.ru/fft/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.dt_fft import *  # #include dt_fft.mqh

MQL5_META = {'props': {'copyright': 'Copyright © 2006, klot', 'link': 'http://alglib.sources.ru/fft/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'i_SpecktrAnalis'}, 'levels': [], 'description': ['FFT for MQL5'], 'name': 'i-spectranalysis', 'source': 'MQL5 Indicators/i-SpectrAnalysis/i-spectranalysis.mq5', 'folder': 'i-SpectrAnalysis', 'inputs': [{'mql': 'N', 'py': 'N', 'param': 'N', 'type': 'uint', 'default': 7, 'label': 'Длина ряда', 'sinput': False}, {'mql': 'SS', 'py': 'SS', 'param': 'SS', 'type': 'uint', 'default': 20, 'label': 'Коэффициент сглаживания', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['dt_fft.mqh']}

# ---- inputs and global variables
N = _input('N', 7)  # Длина ряда
SS = _input('SS', 20)  # Коэффициент сглаживания
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
IndBuffer = Arr(0, 0.0)
M = 0
tnn1 = 0
ss = 0
aa = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global M, min_rates_total, ss, tnn1
    tnn1 = _int(MathPow(2, N))
    M = ArrayResize(aa, tnn1 + 1)
    ss = _int(MathMin(SS, M))
    min_rates_total = M
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'i-SpecktrAnalis')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, begin, price):
    if rates_total < (min_rates_total + begin):
        return 0
    for bbb in range(rates_total - 1, prev_calculated - 1, -1):
        IndBuffer[rates_total - 1 - bbb] = 0.0
    end = M - 1
    for iii in range(M - 1, 0 - 1, -1):
        aa[iii] = price[rates_total - 1 - iii]
    fastcosinetransform(aa, tnn1, False)
    for kkk in range(0, end + 1):
        if kkk >= ss:
            aa[kkk] = 0.0
    fastcosinetransform(aa, tnn1, True)
    for rrr in range(0, end + 1):
        IndBuffer[rates_total - 1 - rrr] = aa[rrr]
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ISpectranalysis(_MQL5Indicator):
    name = 'i-spectranalysis'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'N': 7,  # Длина ряда
        'SS': 20,  # Коэффициент сглаживания
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

