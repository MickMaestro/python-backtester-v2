"""darvasboxes — converted from MQL5: MQL5 Indicators/Darvas Box/darvasboxes.mq5

Copyright: Copyright © 2004, MetaQuotes Software Corp.; Link: http://www.metaquotes.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2004, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [16711680], 2: [16711935]}, 'widths': {1: 2, 2: 2}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Upper DarvasBoxes', 2: 'Lower DarvasBoxes'}, 'levels': [], 'description': [], 'name': 'darvasboxes', 'source': 'MQL5 Indicators/Darvas Box/darvasboxes.mq5', 'folder': 'Darvas Box', 'inputs': [{'mql': 'symmetry', 'py': 'symmetry', 'param': 'symmetry', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
symmetry = _input('symmetry', False)
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
UpperBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
start = 2

def OnInit():
    SetIndexBuffer(0, UpperBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, start)
    PlotIndexSetString(0, PLOT_LABEL, 'Upper DarvasBoxes')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(UpperBuffer, True)
    SetIndexBuffer(1, LowerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, start)
    PlotIndexSetString(1, PLOT_LABEL, 'Lower DarvasBoxes')
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(LowerBuffer, True)
    shortname = 'DarvasBoxes'
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
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - start
        _s_OnCalculate_BOX_TOP = high[limit + 1]
        _s_OnCalculate_BOX_BUTTOM = low[limit + 1]
        _s_OnCalculate_STATE = 1
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
        _sw1 = _s_OnCalculate_state
        if _sw1 == 1:
            _s_OnCalculate_box_top = high[bar]
            if symmetry:
                _s_OnCalculate_box_bottom = low[bar]
        elif _sw1 == 2:
            if _s_OnCalculate_box_top <= high[bar]:
                _s_OnCalculate_box_top = high[bar]
        elif _sw1 == 3:
            if _s_OnCalculate_box_top > high[bar]:
                _s_OnCalculate_box_bottom = low[bar]
            else:
                _s_OnCalculate_box_top = high[bar]
        elif _sw1 == 4:
            if _s_OnCalculate_box_top > high[bar]:
                if _s_OnCalculate_box_bottom >= low[bar]:
                    _s_OnCalculate_box_bottom = low[bar]
            else:
                _s_OnCalculate_box_top = high[bar]
        elif _sw1 == 5:
            if _s_OnCalculate_box_top > high[bar]:
                if _s_OnCalculate_box_bottom >= low[bar]:
                    _s_OnCalculate_box_bottom = low[bar]
            else:
                _s_OnCalculate_box_top = high[bar]
            _s_OnCalculate_state = 0
        UpperBuffer[bar] = _s_OnCalculate_box_top
        LowerBuffer[bar] = _s_OnCalculate_box_bottom
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


class Darvasboxes(_MQL5Indicator):
    name = 'darvasboxes'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'symmetry': False,
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

