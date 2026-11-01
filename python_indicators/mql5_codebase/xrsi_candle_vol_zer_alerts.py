"""XRSI_Candle_Vol_Zer_Alerts — converted from MQL5: MQL5 Indicators/XRSI_Candle_Vol_Zer_Alerts/XRSI_Candle_Vol_Zer_Alerts.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'separate', 'indicator_buffers': 11, 'indicator_plots': 5}, 'types': {1: 7, 2: 1, 3: 17, 4: 1, 5: 12}, 'colors': {1: [16443110], 2: [8421376], 3: [16776960, 16711680, 8421376, 17919, 2763429, 16711935], 4: [3937500], 5: [16748574, 16711935]}, 'widths': {2: 1, 4: 1, 5: 3}, 'styles': {2: 4, 4: 4}, 'labels': {1: 'XRSI_Candle_Vol Channel', 2: 'XRSI_Candle_Vol Res', 3: 'XRSI_Candle_Vol Open;XRSI_Candle_Vol High;XRSI_Candle_Vol Low;XRSI_Candle_Vol Close', 4: 'XRSI_Candle_Vol Supr', 5: 'XRSI_Candle_Vol ZeroSignal'}, 'levels': [0.0], 'description': [], 'name': 'XRSI_Candle_Vol_Zer_Alerts', 'source': 'MQL5 Indicators/XRSI_Candle_Vol_Zer_Alerts/XRSI_Candle_Vol_Zer_Alerts.mq5', 'folder': 'XRSI_Candle_Vol_Zer_Alerts', 'inputs': [{'mql': 'RSIPeriod', 'py': 'RSIPeriod', 'param': 'RSIPeriod', 'type': 'uint', 'default': 14, 'label': 'период индикатора', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'объём', 'sinput': False}, {'mql': 'HighLevel', 'py': 'HighLevel', 'param': 'HighLevel', 'type': 'int', 'default': 7, 'label': 'уровень перекупленности', 'sinput': False}, {'mql': 'LowLevel', 'py': 'LowLevel', 'param': 'LowLevel', 'type': 'int', 'default': -7, 'label': 'уровень перепроданности', 'sinput': False}, {'mql': 'Gap', 'py': 'Gap', 'param': 'Gap', 'type': 'uint', 'default': 10, 'label': 'размер неучитываемого гэпа в пунктах', 'sinput': False}, {'mql': 'MA_SMethod', 'py': 'MA_SMethod', 'param': 'MA_SMethod', 'type': 'int', 'default': 7, 'label': 'Метод усреднения', 'sinput': False}, {'mql': 'MA_Length', 'py': 'MA_Length', 'param': 'MA_Length', 'type': 'uint', 'default': 12, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'MA_Phase', 'py': 'MA_Phase', 'param': 'MA_Phase', 'type': 'int', 'default': 15, 'label': 'параметр первого сглаживания,', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для подачи сигнала', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Разрешение алерта', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': 'Количество алертов', 'sinput': False}, {'mql': 'EMailON', 'py': 'EMailON', 'param': 'EMailON', 'type': 'bool', 'default': False, 'label': 'Разрешение почтовой отправки сигнала', 'sinput': False}, {'mql': 'PushON', 'py': 'PushON', 'param': 'PushON', 'type': 'bool', 'default': False, 'label': 'Разрешение отправки сигнала на мобильный', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# ---- inputs and global variables
RSIPeriod = _input('RSIPeriod', 14)  # период индикатора
VolumeType = _input('VolumeType', VOLUME_TICK)  # объём
HighLevel = _input('HighLevel', 7)  # уровень перекупленности
LowLevel = _input('LowLevel', -7)  # уровень перепроданности
Gap = _input('Gap', 10)  # размер неучитываемого гэпа в пунктах
MA_SMethod = _input('MA_SMethod', MODE_T3)  # Метод усреднения
MA_Length = _input('MA_Length', 12)  # Глубина сглаживания
MA_Phase = _input('MA_Phase', 15)  # параметр первого сглаживания,
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
NumberofBar = _input('NumberofBar', 1)  # Номер бара для подачи сигнала
SoundON = _input('SoundON', True)  # Разрешение алерта
NumberofAlerts = _input('NumberofAlerts', 2)  # Количество алертов
EMailON = _input('EMailON', False)  # Разрешение почтовой отправки сигнала
PushON = _input('PushON', False)  # Разрешение отправки сигнала на мобильный
min_rates_total = 0
min_rates_1 = 0
AtrPeriod = 0
OpenBuffer = Arr(0, 0.0)
HighBuffer = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)
CloseBuffer = Arr(0, 0.0)
ColorBuffer = Arr(0, 0.0)
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
UpCldIndBuffer = Arr(0, 0.0)
DnCldIndBuffer = Arr(0, 0.0)
ZrSigBuffer = Arr(0, 0.0)
ColorZrSigBuffer = Arr(0, 0.0)
RSI_Handle = Arr(4, 0, dyn=False)

def GetRange(index, High, Low, Len):
    AvgRange = 0.0
    for count in range(_int(index + Len - 1), index - 1, -1):
        AvgRange += MathAbs(High[count] - Low[count])
    return _fdiv(AvgRange, Len)

def OnInit():
    global AtrPeriod, min_rates_1, min_rates_total
    min_rates_1 = _int(RSIPeriod)
    min_rates_total = min_rates_1 + GetStartBars(MA_SMethod, MA_Length, MA_Phase)
    AtrPeriod = 15
    RSI_Handle[0] = iRSI(None, 0, RSIPeriod, PRICE_OPEN)
    if RSI_Handle[0] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI 1')
        return INIT_FAILED
    RSI_Handle[1] = iRSI(None, 0, RSIPeriod, PRICE_HIGH)
    if RSI_Handle[1] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI 2')
        return INIT_FAILED
    RSI_Handle[2] = iRSI(None, 0, RSIPeriod, PRICE_LOW)
    if RSI_Handle[2] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI 3')
        return INIT_FAILED
    RSI_Handle[3] = iRSI(None, 0, RSIPeriod, PRICE_CLOSE)
    if RSI_Handle[3] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI 4')
        return INIT_FAILED
    SetIndexBuffer(0, UpCldIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(UpCldIndBuffer, True)
    SetIndexBuffer(1, DnCldIndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(DnCldIndBuffer, True)
    SetIndexBuffer(2, UpIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(UpIndBuffer, True)
    SetIndexBuffer(3, OpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, HighBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, LowBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, CloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(7, ColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(OpenBuffer, True)
    ArraySetAsSeries(HighBuffer, True)
    ArraySetAsSeries(LowBuffer, True)
    ArraySetAsSeries(CloseBuffer, True)
    ArraySetAsSeries(ColorBuffer, True)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_SHOW_DATA, False)
    SetIndexBuffer(8, DnIndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_SHOW_DATA, False)
    ArraySetAsSeries(DnIndBuffer, True)
    SetIndexBuffer(9, ZrSigBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total + AtrPeriod)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(4, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(4, PLOT_ARROW, 124)
    ArraySetAsSeries(ZrSigBuffer, True)
    SetIndexBuffer(10, ColorZrSigBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorZrSigBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'XRSI_Candle_Vol_Zer_Alerts(' + _str(RSIPeriod) + ')')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, Tick_Volume, Volume, Spread):
    if (((BarsCalculated(RSI_Handle[0]) < rates_total or BarsCalculated(RSI_Handle[1]) < rates_total) or BarsCalculated(RSI_Handle[2]) < rates_total) or BarsCalculated(RSI_Handle[3]) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    maxbar = 0
    vol = 0.0
    xvol = 0.0
    maxbar = rates_total - min_rates_1 - 1
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(Close, True)
    ArraySetAsSeries(Open, True)
    ArraySetAsSeries(High, True)
    ArraySetAsSeries(Low, True)
    ArraySetAsSeries(Spread, True)
    if VolumeType == VOLUME_TICK:
        ArraySetAsSeries(Tick_Volume, True)
    else:
        ArraySetAsSeries(Volume, True)
    if CopyBuffer(RSI_Handle[0], 0, 0, to_copy, OpenBuffer) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[1], 0, 0, to_copy, HighBuffer) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[2], 0, 0, to_copy, LowBuffer) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[3], 0, 0, to_copy, CloseBuffer) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Max = MathMax(OpenBuffer[bar], CloseBuffer[bar])
        Max = MathMax(Max, LowBuffer[bar])
        Max = MathMax(Max, HighBuffer[bar])
        Min = MathMin(OpenBuffer[bar], CloseBuffer[bar])
        Min = MathMin(Min, LowBuffer[bar])
        Min = MathMin(Min, HighBuffer[bar])
        HighBuffer[bar] = Max
        LowBuffer[bar] = Min
        OpenBuffer[bar] -= 50
        HighBuffer[bar] -= 50
        LowBuffer[bar] -= 50
        CloseBuffer[bar] -= 50
        if VolumeType == VOLUME_TICK:
            vol = float(Tick_Volume[bar])
        else:
            vol = float(Volume[bar])
        OpenBuffer[bar] *= vol
        HighBuffer[bar] *= vol
        LowBuffer[bar] *= vol
        CloseBuffer[bar] *= vol
        OpenBuffer[bar] = XMAO.XMASeries(maxbar, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, OpenBuffer[bar], bar, True)
        HighBuffer[bar] = XMAH.XMASeries(maxbar, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, HighBuffer[bar], bar, True)
        LowBuffer[bar] = XMAL.XMASeries(maxbar, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, LowBuffer[bar], bar, True)
        CloseBuffer[bar] = XMAC.XMASeries(maxbar, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, CloseBuffer[bar], bar, True)
        xvol = XMAV.XMASeries(maxbar, prev_calculated, rates_total, MA_SMethod, MA_Phase, MA_Length, vol, bar, True)
        if MathAbs(Open[bar] - Close[bar]) <= Gap:
            OpenBuffer[bar] = CloseBuffer[bar + 1]
        UpCldIndBuffer[bar] = HighLevel * xvol
        UpIndBuffer[bar] = UpCldIndBuffer[bar]
        DnCldIndBuffer[bar] = LowLevel * xvol
        DnIndBuffer[bar] = DnCldIndBuffer[bar]
        clr = _int(2.0)
        if CloseBuffer[bar] > UpIndBuffer[bar]:
            if CloseBuffer[bar] >= OpenBuffer[bar]:
                clr = _int(0.0)
            else:
                clr = _int(1.0)
        elif CloseBuffer[bar] < DnIndBuffer[bar]:
            if CloseBuffer[bar] <= OpenBuffer[bar]:
                clr = _int(5.0)
            else:
                clr = _int(4.0)
        else:
            if CloseBuffer[bar] >= OpenBuffer[bar]:
                clr = _int(2.0)
            else:
                clr = _int(3.0)
        ColorBuffer[bar] = clr
        ColorZrSigBuffer[bar] = 2.0
        ZrSigBuffer[bar] = EMPTY_VALUE
        if CloseBuffer[bar + 1] > 0.0 and CloseBuffer[bar] <= 0.0:
            ZrSigBuffer[bar] = HighBuffer[bar] + (GetRange(bar, HighBuffer, LowBuffer, AtrPeriod) * 0.5)
            ColorZrSigBuffer[bar] = 1.0
        if CloseBuffer[bar + 1] < 0.0 and CloseBuffer[bar] >= 0.0:
            ZrSigBuffer[bar] = LowBuffer[bar] - (GetRange(bar, HighBuffer, LowBuffer, AtrPeriod) * 0.5)
            ColorZrSigBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    BuySignal('XRSI_Candle_Vol_Zer_Alerts', rates_total, prev_calculated, Close, Spread)
    SellSignal('XRSI_Candle_Vol_Zer_Alerts', rates_total, prev_calculated, Close, Spread)
    return rates_total

def BuySignal(SignalSirname, Rates_total, Prev_calculated, Close, Spread):
    global _s_BuySignal_counter
    if Rates_total != Prev_calculated:
        _s_BuySignal_counter = 0
    SignalText = ''
    BuySignal_ = False
    index = _int(NumberofBar)
    index1 = _int(NumberofBar) + 1
    if ColorZrSigBuffer[index1] != 0 and ColorZrSigBuffer[index] == 0:
        BuySignal_ = True
        SignalText = SignalText + 'Пробой нуля! '
    if CloseBuffer[index1] <= OpenBuffer[index1] and CloseBuffer[index] > OpenBuffer[index]:
        BuySignal_ = True
        SignalText = SignalText + 'Изменение направления движения свечи! '
    if CloseBuffer[index1] <= UpIndBuffer[index1] and CloseBuffer[index] > UpIndBuffer[index]:
        BuySignal_ = True
        SignalText = SignalText + 'Пробой уровня перекупленности! '
    if CloseBuffer[index1] <= DnIndBuffer[index1] and CloseBuffer[index] > DnIndBuffer[index]:
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
    if ColorZrSigBuffer[index1] != 1 and ColorZrSigBuffer[index] == 1:
        SellSignal_ = True
        SignalText = SignalText + 'Пробой нуля! '
    if CloseBuffer[index1] >= OpenBuffer[index1] and CloseBuffer[index] < OpenBuffer[index]:
        SellSignal_ = True
        SignalText = SignalText + 'Изменение направления движения свечи! '
    if CloseBuffer[index1] >= DnIndBuffer[index1] and CloseBuffer[index] < DnIndBuffer[index]:
        SellSignal_ = True
        SignalText = SignalText + 'Пробой уровня пепроданности! '
    if CloseBuffer[index1] > UpIndBuffer[index1] and CloseBuffer[index] <= UpIndBuffer[index]:
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
XMAO = _alloc(CXMA)
XMAO.__init__()
XMAH = _alloc(CXMA)
XMAH.__init__()
XMAL = _alloc(CXMA)
XMAL.__init__()
XMAC = _alloc(CXMA)
XMAC.__init__()
XMAV = _alloc(CXMA)
XMAV.__init__()

# ---- static local variables
_s_BuySignal_counter = 0
_s_SellSignal_counter = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class XRSICandleVolZerAlerts(_MQL5Indicator):
    name = 'XRSI_Candle_Vol_Zer_Alerts'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSIPeriod': 14,  # период индикатора
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём
        'HighLevel': 7,  # уровень перекупленности
        'LowLevel': -7,  # уровень перепроданности
        'Gap': 10,  # размер неучитываемого гэпа в пунктах
        'MA_SMethod': _Choice({0: 'SMA', 1: 'EMA', 2: 'SMMA', 3: 'LWMA', 4: 'JJMA', 5: 'JurX', 6: 'ParMA', 7: 'T3', 8: 'VIDYA', 9: 'AMA'}, default=7),  # Метод усреднения
        'MA_Length': 12,  # Глубина сглаживания
        'MA_Phase': 15,  # параметр первого сглаживания,
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'NumberofBar': 1,  # Номер бара для подачи сигнала
        'SoundON': True,  # Разрешение алерта
        'NumberofAlerts': 2,  # Количество алертов
        'EMailON': False,  # Разрешение почтовой отправки сигнала
        'PushON': False,  # Разрешение отправки сигнала на мобильный
    }

