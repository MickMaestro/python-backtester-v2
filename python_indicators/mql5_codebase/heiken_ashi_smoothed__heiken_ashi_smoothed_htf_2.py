"""Heiken_Ashi_Smoothed_ — converted from MQL5: MQL5 Indicators/Heiken_Ashi_Smoothed_HTF/Heiken_Ashi_Smoothed_.mq5

Heiken Ashi Smoothed
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16748574, 255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Heiken Ashi Open;Heiken Ashi High;Heiken Ashi Low;Heiken Ashi Close'}, 'levels': [], 'description': ['Heiken Ashi Smoothed'], 'name': 'Heiken_Ashi_Smoothed_', 'source': 'MQL5 Indicators/Heiken_Ashi_Smoothed_HTF/Heiken_Ashi_Smoothed_.mq5', 'folder': 'Heiken_Ashi_Smoothed_HTF', 'inputs': [{'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 4, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 30, 'label': 'глубина  усреднения', 'sinput': False}, {'mql': 'Phase', 'py': 'Phase', 'param': 'Phase', 'type': 'int', 'default': 100, 'label': 'параметр усреднения,', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
MA_Method = _input('MA_Method', MODE_JJMA)  # метод усреднения
Length = _input('Length', 30)  # глубина  усреднения
Phase = _input('Phase', 100)  # параметр усреднения,
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
StartBars = 0

def OnInit():
    global StartBars
    StartBars = XMAO.GetStartBars(MA_Method, Length, Phase) + 1
    XMAO.XMALengthCheck('Length', Length)
    XMAO.XMAPhaseCheck('Phase', Phase, MA_Method)
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, StartBars)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Heiken Ashi Smoothed'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBars:
        return 0
    first = 0
    bar = 0
    XmaOpen = 0.0
    XmaHigh = 0.0
    XmaLow = 0.0
    XmaClose = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        XmaOpen = XMAO.XMASeries(0, prev_calculated, rates_total, MA_Method, Phase, Length, open[bar], bar, False)
        XmaClose = XMAC.XMASeries(0, prev_calculated, rates_total, MA_Method, Phase, Length, close[bar], bar, False)
        XmaHigh = XMAH.XMASeries(0, prev_calculated, rates_total, MA_Method, Phase, Length, high[bar], bar, False)
        XmaLow = XMAL.XMASeries(0, prev_calculated, rates_total, MA_Method, Phase, Length, low[bar], bar, False)
        if bar <= StartBars:
            ExtOpenBuffer[bar] = XmaOpen
            ExtCloseBuffer[bar] = XmaClose
            ExtHighBuffer[bar] = XmaHigh
            ExtLowBuffer[bar] = XmaLow
            continue
        ExtOpenBuffer[bar] = (ExtOpenBuffer[bar - 1] + ExtCloseBuffer[bar - 1]) / 2
        ExtCloseBuffer[bar] = (XmaOpen + XmaHigh + XmaLow + XmaClose) / 4
        ExtHighBuffer[bar] = MathMax(XmaHigh, MathMax(ExtOpenBuffer[bar], ExtCloseBuffer[bar]))
        ExtLowBuffer[bar] = MathMin(XmaLow, MathMin(ExtOpenBuffer[bar], ExtCloseBuffer[bar]))
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


class HeikenAshiSmoothed(_MQL5Indicator):
    name = 'Heiken_Ashi_Smoothed_'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения
        'Length': 30,  # глубина  усреднения
        'Phase': 100,  # параметр усреднения,
    }

