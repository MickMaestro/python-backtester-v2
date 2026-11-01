"""fx_sniper_ergodic_cci — converted from MQL5: MQL5 Indicators/FX_Sniper_Ergodic_CCI/fx_sniper_ergodic_cci.mq5

Louw Coetzer aka FX Sniper
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [255], 2: [13382297]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'CCI', 2: 'FX Sniper Ergo/CCI'}, 'levels': [], 'description': ['Louw Coetzer aka FX Sniper'], 'name': 'fx_sniper_ergodic_cci', 'source': 'MQL5 Indicators/FX_Sniper_Ergodic_CCI/fx_sniper_ergodic_cci.mq5', 'folder': 'FX_Sniper_Ergodic_CCI', 'inputs': [{'mql': 'pq', 'py': 'pq', 'param': 'pq', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'pr', 'py': 'pr', 'param': 'pr', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'ps', 'py': 'ps', 'param': 'ps', 'type': 'uint', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'CCI_period', 'py': 'CCI_period', 'param': 'CCI_period', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
pq = _input('pq', 2)
pr = _input('pr', 14)
ps = _input('ps', 5)
CCI_period = _input('CCI_period', 14)
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
CCIBuffer = Arr(0, 0.0)
ErgoCCIBuffer = Arr(0, 0.0)
CCI_Handle = 0
min_rates_total = 0

def OnInit():
    global CCI_Handle, min_rates_total
    min_rates_total = _int(CCI_period + 1 + pr + pq + ps)
    CCI_Handle = iCCI(None, 0, CCI_period, PRICE_TYPICAL)
    if CCI_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the CCI indicator')
    SetIndexBuffer(0, CCIBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(CCIBuffer, True)
    SetIndexBuffer(1, ErgoCCIBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ErgoCCIBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'FX Sniper Ergo/CCI')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(CCI_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    MaxBarA = 0
    MaxBarB = 0
    MaxBarC = 0
    dc = 0.0
    absdc = 0.0
    e1dc = 0.0
    e1absdc = 0.0
    e2dc = 0.0
    e2absdc = 0.0
    e3dc = 0.0
    e3absdc = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = _int(rates_total - CCI_period - 1)
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    MaxBarA = _int(rates_total - min_rates_total - CCI_period - 1)
    MaxBarB = _int(MaxBarA - pq)
    MaxBarC = _int(MaxBarB - pr)
    ArraySetAsSeries(close, True)
    if CopyBuffer(CCI_Handle, 0, 0, to_copy, CCIBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        dc = close[bar] - close[bar + 1]
        absdc = MathAbs(dc)
        e1dc = EMA1.EMASeries(MaxBarA, prev_calculated, rates_total, pq, dc, bar, True)
        e1absdc = EMA2.EMASeries(MaxBarA, prev_calculated, rates_total, pq, absdc, bar, True)
        e2dc = EMA3.EMASeries(MaxBarB, prev_calculated, rates_total, pr, e1dc, bar, True)
        e2absdc = EMA4.EMASeries(MaxBarB, prev_calculated, rates_total, pr, e1absdc, bar, True)
        e3dc = EMA3.EMASeries(MaxBarC, prev_calculated, rates_total, ps, e2dc, bar, True)
        e3absdc = EMA4.EMASeries(MaxBarC, prev_calculated, rates_total, ps, e2absdc, bar, True)
        if e3absdc:
            ErgoCCIBuffer[bar] = _fdiv(450 * e3dc, e3absdc)
        else:
            ErgoCCIBuffer[bar] = 50.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
EMA1 = _alloc(CMoving_Average)
EMA1.__init__()
EMA2 = _alloc(CMoving_Average)
EMA2.__init__()
EMA3 = _alloc(CMoving_Average)
EMA3.__init__()
EMA4 = _alloc(CMoving_Average)
EMA4.__init__()
EMA5 = _alloc(CMoving_Average)
EMA5.__init__()
EMA6 = _alloc(CMoving_Average)
EMA6.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FxSniperErgodicCci(_MQL5Indicator):
    name = 'fx_sniper_ergodic_cci'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'pq': 2,
        'pr': 14,
        'ps': 5,
        'CCI_period': 14,
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

