"""i-impulsesystem — converted from MQL5: MQL5 Indicators/i-ImpulseSystem/i-impulsesystem.mq5

The Indicator is based on Elder's Impulse system
Copyright: Copyright 2010, D.Zhebrak aka Necron; Link: www.mqlcoder.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2010, D.Zhebrak aka Necron', 'link': 'www.mqlcoder.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [65280, 255, 8421504]}, 'widths': {1: 1}, 'styles': {}, 'labels': {1: 'Open;High;Low;Close'}, 'levels': [], 'description': ["The Indicator is based on Elder's Impulse system"], 'name': 'i-impulsesystem', 'source': 'MQL5 Indicators/i-ImpulseSystem/i-impulsesystem.mq5', 'folder': 'i-ImpulseSystem', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
OBuffer = Arr(0, 0.0)
HBuffer = Arr(0, 0.0)
LBuffer = Arr(0, 0.0)
CBuffer = Arr(0, 0.0)
OsMaBuffer = Arr(0, 0.0)
EMABuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
hOsMaBuffer = 0
hEMABuffer = 0

def OnInit():
    global hEMABuffer, hOsMaBuffer
    if ChartGetInteger(0, CHART_MODE) != CHART_CANDLES:
        Print("It's better to set candstick mode on the chart.")
    SetIndexBuffer(0, OBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, HBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, LBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, CBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, OsMaBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, EMABuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, 27)
    IndicatorSetString(INDICATOR_SHORTNAME, 'i-ImpulseSystem')
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    hOsMaBuffer = iOsMA(Symbol(), PERIOD_CURRENT, 12, 26, 9, PRICE_CLOSE)
    hEMABuffer = iMA(Symbol(), PERIOD_CURRENT, 13, 0, MODE_EMA, PRICE_CLOSE)
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    i = 0
    if rates_total < 27:
        Print('Not enough history for indicator i-ImpulseSystem!')
        return 0
    calculated = BarsCalculated(hOsMaBuffer)
    if calculated < rates_total:
        Print('Not all data of hOsMaBuffer is calculated (', calculated, 'bars ). Error ', GetLastError())
        return 0
    calculated = BarsCalculated(hEMABuffer)
    if calculated < rates_total:
        Print('Not all data of hEMABuffer is calculated (', calculated, 'bars ). Error ', GetLastError())
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if CopyBuffer(hOsMaBuffer, 0, 0, to_copy, OsMaBuffer) <= 0:
        Print('Getting iOsma is failed! Error ', GetLastError())
        return 0
    if CopyBuffer(hEMABuffer, 0, 0, to_copy, EMABuffer) <= 0:
        Print('Getting iMa is failed! Error ', GetLastError())
        return 0
    start = 0
    if prev_calculated == 0:
        start = 1
    else:
        start = prev_calculated - 1
    i = start
    for i in range(i, rates_total):
        OBuffer[i] = open[i]
        HBuffer[i] = high[i]
        LBuffer[i] = low[i]
        CBuffer[i] = close[i]
        if OsMaBuffer[i] > OsMaBuffer[i - 1] and EMABuffer[i] > EMABuffer[i - 1]:
            ColorBuffer[i] = 0.0
        elif OsMaBuffer[i] < OsMaBuffer[i - 1] and EMABuffer[i] < EMABuffer[i - 1]:
            ColorBuffer[i] = 1.0
        else:
            ColorBuffer[i] = 2.0
    else:
        i = _range_end(i, rates_total, 1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IImpulsesystem(_MQL5Indicator):
    name = 'i-impulsesystem'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

