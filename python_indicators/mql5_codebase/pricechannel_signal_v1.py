"""pricechannel_signal_v1 — converted from MQL5: MQL5 Indicators/PriceChannel Signal/pricechannel_signal_v1.mq5

Copyright: Copyright © 2013, TrendLaboratory; Link: http://finance.groups.yahoo.com/group/TrendLaboratory

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2013, TrendLaboratory', 'link': 'http://finance.groups.yahoo.com/group/TrendLaboratory', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 4}, 'types': {1: 5, 2: 5, 3: 5, 4: 5}, 'colors': {1: [16760576], 2: [17919], 3: [16760576], 4: [17919]}, 'widths': {1: 2, 2: 2, 3: 1, 4: 1}, 'styles': {1: 0, 2: 0, 3: 0, 4: 0}, 'labels': {1: 'UpTrend Signal', 2: 'DnTrend Signal', 3: 'UpTrend Re-Entry', 4: 'DnTrend Re-Entry'}, 'levels': [], 'description': [], 'name': 'pricechannel_signal_v1', 'source': 'MQL5 Indicators/PriceChannel Signal/pricechannel_signal_v1.mq5', 'folder': 'PriceChannel Signal', 'inputs': [{'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'int', 'default': 9, 'label': 'Price Channel Period', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 1, 'label': 'Applied Price', 'sinput': False}, {'mql': 'Risk', 'py': 'Risk', 'param': 'Risk', 'type': 'double', 'default': 3.0, 'label': 'Risk Factor in units (0...10)', 'sinput': False}, {'mql': 'UseReEntry', 'py': 'UseReEntry', 'param': 'UseReEntry', 'type': 'int', 'default': 1, 'label': 'Re-Entry Mode: 0-off,1-on', 'sinput': False}, {'mql': 'AlertMode', 'py': 'AlertMode', 'param': 'AlertMode', 'type': 'int', 'default': 0, 'label': 'Alert Mode: 0-off,1-on', 'sinput': False}, {'mql': 'WarningMode', 'py': 'WarningMode', 'param': 'WarningMode', 'type': 'int', 'default': 0, 'label': 'Warning Mode: 0-off,1-on', 'sinput': False}, {'mql': 'WarningSound', 'py': 'WarningSound', 'param': None, 'type': 'string', 'default': 'tick.wav', 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Length = _input('Length', 9)  # Price Channel Period
Price = _input('Price', PRICE_CLOSE)  # Applied Price
Risk = _input('Risk', 3.0)  # Risk Factor in units (0...10)
UseReEntry = _input('UseReEntry', 1)  # Re-Entry Mode: 0-off,1-on
AlertMode = _input('AlertMode', 0)  # Alert Mode: 0-off,1-on
WarningMode = _input('WarningMode', 0)  # Warning Mode: 0-off,1-on
WarningSound = _input('WarningSound', 'tick.wav')
UpSignal = Arr(0, 0.0)
DnSignal = Arr(0, 0.0)
UpEntry = Arr(0, 0.0)
DnEntry = Arr(0, 0.0)
price = Arr(0, 0.0)
atr = Arr(0, 0.0)
trend = Arr(0, 0.0)
UpBand = Arr(3, 0.0, dyn=False)
LoBand = Arr(3, 0.0, dyn=False)
Price_handle = 0
atr_handle = 0
prevTime = 0
prevAlertTime = 0
UpTrendAlert = False
DownTrendAlert = False

def OnInit():
    global Price_handle, atr_handle
    SetIndexBuffer(0, UpSignal, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_ARROW, 108)
    SetIndexBuffer(1, DnSignal, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_ARROW, 108)
    SetIndexBuffer(2, UpEntry, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_ARROW, 159)
    SetIndexBuffer(3, DnEntry, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_ARROW, 159)
    SetIndexBuffer(4, price, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, atr, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, trend, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'PriceChannel_Signal_v1(' + _str(Length) + ',' + priceToString(Price) + ',' + DoubleToString(Risk, 2) + ',' + _str(UseReEntry) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    begin = MathMax(2, Length)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, begin)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, begin)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, begin)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, begin)
    Price_handle = iMA(None, 0, 1, 0, 0, Price)
    atr_handle = iATR(None, 0, Length)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    global DownTrendAlert, UpTrendAlert, prevAlertTime, prevTime
    shift = 0
    limit = 0
    copied = 0
    up = 0.0
    lo = 0.0
    if prev_calculated == 0:
        limit = Length
        ArrayInitialize(UpSignal, EMPTY_VALUE)
        ArrayInitialize(DnSignal, EMPTY_VALUE)
        ArrayInitialize(UpEntry, EMPTY_VALUE)
        ArrayInitialize(DnEntry, EMPTY_VALUE)
    else:
        limit = rates_total - 1
    copied = CopyBuffer(Price_handle, 0, 0, rates_total - 1, price)
    if copied < 0:
        Print('not all prices copied. Will try on next tick Error =', GetLastError(), ', copied =', copied)
        return 0
    copied = CopyBuffer(atr_handle, 0, 0, rates_total - 1, atr)
    if copied < 0:
        Print('not all ATRs copied. Will try on next tick Error =', GetLastError(), ', copied =', copied)
        return 0
    shift = limit
    for shift in range(shift, rates_total):
        if prevTime != Time[shift]:
            UpBand[2] = UpBand[1]
            UpBand[1] = UpBand[0]
            LoBand[2] = LoBand[1]
            LoBand[1] = LoBand[0]
            prevTime = Time[shift]
        up = 0.0
        lo = 10000000000.0
        for i in range(0, Length):
            up = MathMax(up, High[shift - i])
            lo = MathMin(lo, Low[shift - i])
        UpBand[0] = up - (((33 - Risk) * (up - lo)) / 100)
        LoBand[0] = lo + (((33 - Risk) * (up - lo)) / 100)
        UpSignal[shift] = EMPTY_VALUE
        DnSignal[shift] = EMPTY_VALUE
        UpEntry[shift] = EMPTY_VALUE
        DnEntry[shift] = EMPTY_VALUE
        trend[shift] = trend[shift - 1]
        if price[shift] > UpBand[0]:
            trend[shift] = 1.0
        if price[shift] < LoBand[0]:
            trend[shift] = -1.0
        if trend[shift] > 0:
            if trend[shift - 1] < 0:
                UpSignal[shift] = Low[shift] - (0.5 * atr[shift])
                if WarningMode > 0 and shift == (rates_total - 1):
                    PlaySound(WarningSound)
            elif (UseReEntry > 0 and price[shift] > UpBand[0]) and price[shift - 1] <= UpBand[1]:
                UpEntry[shift] = Low[shift] - (0.5 * atr[shift])
                if WarningMode > 0 and shift == (rates_total - 1):
                    PlaySound(WarningSound)
        elif trend[shift] < 0:
            if trend[shift - 1] > 0:
                DnSignal[shift] = High[shift] + (0.5 * atr[shift])
                if WarningMode > 0 and shift == (rates_total - 1):
                    PlaySound(WarningSound)
            elif (UseReEntry > 0 and price[shift] < LoBand[0]) and price[shift - 1] >= LoBand[1]:
                DnEntry[shift] = High[shift] + (0.5 * atr[shift])
                if WarningMode > 0 and shift == (rates_total - 1):
                    PlaySound(WarningSound)
        message = ''
        if shift == (rates_total - 1) and AlertMode > 0:
            if trend[shift - 1] > 0:
                if trend[shift - 2] < 0 and (not UpTrendAlert):
                    message = ' ' + Symbol() + timeframeToString(Period()) + ': PriceChannel Signal for BUY'
                    Alert(message)
                    UpTrendAlert = True
                    DownTrendAlert = False
                if (((UseReEntry > 0 and trend[shift - 2] > 0) and price[shift - 1] > UpBand[1]) and price[shift - 2] <= UpBand[2]) and Time[shift] != prevAlertTime:
                    message = ' ' + Symbol() + timeframeToString(Period()) + ': PriceChannel Re-Entry for BUY'
                    Alert(message)
                    prevAlertTime = Time[shift]
            elif trend[shift - 1] < 0:
                if trend[shift - 2] > 0 and (not DownTrendAlert):
                    message = ' ' + Symbol() + timeframeToString(Period()) + ': PriceChannel Signal for SELL'
                    Alert(message)
                    DownTrendAlert = True
                    UpTrendAlert = False
                if (((UseReEntry > 0 and trend[shift - 2] < 0) and price[shift - 1] < LoBand[1]) and price[shift - 2] >= LoBand[shift - 2]) and Time[shift] != prevAlertTime:
                    message = ' ' + Symbol() + timeframeToString(Period()) + ': PriceChannel Re-Entry for SELL'
                    Alert(message)
                    prevAlertTime = Time[shift]
    else:
        shift = _range_end(shift, rates_total, 1)
    return rates_total

def priceToString(app_price):
    _sw1 = app_price
    if _sw1 == PRICE_CLOSE:
        return 'Close'
    elif _sw1 == PRICE_HIGH:
        return 'High'
    elif _sw1 == PRICE_LOW:
        return 'Low'
    elif _sw1 == PRICE_MEDIAN:
        return 'Median'
    elif _sw1 == PRICE_OPEN:
        return 'Open'
    elif _sw1 == PRICE_TYPICAL:
        return 'Typical'
    elif _sw1 == PRICE_WEIGHTED:
        return 'Weighted'
    else:
        return ''

def timeframeToString(TF):
    _sw2 = TF
    if _sw2 == PERIOD_CURRENT:
        return 'Current'
    elif _sw2 == PERIOD_M1:
        return 'M1'
    elif _sw2 == PERIOD_M2:
        return 'M2'
    elif _sw2 == PERIOD_M3:
        return 'M3'
    elif _sw2 == PERIOD_M4:
        return 'M4'
    elif _sw2 == PERIOD_M5:
        return 'M5'
    elif _sw2 == PERIOD_M6:
        return 'M6'
    elif _sw2 == PERIOD_M10:
        return 'M10'
    elif _sw2 == PERIOD_M12:
        return 'M12'
    elif _sw2 == PERIOD_M15:
        return 'M15'
    elif _sw2 == PERIOD_M20:
        return 'M20'
    elif _sw2 == PERIOD_M30:
        return 'M30'
    elif _sw2 == PERIOD_H1:
        return 'H1'
    elif _sw2 == PERIOD_H2:
        return 'H2'
    elif _sw2 == PERIOD_H3:
        return 'H3'
    elif _sw2 == PERIOD_H4:
        return 'H4'
    elif _sw2 == PERIOD_H6:
        return 'H6'
    elif _sw2 == PERIOD_H8:
        return 'H8'
    elif _sw2 == PERIOD_H12:
        return 'H12'
    elif _sw2 == PERIOD_D1:
        return 'D1'
    elif _sw2 == PERIOD_W1:
        return 'W1'
    elif _sw2 == PERIOD_MN1:
        return 'MN1'
    else:
        return 'Current'


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PricechannelSignalV1(_MQL5Indicator):
    name = 'pricechannel_signal_v1'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 9,  # Price Channel Period
        'Price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),  # Applied Price
        'Risk': 3.0,  # Risk Factor in units (0...10)
        'UseReEntry': 1,  # Re-Entry Mode: 0-off,1-on
        'AlertMode': 0,  # Alert Mode: 0-off,1-on
        'WarningMode': 0,  # Warning Mode: 0-off,1-on
    }

