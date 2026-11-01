"""XXDPO_Candle_Alerts — converted from MQL5: MQL5 Indicators/XXDPO_Candle_Alerts/XXDPO_Candle_Alerts.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16711935, 2763429, 8421504, 16711680, 16748574]}, 'widths': {}, 'styles': {}, 'labels': {1: 'XXDPO Open;XXDPO High;XXDPO Low;XXDPO Close'}, 'levels': [0.0], 'description': [], 'name': 'XXDPO_Candle_Alerts', 'source': 'MQL5 Indicators/XXDPO_Candle_Alerts/XXDPO_Candle_Alerts.mq5', 'folder': 'XXDPO_Candle_Alerts', 'inputs': [{'mql': 'MA_Method1', 'py': 'MA_Method1', 'param': 'MA_Method1', 'type': 'int', 'default': 7, 'label': 'метод усреднения DPO', 'sinput': False}, {'mql': 'Length1', 'py': 'Length1', 'param': 'Length1', 'type': 'int', 'default': 21, 'label': 'глубина  усреднения DPO', 'sinput': False}, {'mql': 'Phase1', 'py': 'Phase1', 'param': 'Phase1', 'type': 'int', 'default': 15, 'label': 'параметр усреднения DPO,', 'sinput': False}, {'mql': 'MA_Method2', 'py': 'MA_Method2', 'param': 'MA_Method2', 'type': 'int', 'default': 4, 'label': 'метод сглаживания индикатора', 'sinput': False}, {'mql': 'Length2', 'py': 'Length2', 'param': 'Length2', 'type': 'int', 'default': 13, 'label': 'глубина сглаживания индикатора', 'sinput': False}, {'mql': 'Phase2', 'py': 'Phase2', 'param': 'Phase2', 'type': 'int', 'default': 100, 'label': 'параметр сглаживания индикатора', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвигиндикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Gap', 'py': 'Gap', 'param': 'Gap', 'type': 'uint', 'default': 10, 'label': 'размер неучитываемого гэпа в пунктах', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'double', 'default': 0.6, 'label': 'уровень перекупленности', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'double', 'default': -0.6, 'label': 'уровень перепроданности', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для подачи сигнала', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Разрешение алерта', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': 'Количество алертов', 'sinput': False}, {'mql': 'EMailON', 'py': 'EMailON', 'param': 'EMailON', 'type': 'bool', 'default': False, 'label': 'Разрешение почтовой отправки сигнала', 'sinput': False}, {'mql': 'PushON', 'py': 'PushON', 'param': 'PushON', 'type': 'bool', 'default': False, 'label': 'Разрешение отправки сигнала на мобильный', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
MA_Method1 = _input('MA_Method1', MODE_T3)  # метод усреднения DPO
Length1 = _input('Length1', 21)  # глубина  усреднения DPO
Phase1 = _input('Phase1', 15)  # параметр усреднения DPO,
MA_Method2 = _input('MA_Method2', MODE_JJMA)  # метод сглаживания индикатора
Length2 = _input('Length2', 13)  # глубина сглаживания индикатора
Phase2 = _input('Phase2', 100)  # параметр сглаживания индикатора
Shift = _input('Shift', 0)  # сдвигиндикатора по горизонтали в барах
Gap = _input('Gap', 10)  # размер неучитываемого гэпа в пунктах
HighLevel = _input('HighLevel', 0.6)  # уровень перекупленности
LowLevel = _input('LowLevel', -0.6)  # уровень перепроданности
NumberofBar = _input('NumberofBar', 1)  # Номер бара для подачи сигнала
SoundON = _input('SoundON', True)  # Разрешение алерта
NumberofAlerts = _input('NumberofAlerts', 2)  # Количество алертов
EMailON = _input('EMailON', False)  # Разрешение почтовой отправки сигнала
PushON = _input('PushON', False)  # Разрешение отправки сигнала на мобильный
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
StartBars = 0
StartBars1 = 0
StartBars2 = 0

def OnInit():
    global StartBars, StartBars1, StartBars2
    StartBars1 = GetStartBars(MA_Method1, Length1, Phase1)
    StartBars2 = GetStartBars(MA_Method2, Length2, Phase2)
    StartBars = StartBars1 + StartBars2
    XMA1[0].XMALengthCheck('Length1', Length1)
    XMA2[0].XMALengthCheck('Length2', Length2)
    XMA1[0].XMAPhaseCheck('Phase1', Phase1, MA_Method1)
    XMA2[0].XMAPhaseCheck('Phase2', Phase2, MA_Method2)
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, StartBars)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    shortname = Box("")
    Smooth1 = XMA1[0].GetString_MA_Method(MA_Method1)
    Smooth2 = XMA1[0].GetString_MA_Method(MA_Method2)
    StringConcatenate(shortname, 'XXDPO_Candle_Alerts(', Length1, ', ', Length2, ', ', Smooth1, ', ', Smooth2, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetInteger(INDICATOR_DIGITS, 4)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 0.0)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrLimeGreen)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrMagenta)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_SOLID)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBars:
        return 0
    XO = 0.0
    XH = 0.0
    XL = 0.0
    XC = 0.0
    XXO = 0.0
    XXH = 0.0
    XXL = 0.0
    XXC = 0.0
    Max = 0.0
    Min = 0.0
    xodpo = 0.0
    xhdpo = 0.0
    xldpo = 0.0
    xcdpo = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        XO = XMA1[0].XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, open[bar], bar, False)
        xodpo = open[bar] - XO
        XXO = XMA2[0].XMASeries(StartBars1, prev_calculated, rates_total, MA_Method2, Phase2, Length2, xodpo, bar, False)
        XH = XMA1[1].XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, high[bar], bar, False)
        xhdpo = high[bar] - XH
        XXH = XMA2[1].XMASeries(StartBars1, prev_calculated, rates_total, MA_Method2, Phase2, Length2, xhdpo, bar, False)
        XL = XMA1[2].XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, low[bar], bar, False)
        xldpo = low[bar] - XL
        XXL = XMA2[2].XMASeries(StartBars1, prev_calculated, rates_total, MA_Method2, Phase2, Length2, xldpo, bar, False)
        XC = XMA1[3].XMASeries(0, prev_calculated, rates_total, MA_Method1, Phase1, Length1, close[bar], bar, False)
        xcdpo = close[bar] - XC
        XXC = XMA2[3].XMASeries(StartBars1, prev_calculated, rates_total, MA_Method2, Phase2, Length2, xcdpo, bar, False)
        Max = MathMax(XXO, XXC)
        Max = MathMax(Max, XXL)
        Max = MathMax(Max, XXH)
        Min = MathMin(XXO, XXC)
        Min = MathMin(Min, XXL)
        Min = MathMin(Min, XXH)
        ExtOpenBuffer[bar] = XXO
        ExtHighBuffer[bar] = Max
        ExtLowBuffer[bar] = Min
        ExtCloseBuffer[bar] = XXC
        if MathAbs(open[bar] - close[bar]) <= Gap:
            ExtOpenBuffer[bar] = ExtCloseBuffer[MathMax(bar - 1, 0)]
        clr = 2
        trend = ExtCloseBuffer[bar] - ExtOpenBuffer[bar]
        if ExtCloseBuffer[bar] > HighLevel or ExtCloseBuffer[bar] < LowLevel:
            if trend > 0:
                clr = _int(4.0)
            elif trend < 0:
                clr = _int(0.0)
        else:
            if trend > 0:
                clr = _int(3.0)
            elif trend < 0:
                clr = _int(1.0)
        ExtColorBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    BuySignal('XXDPO_Candle_Alerts', rates_total, prev_calculated, close, spread)
    SellSignal('XXDPO_Candle_Alerts', rates_total, prev_calculated, close, spread)
    return rates_total

def BuySignal(SignalSirname, Rates_total, Prev_calculated, Close, Spread):
    global _s_BuySignal_counter
    if Rates_total != Prev_calculated:
        _s_BuySignal_counter = 0
    SignalText = ''
    BuySignal_ = False
    index = _int(Rates_total - 1 - NumberofBar)
    index1 = _int(Rates_total - 1 - NumberofBar) - 1
    if ExtCloseBuffer[index1] <= 0 and ExtCloseBuffer[index] > 0:
        BuySignal_ = True
        SignalText = SignalText + 'Пробой нуля! '
    if ExtColorBuffer[index1] < 3 and ExtColorBuffer[index] > 2:
        BuySignal_ = True
        SignalText = SignalText + 'Изменение направления движения свечи! '
    if ExtCloseBuffer[index1] <= HighLevel and ExtCloseBuffer[index] > HighLevel:
        BuySignal_ = True
        SignalText = SignalText + 'Пробой уровня перекупленности! '
    if ExtCloseBuffer[index1] < LowLevel and ExtCloseBuffer[index] >= LowLevel:
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
    index = _int(Rates_total - 1 - NumberofBar)
    index1 = _int(Rates_total - 1 - NumberofBar) - 1
    if ExtCloseBuffer[index1] >= 0 and ExtCloseBuffer[index] < 0:
        SellSignal_ = True
        SignalText = SignalText + 'Пробой нуля! '
    if ExtColorBuffer[index1] > 1 and ExtColorBuffer[index] < 2:
        SellSignal_ = True
        SignalText = SignalText + 'Изменение направления движения свечи! '
    if ExtCloseBuffer[index1] >= LowLevel and ExtCloseBuffer[index] < LowLevel:
        SellSignal_ = True
        SignalText = SignalText + 'Пробой уровня пепроданности! '
    if ExtCloseBuffer[index1] > HighLevel and ExtCloseBuffer[index] <= HighLevel:
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

# ---- global variables initialised from expressions
XMA1 = Arr(4, 0, dyn=False, factory=CXMA)
XMA2 = Arr(4, 0, dyn=False, factory=CXMA)

# ---- static local variables
_s_BuySignal_counter = 0
_s_SellSignal_counter = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XXDPOCandleAlerts(_MQL5Indicator):
    name = 'XXDPO_Candle_Alerts'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'MA_Method1': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # метод усреднения DPO
        'Length1': 21,  # глубина  усреднения DPO
        'Phase1': 15,  # параметр усреднения DPO,
        'MA_Method2': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод сглаживания индикатора
        'Length2': 13,  # глубина сглаживания индикатора
        'Phase2': 100,  # параметр сглаживания индикатора
        'Shift': 0,  # сдвигиндикатора по горизонтали в барах
        'Gap': 10,  # размер неучитываемого гэпа в пунктах
        'HighLevel': 0.6,  # уровень перекупленности
        'LowLevel': -0.6,  # уровень перепроданности
        'NumberofBar': 1,  # Номер бара для подачи сигнала
        'SoundON': True,  # Разрешение алерта
        'NumberofAlerts': 2,  # Количество алертов
        'EMailON': False,  # Разрешение почтовой отправки сигнала
        'PushON': False,  # Разрешение отправки сигнала на мобильный
    }

