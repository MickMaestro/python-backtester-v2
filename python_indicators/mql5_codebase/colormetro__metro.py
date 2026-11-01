"""colormetro — converted from MQL5: MQL5 Indicators/METRO/colormetro.mq5

METRO
Copyright: Copyright © 2005, TrendLaboratory Ltd.; Link: E-mail: igorad2004@list.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, TrendLaboratory Ltd.', 'link': 'E-mail: igorad2004@list.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2, 'indicator_minimum': 0.0, 'indicator_maximum': 100.0}, 'types': {1: 7, 2: 1}, 'colors': {1: [16711680, 16711935], 2: [42495]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Step RSI', 2: 'RSI'}, 'levels': [70.0, 50.0, 30.0], 'description': ['METRO'], 'name': 'colormetro', 'source': 'MQL5 Indicators/METRO/colormetro.mq5', 'folder': 'METRO', 'inputs': [{'mql': 'PeriodRSI', 'py': 'PeriodRSI', 'param': 'PeriodRSI', 'type': 'int', 'default': 7, 'label': 'Indicator period', 'sinput': False}, {'mql': 'StepSizeFast', 'py': 'StepSizeFast', 'param': 'StepSizeFast', 'type': 'int', 'default': 5, 'label': 'Fast step', 'sinput': False}, {'mql': 'StepSizeSlow', 'py': 'StepSizeSlow', 'param': 'StepSizeSlow', 'type': 'int', 'default': 15, 'label': 'Slow step', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
PeriodRSI = _input('PeriodRSI', 7)  # Indicator period
StepSizeFast = _input('StepSizeFast', 5)  # Fast step
StepSizeSlow = _input('StepSizeSlow', 15)  # Slow step
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
Line1Buffer = Arr(0, 0.0)
Line2Buffer = Arr(0, 0.0)
Line3Buffer = Arr(0, 0.0)
RSI_Handle = 0
min_rates_total = 0

def OnInit():
    global RSI_Handle, min_rates_total
    min_rates_total = PeriodRSI
    RSI_Handle = iRSI(None, 0, PeriodRSI, PRICE_CLOSE)
    if RSI_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the RSI indicator')
        return 1
    SetIndexBuffer(0, Line2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Line2Buffer, True)
    SetIndexBuffer(1, Line3Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Line3Buffer, True)
    SetIndexBuffer(2, Line1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Line1Buffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'METRO(', PeriodRSI, ', ', StepSizeFast, ', ', StepSizeSlow, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_fmax1, _s_OnCalculate_fmin1, _s_OnCalculate_ftrend_, _s_OnCalculate_smax1, _s_OnCalculate_smin1, _s_OnCalculate_strend_
    if BarsCalculated(RSI_Handle) < rates_total or rates_total < min_rates_total:
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
    RSI0 = 0.0
    RSI = Arr(0, 0.0)
    ArraySetAsSeries(RSI, True)
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
    if CopyBuffer(RSI_Handle, 0, 0, to_copy, RSI) <= 0:
        return 0
    ftrend = _s_OnCalculate_ftrend_
    strend = _s_OnCalculate_strend_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            _s_OnCalculate_ftrend_ = ftrend
            _s_OnCalculate_strend_ = strend
        RSI0 = RSI[bar]
        fmax0 = RSI0 + (2 * StepSizeFast)
        fmin0 = RSI0 - (2 * StepSizeFast)
        if RSI0 > _s_OnCalculate_fmax1:
            ftrend = 1
        if RSI0 < _s_OnCalculate_fmin1:
            ftrend = -1
        if ftrend > 0 and fmin0 < _s_OnCalculate_fmin1:
            fmin0 = _s_OnCalculate_fmin1
        if ftrend < 0 and fmax0 > _s_OnCalculate_fmax1:
            fmax0 = _s_OnCalculate_fmax1
        smax0 = RSI0 + (2 * StepSizeSlow)
        smin0 = RSI0 - (2 * StepSizeSlow)
        if RSI0 > _s_OnCalculate_smax1:
            strend = 1
        if RSI0 < _s_OnCalculate_smin1:
            strend = -1
        if strend > 0 and smin0 < _s_OnCalculate_smin1:
            smin0 = _s_OnCalculate_smin1
        if strend < 0 and smax0 > _s_OnCalculate_smax1:
            smax0 = _s_OnCalculate_smax1
        Line1Buffer[bar] = RSI0
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


class Colormetro(_MQL5Indicator):
    name = 'colormetro'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'PeriodRSI': 7,  # Indicator period
        'StepSizeFast': 5,  # Fast step
        'StepSizeSlow': 15,  # Slow step
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }
    y_range = (0.0, 100.0)

