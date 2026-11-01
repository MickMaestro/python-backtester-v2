"""H_L_ — converted from MQL5: MQL5 Indicators/H_L_/H_L_.mq5

Copyright: Copyright © 2004, MetaQuotes Software Corp.; Link: http://www.metaquotes.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2004, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 1}, 'colors': {1: [16748574], 2: [16711680], 3: [255], 4: [16711935]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1}, 'styles': {1: 0, 3: 0, 4: 0}, 'labels': {1: 'High 2', 2: 'High 1', 3: 'Low 1', 4: 'Low 2'}, 'levels': [], 'description': [], 'name': 'H_L_', 'source': 'MQL5 Indicators/H_L_/H_L_.mq5', 'folder': 'H_L_', 'inputs': [{'mql': 'S', 'py': 'S', 'param': 'S', 'type': 'uint', 'default': 4, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
S = _input('S', 4)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
Buffer_0 = Arr(0, 0.0)
Buffer_1 = Arr(0, 0.0)
Buffer_2 = Arr(0, 0.0)
Buffer_3 = Arr(0, 0.0)
MaRo = 0.0
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(S)
    SetIndexBuffer(0, Buffer_0, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, Buffer_1, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, Buffer_2, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(3, Buffer_3, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(Buffer_0, True)
    ArraySetAsSeries(Buffer_1, True)
    ArraySetAsSeries(Buffer_2, True)
    ArraySetAsSeries(Buffer_3, True)
    shortname = Box("")
    StringConcatenate(shortname, 'H_L_(', S, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    limit = rates_total - 1 - _int(S)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    A1 = 0
    A1d = 0
    A2 = 0
    A2d = 0
    V1 = 0
    V1d = 0
    V2 = 0
    V2d = 0
    AX = 0
    AXd = 0
    BX = 0
    BXd = 0
    CX = 0
    CXd = 0
    DX = 0
    DXd = 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Buffer_0[bar] = high[bar]
        Buffer_1[bar] = low[bar]
        Buffer_2[bar] = (open[bar] + close[bar]) / 2
        Buffer_3[bar] = (open[bar] + close[bar]) / 2
    else:
        bar = _range_end(bar, 0 - 1, -1)
    for cnt2 in range(0, _int(S)):
        AX = 0
        BX = 0
        CX = 0
        DX = 0
        A1 = 0
        A2 = 0
        V1 = 0
        V2 = 0
        AXd = 0
        BXd = 0
        CXd = 0
        DXd = 0
        A1d = 0
        A2d = 0
        V1d = 0
        V2d = 0
        bar = limit - 1
        for bar in range(bar, 0 - 1, -1):
            if bar > 0 and Buffer_0[bar] < Buffer_0[bar - 1]:
                AX = bar - 1
                BX = AX
            if (bar > 0 and Buffer_0[bar] == Buffer_0[bar - 1]) and AX > 0:
                BX = bar - 1
            if (bar > 0 and Buffer_0[bar] > Buffer_0[bar - 1]) and AX > 0:
                if A1 == 0:
                    A1 = _idiv(AX + BX, 2)
                if A1 > 0:
                    A2 = _idiv(AX + BX, 2)
                if A1 > 0 and A2 > 0:
                    for cnt4 in range(1, A1 - A2 + 1):
                        Buffer_0[A2 + cnt4] = Buffer_0[A2] + _fdiv((Buffer_0[A1] - Buffer_0[A2]) * cnt4, A1 - A2)
                    A1 = A2
                    A2 = 0
            if bar > 0 and Buffer_1[bar] > Buffer_1[bar - 1]:
                CX = bar - 1
                DX = CX
            if (bar > 0 and Buffer_1[bar] == Buffer_1[bar - 1]) and CX > 0:
                DX = bar - 1
            if (bar > 0 and Buffer_1[bar] < Buffer_1[bar - 1]) and CX > 0:
                if V1 == 0:
                    V1 = _idiv(CX + DX, 2)
                if V1 > 0:
                    V2 = _idiv(CX + DX, 2)
                if V1 > 0 and V2 > 0:
                    for cnt5 in range(1, V1 - V2 + 1):
                        Buffer_1[V2 + cnt5] = Buffer_1[V2] + _fdiv((Buffer_1[V1] - Buffer_1[V2]) * cnt5, V1 - V2)
                    V1 = V2
                    V2 = 0
            if bar > 0 and Buffer_2[bar] < Buffer_2[bar - 1]:
                AXd = bar - 1
                BXd = AXd
            if (bar > 0 and Buffer_2[bar] == Buffer_2[bar - 1]) and AXd > 0:
                BXd = bar - 1
            if (bar > 0 and Buffer_2[bar] > Buffer_2[bar - 1]) and AXd > 0:
                if A1d == 0:
                    A1d = _idiv(AXd + BXd, 2)
                if A1d > 0:
                    A2d = _idiv(AXd + BXd, 2)
                if A1d > 0 and A2d > 0:
                    for cnt41 in range(1, A1d - A2d + 1):
                        Buffer_2[A2d + cnt41] = Buffer_2[A2d] + _fdiv((Buffer_2[A1d] - Buffer_2[A2d]) * cnt41, A1d - A2d)
                    A1d = A2d
                    A2d = 0
            if bar > 0 and Buffer_3[bar] > Buffer_3[bar - 1]:
                CXd = bar - 1
                DXd = CXd
            if (bar > 0 and Buffer_3[bar] == Buffer_3[bar - 1]) and CXd > 0:
                DXd = bar - 1
            if (bar > 0 and Buffer_3[bar] < Buffer_3[bar - 1]) and CXd > 0:
                if V1d == 0:
                    V1d = _idiv(CXd + DXd, 2)
                if V1d > 0:
                    V2d = _idiv(CXd + DXd, 2)
                if V1d > 0 and V2d > 0:
                    for cnt51 in range(1, V1d - V2d + 1):
                        Buffer_3[V2d + cnt51] = Buffer_3[V2d] + _fdiv((Buffer_3[V1d] - Buffer_3[V2d]) * cnt51, V1d - V2d)
                    V1d = V2d
                    V2d = 0
        else:
            bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HL(_MQL5Indicator):
    name = 'H_L_'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'S': 4,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

