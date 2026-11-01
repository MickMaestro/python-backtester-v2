"""colorstepxccx — converted from MQL5: MQL5 Indicators/ColorStepXCCX_HTF/colorstepxccx.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [8421376, 16711935]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'Step XCCX'}, 'levels': [-50.0, 50.0], 'description': [], 'name': 'colorstepxccx', 'source': 'MQL5 Indicators/ColorStepXCCX_HTF/colorstepxccx.mq5', 'folder': 'ColorStepXCCX_HTF', 'inputs': [{'mql': 'DSmoothMethod', 'py': 'DSmoothMethod', 'param': 'DSmoothMethod', 'type': 'int', 'default': 4, 'label': 'Метод усреднения цены', 'sinput': False}, {'mql': 'DPeriod', 'py': 'DPeriod', 'param': 'DPeriod', 'type': 'uint', 'default': 30, 'label': 'Период средней', 'sinput': False}, {'mql': 'DPhase', 'py': 'DPhase', 'param': 'DPhase', 'type': 'int', 'default': 100, 'label': 'Параметр усреднения', 'sinput': False}, {'mql': 'MSmoothMethod', 'py': 'MSmoothMethod', 'param': 'MSmoothMethod', 'type': 'int', 'default': 7, 'label': 'Метод усреднения отклонения', 'sinput': False}, {'mql': 'MPeriod', 'py': 'MPeriod', 'param': 'MPeriod', 'type': 'uint', 'default': 7, 'label': 'Период среднего отклонения', 'sinput': False}, {'mql': 'MPhase', 'py': 'MPhase', 'param': 'MPhase', 'type': 'int', 'default': 15, 'label': 'Параметр усреднения отклонения', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 6, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'StepSizeFast', 'py': 'StepSizeFast', 'param': 'StepSizeFast', 'type': 'uint', 'default': 5, 'label': 'Быстрый шаг', 'sinput': False}, {'mql': 'StepSizeSlow', 'py': 'StepSizeSlow', 'param': 'StepSizeSlow', 'type': 'uint', 'default': 30, 'label': 'Медленный шаг', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
DSmoothMethod = _input('DSmoothMethod', MODE_JJMA)  # Метод усреднения цены
DPeriod = _input('DPeriod', 30)  # Период средней
DPhase = _input('DPhase', 100)  # Параметр усреднения
MSmoothMethod = _input('MSmoothMethod', MODE_T3)  # Метод усреднения отклонения
MPeriod = _input('MPeriod', 7)  # Период среднего отклонения
MPhase = _input('MPhase', 15)  # Параметр усреднения отклонения
IPC = _input('IPC', PRICE_TYPICAL)  # Ценовая константа
StepSizeFast = _input('StepSizeFast', 5)  # Быстрый шаг
StepSizeSlow = _input('StepSizeSlow', 30)  # Медленный шаг
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
Line2Buffer = Arr(0, 0.0)
Line3Buffer = Arr(0, 0.0)
RSI_Handle = 0
min_rates_total = 0
min_rates_total_D = 0
min_rates_total_M = 0

def OnInit():
    global min_rates_total, min_rates_total_D, min_rates_total_M
    min_rates_total_D = XMAD.GetStartBars(DSmoothMethod, DPeriod, DPhase)
    min_rates_total_M = XMAD.GetStartBars(MSmoothMethod, MPeriod, MPhase)
    min_rates_total = min_rates_total_D + min_rates_total_M
    XMAD.XMALengthCheck('DPeriod', DPeriod)
    XMAD.XMALengthCheck('MPeriod', MPeriod)
    XMAD.XMAPhaseCheck('DPhase', DPhase, DSmoothMethod)
    SetIndexBuffer(0, Line2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    SetIndexBuffer(1, Line3Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = Box("")
    SmoothD = ""
    SmoothM = ""
    SmoothD = XMAD.GetString_MA_Method(DSmoothMethod)
    SmoothM = XMAD.GetString_MA_Method(MSmoothMethod)
    StringConcatenate(shortname, 'StepXCCX(', _str(DPeriod), ',', _str(MPeriod), ',', SmoothD, ',', SmoothM, StepSizeFast, ', ', StepSizeSlow, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_fmax1, _s_OnCalculate_fmin1, _s_OnCalculate_ftrend_, _s_OnCalculate_smax1, _s_OnCalculate_smin1, _s_OnCalculate_strend_
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    ftrend = 0
    strend = 0
    recbar = 0
    fmin0 = 0.0
    fmax0 = 0.0
    smin0 = 0.0
    smax0 = 0.0
    price_ = 0.0
    xma = 0.0
    upccx = 0.0
    dnccx = 0.0
    xupccx = 0.0
    xdnccx = 0.0
    xccx = 0.0
    ftrend = _s_OnCalculate_ftrend_
    strend = _s_OnCalculate_strend_
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        _s_OnCalculate_fmin1 = 999999.0
        _s_OnCalculate_fmax1 = -999999.0
        _s_OnCalculate_smin1 = 999999.0
        _s_OnCalculate_smax1 = -999999.0
        _s_OnCalculate_ftrend_ = 0
        _s_OnCalculate_strend_ = 0
    else:
        first = prev_calculated - 1
    recbar = rates_total - 1
    bar = first
    for bar in range(bar, rates_total):
        if rates_total != prev_calculated and bar == recbar:
            _s_OnCalculate_ftrend_ = ftrend
            _s_OnCalculate_strend_ = strend
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        xma = XMAD.XMASeries(0, prev_calculated, rates_total, DSmoothMethod, DPhase, DPeriod, price_, bar, False)
        if bar < min_rates_total_D:
            continue
        upccx = price_ - xma
        dnccx = MathAbs(upccx)
        xupccx = XMAH.XMASeries(min_rates_total_D, prev_calculated, rates_total, MSmoothMethod, MPhase, MPeriod, upccx, bar, False)
        xdnccx = XMAL.XMASeries(min_rates_total_D, prev_calculated, rates_total, MSmoothMethod, MPhase, MPeriod, dnccx, bar, False)
        if xupccx != 0.0:
            xccx = _fdiv(100 * xupccx, xdnccx)
        else:
            xccx = 0.0
        fmax0 = xccx + (2 * StepSizeFast)
        fmin0 = xccx - (2 * StepSizeFast)
        if xccx > _s_OnCalculate_fmax1:
            ftrend = 1
        if xccx < _s_OnCalculate_fmin1:
            ftrend = -1
        if ftrend > 0 and fmin0 < _s_OnCalculate_fmin1:
            fmin0 = _s_OnCalculate_fmin1
        if ftrend < 0 and fmax0 > _s_OnCalculate_fmax1:
            fmax0 = _s_OnCalculate_fmax1
        smax0 = xccx + (2 * StepSizeSlow)
        smin0 = xccx - (2 * StepSizeSlow)
        if xccx > _s_OnCalculate_smax1:
            strend = 1
        if xccx < _s_OnCalculate_smin1:
            strend = -1
        if strend > 0 and smin0 < _s_OnCalculate_smin1:
            smin0 = _s_OnCalculate_smin1
        if strend < 0 and smax0 > _s_OnCalculate_smax1:
            smax0 = _s_OnCalculate_smax1
        if ftrend > 0:
            Line2Buffer[bar] = fmin0 + StepSizeFast
        if ftrend < 0:
            Line2Buffer[bar] = fmax0 - StepSizeFast
        if strend > 0:
            Line3Buffer[bar] = smin0 + StepSizeSlow
        if strend < 0:
            Line3Buffer[bar] = smax0 - StepSizeSlow
        if bar < recbar:
            _s_OnCalculate_fmin1 = fmin0
            _s_OnCalculate_fmax1 = fmax0
            _s_OnCalculate_smin1 = smin0
            _s_OnCalculate_smax1 = smax0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMAD = _alloc(CXMA)
XMAD.__init__()
XMAH = _alloc(CXMA)
XMAH.__init__()
XMAL = _alloc(CXMA)
XMAL.__init__()

# ---- static local variables
_s_OnCalculate_fmax1 = 0.0
_s_OnCalculate_fmin1 = 0.0
_s_OnCalculate_smin1 = 0.0
_s_OnCalculate_smax1 = 0.0
_s_OnCalculate_ftrend_ = 0
_s_OnCalculate_strend_ = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Colorstepxccx(_MQL5Indicator):
    name = 'colorstepxccx'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'DSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод усреднения цены
        'DPeriod': 30,  # Период средней
        'DPhase': 100,  # Параметр усреднения
        'MSmoothMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # Метод усреднения отклонения
        'MPeriod': 7,  # Период среднего отклонения
        'MPhase': 15,  # Параметр усреднения отклонения
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=6),  # Ценовая константа
        'StepSizeFast': 5,  # Быстрый шаг
        'StepSizeSlow': 30,  # Медленный шаг
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

