"""heiken_ashi_smoothed — converted from MQL5: MQL5 Indicators/Heiken Ashi Smoothed/heiken_ashi_smoothed.mq5

Heiken Ashi Smoothed
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16748574, 255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Heiken Ashi Open;Heiken Ashi High;Heiken Ashi Low;Heiken Ashi Close'}, 'levels': [], 'description': ['Heiken Ashi Smoothed'], 'name': 'heiken_ashi_smoothed', 'source': 'MQL5 Indicators/Heiken Ashi Smoothed/heiken_ashi_smoothed.mq5', 'folder': 'Heiken Ashi Smoothed', 'inputs': [{'mql': 'MA_SMethod', 'py': 'MA_SMethod', 'param': 'MA_SMethod', 'type': 'int', 'default': 4, 'label': 'Smoothing method', 'sinput': False}, {'mql': 'SmLength', 'py': 'SmLength', 'param': 'SmLength', 'type': 'int', 'default': 30, 'label': 'Smoothing depth', 'sinput': False}, {'mql': 'SmPhase', 'py': 'SmPhase', 'param': 'SmPhase', 'type': 'int', 'default': 100, 'label': 'Smoothing parameter,', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
MA_SMethod = _input('MA_SMethod', MODE_JJMA)  # Smoothing method
SmLength = _input('SmLength', 30)  # Smoothing depth
SmPhase = _input('SmPhase', 100)  # Smoothing parameter,
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
StartBars = 0

def OnInit():
    global StartBars
    StartBars = XMAO.GetStartBars(MA_SMethod, SmLength, SmPhase) + 1
    XMAO.XMALengthCheck('Length', SmLength)
    XMAO.XMAPhaseCheck('Phase', SmPhase, MA_SMethod)
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
        XmaOpen = XMAO.XMASeries(0, prev_calculated, rates_total, MA_SMethod, SmPhase, SmLength, open[bar], bar, False)
        XmaClose = XMAC.XMASeries(0, prev_calculated, rates_total, MA_SMethod, SmPhase, SmLength, close[bar], bar, False)
        XmaHigh = XMAH.XMASeries(0, prev_calculated, rates_total, MA_SMethod, SmPhase, SmLength, high[bar], bar, False)
        XmaLow = XMAL.XMASeries(0, prev_calculated, rates_total, MA_SMethod, SmPhase, SmLength, low[bar], bar, False)
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
    name = 'heiken_ashi_smoothed'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_SMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Smoothing method
        'SmLength': 30,  # Smoothing depth
        'SmPhase': 100,  # Smoothing parameter,
    }

