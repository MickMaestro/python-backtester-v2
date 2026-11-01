"""Price Alerts 1.01 — converted from MQL5: MQL5 Indicators/Click on the market chart to create a price alert/Price Alerts 1.01.mq5

Copyright: Copyright phade 2024, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright phade 2024, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 5}, 'colors': {1: [15128749]}, 'widths': {}, 'styles': {1: 0}, 'labels': {1: 'PRICE ALERT'}, 'levels': [], 'description': [], 'name': 'Price Alerts 1.01', 'source': 'MQL5 Indicators/Click on the market chart to create a price alert/Price Alerts 1.01.mq5', 'folder': 'Click on the market chart to create a price alert', 'inputs': [{'mql': 'timezone', 'py': 'timezone', 'param': 'timezone', 'type': 'int', 'default': 1, 'label': 'Timezone', 'sinput': False}, {'mql': 'type', 'py': 'type_', 'param': 'type_', 'type': 'int', 'default': 0, 'label': 'Type of alert', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum GMTOffset
GMT_plus_3 = 3
GMT_plus_2 = 2
GMT_plus_1 = 1
GMT = 0
_enum('GMTOffset', {3: 'GMT_plus_3', 2: 'GMT_plus_2', 1: 'GMT_plus_1', 0: 'GMT'})

# enum AlertType
email = 2
mobile = 1
normal = 0
_enum('AlertType', {2: 'email', 1: 'mobile', 0: 'normal'})

# ---- inputs and global variables
timezone = _input('timezone', 1)  # Timezone
type_ = _input('type_', 0)  # Type of alert
isMouseClicked = False
bars = 0
price_buf = Arr(0, 0.0)
completedProcess = 0
aboveMarket = -1

def OnInit():
    global bars
    SetIndexBuffer(0, price_buf, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 214)
    bars = Bars(Symbol(), Period())
    ChartRedraw(0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global aboveMarket, completedProcess
    if rates_total < (bars - 1):
        return 0
    if price_buf[bars - 1] == 0.0:
        price_buf[bars - 1] = EMPTY_VALUE
    if not isMouseClicked:
        if price_buf[bars - 1] > close[rates_total - 1]:
            aboveMarket = 1
        elif price_buf[bars - 1] < close[rates_total - 1]:
            aboveMarket = 0
    if price_buf[bars - 1] != 0.0 and price_buf[bars - 1] != EMPTY_VALUE:
        currentPrice = close[rates_total - 1]
        if (currentPrice > price_buf[bars - 1] and aboveMarket == 1) and completedProcess != 1:
            alertMessage = Symbol() + ': ' + 'Market moved up past the price alert threshold at the price level: ' + DoubleToString(currentPrice, Digits())
            if type_ == 0:
                Alert(alertMessage)
            elif type_ == 1:
                SendNotification(alertMessage)
            elif type_ == 2:
                SendMail('Price Alert for ' + Symbol(), alertMessage)
            completedProcess = 1
        elif (currentPrice < price_buf[bars - 1] and aboveMarket == 0) and completedProcess != 1:
            alertMessage = Symbol() + ': ' + 'Market moved down past the price alert threshold at the level: ' + DoubleToString(currentPrice, Digits())
            if type_ == 0:
                Alert(alertMessage)
            elif type_ == 1:
                SendNotification(alertMessage)
            elif type_ == 2:
                SendMail('Price Alert for ' + Symbol(), alertMessage)
            completedProcess = 1
    return rates_total

def OnChartEvent(id_, lparam, dparam, sparam):
    global completedProcess, isMouseClicked
    if id_ == CHARTEVENT_KEYDOWN:
        if _int(lparam) == 38:
            isMouseClicked = False
            completedProcess = 0
    if id_ == CHARTEVENT_CLICK and (not isMouseClicked):
        currentTime = AdjustTimeForGMT(TimeCurrent(), GMT_plus_1)
        formattedTime = TimeToString(currentTime, (TIME_DATE | TIME_MINUTES) | TIME_SECONDS)
        Print('Created an alert on ' + Symbol() + ' at price: ' + DoubleToString(GetMouseY(dparam)) + ' ' + formattedTime)
        price_buf[bars - 1] = GetMouseY(dparam)
        Comment('ALERT AT PRICE: ', NormalizeDouble(GetMouseY(dparam), 5))
        isMouseClicked = True

def GetMouseY(dparam):
    chartHeightInPixels = ChartGetInteger(0, CHART_HEIGHT_IN_PIXELS)
    priceRange = ChartGetDouble(0, CHART_PRICE_MAX) - ChartGetDouble(0, CHART_PRICE_MIN)
    pixelsPerPrice = _fdiv(chartHeightInPixels, priceRange)
    mouseYValue = ChartGetDouble(0, CHART_PRICE_MAX) - _fdiv(dparam, pixelsPerPrice)
    return mouseYValue

def AdjustTimeForGMT(time, gmt_offset):
    adjusted_time = 0
    _sw1 = gmt_offset
    if _sw1 == 3:
        adjusted_time = time
    elif _sw1 == 2:
        adjusted_time = time - 3600
    elif _sw1 == 1:
        adjusted_time = time - 7200
    elif _sw1 == 0:
        adjusted_time = time - 10800
    else:
        adjusted_time = time
        Print('Invalid GMT offset provided.')
    return adjusted_time

def OnDeinit(reason):
    ChartSetString(0, CHART_COMMENT, '')
    IndicatorRelease(0)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PriceAlerts101(_MQL5Indicator):
    name = 'Price Alerts 1.01'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'timezone': _Choice({3: 'GMT+3', 2: 'GMT+2', 1: 'GMT+1', 0: 'GMT'}, default=1),  # Timezone
        'type_': _Choice({2: 'Email', 1: 'Mobile Notification', 0: 'Basic Alert'}, default=0),  # Type of alert
    }

