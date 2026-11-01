"""XPeriodCandleSystem_Alert — converted from MQL5: MQL5 Indicators/XPeriodCandleSystem_Alert/XPeriodCandleSystem_Alert.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 8, 'indicator_plots': 4}, 'types': {1: 1, 2: 1, 3: 1, 4: 17}, 'colors': {1: [14822282], 2: [65280], 3: [255], 4: [16748574, 16436871, 8421504, 13353215, 16711935]}, 'widths': {1: 2, 2: 2, 3: 2}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'XMA', 2: '+2Sigma', 3: '-2Sigma', 4: 'Open;High;Low;Close'}, 'levels': [], 'description': [], 'name': 'XPeriodCandleSystem_Alert', 'source': 'MQL5 Indicators/XPeriodCandleSystem_Alert/XPeriodCandleSystem_Alert.mq5', 'folder': 'XPeriodCandleSystem_Alert', 'inputs': [{'mql': 'period', 'py': 'period', 'param': 'period', 'type': 'uint', 'default': 5, 'label': 'Период расчёта свечей', 'sinput': False}, {'mql': 'MA_SMethod', 'py': 'MA_SMethod', 'param': 'MA_SMethod', 'type': 'int', 'default': 4, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'MA_Length', 'py': 'MA_Length', 'param': 'MA_Length', 'type': 'int', 'default': 3, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'MA_Phase', 'py': 'MA_Phase', 'param': 'MA_Phase', 'type': 'int', 'default': 100, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'BB_Method', 'py': 'BB_Method', 'param': 'BB_Method', 'type': 'int', 'default': 0, 'label': 'метод усреднения полос Боллинджера', 'sinput': False}, {'mql': 'BBLength', 'py': 'BBLength', 'param': 'BBLength', 'type': 'uint', 'default': 20, 'label': 'глубина  усреднения полос Боллинджера', 'sinput': False}, {'mql': 'BBPhase', 'py': 'BBPhase', 'param': 'BBPhase', 'type': 'int', 'default': 15, 'label': 'параметр усреднения полос Боллинджера,', 'sinput': False}, {'mql': 'BandsDeviation', 'py': 'BandsDeviation', 'param': 'BandsDeviation', 'type': 'double', 'default': 1.001, 'label': 'девиация', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'uint', 'default': 0, 'label': 'сдвиг свеч индикатора по горизонтали в барах влево', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для подачи сигнала', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Разрешение алерта', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': 'Количество алертов', 'sinput': False}, {'mql': 'EMailON', 'py': 'EMailON', 'param': 'EMailON', 'type': 'bool', 'default': False, 'label': 'Разрешение почтовой отправки сигнала', 'sinput': False}, {'mql': 'PushON', 'py': 'PushON', 'param': 'PushON', 'type': 'bool', 'default': False, 'label': 'Разрешение отправки сигнала на мобильный', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
period = _input('period', 5)  # Период расчёта свечей
MA_SMethod = _input('MA_SMethod', MODE_JJMA)  # Метод усреднения
MA_Length = _input('MA_Length', 3)  # глубина сглаживания
MA_Phase = _input('MA_Phase', 100)  # параметр сглаживания,
BB_Method = _input('BB_Method', MODE_SMA_)  # метод усреднения полос Боллинджера
BBLength = _input('BBLength', 20)  # глубина  усреднения полос Боллинджера
BBPhase = _input('BBPhase', 15)  # параметр усреднения полос Боллинджера,
BandsDeviation = _input('BandsDeviation', 1.001)  # девиация
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг свеч индикатора по горизонтали в барах влево
NumberofBar = _input('NumberofBar', 1)  # Номер бара для подачи сигнала
SoundON = _input('SoundON', True)  # Разрешение алерта
NumberofAlerts = _input('NumberofAlerts', 2)  # Количество алертов
EMailON = _input('EMailON', False)  # Разрешение почтовой отправки сигнала
PushON = _input('PushON', False)  # Разрешение отправки сигнала на мобильный
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorsBuffer = Arr(0, 0.0)
ExtLineBuffer0 = Arr(0, 0.0)
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
min_rates_2 = 0
min_rates_3 = 0
Count = Arr(0, 0)
iopen = Arr(0, 0.0)
ihigh = Arr(0, 0.0)
ilow = Arr(0, 0.0)

def Recount_ArrayZeroPos(CoArr, Size):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def OnInit():
    global min_rates_1, min_rates_2, min_rates_3, min_rates_total
    min_rates_1 = GetStartBars(MA_SMethod, MA_Length, MA_Phase)
    min_rates_2 = min_rates_1 + _int(period) + 1
    min_rates_3 = GetStartBars(BB_Method, BBLength, BBPhase) + 1
    min_rates_total = min_rates_3 + _int(BBLength)
    ArrayResize(Count, period)
    ArrayResize(iopen, period)
    ArrayResize(ihigh, period)
    ArrayResize(ilow, period)
    SetIndexBuffer(0, ExtLineBuffer0, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    SetIndexBuffer(1, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLineBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(3, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, ExtColorsBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(3, PLOT_SHIFT, -_int(Shift))
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorsBuffer, True)
    ArraySetAsSeries(ExtLineBuffer0, True)
    ArraySetAsSeries(ExtLineBuffer1, True)
    ArraySetAsSeries(ExtLineBuffer2, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'XPeriodCandleSystem_Alert'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    bar = 0
    limit = 0
    maxbar1 = 0
    maxbar2 = 0
    maxbar3 = 0
    HH = 0.0
    LL = 0.0
    iclose = 0.0
    price = 0.0
    xma = 0.0
    stdev = 0.0
    maxbar1 = rates_total - 2
    maxbar2 = maxbar1 - min_rates_2
    maxbar3 = maxbar2 - min_rates_3
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = maxbar1
        ArrayInitialize(Count, 0)
        ArrayInitialize(iopen, open[maxbar1])
        ArrayInitialize(ihigh, high[maxbar1])
        ArrayInitialize(ilow, low[maxbar1])
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(iopen, True)
    ArraySetAsSeries(ihigh, True)
    ArraySetAsSeries(ilow, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        iopen[Count[0]] = XMAO.XMASeries(maxbar1, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, open[bar], bar, True)
        ihigh[Count[0]] = XMAH.XMASeries(maxbar1, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, high[bar], bar, True)
        ilow[Count[0]] = XMAL.XMASeries(maxbar1, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, low[bar], bar, True)
        iclose = XMAC.XMASeries(maxbar1, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, close[bar], bar, True)
        HH = ihigh[ArrayMaximum(ihigh, 0, period)]
        LL = ilow[ArrayMinimum(ilow, 0, period)]
        ExtOpenBuffer[bar] = iopen[Count[period - 1]]
        ExtHighBuffer[bar] = HH
        ExtLowBuffer[bar] = LL
        ExtCloseBuffer[bar] = iclose
        ExtColorsBuffer[bar] = 2.0
        Max = MathMax(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        Min = MathMin(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        ExtHighBuffer[bar] = MathMax(Max, ExtHighBuffer[bar])
        ExtLowBuffer[bar] = MathMin(Min, ExtLowBuffer[bar])
        if ExtOpenBuffer[bar] <= ExtCloseBuffer[bar]:
            ExtColorsBuffer[bar] = 1.0
        else:
            ExtColorsBuffer[bar] = 3.0
        if bar:
            Recount_ArrayZeroPos(Count, period)
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        price = PriceSeries(IPC, bar, ExtOpenBuffer, ExtLineBuffer0, ExtHighBuffer, ExtCloseBuffer)
        xma = XMA1.XMASeries(maxbar2, prev_calculated, rates_total, BB_Method, BBPhase, BBLength, price, bar, True)
        ExtLineBuffer0[bar] = xma
        stdev = STD.StdDevSeries(maxbar3, prev_calculated, rates_total, BBLength, BandsDeviation, price, xma, bar, True)
        ExtLineBuffer1[bar] = xma + stdev
        ExtLineBuffer2[bar] = xma - stdev
        if ExtOpenBuffer[bar] <= ExtCloseBuffer[bar] and ExtCloseBuffer[bar] > ExtLineBuffer1[bar + Shift]:
            ExtColorsBuffer[bar] = 0.0
        if ExtOpenBuffer[bar] > ExtCloseBuffer[bar] and ExtCloseBuffer[bar] < ExtLineBuffer2[bar + Shift]:
            ExtColorsBuffer[bar] = 4.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    BuySignal('XPeriodCandleSystem_Alert', ExtColorsBuffer, rates_total, prev_calculated, close, spread)
    SellSignal('XPeriodCandleSystem_Alert', ExtColorsBuffer, rates_total, prev_calculated, close, spread)
    return rates_total

def BuySignal(SignalSirname, ColorArrow, Rates_total, Prev_calculated, Close, Spread):
    global _s_BuySignal_counter
    if Rates_total != Prev_calculated:
        _s_BuySignal_counter = 0
    BuySignal_ = False
    SeriesTest = ArrayGetAsSeries(ColorArrow)
    index = 0
    index1 = 0
    if SeriesTest:
        index = _int(NumberofBar)
        index1 = index + 1
    else:
        index = Rates_total - _int(NumberofBar) - 1
        index1 = index - 1
    if ColorArrow[index] == 0 and ColorArrow[index1] != 0:
        BuySignal_ = True
    if BuySignal_ and _s_BuySignal_counter <= NumberofAlerts:
        _s_BuySignal_counter += 1
        tm = MqlDateTime()
        TimeToStruct(TimeCurrent(), tm)
        text = TimeToString(TimeCurrent(), TIME_DATE) + ' ' + _str(tm.hour) + ':' + _str(tm.min)
        SeriesTest = ArrayGetAsSeries(Close)
        if SeriesTest:
            index = _int(NumberofBar)
        else:
            index = Rates_total - _int(NumberofBar) - 1
        Ask = Close[index]
        Bid = Close[index]
        SeriesTest = ArrayGetAsSeries(Spread)
        if SeriesTest:
            index = _int(NumberofBar)
        else:
            index = Rates_total - _int(NumberofBar) - 1
        Bid += Spread[index] * Point()
        sAsk = DoubleToString(Ask, Digits())
        sBid = DoubleToString(Bid, Digits())
        sPeriod = GetStringTimeframe(ChartPeriod())
        if SoundON:
            Alert('BUY signal \n Ask=', Ask, '\n Bid=', Bid, '\n currtime=', text, '\n Symbol=', Symbol(), ' Period=', sPeriod)
        if EMailON:
            SendMail(SignalSirname + ': BUY signal alert', 'BUY signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
        if PushON:
            SendNotification(SignalSirname + ': BUY signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)

def SellSignal(SignalSirname, ColorArrow, Rates_total, Prev_calculated, Close, Spread):
    global _s_SellSignal_counter
    if Rates_total != Prev_calculated:
        _s_SellSignal_counter = 0
    SellSignal_ = False
    SeriesTest = ArrayGetAsSeries(ColorArrow)
    index = 0
    index1 = 0
    if SeriesTest:
        index = _int(NumberofBar)
        index1 = index + 1
    else:
        index = Rates_total - _int(NumberofBar) - 1
        index1 = index - 1
    if ColorArrow[index] == 4 and ColorArrow[index1] != 4:
        SellSignal_ = True
    if SellSignal_ and _s_SellSignal_counter <= NumberofAlerts:
        _s_SellSignal_counter += 1
        tm = MqlDateTime()
        TimeToStruct(TimeCurrent(), tm)
        text = TimeToString(TimeCurrent(), TIME_DATE) + ' ' + _str(tm.hour) + ':' + _str(tm.min)
        SeriesTest = ArrayGetAsSeries(Close)
        if SeriesTest:
            index = _int(NumberofBar)
        else:
            index = Rates_total - _int(NumberofBar) - 1
        Ask = Close[index]
        Bid = Close[index]
        SeriesTest = ArrayGetAsSeries(Spread)
        if SeriesTest:
            index = _int(NumberofBar)
        else:
            index = Rates_total - _int(NumberofBar) - 1
        Bid += Spread[index] * Point()
        sAsk = DoubleToString(Ask, Digits())
        sBid = DoubleToString(Bid, Digits())
        sPeriod = GetStringTimeframe(ChartPeriod())
        if SoundON:
            Alert('SELL signal \n Ask=', Ask, '\n Bid=', Bid, '\n currtime=', text, '\n Symbol=', Symbol(), ' Period=', sPeriod)
        if EMailON:
            SendMail(SignalSirname + ': SELL signal alert', 'SELL signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
        if PushON:
            SendNotification(SignalSirname + ': SELL signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

# ---- global variables initialised from expressions
XMAO = _alloc(CXMA)
XMAO.__init__()
XMAL = _alloc(CXMA)
XMAL.__init__()
XMAH = _alloc(CXMA)
XMAH.__init__()
XMAC = _alloc(CXMA)
XMAC.__init__()
XMA1 = _alloc(CXMA)
XMA1.__init__()
STD = _alloc(CStdDeviation)
STD.__init__()

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1
_s_BuySignal_counter = 0
_s_SellSignal_counter = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XPeriodCandleSystemAlert(_MQL5Indicator):
    name = 'XPeriodCandleSystem_Alert'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'period': 5,  # Период расчёта свечей
        'MA_SMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # Метод усреднения
        'MA_Length': 3,  # глубина сглаживания
        'MA_Phase': 100,  # параметр сглаживания,
        'BB_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=0),  # метод усреднения полос Боллинджера
        'BBLength': 20,  # глубина  усреднения полос Боллинджера
        'BBPhase': 15,  # параметр усреднения полос Боллинджера,
        'BandsDeviation': 1.001,  # девиация
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг свеч индикатора по горизонтали в барах влево
        'NumberofBar': 1,  # Номер бара для подачи сигнала
        'SoundON': True,  # Разрешение алерта
        'NumberofAlerts': 2,  # Количество алертов
        'EMailON': False,  # Разрешение почтовой отправки сигнала
        'PushON': False,  # Разрешение отправки сигнала на мобильный
    }

