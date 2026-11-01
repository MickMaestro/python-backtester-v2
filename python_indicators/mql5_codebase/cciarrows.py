"""cciarrows — converted from MQL5: MQL5 Indicators/CCIArrows/cciarrows.mq5

CCI Arrows - direct trading signals based on CCI indicator.
Displays red and blue arrows for Short and Long signals.
Copyright: Copyright © 2009, EarnForex; Link: http://www.earnforex.com; Version: 1.20

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2009, EarnForex', 'link': 'http://www.earnforex.com', 'version': '1.20', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [16711935], 2: [16711680]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'CCIArrows Sell', 2: 'CCIArrows Buy'}, 'levels': [], 'description': ['CCI Arrows - direct trading signals based on CCI indicator.', 'Displays red and blue arrows for Short and Long signals.'], 'name': 'cciarrows', 'source': 'MQL5 Indicators/CCIArrows/cciarrows.mq5', 'folder': 'CCIArrows', 'inputs': [{'mql': 'CCI_Period', 'py': 'CCI_Period', 'param': 'CCI_Period', 'type': 'uint', 'default': 14, 'label': 'This value sets the CCI Period Used, The default is 21', 'sinput': False}, {'mql': 'CCI_Price', 'py': 'CCI_Price', 'param': 'CCI_Price', 'type': 'int', 'default': 1, 'label': 'price type', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
CCI_Period = _input('CCI_Period', 14)  # This value sets the CCI Period Used, The default is 21
CCI_Price = _input('CCI_Price', PRICE_CLOSE)  # price type
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
min_rates_total = 0
CCI_Handle = 0

def OnInit():
    global CCI_Handle, min_rates_total
    min_rates_total = _int(CCI_Period + 1)
    CCI_Handle = iCCI(Symbol(), PERIOD_CURRENT, CCI_Period, CCI_Price)
    if CCI_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iCCI indicator')
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(0, PLOT_LABEL, 'CCIArrows Sell')
    PlotIndexSetInteger(0, PLOT_ARROW, 159)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(1, PLOT_LABEL, 'CCIArrows Buy')
    PlotIndexSetInteger(1, PLOT_ARROW, 159)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'CCIArrows'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(CCI_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    CCI = Arr(0, 0.0)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(CCI, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 2
    if CopyBuffer(CCI_Handle, 0, 0, to_copy, CCI) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        SellBuffer[bar] = 0.0
        BuyBuffer[bar] = 0.0
        if CCI[bar + 1] >= 0 and CCI[bar] < 0:
            SellBuffer[bar] = high[bar] + GetRange(high, low, bar)
        if CCI[bar + 1] <= 0 and CCI[bar] > 0:
            BuyBuffer[bar] = low[bar] - GetRange(high, low, bar)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def GetRange(High, Low, index):
    AvgRange = 0.0
    for count in range(index, index + 10):
        AvgRange += MathAbs(High[count] - Low[count])
    return AvgRange / 20


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Cciarrows(_MQL5Indicator):
    name = 'cciarrows'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'CCI_Period': 14,  # This value sets the CCI Period Used, The default is 21
        'CCI_Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # price type
    }

