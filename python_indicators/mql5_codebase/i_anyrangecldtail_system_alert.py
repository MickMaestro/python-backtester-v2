"""i-AnyRangeCldTail_System_Alert — converted from MQL5: MQL5 Indicators/i-AnyRangeCldTail_System_Alert/i-AnyRangeCldTail_System_Alert.mq5

Индикатор диапазонов произвольных временных интервалов
Copyright: Copyright © 2006, Ким Игорь В. aka KimIV; Link: http://www.kimiv.ru; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Ким Игорь В. aka KimIV', 'link': 'http://www.kimiv.ru', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 13, 'indicator_plots': 7}, 'types': {1: 7, 2: 1, 3: 1, 4: 7, 5: 1, 6: 1, 7: 17}, 'colors': {1: [16443110], 2: [16711680], 3: [255], 4: [16118015], 5: [16711680], 6: [255], 7: [9639167, 8388736, 8421376, 13749760]}, 'widths': {2: 3, 3: 3, 5: 1, 6: 1}, 'styles': {1: 0, 3: 0, 5: 4, 6: 4}, 'labels': {1: 'i-AnyRange', 2: 'Upper Zone', 3: 'Lower Zone', 4: 'i-AnyRange tail', 5: 'Upper Zone  tail', 6: 'Lower Zone  tail', 7: 'i-AnyRange_Open;i-AnyRange_High;i-AnyRange_Low;i-AnyRange_Close'}, 'levels': [], 'description': ['Индикатор диапазонов произвольных временных интервалов'], 'name': 'i-AnyRangeCldTail_System_Alert', 'source': 'MQL5 Indicators/i-AnyRangeCldTail_System_Alert/i-AnyRangeCldTail_System_Alert.mq5', 'folder': 'i-AnyRangeCldTail_System_Alert', 'inputs': [{'mql': 'Time1', 'py': 'Time1', 'param': None, 'type': 'string', 'default': '02:00', 'label': 'Временная точка 1', 'sinput': False}, {'mql': 'Time2', 'py': 'Time2', 'param': None, 'type': 'string', 'default': '07:00', 'label': 'Временная точка 2', 'sinput': False}, {'mql': 'nDays', 'py': 'nDays', 'param': 'nDays', 'type': 'uint', 'default': 8, 'label': 'Количество дней обсчёта (0-все)', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для подачи сигнала', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Разрешение алерта', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': 'Количество алертов', 'sinput': False}, {'mql': 'EMailON', 'py': 'EMailON', 'param': 'EMailON', 'type': 'bool', 'default': False, 'label': 'Разрешение почтовой отправки сигнала', 'sinput': False}, {'mql': 'PushON', 'py': 'PushON', 'param': 'PushON', 'type': 'bool', 'default': False, 'label': 'Разрешение отправки сигнала на мобильный', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Time1 = _input('Time1', '02:00')  # Временная точка 1
Time2 = _input('Time2', '07:00')  # Временная точка 2
nDays = _input('nDays', 8)  # Количество дней обсчёта (0-все)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
NumberofBar = _input('NumberofBar', 1)  # Номер бара для подачи сигнала
SoundON = _input('SoundON', True)  # Разрешение алерта
NumberofAlerts = _input('NumberofAlerts', 2)  # Количество алертов
EMailON = _input('EMailON', False)  # Разрешение почтовой отправки сигнала
PushON = _input('PushON', False)  # Разрешение отправки сигнала на мобильный
Up0Buffer = Arr(0, 0.0)
Dn0Buffer = Arr(0, 0.0)
Up1Buffer = Arr(0, 0.0)
Dn1Buffer = Arr(0, 0.0)
Up2Buffer = Arr(0, 0.0)
Dn2Buffer = Arr(0, 0.0)
Up3Buffer = Arr(0, 0.0)
Dn3Buffer = Arr(0, 0.0)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
Max = 0

def OnInit():
    global Max, min_rates_total
    min_rates_total = _int(_idiv(24 * 60 * 60 * nDays, PeriodSeconds()) + 1)
    Max = _int(_idiv(nDays * 1440 * 60, PeriodSeconds()))
    SetIndexBuffer(0, Up0Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Up0Buffer, True)
    SetIndexBuffer(1, Dn0Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Dn0Buffer, True)
    SetIndexBuffer(2, Up1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Up1Buffer, True)
    SetIndexBuffer(3, Dn1Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Dn1Buffer, True)
    SetIndexBuffer(4, Up2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(Up2Buffer, True)
    SetIndexBuffer(5, Dn2Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Dn2Buffer, True)
    SetIndexBuffer(6, Up3Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Up3Buffer, True)
    SetIndexBuffer(7, Dn3Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(Dn3Buffer, True)
    SetIndexBuffer(8, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(9, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(10, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(11, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(12, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, None)
    PlotIndexSetInteger(6, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(6, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'i-AnyRangeCldTail_System(', Time1, ', ', Time2, ', ', nDays, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnDeinit(reason):
    Comment('')

def iBarShift_u(symbol, timeframe, time):
    if time < 0:
        return -1
    Arr_ = Arr(0, 0)
    time1 = 0
    time1 = SeriesInfoInteger(symbol, timeframe, SERIES_LASTBAR_DATE)
    if time >= time1:
        return 0
    if CopyTime(symbol, timeframe, _DT(time), _DT(time1), Arr_) > 0:
        size = ArraySize(Arr_)
        return size - 1
    else:
        return -1

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if Period() > PERIOD_H1:
        Comment('Индикатору i-AnyRange нужен ТФ младше H4!')
        return 0
    else:
        Comment('')
    if rates_total < min_rates_total:
        return 0
    up = 0.0
    dn = 0.0
    bar = 0
    limit = 0
    kd = 0
    nb1 = 0
    nb2 = 0
    nd = 0
    rates_10 = 0
    sdt = ""
    rates_10 = rates_total - 10
    if nDays == 0:
        limit = rates_10
    else:
        limit = Max
    limit = MathMin(rates_10, limit)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, rates_total - limit)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, rates_total - limit)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, rates_total - limit)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, rates_total - limit)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, rates_total - limit)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, rates_total - limit)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, rates_total - limit)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(time, True)
    bar = 0
    for bar in range(bar, limit):
        Up0Buffer[bar] = 0.0
        Dn0Buffer[bar] = 0.0
        Up1Buffer[bar] = EMPTY_VALUE
        Dn1Buffer[bar] = EMPTY_VALUE
    else:
        bar = _range_end(bar, limit, 1)
    bar = 0
    for bar in range(bar, limit):
        Up1Buffer[bar] = EMPTY_VALUE
        Dn1Buffer[bar] = EMPTY_VALUE
        tm = MqlDateTime()
        TimeToStruct(time[bar], tm)
        if nd != tm.day:
            nd = tm.day
            kd += 1
            if kd > _int(nDays) and nDays:
                break
            sdt = TimeToString(time[bar], TIME_DATE)
            nb1 = iBarShift_u("", 0, StringToTime(sdt + ' ' + Time1))
            nb2 = iBarShift_u("", 0, StringToTime(sdt + ' ' + Time2))
            if nb1 > (nb2 + 1):
                up = high[ArrayMaximum(high, nb2 + 1, nb1 - nb2)]
                dn = low[ArrayMinimum(low, nb2 + 1, nb1 - nb2)]
            if nb2 > (nb1 + 1):
                up = high[ArrayMaximum(high, nb1 + 1, nb2 - nb1)]
                dn = low[ArrayMinimum(low, nb1 + 1, nb2 - nb1)]
        if (nb1 >= bar and bar > nb2) or (nb2 >= bar and bar > nb1):
            Up1Buffer[bar] = up
            Dn1Buffer[bar] = dn
            Up0Buffer[bar] = up
            Dn0Buffer[bar] = dn
        else:
            Up1Buffer[bar] = EMPTY_VALUE
            Dn1Buffer[bar] = EMPTY_VALUE
    else:
        bar = _range_end(bar, limit, 1)
    bar = 0
    for bar in range(bar, limit):
        if Up1Buffer[bar] == EMPTY_VALUE and Dn1Buffer[bar] == EMPTY_VALUE:
            Up0Buffer[bar] = 0.0
            Dn0Buffer[bar] = 0.0
    else:
        bar = _range_end(bar, limit, 1)
    dn = EMPTY_VALUE
    up = dn
    bar = limit - 1
    for bar in range(bar, 0 - 1, -1):
        Up2Buffer[bar] = 0.0
        Dn2Buffer[bar] = 0.0
        Up3Buffer[bar] = EMPTY_VALUE
        Dn3Buffer[bar] = EMPTY_VALUE
        if Up0Buffer[bar]:
            up = Up0Buffer[bar]
            dn = Dn0Buffer[bar]
        else:
            Up3Buffer[bar] = up
            Up2Buffer[bar] = Up3Buffer[bar]
            Dn3Buffer[bar] = dn
            Dn2Buffer[bar] = Dn3Buffer[bar]
            bar1 = bar + 1
            if Up0Buffer[bar1]:
                Up3Buffer[bar1] = up
                Up2Buffer[bar1] = Up3Buffer[bar1]
                Dn3Buffer[bar1] = dn
                Dn2Buffer[bar1] = Dn3Buffer[bar1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    bar = limit - 1
    for bar in range(bar, 0 - 1, -1):
        ExtLowBuffer[bar] = 0.0
        ExtHighBuffer[bar] = ExtLowBuffer[bar]
        ExtCloseBuffer[bar] = ExtHighBuffer[bar]
        ExtOpenBuffer[bar] = ExtCloseBuffer[bar]
        ExtColorBuffer[bar] = 4.0
        if Up2Buffer[bar] and close[bar] > Up2Buffer[bar]:
            ExtOpenBuffer[bar] = open[bar]
            ExtCloseBuffer[bar] = close[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
            if close[bar] >= open[bar]:
                ExtColorBuffer[bar] = 3.0
            else:
                ExtColorBuffer[bar] = 2.0
        if Dn2Buffer[bar] and close[bar] < Dn2Buffer[bar]:
            ExtOpenBuffer[bar] = open[bar]
            ExtCloseBuffer[bar] = close[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
            if close[bar] <= open[bar]:
                ExtColorBuffer[bar] = 0.0
            else:
                ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    BuySignal('i-AnyRangeCldTail_System_Alert', ExtColorBuffer, rates_total, prev_calculated, close, spread)
    SellSignal('i-AnyRangeCldTail_System_Alert', ExtColorBuffer, rates_total, prev_calculated, close, spread)
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
    if (ColorArrow[index] != 4 and ColorArrow[index] > 1) and (ColorArrow[index1] < 2 or ColorArrow[index1] == 4):
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
    if ColorArrow[index] < 2 and ColorArrow[index1] > 1:
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

# ---- static local variables
_s_BuySignal_counter = 0
_s_SellSignal_counter = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IAnyRangeCldTailSystemAlert(_MQL5Indicator):
    name = 'i-AnyRangeCldTail_System_Alert'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'nDays': 8,  # Количество дней обсчёта (0-все)
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'NumberofBar': 1,  # Номер бара для подачи сигнала
        'SoundON': True,  # Разрешение алерта
        'NumberofAlerts': 2,  # Количество алертов
        'EMailON': False,  # Разрешение почтовой отправки сигнала
        'PushON': False,  # Разрешение отправки сигнала на мобильный
    }

