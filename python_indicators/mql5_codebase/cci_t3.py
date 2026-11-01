"""cci_t3 — converted from MQL5: MQL5 Indicators/CCI T3/cci_t3.mq5

CCI T3 Indicator
Copyright: Alextp., 2012 г.; Link: atopunov@mail.ru; Version: 1.1

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Alextp., 2012 г.', 'link': 'atopunov@mail.ru', 'version': '1.1', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 2}, 'types': {1: 10, 2: 8}, 'colors': {1: [4294967295, 65280, 255], 2: [4294967295, 0]}, 'widths': {1: 2, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'CCI T3', 2: 'MA'}, 'levels': [], 'description': ['CCI T3 Indicator'], 'name': 'cci_t3', 'source': 'MQL5 Indicators/CCI T3/cci_t3.mq5', 'folder': 'CCI T3', 'inputs': [{'mql': 'CCI_Period', 'py': 'CCI_Period', 'param': 'CCI_Period', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'CCI_Price_Type', 'py': 'CCI_Price_Type', 'param': 'CCI_Price_Type', 'type': 'int', 'default': 6, 'label': '', 'sinput': False}, {'mql': 'T3_Period', 'py': 'T3_Period', 'param': 'T3_Period', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'Koeff_B', 'py': 'Koeff_B', 'param': 'Koeff_B', 'type': 'double', 'default': 0.618, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CCI_Period = _input('CCI_Period', 14)
CCI_Price_Type = _input('CCI_Price_Type', PRICE_TYPICAL)
T3_Period = _input('T3_Period', 5)
Koeff_B = _input('Koeff_B', 0.618)
CCIBuff = Arr(0, 0.0)
MCCIBuff = Arr(0, 0.0)
MCCIColorBuff = Arr(0, 0.0)
MABuff = Arr(0, 0.0)
MAColorBuff = Arr(0, 0.0)
cci_handler = 0
cci_bars_calculated = 0  # number of values in the CCI indicator
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
n = 0
start = 0
values_to_copy = 0

def OnInit():
    global b2, b3, c1, c2, c3, c4, cci_handler, n, w1, w2
    Comment('')
    SetIndexBuffer(0, MCCIBuff, INDICATOR_DATA)
    SetIndexBuffer(1, MCCIColorBuff, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, MABuff, INDICATOR_DATA)
    SetIndexBuffer(3, MAColorBuff, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, CCIBuff, INDICATOR_CALCULATIONS)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'CCI T3( CCI_Period = ' + _str(CCI_Period) + ', T3_Period = ' + _str(T3_Period) + ' )')
    cci_handler = iCCI(Symbol(), Period(), CCI_Period, CCI_Price_Type)
    if cci_handler == INVALID_HANDLE:
        Print('Failed to create the CCI indicator')
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
    ChartRedraw()
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_error, e1, e2, e3, e4, e5, e6, start
    if prev_calculated == 0:
        _s_OnCalculate_error = True
    if _s_OnCalculate_error:
        start = 0
        _s_OnCalculate_error = False
    else:
        start = prev_calculated - 1
    if CopyBuffer(cci_handler, 0, 0, rates_total - start, CCIBuff) == -1:
        _s_OnCalculate_error = True
        return rates_total
    if prev_calculated == 0 or CheakNewBar(Symbol(), Period(), _GlobRef(globals(), '_s_OnCalculate_last_bar_datetime_chart')) == 1:
        for i in range(start, rates_total - 1):
            e1 = (w1 * CCIBuff[i]) + (w2 * e1)
            e2 = (w1 * e1) + (w2 * e2)
            e3 = (w1 * e2) + (w2 * e3)
            e4 = (w1 * e3) + (w2 * e4)
            e5 = (w1 * e4) + (w2 * e5)
            e6 = (w1 * e5) + (w2 * e6)
            MCCIBuff[i] = (c1 * e6) + (c2 * e5) + (c3 * e4) + (c4 * e3)
            MABuff[i] = MCCIBuff[i]
            MAColorBuff[i] = 1.0
            if MCCIBuff[i] > 0.0:
                MCCIColorBuff[i] = 1.0
            elif MCCIBuff[i] < 0.0:
                MCCIColorBuff[i] = 2.0
            else:
                MCCIColorBuff[i] = 0.0
        MCCIBuff[rates_total - 1] = 0.0
        MCCIColorBuff[rates_total - 1] = 0.0
        MABuff[rates_total - 1] = MCCIBuff[rates_total - 1]
        MAColorBuff[rates_total - 1] = 0.0
    return rates_total

def OnDeinit(_reason):
    if cci_handler != INVALID_HANDLE:
        IndicatorRelease(cci_handler)
    ChartRedraw()

def CheakNewBar(_symbol, _period, _last_dt):
    curr_time = SeriesInfoInteger(_symbol, _period, SERIES_LASTBAR_DATE)
    if curr_time > _last_dt.v:
        _last_dt.v = curr_time
        return 1
    return 0

# ---- static local variables
_s_OnCalculate_last_bar_datetime_chart = 0
_s_OnCalculate_error = True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CciT3(_MQL5Indicator):
    name = 'cci_t3'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'CCI_Period': 14,
        'CCI_Price_Type': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=6),
        'T3_Period': 5,
        'Koeff_B': 0.618,
    }

