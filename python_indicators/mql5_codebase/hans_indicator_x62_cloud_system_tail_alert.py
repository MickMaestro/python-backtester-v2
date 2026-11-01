"""Hans_Indicator_x62_Cloud_System_Tail_Alert — converted from MQL5: MQL5 Indicators/Hans_Indicator_x62_Cloud_System_Tail_Alert/Hans_Indicator_x62_Cloud_System_Tail_Alert.mq5

Индикатор расширяющихся коридоров временных зон с тридцатью одним коридором,  с фоновым цветовым заполнением, средней линией коридора,
с окрашиванием свечек при выходе из сформированного четырёхчасового коридора.
Сформированный коридор равен четырём часам, расширения коридора - шестнадцать часов.
Copyright: Copyright © 2014, Shimodax; Link: http://www.strategybuilderfx.com/forums/showthread.php?t=15439; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2014, Shimodax', 'link': 'http://www.strategybuilderfx.com/forums/showthread.php?t=15439', 'version': '1.02', 'window': 'chart', 'indicator_buffers': 74, 'indicator_plots': 68}, 'types': {1: 7, 2: 7, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 67: 1, 68: 17}, 'colors': {1: [15597514], 2: [16769535], 3: [16711680], 4: [16711935], 5: [65280], 6: [255], 7: [32768], 8: [8519755], 9: [32768], 10: [8519755], 11: [32768], 12: [8519755], 13: [32768], 14: [8519755], 67: [9470064], 68: [16760576, 16711680, 8421504, 8388736, 16711935]}, 'widths': {3: 1, 4: 1, 5: 3, 6: 3, 7: 3, 8: 3, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 67: 2}, 'styles': {3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 1, 10: 1, 11: 4, 12: 4, 13: 0, 14: 0, 67: 0}, 'labels': {1: 'Upper Hans_Indicator_x62 cloud', 2: 'Lower Hans_Indicator_x62 cloud', 3: 'Upper Hans_Indicator 1', 4: 'Lower Hans_Indicator 1', 5: 'Upper Hans_Indicator 2', 6: 'Lower Hans_Indicator 2', 7: 'Upper Hans_Indicator 3', 8: 'Lower Hans_Indicator 3', 9: 'Upper Hans_Indicator 4', 10: 'Lower Hans_Indicator 4', 11: 'Upper Hans_Indicator 5', 12: 'Lower Hans_Indicator 5', 13: 'Upper Hans_Indicator 6', 14: 'Lower Hans_Indicator 6', 67: 'Middle Hans_Indicator', 68: 'Hans_Indicator Open;Hans_Indicator High;Hans_Indicator Low;Hans_Indicator Close'}, 'levels': [], 'description': ['Индикатор расширяющихся коридоров временных зон с тридцатью одним коридором,  с фоновым цветовым заполнением, средней линией коридора,', 'с окрашиванием свечек при выходе из сформированного четырёхчасового коридора.', 'Сформированный коридор равен четырём часам, расширения коридора - шестнадцать часов.'], 'name': 'Hans_Indicator_x62_Cloud_System_Tail_Alert', 'source': 'MQL5 Indicators/Hans_Indicator_x62_Cloud_System_Tail_Alert/Hans_Indicator_x62_Cloud_System_Tail_Alert.mq5', 'folder': 'Hans_Indicator_x62_Cloud_System_Tail_Alert', 'inputs': [{'mql': 'LocalTimeZone', 'py': 'LocalTimeZone', 'param': 'LocalTimeZone', 'type': 'uint', 'default': 0, 'label': 'час начала отсчёта исходного коридора', 'sinput': False}, {'mql': 'DestTimeZone', 'py': 'DestTimeZone', 'param': 'DestTimeZone', 'type': 'uint', 'default': 4, 'label': 'сдвиг коридора влево в барах', 'sinput': False}, {'mql': 'PipsForEntryStep', 'py': 'PipsForEntryStep', 'param': 'PipsForEntryStep', 'type': 'uint', 'default': 50, 'label': 'шаг расширения границ каждого сформированного коридора в пунктах', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Draw_Tail', 'py': 'Draw_Tail', 'param': 'Draw_Tail', 'type': 'bool', 'default': True, 'label': 'Разрешение дорисовки уровней до конца ссесии', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для подачи сигнала', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Разрешение алерта', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': 'Количество алертов', 'sinput': False}, {'mql': 'EMailON', 'py': 'EMailON', 'param': 'EMailON', 'type': 'bool', 'default': False, 'label': 'Разрешение почтовой отправки сигнала', 'sinput': False}, {'mql': 'PushON', 'py': 'PushON', 'param': 'PushON', 'type': 'bool', 'default': False, 'label': 'Разрешение отправки сигнала на мобильный', 'sinput': False}, {'mql': 'Slip', 'py': 'Slip', 'param': 'Slip', 'type': 'uint', 'default': 0, 'label': 'Смещение координатной сетки по вертикали на PipsForEntryStep от середины', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
LocalTimeZone = _input('LocalTimeZone', 0)  # час начала отсчёта исходного коридора
DestTimeZone = _input('DestTimeZone', 4)  # сдвиг коридора влево в барах
PipsForEntryStep = _input('PipsForEntryStep', 50)  # шаг расширения границ каждого сформированного коридора в пунктах
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
Draw_Tail = _input('Draw_Tail', True)  # Разрешение дорисовки уровней до конца ссесии
NumberofBar = _input('NumberofBar', 1)  # Номер бара для подачи сигнала
SoundON = _input('SoundON', True)  # Разрешение алерта
NumberofAlerts = _input('NumberofAlerts', 2)  # Количество алертов
EMailON = _input('EMailON', False)  # Разрешение почтовой отправки сигнала
PushON = _input('PushON', False)  # Разрешение отправки сигнала на мобильный
Slip = _input('Slip', 0)  # Смещение координатной сетки по вертикали на PipsForEntryStep от середины
UpUpBuffer = Arr(0, 0.0)
UpDnBuffer = Arr(0, 0.0)
DnUpBuffer = Arr(0, 0.0)
DnDnBuffer = Arr(0, 0.0)
MiddleBuffer = Arr(0, 0.0)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0

class CIndicatorsBuffers(MqlObject):
    _q_fields = ('ZoneUpper', 'ZoneLower')
    def __init__(self, *args):
        self.ZoneUpper = Arr(0, 0.0)
        self.ZoneLower = Arr(0, 0.0)

def OnInit():
    global min_rates_total
    min_rates_total = 100
    line_style = Arr(0, 0)
    line_color = Arr(0, 0)
    line_width = Arr(0, 0)
    plot_type = Arr(0, 0)
    size = 10
    ArrayResize(line_style, size)
    ArrayResize(line_color, size)
    ArrayResize(line_width, size)
    ArrayResize(plot_type, size)
    ArrayResize(Ind, 32)
    for plot in range(4, 14):
        plot_type[plot - 4] = PlotIndexGetInteger(plot, PLOT_DRAW_TYPE)
        line_style[plot - 4] = PlotIndexGetInteger(plot, PLOT_LINE_STYLE)
        line_width[plot - 4] = PlotIndexGetInteger(plot, PLOT_LINE_WIDTH)
        line_color[plot - 4] = _uint(PlotIndexGetInteger(plot, PLOT_LINE_COLOR))
    for step in range(0, 5):
        for count in range(0, 10):
            number = 14 + (10 * step) + count
            PlotIndexSetInteger(number, PLOT_DRAW_TYPE, plot_type[count])
            PlotIndexSetInteger(number, PLOT_LINE_STYLE, line_style[count])
            PlotIndexSetInteger(number, PLOT_LINE_WIDTH, line_width[count])
            PlotIndexSetInteger(number, PLOT_LINE_COLOR, line_color[count])
    for count in range(0, 2):
        number = 64 + count
        PlotIndexSetInteger(number, PLOT_DRAW_TYPE, plot_type[count])
        PlotIndexSetInteger(number, PLOT_LINE_STYLE, line_style[count])
        PlotIndexSetInteger(number, PLOT_LINE_WIDTH, line_width[count])
        PlotIndexSetInteger(number, PLOT_LINE_COLOR, line_color[count])
    for count in range(0, 32 - 6):
        PlotIndexSetString(14 + (2 * count), PLOT_LABEL, 'Upper Hans_Indicator ' + _str(7 + count))
        PlotIndexSetString(15 + (2 * count), PLOT_LABEL, 'Lower Hans_Indicator ' + _str(7 + count))
    IndBufferInit(0, UpUpBuffer)
    IndBufferInit(1, UpDnBuffer)
    IndBufferInit(2, DnUpBuffer)
    IndBufferInit(3, DnDnBuffer)
    for numb in range(0, 32):
        IndBufferInit(4 + (2 * numb), Ind[numb].ZoneUpper)
        IndBufferInit(5 + (2 * numb), Ind[numb].ZoneLower)
    IndBufferInit(4 + (2 * 32), MiddleBuffer)
    IndBufferInit(5 + (2 * 32), ExtOpenBuffer)
    IndBufferInit(6 + (2 * 32), ExtHighBuffer)
    IndBufferInit(7 + (2 * 32), ExtLowBuffer)
    IndBufferInit(8 + (2 * 32), ExtCloseBuffer)
    IndBufferInit(9 + (2 * 32), ExtColorBuffer)
    for count in range(0, 2):
        IndInit(count, EMPTY_VALUE, min_rates_total, Shift)
    for count in range(2, (2 * 32) + 6):
        IndInit(count, 0.0, min_rates_total, Shift)
    IndicatorSetString(INDICATOR_SHORTNAME, 'Hans_Indicator_x62_Cloud_System_Tail_Alert(' + _str(LocalTimeZone) + ',' + _str(DestTimeZone) + ',' + _str(PipsForEntryStep) + ',' + _str(Shift) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def IndBufferInit(BuffNumber, Buffer):
    SetIndexBuffer(BuffNumber, Buffer, INDICATOR_DATA)
    ArraySetAsSeries(Buffer, True)

def IndCldInit(PlotNumber, Draw_Begin, nShift):
    PlotIndexSetInteger(PlotNumber, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetInteger(PlotNumber, PLOT_SHIFT, nShift)
    PlotIndexSetInteger(PlotNumber, PLOT_SHOW_DATA, False)

def IndInit(PlotNumber, Empty_Value, Draw_Begin, nShift):
    PlotIndexSetInteger(PlotNumber, PLOT_DRAW_BEGIN, Draw_Begin)
    PlotIndexSetDouble(PlotNumber, PLOT_EMPTY_VALUE, Empty_Value)
    PlotIndexSetInteger(PlotNumber, PLOT_SHIFT, nShift)
    PlotIndexSetInteger(PlotNumber, PLOT_SHOW_DATA, False)

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if rates_total < min_rates_total:
        return 0
    limit = Box(0)
    limit1 = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit1 = rates_total - min_rates_total - 1
        limit.v = limit1
    else:
        limit1 = rates_total - prev_calculated
        limit.v = limit1
    ArraySetAsSeries(Time, True)
    ArraySetAsSeries(Open, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Close, True)
    BreakoutRanges(0, limit, LocalTimeZone, DestTimeZone, rates_total, Time, Open, High, Low, Close)
    if Draw_Tail:
        last_tail = FindLastTail(rates_total, Open, High, Low, Close, limit1)
        if last_tail > 0:
            limit1 = last_tail
        for bar in range(limit1, 0 - 1, -1):
            if not Ind[0].ZoneUpper[bar]:
                for numb in range(1, 32):
                    Ind[numb].ZoneUpper[bar] = Ind[numb].ZoneUpper[bar + 1]
                    Ind[numb].ZoneLower[bar] = Ind[numb].ZoneLower[bar + 1]
                MiddleBuffer[bar] = MiddleBuffer[bar + 1]
                ExtCloseBuffer[bar] = 0.0
                ExtLowBuffer[bar] = ExtCloseBuffer[bar]
                ExtHighBuffer[bar] = ExtLowBuffer[bar]
                ExtOpenBuffer[bar] = ExtHighBuffer[bar]
                ExtColorBuffer[bar] = 2.0
                if Close[bar] > Ind[1].ZoneUpper[bar]:
                    ExtOpenBuffer[bar] = Open[bar]
                    ExtHighBuffer[bar] = High[bar]
                    ExtLowBuffer[bar] = Low[bar]
                    ExtCloseBuffer[bar] = Close[bar]
                    if Close[bar] >= Open[bar]:
                        ExtColorBuffer[bar] = 0.0
                    else:
                        ExtColorBuffer[bar] = 1.0
                if Close[bar] < Ind[1].ZoneLower[bar]:
                    ExtOpenBuffer[bar] = Open[bar]
                    ExtHighBuffer[bar] = High[bar]
                    ExtLowBuffer[bar] = Low[bar]
                    ExtCloseBuffer[bar] = Close[bar]
                    if Close[bar] <= Open[bar]:
                        ExtColorBuffer[bar] = 4.0
                    else:
                        ExtColorBuffer[bar] = 3.0
            if Ind[0].ZoneUpper[bar]:
                if not Ind[0].ZoneUpper[bar + 1]:
                    MiddleBuffer[bar + 1] = 0.0
                    for numb in range(1, 32):
                        Ind[numb].ZoneLower[bar] = 0.0
                        Ind[numb].ZoneUpper[bar] = Ind[numb].ZoneLower[bar]
    BuySignal('Hans_Indicator_x62_Cloud_System_Tail_Alert', ExtColorBuffer, rates_total, prev_calculated, Close, Spread)
    SellSignal('Hans_Indicator_x62_Cloud_System_Tail_Alert', ExtColorBuffer, rates_total, prev_calculated, Close, Spread)
    return rates_total

def FindLastTail(Rates_Total, Open_, High_, Low_, Close_, nShift):
    for bar in range(nShift, Rates_Total):
        if not Ind[0].ZoneUpper[bar]:
            for index in range(bar, Rates_Total):
                if Ind[0].ZoneUpper[index]:
                    return index
    return -1

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
    if ColorArrow[index] < 2 and ColorArrow[index1] > 1:
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
    if ColorArrow[index] > 2 and ColorArrow[index1] < 3:
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

def BreakoutRanges(offset, lastbar, tzlocal, tzdest, rates_total_, Time_, Open_, High_, Low_, Close_):
    i = 0
    j = 0
    k = 0
    tzdiff = tzlocal - tzdest
    tzdiffsec = tzdiff * 3600
    tidxstart = Arr.of([0, 0], fill=0, dyn=False, size=2)
    tidxend = Arr.of([0, 0], fill=0, dyn=False, size=2)
    thigh = Arr.of([0.0, 0.0], fill=0.0, dyn=False, size=2)
    tlow = Arr.of([DBL_MAX], fill=0.0, dyn=False, size=2)
    tfrom = Arr.of(['04:00', '08:00', '12:00'], fill="", dyn=False, size=3)
    tto = Arr.of(['08:00', '12:00', '24:00'], fill="", dyn=False, size=3)
    tday = ""
    inperiod = (-1 != 0)
    timet = 0
    tday = TimeToString(Time_[lastbar.v] - tzdiffsec, TIME_DATE)
    while lastbar.v < (rates_total_ - 1):
        if TimeToString(Time_[lastbar.v] - tzdiffsec, TIME_DATE) != tday:
            lastbar.v -= 1
            break
        lastbar.v += 1
    tday = 'XXX'
    i = lastbar.v
    for i in range(i, offset - 1, -1):
        timet = Time_[i] - tzdiffsec
        timestr = TimeToString(timet, TIME_MINUTES)
        thisday = TimeToString(timet, TIME_DATE)
        j = 0
        for j in range(j, 2):
            if tfrom[j] <= timestr and timestr < tto[j]:
                if inperiod != j:
                    if j > 0:
                        k = tidxstart[j - 1]
                        while k >= tidxend[j - 1]:
                            ExtCloseBuffer[k] = 0.0
                            ExtLowBuffer[k] = ExtCloseBuffer[k]
                            ExtHighBuffer[k] = ExtLowBuffer[k]
                            ExtOpenBuffer[k] = ExtHighBuffer[k]
                            ExtColorBuffer[k] = 2.0
                            if (j - 1) == 0:
                                Ind[0].ZoneUpper[k] = thigh[j - 1]
                                Ind[0].ZoneLower[k] = tlow[j - 1]
                                MiddleBuffer[k] = (Ind[0].ZoneUpper[k] + Ind[0].ZoneLower[k]) / 2
                                if Close_[k] > Ind[0].ZoneUpper[k]:
                                    ExtOpenBuffer[k] = Open_[k]
                                    ExtHighBuffer[k] = High_[k]
                                    ExtLowBuffer[k] = Low_[k]
                                    ExtCloseBuffer[k] = Close_[k]
                                    if Close_[k] >= Open_[k]:
                                        ExtColorBuffer[k] = 0.0
                                    else:
                                        ExtColorBuffer[k] = 1.0
                                if Close_[k] < Ind[0].ZoneLower[k]:
                                    ExtOpenBuffer[k] = Open_[k]
                                    ExtHighBuffer[k] = High_[k]
                                    ExtLowBuffer[k] = Low_[k]
                                    ExtCloseBuffer[k] = Close_[k]
                                    if Close_[k] <= Open_[k]:
                                        ExtColorBuffer[k] = 4.0
                                    else:
                                        ExtColorBuffer[k] = 3.0
                            if (j - 1) == 1:
                                Ind[1].ZoneUpper[k] = thigh[j - 1]
                                Ind[1].ZoneLower[k] = tlow[j - 1]
                                MiddleBuffer[k] = (Ind[1].ZoneUpper[k] + Ind[1].ZoneLower[k]) / 2
                                if Close_[k] > Ind[1].ZoneUpper[k]:
                                    ExtOpenBuffer[k] = Open_[k]
                                    ExtHighBuffer[k] = High_[k]
                                    ExtLowBuffer[k] = Low_[k]
                                    ExtCloseBuffer[k] = Close_[k]
                                    if Close_[k] >= Open_[k]:
                                        ExtColorBuffer[k] = 0.0
                                    else:
                                        ExtColorBuffer[k] = 1.0
                                if Close_[k] < Ind[1].ZoneLower[k]:
                                    ExtOpenBuffer[k] = Open_[k]
                                    ExtHighBuffer[k] = High_[k]
                                    ExtLowBuffer[k] = Low_[k]
                                    ExtCloseBuffer[k] = Close_[k]
                                    if Close_[k] <= Open_[k]:
                                        ExtColorBuffer[k] = 4.0
                                    else:
                                        ExtColorBuffer[k] = 3.0
                            k -= 1
                    inperiod = (j != 0)
                if inperiod == 2:
                    break
                if tidxstart[j] == 0:
                    tidxstart[j] = i
                    tday = thisday
                tidxend[j] = i
                thigh[j] = MathMax(thigh[j], High_[i])
                tlow[j] = MathMin(tlow[j], Low_[i])
        else:
            j = _range_end(j, 2, 1)
        if inperiod >= 1 and tday == thisday:
            for numb in range(1, 32):
                Ind[numb].ZoneUpper[i] = thigh[0] + (numb * PipsForEntryStep * Point())
                Ind[numb].ZoneLower[i] = tlow[0] - (numb * PipsForEntryStep * Point())
            Ind[0].ZoneUpper[i] = Ind[1].ZoneUpper[i]
            Ind[0].ZoneLower[i] = Ind[1].ZoneLower[i]
            for numb in range(1, 32):
                Ind[numb].ZoneUpper[i] += Slip * PipsForEntryStep * Point()
                Ind[numb].ZoneLower[i] -= Slip * PipsForEntryStep * Point()
            DnUpBuffer[i] = (Ind[0].ZoneUpper[i] + Ind[0].ZoneLower[i]) / 2
            UpDnBuffer[i] = DnUpBuffer[i]
            MiddleBuffer[i] = UpDnBuffer[i]
            UpUpBuffer[i] = Ind[32 - 1].ZoneUpper[i]
            DnDnBuffer[i] = Ind[32 - 1].ZoneLower[i]
            ExtCloseBuffer[i] = 0.0
            ExtLowBuffer[i] = ExtCloseBuffer[i]
            ExtHighBuffer[i] = ExtLowBuffer[i]
            ExtOpenBuffer[i] = ExtHighBuffer[i]
            ExtColorBuffer[i] = 2.0
            if Close_[i] > Ind[0].ZoneUpper[i]:
                ExtOpenBuffer[i] = Open_[i]
                ExtHighBuffer[i] = High_[i]
                ExtLowBuffer[i] = Low_[i]
                ExtCloseBuffer[i] = Close_[i]
                if Close_[i] >= Open_[i]:
                    ExtColorBuffer[i] = 0.0
                else:
                    ExtColorBuffer[i] = 1.0
            if Close_[i] < Ind[0].ZoneLower[i]:
                ExtOpenBuffer[i] = Open_[i]
                ExtHighBuffer[i] = High_[i]
                ExtLowBuffer[i] = Low_[i]
                ExtCloseBuffer[i] = Close_[i]
                if Close_[i] <= Open_[i]:
                    ExtColorBuffer[i] = 4.0
                else:
                    ExtColorBuffer[i] = 3.0
        else:
            Ind[0].ZoneUpper[i] = 0.0
            Ind[0].ZoneLower[i] = 0.0
            for numb in range(0, 32):
                Ind[numb].ZoneUpper[i] = 0.0
                Ind[numb].ZoneLower[i] = 0.0
            DnDnBuffer[i] = 0.0
            UpUpBuffer[i] = DnDnBuffer[i]
            DnUpBuffer[i] = UpUpBuffer[i]
            UpDnBuffer[i] = DnUpBuffer[i]
            MiddleBuffer[i] = UpDnBuffer[i]
            ExtCloseBuffer[i] = 0.0
            ExtLowBuffer[i] = ExtCloseBuffer[i]
            ExtHighBuffer[i] = ExtLowBuffer[i]
            ExtOpenBuffer[i] = ExtHighBuffer[i]
            ExtColorBuffer[i] = 2.0
        if tday != 'XXX' and tday != thisday:
            tday = 'XXX'
            inperiod = (-1 != 0)
            j = 0
            for j in range(j, 2):
                tidxstart[j] = 0
                tidxend[j] = 0
                thigh[j] = 0.0
                tlow[j] = 99999.0
            else:
                j = _range_end(j, 2, 1)
    else:
        i = _range_end(i, offset - 1, -1)
    return 0

# ---- global variables initialised from expressions
Ind = Arr(0, 0, factory=CIndicatorsBuffers)

# ---- static local variables
_s_BuySignal_counter = 0
_s_SellSignal_counter = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class HansIndicatorX62CloudSystemTailAlert(_MQL5Indicator):
    name = 'Hans_Indicator_x62_Cloud_System_Tail_Alert'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'LocalTimeZone': 0,  # час начала отсчёта исходного коридора
        'DestTimeZone': 4,  # сдвиг коридора влево в барах
        'PipsForEntryStep': 50,  # шаг расширения границ каждого сформированного коридора в пунктах
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'Draw_Tail': True,  # Разрешение дорисовки уровней до конца ссесии
        'NumberofBar': 1,  # Номер бара для подачи сигнала
        'SoundON': True,  # Разрешение алерта
        'NumberofAlerts': 2,  # Количество алертов
        'EMailON': False,  # Разрешение почтовой отправки сигнала
        'PushON': False,  # Разрешение отправки сигнала на мобильный
        'Slip': 0,  # Смещение координатной сетки по вертикали на PipsForEntryStep от середины
    }

