"""i-intradayfibonacci — converted from MQL5: MQL5 Indicators/i-IntradayFibonacci/i-intradayfibonacci.mq5

Copyright: Copyright © 2007, Kim Igor V. aka KimIV; Link: http://www.kimiv.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, Kim Igor V. aka KimIV', 'link': 'http://www.kimiv.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 8}, 'types': {1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5}, 'colors': {1: [16711680], 2: [65280], 3: [42495], 4: [9639167], 5: [9639167], 6: [42495], 7: [65280], 8: [16711680]}, 'widths': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1}, 'styles': {}, 'labels': {1: 'INDICATOR_NAME+" -0.236"', 2: 'INDICATOR_NAME+" -0.382"', 3: 'INDICATOR_NAME+" -0.618"', 4: 'INDICATOR_NAME+" -0.764"'}, 'levels': [], 'description': [], 'name': 'i-intradayfibonacci', 'source': 'MQL5 Indicators/i-IntradayFibonacci/i-intradayfibonacci.mq5', 'folder': 'i-IntradayFibonacci', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16408, 'label': 'Chart period', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'vertical shift of the indicator in points', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_D1)  # Chart period
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # vertical shift of the indicator in points
IndBuffer1 = Arr(0, 0.0)
IndBuffer2 = Arr(0, 0.0)
IndBuffer3 = Arr(0, 0.0)
IndBuffer4 = Arr(0, 0.0)
IndBuffer5 = Arr(0, 0.0)
IndBuffer6 = Arr(0, 0.0)
IndBuffer7 = Arr(0, 0.0)
IndBuffer8 = Arr(0, 0.0)
Init = False
Symbol_ = ""
min_rates_total = 0

def IndInit(Number, Arrow, DRAW_BEGIN_, EMPTY_VALUE_):
    SetIndexBuffer(Number, Arrow, INDICATOR_DATA)
    PlotIndexSetInteger(Number, PLOT_DRAW_BEGIN, DRAW_BEGIN_)
    PlotIndexSetDouble(Number, PLOT_EMPTY_VALUE, EMPTY_VALUE_)
    ArraySetAsSeries(Arrow, True)

def OnInit():
    global Init, Symbol_, min_rates_total
    Init = True
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('The chart period cannot be less than the current chart period')
        Init = False
        return
    min_rates_total = _idiv(PeriodSeconds(TimeFrame), PeriodSeconds(PERIOD_CURRENT)) + 1
    Symbol_ = Symbol()
    IndInit(0, IndBuffer1, min_rates_total, 0.0)
    IndInit(1, IndBuffer2, min_rates_total, 0.0)
    IndInit(2, IndBuffer3, min_rates_total, 0.0)
    IndInit(3, IndBuffer4, min_rates_total, 0.0)
    IndInit(4, IndBuffer5, min_rates_total, 0.0)
    IndInit(5, IndBuffer6, min_rates_total, 0.0)
    IndInit(6, IndBuffer7, min_rates_total, 0.0)
    IndInit(7, IndBuffer8, min_rates_total, 0.0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'i-IntradayFibonacci')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total or (not Init):
        return 0
    iHigh_ = Arr(2, 0.0, dyn=False)
    iLow_ = Arr(2, 0.0, dyn=False)
    limit = 0
    bar = 0
    iTime_ = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if CopyTime(Symbol_, TimeFrame, _DT(time[bar]), 1, iTime_) <= 0:
            return 0
        if time[bar] >= iTime_[0] and time[bar + 1] < iTime_[0]:
            _s_OnCalculate_LastCountBar = bar
            if CopyLow(Symbol_, TimeFrame, _DT(time[bar]), 2, iLow_) <= 0:
                return 0
            if CopyHigh(Symbol_, TimeFrame, _DT(time[bar]), 2, iHigh_) <= 0:
                return 0
            Range = iHigh_[0] - iLow_[0]
            IndBuffer1[bar] = iHigh_[0] + (Range * 0.764)
            IndBuffer2[bar] = iHigh_[0] + (Range * 0.618)
            IndBuffer3[bar] = iHigh_[0] + (Range * 0.382)
            IndBuffer4[bar] = iHigh_[0] + (Range * 0.236)
            IndBuffer5[bar] = iLow_[0] - (Range * 0.236)
            IndBuffer6[bar] = iLow_[0] - (Range * 0.382)
            IndBuffer7[bar] = iLow_[0] - (Range * 0.618)
            IndBuffer8[bar] = iLow_[0] - (Range * 0.764)
        else:
            IndBuffer1[bar] = IndBuffer1[bar + 1]
            IndBuffer2[bar] = IndBuffer2[bar + 1]
            IndBuffer3[bar] = IndBuffer3[bar + 1]
            IndBuffer4[bar] = IndBuffer4[bar + 1]
            IndBuffer5[bar] = IndBuffer5[bar + 1]
            IndBuffer6[bar] = IndBuffer6[bar + 1]
            IndBuffer7[bar] = IndBuffer7[bar + 1]
            IndBuffer8[bar] = IndBuffer8[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IIntradayfibonacci(_MQL5Indicator):
    name = 'i-intradayfibonacci'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16408),  # Chart period
        'Shift': 0,  # horizontal shift of the indicator in bars
        'PriceShift': 0,  # vertical shift of the indicator in points
    }

