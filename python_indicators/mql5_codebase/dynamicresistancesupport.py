"""dynamicresistancesupport — converted from MQL5: MQL5 Indicators/Dynamic Auto Resistance Support/dynamicresistancesupport.mq5

Dynamic Resistance Support
Copyright: 2014, Michael Schmidt root@shellsangles.de; Link: http://www.xvirt.net

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': '2014, Michael Schmidt root@shellsangles.de', 'link': 'http://www.xvirt.net', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [32768]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'Resistance', 2: 'Support'}, 'levels': [], 'description': ['Dynamic Resistance Support'], 'name': 'dynamicresistancesupport', 'source': 'MQL5 Indicators/Dynamic Auto Resistance Support/dynamicresistancesupport.mq5', 'folder': 'Dynamic Auto Resistance Support', 'inputs': [{'mql': 'InpAccurency', 'py': 'InpAccurency', 'param': 'InpAccurency', 'type': 'double', 'default': 75.0, 'label': '', 'sinput': False}, {'mql': 'InpBacklook', 'py': 'InpBacklook', 'param': 'InpBacklook', 'type': 'int', 'default': 100, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtResistanceBuffer = Arr(0, 0.0)
ExtSupportBuffer = Arr(0, 0.0)
InpAccurency = _input('InpAccurency', 75.0)
InpBacklook = _input('InpBacklook', 100)
accurency = 0.0
backlook = 0
avgCandleHeight = 0.0

def OnInit():
    global accurency, backlook
    if InpAccurency > 100.0:
        printf('Incorrect value for input variable InpAccurency=%f to high, set to 100', InpAccurency)
        accurency = 100.0
    elif InpAccurency < 10:
        printf('Incorrect value for input variable InpAccurency=%f to low, set to 10', InpAccurency)
        accurency = 10.0
    else:
        accurency = InpAccurency
    if InpBacklook < 5:
        printf('Incorrect value for input variable InpBacklook=%f to low, set to 5', InpBacklook)
        backlook = 5
    else:
        backlook = InpBacklook
    PlotIndexSetInteger(0, PLOT_ARROW, 158)
    PlotIndexSetInteger(1, PLOT_ARROW, 158)
    SetIndexBuffer(0, ExtResistanceBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtSupportBuffer, INDICATOR_DATA)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    global avgCandleHeight
    start = prev_calculated - 1
    if start < 1:
        ExtResistanceBuffer[0] = EMPTY_VALUE
        ExtSupportBuffer[0] = EMPTY_VALUE
        start = 1
        avgCandleHeight = getAvgCandleHeight(rates_total, High, Low)
        printf('Calculated average candle hight for this time frame is %.4f', avgCandleHeight)
    for i in range(start, rates_total):
        matches = 0
        matchSumUpper = 0.0
        matchSumLower = 0.0
        matchAvgUpper = 0.0
        matchAvgLower = 0.0
        iUpper = High[i] + avgCandleHeight
        iLower = Low[i] - avgCandleHeight
        ExtResistanceBuffer[i] = ExtResistanceBuffer[i - 1]
        ExtSupportBuffer[i] = ExtSupportBuffer[i - 1]
        if not isNormalCandle(High[i], Low[i]):
            continue
        k = i - 1
        while k >= (i - backlook) and k >= 0:
            if High[k] <= iUpper and Low[k] >= iLower:
                matches += 1
                matchSumUpper += High[k]
                matchSumLower += Low[k]
            k -= 1
        if (_fdiv(matches, float(backlook)) * 100) >= accurency:
            matchAvgUpper = _fdiv(matchSumUpper, float(matches))
            matchAvgLower = _fdiv(matchSumLower, float(matches))
            if matchAvgUpper > ExtResistanceBuffer[i] or matchAvgLower < ExtSupportBuffer[i]:
                ExtResistanceBuffer[i] = matchAvgUpper + avgCandleHeight
                ExtSupportBuffer[i] = matchAvgLower - avgCandleHeight
    return rates_total

def getAvgCandleHeight(rates_total, High, Low):
    sum_ = 0.0
    for i in range(0, rates_total - 1):
        sum_ += High[i] - Low[i]
    return _fdiv(sum_, rates_total - 1)

def isNormalCandle(high, low):
    if (high - low) > (avgCandleHeight * 2.0):
        return False
    return True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Dynamicresistancesupport(_MQL5Indicator):
    name = 'dynamicresistancesupport'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'InpAccurency': 75.0,
        'InpBacklook': 100,
    }

