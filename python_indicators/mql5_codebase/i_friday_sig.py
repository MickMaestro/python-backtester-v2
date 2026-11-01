"""i-friday_sig — converted from MQL5: MQL5 Indicators/i-Friday_Sig/i-friday_sig.mq5

Input and output signals by the Friday effect system
Copyright: Copyright © 2005, Igor V. Kim aka KimIV; Link: http://www.kimiv.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Igor V. Kim aka KimIV', 'link': 'http://www.kimiv.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [65280], 2: [255], 3: [65280], 4: [255]}, 'widths': {1: 2, 2: 2, 3: 5, 4: 5}, 'styles': {}, 'labels': {1: 'i-Friday_Sig Buy', 2: 'i-Friday_Sig Sell', 3: 'i-Friday_Sig Buy Stop', 4: 'i-Friday_Sig Sell Stop'}, 'levels': [], 'description': ['Input and output signals by the Friday effect system'], 'name': 'i-friday_sig', 'source': 'MQL5 Indicators/i-Friday_Sig/i-friday_sig.mq5', 'folder': 'i-Friday_Sig', 'inputs': [{'mql': 'HourOpenPos', 'py': 'HourOpenPos', 'param': 'HourOpenPos', 'type': 'int', 'default': 6, 'label': 'Time of position opening', 'sinput': False}, {'mql': 'HourClosePos', 'py': 'HourClosePos', 'param': 'HourClosePos', 'type': 'int', 'default': 18, 'label': 'Time of position closing', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum Hour
H0_ = 0
H1_ = 1
H2_ = 2
H3_ = 3
H4_ = 4
H5_ = 5
H7_ = 6
H8_ = 7
H9_ = 8
H10_ = 9
H11_ = 10
H12_ = 11
H13_ = 12
H14_ = 13
H15_ = 14
H16_ = 15
H17_ = 16
H18_ = 17
H19_ = 18
H20_ = 19
H21_ = 20
H22_ = 21
H23_ = 22
_enum('Hour', {0: 'H0_', 1: 'H1_', 2: 'H2_', 3: 'H3_', 4: 'H4_', 5: 'H5_', 6: 'H7_', 7: 'H8_', 8: 'H9_', 9: 'H10_', 10: 'H11_', 11: 'H12_', 12: 'H13_', 13: 'H14_', 14: 'H15_', 15: 'H16_', 16: 'H17_', 17: 'H18_', 18: 'H19_', 19: 'H20_', 20: 'H21_', 21: 'H22_', 22: 'H23_'})

# ---- inputs and global variables
HourOpenPos = _input('HourOpenPos', H7_)  # Time of position opening
HourClosePos = _input('HourClosePos', H19_)  # Time of position closing
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
BuyBuffer = Arr(0, 0.0)
SellBuffer = Arr(0, 0.0)
BuyStopBuffer = Arr(0, 0.0)
SellStopBuffer = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_total
    ATRPeriod = 10
    ATR_Handle = iATR(None, 0, ATRPeriod)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the ATR indicator')
        return 1
    if PeriodSeconds(PERIOD_CURRENT) > PeriodSeconds(PERIOD_H1):
        Print('The i-Friday_Sig indicator does not works at Time Frames more than a hour')
        return 1
    min_rates_total = MathMax(_idiv(2 * PeriodSeconds(PERIOD_D1), PeriodSeconds(PERIOD_CURRENT)), ATRPeriod)
    SetIndexBuffer(0, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(BuyBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_ARROW, 233)
    SetIndexBuffer(1, SellBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SellBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_ARROW, 234)
    SetIndexBuffer(2, BuyStopBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(BuyStopBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_ARROW, 163)
    SetIndexBuffer(3, SellStopBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(SellStopBuffer, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_ARROW, 163)
    shortname = Box("")
    StringConcatenate(shortname, 'i-Friday_Sig(', HourOpenPos, ', ', HourClosePos, ', ', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    if PeriodSeconds(PERIOD_CURRENT) > PeriodSeconds(PERIOD_H1):
        return 0
    ATR = Arr(0, 0.0)
    iOpen_ = Arr(2, 0.0, dyn=False)
    iClose_ = Arr(2, 0.0, dyn=False)
    limit = 0
    to_copy = 0
    bar = 0
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        BuyBuffer[bar] = EMPTY_VALUE
        SellBuffer[bar] = EMPTY_VALUE
        BuyStopBuffer[bar] = EMPTY_VALUE
        SellStopBuffer[bar] = EMPTY_VALUE
        if CopyOpen(Symbol(), PERIOD_D1, _DT(time[bar]), 2, iOpen_) <= 0:
            return 0
        if CopyClose(Symbol(), PERIOD_D1, _DT(time[bar]), 2, iClose_) <= 0:
            return 0
        tm = MqlDateTime()
        TimeToStruct(time[bar], tm)
        if tm.day_of_week == 5 and tm.min == 0:
            if tm.hour == HourOpenPos:
                if iOpen_[0] > iClose_[0]:
                    BuyBuffer[bar] = low[bar] - (ATR[bar] / 3)
                if iOpen_[0] < iClose_[0]:
                    SellBuffer[bar] = high[bar] + (ATR[bar] / 3)
            if tm.hour == HourClosePos:
                if iOpen_[0] > iClose_[0]:
                    BuyStopBuffer[bar] = close[bar]
                if iOpen_[0] < iClose_[0]:
                    SellStopBuffer[bar] = close[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IFridaySig(_MQL5Indicator):
    name = 'i-friday_sig'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'HourOpenPos': _Choice({0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '7', 7: '8', 8: '9', 9: '10', 10: '11', 11: '12', 12: '13', 13: '14', 14: '15', 15: '16', 16: '17', 17: '18', 18: '19', 19: '20', 20: '21', 21: '22', 22: '23'}, default=6),  # Time of position opening
        'HourClosePos': _Choice({0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '7', 7: '8', 8: '9', 9: '10', 10: '11', 11: '12', 12: '13', 13: '14', 14: '15', 15: '16', 16: '17', 17: '18', 18: '19', 19: '20', 20: '21', 21: '22', 22: '23'}, default=18),  # Time of position closing
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }

