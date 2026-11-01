"""PriceAlert_V2 — converted from MQL5: MQL5 Indicators/PriceAlert_V2/PriceAlert_V2.mq5

Индикатор подает сигналы при пробое горизонтального уровня
Copyright: Copyright © 2018, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.10

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.10', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Индикатор подает сигналы при пробое горизонтального уровня'], 'name': 'PriceAlert_V2', 'source': 'MQL5 Indicators/PriceAlert_V2/PriceAlert_V2.mq5', 'folder': 'PriceAlert_V2', 'inputs': [{'mql': 'level_name', 'py': 'level_name', 'param': None, 'type': 'string', 'default': 'Price_Level_1', 'label': 'Имя уровня срабатывания', 'sinput': False}, {'mql': 'level_comment', 'py': 'level_comment', 'param': None, 'type': 'string', 'default': 'уровень срабатывания', 'label': 'Комментарий к уровню срабатывания', 'sinput': False}, {'mql': 'active_level_color', 'py': 'active_level_color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Цвет активированного уровня', 'sinput': False}, {'mql': 'inactive_level_color', 'py': 'inactive_level_color', 'param': None, 'type': 'color', 'default': 0, 'label': 'Цвет сработавшего уровня', 'sinput': False}, {'mql': 'level_style', 'py': 'level_style', 'param': 'level_style', 'type': 'int', 'default': 0, 'label': 'Стиль уровня срабатывания', 'sinput': False}, {'mql': 'level_width', 'py': 'level_width', 'param': 'level_width', 'type': 'int', 'default': 3, 'label': 'Толщина уровня срабатывания', 'sinput': False}, {'mql': 'AlertON', 'py': 'AlertON', 'param': 'AlertON', 'type': 'bool', 'default': True, 'label': 'Разрешение подачи алерта', 'sinput': False}, {'mql': 'AlertTotal', 'py': 'AlertTotal', 'param': 'AlertTotal', 'type': 'uint', 'default': 3, 'label': 'количество сигналов', 'sinput': False}, {'mql': 'EMailON', 'py': 'EMailON', 'param': 'EMailON', 'type': 'bool', 'default': False, 'label': 'Разрешение почтовой отправки сигнала', 'sinput': False}, {'mql': 'PushON', 'py': 'PushON', 'param': 'PushON', 'type': 'bool', 'default': False, 'label': 'Разрешение отправки сигнала на мобильный', 'sinput': False}, {'mql': 'Deletelevel', 'py': 'Deletelevel', 'param': 'Deletelevel', 'type': 'bool', 'default': True, 'label': 'удаление настройки уровня при смене таймфрейма', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

Gray = 0x808080  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

# enum ENUM_WIDTH
w_1 = 1
w_2 = 2
w_3 = 3
w_4 = 4
w_5 = 5
_enum('ENUM_WIDTH', {1: 'w_1', 2: 'w_2', 3: 'w_3', 4: 'w_4', 5: 'w_5'})

# ---- inputs and global variables
level_name = _input('level_name', 'Price_Level_1')  # Имя уровня срабатывания
level_comment = _input('level_comment', 'уровень срабатывания')  # Комментарий к уровню срабатывания
level_style = _input('level_style', STYLE_SOLID)  # Стиль уровня срабатывания
level_width = _input('level_width', w_3)  # Толщина уровня срабатывания
AlertON = _input('AlertON', True)  # Разрешение подачи алерта
AlertTotal = _input('AlertTotal', 3)  # количество сигналов
EMailON = _input('EMailON', False)  # Разрешение почтовой отправки сигнала
PushON = _input('PushON', False)  # Разрешение отправки сигнала на мобильный
Deletelevel = _input('Deletelevel', True)  # удаление настройки уровня при смене таймфрейма

def CreateHline(chart_id, name, nwin, price, Color, style, width, background, text):
    ObjectCreate(chart_id, name, OBJ_HLINE, nwin, 0, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_STYLE, style)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, width)
    ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, background)
    ObjectSetInteger(chart_id, name, OBJPROP_RAY, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTED, True)
    ObjectSetInteger(chart_id, name, OBJPROP_SELECTABLE, True)
    ObjectSetInteger(chart_id, name, OBJPROP_ZORDER, True)

def SetHline(chart_id, name, nwin, price, Color, style, width, background, text):
    if ObjectFind(chart_id, name) == -1:
        CreateHline(chart_id, name, nwin, price, Color, style, width, background, text)
    else:
        ObjectSetString(chart_id, name, OBJPROP_TEXT, text)
        ObjectMove(chart_id, name, 0, 0, price)
        ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)

def OnInit():
    if ObjectFind(0, level_name) == -1:
        CreateHline(0, level_name, 0, 0.0, inactive_level_color, level_style, level_width, False, level_comment)

def OnDeinit(reason):
    if Deletelevel:
        ObjectDelete(0, level_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_count, _s_OnCalculate_oldlevel, _s_OnCalculate_startprice
    level = 0.0
    price0 = close[rates_total - 1]
    if ObjectFind(0, level_name) == -1:
        if _s_OnCalculate_count:
            CreateHline(0, level_name, 0, _s_OnCalculate_oldlevel, active_level_color, level_style, level_width, False, level_comment)
        else:
            CreateHline(0, level_name, 0, _s_OnCalculate_oldlevel, inactive_level_color, level_style, level_width, False, level_comment)
    if prev_calculated > rates_total or prev_calculated <= 0:
        level = ObjectGetDouble(0, level_name, OBJPROP_PRICE)
        if not level:
            level = price0
            SetHline(0, level_name, 0, level, inactive_level_color, level_style, level_width, False, level_comment)
            _s_OnCalculate_oldlevel = level
            _s_OnCalculate_count = 0
    level = ObjectGetDouble(0, level_name, OBJPROP_PRICE)
    if level != _s_OnCalculate_oldlevel:
        SetHline(0, level_name, 0, level, active_level_color, level_style, level_width, False, level_comment)
        _s_OnCalculate_oldlevel = level
        _s_OnCalculate_count = AlertTotal
        _s_OnCalculate_startprice = price0
    if _s_OnCalculate_count:
        if price0 >= level and _s_OnCalculate_startprice < level:
            BuySignal('PriceAlert_V2: Произошел пробой ценового уровня ' + DoubleToString(level, Digits()), rates_total, prev_calculated, close, spread)
            _s_OnCalculate_count -= 1
            if not _s_OnCalculate_count:
                SetHline(0, level_name, 0, level, inactive_level_color, level_style, level_width, False, level_comment)
    if _s_OnCalculate_count:
        if price0 <= level and _s_OnCalculate_startprice > level:
            SellSignal('PriceAlert_V2: Произошел пробой ценового уровня ' + DoubleToString(level, Digits()), rates_total, prev_calculated, close, spread)
            _s_OnCalculate_count -= 1
            if not _s_OnCalculate_count:
                SetHline(0, level_name, 0, level, inactive_level_color, level_style, level_width, False, level_comment)
    return rates_total

def BuySignal(SignalSirname, Rates_total, Prev_calculated, Close, Spread):
    global _s_BuySignal_counter
    if Rates_total != Prev_calculated:
        _s_BuySignal_counter = 0
    BuySignal_ = True
    SeriesTest = ArrayGetAsSeries(Close)
    index = 0
    if SeriesTest:
        index = 0
    else:
        index = Rates_total - 1
    if BuySignal_ and _s_BuySignal_counter <= AlertTotal:
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
        if AlertON:
            Alert(SignalSirname)
            Alert('BUY signal \n Ask=', Ask, '\n Bid=', Bid, '\n currtime=', text, '\n Symbol=', Symbol(), ' Period=', sPeriod)
        if EMailON:
            SendMail(SignalSirname + ': BUY signal alert', 'BUY signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
        if PushON:
            SendNotification(SignalSirname)
            SendNotification('BUY signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)

def SellSignal(SignalSirname, Rates_total, Prev_calculated, Close, Spread):
    global _s_SellSignal_counter
    if Rates_total != Prev_calculated:
        _s_SellSignal_counter = 0
    SellSignal_ = True
    SeriesTest = ArrayGetAsSeries(Close)
    index = 0
    if SeriesTest:
        index = 0
    else:
        index = Rates_total - 1
    if SellSignal_ and _s_SellSignal_counter <= AlertTotal:
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
        if AlertON:
            Alert(SignalSirname)
            Alert('SELL signal \n Ask=', Ask, '\n Bid=', Bid, '\n currtime=', text, '\n Symbol=', Symbol(), ' Period=', sPeriod)
        if EMailON:
            SendMail(SignalSirname + ': SELL signal alert', 'SELL signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)
        if PushON:
            SendNotification(SignalSirname)
            SendNotification('SELL signal at Ask=' + sAsk + ', Bid=' + sBid + ', Date=' + text + ' Symbol=' + Symbol() + ' Period=' + sPeriod)

def GetStringTimeframe(timeframe):
    return StringSubstr(EnumToString(timeframe, 'ENUM_TIMEFRAMES'), 7, -1)

# ---- global variables initialised from expressions
active_level_color = _input('active_level_color', _uint(Red))  # Цвет активированного уровня
inactive_level_color = _input('inactive_level_color', _uint(Gray))  # Цвет сработавшего уровня

# ---- static local variables
_s_OnCalculate_startprice = 0.0
_s_OnCalculate_oldlevel = 0.0
_s_OnCalculate_count = 0
_s_BuySignal_counter = 0
_s_SellSignal_counter = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class PriceAlertV2(_MQL5Indicator):
    name = 'PriceAlert_V2'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'level_style': _Choice({0: 'Solid', 1: 'Dash', 2: 'Dot', 3: 'Dashdot', 4: 'Dashdotdot'}, default=0),  # Стиль уровня срабатывания
        'level_width': _Choice({1: '1', 2: '2', 3: '3', 4: '4', 5: '5'}, default=3),  # Толщина уровня срабатывания
        'AlertON': True,  # Разрешение подачи алерта
        'AlertTotal': 3,  # количество сигналов
        'EMailON': False,  # Разрешение почтовой отправки сигнала
        'PushON': False,  # Разрешение отправки сигнала на мобильный
        'Deletelevel': True,  # удаление настройки уровня при смене таймфрейма
    }

