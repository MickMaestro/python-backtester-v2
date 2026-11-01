"""XXDPO_Candle — converted from MQL5: MQL5 Indicators/XXDPO_Candle/XXDPO_Candle.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [2763429, 8421504, 16748574]}, 'widths': {}, 'styles': {}, 'labels': {1: 'XXDPO Open;XXDPO High;XXDPO Low;XXDPO Close'}, 'levels': [0.0], 'description': [], 'name': 'XXDPO_Candle', 'source': 'MQL5 Indicators/XXDPO_Candle/XXDPO_Candle.mq5', 'folder': 'XXDPO_Candle', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 7, 'label': 'метод усреднения DPO', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'int', 'default': 21, 'label': 'глубина  усреднения DPO', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'параметр усреднения DPO,', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 4, 'label': 'метод сглаживания индикатора', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'int', 'default': 5, 'label': 'глубина сглаживания индикатора', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 100, 'label': 'параметр сглаживания индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг Фатла по горизонтали в барах', 'sinput': False}, {'mql': 'Gap', 'py': 'Gap', 'param': 'Gap', 'type': 'uint', 'default': 10, 'label': 'размер неучитываемого гэпа в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
MA_Method1 = _input('MA_Method1', MODE_T3)  # метод усреднения DPO
Length1 = _input('Length1', 21)  # глубина  усреднения DPO
Phase1 = _input('Phase1', 15)  # параметр усреднения DPO,
MA_Method2 = _input('MA_Method2', MODE_JJMA)  # метод сглаживания индикатора
Length2 = _input('Length2', 5)  # глубина сглаживания индикатора
Phase2 = _input('Phase2', 100)  # параметр сглаживания индикатора
Shift = _input('Shift', 0)  # сдвиг Фатла по горизонтали в барах
Gap = _input('Gap', 10)  # размер неучитываемого гэпа в пунктах
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
StartBars = 0
StartBars1 = 0
StartBars2 = 0

def OnInit():
    global StartBars, StartBars1, StartBars2
    StartBars1 = GetStartBars(MA_Method1, Length1, Phase1)
    StartBars2 = GetStartBars(MA_Method2, Length2, Phase2)
    StartBars = StartBars1 + StartBars2
    XMA1[0].XMALengthCheck('Length1', Length1)
    XMA2[0].XMALengthCheck('Length2', Length2)
    XMA1[0].XMAPhaseCheck('Phase1', Phase1, MA_Method1)
    XMA2[0].XMAPhaseCheck('Phase2', Phase2, MA_Method2)
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    shortname = Box("")
    Smooth1 = XMA1[0].GetString_MA_Method(MA_Method1)
    Smooth2 = XMA1[0].GetString_MA_Method(MA_Method2)
    StringConcatenate(shortname, 'XXDPO_Candle(', Length1, ', ', Length2, ', ', Smooth1, ', ', Smooth2, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBars:
        return 0
    XO = 0.0
    XH = 0.0
    XL = 0.0
    XC = 0.0
    XXO = 0.0
    XXH = 0.0
    XXL = 0.0
    XXC = 0.0
    Max = 0.0
    Min = 0.0
    xodpo = 0.0
    xhdpo = 0.0
    xldpo = 0.0
    xcdpo = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        XO = XMA1[0].XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, open[bar], bar, False)
        xodpo = open[bar] - XO
        XXO = XMA2[0].XMASeries(StartBars1, prev_calculated, rates_total, MA_Method2, Phase2, Length2, xodpo, bar, False)
        XH = XMA1[1].XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, high[bar], bar, False)
        xhdpo = high[bar] - XH
        XXH = XMA2[1].XMASeries(StartBars1, prev_calculated, rates_total, MA_Method2, Phase2, Length2, xhdpo, bar, False)
        XL = XMA1[2].XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, low[bar], bar, False)
        xldpo = low[bar] - XL
        XXL = XMA2[2].XMASeries(StartBars1, prev_calculated, rates_total, MA_Method2, Phase2, Length2, xldpo, bar, False)
        XC = XMA1[3].XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, close[bar], bar, False)
        xcdpo = close[bar] - XC
        XXC = XMA2[3].XMASeries(StartBars1, prev_calculated, rates_total, MA_Method2, Phase2, Length2, xcdpo, bar, False)
        Max = MathMax(XXO, XXC)
        Max = MathMax(Max, XXL)
        Max = MathMax(Max, XXH)
        Min = MathMin(XXO, XXC)
        Min = MathMin(Min, XXL)
        Min = MathMin(Min, XXH)
        ExtOpenBuffer[bar] = XXO
        ExtHighBuffer[bar] = Max
        ExtLowBuffer[bar] = Min
        ExtCloseBuffer[bar] = XXC
        if MathAbs(open[bar] - close[bar]) <= Gap:
            ExtOpenBuffer[bar] = ExtCloseBuffer[MathMax(bar - 1, 0)]
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 2.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = Arr(4, 0, dyn=False, factory=CXMA)
XMA2 = Arr(4, 0, dyn=False, factory=CXMA)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XXDPOCandle(_MQL5Indicator):
    name = 'XXDPO_Candle'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # метод усреднения DPO
        'Length1': 21,  # глубина  усреднения DPO
        'Phase1': 15,  # параметр усреднения DPO,
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод сглаживания индикатора
        'Length2': 5,  # глубина сглаживания индикатора
        'Phase2': 100,  # параметр сглаживания индикатора
        'Shift': 0,  # сдвиг Фатла по горизонтали в барах
        'Gap': 10,  # размер неучитываемого гэпа в пунктах
    }

