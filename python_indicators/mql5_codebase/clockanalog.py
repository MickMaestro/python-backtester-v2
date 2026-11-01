"""clockanalog — converted from MQL5: MQL5 Indicators/ClockAnalog/clockanalog.mq5

Copyright: Copyright 2014, MetaQuotes Software Corp.; Link: http://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.clockanalog_cstockclock import *  # #include CStockClock.mqh
from backtester.mql5.lib.clockanalog_stockclockenums import *  # #include StockClockEnums.mqh
from backtester.mql5.lib.clockanalog_cgtrendline import *  # #include CGTrendLine.mqh
from backtester.mql5.lib.clockanalog_cgraphbase import *  # #include CGraphBase.mqh
from backtester.mql5.lib.clockanalog_cgbitmaplabel import *  # #include CGBitmapLabel.mqh
from backtester.mql5.lib.clockanalog_cglabel import *  # #include CGLabel.mqh
from backtester.mql5.lib.clockanalog_cgbutton import *  # #include CGButton.mqh

MQL5_META = {'props': {'copyright': 'Copyright 2014, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'clockanalog', 'source': 'MQL5 Indicators/ClockAnalog/clockanalog.mq5', 'folder': 'ClockAnalog', 'inputs': [{'mql': 'comment0', 'py': 'comment0', 'param': None, 'type': 'string', 'default': 'Position', 'label': '', 'sinput': False}, {'mql': 'TopLeft', 'py': 'TopLeft', 'param': 'TopLeft', 'type': 'int', 'default': 10, 'label': 'Left position', 'sinput': False}, {'mql': 'TopHigh', 'py': 'TopHigh', 'param': 'TopHigh', 'type': 'int', 'default': 15, 'label': 'Top position', 'sinput': False}, {'mql': 'comment1', 'py': 'comment1', 'param': None, 'type': 'string', 'default': 'Colors and style', 'label': '', 'sinput': False}, {'mql': 'IptScheme', 'py': 'IptScheme', 'param': 'IptScheme', 'type': 'int', 'default': 0, 'label': 'Color scheme', 'sinput': False}, {'mql': 'IptBlack', 'py': 'IptBlack', 'param': None, 'type': 'color', 'default': 3145645, 'label': 'Second hand color in black scheme', 'sinput': False}, {'mql': 'IptWhite', 'py': 'IptWhite', 'param': None, 'type': 'color', 'default': 36095, 'label': 'Second hand color in white scheme', 'sinput': False}, {'mql': 'IptSecStyle', 'py': 'IptSecStyle', 'param': 'IptSecStyle', 'type': 'int', 'default': 0, 'label': 'Second hand style', 'sinput': False}, {'mql': 'ShowSecond', 'py': 'ShowSecond', 'param': 'ShowSecond', 'type': 'bool', 'default': True, 'label': 'Show second hand', 'sinput': False}, {'mql': 'comment2', 'py': 'comment2', 'param': None, 'type': 'string', 'default': 'Demo-mode', 'label': '', 'sinput': False}, {'mql': 'year', 'py': 'year', 'param': 'year', 'type': 'int', 'default': 0, 'label': 'Year to show', 'sinput': False}, {'mql': 'month', 'py': 'month', 'param': 'month', 'type': 'int', 'default': 0, 'label': 'Month to show', 'sinput': False}, {'mql': 'day', 'py': 'day', 'param': 'day', 'type': 'int', 'default': 0, 'label': 'Day to show', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['CStockClock.mqh', 'StockClockEnums.mqh', 'CGTrendLine.mqh', 'CGraphBase.mqh', 'CGBitmapLabel.mqh', 'CGLabel.mqh', 'CGButton.mqh']}

# ---- inputs and global variables
comment0 = _input('comment0', 'Position')
TopLeft = _input('TopLeft', 10)  # Left position
TopHigh = _input('TopHigh', 15)  # Top position
comment1 = _input('comment1', 'Colors and style')
IptScheme = _input('IptScheme', black)  # Color scheme
IptBlack = _input('IptBlack', clrGreenYellow)  # Second hand color in black scheme
IptWhite = _input('IptWhite', clrDarkOrange)  # Second hand color in white scheme
IptSecStyle = _input('IptSecStyle', STYLE_SOLID)  # Second hand style
ShowSecond = _input('ShowSecond', True)  # Show second hand
comment2 = _input('comment2', 'Demo-mode')
year = _input('year', 0)  # Year to show
month = _input('month', 0)  # Month to show
day = _input('day', 0)  # Day to show
clock = None
timer = True

def OnInit():
    global clock, timer
    ResetLastError()
    if not EventSetTimer(1):
        Print('OnInit', ' Error setting timer. Code: ', GetLastError())
        timer = False
    else:
        timer = True
        clock = CStockClock(TopLeft, TopHigh, 'ClockAnalog', ShowSecond, IptScheme)
        if year > 0:
            clock.SetDebugDate(year, month, day)
        clock.DefaultsSkin()
        clock.SetExtSecond(IptBlack, IptWhite, IptSecStyle)
        clock.DefaultsSecond()
        clock.HandSecondMove()
        clock.DefaultsHours()
        clock.HandHourMove()
        clock.DefaultsMinute()
        clock.HandMinuteMove()
        clock.DefaultsHeader()
        clock.DefaultsHeaderLabel()
        clock.DefaultsMove()
        clock.DefaultsBack()
        clock.DefaultsHide()
        ChartRedraw(0)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    EventKillTimer()
    if timer:
        _delete(clock)
    DeleteAll()

def OnCalculate(rates_total, prev_calculated, begin, price):
    return rates_total

def OnTimer():
    clock.ProcessingDstEvent()
    clock.HandHourMove()
    clock.HandMinuteMove()
    clock.HandSecondMove()
    ChartRedraw(0)

def OnChartEvent(id_, lparam, dparam, sparam):
    if not clock.ClockHidden():
        clock.EventBack(id_, lparam, dparam, sparam)
    if not clock.ClockHidden():
        clock.EventMove(id_, lparam, dparam, sparam)
    clock.EventHide(id_, lparam, dparam, sparam)
    if clock.ClockHidden():
        clock.SetBackOn()
        clock.SetMoveOff()
    ChartRedraw(0)

def DeleteAll():
    obj_name = ''
    obj_total = ObjectsTotal(0, 0, -1)
    for i in range(obj_total - 1, 0 - 1, -1):
        obj_name = ObjectName(0, i, 0, -1)
        if StringFind(obj_name, 'Clock', 0) == 0:
            ObjectDelete(0, obj_name)
    ChartRedraw()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Clockanalog(_MQL5Indicator):
    name = 'clockanalog'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TopLeft': 10,  # Left position
        'TopHigh': 15,  # Top position
        'IptScheme': _Choice({0: 'black', 1: 'white'}, default=0),  # Color scheme
        'IptSecStyle': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Second hand style
        'ShowSecond': True,  # Show second hand
        'year': 0,  # Year to show
        'month': 0,  # Month to show
        'day': 0,  # Day to show
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

