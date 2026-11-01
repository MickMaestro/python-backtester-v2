"""FractalLevels_System — converted from MQL5: MQL5 Indicators/FractalLevels_System/FractalLevels_System.mq5

Fractal Levels
Copyright: Copyright © 2008, lotos4u; Link: lotos4u@gmail.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, lotos4u', 'link': 'lotos4u@gmail.com', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 13, 'indicator_plots': 8}, 'types': {1: 7, 2: 1, 3: 1, 4: 5, 5: 5, 6: 5, 7: 5, 8: 17}, 'colors': {1: [16443110], 2: [16748574], 3: [13850042], 4: [65280], 5: [255], 6: [16711680], 7: [8388736], 8: [65407, 8421376, 8388736, 16711935]}, 'widths': {2: 1, 3: 1, 4: 2, 5: 2, 6: 3, 7: 3}, 'styles': {2: 0, 3: 0}, 'labels': {1: 'FractalLevels Cloud', 2: 'Фрактальное сопротивление', 3: 'Фрактальное поддержка', 4: 'Фрактал ВЕРХ', 5: 'Фрактал ВНИЗ', 6: 'Пробой ВВЕРХ', 7: 'Пробой ВНИЗ', 8: 'Zigzag2_R_channel_Candle'}, 'levels': [], 'description': ['Fractal Levels'], 'name': 'FractalLevels_System', 'source': 'MQL5 Indicators/FractalLevels_System/FractalLevels_System.mq5', 'folder': 'FractalLevels_System', 'inputs': [{'mql': 'LeftBars_', 'py': 'LeftBars_', 'param': 'LeftBars_', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'RightBars_', 'py': 'RightBars_', 'param': 'RightBars_', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для подачи сигнала', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Разрешение алерта', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': 'Количество алертов', 'sinput': False}, {'mql': 'EMailON', 'py': 'EMailON', 'param': 'EMailON', 'type': 'bool', 'default': False, 'label': 'Разрешение почтовой отправки сигнала', 'sinput': False}, {'mql': 'PushON', 'py': 'PushON', 'param': 'PushON', 'type': 'bool', 'default': False, 'label': 'Разрешение отправки сигнала на мобильный', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
LeftBars_ = _input('LeftBars_', 3)
RightBars_ = _input('RightBars_', 3)
NumberofBar = _input('NumberofBar', 1)  # Номер бара для подачи сигнала
SoundON = _input('SoundON', True)  # Разрешение алерта
NumberofAlerts = _input('NumberofAlerts', 2)  # Количество алертов
EMailON = _input('EMailON', False)  # Разрешение почтовой отправки сигнала
PushON = _input('PushON', False)  # Разрешение отправки сигнала на мобильный
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
LineUpBuffer = Arr(0, 0.0)
LineDownBuffer = Arr(0, 0.0)
ArrowUpBuffer = Arr(0, 0.0)
ArrowDownBuffer = Arr(0, 0.0)
ArrowBreakUpBuffer = Arr(0, 0.0)
ArrowBreakDownBuffer = Arr(0, 0.0)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
min_rates_total = 0
LeftBars = 0
RightBars = 0

def OnInit():
    global LeftBars, RightBars, min_rates_total
    LeftBars = LeftBars_
    RightBars = RightBars_
    if LeftBars < 2:
        LeftBars = 2
    if RightBars < 2:
        RightBars = 2
    min_rates_total = _int(LeftBars + RightBars + 1)
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(UpBuffer, True)
    ArraySetAsSeries(DnBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(2, LineUpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(LineUpBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(3, LineDownBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(LineDownBuffer, True)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(4, ArrowUpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, 119)
    ArraySetAsSeries(ArrowUpBuffer, True)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(5, ArrowDownBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_ARROW, 119)
    ArraySetAsSeries(ArrowDownBuffer, True)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(6, ArrowBreakUpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(5, PLOT_ARROW, 108)
    ArraySetAsSeries(ArrowBreakUpBuffer, True)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(7, ArrowBreakDownBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(6, PLOT_ARROW, 108)
    ArraySetAsSeries(ArrowBreakDownBuffer, True)
    PlotIndexSetDouble(6, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(8, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(9, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(10, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(11, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(12, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'Fractal Levels'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def isFractalUp(index, lBars, rBars, High):
    start = index - rBars
    end = index + lBars + 1
    max_ = High[index]
    for i in range(start, end):
        if max_ < High[i] and i != index:
            if max_ < High[i]:
                return 0.0
            if MathAbs(i - index) > 1:
                return 0.0
    return max_

def isFractalDown(index, lBars, rBars, Low):
    start = index - rBars
    end = index + lBars + 1
    min_ = Low[index]
    for i in range(start, end):
        if min_ > Low[i] and i != index:
            if min_ > Low[i]:
                return 0.0
            if MathAbs(i - index) > 1:
                return 0.0
    return min_

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated + min_rates_total
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ArrowUpBuffer[bar] = 0.0
        ArrowDownBuffer[bar] = 0.0
        ArrowBreakUpBuffer[bar] = 0.0
        ArrowBreakDownBuffer[bar] = 0.0
        if bar < _int(RightBars):
            UpBuffer[bar] = LineUpBuffer[bar + 1]
            LineUpBuffer[bar] = UpBuffer[bar]
            DnBuffer[bar] = LineDownBuffer[bar + 1]
            LineDownBuffer[bar] = DnBuffer[bar]
            continue
        LineUpBuffer[bar] = isFractalUp(bar, LeftBars, RightBars, high)
        UpBuffer[bar] = LineUpBuffer[bar]
        if not LineUpBuffer[bar]:
            UpBuffer[bar] = LineUpBuffer[bar + 1]
            LineUpBuffer[bar] = UpBuffer[bar]
        else:
            ArrowUpBuffer[bar] = LineUpBuffer[bar]
        DnBuffer[bar] = isFractalDown(bar, LeftBars, RightBars, low)
        LineDownBuffer[bar] = DnBuffer[bar]
        if not LineDownBuffer[bar]:
            DnBuffer[bar] = LineDownBuffer[bar + 1]
            LineDownBuffer[bar] = DnBuffer[bar]
        else:
            ArrowDownBuffer[bar] = LineDownBuffer[bar]
        if close[bar] > LineUpBuffer[bar] and close[bar + 1] <= LineUpBuffer[bar + 1]:
            ArrowBreakUpBuffer[bar] = close[bar]
        if close[bar] < LineDownBuffer[bar] and close[bar + 1] >= LineDownBuffer[bar + 1]:
            ArrowBreakDownBuffer[bar] = close[bar]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    barHH = 0
    barLL = 0
    barHH1 = 0
    barLL1 = 0
    HH = Box(0.0)
    LL = Box(0.0)
    HH1 = Box(0.0)
    LL1 = Box(0.0)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtOpenBuffer[bar] = 0.0
        ExtHighBuffer[bar] = 0.0
        ExtLowBuffer[bar] = 0.0
        ExtCloseBuffer[bar] = 0.0
        ExtColorBuffer[bar] = EMPTY_VALUE
        barHH = FindFirstExtremum(bar, rates_total, ArrowBreakUpBuffer, HH)
        barHH1 = FindFirstExtremum(barHH + 1, rates_total, ArrowBreakUpBuffer, HH1)
        barLL = FindFirstExtremum(bar, rates_total, ArrowBreakDownBuffer, LL)
        barLL1 = FindFirstExtremum(barLL + 1, rates_total, ArrowBreakDownBuffer, LL1)
        if ((barHH >= 0 and barHH1 >= 0) and barLL >= 0) and barLL1 >= 0:
            for index in range(MathMax(barHH1 - 1, barLL1 - 1), bar - 1, -1):
                ExtOpenBuffer[index] = 0.0
                ExtHighBuffer[index] = 0.0
                ExtLowBuffer[index] = 0.0
                ExtCloseBuffer[index] = 0.0
                ExtColorBuffer[index] = EMPTY_VALUE
                if (close[index] - UpBuffer[index]) > 0.0:
                    ExtOpenBuffer[index] = open[index]
                    ExtHighBuffer[index] = high[index]
                    ExtLowBuffer[index] = low[index]
                    ExtCloseBuffer[index] = close[index]
                    if (close[index] - open[index]) < 0:
                        ExtColorBuffer[index] = 1.0
                    else:
                        ExtColorBuffer[index] = 0.0
                if (DnBuffer[index] - close[index]) > 0.0:
                    ExtOpenBuffer[index] = open[index]
                    ExtHighBuffer[index] = high[index]
                    ExtLowBuffer[index] = low[index]
                    ExtCloseBuffer[index] = close[index]
                    ExtColorBuffer[index] = 1.0
                    if (close[index] - open[index]) > 0:
                        ExtColorBuffer[index] = 2.0
                    else:
                        ExtColorBuffer[index] = 3.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    text = 'FractalLevels_System'
    if ExtColorBuffer[NumberofBar] == 0 or ExtColorBuffer[NumberofBar] == 1:
        if ExtColorBuffer[NumberofBar + 1] != 0 and ExtColorBuffer[NumberofBar + 1] != 1:
            text = text + ' Пробой канала! '
        else:
            text = text + ' Продолжение тренда! '
    if ExtColorBuffer[NumberofBar] == 2 or ExtColorBuffer[NumberofBar] == 3:
        if ExtColorBuffer[NumberofBar] != 2 and ExtColorBuffer[NumberofBar + 1] != 3:
            text = text + ' Пробой канала! '
        else:
            text = text + ' Продолжение тренда! '
    BuySignal(text, ExtColorBuffer, rates_total, prev_calculated, close, spread)
    SellSignal(text, ExtColorBuffer, rates_total, prev_calculated, close, spread)
    return rates_total

def FindFirstExtremum(StartPos, Rates_total, Array, Extremum):
    for bar in range(StartPos, Rates_total):
        if Array[bar] and Array[bar] != EMPTY_VALUE:
            Extremum.v = Array[bar]
            return bar
            break
    Extremum.v = 0.0
    return -1

def BuySignal(SignalSirname, BuyArrow, Rates_total, Prev_calculated, Close, Spread):
    global _s_BuySignal_counter
    if Rates_total != Prev_calculated:
        _s_BuySignal_counter = 0
    BuySignal_ = False
    SeriesTest = ArrayGetAsSeries(BuyArrow)
    index = 0
    if SeriesTest:
        index = _int(NumberofBar)
    else:
        index = Rates_total - _int(NumberofBar) - 1
    if BuyArrow[index] == 0 or BuyArrow[index] == 1:
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

def SellSignal(SignalSirname, SellArrow, Rates_total, Prev_calculated, Close, Spread):
    global _s_SellSignal_counter
    if Rates_total != Prev_calculated:
        _s_SellSignal_counter = 0
    SellSignal_ = False
    SeriesTest = ArrayGetAsSeries(SellArrow)
    index = 0
    if SeriesTest:
        index = _int(NumberofBar)
    else:
        index = Rates_total - _int(NumberofBar) - 1
    if SellArrow[index] == 2 or SellArrow[index] == 3:
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


class FractalLevelsSystem(_MQL5Indicator):
    name = 'FractalLevels_System'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'LeftBars_': 3,
        'RightBars_': 3,
        'NumberofBar': 1,  # Номер бара для подачи сигнала
        'SoundON': True,  # Разрешение алерта
        'NumberofAlerts': 2,  # Количество алертов
        'EMailON': False,  # Разрешение почтовой отправки сигнала
        'PushON': False,  # Разрешение отправки сигнала на мобильный
    }

