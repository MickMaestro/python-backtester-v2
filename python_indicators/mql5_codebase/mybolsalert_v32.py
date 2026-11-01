"""mybolsalert_v32 — converted from MQL5: MQL5 Indicators/MyBOLsAlert/mybolsalert_v32.mq5

Bollinger Bands
------------------------- 2015 SearchSurf's Version 3.2 (RmDj)
Copyright: 2009, MetaQuotes Software Corp.; Link: http://www.mql5.com

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.movingaverages import *  # #include MovingAverages.mqh

MQL5_META = {'props': {'copyright': '2009, MetaQuotes Software Corp.', 'link': 'http://www.mql5.com', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 5}, 'types': {1: 1, 2: 1, 3: 1, 4: 5, 5: 5}, 'colors': {1: [11186720], 2: [11186720], 3: [11186720], 4: [16711680], 5: [255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'Bands middle', 2: 'Bands upper', 3: 'Bands lower'}, 'levels': [], 'description': ['Bollinger Bands', "------------------------- 2015 SearchSurf's Version 3.2 (RmDj)"], 'name': 'mybolsalert_v32', 'source': 'MQL5 Indicators/MyBOLsAlert/mybolsalert_v32.mq5', 'folder': 'MyBOLsAlert', 'inputs': [{'mql': 'InpBandsPeriod', 'py': 'InpBandsPeriod', 'param': 'InpBandsPeriod', 'type': 'int', 'default': 20, 'label': 'Period', 'sinput': False}, {'mql': 'InpBandsShift', 'py': 'InpBandsShift', 'param': 'InpBandsShift', 'type': 'int', 'default': 0, 'label': 'Shift', 'sinput': False}, {'mql': 'InpBandsDeviations', 'py': 'InpBandsDeviations', 'param': 'InpBandsDeviations', 'type': 'double', 'default': 0.5, 'label': 'Deviation', 'sinput': False}, {'mql': 'Play_sound', 'py': 'Play_sound', 'param': 'Play_sound', 'type': 'bool', 'default': True, 'label': 'Enable wav play.', 'sinput': False}, {'mql': 'Emailing', 'py': 'Emailing', 'param': 'Emailing', 'type': 'bool', 'default': False, 'label': 'Enable Email Alert.', 'sinput': False}, {'mql': 'OuterBandArrow', 'py': 'OuterBandArrow', 'param': 'OuterBandArrow', 'type': 'bool', 'default': True, 'label': 'Enable Arrow Indicator', 'sinput': False}, {'mql': 'BandLineOnly', 'py': 'BandLineOnly', 'param': 'BandLineOnly', 'type': 'bool', 'default': False, 'label': 'Arrow on BandLine Only', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['MovingAverages.mqh']}

# ---- inputs and global variables
InpBandsPeriod = _input('InpBandsPeriod', 20)  # Period
InpBandsShift = _input('InpBandsShift', 0)  # Shift
InpBandsDeviations = _input('InpBandsDeviations', 0.5)  # Deviation
Play_sound = _input('Play_sound', True)  # Enable wav play.
Emailing = _input('Emailing', False)  # Enable Email Alert.
OuterBandArrow = _input('OuterBandArrow', True)  # Enable Arrow Indicator
BandLineOnly = _input('BandLineOnly', False)  # Arrow on BandLine Only
ExtBandsPeriod = 0
ExtBandsShift = 0
ExtBandsDeviations = 0.0
ExtPlotBegin = 0
ExtMLBuffer = Arr(0, 0.0)
ExtTLBuffer = Arr(0, 0.0)
ExtBLBuffer = Arr(0, 0.0)
ExtUpBuffer = Arr(0, 0.0)
ExtLoBuffer = Arr(0, 0.0)
ExtStdDevBuffer = Arr(0, 0.0)
UpperBOL = 0.0
LowerBOL = 0.0
MidBOL = 0.0
InSeconds = ""  # The string
sec = Arr(0, "")  # result
usec = 0  # code of seperator
seconds = 0
play = (1 != 0)
delay_sec = 0
mailcon = True  # mail condition  (true = Allow / false = Don't queue);

def OnInit():
    global ExtBandsDeviations, ExtBandsPeriod, ExtBandsShift, ExtPlotBegin
    if InpBandsPeriod < 2:
        ExtBandsPeriod = 20
        printf('Incorrect value for input variable InpBandsPeriod=%d. Indicator will use value=%d for calculations.', InpBandsPeriod, ExtBandsPeriod)
    else:
        ExtBandsPeriod = InpBandsPeriod
    if InpBandsShift < 0:
        ExtBandsShift = 0
        printf('Incorrect value for input variable InpBandsShift=%d. Indicator will use value=%d for calculations.', InpBandsShift, ExtBandsShift)
    else:
        ExtBandsShift = InpBandsShift
    if InpBandsDeviations == 0.0:
        ExtBandsDeviations = 2.0
        printf('Incorrect value for input variable InpBandsDeviations=%f. Indicator will use value=%f for calculations.', InpBandsDeviations, ExtBandsDeviations)
    else:
        ExtBandsDeviations = InpBandsDeviations
    SetIndexBuffer(0, ExtMLBuffer)
    SetIndexBuffer(1, ExtTLBuffer)
    SetIndexBuffer(2, ExtBLBuffer)
    SetIndexBuffer(3, ExtUpBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtLoBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ExtStdDevBuffer, INDICATOR_CALCULATIONS)
    PlotIndexSetString(0, PLOT_LABEL, 'Bands(' + _str(ExtBandsPeriod) + ') Middle')
    PlotIndexSetString(1, PLOT_LABEL, 'Bands(' + _str(ExtBandsPeriod) + ') Upper')
    PlotIndexSetString(2, PLOT_LABEL, 'Bands(' + _str(ExtBandsPeriod) + ') Lower')
    IndicatorSetString(INDICATOR_SHORTNAME, 'Bollinger Bands')
    ExtPlotBegin = ExtBandsPeriod - 1
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtBandsPeriod)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, ExtBandsPeriod)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, ExtBandsPeriod)
    PlotIndexSetInteger(3, PLOT_ARROW, 217)
    PlotIndexSetInteger(4, PLOT_ARROW, 218)
    PlotIndexSetInteger(0, PLOT_SHIFT, ExtBandsShift)
    PlotIndexSetInteger(1, PLOT_SHIFT, ExtBandsShift)
    PlotIndexSetInteger(2, PLOT_SHIFT, ExtBandsShift)
    PlotIndexSetInteger(3, PLOT_ARROW_SHIFT, ExtBandsShift)
    PlotIndexSetInteger(4, PLOT_ARROW_SHIFT, ExtBandsShift)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnDeinit(reason):
    pass

def OnCalculate(rates_total, prev_calculated, begin, price):
    global ExtPlotBegin, InSeconds, LowerBOL, MidBOL, UpperBOL, delay_sec, mailcon, play, seconds, usec
    pos = 0
    i = 0
    Ptrimmed = ""
    the_price = 0.0
    if ExtPlotBegin != (ExtBandsPeriod + begin):
        ExtPlotBegin = ExtBandsPeriod + begin
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, ExtPlotBegin)
        PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, ExtPlotBegin)
        PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, ExtPlotBegin)
    if rates_total < ExtPlotBegin:
        return 0
    if prev_calculated > 1:
        pos = prev_calculated - 1
    else:
        pos = 0
    crates = Arr(0, 0, factory=MqlRates)
    if CopyRates(Symbol(), Period(), 0, rates_total, crates) < 0:
        Alert('Unable to get total rates bars --- ', GetLastError())
        return rates_total
    i = pos
    for i in range(i, rates_total):
        ExtMLBuffer[i] = SimpleMA(i, ExtBandsPeriod, price)
        ExtStdDevBuffer[i] = StdDev_Func(i, price, ExtMLBuffer, ExtBandsPeriod)
        ExtTLBuffer[i] = ExtMLBuffer[i] + (ExtBandsDeviations * ExtStdDevBuffer[i])
        ExtBLBuffer[i] = ExtMLBuffer[i] - (ExtBandsDeviations * ExtStdDevBuffer[i])
        MidBOL = ExtMLBuffer[i]
        LowerBOL = ExtBLBuffer[i]
        UpperBOL = ExtTLBuffer[i]
        ExtUpBuffer[i] = 0.0
        ExtLoBuffer[i] = 0.0
        if OuterBandArrow:
            if BandLineOnly:
                if crates[i].low < UpperBOL and crates[i].high > UpperBOL:
                    ExtUpBuffer[i] = UpperBOL
                else:
                    ExtUpBuffer[i] = 0.0
                if crates[i].high > LowerBOL and crates[i].low < LowerBOL:
                    ExtLoBuffer[i] = LowerBOL
                else:
                    ExtLoBuffer[i] = 0.0
            else:
                if (crates[i].low < UpperBOL and crates[i].high > UpperBOL) or (crates[i].low > UpperBOL and crates[i].high > UpperBOL):
                    ExtUpBuffer[i] = UpperBOL
                else:
                    ExtUpBuffer[i] = 0.0
                if (crates[i].high > LowerBOL and crates[i].low < LowerBOL) or (crates[i].high < LowerBOL and crates[i].low < LowerBOL):
                    ExtLoBuffer[i] = LowerBOL
                else:
                    ExtLoBuffer[i] = 0.0
    else:
        i = _range_end(i, rates_total, 1)
    mrates = Arr(0, 0, factory=MqlRates)
    ArraySetAsSeries(mrates, True)
    if CopyRates(Symbol(), Period(), 0, 3, mrates) < 0:
        Alert('Unable to get rates of 3 bars --- ', GetLastError())
        return rates_total
    if Play_sound:
        InSeconds = TimeToString(TimeLocal(), TIME_SECONDS)
        usec = StringGetCharacter(':', 0)
        StringSplit(InSeconds, usec, sec)
        seconds = StringToInteger(sec[2])
    else:
        seconds = 1
    the_price = mrates[0].close
    if mrates[0].close == MidBOL:
        mailcon = True
    if seconds != delay_sec:
        if ((((((((((seconds == 5 or seconds == 10) or seconds == 15) or seconds == 20) or seconds == 25) or seconds == 30) or seconds == 35) or seconds == 40) or seconds == 45) or seconds == 50) or seconds == 55) or seconds == 0:
            play = True
    delay_sec = seconds
    if mrates[0].close > UpperBOL or mrates[0].close < LowerBOL:
        if mrates[0].close > UpperBOL:
            if Play_sound and play:
                PlaySound('UpperBandAlert.wav')
                play = False
            if mailcon and Emailing:
                mailcon = False
                usec = StringGetCharacter('_', 0)
                StringSplit(EnumToString(Period(), 'ENUM_TIMEFRAMES'), usec, sec)
                Ptrimmed = sec[1]
                if not SendMail(Ptrimmed + 'UpB_' + Symbol(), Ptrimmed + Symbol() + " detected ABOVE Bollinger's Upper Band: " + DoubleToString(the_price, 8) + '  This is an Alert Message.'):
                    Alert('Mail queue failed.')
                    return rates_total
        elif mrates[0].close < LowerBOL:
            if Play_sound and play:
                PlaySound('LowerBandAlert.wav')
                play = False
            if mailcon and Emailing:
                mailcon = False
                usec = StringGetCharacter('_', 0)
                StringSplit(EnumToString(Period(), 'ENUM_TIMEFRAMES'), usec, sec)
                Ptrimmed = sec[1]
                if not SendMail(Ptrimmed + 'LwB_' + Symbol(), Ptrimmed + Symbol() + " detected BELOW Bollinger's Lower Band: " + DoubleToString(the_price, 8) + '  This is an Alert Message.'):
                    Alert('Mail queue failed.')
                    return rates_total
        else:
            pass
    return rates_total

def StdDev_Func(position, price, MAprice, period):
    StdDev_dTmp = 0.0
    if position < period:
        return StdDev_dTmp
    for i in range(0, period):
        StdDev_dTmp += MathPow(price[position - i] - MAprice[position], 2)
    StdDev_dTmp = MathSqrt(_fdiv(StdDev_dTmp, period))
    return StdDev_dTmp


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class MybolsalertV32(_MQL5Indicator):
    name = 'mybolsalert_v32'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'InpBandsPeriod': 20,  # Period
        'InpBandsShift': 0,  # Shift
        'InpBandsDeviations': 0.5,  # Deviation
        'Play_sound': True,  # Enable wav play.
        'Emailing': False,  # Enable Email Alert.
        'OuterBandArrow': True,  # Enable Arrow Indicator
        'BandLineOnly': False,  # Arrow on BandLine Only
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

