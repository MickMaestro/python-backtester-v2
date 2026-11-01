"""predict — converted from MQL5: MQL5 Indicators/Predict/predict.mq5

Copyright: Copyright © 2006, Ronald Verwer / ROVERCOM; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Ronald Verwer / ROVERCOM', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 5, 2: 5, 3: 5}, 'colors': {1: [16711935], 2: [65280], 3: [16711680]}, 'widths': {1: 2, 2: 2, 3: 3}, 'styles': {}, 'labels': {1: 'Predict Sell', 2: 'Predict Buy', 3: 'Predict Fl'}, 'levels': [], 'description': [''], 'name': 'predict', 'source': 'MQL5 Indicators/Predict/predict.mq5', 'folder': 'Predict', 'inputs': [{'mql': 'BuyLevel', 'py': 'BuyLevel', 'param': 'BuyLevel', 'type': 'int', 'default': 56, 'label': '', 'sinput': False}, {'mql': 'SellLevel', 'py': 'SellLevel', 'param': 'SellLevel', 'type': 'int', 'default': 56, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
BuyLevel = _input('BuyLevel', 56)
SellLevel = _input('SellLevel', 56)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
FlBuffer = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 11
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 119)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 119)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, FlBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    ArraySetAsSeries(FlBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Predict'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    global _s_OnCalculate_Drctn1
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    Drctn0 = 0
    D1 = 0.0
    D2 = 0.0
    Pr = 0.0
    Range = 0.0
    AvgRange = 0.0
    Txt = ""
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        _s_OnCalculate_Drctn1 = 0
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        SellBuffer[bar] = 0.0
        BuyBuffer[bar] = 0.0
        FlBuffer[bar] = 0.0
        AvgRange = 0.0
        for count in range(bar, bar + 10):
            AvgRange = AvgRange + MathAbs(High[count] - Low[count])
        Range = AvgRange / 10
        Range = Range / 2
        D1 = (Close[bar + 1] + Close[bar + 2]) / 2
        D2 = (Close[bar + 1] + Close[bar + 2] + Close[bar + 3] + Close[bar + 4] + Close[bar + 5]) / 5
        if Close[bar + 1]:
            Pr = (((_fdiv(MathAbs(D1 - D2), Close[bar + 1]) * 125.75) + 0.54528) * 10000) / 100
        if D1 > D2 and Pr > BuyLevel:
            Drctn0 = 1
            if Drctn0 != _s_OnCalculate_Drctn1:
                BuyBuffer[bar] = Low[bar] - Range
        elif D1 < D2 and Pr > SellLevel:
            Drctn0 = -1
            if Drctn0 != _s_OnCalculate_Drctn1:
                SellBuffer[bar] = High[bar] + Range
        elif Pr > 50 and Pr < 60:
            Drctn0 = 0
            if _s_OnCalculate_Drctn1 == 1:
                FlBuffer[bar] = Low[bar] - Range
            elif _s_OnCalculate_Drctn1 == -1:
                FlBuffer[bar] = High[bar] + Range
        else:
            Drctn0 = 0
        if bar:
            _s_OnCalculate_Drctn1 = Drctn0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if Drctn0 == -1:
        Txt = 'Short'
    elif Drctn0 == 1:
        Txt = 'Long'
    else:
        Txt = 'Flat'
    Comment('Predictions: Pr = ' + DoubleToString(Pr, 3) + ' ; Current Signal =  ' + Txt)
    return rates_total

# ---- static local variables
_s_OnCalculate_Drctn1 = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Predict(_MQL5Indicator):
    name = 'predict'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BuyLevel': 56,
        'SellLevel': 56,
    }

