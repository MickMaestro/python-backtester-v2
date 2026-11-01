"""XFisher_org_v1_Candle — converted from MQL5: MQL5 Indicators/XFisher_org_v1_Candle/XFisher_org_v1_Candle.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16711935, 8421504, 16748574]}, 'widths': {}, 'styles': {}, 'labels': {1: 'XFisher_org_v1 Open;XFisher_org_v1 High;XFisher_org_v1 Low;XFisher_org_v1 Close'}, 'levels': [1.5, 0.0, -1.5], 'description': [], 'name': 'XFisher_org_v1_Candle', 'source': 'MQL5 Indicators/XFisher_org_v1_Candle/XFisher_org_v1_Candle.mq5', 'folder': 'XFisher_org_v1_Candle', 'inputs': [{'mql': 'FLength', 'py': 'FLength', 'param': 'FLength', 'type': 'uint', 'default': 14, 'label': 'глубина усреднения', 'sinput': False}, {'mql': 'MA_SMethod', 'py': 'MA_SMethod', 'param': 'MA_SMethod', 'type': 'int', 'default': 4, 'label': 'Метод сглаживания', 'sinput': False}, {'mql': 'MA_Length', 'py': 'MA_Length', 'param': 'MA_Length', 'type': 'uint', 'default': 5, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'MA_Phase', 'py': 'MA_Phase', 'param': 'MA_Phase', 'type': 'int', 'default': 15, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'Gap', 'py': 'Gap', 'param': 'Gap', 'type': 'uint', 'default': 10, 'label': 'размер неучитываемого гэпа в пунктах', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
FLength = _input('FLength', 14)  # глубина усреднения
MA_SMethod = _input('MA_SMethod', MODE_JJMA)  # Метод сглаживания
MA_Length = _input('MA_Length', 5)  # Глубина сглаживания
MA_Phase = _input('MA_Phase', 15)  # параметр сглаживания,
Gap = _input('Gap', 10)  # размер неучитываемого гэпа в пунктах
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0

def OnInit():
    global min_rates_1, min_rates_total
    min_rates_1 = _int(FLength) + 1
    min_rates_total = min_rates_1 + GetStartBars(MA_SMethod, MA_Length, MA_Phase)
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    shortname = Box("")
    StringConcatenate(shortname, 'XFisher_org_v1_Candle(', FLength, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 4)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_cfish_prev, _s_OnCalculate_cvalue_prev, _s_OnCalculate_hfish_prev, _s_OnCalculate_hvalue_prev, _s_OnCalculate_lfish_prev, _s_OnCalculate_lvalue_prev, _s_OnCalculate_ofish_prev, _s_OnCalculate_ovalue_prev
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    smax = 0.0
    smin = 0.0
    price = 0.0
    wpr = 0.0
    ovalue = 0.0
    hvalue = 0.0
    lvalue = 0.0
    cvalue = 0.0
    res1 = 0.0
    res2 = 0.0
    ofish = 0.0
    hfish = 0.0
    lfish = 0.0
    cfish = 0.0
    O = 0.0
    H = 0.0
    L = 0.0
    C = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_1
        _s_OnCalculate_cvalue_prev = 0.0
        _s_OnCalculate_lvalue_prev = _s_OnCalculate_cvalue_prev
        _s_OnCalculate_hvalue_prev = _s_OnCalculate_lvalue_prev
        _s_OnCalculate_ovalue_prev = _s_OnCalculate_hvalue_prev
        _s_OnCalculate_cfish_prev = 0.0
        _s_OnCalculate_lfish_prev = _s_OnCalculate_cfish_prev
        _s_OnCalculate_hfish_prev = _s_OnCalculate_lfish_prev
        _s_OnCalculate_ofish_prev = _s_OnCalculate_hfish_prev
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        smax = DBL_MIN
        smin = DBL_MAX
        for iii in range(0, _int(FLength)):
            barx = bar - iii
            smax = MathMax(smax, high[barx])
            smin = MathMin(smin, low[barx])
        if smax == smin:
            smax += Point()
        price = open[bar]
        wpr = _fdiv(price - smin, smax - smin)
        ovalue = wpr - 0.5 + (0.67 * _s_OnCalculate_ovalue_prev)
        ovalue = MathMin(ovalue, DBL_MAX)
        ovalue = MathMax(ovalue, -DBL_MAX)
        res1 = 1.0 - ovalue
        if not res1:
            res1 = 1.0
        res2 = _fdiv(1.0 + ovalue, 1.0 - ovalue)
        if res2 < 1e-07:
            res2 = 1.0
        ofish = (0.5 * MathLog(res2)) + (0.5 * _s_OnCalculate_ofish_prev)
        O = oXMA.XMASeries(min_rates_1, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, ofish, bar, False)
        price = high[bar]
        wpr = _fdiv(price - smin, smax - smin)
        hvalue = wpr - 0.5 + (0.67 * _s_OnCalculate_hvalue_prev)
        hvalue = MathMin(hvalue, DBL_MAX)
        hvalue = MathMax(hvalue, -DBL_MAX)
        res1 = 1.0 - hvalue
        if not res1:
            res1 = 1.0
        res2 = _fdiv(1.0 + hvalue, 1.0 - hvalue)
        if res2 < 1e-07:
            res2 = 1.0
        hfish = (0.5 * MathLog(res2)) + (0.5 * _s_OnCalculate_hfish_prev)
        H = hXMA.XMASeries(min_rates_1, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, hfish, bar, False)
        price = low[bar]
        wpr = _fdiv(price - smin, smax - smin)
        lvalue = wpr - 0.5 + (0.67 * _s_OnCalculate_lvalue_prev)
        lvalue = MathMin(lvalue, DBL_MAX)
        lvalue = MathMax(lvalue, -DBL_MAX)
        res1 = 1.0 - lvalue
        if not res1:
            res1 = 1.0
        res2 = _fdiv(1.0 + lvalue, 1.0 - lvalue)
        if res2 < 1e-07:
            res2 = 1.0
        lfish = (0.5 * MathLog(res2)) + (0.5 * _s_OnCalculate_lfish_prev)
        L = lXMA.XMASeries(min_rates_1, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, lfish, bar, False)
        price = close[bar]
        wpr = _fdiv(price - smin, smax - smin)
        cvalue = wpr - 0.5 + (0.67 * _s_OnCalculate_cvalue_prev)
        cvalue = MathMin(cvalue, DBL_MAX)
        cvalue = MathMax(cvalue, -DBL_MAX)
        res1 = 1.0 - cvalue
        if not res1:
            res1 = 1.0
        res2 = _fdiv(1.0 + cvalue, 1.0 - cvalue)
        if res2 < 1e-07:
            res2 = 1.0
        cfish = (0.5 * MathLog(res2)) + (0.5 * _s_OnCalculate_cfish_prev)
        C = cXMA.XMASeries(min_rates_1, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, cfish, bar, False)
        Max = MathMax(O, C)
        Max = MathMax(Max, L)
        Max = MathMax(Max, H)
        Min = MathMin(O, C)
        Min = MathMin(Min, L)
        Min = MathMin(Min, H)
        ExtOpenBuffer[bar] = O
        ExtHighBuffer[bar] = Max
        ExtLowBuffer[bar] = Min
        ExtCloseBuffer[bar] = C
        if MathAbs(open[bar] - close[bar]) <= Gap:
            ExtOpenBuffer[bar] = ExtCloseBuffer[MathMax(bar - 1, 0)]
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 2.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
        if bar < (rates_total - 1):
            _s_OnCalculate_ovalue_prev = ovalue
            _s_OnCalculate_ofish_prev = ofish
            _s_OnCalculate_hvalue_prev = hvalue
            _s_OnCalculate_hfish_prev = hfish
            _s_OnCalculate_lvalue_prev = lvalue
            _s_OnCalculate_lfish_prev = lfish
            _s_OnCalculate_cvalue_prev = cvalue
            _s_OnCalculate_cfish_prev = cfish
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
oXMA = _alloc(CXMA)
oXMA.__init__()
hXMA = _alloc(CXMA)
hXMA.__init__()
lXMA = _alloc(CXMA)
lXMA.__init__()
cXMA = _alloc(CXMA)
cXMA.__init__()

# ---- static local variables
_s_OnCalculate_ovalue_prev = 0.0
_s_OnCalculate_ofish_prev = 0.0
_s_OnCalculate_hvalue_prev = 0.0
_s_OnCalculate_hfish_prev = 0.0
_s_OnCalculate_lvalue_prev = 0.0
_s_OnCalculate_lfish_prev = 0.0
_s_OnCalculate_cvalue_prev = 0.0
_s_OnCalculate_cfish_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XFisherOrgV1Candle(_MQL5Indicator):
    name = 'XFisher_org_v1_Candle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FLength': 14,  # глубина усреднения
        'MA_SMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод сглаживания
        'MA_Length': 5,  # Глубина сглаживания
        'MA_Phase': 15,  # параметр сглаживания,
        'Gap': 10,  # размер неучитываемого гэпа в пунктах
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

