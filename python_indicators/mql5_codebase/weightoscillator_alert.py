"""WeightOscillator_Alert — converted from MQL5: MQL5 Indicators/WeightOscillator_Alert/WeightOscillator_Alert.mq5

Осциллятор, представляющий взвешенную сглаженную сумму четырёх индикаторов - RSI, MFI, WPR и DeMarker.
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 3, 'indicator_plots': 1}, 'types': {1: 11}, 'colors': {1: [16748574, 15658671, 8421504, 55295, 42495]}, 'widths': {1: 2}, 'styles': {1: 0}, 'labels': {1: 'WeightOscillator_Alert'}, 'levels': [0.0], 'description': ['Осциллятор, представляющий взвешенную сглаженную сумму четырёх индикаторов - RSI, MFI, WPR и DeMarker.'], 'name': 'WeightOscillator_Alert', 'source': 'MQL5 Indicators/WeightOscillator_Alert/WeightOscillator_Alert.mq5', 'folder': 'WeightOscillator_Alert', 'inputs': [{'mql': 'RSIWeight', 'py': 'RSIWeight', 'param': 'RSIWeight', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'RSIPrice', 'py': 'RSIPrice', 'param': 'RSIPrice', 'type': 'int', 'default': 1, 'label': '', 'sinput': False}, {'mql': 'MFIWeight', 'py': 'MFIWeight', 'param': 'MFIWeight', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'MFIPeriod', 'py': 'MFIPeriod', 'param': 'MFIPeriod', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'MFIVolumeType', 'py': 'MFIVolumeType', 'param': 'MFIVolumeType', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'WPRWeight', 'py': 'WPRWeight', 'param': 'WPRWeight', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'WPRPeriod', 'py': 'WPRPeriod', 'param': 'WPRPeriod', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'DeMarkerWeight', 'py': 'DeMarkerWeight', 'param': 'DeMarkerWeight', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'DeMarkerPeriod', 'py': 'DeMarkerPeriod', 'param': 'DeMarkerPeriod', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'bMA_Method', 'py': 'bMA_Method', 'param': 'bMA_Method', 'type': 'int', 'default': 4, 'label': 'метод усреднения', 'sinput': False}, {'mql': 'bLength', 'py': 'bLength', 'param': 'bLength', 'type': 'uint', 'default': 5, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'bPhase', 'py': 'bPhase', 'param': 'bPhase', 'type': 'int', 'default': 100, 'label': 'параметр сглаживания,', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'uint', 'default': 70, 'label': 'уровень перезакупа', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'uint', 'default': 30, 'label': 'уровень перепроданности', 'sinput': False}, {'mql': 'SignMode', 'py': 'SignMode', 'param': 'SignMode', 'type': 'int', 'default': 0, 'label': 'Вариант подачи сигнала', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для подачи сигнала', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Разрешение алерта', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': 'Количество алертов', 'sinput': False}, {'mql': 'EMailON', 'py': 'EMailON', 'param': 'EMailON', 'type': 'bool', 'default': False, 'label': 'Разрешение почтовой отправки сигнала', 'sinput': False}, {'mql': 'PushON', 'py': 'PushON', 'param': 'PushON', 'type': 'bool', 'default': False, 'label': 'Разрешение отправки сигнала на мобильный', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum ENUM_SIGNAL_MODE
MODE_SIGNAL = 0
MODE_TREND = 1
_enum('ENUM_SIGNAL_MODE', {0: 'MODE_SIGNAL', 1: 'MODE_TREND'})

# ---- inputs and global variables
RSIWeight = _input('RSIWeight', 1.0)
RSIPeriod = _input('RSIPeriod', 14)
RSIPrice = _input('RSIPrice', PRICE_CLOSE)
MFIWeight = _input('MFIWeight', 1.0)
MFIPeriod = _input('MFIPeriod', 14)
MFIVolumeType = _input('MFIVolumeType', VOLUME_TICK)
WPRWeight = _input('WPRWeight', 1.0)
WPRPeriod = _input('WPRPeriod', 14)
DeMarkerWeight = _input('DeMarkerWeight', 1.0)
DeMarkerPeriod = _input('DeMarkerPeriod', 14)
bMA_Method = _input('bMA_Method', MODE_JJMA)  # метод усреднения
bLength = _input('bLength', 5)  # глубина сглаживания
bPhase = _input('bPhase', 100)  # параметр сглаживания,
HighLevel = _input('HighLevel', 70)  # уровень перезакупа
LowLevel = _input('LowLevel', 30)  # уровень перепроданности
SignMode = _input('SignMode', MODE_SIGNAL)  # Вариант подачи сигнала
NumberofBar = _input('NumberofBar', 1)  # Номер бара для подачи сигнала
SoundON = _input('SoundON', True)  # Разрешение алерта
NumberofAlerts = _input('NumberofAlerts', 2)  # Количество алертов
EMailON = _input('EMailON', False)  # Разрешение почтовой отправки сигнала
PushON = _input('PushON', False)  # Разрешение отправки сигнала на мобильный
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_total_1 = 0
SumWeight = 0.0
RSI_Handle = 0
MFI_Handle = 0
WPR_Handle = 0
DeMarker_Handle = 0

def OnInit():
    global DeMarker_Handle, MFI_Handle, RSI_Handle, SumWeight, WPR_Handle, min_rates_total, min_rates_total_1
    if HighLevel < 50:
        Print(' Значение уровня перекупленности должно быть не меньше 50')
        return INIT_FAILED
    if LowLevel > 50:
        Print(' Значение уровня перепроданности должно быть не больше 50')
        return INIT_FAILED
    min_rates_total_1 = _int(MathMax(RSIPeriod, MathMax(MFIPeriod, MathMax(WPRPeriod, DeMarkerPeriod)))) + 1
    min_rates_total = min_rates_total_1 + GetStartBars(bMA_Method, bLength, bPhase)
    SumWeight = RSIWeight + MFIWeight + WPRWeight + DeMarkerWeight
    XMA1.XMALengthCheck('bLength', bLength)
    XMA1.XMAPhaseCheck('bPhase', bPhase, bMA_Method)
    RSI_Handle = iRSI(None, 0, RSIPeriod, RSIPrice)
    if RSI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI')
        return INIT_FAILED
    MFI_Handle = iMFI(None, 0, MFIPeriod, MFIVolumeType)
    if MFI_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMFI')
        return INIT_FAILED
    WPR_Handle = iWPR(None, 0, WPRPeriod)
    if WPR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iWPR')
        return INIT_FAILED
    DeMarker_Handle = iDeMarker(None, 0, DeMarkerPeriod)
    if DeMarker_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iDeMarker')
        return INIT_FAILED
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(UpBuffer, True)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnBuffer, True)
    SetIndexBuffer(2, ColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorBuffer, True)
    shortname = Box("")
    Smooth1 = XMA1.GetString_MA_Method(bMA_Method)
    StringConcatenate(shortname, 'WeightOscillator_Alert(', bLength, ', ', Smooth1, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetInteger(INDICATOR_LEVELS, 3)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 0, HighLevel)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 1, 50)
    IndicatorSetDouble(INDICATOR_LEVELVALUE, 2, LowLevel)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 0, clrLimeGreen)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 1, clrGray)
    IndicatorSetInteger(INDICATOR_LEVELCOLOR, 2, clrRed)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 0, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 1, STYLE_DASHDOTDOT)
    IndicatorSetInteger(INDICATOR_LEVELSTYLE, 2, STYLE_DASHDOTDOT)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (((BarsCalculated(RSI_Handle) < rates_total or BarsCalculated(MFI_Handle) < rates_total) or BarsCalculated(WPR_Handle) < rates_total) or BarsCalculated(DeMarker_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar = 0
    RSI = Arr(0, 0.0)
    MFI = Arr(0, 0.0)
    WPR = Arr(0, 0.0)
    DeMarker = Arr(0, 0.0)
    WeightOscillator = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(RSI_Handle, 0, 0, to_copy, RSI) <= 0:
        return 0
    if CopyBuffer(MFI_Handle, 0, 0, to_copy, MFI) <= 0:
        return 0
    if CopyBuffer(WPR_Handle, 0, 0, to_copy, WPR) <= 0:
        return 0
    if CopyBuffer(DeMarker_Handle, 0, 0, to_copy, DeMarker) <= 0:
        return 0
    ArraySetAsSeries(RSI, True)
    ArraySetAsSeries(MFI, True)
    ArraySetAsSeries(WPR, True)
    ArraySetAsSeries(DeMarker, True)
    maxbar = rates_total - min_rates_total_1 - 1
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        WeightOscillator = _fdiv((RSIWeight * RSI[bar]) + (MFIWeight * MFI[bar]) + (WPRWeight * (WPR[bar] + 100)) + (DeMarkerWeight * 100 * DeMarker[bar]), SumWeight)
        UpBuffer[bar] = XMA1.XMASeries(maxbar, prev_calculated, rates_total, bMA_Method, bPhase, bLength, WeightOscillator, bar, True)
        DnBuffer[bar] = 50.0
        clr = _int(2.0)
        if UpBuffer[bar] > HighLevel:
            clr = _int(0.0)
        elif UpBuffer[bar] > 50:
            clr = _int(1.0)
        elif UpBuffer[bar] < LowLevel:
            clr = _int(4.0)
        elif UpBuffer[bar] < 50:
            clr = _int(3.0)
        ColorBuffer[bar] = clr
    else:
        bar = _range_end(bar, 0 - 1, -1)
    BuySignal('WeightOscillator_Alert', ColorBuffer, 0, rates_total, prev_calculated, close, spread)
    SellSignal('WeightOscillator_Alert', ColorBuffer, 4, rates_total, prev_calculated, close, spread)
    return rates_total

def BuySignal(SignalSirname, ColorArray, ColorIndex, Rates_total, Prev_calculated, Close, Spread):
    global _s_BuySignal_counter
    if Rates_total != Prev_calculated:
        _s_BuySignal_counter = 0
    BuySignal_ = False
    SeriesTest = ArrayGetAsSeries(ColorArray)
    index = 0
    index1 = 0
    if SeriesTest:
        index = _int(NumberofBar)
        index1 = index + 1
    else:
        index = Rates_total - _int(NumberofBar) - 1
        index1 = index - 1
    if SignMode == MODE_SIGNAL:
        if ColorArray[index1] != ColorIndex and ColorArray[index] == ColorIndex:
            BuySignal_ = True
    else:
        if ColorArray[index] == ColorIndex:
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
        Bid += Point() * Spread[index]
        sAsk = DoubleToString(Ask, Digits())
        sBid = DoubleToString(Bid, Digits())
        sPeriod = GetStringTimeframe(ChartPeriod())
        if SignMode == MODE_SIGNAL or (SignMode == MODE_TREND and ColorArray[index1] != ColorIndex):
            if SoundON:
                Alert('BUY signal \n Ask=', Ask, '\n Bid=', Bid, '\n currtime=', text, '\n Symbol=', Symbol(), ' Period=', sPeriod)
            if EMailON:
                SendMail(SignalSirname + ': BUY signal alert', 'BUY signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
            if PushON:
                SendNotification(SignalSirname + ': BUY signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
        else:
            if SoundON:
                Alert('Up Trend signal \n Ask=', Ask, '\n Bid=', Bid, '\n currtime=', text, '\n Symbol=', Symbol(), ' Period=', sPeriod)
            if EMailON:
                SendMail(SignalSirname + ': Up Trend signal alert', 'BUY signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
            if PushON:
                SendNotification(SignalSirname + ': Up Trend signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)

def SellSignal(SignalSirname, ColorArray, ColorIndex, Rates_total, Prev_calculated, Close, Spread):
    global _s_SellSignal_counter
    if Rates_total != Prev_calculated:
        _s_SellSignal_counter = 0
    SellSignal_ = False
    SeriesTest = ArrayGetAsSeries(ColorArray)
    index = 0
    index1 = 0
    if SeriesTest:
        index = _int(NumberofBar)
        index1 = index + 1
    else:
        index = Rates_total - _int(NumberofBar) - 1
        index1 = index - 1
    if SignMode == MODE_SIGNAL:
        if ColorArray[index1] != ColorIndex and ColorArray[index] == ColorIndex:
            SellSignal_ = True
    else:
        if ColorArray[index] == ColorIndex:
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
        Bid += Point() * Spread[index]
        sAsk = DoubleToString(Ask, Digits())
        sBid = DoubleToString(Bid, Digits())
        sPeriod = GetStringTimeframe(ChartPeriod())
        if SignMode == MODE_SIGNAL or (SignMode == MODE_TREND and ColorArray[index1] != ColorIndex):
            if SoundON:
                Alert('SELL signal \n Ask=', Ask, '\n Bid=', Bid, '\n currtime=', text, '\n Symbol=', Symbol(), ' Period=', sPeriod)
            if EMailON:
                SendMail(SignalSirname + ': SELL signal alert', 'SELL signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
            if PushON:
                SendNotification(SignalSirname + ': SELL signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
        else:
            if SoundON:
                Alert('Down trend signal \n Ask=', Ask, '\n Bid=', Bid, '\n currtime=', text, '\n Symbol=', Symbol(), ' Period=', sPeriod)
            if EMailON:
                SendMail(SignalSirname + ': Down trend signal alert', 'SELL signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
            if PushON:
                SendNotification(SignalSirname + ': Down trend signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

def CreateRightPrice(chart_id, name, nwin, time, price, Color):
    ObjectCreate(chart_id, name, OBJ_ARROW_RIGHT_PRICE, nwin, time, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, 2)

def SetRightPrice(chart_id, name, nwin, time, price, Color):
    if ObjectFind(chart_id, name) == -1:
        CreateRightPrice(chart_id, name, nwin, time, price, Color)
    else:
        ObjectMove(chart_id, name, 0, time, price)

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()

# ---- static local variables
_s_BuySignal_counter = 0
_s_SellSignal_counter = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WeightOscillatorAlert(_MQL5Indicator):
    name = 'WeightOscillator_Alert'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSIWeight': 1.0,
        'RSIPeriod': 14,
        'RSIPrice': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median', 6: 'Typical', 7: 'Weighted'}, default=1),
        'MFIWeight': 1.0,
        'MFIPeriod': 14,
        'MFIVolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),
        'WPRWeight': 1.0,
        'WPRPeriod': 14,
        'DeMarkerWeight': 1.0,
        'DeMarkerPeriod': 14,
        'bMA_Method': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=4),  # метод усреднения
        'bLength': 5,  # глубина сглаживания
        'bPhase': 100,  # параметр сглаживания,
        'HighLevel': 70,  # уровень перезакупа
        'LowLevel': 30,  # уровень перепроданности
        'SignMode': _Choice({0: 'Сигналы пробоя', 1: 'Сигналы пробоя и тренда'}, default=0),  # Вариант подачи сигнала
        'NumberofBar': 1,  # Номер бара для подачи сигнала
        'SoundON': True,  # Разрешение алерта
        'NumberofAlerts': 2,  # Количество алертов
        'EMailON': False,  # Разрешение почтовой отправки сигнала
        'PushON': False,  # Разрешение отправки сигнала на мобильный
    }

