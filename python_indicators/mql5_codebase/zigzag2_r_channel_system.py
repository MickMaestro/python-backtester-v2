"""Zigzag2_R_channel_System — converted from MQL5: MQL5 Indicators/Zigzag2_R_channel_System/Zigzag2_R_channel_System.mq5

ZigZag
Copyright: Copyright © 2005, MetaQuotes Software Corp.; Link: http://www.metaquotes.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 15, 'indicator_plots': 6}, 'types': {1: 7, 2: 8, 3: 8, 4: 5, 5: 5, 6: 17}, 'colors': {1: [16443110], 2: [16776960, 55295], 3: [16776960, 55295], 4: [16711680], 5: [9639167], 6: [65407, 8421376, 8388736, 16711935]}, 'widths': {2: 2, 3: 2, 4: 2, 5: 2}, 'styles': {}, 'labels': {1: 'Zigzag2_R_channel Cloud', 2: 'Up Zigzag2_R_channel', 3: 'Down Zigzag2_R_channel', 4: 'Up Zigzag2_R_Arrows', 5: 'Down Zigzag2_R_Arrows', 6: 'Zigzag2_R_channel_Candle'}, 'levels': [], 'description': ['ZigZag'], 'name': 'Zigzag2_R_channel_System', 'source': 'MQL5 Indicators/Zigzag2_R_channel_System/Zigzag2_R_channel_System.mq5', 'folder': 'Zigzag2_R_channel_System', 'inputs': [{'mql': 'ExtDepth', 'py': 'ExtDepth', 'param': 'ExtDepth', 'type': 'int', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'ExtDeviation', 'py': 'ExtDeviation', 'param': 'ExtDeviation', 'type': 'int', 'default': 5, 'label': '', 'sinput': False}, {'mql': 'ExtBackstep', 'py': 'ExtBackstep', 'param': 'ExtBackstep', 'type': 'int', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'UpLable', 'py': 'UpLable', 'param': 'UpLable', 'type': 'uint', 'default': 119, 'label': 'лейба верхнего фрактала', 'sinput': False}, {'mql': 'DnLable', 'py': 'DnLable', 'param': 'DnLable', 'type': 'uint', 'default': 119, 'label': 'лейба нижнего фрактала', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для подачи сигнала', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Разрешение алерта', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': 'Количество алертов', 'sinput': False}, {'mql': 'EMailON', 'py': 'EMailON', 'param': 'EMailON', 'type': 'bool', 'default': False, 'label': 'Разрешение почтовой отправки сигнала', 'sinput': False}, {'mql': 'PushON', 'py': 'PushON', 'param': 'PushON', 'type': 'bool', 'default': False, 'label': 'Разрешение отправки сигнала на мобильный', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtDepth = _input('ExtDepth', 12)
ExtDeviation = _input('ExtDeviation', 5)
ExtBackstep = _input('ExtBackstep', 3)
UpLable = _input('UpLable', 119)  # лейба верхнего фрактала
DnLable = _input('DnLable', 119)  # лейба нижнего фрактала
NumberofBar = _input('NumberofBar', 1)  # Номер бара для подачи сигнала
SoundON = _input('SoundON', True)  # Разрешение алерта
NumberofAlerts = _input('NumberofAlerts', 2)  # Количество алертов
EMailON = _input('EMailON', False)  # Разрешение почтовой отправки сигнала
PushON = _input('PushON', False)  # Разрешение отправки сигнала на мобильный
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
UpperBuffer = Arr(0, 0.0)
LowerBuffer = Arr(0, 0.0)
ColorUpperBuffer = Arr(0, 0.0)
ColorLowerBuffer = Arr(0, 0.0)
ZigzagPeakBuffer = Arr(0, 0.0)
ZigzagLawnBuffer = Arr(0, 0.0)
HighMapBuffer = Arr(0, 0.0)
LowMapBuffer = Arr(0, 0.0)
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
level = 3  # recounting's depth
downloadhistory = False
dExtDeviation = 0.0
min_rates_total = 0

def OnInit():
    global dExtDeviation, min_rates_total
    min_rates_total = ExtDepth + ExtBackstep
    dExtDeviation = ExtDeviation * Point()
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, UpperBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ColorUpperBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(4, LowerBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ColorLowerBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(6, ZigzagPeakBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, ZigzagLawnBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, None)
    PlotIndexSetDouble(5, PLOT_EMPTY_VALUE, None)
    ArraySetAsSeries(UpBuffer, True)
    ArraySetAsSeries(DnBuffer, True)
    ArraySetAsSeries(UpperBuffer, True)
    ArraySetAsSeries(LowerBuffer, True)
    ArraySetAsSeries(ColorUpperBuffer, True)
    ArraySetAsSeries(ColorLowerBuffer, True)
    ArraySetAsSeries(ZigzagLawnBuffer, True)
    ArraySetAsSeries(ZigzagPeakBuffer, True)
    ArraySetAsSeries(HighMapBuffer, True)
    ArraySetAsSeries(LowMapBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_ARROW, DnLable)
    PlotIndexSetInteger(4, PLOT_ARROW, UpLable)
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
    SetIndexBuffer(13, HighMapBuffer, INDICATOR_CALCULATIONS)
    SetIndexBuffer(14, LowMapBuffer, INDICATOR_CALCULATIONS)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    shortname = Box("")
    StringConcatenate(shortname, 'Zigzag2_R_Arrows(ExtDepth=', ExtDepth, 'ExtDeviation = ', ExtDeviation, 'ExtBackstep = ', ExtBackstep, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    iii = 0
    counterZ = 0
    whatlookfor = 0
    back = 0
    lasthighpos = 0
    lastlowpos = 0
    val = 0.0
    res = 0.0
    curlow = 9999999999.0
    curhigh = 0.0
    lasthigh = 0.0
    lastlow = 999999999.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        ArrayInitialize(ZigzagPeakBuffer, None)
        ArrayInitialize(ZigzagLawnBuffer, None)
        ArrayInitialize(HighMapBuffer, None)
        ArrayInitialize(LowMapBuffer, None)
    else:
        limit = rates_total - prev_calculated
        while counterZ < level and iii < 100:
            res = ZigzagPeakBuffer[iii] + ZigzagLawnBuffer[iii]
            if res:
                counterZ += 1
            iii += 1
        iii -= 1
        limit = iii
        if LowMapBuffer[iii]:
            curlow = LowMapBuffer[iii]
            whatlookfor = 1
        else:
            curhigh = HighMapBuffer[iii]
            whatlookfor = -1
        iii = limit - 1
        for iii in range(iii, 0 - 1, -1):
            ZigzagPeakBuffer[iii] = 0.0
            ZigzagLawnBuffer[iii] = 0.0
            LowMapBuffer[iii] = 0.0
            HighMapBuffer[iii] = 0.0
        else:
            iii = _range_end(iii, 0 - 1, -1)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        val = low[ArrayMinimum(low, bar, ExtDepth)]
        if val == lastlow:
            val = 0.0
        else:
            lastlow = val
            if (low[bar] - val) > dExtDeviation:
                val = 0.0
            else:
                back = 1
                for back in range(back, ExtBackstep + 1):
                    res = LowMapBuffer[bar + back]
                    if res and res > val:
                        LowMapBuffer[bar + back] = 0.0
                else:
                    back = _range_end(back, ExtBackstep + 1, 1)
        if low[bar] == val:
            LowMapBuffer[bar] = val
        else:
            LowMapBuffer[bar] = 0.0
        val = high[ArrayMaximum(high, bar, ExtDepth)]
        if val == lasthigh:
            val = 0.0
        else:
            lasthigh = val
            if (val - high[bar]) > dExtDeviation:
                val = 0.0
            else:
                back = 1
                for back in range(back, ExtBackstep + 1):
                    res = HighMapBuffer[bar + back]
                    if res and res < val:
                        HighMapBuffer[bar + back] = 0.0
                else:
                    back = _range_end(back, ExtBackstep + 1, 1)
        if high[bar] == val:
            HighMapBuffer[bar] = val
        else:
            HighMapBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if not whatlookfor:
        lastlow = 0.0
        lasthigh = 0.0
    else:
        lastlow = curlow
        lasthigh = curhigh
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        res = 0.0
        _sw1 = whatlookfor
        if _sw1 == 0:
            if (not lastlow) and (not lasthigh):
                if HighMapBuffer[bar]:
                    lasthigh = high[bar]
                    lasthighpos = bar
                    whatlookfor = -1
                    ZigzagPeakBuffer[bar] = lasthigh
                    res = 1.0
                if LowMapBuffer[bar]:
                    lastlow = low[bar]
                    lastlowpos = bar
                    whatlookfor = 1
                    ZigzagLawnBuffer[bar] = lastlow
                    res = 1.0
        elif _sw1 == 1:
            if (LowMapBuffer[bar] and LowMapBuffer[bar] < lastlow) and (not HighMapBuffer[bar]):
                ZigzagLawnBuffer[lastlowpos] = 0.0
                lastlowpos = bar
                lastlow = LowMapBuffer[bar]
                ZigzagLawnBuffer[bar] = lastlow
                res = 1.0
            if HighMapBuffer[bar] and (not LowMapBuffer[bar]):
                lasthigh = HighMapBuffer[bar]
                lasthighpos = bar
                ZigzagPeakBuffer[bar] = lasthigh
                whatlookfor = -1
                res = 1.0
        elif _sw1 == -1:
            if (HighMapBuffer[bar] and HighMapBuffer[bar] > lasthigh) and (not LowMapBuffer[bar]):
                ZigzagPeakBuffer[lasthighpos] = 0.0
                lasthighpos = bar
                lasthigh = HighMapBuffer[bar]
                ZigzagPeakBuffer[bar] = lasthigh
            if LowMapBuffer[bar] and (not HighMapBuffer[bar]):
                lastlow = LowMapBuffer[bar]
                lastlowpos = bar
                ZigzagLawnBuffer[bar] = lastlow
                whatlookfor = 1
        else:
            return rates_total
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
        barHH = FindFirstExtremum(bar, rates_total, ZigzagPeakBuffer, HH)
        barHH1 = FindFirstExtremum(barHH + 1, rates_total, ZigzagPeakBuffer, HH1)
        if barHH >= 0 and barHH1 >= 0:
            for index in range(barHH1 - 1, barHH, -1):
                UpBuffer[index] = HH1.v
                UpperBuffer[index] = HH1.v
                ColorUpperBuffer[index] = ColorUpperBuffer[index + 1]
            for index in range(barHH, bar - 1, -1):
                UpBuffer[index] = HH.v
                UpperBuffer[index] = HH.v
                if HH.v > HH1.v:
                    ColorUpperBuffer[index] = 0.0
                elif HH.v < HH1.v:
                    ColorUpperBuffer[index] = 1.0
                else:
                    ColorUpperBuffer[index] = ColorUpperBuffer[index + 1]
        barLL = FindFirstExtremum(bar, rates_total, ZigzagLawnBuffer, LL)
        barLL1 = FindFirstExtremum(barLL + 1, rates_total, ZigzagLawnBuffer, LL1)
        if barLL >= 0 and barLL1 >= 0:
            for index in range(barLL1 - 1, barLL, -1):
                DnBuffer[index] = LL1.v
                LowerBuffer[index] = LL1.v
                ColorLowerBuffer[index] = ColorLowerBuffer[index + 1]
            for index in range(barLL, bar - 1, -1):
                DnBuffer[index] = LL.v
                LowerBuffer[index] = LL.v
                if LL.v > LL1.v:
                    ColorLowerBuffer[index] = 0.0
                elif LL.v < LL1.v:
                    ColorLowerBuffer[index] = 1.0
                else:
                    ColorLowerBuffer[index] = ColorLowerBuffer[index + 1]
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
    text = 'Zigzag2_R_channel_System'
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


class Zigzag2RChannelSystem(_MQL5Indicator):
    name = 'Zigzag2_R_channel_System'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'ExtDepth': 12,
        'ExtDeviation': 5,
        'ExtBackstep': 3,
        'UpLable': 119,  # лейба верхнего фрактала
        'DnLable': 119,  # лейба нижнего фрактала
        'NumberofBar': 1,  # Номер бара для подачи сигнала
        'SoundON': True,  # Разрешение алерта
        'NumberofAlerts': 2,  # Количество алертов
        'EMailON': False,  # Разрешение почтовой отправки сигнала
        'PushON': False,  # Разрешение отправки сигнала на мобильный
    }

