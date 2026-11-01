"""i-fractals-sig — converted from MQL5: MQL5 Indicators/i-Fractals-sig/i-fractals-sig.mq5

Signals indicator
Copyright: 3172552 & KimIV; Link: http://www.kimiv.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '3172552 & KimIV', 'link': 'http://www.kimiv.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16711680]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'i-Fractals Sell', 2: 'i-Fractals Buy'}, 'levels': [], 'description': ['Signals indicator'], 'name': 'i-fractals-sig', 'source': 'MQL5 Indicators/i-Fractals-sig/i-fractals-sig.mq5', 'folder': 'i-Fractals-sig', 'inputs': [{'mql': 'bd', 'py': 'bd', 'param': 'bd', 'type': 'int', 'default': 7, 'label': 'Last bar body length', 'sinput': False}, {'mql': 'bdd', 'py': 'bdd', 'param': 'bdd', 'type': 'int', 'default': 40, 'label': 'Body lenght for double top/buttom bars', 'sinput': False}, {'mql': 'sd', 'py': 'sd', 'param': 'sd', 'type': 'int', 'default': 11, 'label': 'Shadow difference for fractal bars', 'sinput': False}, {'mql': 'sdd', 'py': 'sdd', 'param': 'sdd', 'type': 'int', 'default': 6, 'label': 'Shadow difference for double tops/buttoms bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
bd = _input('bd', 7)  # Last bar body length
bdd = _input('bdd', 40)  # Body lenght for double top/buttom bars
sd = _input('sd', 11)  # Shadow difference for fractal bars
sdd = _input('sdd', 6)  # Shadow difference for double tops/buttoms bars
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
StartBars = 0
Bd = 0.0
Bdd = 0.0
Sd = 0.0
Sdd = 0.0
ArrowInterval = 0.0

def GetArrowInterval():
    _sw1 = Period()
    if _sw1 == PERIOD_M1:
        return 5
    elif _sw1 == PERIOD_M2:
        return 5
    elif _sw1 == PERIOD_M3:
        return 6
    elif _sw1 == PERIOD_M4:
        return 6
    elif _sw1 == PERIOD_M5:
        return 7
    elif _sw1 == PERIOD_M6:
        return 8
    elif _sw1 == PERIOD_M10:
        return 9
    elif _sw1 == PERIOD_M12:
        return 9
    elif _sw1 == PERIOD_M15:
        return 10
    elif _sw1 == PERIOD_M20:
        return 12
    elif _sw1 == PERIOD_M30:
        return 15
    elif _sw1 == PERIOD_H1:
        return 20
    elif _sw1 == PERIOD_H2:
        return 23
    elif _sw1 == PERIOD_H3:
        return 27
    elif _sw1 == PERIOD_H4:
        return 30
    elif _sw1 == PERIOD_H6:
        return 35
    elif _sw1 == PERIOD_H8:
        return 50
    elif _sw1 == PERIOD_H12:
        return 65
    elif _sw1 == PERIOD_D1:
        return 80
    elif _sw1 == PERIOD_W1:
        return 150
    elif _sw1 == PERIOD_MN1:
        return 250
    return 10

def OnInit():
    global ArrowInterval, Bd, Bdd, Sd, Sdd, StartBars
    StartBars = 7
    Bd = bd * Point()
    Sd = sd * Point()
    Bdd = bdd * Point()
    Sdd = sdd * Point()
    ArrowInterval = GetArrowInterval() * Point()
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(0, PLOT_ARROW, 108)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetInteger(1, PLOT_ARROW, 108)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'i-Fractals-sig'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBars:
        return 0
    limit = 0
    bar = 0
    bc1 = False
    bc2 = False
    bc3 = False
    sc1 = False
    sc2 = False
    sc3 = False
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - StartBars
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = 0.0
        SellBuffer[bar] = 0.0
        bc1 = False
        bc2 = False
        bc3 = False
        sc1 = False
        sc2 = False
        sc3 = False
        bc1 = (((low[bar + 3] - low[bar + 2]) > Sd and (low[bar + 4] - low[bar + 2]) > Sd) and (low[bar + 1] - low[bar + 2]) > Sd) and (close[bar + 1] - open[bar + 1]) > Bd
        sc1 = (((high[bar + 2] - high[bar + 3]) > Sd and (high[bar + 2] - high[bar + 4]) > Sd) and (high[bar + 2] - high[bar + 1]) > Sd) and (open[bar + 1] - close[bar + 1]) > Bd
        bc2 = ((((low[bar + 4] - low[bar + 2]) > Sd and (low[bar + 5] - low[bar + 2]) > Sd) and (low[bar + 1] - low[bar + 2]) > Sd) and (close[bar + 1] - open[bar + 1]) > Bd) and MathAbs(low[bar + 3] - low[bar + 2]) < Sdd
        sc2 = ((((high[bar + 2] - high[bar + 4]) > Sd and (high[bar + 2] - high[bar + 5]) > Sd) and (high[bar + 2] - high[bar + 1]) > Sd) and (open[bar + 1] - close[bar + 1]) > Bd) and MathAbs(high[bar + 3] - high[bar + 2]) < Sdd
        bc3 = ((((low[bar + 3] - low[bar + 2]) > Sd and (low[bar + 4] - low[bar + 2]) > Sd) and MathAbs(low[bar + 1] - low[bar + 2]) < Sdd) and (close[bar + 1] - open[bar + 1]) > Bdd) and (open[bar + 2] - close[bar + 2]) > Bdd
        sc3 = ((((high[bar + 2] - low[bar + 3]) > Sd and (high[bar + 2] - high[bar + 4]) > Sd) and MathAbs(high[bar + 2] - high[bar + 1]) < Sdd) and (open[bar + 1] - close[bar + 1]) > Bdd) and (close[bar + 2] - open[bar + 2]) > Bdd
        if (bc1 or bc2) or bc3:
            BuyBuffer[bar] = low[bar] - ArrowInterval
        if (sc1 or sc2) or sc3:
            SellBuffer[bar] = high[bar] + ArrowInterval
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IFractalsSig(_MQL5Indicator):
    name = 'i-fractals-sig'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'bd': 7,  # Last bar body length
        'bdd': 40,  # Body lenght for double top/buttom bars
        'sd': 11,  # Shadow difference for fractal bars
        'sdd': 6,  # Shadow difference for double tops/buttoms bars
    }

