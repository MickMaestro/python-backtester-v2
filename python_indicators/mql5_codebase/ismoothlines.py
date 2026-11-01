"""ismoothlines — converted from MQL5: MQL5 Indicators/Smooth Lines/ismoothlines.mq5

Smooth lines for iCustomChart
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Imports DLL/library functions: LibCustomChart.ex5 (not available).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.libcustomchart import *  # #include libcustomchart.mqh
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [13458026, 16711935]}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Smooth lines for iCustomChart'], 'name': 'ismoothlines', 'source': 'MQL5 Indicators/Smooth Lines/ismoothlines.mq5', 'folder': 'Smooth Lines', 'inputs': [{'mql': 'MA_SMethod', 'py': 'MA_SMethod', 'param': 'MA_SMethod', 'type': 'int', 'default': 3, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'MA_Length', 'py': 'MA_Length', 'param': 'MA_Length', 'type': 'int', 'default': 30, 'label': 'Smoothing depth', 'sinput': False}, {'mql': 'MA_Phase', 'py': 'MA_Phase', 'param': 'MA_Phase', 'type': 'int', 'default': 100, 'label': 'Smoothing parameter', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': ['LibCustomChart.ex5'], 'libraries': ['libcustomchart.mqh', 'SmoothAlgorithms.mqh']}

# ---- inputs and global variables
ExtIndicatorBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
MA_SMethod = _input('MA_SMethod', MODE_LWMA)  # Smoothing method
MA_Length = _input('MA_Length', 30)  # Smoothing depth
MA_Phase = _input('MA_Phase', 100)  # Smoothing parameter
StartBars = 0

def OnInit():
    global StartBars
    StartBars = ind.GetStartBars(MA_SMethod, MA_Length, MA_Phase) + 1
    ind.XMALengthCheck('Length', MA_Length)
    ind.XMAPhaseCheck('Phase', MA_Phase, MA_SMethod)
    SetIndexBuffer(0, ExtIndicatorBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = EnumToString(MA_SMethod, 'Smooth_Method') + '(' + _str(MA_Length) + ',' + _str(MA_Phase) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return not CustomChartInit()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if not CustomChartRefresh():
        return 0
    if CustomChartBars() < StartBars:
        return 0
    if not CustomChartSync(ExtIndicatorBuffer):
        return prev_calculated
    if not CustomChartSync(ExtColorBuffer):
        return prev_calculated
    first = 0
    bar = 0
    custom_begin = 0
    custom_prev_calculated = 0
    custom_price = Arr(1, 0.0, dyn=False)
    custom_begin = CustomChartBegin()
    custom_prev_calculated = rates_total - CustomChartNewBar()
    if prev_calculated > rates_total or prev_calculated <= custom_begin:
        first = custom_begin
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, custom_begin + StartBars)
    else:
        first = custom_prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        if CopyClose_u_2(rates_total - 1 - bar, 1, custom_price) != 1:
            custom_price[0] = EMPTY_VALUE
        ExtIndicatorBuffer[bar] = ind.XMASeries(custom_begin, custom_prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, custom_price[0], bar, False)
        if bar <= (custom_begin + StartBars):
            continue
        if ExtIndicatorBuffer[bar - 1] < ExtIndicatorBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
ind = _alloc(CXMA)
ind.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Ismoothlines(_MQL5Indicator):
    name = 'ismoothlines'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_SMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # Smoothing method
        'MA_Length': 30,  # Smoothing depth
        'MA_Phase': 100,  # Smoothing parameter
    }

