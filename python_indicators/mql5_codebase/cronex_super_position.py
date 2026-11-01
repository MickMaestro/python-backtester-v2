"""cronex_super_position — converted from MQL5: MQL5 Indicators/Cronex Super Position/cronex_super_position.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 6}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 10}, 'colors': {1: [12632256], 2: [36095], 3: [0], 4: [255], 5: [16711680], 6: [8421504, 8421376, 14822282, 6053069, 16711935]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 3}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}, 'labels': {1: 'RSI Super Position', 2: 'DeMarker Super Position', 3: 'Cronex Super Position', 4: 'Fast Signal Line', 5: 'Slow Signal Line', 6: 'Super Position Divergence'}, 'levels': [-0.2, 0.2, 0.5, 0.8], 'description': [], 'name': 'cronex_super_position', 'source': 'MQL5 Indicators/Cronex Super Position/cronex_super_position.mq5', 'folder': 'Cronex Super Position', 'inputs': [{'mql': 'RSI', 'py': 'RSI', 'param': 'RSI', 'type': 'int', 'default': 10, 'label': 'RSI period', 'sinput': False}, {'mql': 'DeMarker', 'py': 'DeMarker', 'param': 'DeMarker', 'type': 'int', 'default': 10, 'label': 'DeMarker period', 'sinput': False}, {'mql': 'SPStep', 'py': 'SPStep', 'param': 'SPStep', 'type': 'int', 'default': 4, 'label': 'Interval range', 'sinput': False}, {'mql': 'FastMA', 'py': 'FastMA', 'param': 'FastMA', 'type': 'int', 'default': 10, 'label': 'Fast smoothing period', 'sinput': False}, {'mql': 'SlowMA', 'py': 'SlowMA', 'param': 'SlowMA', 'type': 'int', 'default': 18, 'label': 'Slow smoothing period', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
RSI = _input('RSI', 10)  # RSI period
DeMarker = _input('DeMarker', 10)  # DeMarker period
SPStep = _input('SPStep', 4)  # Interval range
FastMA = _input('FastMA', 10)  # Fast smoothing period
SlowMA = _input('SlowMA', 18)  # Slow smoothing period
RSI_Handle = Arr(4, 0, dyn=False)
DEM_Handle = Arr(4, 0, dyn=False)
start = 0
sp_start = 0
RSIBuffer = Arr(0, 0.0)
DeMarkerBuffer = Arr(0, 0.0)
SPBuffer = Arr(0, 0.0)
FastMABuffer = Arr(0, 0.0)
SlowMABuffer = Arr(0, 0.0)
DiverBuffer = Arr(0, 0.0)
ColorDiverBuffer = Arr(0, 0.0)

def OnInit():
    global sp_start, start
    rsi_start = RSI + (SPStep * 3)
    demark_start = DeMarker + (SPStep * 3)
    sp_start = MathMax(rsi_start, demark_start)
    start = sp_start + MathMax(FastMA, SlowMA)
    for numb in range(0, 4):
        RSI_Handle[numb] = iRSI(None, 0, RSI + (SPStep * numb), PRICE_WEIGHTED)
        DEM_Handle[numb] = iDeMarker(None, 0, DeMarker + (SPStep * numb))
    SetIndexBuffer(0, RSIBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, rsi_start)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(RSIBuffer, True)
    SetIndexBuffer(1, DeMarkerBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, demark_start)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(DeMarkerBuffer, True)
    SetIndexBuffer(2, SPBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, sp_start)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(SPBuffer, True)
    SetIndexBuffer(3, FastMABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, sp_start)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(FastMABuffer, True)
    SetIndexBuffer(4, SlowMABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, sp_start)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(SlowMABuffer, True)
    SetIndexBuffer(5, DiverBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, start)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(DiverBuffer, True)
    SetIndexBuffer(6, ColorDiverBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, start + 1)
    ArraySetAsSeries(ColorDiverBuffer, True)
    MA1.MALengthCheck_1('RSI', RSI)
    MA1.MALengthCheck_1('DeMarker', DeMarker)
    MA1.MALengthCheck_1('FastMA', FastMA)
    MA1.MALengthCheck_1('SlowMA', SlowMA)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RSI DeMarker Super Position')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < start:
        return 0
    for numb in range(0, 4):
        if BarsCalculated(RSI_Handle[numb]) < rates_total:
            return 0
    for numb in range(0, 4):
        if BarsCalculated(DEM_Handle[numb]) < rates_total:
            return 0
    limit = 0
    bar = 0
    to_copy = 0
    StartBar = 0
    RSI0 = Arr(0, 0.0)
    RSI1 = Arr(0, 0.0)
    RSI2 = Arr(0, 0.0)
    RSI3 = Arr(0, 0.0)
    DEM0 = Arr(0, 0.0)
    DEM1 = Arr(0, 0.0)
    DEM2 = Arr(0, 0.0)
    DEM3 = Arr(0, 0.0)
    TmpDiver = 0.0
    ArraySetAsSeries(RSI0, True)
    ArraySetAsSeries(RSI1, True)
    ArraySetAsSeries(RSI2, True)
    ArraySetAsSeries(RSI3, True)
    ArraySetAsSeries(DEM0, True)
    ArraySetAsSeries(DEM1, True)
    ArraySetAsSeries(DEM2, True)
    ArraySetAsSeries(DEM3, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - sp_start
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    StartBar = rates_total - sp_start - 1
    if CopyBuffer(RSI_Handle[0], 0, 0, to_copy, RSI0) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[1], 0, 0, to_copy, RSI1) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[2], 0, 0, to_copy, RSI2) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[3], 0, 0, to_copy, RSI3) <= 0:
        return 0
    if CopyBuffer(DEM_Handle[0], 0, 0, to_copy, DEM0) <= 0:
        return 0
    if CopyBuffer(DEM_Handle[1], 0, 0, to_copy, DEM1) <= 0:
        return 0
    if CopyBuffer(DEM_Handle[2], 0, 0, to_copy, DEM2) <= 0:
        return 0
    if CopyBuffer(DEM_Handle[3], 0, 0, to_copy, DEM3) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        RSIBuffer[bar] = (RSI0[bar] + RSI1[bar] + RSI2[bar] + RSI3[bar]) / 400.0
        DeMarkerBuffer[bar] = (DEM0[bar] + DEM1[bar] + DEM2[bar] + DEM3[bar]) / 4.0
        SPBuffer[bar] = (RSIBuffer[bar] + DeMarkerBuffer[bar]) / 2
        TmpDiver = DeMarkerBuffer[bar] - RSIBuffer[bar]
        FastMABuffer[bar] = MA1.MASeries(StartBar, prev_calculated, rates_total, FastMA, MODE_LWMA, SPBuffer[bar], bar, True)
        SlowMABuffer[bar] = MA2.MASeries(StartBar, prev_calculated, rates_total, SlowMA, MODE_LWMA, SPBuffer[bar], bar, True)
        DiverBuffer[bar] = MA3.MASeries(StartBar, prev_calculated, rates_total, FastMA, MODE_LWMA, TmpDiver, bar, True)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit -= 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ColorDiverBuffer[bar] = 0.0
        if DiverBuffer[bar] > 0:
            if DiverBuffer[bar] > DiverBuffer[bar + 1]:
                ColorDiverBuffer[bar] = 1.0
            if DiverBuffer[bar] < DiverBuffer[bar + 1]:
                ColorDiverBuffer[bar] = 2.0
        if DiverBuffer[bar] < 0:
            if DiverBuffer[bar] < DiverBuffer[bar + 1]:
                ColorDiverBuffer[bar] = 3.0
            if DiverBuffer[bar] > DiverBuffer[bar + 1]:
                ColorDiverBuffer[bar] = 4.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- global variables initialised from expressions
MA1 = _alloc(CMoving_Average)
MA1.__init__()
MA2 = _alloc(CMoving_Average)
MA2.__init__()
MA3 = _alloc(CMoving_Average)
MA3.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CronexSuperPosition(_MQL5Indicator):
    name = 'cronex_super_position'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSI': 10,  # RSI period
        'DeMarker': 10,  # DeMarker period
        'SPStep': 4,  # Interval range
        'FastMA': 10,  # Fast smoothing period
        'SlowMA': 18,  # Slow smoothing period
    }

