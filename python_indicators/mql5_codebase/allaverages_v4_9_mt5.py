"""AllAverages_v4.9_MT5 — converted from MQL5: MQL5 Indicators/AllAverages v4.9 MT5/AllAverages_v4.9_MT5.mq5

Copyright: Copyright © 2019, TrendLaboratory; Link: http://newdigital-world.com/forum.php

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2019, TrendLaboratory', 'link': 'http://newdigital-world.com/forum.php', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 8}, 'colors': {1: [65535, 16760576, 17919]}, 'widths': {1: 2}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'AllAverages_v4.9_MT5', 'source': 'MQL5 Indicators/AllAverages v4.9 MT5/AllAverages_v4.9_MT5.mq5', 'folder': 'AllAverages v4.9 MT5', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 0, 'label': 'Timeframe', 'sinput': False}, {'mql': 'Price', 'py': 'Price', 'param': 'Price', 'type': 'int', 'default': 0, 'label': 'Apply To', 'sinput': False}, {'mql': 'MA_Period', 'py': 'MA_Period', 'param': 'MA_Period', 'type': 'int', 'default': 14, 'label': 'Period', 'sinput': False}, {'mql': 'MA_Shift', 'py': 'MA_Shift', 'param': 'MA_Shift', 'type': 'int', 'default': 0, 'label': 'Shift', 'sinput': False}, {'mql': 'MA_Method', 'py': 'MA_Method', 'param': 'MA_Method', 'type': 'int', 'default': 0, 'label': 'Method', 'sinput': False}, {'mql': 'ShowInColor', 'py': 'ShowInColor', 'param': 'ShowInColor', 'type': 'bool', 'default': True, 'label': 'Show In Color', 'sinput': False}, {'mql': 'CountBars', 'py': 'CountBars', 'param': 'CountBars', 'type': 'int', 'default': 0, 'label': 'Number of bars counted: 0-all bars', 'sinput': False}, {'mql': 'Alerts', 'py': 'Alerts', 'param': None, 'type': 'string', 'default': '=== Alerts, Emails & Notifications ===', 'label': '', 'sinput': False}, {'mql': 'AlertOn', 'py': 'AlertOn', 'param': 'AlertOn', 'type': 'bool', 'default': False, 'label': 'Alert On', 'sinput': False}, {'mql': 'AlertShift', 'py': 'AlertShift', 'param': 'AlertShift', 'type': 'int', 'default': 1, 'label': 'Alert Shift:0-current bar,1-previous bar', 'sinput': False}, {'mql': 'SoundsNumber', 'py': 'SoundsNumber', 'param': 'SoundsNumber', 'type': 'int', 'default': 5, 'label': 'Number of sounds after Signal', 'sinput': False}, {'mql': 'SoundsPause', 'py': 'SoundsPause', 'param': 'SoundsPause', 'type': 'int', 'default': 5, 'label': 'Pause in sec between sounds', 'sinput': False}, {'mql': 'UpTrendSound', 'py': 'UpTrendSound', 'param': None, 'type': 'string', 'default': 'alert.wav', 'label': 'UpTrend Sound', 'sinput': False}, {'mql': 'DnTrendSound', 'py': 'DnTrendSound', 'param': None, 'type': 'string', 'default': 'alert2.wav', 'label': 'DownTrend Sound', 'sinput': False}, {'mql': 'EmailOn', 'py': 'EmailOn', 'param': 'EmailOn', 'type': 'bool', 'default': False, 'label': 'Email Alert On', 'sinput': False}, {'mql': 'EmailsNumber', 'py': 'EmailsNumber', 'param': 'EmailsNumber', 'type': 'int', 'default': 1, 'label': 'Emails Number', 'sinput': False}, {'mql': 'PushNotificationOn', 'py': 'PushNotificationOn', 'param': 'PushNotificationOn', 'type': 'bool', 'default': False, 'label': 'Push Notification On', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

MQL5_PROGRAM_NAME = 0  # MQL5 constant unknown to the converter

# enum ENUM_PRICE
close = 0
open = 1
high = 2
low = 3
median = 4
typical = 5
weightedClose = 6
medianBody = 7
average = 8
trendBiased = 9
trendBiasedExt = 10
haClose = 11
haOpen = 12
haHigh = 13
haLow = 14
haMedian = 15
haTypical = 16
haWeighted = 17
haMedianBody = 18
haAverage = 19
haTrendBiased = 20
haTrendBiasedExt = 21
_enum('ENUM_PRICE', {0: 'close', 1: 'open', 2: 'high', 3: 'low', 4: 'median', 5: 'typical', 6: 'weightedClose', 7: 'medianBody', 8: 'average', 9: 'trendBiased', 10: 'trendBiasedExt', 11: 'haClose', 12: 'haOpen', 13: 'haHigh', 14: 'haLow', 15: 'haMedian', 16: 'haTypical', 17: 'haWeighted', 18: 'haMedianBody', 19: 'haAverage', 20: 'haTrendBiased', 21: 'haTrendBiasedExt'})

# enum ENUM_MA_MODE
SMA = 0
EMA = 1
Wilder = 2
LWMA = 3
SineWMA = 4
TriMA = 5
LSMA = 6
SMMA = 7
HMA = 8
ZeroLagEMA = 9
DEMA = 10
T3_basic = 11
ITrend = 12
Median = 13
GeoMean = 14
REMA = 15
ILRS = 16
IE_2 = 17
TriMAgen = 18
VWMA = 19
JSmooth = 20
SMA_eq = 21
ALMA = 22
TEMA = 23
T3 = 24
Laguerre = 25
MD = 26
BF2P = 27
BF3P = 28
SuperSmu = 29
Decycler = 30
eVWMA = 31
EWMA = 32
DsEMA = 33
TsEMA = 34
VEMA = 35
_enum('ENUM_MA_MODE', {0: 'SMA', 1: 'EMA', 2: 'Wilder', 3: 'LWMA', 4: 'SineWMA', 5: 'TriMA', 6: 'LSMA', 7: 'SMMA', 8: 'HMA', 9: 'ZeroLagEMA', 10: 'DEMA', 11: 'T3_basic', 12: 'ITrend', 13: 'Median', 14: 'GeoMean', 15: 'REMA', 16: 'ILRS', 17: 'IE_2', 18: 'TriMAgen', 19: 'VWMA', 20: 'JSmooth', 21: 'SMA_eq', 22: 'ALMA', 23: 'TEMA', 24: 'T3', 25: 'Laguerre', 26: 'MD', 27: 'BF2P', 28: 'BF3P', 29: 'SuperSmu', 30: 'Decycler', 31: 'eVWMA', 32: 'EWMA', 33: 'DsEMA', 34: 'TsEMA', 35: 'VEMA'})

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', 0)  # Timeframe
Price = _input('Price', 0)  # Apply To
MA_Period = _input('MA_Period', 14)  # Period
MA_Shift = _input('MA_Shift', 0)  # Shift
MA_Method = _input('MA_Method', SMA)  # Method
ShowInColor = _input('ShowInColor', True)  # Show In Color
CountBars = _input('CountBars', 0)  # Number of bars counted: 0-all bars
Alerts = _input('Alerts', '=== Alerts, Emails & Notifications ===')
AlertOn = _input('AlertOn', False)  # Alert On
AlertShift = _input('AlertShift', 1)  # Alert Shift:0-current bar,1-previous bar
SoundsNumber = _input('SoundsNumber', 5)  # Number of sounds after Signal
SoundsPause = _input('SoundsPause', 5)  # Pause in sec between sounds
UpTrendSound = _input('UpTrendSound', 'alert.wav')  # UpTrend Sound
DnTrendSound = _input('DnTrendSound', 'alert2.wav')  # DownTrend Sound
EmailOn = _input('EmailOn', False)  # Email Alert On
EmailsNumber = _input('EmailsNumber', 1)  # Emails Number
PushNotificationOn = _input('PushNotificationOn', False)  # Push Notification On
moving = Arr(0, 0.0)
trend = Arr(0, 0.0)
iprice = Arr(0, 0.0)
tf = 0
mtf_handle = 0
draw_begin = 0
masize = 0
cBars = 0
ma_period = 0
TF = ""
IndicatorName = ""
short_name = ""
maname = ""
mtf_moving = Arr(1, 0.0, dyn=False)
mtf_trend = Arr(1, 0.0, dyn=False)
tmp = Arr(0, 0.0, dims=(1, 2,))
ma = Arr(1, 0.0, dyn=False, dims=(4,))
prevbar = Arr(1, 0, dyn=False)
prevhabar = Arr(1, 0, dyn=False)
haClose = Arr(1, 0.0, dyn=False, dims=(2,))
haOpen = Arr(1, 0.0, dyn=False, dims=(2,))
haHigh = Arr(1, 0.0, dyn=False, dims=(2,))
haLow = Arr(1, 0.0, dyn=False, dims=(2,))
prevnbtime = 0
prevmess = ""
pausetime = 0
warningtime = 0
prevemail = ""
prevpush = ""

def OnInit():
    global IndicatorName, TF, ma_period, maname, masize, mtf_handle, short_name, tf
    if TimeFrame <= Period():
        tf = Period()
    else:
        tf = TimeFrame
    TF = timeframeToString(tf)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    SetIndexBuffer(0, moving, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_COLOR_INDEXES, 3)
    SetIndexBuffer(1, trend, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(2, iprice, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_SHIFT, _idiv(MA_Shift * PeriodSeconds(tf), PeriodSeconds(Period())))
    PlotIndexSetInteger(1, PLOT_SHIFT, _idiv(MA_Shift * PeriodSeconds(tf), PeriodSeconds(Period())))
    maname = EnumToString(MA_Method, 'ENUM_MA_MODE')
    masize = averageSize(MA_Method)
    IndicatorName = MQLInfoString(_int(MQL5_PROGRAM_NAME))
    short_name = IndicatorName + '[' + TF + '](' + EnumToString(Price, 'ENUM_PRICE') + ',' + _str(MA_Period) + ',' + maname + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    if MA_Method == EWMA:
        ma_period = 5 * MA_Period
    else:
        ma_period = MA_Period
    if MA_Method == HMA:
        ma_period += _int(MathSqrt(MA_Period))
    ArrayResize(tmp, masize)
    if TimeFrame > 0 and tf > Period():
        mtf_handle = iCustom(Symbol(), tf, IndicatorName, tf, Price, MA_Period, 0, MA_Method, ShowInColor, CountBars, '', AlertOn, AlertShift, SoundsNumber, SoundsPause, UpTrendSound, DnTrendSound, EmailOn, EmailsNumber, PushNotificationOn)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    global cBars
    x = 0
    y = 0
    shift = 0
    limit = 0
    mtflimit = 0
    copied = 0
    mtf_time = 0
    if prev_calculated == 0:
        if CountBars == 0:
            cBars = rates_total - ma_period
        else:
            cBars = _idiv(CountBars * PeriodSeconds(tf), PeriodSeconds(Period()))
        limit = rates_total - cBars - ma_period
        mtflimit = rates_total - 1
        ArrayInitialize(moving, EMPTY_VALUE)
        ArrayInitialize(trend, 0)
    else:
        limit = rates_total - 1
        mtflimit = _idiv(PeriodSeconds(tf), PeriodSeconds(Period())) + 1
    if tf > Period():
        ArraySetAsSeries(Time, True)
        shift = 0
        y = 0
        while shift < mtflimit:
            if Time[shift] < iTime(None, TimeFrame, y):
                y += 1
            mtf_time = iTime(None, TimeFrame, y)
            copied = CopyBuffer(mtf_handle, 0, _DT(mtf_time), _DT(mtf_time), mtf_moving)
            if copied <= 0:
                return 0
            x = rates_total - shift - 1
            moving[x] = mtf_moving[0]
            if ShowInColor:
                copied = CopyBuffer(mtf_handle, 1, _DT(mtf_time), _DT(mtf_time), mtf_trend)
                if copied <= 0:
                    return 0
                trend[x] = mtf_trend[0]
            else:
                trend[x] = 0.0
            shift += 1
        PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, rates_total - cBars)
    else:
        shift = limit
        for shift in range(shift, rates_total):
            if Price <= 10:
                iprice[shift] = getPrice(Price, Close[shift], Open[shift], High[shift], Low[shift], shift)
            elif Price > 10 and Price <= 21:
                iprice[shift] = HeikenAshi(0, Price - 11, Close[shift], Open[shift], High[shift], Low[shift], rates_total - cBars - ma_period, shift)
            startbar = rates_total - cBars
            if shift < (startbar - ma_period + 1):
                continue
            moving[shift] = allAveragesOnArray(0, iprice, MA_Period, MA_Method, masize, startbar, rates_total, shift)
            if shift > 0:
                if ShowInColor and moving[shift - 1] != EMPTY_VALUE:
                    trend[shift] = trend[shift - 1]
                    if moving[shift] > moving[shift - 1]:
                        trend[shift] = 1.0
                    if moving[shift] < moving[shift - 1]:
                        trend[shift] = 2.0
                else:
                    trend[shift] = 0.0
        else:
            shift = _range_end(shift, rates_total, 1)
    if (AlertOn or EmailOn) or PushNotificationOn:
        alertbar = rates_total - 1 - AlertShift
        uptrend = trend[alertbar] == 1 and trend[alertbar - 1] == 2
        dntrend = trend[alertbar] == 2 and trend[alertbar - 1] == 1
        if uptrend or dntrend:
            if isNewBar(tf):
                if AlertOn:
                    BoxAlert(uptrend, ' : ' + maname + '(' + _str(MA_Period) + ') is going Up @ ' + DoubleToString(Close[alertbar], Digits()))
                    BoxAlert(dntrend, ' : ' + maname + '(' + _str(MA_Period) + ') is going Down @ ' + DoubleToString(Close[alertbar], Digits()))
                if EmailOn:
                    EmailAlert(uptrend, 'BUY', ' : ' + maname + '(' + _str(MA_Period) + ') is going Up @ ' + DoubleToString(Close[alertbar], Digits()), EmailsNumber)
                    EmailAlert(dntrend, 'SELL', ' : ' + maname + '(' + _str(MA_Period) + ') is going Down @ ' + DoubleToString(Close[alertbar], Digits()), EmailsNumber)
                if PushNotificationOn:
                    PushAlert(uptrend, ' : ' + maname + '(' + _str(MA_Period) + ') is going Up @ ' + DoubleToString(Close[alertbar], Digits()))
                    PushAlert(dntrend, ' : ' + maname + '(' + _str(MA_Period) + ') is going Down @ ' + DoubleToString(Close[alertbar], Digits()))
            else:
                if AlertOn:
                    WarningSound(uptrend, SoundsNumber, SoundsPause, UpTrendSound, Time[alertbar])
                    WarningSound(dntrend, SoundsNumber, SoundsPause, DnTrendSound, Time[alertbar])
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, rates_total - cBars)
    return rates_total

def averageSize(mode):
    arraysize = 0
    _sw1 = mode
    if _sw1 == DEMA:
        arraysize = 2
    elif _sw1 == T3_basic:
        arraysize = 6
    elif _sw1 == JSmooth:
        arraysize = 5
    elif _sw1 == TEMA:
        arraysize = 4
    elif _sw1 == T3:
        arraysize = 6
    elif _sw1 == Laguerre:
        arraysize = 4
    elif _sw1 == DsEMA:
        arraysize = 2
    elif _sw1 == TsEMA:
        arraysize = 3
    elif _sw1 == VEMA:
        arraysize = 2
    else:
        arraysize = 0
    return arraysize

def allAveragesOnArray(index, price, period, mode, arraysize, cbars, rates, bar):
    i = 0
    if period == 1:
        return price[bar]
    MA = Arr(4, 0.0, dyn=False)
    _sw2 = mode
    if _sw2 in (EMA, Wilder, SMMA, ZeroLagEMA, DEMA, T3_basic, ITrend, REMA, JSmooth, SMA_eq, TEMA, T3, Laguerre, MD, BF2P, BF3P, SuperSmu, Decycler, eVWMA, DsEMA, TsEMA, VEMA):
        if prevbar[index] != bar:
            ma[index][3] = ma[index][2]
            ma[index][2] = ma[index][1]
            ma[index][1] = ma[index][0]
            if arraysize > 0:
                i = 0
                for i in range(i, arraysize):
                    tmp[i][index][1] = tmp[i][index][0]
                else:
                    i = _range_end(i, arraysize, 1)
            prevbar[index] = bar
        if ((mode == ITrend or mode == REMA) or mode == SMA_eq) or (mode >= BF2P and mode < eVWMA):
            i = 0
            for i in range(i, 4):
                MA[i] = ma[index][i]
            else:
                i = _range_end(i, 4, 1)
    _sw3 = mode
    if _sw3 == EMA:
        ma[index][0] = EMAOnArray(price[bar], ma[index][1], period, cbars, bar)
    elif _sw3 == Wilder:
        ma[index][0] = WilderOnArray(price[bar], ma[index][1], period, cbars, bar)
    elif _sw3 == LWMA:
        ma[index][0] = LWMAOnArray(0, price, period, bar)
    elif _sw3 == SineWMA:
        ma[index][0] = SineWMAOnArray(price, period, bar)
    elif _sw3 == TriMA:
        ma[index][0] = TriMAOnArray(price, period, bar)
    elif _sw3 == LSMA:
        ma[index][0] = LSMAOnArray(price, period, bar)
    elif _sw3 == SMMA:
        ma[index][0] = SMMAOnArray(price, ma[index][1], period, cbars, bar)
    elif _sw3 == HMA:
        ma[index][0] = HMAOnArray(price, period, cbars, bar)
    elif _sw3 == ZeroLagEMA:
        ma[index][0] = ZeroLagEMAOnArray(price, ma[index][1], period, cbars, bar)
    elif _sw3 == DEMA:
        ma[index][0] = DEMAOnArray(index, 0, price[bar], period, 1.0, cbars, bar)
    elif _sw3 == T3_basic:
        ma[index][0] = T3_basicOnArray(index, 0, price[bar], period, 0.7, cbars, bar)
    elif _sw3 == ITrend:
        ma[index][0] = ITrendOnArray(price, MA, period, cbars, bar)
    elif _sw3 == Median:
        ma[index][0] = MedianOnArray(price, period, cbars, bar)
    elif _sw3 == GeoMean:
        ma[index][0] = GeoMeanOnArray(price, period, cbars, bar)
    elif _sw3 == REMA:
        ma[index][0] = REMAOnArray(price[bar], MA, period, 0.5, cbars, bar)
    elif _sw3 == ILRS:
        ma[index][0] = ILRSOnArray(price, period, cbars, bar)
    elif _sw3 == IE_2:
        ma[index][0] = IE2OnArray(price, period, cbars, bar)
    elif _sw3 == TriMAgen:
        ma[index][0] = TriMA_genOnArray(0, price, period, cbars, bar)
    elif _sw3 == VWMA:
        ma[index][0] = VWMAOnArray(price, period, rates, bar)
    elif _sw3 == JSmooth:
        ma[index][0] = JSmoothOnArray(index, 0, price[bar], period, 1.0, cbars, bar)
    elif _sw3 == SMA_eq:
        ma[index][0] = SMA_eqOnArray(price, MA, period, cbars, bar)
    elif _sw3 == ALMA:
        ma[index][0] = ALMAOnArray(price, period, 0.85, 8.0, bar)
    elif _sw3 == TEMA:
        ma[index][0] = TEMAOnArray(index, price[bar], period, 1.0, cbars, bar)
    elif _sw3 == T3:
        ma[index][0] = T3OnArray(index, 0, price[bar], period, 0.7, cbars, bar)
    elif _sw3 == Laguerre:
        ma[index][0] = LaguerreOnArray(index, price[bar], period, 4, cbars, bar)
    elif _sw3 == MD:
        ma[index][0] = McGinleyOnArray(price[bar], ma[index][1], period, cbars, bar)
    elif _sw3 == BF2P:
        ma[index][0] = BF2POnArray(price, MA, period, cbars, bar)
    elif _sw3 == BF3P:
        ma[index][0] = BF3POnArray(price, MA, period, cbars, bar)
    elif _sw3 == SuperSmu:
        ma[index][0] = SuperSmuOnArray(price, MA, period, cbars, bar)
    elif _sw3 == Decycler:
        ma[index][0] = DecyclerOnArray(price, MA, period, cbars, bar)
        return price[bar] - ma[index][0]
    elif _sw3 == eVWMA:
        ma[index][0] = eVWMAOnArray(price[bar], ma[index][1], period, cbars, rates, bar)
    elif _sw3 == EWMA:
        ma[index][0] = EWMAOnArray(price, period, bar)
    elif _sw3 == DsEMA:
        ma[index][0] = DsEMAOnArray(index, price[bar], period, cbars, bar)
    elif _sw3 == TsEMA:
        ma[index][0] = TsEMAOnArray(index, price[bar], period, cbars, bar)
    elif _sw3 == VEMA:
        ma[index][0] = VEMAOnArray(index, price[bar], period, cbars, rates, bar)
    else:
        ma[index][0] = SMAOnArray(0, price, period, bar)
    return ma[index][0]

def SMAOnArray(mode, array, per, bar):
    sum_ = 0.0
    if mode == 0:
        if bar >= per:
            for i in range(0, per):
                sum_ += array[bar - i]
    else:
        for i in range(0, per):
            sum_ += array[bar + i]
    return _fdiv(sum_, per)

def EMAOnArray(price, prev, per, cbars, bar):
    ema = 0.0
    if bar < cbars:
        ema = price
    else:
        ema = prev + (_fdiv(2.0, 1 + per) * (price - prev))
    return ema

def WilderOnArray(price, prev, per, cbars, bar):
    wilder = 0.0
    if bar < cbars:
        wilder = price
    else:
        wilder = prev + _fdiv(price - prev, per)
    return wilder

def LWMAOnArray(mode, array, per, bar):
    lwma = EMPTY_VALUE
    sum_ = 0.0
    weight = 0.0
    if mode == 0:
        if bar > per:
            for i in range(0, per):
                weight += per - i
                sum_ += array[bar - i] * (per - i)
    else:
        for i in range(0, per):
            weight += per - i
            sum_ += array[i] * (per - i)
    if weight > 0:
        lwma = _fdiv(sum_, weight)
    else:
        lwma = 0.0
    return lwma

def SineWMAOnArray(array, per, bar):
    swma = EMPTY_VALUE
    sum_ = 0.0
    weight = 0.0
    if bar > per:
        for i in range(0, per):
            weight += MathSin(_fdiv(3.141592653589793 * (i + 1), per + 1))
            sum_ += array[bar - i] * MathSin(_fdiv(3.141592653589793 * (i + 1), per + 1))
        if weight > 0:
            swma = _fdiv(sum_, weight)
        else:
            swma = 0.0
    return swma

def TriMAOnArray(array, per, bar):
    len_ = _int(MathCeil((per + 1) * 0.5))
    trima = EMPTY_VALUE
    sma = 0.0
    sum_ = 0.0
    if bar > per:
        for i in range(0, len_):
            sma = SMAOnArray(0, array, len_, bar - i)
            sum_ += sma
        trima = _fdiv(sum_, len_)
    return trima

def LSMAOnArray(array, per, bar):
    lsma = EMPTY_VALUE
    sum_ = 0.0
    if bar > per:
        for i in range(per, 1 - 1, -1):
            sum_ += (i - ((per + 1) / 3.0)) * array[bar - (per - i)]
        lsma = _fdiv(sum_ * 6, per * (per + 1))
    return lsma

def SMMAOnArray(array, prev, per, cbars, bar):
    smma = EMPTY_VALUE
    if bar == cbars:
        smma = SMAOnArray(0, array, per, bar)
    elif bar > cbars:
        sum_ = 0.0
        for i in range(0, per):
            sum_ += array[bar - (i + 1)]
        smma = _fdiv(sum_ - prev + array[bar], per)
    return smma

def HMAOnArray(array, per, cbars, bar):
    hma = EMPTY_VALUE
    tmparray = Arr(0, 0.0)
    i = 0
    len_ = _int(MathSqrt(per))
    ArrayResize(tmparray, len_)
    if bar == cbars:
        hma = array[bar]
    elif bar > cbars:
        i = 0
        for i in range(i, len_):
            tmparray[i] = (2 * LWMAOnArray(0, array, _idiv(per, 2), bar - i)) - LWMAOnArray(0, array, per, bar - i)
        else:
            i = _range_end(i, len_, 1)
        hma = LWMAOnArray(1, tmparray, len_, 0)
    return hma

def ZeroLagEMAOnArray(price, prev, per, cbars, bar):
    zema = EMPTY_VALUE
    alpha = _fdiv(2.0, 1 + per)
    lag = 0.5 * (per - 1)
    if bar == cbars:
        zema = price[bar]
    elif bar > cbars:
        zema = (alpha * ((2 * price[bar]) - price[bar - _int(lag)])) + ((1 - alpha) * prev)
    return zema

def DEMAOnArray(index, num, price, per, v, cbars, bar):
    dema = EMPTY_VALUE
    alpha = _fdiv(2.0, 1 + per)
    if bar == cbars:
        dema = price
        tmp[num][index][0] = dema
        tmp[num + 1][index][0] = dema
    elif bar > cbars:
        tmp[num][index][0] = tmp[num][index][1] + (alpha * (price - tmp[num][index][1]))
        tmp[num + 1][index][0] = tmp[num + 1][index][1] + (alpha * (tmp[num][index][0] - tmp[num + 1][index][1]))
        dema = (tmp[num][index][0] * (1 + v)) - (tmp[num + 1][index][0] * v)
    return dema

def T3_basicOnArray(index, num, price, per, v, cbars, bar):
    T3_ = EMPTY_VALUE
    dema1 = 0.0
    dema2 = 0.0
    if bar == cbars:
        T3_ = price
        for k in range(0, 6):
            tmp[num + k][index][0] = T3_
    elif bar > cbars:
        dema1 = DEMAOnArray(index, num, price, per, v, cbars, bar)
        dema2 = DEMAOnArray(index, num + 2, dema1, per, v, cbars, bar)
        T3_ = DEMAOnArray(index, num + 4, dema2, per, v, cbars, bar)
    return T3_

def ITrendOnArray(price, array, per, cbars, bar):
    it = EMPTY_VALUE
    alpha = _fdiv(2.0, per + 1)
    if (bar > cbars and array[1] != EMPTY_VALUE) and array[2] != EMPTY_VALUE:
        it = ((alpha - (0.25 * alpha * alpha)) * price[bar]) + (0.5 * alpha * alpha * price[bar - 1]) - ((alpha - (0.75 * alpha * alpha)) * price[bar - 2]) + (2 * (1 - alpha) * array[1]) - ((1 - alpha) * (1 - alpha) * array[2])
    elif bar <= cbars and bar > 2:
        it = (price[bar] + (2 * price[bar - 1]) + price[bar - 2]) / 4
    return it

def MedianOnArray(price, per, cbars, bar):
    median_ = EMPTY_VALUE
    array = Arr(0, 0.0)
    ArrayResize(array, per)
    if bar >= cbars:
        for i in range(0, per):
            array[i] = price[bar - i]
        ArraySort(array)
        num = MathRound(0.5 * (per - 1))
        if MathMod(per, 2) > 0:
            median_ = array[_int(num)]
        else:
            median_ = 0.5 * (array[_int(num)] + array[_int(num) + 1])
    return median_

def GeoMeanOnArray(price, per, cbars, bar):
    gmean = EMPTY_VALUE
    if bar > cbars:
        gmean = MathPow(price[bar], _fdiv(1.0, per))
        for i in range(1, per):
            gmean *= MathPow(price[bar - i], _fdiv(1.0, per))
    elif bar == cbars:
        gmean = SMAOnArray(0, price, per, bar)
    return gmean

def REMAOnArray(price, array, per, lambda_, cbars, bar):
    rema = EMPTY_VALUE
    alpha = _fdiv(2.0, per + 1)
    if bar > cbars:
        rema = _fdiv((array[1] * (1 + (2 * lambda_))) + (alpha * (price - array[1])) - (lambda_ * array[2]), 1 + lambda_)
    else:
        rema = price
    return rema

def ILRSOnArray(price, per, cbars, bar):
    ilrs = EMPTY_VALUE
    slope = 0.0
    sum_ = per * (per - 1) * 0.5
    sum2 = ((per - 1) * per * ((2 * per) - 1)) / 6.0
    sum1 = 0.0
    sumy = 0.0
    if bar >= cbars:
        for i in range(0, per):
            sum1 += i * price[bar - i]
            sumy += price[bar - i]
        num1 = (per * sum1) - (sum_ * sumy)
        num2 = (sum_ * sum_) - (per * sum2)
        if num2 != 0:
            slope = _fdiv(num1, num2)
        else:
            slope = 0.0
        ilrs = slope + SMAOnArray(0, price, per, bar)
    return ilrs

def IE2OnArray(price, per, cbars, bar):
    ie = EMPTY_VALUE
    if bar >= cbars:
        ie = 0.5 * (ILRSOnArray(price, per, cbars, bar) + LSMAOnArray(price, per, bar))
    return ie

def TriMA_genOnArray(mode, array, per, cbars, bar):
    len1 = _int(MathFloor((per + 1) * 0.5))
    len2 = _int(MathCeil((per + 1) * 0.5))
    trimagen = EMPTY_VALUE
    sum_ = 0.0
    if mode == 0:
        if bar > per:
            for i in range(0, len2):
                sum_ += SMAOnArray(0, array, len1, bar - i)
    else:
        for i in range(0, len2):
            sum_ += SMAOnArray(1, array, len1, i)
    trimagen = _fdiv(sum_, len2)
    return trimagen

def VWMAOnArray(array, per, rates, bar):
    vwma = EMPTY_VALUE
    Sum = 0.0
    Weight = 0.0
    volume = Arr(0, 0)
    ArraySetAsSeries(volume, True)
    volumes = CopyTickVolume(Symbol(), 0, rates - 1 - bar, per, volume)
    if volumes < 0:
        return EMPTY_VALUE
    if bar > per:
        for i in range(0, per):
            Weight += float(volume[i])
            Sum += array[bar - i] * volume[i]
        if Weight > 0:
            vwma = _fdiv(Sum, Weight)
        else:
            vwma = 0.0
    return vwma

def JSmoothOnArray(index, num, price, per, pow_, cbars, bar):
    beta = _fdiv(0.45 * (per - 1), (0.45 * (per - 1)) + 2)
    alpha = MathPow(beta, pow_)
    if bar == cbars:
        tmp[num + 4][index][0] = price
        tmp[num + 0][index][0] = price
        tmp[num + 1][index][0] = 0.0
        tmp[num + 2][index][0] = price
        tmp[num + 3][index][0] = 0.0
    elif bar > cbars:
        tmp[num + 0][index][0] = ((1 - alpha) * price) + (alpha * tmp[num + 0][index][1])
        tmp[num + 1][index][0] = ((price - tmp[num + 0][index][0]) * (1 - beta)) + (beta * tmp[num + 1][index][1])
        tmp[num + 2][index][0] = tmp[num + 0][index][0] + tmp[num + 1][index][0]
        tmp[num + 3][index][0] = ((tmp[num + 2][index][0] - tmp[num + 4][index][1]) * MathPow(1 - alpha, 2)) + (MathPow(alpha, 2) * tmp[num + 3][index][1])
        tmp[num + 4][index][0] = tmp[num + 4][index][1] + tmp[num + 3][index][0]
    return tmp[num + 4][index][0]

def SMA_eqOnArray(price, array, per, cbars, bar):
    sma = EMPTY_VALUE
    if bar == cbars:
        sma = SMAOnArray(0, price, per, bar)
    elif bar > cbars:
        sma = _fdiv(price[bar] - price[bar - per], per) + array[1]
    return sma

def ALMAOnArray(array, per, offset, sigma, bar):
    alma = EMPTY_VALUE
    m = MathFloor(offset * (per - 1))
    s = _fdiv(per, sigma)
    w = 0.0
    sum_ = 0.0
    wsum = 0.0
    if bar > per:
        for i in range(0, per):
            w = MathExp(_fdiv(-((i - m) * (i - m)), 2 * s * s))
            wsum += w
            sum_ += array[bar - (per - 1 - i)] * w
        if wsum != 0:
            alma = _fdiv(sum_, wsum)
    return alma

def TEMAOnArray(index, price, per, v, cbars, bar):
    alpha = _fdiv(2.0, per + 1)
    if bar == cbars:
        for k in range(0, 4):
            tmp[k][index][0] = price
    elif bar > cbars:
        tmp[0][index][0] = tmp[0][index][1] + (alpha * (price - tmp[0][index][1]))
        tmp[1][index][0] = tmp[1][index][1] + (alpha * (tmp[0][index][0] - tmp[1][index][1]))
        tmp[2][index][0] = tmp[2][index][1] + (alpha * (tmp[1][index][0] - tmp[2][index][1]))
        tmp[3][index][0] = tmp[0][index][0] + (v * (tmp[0][index][0] + (v * (tmp[0][index][0] - tmp[1][index][0])) - tmp[1][index][0] - (v * (tmp[1][index][0] - tmp[2][index][0]))))
    return tmp[3][index][0]

def T3OnArray(index, num, price, per, v, cbars, bar):
    T3_ = EMPTY_VALUE
    len_ = MathMax(((per + 5.0) / 3.0) - 1, 1)
    dema1 = 0.0
    dema2 = 0.0
    if bar == cbars:
        T3_ = price
        for k in range(0, 6):
            tmp[num + k][index][0] = T3_
    elif bar > cbars:
        dema1 = DEMAOnArray(index, num, price, len_, v, cbars, bar)
        dema2 = DEMAOnArray(index, num + 2, dema1, len_, v, cbars, bar)
        T3_ = DEMAOnArray(index, num + 4, dema2, len_, v, cbars, bar)
    return T3_

def LaguerreOnArray(index, price, per, order, cbars, bar):
    laguerre = EMPTY_VALUE
    gamma = 1 - _fdiv(10.0, per + 9)
    aprice = Arr(0, 0.0)
    ArrayResize(aprice, order)
    ArrayInitialize(aprice, price)
    if bar >= cbars:
        for i in range(0, order):
            if bar == cbars:
                tmp[i][index][0] = price
            elif bar > cbars:
                if i == 0:
                    tmp[i][index][0] = ((1 - gamma) * price) + (gamma * tmp[i][index][1])
                else:
                    tmp[i][index][0] = ((-gamma) * tmp[i - 1][index][0]) + tmp[i - 1][index][1] + (gamma * tmp[i][index][1])
                aprice[i] = tmp[i][index][0]
        if bar > cbars:
            laguerre = TriMA_genOnArray(1, aprice, order, cbars, 0)
        else:
            laguerre = price
    return laguerre

def McGinleyOnArray(price, prev, per, cbars, bar):
    md = EMPTY_VALUE
    if bar == cbars:
        md = price
    elif bar > cbars:
        if prev != 0:
            md = prev + _fdiv(price - prev, (per * MathPow(_fdiv(price, prev), 4)) / 2)
        else:
            md = price
    return md

def BF2POnArray(price, array, per, cbars, bar):
    bf2p = EMPTY_VALUE
    a = MathExp(_fdiv(-1.414 * 3.141592653589793, per))
    b = 2 * a * MathCos(_fdiv(1.414 * 1.25 * 3.141592653589793, per))
    c2 = b
    c3 = (-a) * a
    c1 = 1 - c2 - c3
    if (bar >= cbars and array[1] != EMPTY_VALUE) and array[2] != EMPTY_VALUE:
        bf2p = ((c1 * (price[bar] + (2 * price[bar - 1]) + price[bar - 2])) / 4) + (c2 * array[1]) + (c3 * array[2])
    elif bar < cbars and bar > 2:
        bf2p = (price[bar] + (2 * price[bar - 1]) + price[bar - 2]) / 4
    return bf2p

def BF3POnArray(price, array, per, cbars, bar):
    bf3p = 0.0
    a = MathExp(_fdiv(-3.141592653589793, per))
    b = 2 * a * MathCos(_fdiv(1.738 * 3.141592653589793, per))
    c = a * a
    d2 = b + c
    d3 = -(c + (b * c))
    d4 = c * c
    d1 = 1 - d2 - d3 - d4
    if ((bar >= cbars and array[1] != EMPTY_VALUE) and array[2] != EMPTY_VALUE) and array[3] != EMPTY_VALUE:
        bf3p = ((d1 * (price[bar] + (3 * price[bar - 1]) + (3 * price[bar - 2]) + price[bar - 3])) / 8) + (d2 * array[1]) + (d3 * array[2]) + (d4 * array[3])
    elif bar < cbars and bar > 2:
        bf3p = (price[bar] + (3 * price[bar - 1]) + (3 * price[bar - 2]) + price[bar - 3]) / 8
    return bf3p

def SuperSmuOnArray(price, array, per, cbars, bar):
    supsm = 0.0
    a = MathExp(_fdiv(-1.414 * 3.141592653589793, per))
    b = 2 * a * MathCos(_fdiv(1.414 * 3.141592653589793, per))
    c2 = b
    c3 = (-a) * a
    c1 = 1 - c2 - c3
    if (bar >= cbars and array[1] != EMPTY_VALUE) and array[2] != EMPTY_VALUE:
        supsm = ((c1 * (price[bar] + price[bar - 1])) / 2) + (c2 * array[1]) + (c3 * array[2])
    elif bar < cbars and bar > 2:
        supsm = (price[bar] + price[bar - 1]) / 2
    return supsm

def DecyclerOnArray(price, hp, per, cbars, bar):
    alpha1 = _fdiv(MathCos(_fdiv(1.414 * 3.141592653589793, per)) + MathSin(_fdiv(1.414 * 3.141592653589793, per)) - 1, MathCos(_fdiv(1.414 * 3.141592653589793, per)))
    if bar < (cbars - 4):
        return 0.0
    hp[0] = ((1 - (alpha1 / 2)) * (1 - (alpha1 / 2)) * (price[bar] - (2 * price[bar - 1]) + price[bar - 2])) + (2 * (1 - alpha1) * hp[1]) - ((1 - alpha1) * (1 - alpha1) * hp[2])
    return hp[0]

def eVWMAOnArray(price, prev, per, cbars, rates, bar):
    evwma = EMPTY_VALUE
    volume = Arr(0, 0)
    ArraySetAsSeries(volume, True)
    volumes = CopyTickVolume(Symbol(), 0, rates - 1 - bar, per, volume)
    if volumes < 0:
        return EMPTY_VALUE
    if bar == cbars:
        evwma = price
    elif bar > cbars:
        max_ = 0.0
        for i in range(0, per):
            max_ = MathMax(max_, volume[i])
        diff = (3 * max_) - volume[0]
        if diff < 0:
            evwma = prev
        else:
            evwma = _fdiv((diff * prev) + (volume[0] * price), 3 * max_)
    return evwma

def EWMAOnArray(array, per, bar):
    sum_ = 0.0
    weight = 0.0
    alpha = _fdiv(2.0, 1 + per)
    if bar >= ma_period:
        for i in range(0, ma_period):
            weight += alpha * MathPow(1 - alpha, i)
            sum_ += array[bar - i] * alpha * MathPow(1 - alpha, i)
    if weight > 0:
        return _fdiv(sum_, weight)
    else:
        return 0.0

def DsEMAOnArray(index, price, per, cbars, bar):
    alpha = _fdiv(4.0, per + 3)
    if bar == cbars:
        for k in range(0, 2):
            tmp[k][index][0] = price
        return price
    elif bar > cbars:
        tmp[0][index][0] = tmp[0][index][1] + (alpha * (price - tmp[0][index][1]))
        tmp[1][index][0] = tmp[1][index][1] + (alpha * (tmp[0][index][0] - tmp[1][index][1]))
    return tmp[1][index][0]

def TsEMAOnArray(index, price, per, cbars, bar):
    alpha = _fdiv(6.0, per + 5)
    if bar == cbars:
        for k in range(0, 3):
            tmp[k][index][0] = price
        return price
    elif bar > cbars:
        tmp[0][index][0] = tmp[0][index][1] + (alpha * (price - tmp[0][index][1]))
        tmp[1][index][0] = tmp[1][index][1] + (alpha * (tmp[0][index][0] - tmp[1][index][1]))
        tmp[2][index][0] = tmp[2][index][1] + (alpha * (tmp[1][index][0] - tmp[2][index][1]))
    return tmp[2][index][0]

def VEMAOnArray(index, price, per, cbars, rates, bar):
    vema = price
    alpha = _fdiv(2.0, per + 1)
    volume = Arr(0, 0)
    ArraySetAsSeries(volume, True)
    volumes = CopyTickVolume(Symbol(), 0, rates - 1 - bar, 1, volume)
    if volumes < 0:
        return EMPTY_VALUE
    if bar == cbars:
        tmp[0][index][0] = (1 - alpha) * price * volume[0]
        tmp[1][index][0] = (1 - alpha) * volume[0]
    elif bar > cbars:
        tmp[0][index][0] = tmp[0][index][1] + (alpha * ((price * volume[0]) - tmp[0][index][1]))
        tmp[1][index][0] = tmp[1][index][1] + (alpha * (volume[0] - tmp[1][index][1]))
    if tmp[1][index][0] > 0:
        vema = _fdiv(tmp[0][index][0], tmp[1][index][0])
    return vema

def HeikenAshi(index, price, close_, open_, high_, low_, cbars, bar):
    if prevhabar[index] != bar:
        haClose[index][1] = haClose[index][0]
        haOpen[index][1] = haOpen[index][0]
        haHigh[index][1] = haHigh[index][0]
        haLow[index][1] = haLow[index][0]
        prevhabar[index] = bar
    if bar == cbars:
        haClose[index][0] = close_
        haOpen[index][0] = open_
        haHigh[index][0] = high_
        haLow[index][0] = low_
    else:
        haClose[index][0] = (open_ + high_ + low_ + close_) / 4
        haOpen[index][0] = (haOpen[index][1] + haClose[index][1]) / 2
        haHigh[index][0] = MathMax(high_, MathMax(haOpen[index][0], haClose[index][0]))
        haLow[index][0] = MathMin(low_, MathMin(haOpen[index][0], haClose[index][0]))
    _sw4 = price
    if _sw4 == 0:
        return haClose[index][0]
    elif _sw4 == 1:
        return haOpen[index][0]
    elif _sw4 == 2:
        return haHigh[index][0]
    elif _sw4 == 3:
        return haLow[index][0]
    elif _sw4 == 4:
        return (haHigh[index][0] + haLow[index][0]) / 2
    elif _sw4 == 5:
        return (haHigh[index][0] + haLow[index][0] + haClose[index][0]) / 3
    elif _sw4 == 6:
        return (haHigh[index][0] + haLow[index][0] + (2 * haClose[index][0])) / 4
    elif _sw4 == 7:
        return (haClose[index][0] + haOpen[index][0]) / 2
    elif _sw4 == 8:
        return (haHigh[index][0] + haLow[index][0] + haClose[index][0] + haOpen[index][0]) / 4
    elif _sw4 == 9:
        if haClose[index][0] > haOpen[index][0]:
            return (haHigh[index][0] + haClose[index][0]) / 2
        else:
            return (haLow[index][0] + haClose[index][0]) / 2
    elif _sw4 == 10:
        if haClose[index][0] > haOpen[index][0]:
            return haHigh[index][0]
        else:
            return haLow[index][0]
    else:
        return haClose[index][0]

def getPrice(price, close_, open_, high_, low_, bar):
    _sw5 = price
    if _sw5 == 0:
        return close_
    elif _sw5 == 1:
        return open_
    elif _sw5 == 2:
        return high_
    elif _sw5 == 3:
        return low_
    elif _sw5 == 4:
        return (high_ + low_) / 2
    elif _sw5 == 5:
        return (high_ + low_ + close_) / 3
    elif _sw5 == 6:
        return (high_ + low_ + (2 * close_)) / 4
    elif _sw5 == 7:
        return (close_ + open_) / 2
    elif _sw5 == 8:
        return (high_ + low_ + close_ + open_) / 4
    elif _sw5 == 9:
        if close_ > open_:
            return (high_ + close_) / 2
        else:
            return (low_ + close_) / 2
    elif _sw5 == 10:
        if close_ > open_:
            return high_
        else:
            return low_
    else:
        return close_

def timeframeToString(timeframe):
    _sw6 = timeframe
    if _sw6 == PERIOD_CURRENT:
        return 'Current'
    elif _sw6 == PERIOD_M1:
        return 'M1'
    elif _sw6 == PERIOD_M2:
        return 'M2'
    elif _sw6 == PERIOD_M3:
        return 'M3'
    elif _sw6 == PERIOD_M4:
        return 'M4'
    elif _sw6 == PERIOD_M5:
        return 'M5'
    elif _sw6 == PERIOD_M6:
        return 'M6'
    elif _sw6 == PERIOD_M10:
        return 'M10'
    elif _sw6 == PERIOD_M12:
        return 'M12'
    elif _sw6 == PERIOD_M15:
        return 'M15'
    elif _sw6 == PERIOD_M20:
        return 'M20'
    elif _sw6 == PERIOD_M30:
        return 'M30'
    elif _sw6 == PERIOD_H1:
        return 'H1'
    elif _sw6 == PERIOD_H2:
        return 'H2'
    elif _sw6 == PERIOD_H3:
        return 'H3'
    elif _sw6 == PERIOD_H4:
        return 'H4'
    elif _sw6 == PERIOD_H6:
        return 'H6'
    elif _sw6 == PERIOD_H8:
        return 'H8'
    elif _sw6 == PERIOD_H12:
        return 'H12'
    elif _sw6 == PERIOD_D1:
        return 'D1'
    elif _sw6 == PERIOD_W1:
        return 'W1'
    elif _sw6 == PERIOD_MN1:
        return 'MN1'
    else:
        return 'Current'

def isNewBar(timeframe):
    global prevnbtime
    res = False
    if tf >= 0:
        if iTime(None, timeframe, 0) != prevnbtime:
            res = True
            prevnbtime = iTime(None, timeframe, 0)
    else:
        res = True
    return res

def BoxAlert(cond, text):
    global prevmess
    mess = IndicatorName + '(' + Symbol() + ',' + TF + ')' + text
    if cond and mess != prevmess:
        Alert(mess)
        prevmess = mess
        return True
    return False

def Pause(sec):
    global pausetime
    if TimeCurrent() >= (pausetime + sec):
        pausetime = TimeCurrent()
        return True
    return False

def WarningSound(cond, num, sec, sound, curtime):
    global _s_WarningSound_i, warningtime
    if cond:
        if curtime != warningtime:
            _s_WarningSound_i = 0
        if _s_WarningSound_i < num and Pause(sec):
            PlaySound(sound)
            warningtime = curtime
            _s_WarningSound_i += 1

def EmailAlert(cond, text1, text2, num):
    global prevemail
    subj = 'New ' + text1 + ' Signal from ' + IndicatorName + '!!!'
    mess = IndicatorName + '(' + Symbol() + ',' + TF + ')' + text2
    if cond and mess != prevemail:
        if subj != '' and mess != '':
            for i in range(0, num):
                SendMail(subj, mess)
        prevemail = mess
        return True
    return False

def PushAlert(cond, text):
    global prevpush
    push = IndicatorName + '(' + Symbol() + ',' + TF + ')' + text
    if cond and push != prevpush:
        SendNotification(push)
        prevpush = push
        return True
    return False

# ---- static local variables
_s_WarningSound_i = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AllAveragesV49MT5(_MQL5Indicator):
    name = 'AllAverages_v4.9_MT5'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=0),  # Timeframe
        'Price': _Choice({0: 'Close', 1: 'Open', 2: 'High', 3: 'Low', 4: 'Median', 5: 'Typical', 6: 'Weighted Close', 7: 'Median Body (Open+Close)/2', 8: 'Average (High+Low+Open+Close)/4', 9: 'Trend Biased', 10: 'Trend Biased(extreme)', 11: 'Heiken Ashi Close', 12: 'Heiken Ashi Open', 13: 'Heiken Ashi High', 14: 'Heiken Ashi Low', 15: 'Heiken Ashi Median', 16: 'Heiken Ashi Typical', 17: 'Heiken Ashi Weighted Close', 18: 'Heiken Ashi Median Body', 19: 'Heiken Ashi Average', 20: 'Heiken Ashi Trend Biased', 21: 'Heiken Ashi Trend Biased(extreme)'}, default=0),  # Apply To
        'MA_Period': 14,  # Period
        'MA_Shift': 0,  # Shift
        'MA_Method': _Choice({0: 'Simple Moving Average', 1: 'Exponential Moving Average', 2: 'Wilder Exponential Moving Average', 3: 'Linear Weighted Moving Average', 4: 'Sine Weighted Moving Average', 5: 'Triangular Moving Average', 6: 'Least Square Moving Average (or EPMA, Linear Regression Line)', 7: 'Smoothed Moving Average', 8: 'Hull Moving Average by Alan Hull', 9: 'Zero-Lag Exponential Moving Average', 10: 'Double Exponential Moving Average by Patrick Mulloy', 11: 'T3 by T.Tillson (original version)', 12: 'Instantaneous Trendline by J.Ehlers', 13: 'Moving Median', 14: 'Geometric Mean', 15: 'Regularized EMA by Chris Satchwell', 16: 'Integral of Linear Regression Slope', 17: 'Combination of LSMA and ILRS', 18: 'Triangular Moving Average generalized by J.Ehlers', 19: 'Volume Weighted Moving Average', 20: 'Smoothing by Mark Jurik', 21: 'Simplified SMA', 22: 'Arnaud Legoux Moving Average', 23: 'Triple Exponential Moving Average by Patrick Mulloy', 24: 'T3 by T.Tillson (correct version)', 25: 'Laguerre filter by J.Ehlers', 26: 'McGinley Dynamic', 27: 'Two-pole modified Butterworth filter by J.Ehlers', 28: 'Three-pole modified Butterworth filter by J.Ehlers', 29: 'SuperSmoother by J.Ehlers', 30: 'Simple Decycler by J.Ehlers', 31: 'Modified eVWMA', 32: 'Exponential Weighted Moving Average', 33: 'Double Smoothed EMA', 34: 'Triple Smoothed EMA', 35: 'Volume-weighted Exponential Moving Average(V-EMA)'}, default=0),  # Method
        'ShowInColor': True,  # Show In Color
        'CountBars': 0,  # Number of bars counted: 0-all bars
        'AlertOn': False,  # Alert On
        'AlertShift': 1,  # Alert Shift:0-current bar,1-previous bar
        'SoundsNumber': 5,  # Number of sounds after Signal
        'SoundsPause': 5,  # Pause in sec between sounds
        'EmailOn': False,  # Email Alert On
        'EmailsNumber': 1,  # Emails Number
        'PushNotificationOn': False,  # Push Notification On
    }

