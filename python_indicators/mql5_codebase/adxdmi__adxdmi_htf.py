"""ADXDMI — converted from MQL5: MQL5 Indicators/ADXDMI_HTF/ADXDMI.mq5

Copyright: Copyright © 2006, FXTEAM Turkey; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, FXTEAM Turkey', 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [16711680, 255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'ADXDMI'}, 'levels': [0.0], 'description': [], 'name': 'ADXDMI', 'source': 'MQL5 Indicators/ADXDMI_HTF/ADXDMI.mq5', 'folder': 'ADXDMI_HTF', 'inputs': [{'mql': 'DMIPeriod', 'py': 'DMIPeriod', 'param': 'DMIPeriod', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'Smooth', 'py': 'Smooth', 'param': 'Smooth', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
DMIPeriod = _input('DMIPeriod', 14)
Smooth = _input('Smooth', 10)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 4
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'ADXDMI(', DMIPeriod, ', ', Smooth, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 4)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_PREADX, _s_OnCalculate_PREN, _s_OnCalculate_PREP, _s_OnCalculate_PRETR
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    tr = 0.0
    xx = 0.0
    price_high = 0.0
    price_low = 0.0
    PD = 0.0
    ND = 0.0
    Buff = 0.0
    ADX = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 2
        _s_OnCalculate_PREP = 0.0
        _s_OnCalculate_PREN = 0.0
        _s_OnCalculate_PRETR = 0.0
        ADX = 0.0
        _s_OnCalculate_PREADX = 0.0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if high[bar] > high[bar - 1] and (high[bar] - high[bar - 1]) > (low[bar - 1] - low[bar]):
            xx = high[bar] - high[bar - 1]
        else:
            xx = 0.0
        PD = (((DMIPeriod - 1.0) * _s_OnCalculate_PREP) + xx) / DMIPeriod
        if low[bar] < low[bar - 1] and (low[bar - 1] - low[bar]) > (high[bar] - high[bar - 1]):
            xx = low[bar - 1] - low[bar]
        else:
            xx = 0.0
        ND = (((DMIPeriod - 1.0) * _s_OnCalculate_PREN) + xx) / DMIPeriod
        Buff = MathAbs(PD - ND)
        if not Buff:
            ADX = ((Smooth - 1.0) * _s_OnCalculate_PREADX) / Smooth
        else:
            ADX = (((Smooth - 1.0) * _s_OnCalculate_PREADX) + _fdiv(MathAbs(PD - ND), PD + ND)) / Smooth
        price_high = MathMax(high[bar], close[bar - 1])
        price_low = MathMin(low[bar], close[bar - 1])
        num1 = MathAbs(price_high - price_low)
        num2 = MathAbs(price_high - close[bar - 1])
        num3 = MathAbs(close[bar - 1] - price_low)
        tr = MathMax(num1, num2)
        tr = MathMax(tr, num3)
        tr = (((DMIPeriod - 1.0) * _s_OnCalculate_PRETR) + tr) / DMIPeriod
        UpBuffer[bar] = 100000 * _fdiv(PD, tr)
        DnBuffer[bar] = 100000 * _fdiv(ND, tr)
        if bar < (rates_total - 1):
            _s_OnCalculate_PREN = ND
            _s_OnCalculate_PREP = PD
            _s_OnCalculate_PREADX = ADX
            _s_OnCalculate_PRETR = tr
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_PREADX = 0.0
_s_OnCalculate_PREP = 0.0
_s_OnCalculate_PREN = 0.0
_s_OnCalculate_PRETR = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ADXDMI(_MQL5Indicator):
    name = 'ADXDMI'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'DMIPeriod': 14,
        'Smooth': 10,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

