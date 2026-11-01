"""slopedirectionline — converted from MQL5: MQL5 Indicators/SlopeDirectionLine/slopedirectionline.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [9639167, 8421504, 13828244]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'SlopeDirectionLine'}, 'levels': [], 'description': [], 'name': 'slopedirectionline', 'source': 'MQL5 Indicators/SlopeDirectionLine/slopedirectionline.mq5', 'folder': 'SlopeDirectionLine', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 3, 'label': 'First smoothing method', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'uint', 'default': 12, 'label': 'First smoothing depth', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'First smoothing parameter', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 0, 'label': 'Second smoothing averaging method', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 15, 'label': 'Second smoothing parameter', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Price constant', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Vertical shift of the indicator in pointsх', 'sinput': False}, {'mql': 'On_Push', 'py': 'On_Push', 'param': 'On_Push', 'type': 'bool', 'default': False, 'label': 'Allow to send push-messages', 'sinput': False}, {'mql': 'On_Email', 'py': 'On_Email', 'param': 'On_Email', 'type': 'bool', 'default': False, 'label': 'Allow to send e-mail messages', 'sinput': False}, {'mql': 'On_Alert', 'py': 'On_Alert', 'param': 'On_Alert', 'type': 'bool', 'default': True, 'label': 'Allow to put alert', 'sinput': False}, {'mql': 'On_Play_Sound', 'py': 'On_Play_Sound', 'param': 'On_Play_Sound', 'type': 'bool', 'default': False, 'label': 'Allow to put sound signal', 'sinput': False}, {'mql': 'NameFileSound', 'py': 'NameFileSound', 'param': None, 'type': 'string', 'default': 'expert.wav', 'label': 'Name of the file with sound', 'sinput': False}, {'mql': 'CommentSirName', 'py': 'CommentSirName', 'param': None, 'type': 'string', 'default': 'SlopeDirectionLine: ', 'label': 'The first part of the allert comment', 'sinput': False}, {'mql': 'SignalBar', 'py': 'SignalBar', 'param': 'SignalBar', 'type': 'uint', 'default': 1, 'label': 'Bar index for getting an entry signal', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_'})

# ---- inputs and global variables
MA_Method1 = _input('MA_Method1', MODE_LWMA)  # First smoothing method
Length1 = _input('Length1', 12)  # First smoothing depth
Phase1 = _input('Phase1', 15)  # First smoothing parameter
MA_Method2 = _input('MA_Method2', MODE_SMA)  # Second smoothing averaging method
Phase2 = _input('Phase2', 15)  # Second smoothing parameter
IPC = _input('IPC', PRICE_CLOSE)  # Price constant
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
PriceShift = _input('PriceShift', 0)  # Vertical shift of the indicator in pointsх
On_Push = _input('On_Push', False)  # Allow to send push-messages
On_Email = _input('On_Email', False)  # Allow to send e-mail messages
On_Alert = _input('On_Alert', True)  # Allow to put alert
On_Play_Sound = _input('On_Play_Sound', False)  # Allow to put sound signal
NameFileSound = _input('NameFileSound', 'expert.wav')  # Name of the file with sound
CommentSirName = _input('CommentSirName', 'SlopeDirectionLine: ')  # The first part of the allert comment
SignalBar = _input('SignalBar', 1)  # Bar index for getting an entry signal
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
LengthX = 0
LengthR = 0
dPriceShift = 0.0
min_rates_total = 0
min_rates_ = 0

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def OnInit():
    global LengthR, LengthX, dPriceShift, min_rates_, min_rates_total
    LengthX = _int(_idiv(Length1, 2))
    LengthR = _int(MathMax(MathSqrt(Length1), 1))
    min_rates_ = XMA1.GetStartBars(MA_Method1, Length1, Phase1)
    min_rates_total = min_rates_ + XMA1.GetStartBars(MA_Method2, LengthR, Phase2)
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetString(0, PLOT_LABEL, 'IndBuffer')
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    shortname = Box("")
    Smooth2 = XMA1.GetString_MA_Method(MA_Method2)
    StringConcatenate(shortname, 'SlopeDirectionLine(', Length1, ', ', LengthR, ', ', Smooth2, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    price = 0.0
    line = 0.0
    xline = 0.0
    first = 0
    bar = 0
    clr = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        line = XMA1.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, price, bar, False)
        line = (2 * XMA2.XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, LengthX, price, bar, False)) - line
        xline = XMA3.XMASeries(min_rates_, prev_calculated, rates_total, MA_Method2, Phase2, LengthR, line, bar, False)
        IndBuffer[bar] = xline + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total - 1
    bar = first
    for bar in range(bar, rates_total):
        clr = 1
        ColorIndBuffer[bar] = 1.0
        if IndBuffer[bar - 1] < IndBuffer[bar]:
            clr = 2
        if IndBuffer[bar - 1] > IndBuffer[bar]:
            clr = 0
        ColorIndBuffer[bar] = clr
        if bar == (rates_total - 1 - SignalBar):
            if ColorIndBuffer[bar - 1] != 2 and clr == 2:
                SignalTime = TimeCurrent()
                if On_Play_Sound:
                    PlaySound(NameFileSound)
                period = GetStringTimeframe(Period())
                comment = Box("")
                sTime = ' CurrTime=' + TimeToString(SignalTime, TIME_MINUTES)
                StringConcatenate(comment, CommentSirName, Symbol(), period, ' ', sTime, ' Buy signal!')
                if On_Alert:
                    Alert(comment.v)
                if On_Push:
                    SendNotification(comment.v)
                if On_Email:
                    SendMail(CommentSirName + Symbol() + period, comment.v)
            if ColorIndBuffer[bar - 1] != 0 and clr == 0:
                SignalTime = TimeCurrent()
                if On_Play_Sound:
                    PlaySound(NameFileSound)
                period = GetStringTimeframe(Period())
                comment = Box("")
                sTime = ' CurrTime=' + TimeToString(SignalTime, TIME_MINUTES)
                StringConcatenate(comment, CommentSirName, Symbol(), period, ' ', sTime, ' Sell signal!')
                if On_Alert:
                    Alert(comment.v)
                if On_Push:
                    SendNotification(comment.v)
                if On_Email:
                    SendMail(CommentSirName + Symbol() + period, comment.v)
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()
XMA2 = _alloc(CXMA)
XMA2.__init__()
XMA3 = _alloc(CXMA)
XMA3.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Slopedirectionline(_MQL5Indicator):
    name = 'slopedirectionline'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=3),  # First smoothing method
        'Length1': 12,  # First smoothing depth
        'Phase1': 15,  # First smoothing parameter
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # Second smoothing averaging method
        'Phase2': 15,  # Second smoothing parameter
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price'}, default=1),  # Price constant
        'Shift': 0,  # Horizontal shift of the indicator in bars
        'PriceShift': 0,  # Vertical shift of the indicator in pointsх
        'On_Push': False,  # Allow to send push-messages
        'On_Email': False,  # Allow to send e-mail messages
        'On_Alert': True,  # Allow to put alert
        'On_Play_Sound': False,  # Allow to put sound signal
        'SignalBar': 1,  # Bar index for getting an entry signal
    }

