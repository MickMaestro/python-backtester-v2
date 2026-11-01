"""marsicd — converted from MQL5: MQL5 Indicators/MARSICD/marsicd.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 6, 'indicator_minimum': -100.0, 'indicator_maximum': 100.0}, 'types': {1: 3, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'colors': {1: [8421504], 2: [13850042], 3: [16748574], 4: [16748574], 5: [255], 6: [65280]}, 'widths': {1: 2, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, 'styles': {1: 0, 2: 4, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'RSI', 2: 'Signal RSI', 3: 'Up RSI', 4: 'Dn RSI', 5: 'Up Signal RSI', 6: 'Dn Signal RSI'}, 'levels': [70.0, 30.0, -30.0, -70.0, 50.0, -50.0], 'description': [], 'name': 'marsicd', 'source': 'MQL5 Indicators/MARSICD/marsicd.mq5', 'folder': 'MARSICD', 'inputs': [{'mql': 'MAMethod', 'py': 'MAMethod', 'param': 'MAMethod', 'type': 'int', 'default': 3, 'label': 'smoothing method', 'sinput': False}, {'mql': 'ARSI_PERIOD', 'py': 'ARSI_PERIOD', 'param': 'ARSI_PERIOD', 'type': 'uint', 'default': 14, 'label': 'RSI A period', 'sinput': False}, {'mql': 'RRSI_PERIOD', 'py': 'RRSI_PERIOD', 'param': 'RRSI_PERIOD', 'type': 'uint', 'default': 14, 'label': 'RSI R period', 'sinput': False}, {'mql': 'AMA_PERIOD', 'py': 'AMA_PERIOD', 'param': 'AMA_PERIOD', 'type': 'uint', 'default': 5, 'label': 'signal A period', 'sinput': False}, {'mql': 'RMA_PERIOD', 'py': 'RMA_PERIOD', 'param': 'RMA_PERIOD', 'type': 'uint', 'default': 5, 'label': 'signal R period', 'sinput': False}, {'mql': 'sMAD_PERIOD', 'py': 'sMAD_PERIOD', 'param': 'sMAD_PERIOD', 'type': 'uint', 'default': 21, 'label': 'signal period for the histogram', 'sinput': False}, {'mql': 'MPhase', 'py': 'MPhase', 'param': 'MPhase', 'type': 'uint', 'default': 15, 'label': 'smoothing parameter,', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
MAMethod = _input('MAMethod', MODE_LWMA)  # smoothing method
ARSI_PERIOD = _input('ARSI_PERIOD', 14)  # RSI A period
RRSI_PERIOD = _input('RRSI_PERIOD', 14)  # RSI R period
AMA_PERIOD = _input('AMA_PERIOD', 5)  # signal A period
RMA_PERIOD = _input('RMA_PERIOD', 5)  # signal R period
sMAD_PERIOD = _input('sMAD_PERIOD', 21)  # signal period for the histogram
MPhase = _input('MPhase', 15)  # smoothing parameter,
ARSI_BUF = Arr(0, 0.0)
RRSI_BUF = Arr(0, 0.0)
AMA_BUF = Arr(0, 0.0)
RMA_BUF = Arr(0, 0.0)
Delta = Arr(0, 0.0)
sMAD = Arr(0, 0.0)
ARSI_Handle = 0
RRSI_Handle = 0
min_rates_total = 0
min_rates_total1 = 0
min_rates_total2 = 0

def OnInit():
    global ARSI_Handle, RRSI_Handle, min_rates_total, min_rates_total1, min_rates_total2
    min_rates_total1 = _int(MathMax(ARSI_PERIOD, RRSI_PERIOD))
    min_rates_total2 = min_rates_total1 + MathMax(XMA.GetStartBars(MAMethod, AMA_PERIOD, MPhase), XMA.GetStartBars(MAMethod, RMA_PERIOD, MPhase))
    min_rates_total = min_rates_total2 + XMA.GetStartBars(MAMethod, sMAD_PERIOD, MPhase)
    ARSI_Handle = iRSI(None, 0, ARSI_PERIOD, PRICE_WEIGHTED)
    if ARSI_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the RSI indicator')
    RRSI_Handle = iRSI(None, 0, RRSI_PERIOD, PRICE_WEIGHTED)
    if RRSI_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the RSI indicator')
    SetIndexBuffer(0, Delta, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Delta, True)
    SetIndexBuffer(1, sMAD, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(sMAD, True)
    SetIndexBuffer(2, RRSI_BUF, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(RRSI_BUF, True)
    SetIndexBuffer(3, ARSI_BUF, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ARSI_BUF, True)
    SetIndexBuffer(4, RMA_BUF, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(RMA_BUF, True)
    SetIndexBuffer(5, AMA_BUF, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(AMA_BUF, True)
    shortname = 'MARSICD'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(ARSI_Handle) < rates_total or BarsCalculated(RRSI_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    maxbar1 = 0
    maxbar2 = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ARSI_Handle, 0, 0, to_copy, ARSI_BUF) <= 0:
        return 0
    if CopyBuffer(RRSI_Handle, 0, 0, to_copy, RRSI_BUF) <= 0:
        return 0
    maxbar1 = rates_total - 1 - min_rates_total1
    maxbar2 = maxbar1 - min_rates_total2
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        RRSI_BUF[bar] *= -1
        RRSI_BUF[bar] += 100
        AMA_BUF[bar] = AXMA.XMASeries(maxbar1, prev_calculated, rates_total, MAMethod, MPhase, AMA_PERIOD, ARSI_BUF[bar], bar, True)
        RMA_BUF[bar] = RXMA.XMASeries(maxbar1, prev_calculated, rates_total, MAMethod, MPhase, RMA_PERIOD, RRSI_BUF[bar], bar, True)
        Delta[bar] = AMA_BUF[bar] - RMA_BUF[bar]
        sMAD[bar] = XMA.XMASeries(maxbar2, prev_calculated, rates_total, MAMethod, MPhase, sMAD_PERIOD, Delta[bar], bar, True)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
XMA = _alloc(CXMA)
XMA.__init__()
AXMA = _alloc(CXMA)
AXMA.__init__()
RXMA = _alloc(CXMA)
RXMA.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Marsicd(_MQL5Indicator):
    name = 'marsicd'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MAMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # smoothing method
        'ARSI_PERIOD': 14,  # RSI A period
        'RRSI_PERIOD': 14,  # RSI R period
        'AMA_PERIOD': 5,  # signal A period
        'RMA_PERIOD': 5,  # signal R period
        'sMAD_PERIOD': 21,  # signal period for the histogram
        'MPhase': 15,  # smoothing parameter,
    }
    y_range = (-100.0, 100.0)

