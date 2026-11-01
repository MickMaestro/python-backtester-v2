"""MACrossAlerter — converted from MQL5: MQL5 Indicators/Moving Average with alerts on price crossovers/MACrossAlerter.mq5

Copyright: Copyright 2023, https://www.mql5.com/en/users/phade/; Link: https://www.mql5.com/en/users/phade/; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2023, https://www.mql5.com/en/users/phade/', 'link': 'https://www.mql5.com/en/users/phade/', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [8421504]}, 'widths': {1: 1}, 'styles': {1: 2}, 'labels': {1: 'Line'}, 'levels': [], 'description': [], 'name': 'MACrossAlerter', 'source': 'MQL5 Indicators/Moving Average with alerts on price crossovers/MACrossAlerter.mq5', 'folder': 'Moving Average with alerts on price crossovers', 'inputs': [{'mql': 'slowPeriod', 'py': 'slowPeriod', 'param': 'slowPeriod', 'type': 'int', 'default': 44, 'label': 'Moving Average Length', 'sinput': False}, {'mql': 'Audio_Alert_Sound', 'py': 'Audio_Alert_Sound', 'param': None, 'type': 'string', 'default': 'alert.wav', 'label': 'Audio alert sample', 'sinput': False}, {'mql': 'Audio_Alert_On_Signals', 'py': 'Audio_Alert_On_Signals', 'param': 'Audio_Alert_On_Signals', 'type': 'bool', 'default': False, 'label': 'Enable audio alerts', 'sinput': False}, {'mql': 'pointNum', 'py': 'pointNum', 'param': 'pointNum', 'type': 'int', 'default': 100, 'label': 'Amount of points on MA crossover that should enable a signal', 'sinput': False}, {'mql': 'LongSignalColor', 'py': 'LongSignalColor', 'param': None, 'type': 'color', 'default': 8388736, 'label': 'Set the up arrow color (long signals)', 'sinput': False}, {'mql': 'ShortSignalColor', 'py': 'ShortSignalColor', 'param': None, 'type': 'color', 'default': 0, 'label': 'Set the down arrow color (short signals)', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
prevPeriod = PERIOD_CURRENT
slowPeriod = _input('slowPeriod', 44)  # Moving Average Length
indvalue = Arr(0, 0.0)
slowma = Arr(0, 0.0)
handle = 0
max_bars = 0
arrowDistance = 250.0  # Desired distance
Audio_Alert_Sound = _input('Audio_Alert_Sound', 'alert.wav')  # Audio alert sample
Audio_Alert_On_Signals = _input('Audio_Alert_On_Signals', False)  # Enable audio alerts
pointNum = _input('pointNum', 100)  # Amount of points on MA crossover that should enable a signal
LongSignalColor = _input('LongSignalColor', clrPurple)  # Set the up arrow color (long signals)
ShortSignalColor = _input('ShortSignalColor', clrBlack)  # Set the down arrow color (short signals)
gLongSignal = 0.0
gShortSignal = 0.0

def OnInit():
    global handle, max_bars
    SetIndexBuffer(0, indvalue, INDICATOR_DATA)
    handle = iMA(Symbol(), PERIOD_CURRENT, slowPeriod, 0, MODE_SMA, PRICE_CLOSE)
    if handle == INVALID_HANDLE:
        Print('Get MA Handle failed!')
        return INIT_FAILED
    max_bars = Bars(Symbol(), Period())
    ArrayResize(slowma, max_bars)
    ArrayResize(indvalue, max_bars)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global arrowDistance, gLongSignal, gShortSignal, last_playsound_time, prevPeriod
    to_copy = rates_total - prev_calculated
    if to_copy <= 0:
        to_copy = max_bars
    limit = MathMin(rates_total - prev_calculated, rates_total)
    CopyBuffer(handle, 0, 0, to_copy, slowma)
    if ChartPeriod() != prevPeriod:
        prevPeriod = ChartPeriod()
        ChartRedraw()
    if Period() == PERIOD_M1:
        arrowDistance = 5.0
    elif Period() == PERIOD_M2:
        arrowDistance = 5.0
    elif Period() == PERIOD_M5:
        arrowDistance = 20.0
    elif Period() == PERIOD_M15:
        arrowDistance = 20.0
    elif Period() == PERIOD_M30:
        arrowDistance = 20.0
    elif Period() == PERIOD_H1:
        arrowDistance = 40.0
    elif Period() == PERIOD_H4:
        arrowDistance = 40.0
    elif Period() == PERIOD_D1:
        arrowDistance = 40.0
    elif Period() == PERIOD_W1:
        arrowDistance = 40.0
    elif Period() == PERIOD_MN1:
        arrowDistance = 40.0
    for i in range(prev_calculated - (rates_total == prev_calculated), limit):
        indvalue[i] = slowma[i]
        noSidewaysMarket = False
        significantLiquidity = False
        if i > 0:
            noSidewaysMarket = MathAbs(close[i] - close[i - 1]) > (10 * Point())
        if i > 3:
            significantLiquidity = MathAbs(close[i] - close[i - 3]) > (8 * Point())
        greenCandleFormation = close[i] > open[i]
        redCandleFormation = close[i] < open[i]
        if ((i > 0 and (i - 2) >= 0) and close[i] > (indvalue[i] + (pointNum * Point()))) and close[i - 2] < indvalue[i]:
            bullArrow = MQLInfoString(MQL_PROGRAM_NAME) + IntegerToString(i)
            bullArrowPrice = low[i] - (arrowDistance * Point())
            if ((EntryValid(open, close, high, low, i, time, rates_total) and greenCandleFormation) and noSidewaysMarket) and significantLiquidity:
                gLongSignal = 1.0
                gShortSignal = 0.0
                if Audio_Alert_On_Signals:
                    if last_playsound_time < time[i]:
                        PlaySound(audioFilePath)
                        last_playsound_time = time[i] - _imod(time[i], PeriodSeconds())
                ObjectCreate(0, bullArrow, OBJ_ARROW, 0, time[i], bullArrowPrice)
                ObjectSetInteger(0, bullArrow, OBJPROP_ARROWCODE, 233)
                ObjectSetInteger(0, bullArrow, OBJPROP_BACK, False)
                ObjectSetInteger(0, bullArrow, OBJPROP_COLOR, LongSignalColor)
                ObjectSetInteger(0, bullArrow, OBJPROP_ANCHOR, ANCHOR_TOP)
                ObjectSetInteger(0, bullArrow, OBJPROP_WIDTH, 2)
        elif ((i > 0 and (i - 2) >= 0) and close[i] < (indvalue[i] - (pointNum * Point()))) and close[i - 2] > indvalue[i]:
            bearArrow = MQLInfoString(MQL_PROGRAM_NAME) + IntegerToString(i)
            bearArrowPrice = high[i] + (arrowDistance * Point())
            if ((EntryValid(open, close, high, low, i, time, rates_total) and redCandleFormation) and noSidewaysMarket) and significantLiquidity:
                gLongSignal = 0.0
                gShortSignal = 1.0
                if Audio_Alert_On_Signals:
                    if last_playsound_time < time[i]:
                        PlaySound(audioFilePath)
                        last_playsound_time = time[i] - _imod(time[i], PeriodSeconds())
                ObjectCreate(0, bearArrow, OBJ_ARROW, 0, time[i], bearArrowPrice)
                ObjectSetInteger(0, bearArrow, OBJPROP_ARROWCODE, 234)
                ObjectSetInteger(0, bearArrow, OBJPROP_BACK, False)
                ObjectSetInteger(0, bearArrow, OBJPROP_COLOR, ShortSignalColor)
                ObjectSetInteger(0, bearArrow, OBJPROP_ANCHOR, ANCHOR_BOTTOM)
                ObjectSetInteger(0, bearArrow, OBJPROP_WIDTH, 2)
    return rates_total

def EntryValid(open, close, high, low, idx, time, bars):
    pointSize = SymbolInfoDouble(Symbol(), SYMBOL_POINT)
    valid = True
    liquidityCheck_a = _fdiv(MathAbs(close[idx - 1] - close[idx - 2]), pointSize)
    liquidityCheck_b = _fdiv(MathAbs(close[idx - 3] - close[idx - 4]), pointSize)
    liquidityCheck_c = _fdiv(MathAbs(open[idx] - close[idx]), pointSize)
    liquidityCheck_d = _fdiv(MathAbs(high[idx] - low[idx]), pointSize)
    liquidityCheck_e = _fdiv(MathAbs(open[idx - 1] - close[idx - 1]), pointSize)
    liquidityCheck_f = _fdiv(MathAbs(high[idx - 1] - low[idx - 1]), pointSize)
    liquidityCheck_g = _fdiv(MathAbs(close[idx - 2] - close[idx - 8]), pointSize)
    if liquidityCheck_d < 25:
        valid = False
    elif liquidityCheck_e < 10:
        if _fdiv(MathAbs(high[idx] - low[idx]), pointSize) > 15:
            valid = True
        else:
            valid = False
    elif liquidityCheck_g < 10:
        valid = False
    return valid

def OnDeinit(reason):
    ObjectsDeleteAll(0, MQLInfoString(MQL_PROGRAM_NAME))
    IndicatorRelease(handle)

# ---- global variables initialised from expressions
audioFilePath = '\\Files\\' + Audio_Alert_Sound
last_playsound_time = TimeCurrent()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MACrossAlerter(_MQL5Indicator):
    name = 'MACrossAlerter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'slowPeriod': 44,  # Moving Average Length
        'Audio_Alert_On_Signals': False,  # Enable audio alerts
        'pointNum': 100,  # Amount of points on MA crossover that should enable a signal
    }

