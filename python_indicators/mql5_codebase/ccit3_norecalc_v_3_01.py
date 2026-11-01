"""ccit3_norecalc_v_3-01 — converted from MQL5: MQL5 Indicators/CCIT3_noReCalc/ccit3_norecalc_v_3-01.mq5

Copyright: Copyright © 2012, Im_hungry; Link: CCIT3_noReCalc_v_3-01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2012, Im_hungry', 'link': 'CCIT3_noReCalc_v_3-01', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 10, 2: 8}, 'colors': {1: [4294967295, 65280, 255], 2: [4294967295, 65535]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'CCI T3', 2: 'MA'}, 'levels': [], 'description': [], 'name': 'ccit3_norecalc_v_3-01', 'source': 'MQL5 Indicators/CCIT3_noReCalc/ccit3_norecalc_v_3-01.mq5', 'folder': 'CCIT3_noReCalc', 'inputs': [{'mql': 'CCI_Period', 'py': 'CCI_Period', 'param': 'CCI_Period', 'type': 'int', 'default': 170, 'label': '', 'sinput': False}, {'mql': 'CCI_Price_Type', 'py': 'CCI_Price_Type', 'param': 'CCI_Price_Type', 'type': 'int', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'T3_Period', 'py': 'T3_Period', 'param': 'T3_Period', 'type': 'int', 'default': 80, 'label': '', 'sinput': False}, {'mql': 'Koeff_B', 'py': 'Koeff_B', 'param': 'Koeff_B', 'type': 'double', 'default': 0.618, 'label': '', 'sinput': False}, {'mql': 'Max_bars_calc', 'py': 'Max_bars_calc', 'param': 'Max_bars_calc', 'type': 'int', 'default': 500, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CCI_Period = _input('CCI_Period', 170)
CCI_Price_Type = _input('CCI_Price_Type', PRICE_TYPICAL)
T3_Period = _input('T3_Period', 80)
Koeff_B = _input('Koeff_B', 0.618)
Max_bars_calc = _input('Max_bars_calc', 500)
CCIBuff = Arr(0, 0.0)
MCCIBuff = Arr(0, 0.0)
MCCIColorBuff = Arr(0, 0.0)
MABuff = Arr(0, 0.0)
MAColorBuff = Arr(0, 0.0)
e1 = 0.0
e2 = 0.0
e3 = 0.0
e4 = 0.0
e5 = 0.0
e6 = 0.0
b2 = 0.0
b3 = 0.0
c1 = 0.0
c2 = 0.0
c3 = 0.0
c4 = 0.0
w1 = 0.0
w2 = 0.0
cci_handler = 0
n = 0
start = 0
flag_start = 0

def OnInit():
    global b2, b3, c1, c2, c3, c4, cci_handler, flag_start, n, w1, w2
    SetIndexBuffer(0, MCCIBuff, INDICATOR_DATA)
    SetIndexBuffer(1, MCCIColorBuff, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, MABuff, INDICATOR_DATA)
    SetIndexBuffer(3, MAColorBuff, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, CCIBuff, INDICATOR_CALCULATIONS)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'CCIT3_noReCalc (CCI_Period =' + _str(CCI_Period) + ', T3_Period =' + _str(T3_Period) + ')')
    cci_handler = iCCI(Symbol(), Period(), CCI_Period, CCI_Price_Type)
    if cci_handler == INVALID_HANDLE:
        Print('Error in loading CCIT3_noReCalc_v_3-01 :', GetLastError())
        return -1
    b2 = Koeff_B * Koeff_B
    b3 = b2 * Koeff_B
    c1 = -b3
    c2 = 3.0 * (b2 + b3)
    c3 = -3.0 * ((2.0 * b2) + Koeff_B + b3)
    c4 = 1.0 + (3.0 * Koeff_B) + b3 + (3.0 * b2)
    n = T3_Period
    if n < 1:
        n = 1
    else:
        n = _idiv(n + 1, 2)
    w1 = _fdiv(2.0, n + 1.0)
    w2 = 1.0 - w1
    flag_start = 0
    ChartRedraw()
    return 0

def OnDeinit(_reason):
    if cci_handler != INVALID_HANDLE:
        IndicatorRelease(cci_handler)
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_last_bar, e1, e2, e3, e4, e5, e6, flag_start, start
    ArraySetAsSeries(CCIBuff, True)
    ArraySetAsSeries(MCCIBuff, True)
    ArraySetAsSeries(MABuff, True)
    ArraySetAsSeries(MAColorBuff, True)
    ArraySetAsSeries(MCCIColorBuff, True)
    ArraySetAsSeries(time, True)
    if flag_start == 0:
        ArrayInitialize(MCCIBuff, 0.0)
        ArrayInitialize(MABuff, 0.0)
        if (Bars(Symbol(), None) - 1) < Max_bars_calc:
            start = Bars(Symbol(), None) - 10
        else:
            start = Max_bars_calc - 10
        flag_start = 1
        if CopyBuffer(cci_handler, 0, 0, start, CCIBuff) <= 0:
            return rates_total
    else:
        start = 1
        if CopyBuffer(cci_handler, 0, 0, 2, CCIBuff) <= 0:
            return rates_total
    if time[0] > _s_OnCalculate_last_bar:
        _s_OnCalculate_last_bar = time[0]
        for i in range(0, start + 1):
            e1 = 0.0
            e2 = 0.0
            e3 = 0.0
            e4 = 0.0
            e5 = 0.0
            e6 = 0.0
            if CCIBuff[i] < 1000:
                e1 = (w1 * CCIBuff[i]) + (w2 * e1)
                e2 = (w1 * e1) + (w2 * e2)
                e3 = (w1 * e2) + (w2 * e3)
                e4 = (w1 * e3) + (w2 * e4)
                e5 = (w1 * e4) + (w2 * e5)
                e6 = (w1 * e5) + (w2 * e6)
                MCCIBuff[i] = NormalizeDouble((c1 * e6) + (c2 * e5) + (c3 * e4) + (c4 * e3), Digits())
                MABuff[i] = MCCIBuff[i]
            else:
                MCCIBuff[i] = 0.0
                MABuff[i] = 0.0
            MAColorBuff[i] = 1.0
            if MCCIBuff[i] > 0:
                MCCIColorBuff[i] = 1.0
            else:
                if MCCIBuff[i] < 0:
                    MCCIColorBuff[i] = 2.0
                else:
                    MCCIColorBuff[i] = 0.0
    return rates_total

# ---- static local variables
_s_OnCalculate_last_bar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ccit3NorecalcV301(_MQL5Indicator):
    name = 'ccit3_norecalc_v_3-01'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'CCI_Period': 170,
        'CCI_Price_Type': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),
        'T3_Period': 80,
        'Koeff_B': 0.618,
        'Max_bars_calc': 500,
    }

