"""DarvasBoxesCloud — converted from MQL5: MQL5 Indicators/DarvasBoxesCloud/DarvasBoxesCloud.mq5

Copyright: Copyright © 2004, MetaQuotes Software Corp.; Link: http://www.metaquotes.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2004, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 5}, 'types': {1: 7, 2: 1, 3: 1, 4: 1, 5: 7}, 'colors': {1: [16436871], 2: [16748574], 3: [8421504], 4: [2763429], 5: [14053594]}, 'widths': {2: 2, 3: 2, 4: 2}, 'styles': {2: 0, 3: 0, 4: 0}, 'labels': {1: 'Upper Cloud', 2: 'Upper DarvasBox', 3: 'Middle DarvasBox', 4: 'Lower DarvasBox', 5: 'Lower Cloud'}, 'levels': [], 'description': [], 'name': 'DarvasBoxesCloud', 'source': 'MQL5 Indicators/DarvasBoxesCloud/DarvasBoxesCloud.mq5', 'folder': 'DarvasBoxesCloud', 'inputs': [{'mql': 'symmetry', 'py': 'symmetry', 'param': 'symmetry', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
symmetry = _input('symmetry', True)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
ExtUp1Buffer = Arr(0, 0.0)
ExtUp2Buffer = Arr(0, 0.0)
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
ExtCBuffer = Arr(0, 0.0)
ExtDn1Buffer = Arr(0, 0.0)
ExtDn2Buffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, ExtUp1Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtUp2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ExtUp1Buffer, True)
    ArraySetAsSeries(ExtUp2Buffer, True)
    SetIndexBuffer(2, ExtABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ExtABuffer, True)
    SetIndexBuffer(3, ExtBBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ExtBBuffer, True)
    SetIndexBuffer(4, ExtCBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ExtCBuffer, True)
    SetIndexBuffer(5, ExtDn1Buffer, INDICATOR_DATA)
    SetIndexBuffer(6, ExtDn2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ExtDn1Buffer, True)
    ArraySetAsSeries(ExtDn2Buffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'DarvasBoxesCloud')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_BOX_BUTTOM, _s_OnCalculate_BOX_TOP, _s_OnCalculate_STATE, _s_OnCalculate_box_bottom, _s_OnCalculate_box_top, _s_OnCalculate_state
    if rates_total < min_rates_total:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    limit = 0
    bar = 0
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
    bar = limit
    for bar in range(bar, 0 - 1, -1):
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
        ExtABuffer[bar] = _s_OnCalculate_box_top
        ExtCBuffer[bar] = _s_OnCalculate_box_bottom
        ExtBBuffer[bar] = (_s_OnCalculate_box_top + _s_OnCalculate_box_bottom) / 2.0
        ExtUp1Buffer[bar] = ExtABuffer[bar]
        ExtUp2Buffer[bar] = ExtBBuffer[bar]
        ExtDn1Buffer[bar] = ExtBBuffer[bar]
        ExtDn2Buffer[bar] = ExtCBuffer[bar]
        _s_OnCalculate_state += 1
        if bar == 1:
            _s_OnCalculate_STATE = _s_OnCalculate_state
            _s_OnCalculate_BOX_TOP = _s_OnCalculate_box_top
            _s_OnCalculate_BOX_BUTTOM = _s_OnCalculate_box_bottom
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


class DarvasBoxesCloud(_MQL5Indicator):
    name = 'DarvasBoxesCloud'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'symmetry': True,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

