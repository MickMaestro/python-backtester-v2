"""i-sig — converted from MQL5: MQL5 Indicators/i-sig/i-sig.mq5

Copyright: Copyright © 2005, 3172552 & KimIV; Link: http://www.kimiv.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, 3172552 & KimIV', 'link': 'http://www.kimiv.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'i-sig Sell', 2: 'i-sig Buy'}, 'levels': [], 'description': [], 'name': 'i-sig', 'source': 'MQL5 Indicators/i-sig/i-sig.mq5', 'folder': 'i-sig', 'inputs': [{'mql': 'bd', 'py': 'bd', 'param': 'bd', 'type': 'uint', 'default': 7, 'label': 'Last bar body lenght', 'sinput': False}, {'mql': 'bdd', 'py': 'bdd', 'param': 'bdd', 'type': 'uint', 'default': 40, 'label': 'Body lenght for double top/buttom bars', 'sinput': False}, {'mql': 'sd', 'py': 'sd', 'param': 'sd', 'type': 'uint', 'default': 11, 'label': 'Shadow difference for fractal bars', 'sinput': False}, {'mql': 'sdd', 'py': 'sdd', 'param': 'sdd', 'type': 'uint', 'default': 6, 'label': 'Shadow difference for double tops/buttoms bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
bd = _input('bd', 7)  # Last bar body lenght
bdd = _input('bdd', 40)  # Body lenght for double top/buttom bars
sd = _input('sd', 11)  # Shadow difference for fractal bars
sdd = _input('sdd', 6)  # Shadow difference for double tops/buttoms bars
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
sd_Point = 0.0
bd_Point = 0.0
sdd_Point = 0.0
bdd_Point = 0.0
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, bd_Point, bdd_Point, min_rates_total, sd_Point, sdd_Point
    ATR_Period = 15
    min_rates_total = MathMax(ATR_Period, 5)
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
        return INIT_FAILED
    sd_Point = sd * Point()
    bd_Point = bd * Point()
    sdd_Point = sdd * Point()
    bdd_Point = bdd * Point()
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 115)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 115)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'i-sig'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    ATR = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(ATR, True)
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
        bc1 = (((low[bar + 3] - low[bar + 2]) > sd_Point and (low[bar + 4] - low[bar + 2]) > sd_Point) and (low[bar + 1] - low[bar + 2]) > sd_Point) and (close[bar + 1] - open[bar + 1]) > bd_Point
        sc1 = (((high[bar + 2] - high[bar + 3]) > sd_Point and (high[bar + 2] - high[bar + 4]) > sd_Point) and (high[bar + 2] - high[bar + 1]) > sd_Point) and (open[bar + 1] - close[bar + 1]) > bd_Point
        bc2 = ((((low[bar + 4] - low[bar + 2]) > sd_Point and (low[bar + 5] - low[bar + 2]) > sd_Point) and (low[bar + 1] - low[bar + 2]) > sd_Point) and (close[bar + 1] - open[bar + 1]) > bd_Point) and MathAbs(low[bar + 3] - low[bar + 2]) < sdd_Point
        sc2 = ((((high[bar + 2] - high[bar + 4]) > sd_Point and (high[bar + 2] - high[bar + 5]) > sd_Point) and (high[bar + 2] - high[bar + 1]) > sd_Point) and (open[bar + 1] - close[bar + 1]) > bd_Point) and MathAbs(high[bar + 3] - high[bar + 2]) < sdd_Point
        bc3 = ((((low[bar + 3] - low[bar + 2]) > sd_Point and (low[bar + 4] - low[bar + 2]) > sd_Point) and MathAbs(low[bar + 1] - low[bar + 2]) < sdd_Point) and (close[bar + 1] - open[bar + 1]) > bdd_Point) and (open[bar + 2] - close[bar + 2]) > bdd_Point
        sc3 = ((((high[bar + 2] - high[bar + 3]) > sd_Point and (high[bar + 2] - high[bar + 4]) > sd_Point) and MathAbs(high[bar + 2] - high[bar + 1]) < sdd_Point) and (open[bar + 1] - close[bar + 1]) > bdd_Point) and (close[bar + 2] - open[bar + 2]) > bdd_Point
        if (bc1 or bc2) or bc3:
            BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        if (sc1 or sc2) or sc3:
            SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ISig(_MQL5Indicator):
    name = 'i-sig'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'bd': 7,  # Last bar body lenght
        'bdd': 40,  # Body lenght for double top/buttom bars
        'sd': 11,  # Shadow difference for fractal bars
        'sdd': 6,  # Shadow difference for double tops/buttoms bars
    }

