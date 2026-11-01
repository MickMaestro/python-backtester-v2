"""colormetro_wpr — converted from MQL5: MQL5 Indicators/ColorMETRO_WPR/colormetro_wpr.mq5

METRO_WPR
Copyright: Copyright © 2005, TrendLaboratory Ltd.; Link: E-mail: igorad2004@list.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, TrendLaboratory Ltd.', 'link': 'E-mail: igorad2004@list.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 7, 2: 1}, 'colors': {1: [16748574, 255], 2: [13828244]}, 'widths': {1: 1, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'StepWPR cloud', 2: 'WPR'}, 'levels': [70.0, 50.0, 30.0], 'description': ['METRO_WPR'], 'name': 'colormetro_wpr', 'source': 'MQL5 Indicators/ColorMETRO_WPR/colormetro_wpr.mq5', 'folder': 'ColorMETRO_WPR', 'inputs': [{'mql': 'PeriodWPR', 'py': 'PeriodWPR', 'param': 'PeriodWPR', 'type': 'uint', 'default': 7, 'label': 'Период индикатора', 'sinput': False}, {'mql': 'StepSizeFast', 'py': 'StepSizeFast', 'param': 'StepSizeFast', 'type': 'int', 'default': 5, 'label': 'Быстрый шаг', 'sinput': False}, {'mql': 'StepSizeSlow', 'py': 'StepSizeSlow', 'param': 'StepSizeSlow', 'type': 'int', 'default': 15, 'label': 'Медленный шаг', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
PeriodWPR = _input('PeriodWPR', 7)  # Период индикатора
StepSizeFast = _input('StepSizeFast', 5)  # Быстрый шаг
StepSizeSlow = _input('StepSizeSlow', 15)  # Медленный шаг
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
Line1Buffer = Arr(0, 0.0)
Line2Buffer = Arr(0, 0.0)
Line3Buffer = Arr(0, 0.0)
WPR_Handle = 0
min_rates_total = 0

def OnInit():
    global WPR_Handle, min_rates_total
    min_rates_total = _int(PeriodWPR)
    WPR_Handle = iWPR(None, 0, PeriodWPR)
    if WPR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора WPR')
        return INIT_FAILED
    SetIndexBuffer(0, Line2Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Line2Buffer, True)
    SetIndexBuffer(1, Line3Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Line3Buffer, True)
    SetIndexBuffer(2, Line1Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Line1Buffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = Box("")
    StringConcatenate(shortname, 'METRO_WPR(', PeriodWPR, ', ', StepSizeFast, ', ', StepSizeSlow, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_fmax1, _s_OnCalculate_fmin1, _s_OnCalculate_ftrend_, _s_OnCalculate_smax1, _s_OnCalculate_smin1, _s_OnCalculate_strend_
    if BarsCalculated(WPR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    ftrend = 0
    strend = 0
    fmin0 = 0.0
    fmax0 = 0.0
    smin0 = 0.0
    smax0 = 0.0
    WPR0 = 0.0
    WPR = Arr(0, 0.0)
    ArraySetAsSeries(WPR, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
        _s_OnCalculate_fmin1 = 999999.0
        _s_OnCalculate_fmax1 = -999999.0
        _s_OnCalculate_smin1 = 999999.0
        _s_OnCalculate_smax1 = -999999.0
        _s_OnCalculate_ftrend_ = 0
        _s_OnCalculate_strend_ = 0
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(WPR_Handle, 0, 0, to_copy, WPR) <= 0:
        return 0
    ftrend = _s_OnCalculate_ftrend_
    strend = _s_OnCalculate_strend_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            _s_OnCalculate_ftrend_ = ftrend
            _s_OnCalculate_strend_ = strend
        WPR0 = WPR[bar] + 100
        fmax0 = WPR0 + (2 * StepSizeFast)
        fmin0 = WPR0 - (2 * StepSizeFast)
        if WPR0 > _s_OnCalculate_fmax1:
            ftrend = 1
        if WPR0 < _s_OnCalculate_fmin1:
            ftrend = -1
        if ftrend > 0 and fmin0 < _s_OnCalculate_fmin1:
            fmin0 = _s_OnCalculate_fmin1
        if ftrend < 0 and fmax0 > _s_OnCalculate_fmax1:
            fmax0 = _s_OnCalculate_fmax1
        smax0 = WPR0 + (2 * StepSizeSlow)
        smin0 = WPR0 - (2 * StepSizeSlow)
        if WPR0 > _s_OnCalculate_smax1:
            strend = 1
        if WPR0 < _s_OnCalculate_smin1:
            strend = -1
        if strend > 0 and smin0 < _s_OnCalculate_smin1:
            smin0 = _s_OnCalculate_smin1
        if strend < 0 and smax0 > _s_OnCalculate_smax1:
            smax0 = _s_OnCalculate_smax1
        Line1Buffer[bar] = WPR0
        if ftrend > 0:
            Line2Buffer[bar] = fmin0 + StepSizeFast
        if ftrend < 0:
            Line2Buffer[bar] = fmax0 - StepSizeFast
        if strend > 0:
            Line3Buffer[bar] = smin0 + StepSizeSlow
        if strend < 0:
            Line3Buffer[bar] = smax0 - StepSizeSlow
        if bar > 0:
            _s_OnCalculate_fmin1 = fmin0
            _s_OnCalculate_fmax1 = fmax0
            _s_OnCalculate_smin1 = smin0
            _s_OnCalculate_smax1 = smax0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_fmax1 = 0.0
_s_OnCalculate_fmin1 = 0.0
_s_OnCalculate_smin1 = 0.0
_s_OnCalculate_smax1 = 0.0
_s_OnCalculate_ftrend_ = 0
_s_OnCalculate_strend_ = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColormetroWpr(_MQL5Indicator):
    name = 'colormetro_wpr'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PeriodWPR': 7,  # Период индикатора
        'StepSizeFast': 5,  # Быстрый шаг
        'StepSizeSlow': 15,  # Медленный шаг
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

