"""darvasboxes_system — converted from MQL5: MQL5 Indicators/DarvasBoxes_System/darvasboxes_system.mq5

The breakthrough system using the DarvasBoxes indicator
Copyright: Copyright © 2013, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2013, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 1, 4: 11}, 'colors': {1: [16119285], 2: [7451452], 3: [16711935], 4: [9639167, 8388736, 8421504, 13434880, 16748574]}, 'widths': {2: 2, 3: 2, 4: 2}, 'styles': {2: 0, 3: 0, 4: 0}, 'labels': {1: 'DarvasBoxes', 2: 'Upper DarvasBoxes', 3: 'Lower DarvasBoxes', 4: 'DarvasBoxes_BARS'}, 'levels': [], 'description': ['The breakthrough system using the DarvasBoxes indicator'], 'name': 'darvasboxes_system', 'source': 'MQL5 Indicators/DarvasBoxes_System/darvasboxes_system.mq5', 'folder': 'DarvasBoxes_System', 'inputs': [{'mql': 'symmetry', 'py': 'symmetry', 'param': 'symmetry', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
symmetry = _input('symmetry', True)
Shift = _input('Shift', 2)
Up1Buffer = Arr(0, 0.0)
Dn1Buffer = Arr(0, 0.0)
Up2Buffer = Arr(0, 0.0)
Dn2Buffer = Arr(0, 0.0)
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(2 + Shift)
    SetIndexBuffer(0, Up1Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Up1Buffer, True)
    SetIndexBuffer(1, Dn1Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Dn1Buffer, True)
    SetIndexBuffer(2, Up2Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Up2Buffer, True)
    SetIndexBuffer(3, Dn2Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Dn2Buffer, True)
    SetIndexBuffer(4, UpIndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpIndBuffer, True)
    SetIndexBuffer(5, DnIndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnIndBuffer, True)
    SetIndexBuffer(6, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_SHIFT, 0)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    shortname = Box("")
    StringConcatenate(shortname, 'DarvasBoxes(', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_BOX_BUTTOM, _s_OnCalculate_BOX_TOP, _s_OnCalculate_STATE, _s_OnCalculate_box_bottom, _s_OnCalculate_box_top, _s_OnCalculate_state
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        _s_OnCalculate_BOX_TOP = high[limit + 1]
        _s_OnCalculate_BOX_BUTTOM = low[limit + 1]
        _s_OnCalculate_STATE = 1
    else:
        limit = rates_total - prev_calculated
    _s_OnCalculate_state = _s_OnCalculate_STATE
    _s_OnCalculate_box_top = _s_OnCalculate_BOX_TOP
    _s_OnCalculate_box_bottom = _s_OnCalculate_BOX_BUTTOM
    for bar in range(limit, 0 - 1, -1):
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
        Up1Buffer[bar] = _s_OnCalculate_box_top
        Dn1Buffer[bar] = _s_OnCalculate_box_bottom
        Up2Buffer[bar] = _s_OnCalculate_box_top
        Dn2Buffer[bar] = _s_OnCalculate_box_bottom
        _s_OnCalculate_state += 1
        if bar == 1:
            _s_OnCalculate_STATE = _s_OnCalculate_state
            _s_OnCalculate_BOX_TOP = _s_OnCalculate_box_top
            _s_OnCalculate_BOX_BUTTOM = _s_OnCalculate_box_bottom
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= _int(Shift)
    for bar in range(limit, 0 - 1, -1):
        clr = 2
        UpIndBuffer[bar] = 0.0
        DnIndBuffer[bar] = 0.0
        if close[bar] > Up1Buffer[bar + Shift]:
            if open[bar] < close[bar]:
                clr = 4
            else:
                clr = 3
            UpIndBuffer[bar] = high[bar]
            DnIndBuffer[bar] = low[bar]
        if close[bar] < Dn1Buffer[bar + Shift]:
            if open[bar] > close[bar]:
                clr = 0
            else:
                clr = 1
            UpIndBuffer[bar] = high[bar]
            DnIndBuffer[bar] = low[bar]
        ColorIndBuffer[bar] = clr
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


class DarvasboxesSystem(_MQL5Indicator):
    name = 'darvasboxes_system'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'symmetry': True,
        'Shift': 2,
    }

