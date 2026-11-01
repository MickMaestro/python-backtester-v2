"""demo_indicatorsetdouble — converted from MQL5: MQL5 Indicators/Demo_IndicatorSetDouble/demo_indicatorsetdouble.mq5

Copyright: Copyright 2012, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2012, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_minimum': 0.0, 'indicator_maximum': 100.0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [25.0, 50.0, 75.0], 'description': [], 'name': 'demo_indicatorsetdouble', 'source': 'MQL5 Indicators/Demo_IndicatorSetDouble/demo_indicatorsetdouble.mq5', 'folder': 'Demo_IndicatorSetDouble', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}


def OnInit():
    IndicatorSetString(INDICATOR_LEVELTEXT, 0, 'First Level (index 0)')
    IndicatorSetString(INDICATOR_LEVELTEXT, 1, 'Second Level (index 1)')
    IndicatorSetString(INDICATOR_LEVELTEXT, 2, 'Third Level (index 2)')
    IndicatorSetString(INDICATOR_SHORTNAME, 'IndicatorSetDouble() Demo')
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGreen)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrRed)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_level1, _s_OnCalculate_level2, _s_OnCalculate_level3, _s_OnCalculate_max_, _s_OnCalculate_min_, _s_OnCalculate_shift, _s_OnCalculate_tick_counter
    _s_OnCalculate_tick_counter += 1
    if _imod(_s_OnCalculate_tick_counter, 10) == 0:
        _s_OnCalculate_level1 = -_s_OnCalculate_level1
        _s_OnCalculate_level2 = -_s_OnCalculate_level2
        _s_OnCalculate_level3 = -_s_OnCalculate_level3
        _s_OnCalculate_max_ -= _s_OnCalculate_shift
        _s_OnCalculate_min_ -= _s_OnCalculate_shift
        _s_OnCalculate_shift = -_s_OnCalculate_shift
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, _s_OnCalculate_level1)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, _s_OnCalculate_level2)
        IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, _s_OnCalculate_level3)
        Print('Set up max = ', _s_OnCalculate_max_, ',   min = ', _s_OnCalculate_min_)
        IndicatorSetDouble(INDICATOR_MAXIMUM, _s_OnCalculate_max_)
        IndicatorSetDouble(INDICATOR_MINIMUM, _s_OnCalculate_min_)
    return rates_total

# ---- static local variables
_s_OnCalculate_tick_counter = 0
_s_OnCalculate_level1 = 25.0
_s_OnCalculate_level2 = 50.0
_s_OnCalculate_level3 = 75.0
_s_OnCalculate_max_ = 100.0
_s_OnCalculate_min_ = 0.0
_s_OnCalculate_shift = 100.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DemoIndicatorsetdouble(_MQL5Indicator):
    name = 'demo_indicatorsetdouble'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
    }
    y_range = (0.0, 100.0)

