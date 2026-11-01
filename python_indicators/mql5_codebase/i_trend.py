"""i_trend — converted from MQL5: MQL5 Indicators/i_Trend/i_trend.mq5

Expert rewritten from MQL4, author is unknown, published on mql4.com by Scriptor (http://www.mql4.com/ru/users/Scriptor), link - http://codebase.mql4.com/ru/1712
Copyright: Integer; Link: https://login.mql5.com/ru/users/Integer; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Integer', 'link': 'https://login.mql5.com/ru/users/Integer', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 6, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [3329330], 2: [255]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Label1', 2: 'Label2'}, 'levels': [], 'description': ['', 'Expert rewritten from MQL4, author is unknown, published on mql4.com by Scriptor (http://www.mql4.com/ru/users/Scriptor), link - http://codebase.mql4.com/ru/1712'], 'name': 'i_trend', 'source': 'MQL5 Indicators/i_Trend/i_trend.mq5', 'folder': 'i_Trend', 'inputs': [{'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Price', 'sinput': False}, {'mql': 'BBPeriod', 'py': 'BBPeriod', 'param': 'BBPeriod', 'type': 'int', 'default': 20, 'label': 'BBPeriod', 'sinput': False}, {'mql': 'BBShift', 'py': 'BBShift', 'param': 'BBShift', 'type': 'int', 'default': 0, 'label': 'BBShift', 'sinput': False}, {'mql': 'BBDeviation', 'py': 'BBDeviation', 'param': 'BBDeviation', 'type': 'double', 'default': 2.0, 'label': 'BBDeviation', 'sinput': False}, {'mql': 'BBPrice', 'py': 'BBPrice', 'param': 'BBPrice', 'type': 'int', 'default': 1, 'label': 'BBPrice', 'sinput': False}, {'mql': 'BBLine', 'py': 'BBLine', 'param': 'BBLine', 'type': 'int', 'default': 0, 'label': 'BBLine', 'sinput': False}, {'mql': 'BullsBearsPeriod', 'py': 'BullsBearsPeriod', 'param': 'BullsBearsPeriod', 'type': 'int', 'default': 14, 'label': 'BullsBearsPeriod', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum EBBLine
Base = 0
Upper = 1
Lower = 2
_enum('EBBLine', {0: 'Base', 1: 'Upper', 2: 'Lower'})

# ---- inputs and global variables
Price = _input('Price', PRICE_CLOSE)  # Price
BBPeriod = _input('BBPeriod', 20)  # BBPeriod
BBShift = _input('BBShift', 0)  # BBShift
BBDeviation = _input('BBDeviation', 2.0)  # BBDeviation
BBPrice = _input('BBPrice', PRICE_CLOSE)  # BBPrice
BBLine = _input('BBLine', BASE_LINE)  # BBLine
BullsBearsPeriod = _input('BullsBearsPeriod', 14)  # BullsBearsPeriod
Label1Buffer = Arr(0, 0.0)
Label2Buffer = Arr(0, 0.0)
BufBB = Arr(0, 0.0)
BufBu = Arr(0, 0.0)
BufBe = Arr(0, 0.0)
BufMA = Arr(0, 0.0)
BBHand = INVALID_HANDLE
BullsHand = INVALID_HANDLE
BearsHand = INVALID_HANDLE
MAHand = INVALID_HANDLE

def OnInit_1():
    global BBHand, BearsHand, BullsHand, MAHand
    BBHand = iBands(None, PERIOD_CURRENT, BBPeriod, BBShift, BBDeviation, BBPrice)
    BullsHand = iBullsPower(None, PERIOD_CURRENT, BullsBearsPeriod)
    BearsHand = iBearsPower(None, PERIOD_CURRENT, BullsBearsPeriod)
    MAHand = iMA(None, PERIOD_CURRENT, 1, 0, 0, Price)
    if ((BBHand == INVALID_HANDLE or BullsHand == INVALID_HANDLE) or BearsHand == INVALID_HANDLE) or MAHand == INVALID_HANDLE:
        Alert('Failed to loading the indicator, try again')
        return -1
    SetIndexBuffer(0, Label1Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, Label2Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, BufBB, INDICATOR_CALCULATIONS)
    SetIndexBuffer(3, BufBu, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufBe, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufMA, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, BBPeriod + BBShift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, BullsBearsPeriod)
    return 0

def OnInit_2(reason):
    if BBHand != INVALID_HANDLE:
        IndicatorRelease(BBHand)
    if BullsHand != INVALID_HANDLE:
        IndicatorRelease(BullsHand)
    if BearsHand != INVALID_HANDLE:
        IndicatorRelease(BearsHand)
    if MAHand != INVALID_HANDLE:
        IndicatorRelease(MAHand)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_error
    start = 0
    if prev_calculated == 0:
        _s_OnCalculate_error = True
    if _s_OnCalculate_error:
        start = 0
        _s_OnCalculate_error = False
    else:
        start = prev_calculated - 1
    if ((CopyBuffer(BBHand, BBLine, 0, rates_total - start, BufBB) == -1 or CopyBuffer(BullsHand, 0, 0, rates_total - start, BufBu) == -1) or CopyBuffer(BearsHand, 0, 0, rates_total - start, BufBe) == -1) or CopyBuffer(MAHand, 0, 0, rates_total - start, BufMA) == -1:
        _s_OnCalculate_error = True
        return 0
    for i in range(start, rates_total):
        Label1Buffer[i] = BufMA[i] - BufBB[i]
        Label2Buffer[i] = -(BufBe[i] + BufBu[i])
    return rates_total

# ---- static local variables
_s_OnCalculate_error = True


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ITrend(_MQL5Indicator):
    name = 'i_trend'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Price
        'BBPeriod': 20,  # BBPeriod
        'BBShift': 0,  # BBShift
        'BBDeviation': 2.0,  # BBDeviation
        'BBPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # BBPrice
        'BBLine': _Choice({0: 'Base', 1: 'Upper', 2: 'Lower'}, default=0),  # BBLine
        'BullsBearsPeriod': 14,  # BullsBearsPeriod
    }

