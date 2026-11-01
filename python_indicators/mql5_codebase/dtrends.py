"""dTrends — converted from MQL5: MQL5 Indicators/dTrends/dTrends.mq5

Copyright: Copyright 2019, Roberto Jacobs (3rjfx) ~ By 3rjfx ~ Created: 2019/07/29; Link: https://www.mql5.com/en/users/3rjfx; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2019, Roberto Jacobs (3rjfx) ~ By 3rjfx ~ Created: 2019/07/29', 'link': 'https://www.mql5.com/en/users/3rjfx', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 4, 'indicator_plots': 4}, 'types': {1: 0, 2: 0, 3: 5, 4: 5}, 'colors': {3: [16776960], 4: [17919]}, 'widths': {3: 1, 4: 1}, 'styles': {3: 0, 4: 0}, 'labels': {2: 'dTrends', 3: 'Rise', 4: 'Down'}, 'levels': [], 'description': [], 'name': 'dTrends', 'source': 'MQL5 Indicators/dTrends/dTrends.mq5', 'folder': 'dTrends', 'inputs': [{'mql': 'Trend_price', 'py': 'Trend_price', 'param': 'Trend_price', 'type': 'int', 'default': 1, 'label': 'Select Applied Price', 'sinput': False}, {'mql': 'ema_period', 'py': 'ema_period', 'param': 'ema_period', 'type': 'int', 'default': 13, 'label': 'EMA Period', 'sinput': False}, {'mql': 'dist', 'py': 'dist', 'param': 'dist', 'type': 'double', 'default': 2.3, 'label': 'Distance from Zero in pips', 'sinput': False}, {'mql': 'alerts', 'py': 'alerts', 'param': 'alerts', 'type': 'int', 'default': 1, 'label': 'Display Alerts / Messages (Yes) or (No)', 'sinput': False}, {'mql': 'EmailAlert', 'py': 'EmailAlert', 'param': 'EmailAlert', 'type': 'int', 'default': 0, 'label': 'Email Alert (Yes) or (No)', 'sinput': False}, {'mql': 'sendnotify', 'py': 'sendnotify', 'param': 'sendnotify', 'type': 'int', 'default': 0, 'label': 'Send Notification (Yes) or (No)', 'sinput': False}, {'mql': 'displayinfo', 'py': 'displayinfo', 'param': 'displayinfo', 'type': 'int', 'default': 1, 'label': 'Display Trade Info', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum YN
No = 0
Yes = 1
_enum('YN', {0: 'No', 1: 'Yes'})

# enum TimeReturn
year = 0
mon = 1
day = 2
hour = 3
min_ = 4
sec = 5
day_of_week = 6
day_of_year = 7
_enum('TimeReturn', {0: 'year', 1: 'mon', 2: 'day', 3: 'hour', 4: 'min', 5: 'sec', 6: 'day_of_week', 7: 'day_of_year'})

# ---- inputs and global variables
Trend_price = _input('Trend_price', PRICE_CLOSE)  # Select Applied Price
ema_period = _input('ema_period', 13)  # EMA Period
dist = _input('dist', 2.3)  # Distance from Zero in pips
alerts = _input('alerts', Yes)  # Display Alerts / Messages (Yes) or (No)
EmailAlert = _input('EmailAlert', No)  # Email Alert (Yes) or (No)
sendnotify = _input('sendnotify', No)  # Send Notification (Yes) or (No)
displayinfo = _input('displayinfo', Yes)  # Display Trade Info
value1 = Arr(0, 0.0)
value2 = Arr(0, 0.0)
Rise = Arr(0, 0.0)
Down = Arr(0, 0.0)
Bears = Arr(0, 0.0)
Bulls = Arr(0, 0.0)
Temp = Arr(0, 0.0)
cur = 0
prv = 0
cmnt = 0
pmnt = 0
posisi = ""
sigpos = ""
iname = ""
msgText = ""
pip = 0.0
devi = 0.0
EmaHandle = 0

def OnInit():
    global EmaHandle, devi, iname, pip
    SetIndexBuffer(0, value1, INDICATOR_CALCULATIONS)
    SetIndexBuffer(1, value2, INDICATOR_DATA)
    SetIndexBuffer(2, Rise, INDICATOR_DATA)
    SetIndexBuffer(3, Down, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, True)
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, True)
    PlotIndexSetInteger(3, PLOT_SHOW_DATA, True)
    PlotIndexSetInteger(2, PLOT_ARROW, 172)
    PlotIndexSetInteger(3, PLOT_ARROW, 172)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, ema_period)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, ema_period)
    iname = 'dTrends'
    IndicatorSetString(INDICATOR_SHORTNAME, iname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    if Digits() == 3 or Digits() == 5:
        pip = Point() * 10
    elif Digits() == 2 or Digits() == 4:
        pip = Point()
    if StringSubstr(Symbol(), 0, 1) == 'X' or StringSubstr(Symbol(), 0, 1) == '#':
        pip = Point() * 10
    devi = NormalizeDouble(dist * pip, Digits())
    EmaHandle = iMA(None, 0, ema_period, 0, MODE_EMA, Trend_price)
    return INIT_SUCCEEDED

def OnDeinit(reason):
    Comment('')
    ObjectsDeleteAll(ChartID(), 0, -1)
    return

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global cur
    if rates_total < 99:
        return 0
    limit = 0
    calculated = BarsCalculated(EmaHandle)
    if calculated < rates_total:
        return 0
    to_copy = 0
    if prev_calculated > rates_total or prev_calculated < 0:
        to_copy = rates_total
    else:
        to_copy = rates_total - prev_calculated
        if prev_calculated > 0:
            to_copy += 1
    if calculated < rates_total:
        Print('Not all data of EMAHandle is calculated (', calculated, 'bars ). Error', GetLastError())
        return 0
    if False:
        return 0
    if CopyBuffer(EmaHandle, 0, 0, to_copy, Temp) <= 0:
        Print('getting EMAHandle is failed! Error', GetLastError())
        return 0
    if prev_calculated < 99:
        limit = 2
    else:
        limit = prev_calculated - 1
    ArrayResize(value1, limit)
    ArrayResize(value2, limit)
    ArrayResize(Rise, limit)
    ArrayResize(Down, limit)
    ArrayResize(Bears, limit)
    ArrayResize(Bulls, limit)
    ArrayResize(Temp, limit)
    ArraySetAsSeries(value1, True)
    ArraySetAsSeries(value2, True)
    ArraySetAsSeries(Rise, True)
    ArraySetAsSeries(Down, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(Bears, True)
    ArraySetAsSeries(Bulls, True)
    ArraySetAsSeries(Temp, True)
    for i in range(limit - 1, 0 - 1, -1):
        Bears[i] = low[i] - Temp[i]
        Bulls[i] = high[i] - Temp[i]
    for i in range(limit - 2, 0 - 1, -1):
        value1[i] = -(Bears[i] + Bulls[i])
        if value1[i + 1] > 0 and value1[i] < (-devi):
            Rise[i] = low[i]
            Down[i] = EMPTY_VALUE
            cur = 1
        elif value1[i + 1] < 0 and value1[i] > devi:
            Down[i] = high[i]
            Rise[i] = EMPTY_VALUE
            cur = -1
        else:
            Rise[i] = EMPTY_VALUE
            Down[i] = EMPTY_VALUE
        if value1[i] < 0:
            value2[i] = 1.0
        elif value1[i] > 0:
            value2[i] = -1.0
    if (alerts == Yes or EmailAlert == Yes) or sendnotify == Yes:
        Do_Alerts(cur)
    if displayinfo == Yes:
        ChartComm()
    return rates_total

def Do_Alerts(fcur):
    global cmnt, msgText, pmnt, posisi, prv, sigpos
    cmnt = MqlReturnDateTime(TimeCurrent(), min_)
    if cmnt != pmnt:
        if fcur == 1:
            msgText = iname + ' Start to Up'
            posisi = 'Bullish'
            sigpos = 'Open BUY Order'
        elif fcur == -1:
            msgText = iname + ' Start to Down'
            posisi = 'Bearish'
            sigpos = 'Open SELL Order'
        else:
            msgText = iname + ' Trend Not Found!'
            posisi = 'Not Found!'
            sigpos = 'Wait for Confirmation!'
        if fcur != prv:
            Print(iname, '--- ' + Symbol() + ' ' + TF2Str(Period()) + ': ' + msgText + '\n--- at: ', TimeToString(iTime(Symbol(), 0, 0), TIME_DATE | TIME_MINUTES) + ' - ' + sigpos)
            if alerts == Yes:
                Alert(iname, '--- ' + Symbol() + ' ' + TF2Str(Period()) + ': ' + msgText + '--- at: ', TimeToString(iTime(Symbol(), 0, 0), TIME_DATE | TIME_MINUTES) + ' - ' + sigpos)
            if EmailAlert == Yes:
                SendMail(iname, '--- ' + Symbol() + ' ' + TF2Str(Period()) + ': ' + msgText + '\n--- at: ' + TimeToString(iTime(Symbol(), 0, 0), TIME_DATE | TIME_MINUTES) + ' - ' + sigpos)
            if sendnotify == Yes:
                SendNotification(iname + '--- ' + Symbol() + ' ' + TF2Str(Period()) + ': ' + msgText + '\n--- at: ' + TimeToString(iTime(Symbol(), 0, 0), TIME_DATE | TIME_MINUTES) + ' - ' + sigpos)
            prv = fcur
        pmnt = cmnt
    return

def MqlReturnDateTime(reqtime, mode):
    mqltm = MqlDateTime()
    TimeToStruct(reqtime, mqltm)
    valdate = 0
    _sw1 = mode
    if _sw1 == 0:
        valdate = mqltm.year
    elif _sw1 == 1:
        valdate = mqltm.mon
    elif _sw1 == 2:
        valdate = mqltm.day
    elif _sw1 == 3:
        valdate = mqltm.hour
    elif _sw1 == 4:
        valdate = mqltm.min
    elif _sw1 == 5:
        valdate = mqltm.sec
    elif _sw1 == 6:
        valdate = mqltm.day_of_week
    elif _sw1 == 7:
        valdate = mqltm.day_of_year
    return valdate

def TF2Str(period):
    _sw2 = period
    if _sw2 == PERIOD_M1:
        return 'M1'
    elif _sw2 == PERIOD_M5:
        return 'M5'
    elif _sw2 == PERIOD_M15:
        return 'M15'
    elif _sw2 == PERIOD_M30:
        return 'M30'
    elif _sw2 == PERIOD_H1:
        return 'H1'
    elif _sw2 == PERIOD_H4:
        return 'H4'
    elif _sw2 == PERIOD_D1:
        return 'D1'
    elif _sw2 == PERIOD_W1:
        return 'W1'
    elif _sw2 == PERIOD_MN1:
        return 'MN'
    return _str(period)

def AccountMode():
    account_type = AccountInfoInteger(ACCOUNT_TRADE_MODE)
    trade_mode = ""
    _sw3 = account_type
    if _sw3 == ACCOUNT_TRADE_MODE_DEMO:
        trade_mode = 'Demo'
    elif _sw3 == ACCOUNT_TRADE_MODE_CONTEST:
        trade_mode = 'Contest'
    else:
        trade_mode = 'Real'
    return trade_mode

def ChartComm():
    Year = MqlReturnDateTime(TimeCurrent(), year)
    Month = MqlReturnDateTime(TimeCurrent(), mon)
    Day = MqlReturnDateTime(TimeCurrent(), day)
    Comment('\n     :: Server Date Time : ', _str(Year), '.', _str(Month), '.', _str(Day), '   ', TimeToString(TimeCurrent(), TIME_SECONDS), '\n     ------------------------------------------------------------', '\n      :: Broker             :  ', AccountInfoString(ACCOUNT_COMPANY), '\n      :: Acc. Name       :  ', AccountInfoString(ACCOUNT_NAME), '\n      :: Acc, Number    :  ', _str(AccountInfoInteger(ACCOUNT_LOGIN)), '\n      :: Acc,TradeMode :  ', AccountMode(), '\n      :: Acc. Leverage   :  1 : ', _str(AccountInfoInteger(ACCOUNT_LEVERAGE)), '\n      :: Acc. Balance     :  ', DoubleToString(AccountInfoDouble(ACCOUNT_BALANCE), 2), '\n      :: Acc. Equity       :  ', DoubleToString(AccountInfoDouble(ACCOUNT_EQUITY), 2), '\n      --------------------------------------------', '\n      :: Indicator Name  :  ', iname, '\n      :: Currency Pair    :  ', Symbol(), '\n      :: Current Spread  :  ', IntegerToString(SymbolInfoInteger(Symbol(), SYMBOL_SPREAD), 0), '\n      :: Indicator Signal :  ', posisi, '\n      :: Suggested        :  ', sigpos)
    ChartRedraw()
    return


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DTrends(_MQL5Indicator):
    name = 'dTrends'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Trend_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Select Applied Price
        'ema_period': 13,  # EMA Period
        'dist': 2.3,  # Distance from Zero in pips
        'alerts': _Choice({0: 'No', 1: 'Yes'}, default=1),  # Display Alerts / Messages (Yes) or (No)
        'EmailAlert': _Choice({0: 'No', 1: 'Yes'}, default=0),  # Email Alert (Yes) or (No)
        'sendnotify': _Choice({0: 'No', 1: 'Yes'}, default=0),  # Send Notification (Yes) or (No)
        'displayinfo': _Choice({0: 'No', 1: 'Yes'}, default=1),  # Display Trade Info
    }

