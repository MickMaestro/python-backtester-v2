"""silvertrend_signal — converted from MQL5: MQL5 Indicators/SilverTrend_HTF_Signal/silvertrend_signal.mq5

Copyright: SilverTrend  rewritten by CrazyChart; Link: http://viac.ru/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'SilverTrend  rewritten by CrazyChart', 'link': 'http://viac.ru/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 2}, 'types': {1: 5, 2: 5}, 'colors': {1: [255], 2: [65280]}, 'widths': {1: 4, 2: 4}, 'styles': {}, 'labels': {1: 'Silver Sell', 2: 'Silver Buy'}, 'levels': [], 'description': [], 'name': 'silvertrend_signal', 'source': 'MQL5 Indicators/SilverTrend_HTF_Signal/silvertrend_signal.mq5', 'folder': 'SilverTrend_HTF_Signal', 'inputs': [{'mql': 'RISK', 'py': 'RISK', 'param': 'RISK', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'int', 'default': 2, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RISK = _input('RISK', 3)
NumberofAlerts = _input('NumberofAlerts', 2)
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
K = 0
SSP = 9
counter = 0
old = False
uptrend_ = False
StartBars = 0

def OnInit():
    global StartBars
    StartBars = SSP + 1
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(0, PLOT_LABEL, 'Silver Sell')
    PlotIndexSetInteger(0, PLOT_ARROW, 108)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetString(1, PLOT_LABEL, 'Silver Buy')
    PlotIndexSetInteger(1, PLOT_ARROW, 108)
    ArraySetAsSeries(BuyBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'SilverTrend_Signal'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global K, counter, old, uptrend_
    if rates_total < StartBars:
        return 0
    limit = 0
    Range = 0.0
    AvgRange = 0.0
    smin = 0.0
    smax = 0.0
    SsMax = 0.0
    SsMin = 0.0
    price = 0.0
    uptrend = False
    if prev_calculated > rates_total or prev_calculated <= 0:
        K = 33 - RISK
        limit = rates_total - StartBars
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    uptrend = uptrend_
    for bar in range(limit, 0 - 1, -1):
        if rates_total != prev_calculated and bar == 0:
            uptrend_ = uptrend
        Range = 0.0
        AvgRange = 0.0
        for iii in range(bar, bar + SSP + 1):
            AvgRange = AvgRange + MathAbs(high[iii] - low[iii])
        Range = _fdiv(AvgRange, SSP + 1)
        SsMax = low[bar]
        SsMin = close[bar]
        for kkk in range(bar, bar + SSP - 1 + 1):
            price = high[kkk]
            if SsMax < price:
                SsMax = price
            price = low[kkk]
            if SsMin >= price:
                SsMin = price
        smin = SsMin + (((SsMax - SsMin) * K) / 100)
        smax = SsMax - (((SsMax - SsMin) * K) / 100)
        SellBuffer[bar] = 0.0
        BuyBuffer[bar] = 0.0
        if close[bar] < smin:
            uptrend = False
        if close[bar] > smax:
            uptrend = True
        if uptrend != old and uptrend == True:
            BuyBuffer[bar] = low[bar] - (Range * 0.5)
            if bar == 0:
                if counter <= NumberofAlerts:
                    Alert('Silver Trend ', EnumToString(Period(), ''), ' ', Symbol(), ' BUY')
                    counter += 1
            else:
                counter = 0
        if uptrend != old and uptrend == False:
            SellBuffer[bar] = high[bar] + (Range * 0.5)
            if bar == 0:
                if counter <= NumberofAlerts:
                    Alert('Silver Trend ', EnumToString(Period(), ''), ' ', Symbol(), ' SELL')
                    counter += 1
            else:
                counter = 0
        if bar > 0:
            old = uptrend
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SilvertrendSignal(_MQL5Indicator):
    name = 'silvertrend_signal'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RISK': 3,
        'NumberofAlerts': 2,
    }

