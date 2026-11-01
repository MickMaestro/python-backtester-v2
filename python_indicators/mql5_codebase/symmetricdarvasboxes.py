"""symmetricdarvasboxes — converted from MQL5: MQL5 Indicators/SymmetricDarvasBoxes/symmetricdarvasboxes.mq5

Copyright: Copyright © 2011, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711680], 2: [16711935]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Upper Symmetric DarvasBoxes', 2: 'Lower Symmetric DarvasBoxes'}, 'levels': [], 'description': [], 'name': 'symmetricdarvasboxes', 'source': 'MQL5 Indicators/SymmetricDarvasBoxes/symmetricdarvasboxes.mq5', 'folder': 'SymmetricDarvasBoxes', 'inputs': [{'mql': 'CPeriod', 'py': 'CPeriod', 'param': 'CPeriod', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'StartShift', 'py': 'StartShift', 'param': 'StartShift', 'type': 'int', 'default': 0, 'label': 'Period counting start shift', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CPeriod = _input('CPeriod', 5)
StartShift = _input('StartShift', 0)  # Period counting start shift
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
UpperBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
start = 2
StartShift_ = 0

def OnInit():
    global StartShift_
    if StartShift >= CPeriod:
        StartShift_ = _int(MathMod(StartShift, CPeriod))
    else:
        StartShift_ = StartShift
    SetIndexBuffer(0, UpperBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start)
    PlotIndexSetString(0, PLOT_LABEL, 'Upper Symmetric DarvasBoxes')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpperBuffer, True)
    SetIndexBuffer(1, LowerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, start)
    PlotIndexSetString(1, PLOT_LABEL, 'Lower Symmetric DarvasBoxes')
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(LowerBuffer, True)
    shortname = 'Symmetric DarvasBoxes'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_BOX_BUTTOM, _s_OnCalculate_BOX_TOP, _s_OnCalculate_STATE, _s_OnCalculate_box_bottom, _s_OnCalculate_box_top, _s_OnCalculate_state
    if rates_total < start:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    limit = 0
    bar = 0
    High = 0.0
    Low = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - start
        _s_OnCalculate_BOX_TOP = high[limit + 1]
        _s_OnCalculate_BOX_BUTTOM = low[limit + 1]
        _s_OnCalculate_STATE = StartShift_
    else:
        limit = rates_total - prev_calculated
    _s_OnCalculate_state = _s_OnCalculate_STATE
    _s_OnCalculate_box_top = _s_OnCalculate_BOX_TOP
    _s_OnCalculate_box_bottom = _s_OnCalculate_BOX_BUTTOM
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            _s_OnCalculate_STATE = _s_OnCalculate_state
            _s_OnCalculate_BOX_TOP = _s_OnCalculate_box_top
            _s_OnCalculate_BOX_BUTTOM = _s_OnCalculate_box_bottom
        High = high[bar]
        Low = low[bar]
        if _s_OnCalculate_state < CPeriod:
            if _s_OnCalculate_box_top <= High:
                _s_OnCalculate_box_top = High
            if _s_OnCalculate_box_bottom >= Low:
                _s_OnCalculate_box_bottom = Low
        else:
            _s_OnCalculate_box_top = High
            _s_OnCalculate_box_bottom = Low
            _s_OnCalculate_state = 0
        UpperBuffer[bar] = _s_OnCalculate_box_top
        LowerBuffer[bar] = _s_OnCalculate_box_bottom
        if bar != limit:
            _s_OnCalculate_state += 1
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_state = 0
_s_OnCalculate_STATE = 0
_s_OnCalculate_box_top = 0.0
_s_OnCalculate_box_bottom = 0.0
_s_OnCalculate_BOX_TOP = 0.0
_s_OnCalculate_BOX_BUTTOM = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Symmetricdarvasboxes(_MQL5Indicator):
    name = 'symmetricdarvasboxes'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CPeriod': 5,
        'StartShift': 0,  # Period counting start shift
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

