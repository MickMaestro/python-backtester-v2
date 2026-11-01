"""the_20s_v020 — converted from MQL5: MQL5 Indicators/The_20's_v0.20/the_20s_v020.mq5

Copyright: Copyright © 2005, TraderSeven; Link: TraderSeven@gmx.net; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, TraderSeven', 'link': 'TraderSeven@gmx.net', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [15631086], 2: [13749760]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'Sell', 2: 'Buy'}, 'levels': [], 'description': [], 'name': 'the_20s_v020', 'source': "MQL5 Indicators/The_20's_v0.20/the_20s_v020.mq5", 'folder': "The_20's_v0.20", 'inputs': [{'mql': 'Alg', 'py': 'Alg', 'param': 'Alg', 'type': 'int', 'default': 0, 'label': 'Calculation algorithm', 'sinput': False}, {'mql': 'Level', 'py': 'Level', 'param': 'Level', 'type': 'uint', 'default': 100, 'label': 'Trigger level in points', 'sinput': False}, {'mql': 'Ratio', 'py': 'Ratio', 'param': 'Ratio', 'type': 'double', 'default': 0.2, 'label': 'Ratio', 'sinput': False}, {'mql': 'Direct', 'py': 'Direct', 'param': 'Direct', 'type': 'bool', 'default': False, 'label': 'Signal direction', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Mode
MODE_1 = 0
MODE_2 = 1
_enum('Mode', {0: 'MODE_1', 1: 'MODE_2'})

# ---- inputs and global variables
Alg = _input('Alg', MODE_1)  # Calculation algorithm
Level = _input('Level', 100)  # Trigger level in points
Ratio = _input('Ratio', 0.2)  # Ratio
Direct = _input('Direct', False)  # Signal direction
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
dLevel = 0.0
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, dLevel, min_rates_total
    ATR_Period = 15
    min_rates_total = MathMax(5, ATR_Period)
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
        return INIT_FAILED
    dLevel = Level * Point()
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'The_20s_v020'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    LastBarsRange = 0.0
    Top20 = 0.0
    Bottom20 = 0.0
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
    if Direct:
        bar = limit
        for bar in range(bar, 0 - 1, -1):
            BuyBuffer[bar] = 0.0
            SellBuffer[bar] = 0.0
            LastBarsRange = high[bar + 1] - low[bar + 1]
            Top20 = high[bar + 1] - (LastBarsRange * Ratio)
            Bottom20 = low[bar + 1] + (LastBarsRange * Ratio)
            if Alg == MODE_1:
                if (open[bar + 1] >= Top20 and close[bar + 1] <= Bottom20) and low[bar] <= (low[bar + 1] - dLevel):
                    BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
                elif (open[bar + 1] <= Bottom20 and close[bar + 1] >= Top20) and high[bar] >= (high[bar + 1] + dLevel):
                    SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
            if Alg == MODE_2:
                if ((((high[bar + 4] - low[bar + 4]) > LastBarsRange and (high[bar + 3] - low[bar + 3]) > LastBarsRange) and (high[bar + 2] - low[bar + 2]) > LastBarsRange) and high[bar + 2] > high[bar + 1]) and low[bar + 2] < low[bar + 1]:
                    if open[bar] <= Bottom20:
                        BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
                    if open[bar] >= Top20:
                        SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
        else:
            bar = _range_end(bar, 0 - 1, -1)
    if not Direct:
        bar = limit
        for bar in range(bar, 0 - 1, -1):
            BuyBuffer[bar] = 0.0
            SellBuffer[bar] = 0.0
            LastBarsRange = high[bar + 1] - low[bar + 1]
            Top20 = high[bar + 1] - (LastBarsRange * Ratio)
            Bottom20 = low[bar + 1] + (LastBarsRange * Ratio)
            if Alg == MODE_1:
                if (open[bar + 1] >= Top20 and close[bar + 1] <= Bottom20) and low[bar] <= (low[bar + 1] - dLevel):
                    SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
                elif (open[bar + 1] <= Bottom20 and close[bar + 1] >= Top20) and high[bar] >= (high[bar + 1] + dLevel):
                    BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
            if Alg == MODE_2:
                if ((((high[bar + 4] - low[bar + 4]) > LastBarsRange and (high[bar + 3] - low[bar + 3]) > LastBarsRange) and (high[bar + 2] - low[bar + 2]) > LastBarsRange) and high[bar + 2] > high[bar + 1]) and low[bar + 2] < low[bar + 1]:
                    if open[bar] <= Bottom20:
                        SellBuffer[bar] = high[bar] + ((ATR[bar] * 3) / 8)
                    if open[bar] >= Top20:
                        BuyBuffer[bar] = low[bar] - ((ATR[bar] * 3) / 8)
        else:
            bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class The20sV020(_MQL5Indicator):
    name = 'the_20s_v020'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Alg': _Choice({0: 'Option 1', 1: 'Option 2'}, default=0),  # Calculation algorithm
        'Level': 100,  # Trigger level in points
        'Ratio': 0.2,  # Ratio
        'Direct': False,  # Signal direction
    }

