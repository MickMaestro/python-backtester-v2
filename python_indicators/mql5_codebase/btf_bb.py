"""BTF_BB — converted from MQL5: MQL5 Indicators/BTF_BB/BTF_BB.mq5

Bigger Time Frame Bollinger Bands
Copyright: Copyright 2018, MetaQuotes Software Corp.; Link: https://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, MetaQuotes Software Corp.', 'link': 'https://mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16748574], 2: [3329330], 3: [16748574]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'BB Top', 2: 'BB Middle', 3: 'BB Bottom'}, 'levels': [], 'description': ['Bigger Time Frame Bollinger Bands'], 'name': 'BTF_BB', 'source': 'MQL5 Indicators/BTF_BB/BTF_BB.mq5', 'folder': 'BTF_BB', 'inputs': [{'mql': 'InpPeriod', 'py': 'InpPeriod', 'param': 'InpPeriod', 'type': 'uint', 'default': 14, 'label': 'BB period', 'sinput': False}, {'mql': 'InpDeviation', 'py': 'InpDeviation', 'param': 'InpDeviation', 'type': 'double', 'default': 2.0, 'label': 'BB deviation', 'sinput': False}, {'mql': 'InpAppliedPrice', 'py': 'InpAppliedPrice', 'param': 'InpAppliedPrice', 'type': 'int', 'default': 1, 'label': 'BB applied price', 'sinput': False}, {'mql': 'InpTimeframe', 'py': 'InpTimeframe', 'param': 'InpTimeframe', 'type': 'int', 'default': 16385, 'label': 'BB timeframe', 'sinput': False}, {'mql': 'InpDrawMode', 'py': 'InpDrawMode', 'param': 'InpDrawMode', 'type': 'int', 'default': 0, 'label': 'Drawing mode', 'sinput': False}, {'mql': 'InpShowMiddle', 'py': 'InpShowMiddle', 'param': 'InpShowMiddle', 'type': 'int', 'default': 1, 'label': 'Show middle lines', 'sinput': False}, {'mql': 'InpUseAlerts', 'py': 'InpUseAlerts', 'param': 'InpUseAlerts', 'type': 'int', 'default': 1, 'label': 'Show alerts', 'sinput': False}, {'mql': 'InpSendMail', 'py': 'InpSendMail', 'param': 'InpSendMail', 'type': 'int', 'default': 0, 'label': 'Send mails', 'sinput': False}, {'mql': 'InpSendPush', 'py': 'InpSendPush', 'param': 'InpSendPush', 'type': 'int', 'default': 1, 'label': 'Send push-notifications', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_DRAW_MODE
DRAW_MODE_STEPS = 0
DRAW_MODE_SLOPE = 1
_enum('ENUM_DRAW_MODE', {0: 'DRAW_MODE_STEPS', 1: 'DRAW_MODE_SLOPE'})

# enum ENUM_INPUT_YES_NO
INPUT_YES = 1
INPUT_NO = 0
_enum('ENUM_INPUT_YES_NO', {1: 'INPUT_YES', 0: 'INPUT_NO'})

# ---- inputs and global variables
InpPeriod = _input('InpPeriod', 14)  # BB period
InpDeviation = _input('InpDeviation', 2.0)  # BB deviation
InpAppliedPrice = _input('InpAppliedPrice', PRICE_CLOSE)  # BB applied price
InpTimeframe = _input('InpTimeframe', PERIOD_H1)  # BB timeframe
InpDrawMode = _input('InpDrawMode', DRAW_MODE_STEPS)  # Drawing mode
InpShowMiddle = _input('InpShowMiddle', INPUT_YES)  # Show middle lines
InpUseAlerts = _input('InpUseAlerts', INPUT_YES)  # Show alerts
InpSendMail = _input('InpSendMail', INPUT_NO)  # Send mails
InpSendPush = _input('InpSendPush', INPUT_YES)  # Send push-notifications
BufferTop = Arr(0, 0.0)
BufferMiddle = Arr(0, 0.0)
BufferBottom = Arr(0, 0.0)
BufferTopBB = Arr(0, 0.0)
BufferMiddleBB = Arr(0, 0.0)
BufferBottomBB = Arr(0, 0.0)
timeframeBB = 0
deviation = 0.0
period = 0
handle_bb = 0

def OnInit():
    global deviation, handle_bb, period, timeframeBB
    EventSetTimer(90)
    period = (1 if (InpPeriod < 1) else InpPeriod)
    deviation = InpDeviation
    timeframeBB = (InpTimeframe if (InpTimeframe > Period()) else Period())
    SetIndexBuffer(0, BufferTop, INDICATOR_DATA)
    SetIndexBuffer(1, BufferMiddle, INDICATOR_DATA)
    SetIndexBuffer(2, BufferBottom, INDICATOR_DATA)
    SetIndexBuffer(3, BufferTopBB, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BufferMiddleBB, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BufferBottomBB, INDICATOR_CALCULATIONS)
    label = TimeframeToString(timeframeBB) + ' Bollinger Bands (' + _str(period) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, label)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    PlotIndexSetString(0, PLOT_LABEL, TimeframeToString(timeframeBB) + ' BB Top(' + _str(period) + ')')
    PlotIndexSetString(1, PLOT_LABEL, TimeframeToString(timeframeBB) + ' BB Middle(' + _str(period) + ')')
    PlotIndexSetString(2, PLOT_LABEL, TimeframeToString(timeframeBB) + ' BB Bottom(' + _str(period) + ')')
    PlotIndexSetInteger(1, PLOT_DRAW_TYPE, InpShowMiddle)
    ArraySetAsSeries(BufferTop, True)
    ArraySetAsSeries(BufferMiddle, True)
    ArraySetAsSeries(BufferBottom, True)
    ArraySetAsSeries(BufferTopBB, True)
    ArraySetAsSeries(BufferMiddleBB, True)
    ArraySetAsSeries(BufferBottomBB, True)
    ResetLastError()
    handle_bb = iBands(None, timeframeBB, period, 0, deviation, InpAppliedPrice)
    if handle_bb == INVALID_HANDLE:
        Print('The ', TimeframeToString(timeframeBB), ' iBands(' + _str(period) + ',' + DoubleToString(deviation, 1) + ') object was not created: Error ', GetLastError())
        return INIT_FAILED
    Time("", timeframeBB, 1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_last_time
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    if rates_total < fmax(period, 4) or Bars(None, timeframeBB) < fmax(period, 4):
        return 0
    limit = rates_total - prev_calculated
    if limit > 1:
        limit = rates_total - 1
        ArrayInitialize(BufferTop, EMPTY_VALUE)
        ArrayInitialize(BufferMiddle, EMPTY_VALUE)
        ArrayInitialize(BufferBottom, EMPTY_VALUE)
        ArrayInitialize(BufferTopBB, 0)
        ArrayInitialize(BufferMiddleBB, 0)
        ArrayInitialize(BufferBottomBB, 0)
    if Time("", timeframeBB, 1) == 0:
        return 0
    bars = (rates_total if (timeframeBB == Period()) else Bars(None, timeframeBB))
    count = (fmin(bars, rates_total) if (limit > 1) else 1)
    copied = 0
    copied = CopyBuffer(handle_bb, UPPER_BAND, 0, count, BufferTopBB)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_bb, BASE_LINE, 0, count, BufferMiddleBB)
    if copied != count:
        return 0
    copied = CopyBuffer(handle_bb, LOWER_BAND, 0, count, BufferBottomBB)
    if copied != count:
        return 0
    for i in range(limit, 0 - 1, -1):
        DataConversion(rates_total, "", timeframeBB, i, BufferTopBB, BufferTop, InpDrawMode)
        DataConversion(rates_total, "", timeframeBB, i, BufferMiddleBB, BufferMiddle, InpDrawMode)
        DataConversion(rates_total, "", timeframeBB, i, BufferBottomBB, BufferBottom, InpDrawMode)
    Alerts = ''
    if time[0] > _s_OnCalculate_last_time and (close[0] > BufferTop[0] or (close[0] < BufferBottom[0] and BufferBottom[0] != EMPTY_VALUE)):
        pos = ('above the Upper' if (close[0] > BufferTop[0]) else 'below the Lower')
        message = Symbol() + ', ' + TimeframeToString(Period()) + ': Price is ' + pos + ' ' + TimeframeToString(timeframeBB) + ' Bollinger Band'
        if InpUseAlerts:
            Alert(message)
        if InpSendMail and TerminalInfoInteger(TERMINAL_EMAIL_ENABLED):
            SendMail('Bigger Time Frame Bollinger Bands Signal', message)
        if InpSendPush and TerminalInfoInteger(TERMINAL_NOTIFICATIONS_ENABLED):
            SendNotification(message)
        _s_OnCalculate_last_time = TimeCurrent()
    return rates_total

def OnTimer():
    Time("", timeframeBB, 1)

def DataConversion(rates_total, symbol_name, timeframe_src, shift, buffer_src, buffer_dest, mode=DRAW_MODE_STEPS):
    if timeframe_src == Period():
        buffer_dest[shift] = buffer_src[shift]
        return
    bar_curr = BarToCurrent(symbol_name, timeframe_src, shift)
    if bar_curr > (rates_total - 1):
        return
    bar_prev = BarToCurrent(symbol_name, timeframe_src, shift + 1)
    bar_next = (BarToCurrent(symbol_name, timeframe_src, shift - 1) if (shift > 0) else 0)
    if (bar_prev == WRONG_VALUE or bar_curr == WRONG_VALUE) or bar_next == WRONG_VALUE:
        return
    buffer_dest[bar_curr] = buffer_src[shift]
    if mode == DRAW_MODE_STEPS:
        for j in range(bar_curr, bar_next - 1, -1):
            buffer_dest[j] = buffer_dest[bar_curr]
    else:
        if bar_prev > (rates_total - 1):
            return
        for j in range(bar_prev, bar_curr - 1, -1):
            buffer_dest[j] = EquationDirect(bar_prev, buffer_dest[bar_prev], bar_curr, buffer_dest[bar_curr], j)
        if shift == 0:
            for j in range(bar_curr, 0 - 1, -1):
                buffer_dest[j] = buffer_dest[bar_curr]

def BarToCurrent(symbol_name, timeframe_src, shift, exact=False):
    time = Time(symbol_name, timeframe_src, shift)
    return (BarShift(symbol_name, Period(), time, exact) if (time != 0) else WRONG_VALUE)

def BarShift(symbol_name, timeframe, time, exact=False):
    res = Bars(symbol_name, timeframe, time + 1, UINT_MAX)
    if exact:
        if (timeframe != PERIOD_MN1 or time > TimeCurrent()) and res == Bars(symbol_name, timeframe, time - PeriodSeconds(timeframe) + 1, UINT_MAX):
            return WRONG_VALUE
    return res

def Time(symbol_name, timeframe, shift):
    array = Arr(0, 0)
    ArraySetAsSeries(array, True)
    return (array[0] if (CopyTime(symbol_name, timeframe, shift, 1, array) == 1) else 0)

def EquationDirect(left_bar, left_price, right_bar, right_price, bar_to_search):
    return (left_price if (right_bar == left_bar) else ((_fdiv(right_price - left_price, right_bar - left_bar) * (bar_to_search - left_bar)) + left_price))

def TimeframeToString(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7)

# ---- static local variables
_s_OnCalculate_last_time = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class BTFBB(_MQL5Indicator):
    name = 'BTF_BB'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpPeriod': 14,  # BB period
        'InpDeviation': 2.0,  # BB deviation
        'InpAppliedPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # BB applied price
        'InpTimeframe': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16385),  # BB timeframe
        'InpDrawMode': _Choice({0: 'Steps', 1: 'Slope'}, default=0),  # Drawing mode
        'InpShowMiddle': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show middle lines
        'InpUseAlerts': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Show alerts
        'InpSendMail': _Choice({1: 'Yes', 0: 'No'}, default=0),  # Send mails
        'InpSendPush': _Choice({1: 'Yes', 0: 'No'}, default=1),  # Send push-notifications
    }

