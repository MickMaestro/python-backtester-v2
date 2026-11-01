"""CenterOfGravityCandle — converted from MQL5: MQL5 Indicators/CenterOfGravityCandle/CenterOfGravityCandle.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [9639167, 13458026, 16776960]}, 'widths': {}, 'styles': {}, 'labels': {1: 'CenterOfGravityCandle Open; High; Low; Close'}, 'levels': [], 'description': [], 'name': 'CenterOfGravityCandle', 'source': 'MQL5 Indicators/CenterOfGravityCandle/CenterOfGravityCandle.mq5', 'folder': 'CenterOfGravityCandle', 'inputs': [{'mql': 'Period_', 'py': 'Period_', 'param': 'Period_', 'type': 'uint', 'default': 10, 'label': 'период усреднения индикатора', 'sinput': False}, {'mql': 'SmoothPeriod', 'py': 'SmoothPeriod', 'param': 'SmoothPeriod', 'type': 'uint', 'default': 3, 'label': 'период сглаживания сигнальной линии', 'sinput': False}, {'mql': 'MA_Method_', 'py': 'MA_Method_', 'param': 'MA_Method_', 'type': 'int', 'default': 0, 'label': 'метод усреднения сигнальной линии', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
Period_ = _input('Period_', 10)  # период усреднения индикатора
SmoothPeriod = _input('SmoothPeriod', 3)  # период сглаживания сигнальной линии
MA_Method_ = _input('MA_Method_', MODE_SMA)  # метод усреднения сигнальной линии
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = _int(Period_ + 1 + SmoothPeriod + 2)
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    shortname = Box("")
    StringConcatenate(shortname, 'CenterOfGravityCandle(', Period_, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_startbar
    if rates_total < min_rates_total:
        return 0
    sma = 0.0
    lwma = 0.0
    resalt = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
        _s_OnCalculate_startbar = _int(Period_ + 1)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        sma = _s_OnCalculate_OpMA.MASeries(0, prev_calculated, rates_total, Period_, MODE_SMA, open[bar], bar, False)
        lwma = _s_OnCalculate_OpLWMA.MASeries(0, prev_calculated, rates_total, Period_, MODE_LWMA, open[bar], bar, False)
        resalt = _fdiv(sma * lwma, Point())
        ExtOpenBuffer[bar] = _s_OnCalculate_OpSIGN.MASeries(_s_OnCalculate_startbar, prev_calculated, rates_total, SmoothPeriod, MA_Method_, resalt, bar, False)
        sma = _s_OnCalculate_HMA.MASeries(0, prev_calculated, rates_total, Period_, MODE_SMA, high[bar], bar, False)
        lwma = _s_OnCalculate_HLWMA.MASeries(0, prev_calculated, rates_total, Period_, MODE_LWMA, high[bar], bar, False)
        resalt = _fdiv(sma * lwma, Point())
        ExtHighBuffer[bar] = _s_OnCalculate_HSIGN.MASeries(_s_OnCalculate_startbar, prev_calculated, rates_total, SmoothPeriod, MA_Method_, resalt, bar, False)
        sma = _s_OnCalculate_LMA.MASeries(0, prev_calculated, rates_total, Period_, MODE_SMA, low[bar], bar, False)
        lwma = _s_OnCalculate_LLWMA.MASeries(0, prev_calculated, rates_total, Period_, MODE_LWMA, low[bar], bar, False)
        resalt = _fdiv(sma * lwma, Point())
        ExtLowBuffer[bar] = _s_OnCalculate_LSIGN.MASeries(_s_OnCalculate_startbar, prev_calculated, rates_total, SmoothPeriod, MA_Method_, resalt, bar, False)
        sma = _s_OnCalculate_ClMA.MASeries(0, prev_calculated, rates_total, Period_, MODE_SMA, close[bar], bar, False)
        lwma = _s_OnCalculate_ClLWMA.MASeries(0, prev_calculated, rates_total, Period_, MODE_LWMA, close[bar], bar, False)
        resalt = _fdiv(sma * lwma, Point())
        ExtCloseBuffer[bar] = _s_OnCalculate_ClSIGN.MASeries(_s_OnCalculate_startbar, prev_calculated, rates_total, SmoothPeriod, MA_Method_, resalt, bar, False)
    else:
        bar = _range_end(bar, rates_total, 1)
    bar = first
    for bar in range(bar, rates_total):
        Max = MathMax(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        Min = MathMin(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        ExtHighBuffer[bar] = MathMax(Max, ExtHighBuffer[bar])
        ExtLowBuffer[bar] = MathMin(Min, ExtLowBuffer[bar])
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 2.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- static local variables
_s_OnCalculate_startbar = 0
_s_OnCalculate_OpMA = CMoving_Average()
_s_OnCalculate_OpLWMA = CMoving_Average()
_s_OnCalculate_OpSIGN = CMoving_Average()
_s_OnCalculate_HMA = CMoving_Average()
_s_OnCalculate_HLWMA = CMoving_Average()
_s_OnCalculate_HSIGN = CMoving_Average()
_s_OnCalculate_LMA = CMoving_Average()
_s_OnCalculate_LLWMA = CMoving_Average()
_s_OnCalculate_LSIGN = CMoving_Average()
_s_OnCalculate_ClMA = CMoving_Average()
_s_OnCalculate_ClLWMA = CMoving_Average()
_s_OnCalculate_ClSIGN = CMoving_Average()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CenterOfGravityCandle(_MQL5Indicator):
    name = 'CenterOfGravityCandle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Period_': 10,  # период усреднения индикатора
        'SmoothPeriod': 3,  # период сглаживания сигнальной линии
        'MA_Method_': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=0),  # метод усреднения сигнальной линии
    }

