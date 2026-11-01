"""OnTick — converted from MQL5: MQL5 Indicators/Currency Correlation II/OnTick.mq5

Copyright: Copyright 2020, ernst.; Link: https://www.mql5.com/en/users/pippod; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2020, ernst.', 'link': 'https://www.mql5.com/en/users/pippod', 'version': '1.00', 'window': 'chart'}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'OnTick', 'source': 'MQL5 Indicators/Currency Correlation II/OnTick.mq5', 'folder': 'Currency Correlation II', 'inputs': [{'mql': 'ChartID', 'py': 'ChartID_v', 'param': 'ChartID_v', 'type': 'long', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'EventID', 'py': 'EventID', 'param': 'EventID', 'type': 'ushort', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Pips', 'py': 'Pips', 'param': 'Pips', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ChartID_v = _input('ChartID_v', 0)
EventID = _input('EventID', 0)
Pips = _input('Pips', False)

def OnInit():
    printf('ChartID:%lld Event ID:%d Initialized for %s.', ChartID_v, EventID, Symbol())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    global _s_OnCalculate_close, _s_OnCalculate_muldiv, _s_OnCalculate_open, _s_OnCalculate_point, _s_OnCalculate_preClose
    if prev_calculated:
        if Pips:
            if _s_OnCalculate_muldiv is _UNSET:
                _s_OnCalculate_muldiv = MathPow(10, Digits() - 1)
            if _s_OnCalculate_point is _UNSET:
                _s_OnCalculate_point = Point()
            if rates_total != prev_calculated:
                _s_OnCalculate_open = price[rates_total - 3]
                _s_OnCalculate_close = price[rates_total - 2]
                _s_OnCalculate_open = (_fdiv(MathFloor(_s_OnCalculate_close * _s_OnCalculate_muldiv), _s_OnCalculate_muldiv) if (_s_OnCalculate_close > _s_OnCalculate_open) else _fdiv(MathCeil(_s_OnCalculate_close * _s_OnCalculate_muldiv), _s_OnCalculate_muldiv))
            _s_OnCalculate_close = price[rates_total - 1]
            _s_OnCalculate_close = (_fdiv(MathFloor(_s_OnCalculate_close * _s_OnCalculate_muldiv), _s_OnCalculate_muldiv) if (_s_OnCalculate_close > _s_OnCalculate_open) else _fdiv(MathCeil(_s_OnCalculate_close * _s_OnCalculate_muldiv), _s_OnCalculate_muldiv))
            if rates_total == prev_calculated and MathAbs(_s_OnCalculate_preClose - _s_OnCalculate_close) < _s_OnCalculate_point:
                return rates_total
            _s_OnCalculate_preClose = _s_OnCalculate_close
        EventChartCustom(ChartID_v, EventID, ((rates_total - prev_calculated - 1) if (rates_total != prev_calculated) else 0), 0.0, Symbol())
    return rates_total

# ---- static local variables
_s_OnCalculate_open = 0.0
_s_OnCalculate_close = 0.0
_s_OnCalculate_preClose = 0.0
_s_OnCalculate_muldiv = _UNSET
_s_OnCalculate_point = _UNSET


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class OnTick(_MQL5Indicator):
    name = 'OnTick'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ChartID_v': 0,
        'EventID': 0,
        'Pips': False,
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

