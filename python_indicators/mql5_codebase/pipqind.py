"""PIPQind — converted from MQL5: MQL5 Indicators/PIPQind/PIPQind.mq5

Copyright: Copyright © 2005, emsjoflo; Link: automaticforec.invisionzone.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, emsjoflo', 'link': 'automaticforec.invisionzone.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 11, 4: 1}, 'colors': {1: [65280], 2: [255], 3: [16748574, 4678655], 4: [8519755]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'Buy PIPQind signal', 2: 'Sell PIPQind signal', 3: 'PIPQind Histogram', 4: 'PIPQind Line'}, 'levels': [], 'description': [], 'name': 'PIPQind', 'source': 'MQL5 Indicators/PIPQind/PIPQind.mq5', 'folder': 'PIPQind', 'inputs': [{'mql': 'nPips', 'py': 'nPips', 'param': 'nPips', 'type': 'double', 'default': 65.0, 'label': '', 'sinput': False}, {'mql': 'SendAlert', 'py': 'SendAlert', 'param': 'SendAlert', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'SendEmail', 'py': 'SendEmail', 'param': 'SendEmail', 'type': 'bool', 'default': False, 'label': '', 'sinput': False}, {'mql': 'AlertMinutesB4close', 'py': 'AlertMinutesB4close', 'param': 'AlertMinutesB4close', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'AlertEveryNMinutes', 'py': 'AlertEveryNMinutes', 'param': 'AlertEveryNMinutes', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'ATRmultiplier', 'py': 'ATRmultiplier', 'param': 'ATRmultiplier', 'type': 'double', 'default': 0.45, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
nPips = _input('nPips', 65.0)
SendAlert = _input('SendAlert', False)
SendEmail = _input('SendEmail', False)
AlertMinutesB4close = _input('AlertMinutesB4close', 5)
AlertEveryNMinutes = _input('AlertEveryNMinutes', 10)
ATRmultiplier = _input('ATRmultiplier', 0.45)
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
UpArrow = Arr(0, 0.0)
DownArrow = Arr(0, 0.0)
BlueBar = Arr(0, 0.0)
RedBar = Arr(0, 0.0)
ColorBar = Arr(0, 0.0)
TrStopDots = Arr(0, 0.0)
min_rates_total = 0
ATR_Handle = 0

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Period = 14
    min_rates_total = ATR_Period + 3
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    shortname = Box("")
    StringConcatenate(shortname, 'PIPQind(', _str(nPips), ', ', _str(Shift), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, UpArrow, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(0, PLOT_ARROW, 234)
    ArraySetAsSeries(UpArrow, True)
    SetIndexBuffer(1, DownArrow, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_ARROW, 233)
    ArraySetAsSeries(DownArrow, True)
    SetIndexBuffer(2, BlueBar, INDICATOR_DATA)
    ArraySetAsSeries(BlueBar, True)
    SetIndexBuffer(3, RedBar, INDICATOR_DATA)
    ArraySetAsSeries(RedBar, True)
    SetIndexBuffer(4, ColorBar, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorBar, True)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)
    SetIndexBuffer(5, TrStopDots, INDICATOR_DATA)
    ArraySetAsSeries(TrStopDots, True)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0.0)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectsDeleteAll(0, 'PIPQind_', -1, -1)
    Comment('')
    ChartRedraw(None)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_PREV
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    i = 0
    ATR = Arr(0, 0.0)
    alertsent = 0
    MinutesB4Barcloses = ""
    cnt = 0.0
    stop = 0.0
    atr = 0.0
    atrstop = 0.0
    TrStopLevel = 0.0
    name = ""
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(spread, True)
    ArraySetAsSeries(ATR, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_PREV = close[limit]
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        UpArrow[bar] = 0.0
        DownArrow[bar] = 0.0
        BlueBar[bar] = 0.0
        RedBar[bar] = 0.0
        if close[bar] == _s_OnCalculate_PREV:
            TrStopLevel = _s_OnCalculate_PREV
        else:
            if close[bar + 1] <= _s_OnCalculate_PREV and close[bar] < _s_OnCalculate_PREV:
                TrStopLevel = MathMin(_s_OnCalculate_PREV, close[bar] + (nPips * Point()))
            else:
                if close[bar + 1] >= _s_OnCalculate_PREV and close[bar] > _s_OnCalculate_PREV:
                    TrStopLevel = MathMax(_s_OnCalculate_PREV, close[bar] - (nPips * Point()))
                else:
                    if close[bar] > _s_OnCalculate_PREV:
                        TrStopLevel = close[bar] - (nPips * Point())
                    else:
                        TrStopLevel = close[bar] + (nPips * Point())
        TrStopDots[bar] = TrStopLevel
        if UpArrow[bar] and UpArrow[bar] != TrStopDots[bar]:
            UpArrow[bar] = 0.0
        if DownArrow[bar] != TrStopDots[bar]:
            DownArrow[bar] = 0.0
        if (close[bar] > TrStopLevel and (close[bar + 1] < _s_OnCalculate_PREV or (close[bar + 1] <= TrStopDots[bar + 1] and close[bar + 2] < TrStopDots[bar + 2]))) and _s_OnCalculate_PREV:
            atr = ATR[bar]
            stop = low[ArrayMinimum(low, bar, 3)]
            atrstop = NormalizeDouble(TrStopLevel - (atr * ATRmultiplier), Digits())
            if atrstop > stop:
                stop = atrstop
            name = 'PIPQind_' + TimeToString(time[bar], TIME_MINUTES)
            SetTline(0, name, 0, time[bar + 2], stop, time[bar], stop, clrDodgerBlue, 0, 2, DoubleToString(stop, Digits()))
            Comment(stop)
            Bid = close[bar]
            Ask = Bid + (Point() * spread[bar])
            if ((Bid > TrStopDots[0] and close[1] <= TrStopDots[1]) and (TimeCurrent() - time[0]) >= (time[0] - time[1] - (AlertMinutesB4close * 60))) and (TimeCurrent() - alertsent) > (AlertEveryNMinutes * 60):
                MinutesB4Barcloses = TimeToString(time[0] - time[1] - (TimeCurrent() - time[0]), TIME_MINUTES)
                if SendAlert:
                    Alert('Look for Buying opportunity soon')
                if SendEmail:
                    SendMail('Possible Buy setup on ' + Symbol(), 'PIPQind anticpates a Buy signal on ' + Symbol() + ' in ' + MinutesB4Barcloses + ' minutes' + ' at ' + TimeToString(TimeCurrent()) + ' Bid: ' + DoubleToString(Bid, Digits()) + ' Ask: ' + DoubleToString(Ask, Digits()) + ' close[0]:' + DoubleToString(close[0], Digits()) + 'close[1]: ' + DoubleToString(close[1], Digits()) + ' TrStopDots[1]: ' + DoubleToString(TrStopDots[1], Digits()) + ' PREV: ' + DoubleToString(_s_OnCalculate_PREV, Digits()) + ' TrStopLevel: ' + DoubleToString(TrStopLevel, Digits()) + ' TrStopDots[0]: ' + DoubleToString(TrStopDots[0], Digits()))
                alertsent = TimeCurrent()
            RedBar[bar] = low[bar]
            BlueBar[bar] = high[bar]
            ColorBar[bar] = 0.0
            UpArrow[bar] = TrStopLevel
        if (close[bar] < TrStopLevel and (close[bar + 1] > _s_OnCalculate_PREV or (close[bar + 1] >= TrStopDots[bar + 1] and close[bar + 2] >= TrStopDots[bar + 2]))) and _s_OnCalculate_PREV:
            atr = ATR[bar]
            stop = high[ArrayMaximum(high, bar, 3)]
            atrstop = NormalizeDouble(TrStopLevel + (atr * ATRmultiplier), Digits())
            if atrstop < stop:
                stop = atrstop
            name = 'PIPQind_' + TimeToString(time[bar], TIME_MINUTES)
            SetTline(0, name, 0, time[bar + 2], stop, time[bar], stop, clrRed, 0, 2, DoubleToString(stop, Digits()))
            Comment(stop)
            Bid = close[bar]
            Ask = Bid + (Point() * spread[bar])
            if ((Ask < TrStopDots[0] and close[1] >= TrStopDots[1]) and (TimeCurrent() - time[0]) >= (time[0] - time[1] - (AlertMinutesB4close * 60))) and (TimeCurrent() - alertsent) > (AlertEveryNMinutes * 60):
                MinutesB4Barcloses = TimeToString(time[0] - time[1] - (TimeCurrent() - time[0]), TIME_MINUTES)
                if SendAlert:
                    Alert('Look for Selling opportunity soon')
                if SendEmail:
                    SendMail('Possible Sell setup on ' + Symbol(), 'PIPQind anticipates a sell signal on ' + Symbol() + ' in ' + MinutesB4Barcloses + ' minutes ' + ' at ' + TimeToString(TimeCurrent()) + ' Bid: ' + DoubleToString(Bid, Digits()) + ' Ask: ' + DoubleToString(Ask, Digits()) + ' close[0]:' + DoubleToString(close[0], Digits()) + 'close[1]: ' + DoubleToString(close[1], Digits()) + ' TrStopDots[1]: ' + DoubleToString(TrStopDots[1], Digits()) + ' PREV: ' + DoubleToString(_s_OnCalculate_PREV, Digits()) + ' TrStopLevel: ' + DoubleToString(TrStopLevel, Digits()) + ' TrStopDots[0]: ' + DoubleToString(TrStopDots[0], Digits()))
                alertsent = TimeCurrent()
            BlueBar[bar] = high[bar]
            RedBar[bar] = low[bar]
            ColorBar[bar] = 1.0
            DownArrow[bar] = TrStopLevel
        if bar:
            _s_OnCalculate_PREV = TrStopLevel
    else:
        bar = _range_end(bar, 0 - 1, -1)
    i = 1
    if UpArrow[i] > 0 and UpArrow[i] < TrStopDots[i]:
        UpArrow[i] = 0.0
    if DownArrow[i] > TrStopDots[i]:
        DownArrow[i] = 0.0
    ChartRedraw(None)
    return rates_total

def CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    ObjectCreate(chart_id, name, OBJ_TREND, nwin, time1, price1, time2, price2)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, False)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY_RIGHT, False)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY, False)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(chart_id, name, OBJPROP_ZORDER, True)

def SetTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text):
    if ObjectFind(chart_id, name) == -1:
        CreateTline(chart_id, name, nwin, time1, price1, time2, price2, Color, style, width, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, time1, price1)
        ObjectMove(chart_id, name, 1, time2, price2)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)

# ---- static local variables
_s_OnCalculate_PREV = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PIPQind(_MQL5Indicator):
    name = 'PIPQind'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'nPips': 65.0,
        'SendAlert': False,
        'SendEmail': False,
        'AlertMinutesB4close': 5,
        'AlertEveryNMinutes': 10,
        'ATRmultiplier': 0.45,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
    }

