"""StreamСCandles — converted from MQL5: MQL5 Indicators/Background_StreamСCandles_HTF/StreamСCandles.mq5

Индикатор окрашивает свечки, размер которых в пунктах, умноженных на объём, превышает фиксированный в настройках.
В расчет принимается в зависимости от настроек тело свечи или весь размер свечи.
Copyright: Copyright © 2016, Yuriy Tokman (YTG); Link: http://ytg.com.ua/; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Yuriy Tokman (YTG)', 'link': 'http://ytg.com.ua/', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [65280, 8421504, 255]}, 'widths': {}, 'styles': {}, 'labels': {1: 'StreamСCandles Open;High;Low;Close'}, 'levels': [], 'description': ['Индикатор окрашивает свечки, размер которых в пунктах, умноженных на объём, превышает фиксированный в настройках.', 'В расчет принимается в зависимости от настроек тело свечи или весь размер свечи.'], 'name': 'StreamСCandles', 'source': 'MQL5 Indicators/Background_StreamСCandles_HTF/StreamСCandles.mq5', 'folder': 'Background_StreamСCandles_HTF', 'inputs': [{'mql': 'Candles_Mode', 'py': 'Candles_Mode', 'param': 'Candles_Mode', 'type': 'int', 'default': 0, 'label': 'вариант размера', 'sinput': False}, {'mql': 'Candles_Size', 'py': 'Candles_Size', 'param': 'Candles_Size', 'type': 'uint', 'default': 1000, 'label': 'минимальный размер свечи для срабатывания', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'объём', 'sinput': False}, {'mql': 'NumberofBar', 'py': 'NumberofBar', 'param': 'NumberofBar', 'type': 'uint', 'default': 1, 'label': 'Номер бара для подачи сигнала', 'sinput': False}, {'mql': 'SoundON', 'py': 'SoundON', 'param': 'SoundON', 'type': 'bool', 'default': True, 'label': 'Разрешение алерта', 'sinput': False}, {'mql': 'NumberofAlerts', 'py': 'NumberofAlerts', 'param': 'NumberofAlerts', 'type': 'uint', 'default': 2, 'label': 'Количество алертов', 'sinput': False}, {'mql': 'EMailON', 'py': 'EMailON', 'param': 'EMailON', 'type': 'bool', 'default': False, 'label': 'Разрешение почтовой отправки сигнала', 'sinput': False}, {'mql': 'PushON', 'py': 'PushON', 'param': 'PushON', 'type': 'bool', 'default': False, 'label': 'Разрешение отправки сигнала на мобильный', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_APPLIED_VOLUME_
VOLUME_TICK_ = 0
VOLUME_REAL_ = 1
VOLUME_NONE = 2
_enum('ENUM_APPLIED_VOLUME_', {0: 'VOLUME_TICK_', 1: 'VOLUME_REAL_', 2: 'VOLUME_NONE'})

# enum ENUM_MODE
OPENCLOSE = 0
LOWHIGH = 1
_enum('ENUM_MODE', {0: 'OPENCLOSE', 1: 'LOWHIGH'})

# ---- inputs and global variables
Candles_Mode = _input('Candles_Mode', OPENCLOSE)  # вариант размера
Candles_Size = _input('Candles_Size', 1000)  # минимальный размер свечи для срабатывания
VolumeType = _input('VolumeType', VOLUME_TICK_)  # объём
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
min_rates_total = 0
dCandles_Size = 0.0

def OnInit():
    global dCandles_Size, min_rates_total
    min_rates_total = _int(NumberofBar) + 1
    dCandles_Size = Candles_Size * Point()
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'StreamСCandles(' + _str(Candles_Size) + ')'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    range_ = 0.0
    size = 0.0
    vol = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(tick_volume, True)
    ArraySetAsSeries(volume, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtCloseBuffer[bar] = 0.0
        ExtHighBuffer[bar] = 0.0
        ExtLowBuffer[bar] = 0.0
        ExtOpenBuffer[bar] = 0.0
        ExtColorBuffer[bar] = 1.0
        _sw1 = Candles_Mode
        if _sw1 == OPENCLOSE:
            size = close[bar] - open[bar]
            range_ = MathAbs(size)
        elif _sw1 == LOWHIGH:
            size = close[bar] - open[bar]
            range_ = high[bar] - low[bar]
        _sw2 = VolumeType
        if _sw2 == VOLUME_TICK_:
            vol = tick_volume[bar]
        elif _sw2 == VOLUME_REAL_:
            vol = volume[bar]
        elif _sw2 == VOLUME_NONE:
            vol = _long(1.0)
        range_ *= float(vol)
        if range_ > dCandles_Size:
            ExtCloseBuffer[bar] = close[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
            ExtOpenBuffer[bar] = open[bar]
            if size < 0.0:
                ExtColorBuffer[bar] = 2.0
            else:
                ExtColorBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    BuySignal('StreamСCandles', ExtColorBuffer, rates_total, prev_calculated, close, spread)
    SellSignal('StreamСCandles', ExtColorBuffer, rates_total, prev_calculated, close, spread)
    return rates_total

def BuySignal(SignalSirname, Arrow, Rates_total, Prev_calculated, Close, Spread):
    global _s_BuySignal_counter
    if Rates_total != Prev_calculated:
        _s_BuySignal_counter = 0
    BuySignal_ = False
    SeriesTest = ArrayGetAsSeries(Arrow)
    index = 0
    if SeriesTest:
        index = _int(NumberofBar)
    else:
        index = Rates_total - _int(NumberofBar) - 1
    if Arrow[index] == 2:
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

def SellSignal(SignalSirname, Arrow, Rates_total, Prev_calculated, Close, Spread):
    global _s_SellSignal_counter
    if Rates_total != Prev_calculated:
        _s_SellSignal_counter = 0
    SellSignal_ = False
    SeriesTest = ArrayGetAsSeries(Arrow)
    index = 0
    if SeriesTest:
        index = _int(NumberofBar)
    else:
        index = Rates_total - _int(NumberofBar) - 1
    if Arrow[index] == 0:
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


class StreamСCandles(_MQL5Indicator):
    name = 'StreamСCandles'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Candles_Mode': _Choice({0: 'размер тела свечи', 1: 'полный размер свечи с тенями'}, default=0),  # вариант размера
        'Candles_Size': 1000,  # минимальный размер свечи для срабатывания
        'VolumeType': _Choice({0: 'VOLUME_TICK', 1: 'VOLUME_REAL', 2: 'Без объёмов'}, default=0),  # объём
        'NumberofBar': 1,  # Номер бара для подачи сигнала
        'SoundON': True,  # Разрешение алерта
        'NumberofAlerts': 2,  # Количество алертов
        'EMailON': False,  # Разрешение почтовой отправки сигнала
        'PushON': False,  # Разрешение отправки сигнала на мобильный
    }

