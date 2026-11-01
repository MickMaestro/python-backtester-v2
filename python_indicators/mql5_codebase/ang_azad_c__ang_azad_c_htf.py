"""ang_azad_c — converted from MQL5: MQL5 Indicators/ang_AZad_C_HTF/ang_azad_c.mq5

Copyright: Copyright © 2006, ANG3110@latchess.com; Link: ANG3110@latchess.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, ANG3110@latchess.com', 'link': 'ANG3110@latchess.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'ang_AZad_C'}, 'levels': [0.0], 'description': [], 'name': 'ang_azad_c', 'source': 'MQL5 Indicators/ang_AZad_C_HTF/ang_azad_c.mq5', 'folder': 'ang_AZad_C_HTF', 'inputs': [{'mql': 'ki', 'py': 'ki', 'param': 'ki', 'type': 'double', 'default': 4.0, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ki = _input('ki', 4.0)
Shift = _input('Shift', 0)
min_rates_total = 0
IndBuffer = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = 4
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(IndBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ang_AZad_C')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    global _s_OnCalculate_Za2_, _s_OnCalculate_Za_, _s_OnCalculate_z2_, _s_OnCalculate_z_
    if rates_total < min_rates_total:
        return 0
    z = 0.0
    z2 = 0.0
    Za2 = 0.0
    Za = 0.0
    limit = 0
    ArraySetAsSeries(Close, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_z_ = Close[limit + 1]
        _s_OnCalculate_z2_ = _s_OnCalculate_z_
        Za = _s_OnCalculate_z2_
        _s_OnCalculate_Za2_ = Za
    else:
        limit = rates_total - prev_calculated
    z = _s_OnCalculate_z_
    z2 = _s_OnCalculate_z2_
    Za2 = _s_OnCalculate_Za2_
    Za = _s_OnCalculate_Za_
    for bar in range(limit, 0 - 1, -1):
        if Close[bar] > z and Close[bar] > Close[bar + 1]:
            z = _s_OnCalculate_Za_ + ((Close[bar] - _s_OnCalculate_Za_) / ki)
        if Close[bar] < z and Close[bar] < Close[bar + 1]:
            z = _s_OnCalculate_Za_ + ((Close[bar] - _s_OnCalculate_Za_) / ki)
        if Close[bar] > z2 and Close[bar] < Close[bar + 1]:
            z2 = _s_OnCalculate_Za2_ + ((Close[bar] - _s_OnCalculate_Za2_) / ki)
        if Close[bar] < z2 and Close[bar] > Close[bar + 1]:
            z2 = _s_OnCalculate_Za2_ + ((Close[bar] - _s_OnCalculate_Za2_) / ki)
        Za = z
        Za2 = z2
        IndBuffer[bar] = _fdiv(Za - Za2, Point())
        if bar:
            _s_OnCalculate_z_ = z
            _s_OnCalculate_z2_ = z2
            _s_OnCalculate_Za2_ = Za2
            _s_OnCalculate_Za_ = Za
    return rates_total

# ---- static local variables
_s_OnCalculate_z_ = 0.0
_s_OnCalculate_z2_ = 0.0
_s_OnCalculate_Za2_ = 0.0
_s_OnCalculate_Za_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AngAzadC(_MQL5Indicator):
    name = 'ang_azad_c'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ki': 4.0,
        'Shift': 0,
    }

