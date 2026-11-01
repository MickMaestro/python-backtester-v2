"""SpearmanRankCorrelation_Histogram_Alerts — converted from MQL5: MQL5 Indicators/SpearmanRankCorrelation_Histogram_Alerts/SpearmanRankCorrelation_Histogram_Alerts.mq5

Copyright: Copyright © 2007, MetaQuotes Software Corp.; Link: http://www.metaquotes.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_minimum': -1.0, 'indicator_maximum': 1.0}, 'types': {1: 10}, 'colors': {1: [16711935, 8388736, 8421504, 16711680, 16748574]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {}, 'levels': [], 'description': [], 'name': 'SpearmanRankCorrelation_Histogram_Alerts', 'source': 'MQL5 Indicators/SpearmanRankCorrelation_Histogram_Alerts/SpearmanRankCorrelation_Histogram_Alerts.mq5', 'folder': 'SpearmanRankCorrelation_Histogram_Alerts', 'inputs': [{'mql': 'rangeN', 'py': 'rangeN', 'param': 'rangeN', 'type': 'int', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'CalculatedBars', 'py': 'CalculatedBars', 'param': 'CalculatedBars', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'Maxrange', 'py': 'Maxrange', 'param': 'Maxrange', 'type': 'int', 'default': 30, 'label': '', 'sinput': False}, {'mql': 'direction', 'py': 'direction', 'param': 'direction', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'inHighLevel', 'py': 'inHighLevel', 'param': 'inHighLevel', 'type': 'double', 'default': 0.5, 'label': '', 'sinput': False}, {'mql': 'inLowLevel', 'py': 'inLowLevel', 'param': 'inLowLevel', 'type': 'double', 'default': -0.5, 'label': '', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для подачи сигнала', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Разрешение алерта', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': 'Количество алертов', 'sinput': False}, {'mql': 'EMailON', 'py': 'EMailON', 'param': 'EMailON', 'type': 'bool', 'default': False, 'label': 'Разрешение почтовой отправки сигнала', 'sinput': False}, {'mql': 'PushON', 'py': 'PushON', 'param': 'PushON', 'type': 'bool', 'default': False, 'label': 'Разрешение отправки сигнала на мобильный', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_APPLIED_PRICE_
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
PRICE_DEMARK_ = 12
_enum('ENUM_APPLIED_PRICE_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
rangeN = _input('rangeN', 14)
CalculatedBars = _input('CalculatedBars', 0)
Maxrange = _input('Maxrange', 30)
direction = _input('direction', True)
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
inHighLevel = _input('inHighLevel', 0.5)
inLowLevel = _input('inLowLevel', -0.5)
NumberofBar = _input('NumberofBar', 1)  # Номер бара для подачи сигнала
SoundON = _input('SoundON', True)  # Разрешение алерта
NumberofAlerts = _input('NumberofAlerts', 2)  # Количество алертов
EMailON = _input('EMailON', False)  # Разрешение почтовой отправки сигнала
PushON = _input('PushON', False)  # Разрешение отправки сигнала на мобильный
min_rates_total = 0
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
multiply = 0.0
R2 = Arr(0, 0.0)
TrueRanks = Arr(0, 0.0)
PriceInt = Arr(0, 0)
SortInt = Arr(0, 0)
Maxrange_ = 0

def SpearmanRankCorrelation(Ranks, N):
    res = 0.0
    z2 = 0.0
    for iii in range(0, N):
        z2 += MathPow(Ranks[iii] - iii - 1, 2)
    res = 1 - _fdiv(6 * z2, MathPow(N, 3) - N)
    return res

def RankPrices(TrueRanks_, InitialArray):
    i = 0
    k = 0
    m = 0
    dublicat = 0
    counter = 0
    etalon = 0
    dcounter = 0.0
    averageRank = 0.0
    ArrayCopy(SortInt, InitialArray, 0, 0, WHOLE_ARRAY)
    i = 0
    for i in range(i, rangeN):
        TrueRanks_[i] = i + 1
    else:
        i = _range_end(i, rangeN, 1)
    ArraySort(SortInt)
    i = 0
    while i < (rangeN - 1):
        if SortInt[i] != SortInt[i + 1]:
            i += 1
            continue
        dublicat = SortInt[i]
        k = i + 1
        counter = 1
        averageRank = i + 1
        while k < rangeN:
            if SortInt[k] == dublicat:
                counter += 1
                averageRank += k + 1
                k += 1
            else:
                break
        dcounter = counter
        averageRank = _fdiv(averageRank, dcounter)
        m = i
        for m in range(m, k):
            TrueRanks_[m] = averageRank
        else:
            m = _range_end(m, k, 1)
        i = k
        i += 1
    i = 0
    for i in range(i, rangeN):
        etalon = InitialArray[i]
        k = 0
        while k < rangeN:
            if etalon == SortInt[k]:
                R2[i] = TrueRanks_[k]
                break
            k += 1
    else:
        i = _range_end(i, rangeN, 1)
    return

def OnInit():
    global Maxrange_, multiply
    ArrayResize(R2, rangeN)
    ArrayResize(PriceInt, rangeN)
    ArrayResize(SortInt, rangeN)
    if direction:
        ArraySetAsSeries(SortInt, True)
    ArrayResize(TrueRanks, rangeN)
    if Maxrange <= 0:
        Maxrange_ = 10
    else:
        Maxrange_ = Maxrange
    multiply = MathPow(10, Digits())
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, rangeN)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    shortname = Box("")
    if rangeN > Maxrange_:
        shortname.v = 'Decrease rangeN input!'
    else:
        StringConcatenate(shortname, 'SpearmanRankCorrelation_Histogram_Alerts(', rangeN, ')')
    PlotIndexSetString(0, PLOT_LABEL, shortname.v)
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, inHighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, inLowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrBlue)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASH)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if rates_total < rangeN:
        return 0
    if rangeN > Maxrange_:
        return 0
    limit = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 2 - rangeN
    else:
        if not CalculatedBars:
            limit = rates_total - prev_calculated
        else:
            limit = CalculatedBars
    ArraySetAsSeries(Close, True)
    ArraySetAsSeries(Open, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Spread, True)
    for bar in range(limit, 0 - 1, -1):
        for k in range(0, rangeN):
            PriceInt[k] = _int(PriceSeries(IPC, bar + k, Open, Low, High, Close) * multiply)
        RankPrices(TrueRanks, PriceInt)
        IndBuffer[bar] = SpearmanRankCorrelation(R2, rangeN)
        clr = 2
        res = IndBuffer[bar]
        if res > 0:
            if res > inHighLevel:
                clr = 4
            else:
                clr = 3
        if res < 0:
            if res < inLowLevel:
                clr = 0
            else:
                clr = 1
        ColorIndBuffer[bar] = clr
    BuySignal('SpearmanRankCorrelation_Histogram_Alerts', rates_total, prev_calculated, Close, Spread)
    SellSignal('SpearmanRankCorrelation_Histogram_Alerts', rates_total, prev_calculated, Close, Spread)
    return rates_total

def BuySignal(SignalSirname, Rates_total, Prev_calculated, Close, Spread):
    global _s_BuySignal_counter
    if Rates_total != Prev_calculated:
        _s_BuySignal_counter = 0
    SignalText = ''
    BuySignal_ = False
    index = _int(NumberofBar)
    index1 = _int(NumberofBar) + 1
    if IndBuffer[index1] <= 0 and IndBuffer[index] > 0:
        BuySignal_ = True
        SignalText = SignalText + 'Пробой нуля! '
    if ColorIndBuffer[index1] < 4 and ColorIndBuffer[index] == 4:
        BuySignal_ = True
        SignalText = SignalText + 'Пробой уровня перекупленности! '
    if ColorIndBuffer[index1] == 1 and ColorIndBuffer[index] > 2:
        BuySignal_ = True
        SignalText = SignalText + 'Выход из зоны перепроданности! '
    if BuySignal_ and _s_BuySignal_counter <= NumberofAlerts:
        _s_BuySignal_counter += 1
        tm = MqlDateTime()
        TimeToStruct(TimeCurrent(), tm)
        text = TimeToString(TimeCurrent(), TIME_DATE) + ' ' + _str(tm.hour) + ':' + _str(tm.min)
        Ask = Close[index]
        Bid = Close[index]
        Bid += Spread[index] * Point()
        sAsk = DoubleToString(Ask, Digits())
        sBid = DoubleToString(Bid, Digits())
        sPeriod = GetStringTimeframe(ChartPeriod())
        if SoundON:
            Alert('BUY signal ' + SignalText + '\n Ask=', Ask, '\n Bid=', Bid, '\n currtime=', text, '\n Symbol=', Symbol(), ' Period=', sPeriod)
        if EMailON:
            SendMail(SignalSirname + ': BUY signal ' + SignalText, ' at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
        if PushON:
            SendNotification(SignalSirname + ': BUY signal ' + SignalText + ' at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)

def SellSignal(SignalSirname, Rates_total, Prev_calculated, Close, Spread):
    global _s_SellSignal_counter
    if Rates_total != Prev_calculated:
        _s_SellSignal_counter = 0
    SignalText = ''
    SellSignal_ = False
    index = _int(NumberofBar)
    index1 = _int(NumberofBar) + 1
    if IndBuffer[index1] >= 0 and IndBuffer[index] < 0:
        SellSignal_ = True
        SignalText = SignalText + 'Пробой нуля! '
    if ColorIndBuffer[index1] > 0 and ColorIndBuffer[index] == 0:
        SellSignal_ = True
        SignalText = SignalText + 'Пробой уровня пепроданности! '
    if ColorIndBuffer[index1] == 4 and ColorIndBuffer[index] < 4:
        SellSignal_ = True
        SignalText = SignalText + 'Выход из зоны перекупленности! '
    if SellSignal_ and _s_SellSignal_counter <= NumberofAlerts:
        _s_SellSignal_counter += 1
        tm = MqlDateTime()
        TimeToStruct(TimeCurrent(), tm)
        text = TimeToString(TimeCurrent(), TIME_DATE) + ' ' + _str(tm.hour) + ':' + _str(tm.min)
        Ask = Close[index]
        Bid = Close[index]
        Bid += Spread[index] * Point()
        sAsk = DoubleToString(Ask, Digits())
        sBid = DoubleToString(Bid, Digits())
        sPeriod = GetStringTimeframe(ChartPeriod())
        if SoundON:
            Alert('SELL signal ' + SignalText + '\n Ask=', Ask, '\n Bid=', Bid, '\n currtime=', text, '\n Symbol=', Symbol(), ' Period=', sPeriod)
        if EMailON:
            SendMail(SignalSirname + ': SELL signal ' + SignalText, ' at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
        if PushON:
            SendNotification(SignalSirname + ': SELL signal ' + SignalText + ' at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def PriceSeries(applied_price, bar, Open, Low, High, Close):
    _sw1 = applied_price
    if _sw1 == PRICE_CLOSE:
        return Close[bar]
    elif _sw1 == PRICE_OPEN:
        return Open[bar]
    elif _sw1 == PRICE_HIGH:
        return High[bar]
    elif _sw1 == PRICE_LOW:
        return Low[bar]
    elif _sw1 == PRICE_MEDIAN:
        return (High[bar] + Low[bar]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (Close[bar] + High[bar] + Low[bar]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return ((2 * Close[bar]) + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 8:
        return (Open[bar] + Close[bar]) / 2.0
    elif _sw1 == 9:
        return (Open[bar] + Close[bar] + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 10:
        if Close[bar] > Open[bar]:
            return High[bar]
        else:
            if Close[bar] < Open[bar]:
                return Low[bar]
            else:
                return Close[bar]
    elif _sw1 == 11:
        if Close[bar] > Open[bar]:
            return (High[bar] + Close[bar]) / 2.0
        else:
            if Close[bar] < Open[bar]:
                return (Low[bar] + Close[bar]) / 2.0
            else:
                return Close[bar]
    elif _sw1 == 12:
        res = High[bar] + Low[bar] + Close[bar]
        if Close[bar] < Open[bar]:
            res = (res + Low[bar]) / 2
        if Close[bar] > Open[bar]:
            res = (res + High[bar]) / 2
        if Close[bar] == Open[bar]:
            res = (res + Close[bar]) / 2
        return (res - Low[bar] + (res - High[bar])) / 2
    else:
        return Close[bar]

# ---- static local variables
_s_BuySignal_counter = 0
_s_SellSignal_counter = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class SpearmanRankCorrelationHistogramAlerts(_MQL5Indicator):
    name = 'SpearmanRankCorrelation_Histogram_Alerts'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'rangeN': 14,
        'CalculatedBars': 0,
        'Maxrange': 30,
        'direction': True,
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'inHighLevel': 0.5,
        'inLowLevel': -0.5,
        'NumberofBar': 1,  # Номер бара для подачи сигнала
        'SoundON': True,  # Разрешение алерта
        'NumberofAlerts': 2,  # Количество алертов
        'EMailON': False,  # Разрешение почтовой отправки сигнала
        'PushON': False,  # Разрешение отправки сигнала на мобильный
    }
    y_range = (-1.0, 1.0)

