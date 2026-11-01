"""colormetro_stochastic — converted from MQL5: MQL5 Indicators/ColorMETRO_Stochastic/colormetro_stochastic.mq5

METRO
Copyright: Copyright © 2005, TrendLaboratory Ltd.; Link: E-mail: igorad2004@list.ru; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, TrendLaboratory Ltd.', 'link': 'E-mail: igorad2004@list.ru', 'version': '1.10', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 2}, 'types': {1: 7, 2: 1}, 'colors': {1: [7451452, 4678655], 2: [13458026]}, 'widths': {1: 1, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'StepStochastic cloud', 2: 'Stochastic'}, 'levels': [70.0, 50.0, 30.0], 'description': ['METRO'], 'name': 'colormetro_stochastic', 'source': 'MQL5 Indicators/ColorMETRO_Stochastic/colormetro_stochastic.mq5', 'folder': 'ColorMETRO_Stochastic', 'inputs': [{'mql': 'KPeriod', 'py': 'KPeriod', 'param': 'KPeriod', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'Slowing', 'py': 'Slowing', 'param': 'Slowing', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'StepSizeFast', 'py': 'StepSizeFast', 'param': 'StepSizeFast', 'type': 'int', 'default': 5, 'label': 'Быстрый шаг', 'sinput': False}, {'mql': 'StepSizeSlow', 'py': 'StepSizeSlow', 'param': 'StepSizeSlow', 'type': 'int', 'default': 15, 'label': 'Медленный шаг', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Applied_price', 'py': 'Applied_price', 'param': 'Applied_price', 'type': 'int', 'default': 0, 'label': 'Тип цены или handle', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
KPeriod = _input('KPeriod', 5)
DPeriod = _input('DPeriod', 3)
Slowing = _input('Slowing', 3)
MA_Method = _input('MA_Method', MODE_SMA)
StepSizeFast = _input('StepSizeFast', 5)  # Быстрый шаг
StepSizeSlow = _input('StepSizeSlow', 15)  # Медленный шаг
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
Applied_price = _input('Applied_price', STO_LOWHIGH)  # Тип цены или handle
Line1Buffer = Arr(0, 0.0)
Line2Buffer = Arr(0, 0.0)
Line3Buffer = Arr(0, 0.0)
Stochastic_Handle = 0
min_rates_total = 0

def OnInit():
    global Stochastic_Handle, min_rates_total
    min_rates_total = _int(KPeriod + DPeriod + Slowing)
    Stochastic_Handle = iStochastic(None, 0, KPeriod, DPeriod, Slowing, MA_Method, Applied_price)
    if Stochastic_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора Stochastic')
        return INIT_FAILED
    SetIndexBuffer(0, Line1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Line1Buffer, True)
    SetIndexBuffer(1, Line2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Line2Buffer, True)
    SetIndexBuffer(2, Line3Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Line3Buffer, True)
    shortname = 'METRO_Stochastic'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_fmax1, _s_OnCalculate_fmin1, _s_OnCalculate_ftrend_, _s_OnCalculate_smax1, _s_OnCalculate_smin1, _s_OnCalculate_strend_
    if BarsCalculated(Stochastic_Handle) < rates_total or rates_total < min_rates_total:
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
    Stochastic0 = 0.0
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
    if CopyBuffer(Stochastic_Handle, 1, 0, to_copy, Line3Buffer) <= 0:
        return 0
    ftrend = _s_OnCalculate_ftrend_
    strend = _s_OnCalculate_strend_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            _s_OnCalculate_ftrend_ = ftrend
            _s_OnCalculate_strend_ = strend
        Line3Buffer[bar] = Line3Buffer[bar]
        Stochastic0 = Line3Buffer[bar]
        fmax0 = Stochastic0 + (2 * StepSizeFast)
        fmin0 = Stochastic0 - (2 * StepSizeFast)
        if Stochastic0 > _s_OnCalculate_fmax1:
            ftrend = 1
        if Stochastic0 < _s_OnCalculate_fmin1:
            ftrend = -1
        if ftrend > 0 and fmin0 < _s_OnCalculate_fmin1:
            fmin0 = _s_OnCalculate_fmin1
        if ftrend < 0 and fmax0 > _s_OnCalculate_fmax1:
            fmax0 = _s_OnCalculate_fmax1
        smax0 = Stochastic0 + (2 * StepSizeSlow)
        smin0 = Stochastic0 - (2 * StepSizeSlow)
        if Stochastic0 > _s_OnCalculate_smax1:
            strend = 1
        if Stochastic0 < _s_OnCalculate_smin1:
            strend = -1
        if strend > 0 and smin0 < _s_OnCalculate_smin1:
            smin0 = _s_OnCalculate_smin1
        if strend < 0 and smax0 > _s_OnCalculate_smax1:
            smax0 = _s_OnCalculate_smax1
        if ftrend > 0:
            Line1Buffer[bar] = fmin0 + StepSizeFast
        if ftrend < 0:
            Line1Buffer[bar] = fmax0 - StepSizeFast
        if strend > 0:
            Line2Buffer[bar] = smin0 + StepSizeSlow
        if strend < 0:
            Line2Buffer[bar] = smax0 - StepSizeSlow
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


class ColormetroStochastic(_MQL5Indicator):
    name = 'colormetro_stochastic'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'KPeriod': 5,
        'DPeriod': 3,
        'Slowing': 3,
        'MA_Method': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),
        'StepSizeFast': 5,  # Быстрый шаг
        'StepSizeSlow': 15,  # Медленный шаг
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'Applied_price': _Choice({0: 'Lowhigh', 1: 'Closeclose'}, default=0),  # Тип цены или handle
    }

