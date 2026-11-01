"""kc_cloud — converted from MQL5: MQL5 Indicators/KC_Cloud/kc_cloud.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 7}, 'colors': {1: [10025880]}, 'widths': {}, 'styles': {}, 'labels': {1: 'KC_Cloud'}, 'levels': [], 'description': [], 'name': 'kc_cloud', 'source': 'MQL5 Indicators/KC_Cloud/kc_cloud.mq5', 'folder': 'KC_Cloud', 'inputs': [{'mql': 'Mode', 'py': 'Mode', 'param': 'Mode', 'type': 'int', 'default': 1, 'label': 'Метод расчета цен', 'sinput': False}, {'mql': 'XMA_Method', 'py': 'XMA_Method', 'param': 'XMA_Method', 'type': 'int', 'default': 0, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'XLength', 'py': 'XLength', 'param': 'XLength', 'type': 'int', 'default': 12, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'XPhase', 'py': 'XPhase', 'param': 'XPhase', 'type': 'int', 'default': 15, 'label': 'Параметр сглаживания', 'sinput': False}, {'mql': 'ATRPeriod', 'py': 'ATRPeriod', 'param': 'ATRPeriod', 'type': 'uint', 'default': 13, 'label': '', 'sinput': False}, {'mql': 'ATRFactor', 'py': 'ATRFactor', 'param': 'ATRFactor', 'type': 'double', 'default': 1.5, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum PriceMode
MODE_CLOSE = 0
MODE_HIGHLOW = 1
_enum('PriceMode', {0: 'MODE_CLOSE', 1: 'MODE_HIGHLOW'})

# ---- inputs and global variables
Mode = _input('Mode', MODE_HIGHLOW)  # Метод расчета цен
XMA_Method = _input('XMA_Method', MODE_SMA)  # Метод усреднения
XLength = _input('XLength', 12)  # Глубина сглаживания
XPhase = _input('XPhase', 15)  # Параметр сглаживания
ATRPeriod = _input('ATRPeriod', 13)
ATRFactor = _input('ATRFactor', 1.5)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
ATR_Handle = 0
min_rates_total = 0
ExtHBuffer = Arr(0, 0.0)
ExtLBuffer = Arr(0, 0.0)

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Handle = iATR(None, 0, ATRPeriod)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    min_rates_total = _int(MathMax(GetStartBars(XMA_Method, XLength, XPhase), ATRPeriod))
    SetIndexBuffer(0, ExtHBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    SetIndexBuffer(1, ExtLBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    shortname = 'KC_Cloud'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    ATR = Arr(1, 0.0, dyn=False)
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    if Mode == MODE_HIGHLOW:
        bar = first
        for bar in range(bar, rates_total):
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            res = ATRFactor * ATR[0]
            ExtHBuffer[bar] = _s_OnCalculate_HXMA.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, high[bar], bar, False) + res
            ExtLBuffer[bar] = _s_OnCalculate_LXMA.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, low[bar], bar, False) - res
        else:
            bar = _range_end(bar, rates_total, 1)
    else:
        bar = first
        for bar in range(bar, rates_total):
            if CopyBuffer(ATR_Handle, 0, _DT(time[bar]), 1, ATR) <= 0:
                return 0
            xma = _s_OnCalculate_XMA.XMASeries(0, prev_calculated, rates_total, XMA_Method, XPhase, XLength, close[bar], bar, False)
            res = ATRFactor * ATR[0]
            ExtHBuffer[bar] = xma + res
            ExtLBuffer[bar] = xma - res
        else:
            bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_HXMA = CXMA()
_s_OnCalculate_LXMA = CXMA()
_s_OnCalculate_XMA = CXMA()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KcCloud(_MQL5Indicator):
    name = 'kc_cloud'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Mode': _Choice({0: 'Close', 1: 'High/Low'}, default=1),  # Метод расчета цен
        'XMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Метод усреднения
        'XLength': 12,  # Глубина сглаживания
        'XPhase': 15,  # Параметр сглаживания
        'ATRPeriod': 13,
        'ATRFactor': 1.5,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

