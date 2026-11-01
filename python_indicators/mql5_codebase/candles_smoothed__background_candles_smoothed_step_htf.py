"""candles_smoothed — converted from MQL5: MQL5 Indicators/Background_Candles_Smoothed_Step_HTF/candles_smoothed.mq5

Smoothed Candles
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [13458026, 16711935]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Smoothed Candles Open; Smoothed Candles High; Smoothed Candles Low; Smoothed Candles Close'}, 'levels': [], 'description': ['Smoothed Candles'], 'name': 'candles_smoothed', 'source': 'MQL5 Indicators/Background_Candles_Smoothed_Step_HTF/candles_smoothed.mq5', 'folder': 'Background_Candles_Smoothed_Step_HTF', 'inputs': [{'mql': 'MA_SMethod', 'py': 'MA_SMethod', 'param': 'MA_SMethod', 'type': 'int', 'default': 3, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'MA_Length', 'py': 'MA_Length', 'param': 'MA_Length', 'type': 'int', 'default': 30, 'label': 'Глубина усреднения', 'sinput': False}, {'mql': 'MA_Phase', 'py': 'MA_Phase', 'param': 'MA_Phase', 'type': 'int', 'default': 100, 'label': 'Параметр усреднения', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
MA_SMethod = _input('MA_SMethod', MODE_LWMA)  # Метод усреднения
MA_Length = _input('MA_Length', 30)  # Глубина усреднения
MA_Phase = _input('MA_Phase', 100)  # Параметр усреднения
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
StartBars = 0

def OnInit():
    global StartBars
    StartBars = XMAO.GetStartBars(MA_SMethod, MA_Length, MA_Phase) + 1
    XMAO.XMALengthCheck('Length', MA_Length)
    XMAO.XMAPhaseCheck('Phase', MA_Phase, MA_SMethod)
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, StartBars)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Smoothed Candles'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBars:
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        ExtOpenBuffer[bar] = XMAO.XMASeries(0, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, open[bar], bar, False)
        ExtCloseBuffer[bar] = XMAC.XMASeries(0, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, close[bar], bar, False)
        ExtHighBuffer[bar] = XMAH.XMASeries(0, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, high[bar], bar, False)
        ExtLowBuffer[bar] = XMAL.XMASeries(0, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, low[bar], bar, False)
        if bar <= StartBars:
            continue
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class CandlesSmoothed(_MQL5Indicator):
    name = 'candles_smoothed'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_SMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # Метод усреднения
        'MA_Length': 30,  # Глубина усреднения
        'MA_Phase': 100,  # Параметр усреднения
    }

