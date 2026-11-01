"""vqbars — converted from MQL5: MQL5 Indicators/VQ bars/vqbars.mq5

VQbars
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 12}, 'colors': {1: [8421504, 16711935, 16711680]}, 'widths': {1: 4}, 'styles': {}, 'labels': {1: 'VQbars Flat,VQbars Sell,VQbars Buy'}, 'levels': [], 'description': ['VQbars'], 'name': 'vqbars', 'source': 'MQL5 Indicators/VQ bars/vqbars.mq5', 'folder': 'VQ bars', 'inputs': [{'mql': 'VQMA_Method', 'py': 'VQMA_Method', 'param': 'VQMA_Method', 'type': 'int', 'default': 0, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'VQLength', 'py': 'VQLength', 'param': 'VQLength', 'type': 'int', 'default': 12, 'label': 'Smoothing depth', 'sinput': False}, {'mql': 'VQPhase', 'py': 'VQPhase', 'param': 'VQPhase', 'type': 'int', 'default': 15, 'label': 'Smoothing parameter', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Applied price', 'sinput': False}, {'mql': 'VQMomentum', 'py': 'VQMomentum', 'param': 'VQMomentum', 'type': 'int', 'default': 1, 'label': 'Momentum', 'sinput': False}, {'mql': 'Filter', 'py': 'Filter', 'param': 'Filter', 'type': 'uint', 'default': 5, 'label': 'Maximum deviation', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPLE = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPLE', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
VQMA_Method = _input('VQMA_Method', MODE_SMA)  # Smoothing method
VQLength = _input('VQLength', 12)  # Smoothing depth
VQPhase = _input('VQPhase', 15)  # Smoothing parameter
IPC = _input('IPC', PRICE_CLOSE)  # Applied price
VQMomentum = _input('VQMomentum', 1)  # Momentum
Filter = _input('Filter', 5)  # Maximum deviation
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
xmin_rates_total = 0
min_rates_total_ = 0

def OnInit():
    global min_rates_total, min_rates_total_, xmin_rates_total
    xmin_rates_total = XMAO.GetStartBars(VQMA_Method, VQLength, VQPhase)
    min_rates_total = xmin_rates_total + VQMomentum + 1
    min_rates_total_ = min_rates_total - 1
    XMAO.XMALengthCheck('VQLength', VQLength)
    XMAO.XMAPhaseCheck('VQPhase', VQPhase, VQMA_Method)
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 108)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'VQbars'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_SumVQ1_, _s_OnCalculate_trend1
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    trend0 = 0
    bar0 = 0
    MH = 0.0
    ML = 0.0
    MO = 0.0
    MC = 0.0
    MC1 = 0.0
    VQ = 0.0
    SumVQ0 = 0.0
    SumVQ1 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        _s_OnCalculate_SumVQ1_ = close[min_rates_total_]
    else:
        first = prev_calculated - 1
    bar0 = rates_total - 1
    SumVQ1 = _s_OnCalculate_SumVQ1_
    bar = first
    for bar in range(bar, rates_total):
        if rates_total != prev_calculated and bar == bar0:
            _s_OnCalculate_SumVQ1_ = SumVQ1
        MO = XMAO.XMASeries(0, prev_calculated, rates_total, VQMA_Method, VQPhase, VQLength, open[bar], bar, False)
        MC = XMAC.XMASeries(0, prev_calculated, rates_total, VQMA_Method, VQPhase, VQLength, close[bar], bar, False)
        MH = XMAH.XMASeries(0, prev_calculated, rates_total, VQMA_Method, VQPhase, VQLength, high[bar], bar, False)
        ML = XMAL.XMASeries(0, prev_calculated, rates_total, VQMA_Method, VQPhase, VQLength, low[bar], bar, False)
        MC1 = MC - MOM.MomentumSeries(xmin_rates_total, prev_calculated, rates_total, VQMomentum, MC, bar, False)
        if bar < min_rates_total:
            continue
        if (MH - ML) > 0:
            VQ = MathAbs((_fdiv(MC - MC1, MathMax(MH - ML, MathMax(MH - MC1, MC1 - ML))) + _fdiv(MC - MO, MH - ML)) * 0.5) * ((MC - MC1 + (MC - MO)) * 0.5)
        SumVQ0 = SumVQ1 + VQ
        if bar <= min_rates_total:
            SumVQ1 = SumVQ0
            continue
        if Filter and MathAbs(SumVQ0 - SumVQ1) < (Filter * Point()):
            SumVQ0 = SumVQ1
        trend0 = _s_OnCalculate_trend1
        if SumVQ0 > SumVQ1:
            trend0 = 1
        if SumVQ0 < SumVQ1:
            trend0 = -1
        IndBuffer[bar] = MC
        ColorIndBuffer[bar] = 0.0
        if trend0 > 0:
            ColorIndBuffer[bar] = 2.0
        elif trend0 < 0:
            ColorIndBuffer[bar] = 1.0
        if bar != bar0:
            _s_OnCalculate_trend1 = trend0
        SumVQ1 = SumVQ0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMAO = _alloc(CXMA)
XMAO.__init__()
XMAL = _alloc(CXMA)
XMAL.__init__()
XMAH = _alloc(CXMA)
XMAH.__init__()
XMAC = _alloc(CXMA)
XMAC.__init__()
MOM = _alloc(CMomentum)
MOM.__init__()

# ---- static local variables
_s_OnCalculate_SumVQ1_ = 0.0
_s_OnCalculate_trend1 = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Vqbars(_MQL5Indicator):
    name = 'vqbars'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'VQMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Smoothing method
        'VQLength': 12,  # Smoothing depth
        'VQPhase': 15,  # Smoothing parameter
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simple Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Applied price
        'VQMomentum': 1,  # Momentum
        'Filter': 5,  # Maximum deviation
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

