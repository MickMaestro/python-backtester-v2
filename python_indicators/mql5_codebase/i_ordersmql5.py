"""i-ordersmql5 — converted from MQL5: MQL5 Indicators/i-OrdersMQL5/i-ordersmql5.mq5

Copyright: Copyright 2010, hasayama; Link: mrhasayama@gmail.com; Version: 2.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnTimer is not called (no timer events in a backtest chart).
- OnChartEvent is not called (no chart events).
- Functions not available here: HistoryDealSelect
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2010, hasayama', 'link': 'mrhasayama@gmail.com', 'version': '2.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [], 'name': 'i-ordersmql5', 'source': 'MQL5 Indicators/i-OrdersMQL5/i-ordersmql5.mq5', 'folder': 'i-OrdersMQL5', 'inputs': [{'mql': 'Language', 'py': 'Language', 'param': 'Language', 'type': 'int', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'ShowCurrentPostion', 'py': 'ShowCurrentPostion', 'param': 'ShowCurrentPostion', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'CompactPositionInfo', 'py': 'CompactPositionInfo', 'param': 'CompactPositionInfo', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'ShowDealHistory', 'py': 'ShowDealHistory', 'param': 'ShowDealHistory', 'type': 'bool', 'default': True, 'label': '', 'sinput': False}, {'mql': 'StartTime', 'py': 'StartTime', 'param': None, 'type': 'datetime', 'default': 1262304000, 'label': '', 'sinput': False}, {'mql': 'BuyColor', 'py': 'BuyColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'SellColor', 'py': 'SellColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'InfoColor', 'py': 'InfoColor', 'param': None, 'type': 'color', 'default': 0, 'label': '', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'int', 'default': 8, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

DodgerBlue = 0xFF901E  # MQL4 colour name
Lime = 0x00FF00  # MQL4 colour name
MQL5_PROGRAM_NAME = 0  # MQL5 constant unknown to the converter
Orange = 0x00A5FF  # MQL4 colour name
Red = 0x0000FF  # MQL4 colour name

# enum ENUM_LANGUAGE_PACK
ENG = 0
RUS = 1
_enum('ENUM_LANGUAGE_PACK', {0: 'ENG', 1: 'RUS'})

# ---- inputs and global variables
Language = _input('Language', ENG)
ShowCurrentPostion = _input('ShowCurrentPostion', True)
CompactPositionInfo = _input('CompactPositionInfo', True)
ShowDealHistory = _input('ShowDealHistory', True)
StartTime = _input('StartTime', 1262304000)
FontSize = _input('FontSize', 8)
pre_total_deals = 0
pre_chart_scale = 0
msg_str = ''

def OnInit():
    global msg_str
    attempt = 0
    while True:
        ResetLastError()
        if not EventSetTimer(1):
            msg_str = get_lang('Timer initialization attempt #' + _str(attempt + 1) + 'failed. Error #', 'Неудачная попытка инициализации Таймера №' + _str(attempt + 1) + '. Ошибка №')
            Print(msg_str, GetLastError())
            attempt += 1
        else:
            break
        if attempt > 5:
            msg_str = get_lang('Impossible to initialize Timer.', 'Невозможно инициализировать Таймер.')
            Print(msg_str)
            break
        Sleep(5000)
    return 0

def OnTimer():
    global msg_str, pre_chart_scale, pre_total_deals
    if not ShowDealHistory:
        obj_delete('!##_')
        return
    ResetLastError()
    if not HistorySelect(StartTime, TimeCurrent()):
        msg_str = get_lang('Failed to initialize deals history. Error#', 'Не удалось инициализировать историю сделок. Ошибка №')
        Print(msg_str, GetLastError())
        return
    total_deals = HistoryDealsTotal()
    chart_scale = ChartGetInteger(0, CHART_SCALE)
    if total_deals != pre_total_deals or pre_chart_scale != chart_scale:
        pre_total_deals = total_deals
        pre_chart_scale = chart_scale
        obj_delete('!##_')
        ShowDeals(total_deals)
    return

def OnDeinit(reason):
    obj_delete('!##_')
    obj_delete('#!#_')
    EventKillTimer()
    return

def ShowDeals(total_deals):
    global msg_str
    ticket = 0
    price = 0.0
    time = 0
    symbol = ""
    type_ = 0
    entry = 0
    id_ = 0
    ID = 0
    PRICE = 0.0
    TIME = 0
    name = ""
    for i in range(0, total_deals - 1 + 1):
        ResetLastError()
        ticket = HistoryDealGetTicket(i)
        if ticket <= 0:
            msg_str = get_lang('Imposible to select deal #' + _str(i) + '. Error #', 'Невозможно выбрать сделку №' + _str(i) + '. Ошибка №')
            Print(msg_str, GetLastError())
            return
        symbol = HistoryDealGetString(ticket, DEAL_SYMBOL)
        if symbol != Symbol():
            continue
        price = HistoryDealGetDouble(ticket, DEAL_PRICE)
        time = HistoryDealGetInteger(ticket, DEAL_TIME)
        if price <= 0 or time <= 0:
            continue
        type_ = HistoryDealGetInteger(ticket, DEAL_TYPE)
        entry = HistoryDealGetInteger(ticket, DEAL_ENTRY)
        id_ = HistoryDealGetInteger(ticket, DEAL_POSITION_ID)
        name = '!##_' + MQL5InfoString(MQL5_PROGRAM_NAME) + '_' + _str(ticket) + '_' + _str(id_)
        ObjectCreate(0, name, OBJ_ARROW, 0, time, price, 0, 0)
        if entry == DEAL_ENTRY_IN:
            ObjectSetInteger(0, name, OBJPROP_ARROWCODE, 220)
        elif entry == DEAL_ENTRY_INOUT:
            ObjectSetInteger(0, name, OBJPROP_ARROWCODE, (221 if type_ else 222))
        else:
            ObjectSetInteger(0, name, OBJPROP_ARROWCODE, 219)
        ObjectSetInteger(0, name, OBJPROP_SELECTABLE, 0)
        ObjectSetInteger(0, name, OBJPROP_BACK, 0)
        ObjectSetInteger(0, name, OBJPROP_COLOR, (SellColor if type_ else BuyColor))
        if id_ == ID:
            ObjectCreate(0, name + '_trend', OBJ_TREND, 0, TIME, PRICE, time, price)
            ObjectSetInteger(0, name + '_trend', OBJPROP_COLOR, DodgerBlue)
            ObjectSetInteger(0, name + '_trend', OBJPROP_STYLE, STYLE_DOT)
        if entry == DEAL_ENTRY_IN or entry == DEAL_ENTRY_INOUT:
            ID = id_
            TIME = time
            PRICE = price
    ChartRedraw()

def ShowPosition():
    global msg_str
    pos_id = 0
    volume = 0.0
    pos_op = 0.0
    curr_p = 0.0
    profit = 0.0
    name = '#!#_' + MQL5InfoString(MQL5_PROGRAM_NAME) + '_' + _str(pos_id)
    obj_delete('#!#_')
    if not PositionSelect(Symbol()):
        return
    pos_id = PositionGetInteger(POSITION_IDENTIFIER)
    volume = PositionGetDouble(POSITION_VOLUME)
    pos_op = PositionGetDouble(POSITION_PRICE_OPEN)
    curr_p = PositionGetDouble(POSITION_PRICE_CURRENT)
    profit = PositionGetDouble(POSITION_PROFIT) + PositionGetDouble(POSITION_SWAP)
    shift = 5
    add_shift = _int(NormalizeDouble(_fdiv(ChartGetDouble(0, CHART_PRICE_MAX) - ChartGetDouble(0, CHART_PRICE_MIN), 40 * Point()), 0)) + FontSize
    PRICE = curr_p
    TIME = SeriesInfoInteger(Symbol(), Period(), SERIES_LASTBAR_DATE) + PeriodSeconds(Period())
    if not CompactPositionInfo:
        shift = shift + add_shift
        msg_str = get_lang('Position ID: ' + _str(pos_id), 'ID Позиции: ' + _str(pos_id), False)
        ObjectCreate(0, name, OBJ_TEXT, 0, 0, 0)
        ObjectSetInteger(0, name, OBJPROP_TIME, TIME)
        ObjectSetInteger(0, name, OBJPROP_COLOR, InfoColor)
        ObjectSetInteger(0, name, OBJPROP_FONTSIZE, FontSize)
        ObjectSetDouble(0, name, OBJPROP_PRICE, PRICE - (shift * Point()))
        ObjectSetString(0, name, OBJPROP_TEXT, msg_str)
        shift = shift + add_shift
        msg_str = get_lang('Close Volume: ' + DoubleToString(volume, 2), 'Объем закрытия: ' + DoubleToString(volume, 2), False)
        ObjectCreate(0, name + '1', OBJ_TEXT, 0, 0, 0)
        ObjectSetInteger(0, name + '1', OBJPROP_TIME, TIME)
        ObjectSetInteger(0, name + '1', OBJPROP_COLOR, InfoColor)
        ObjectSetInteger(0, name + '1', OBJPROP_FONTSIZE, FontSize)
        ObjectSetDouble(0, name + '1', OBJPROP_PRICE, PRICE - (shift * Point()))
        ObjectSetString(0, name + '1', OBJPROP_TEXT, msg_str)
        shift = shift + add_shift
        msg_str = get_lang('Position OP: ' + DoubleToString(pos_op, Digits()), 'Цена открытия: ' + DoubleToString(pos_op, Digits()), False)
        ObjectCreate(0, name + '2', OBJ_TEXT, 0, 0, 0)
        ObjectSetInteger(0, name + '2', OBJPROP_TIME, TIME)
        ObjectSetInteger(0, name + '2', OBJPROP_COLOR, InfoColor)
        ObjectSetInteger(0, name + '2', OBJPROP_FONTSIZE, FontSize)
        ObjectSetDouble(0, name + '2', OBJPROP_PRICE, PRICE - (shift * Point()))
        ObjectSetString(0, name + '2', OBJPROP_TEXT, msg_str)
        shift = shift + add_shift
        msg_str = get_lang('Current Price: ' + DoubleToString(curr_p, Digits()), 'Текущая цена: ' + DoubleToString(curr_p, Digits()), False)
        ObjectCreate(0, name + '0', OBJ_TEXT, 0, 0, 0)
        ObjectSetInteger(0, name + '0', OBJPROP_TIME, TIME)
        ObjectSetInteger(0, name + '0', OBJPROP_COLOR, InfoColor)
        ObjectSetInteger(0, name + '0', OBJPROP_FONTSIZE, FontSize)
        ObjectSetDouble(0, name + '0', OBJPROP_PRICE, PRICE - (shift * Point()))
        ObjectSetString(0, name + '0', OBJPROP_TEXT, msg_str)
    shift = shift + (add_shift * 2)
    msg_str = get_lang('Position Profit: ' + DoubleToString(profit, 2), 'Прибыль позиции: ' + DoubleToString(profit, 2), False)
    ObjectCreate(0, name + '4', OBJ_TEXT, 0, 0, 0)
    ObjectSetInteger(0, name + '4', OBJPROP_TIME, TIME)
    ObjectSetInteger(0, name + '4', OBJPROP_COLOR, InfoColor)
    ObjectSetInteger(0, name + '4', OBJPROP_FONTSIZE, FontSize + 2)
    ObjectSetDouble(0, name + '4', OBJPROP_PRICE, PRICE - (shift * Point()))
    ObjectSetString(0, name + '4', OBJPROP_TEXT, msg_str)
    if profit > 0:
        ObjectSetInteger(0, name + '4', OBJPROP_COLOR, BuyColor)
    elif profit < 0:
        ObjectSetInteger(0, name + '4', OBJPROP_COLOR, SellColor)
    ChartRedraw()

def OnChartEvent(id_, lparam, dparam, sparam):
    global msg_str
    if id_ != CHARTEVENT_OBJECT_CLICK:
        return
    if StringFind(sparam, '!##_') < 0:
        return
    if StringFind(sparam, 'trend') > 0:
        return
    if StringFind(sparam, 'text') > 0:
        return
    ticket = 0
    tmp_locker = ''
    tmp_locker = StringSubstr(sparam, 5 + StringLen(MQL5InfoString(MQL5_PROGRAM_NAME)))
    tmp_locker = StringSubstr(tmp_locker, 0, StringFind(tmp_locker, '_'))
    ticket = StringToInteger(tmp_locker)
    PRICE = 0.0
    TIME = 0
    ResetLastError()
    if not _missing('HistoryDealSelect')(ticket):
        msg_str = get_lang('Cannot select deal #' + tmp_locker + '. Error #', 'Невозможно выбрать сделку №' + tmp_locker + '. Ошибка №')
        Print(msg_str, GetLastError())
        return
    PRICE = HistoryDealGetDouble(ticket, DEAL_PRICE)
    TIME = HistoryDealGetInteger(ticket, DEAL_TIME)
    name = sparam + '_text'
    shift = 15
    add_shift = 0
    pos_id = _int(HistoryDealGetInteger(ticket, DEAL_POSITION_ID))
    dprofit = HistoryDealGetDouble(ticket, DEAL_PROFIT) + HistoryDealGetDouble(ticket, DEAL_SWAP)
    entry = 0
    volume = 0.0
    pos_op = 0.0
    pos_cp = 0.0
    profit = 0.0
    ResetLastError()
    if not HistorySelectByPosition(pos_id):
        msg_str = get_lang('Failed to get position data. Error#', 'Не удалось получить данные о позиции. Ошибка №')
        Print(msg_str, GetLastError())
        return
    i = 0
    while i < HistoryDealsTotal():
        ResetLastError()
        ticket = HistoryDealGetTicket(i)
        if ticket <= 0:
            msg_str = get_lang('Imposible to select deal #' + _str(i) + '. Error #', 'Невозможно выбрать сделку №' + _str(i) + '. Ошибка №')
            Print(msg_str, GetLastError())
            i += 1
            continue
        entry = HistoryDealGetInteger(ticket, DEAL_ENTRY)
        if entry == DEAL_ENTRY_IN:
            pos_op = HistoryDealGetDouble(ticket, DEAL_PRICE)
            i += 1
            continue
        if entry == DEAL_ENTRY_INOUT:
            profit = profit + HistoryDealGetDouble(ticket, DEAL_PROFIT) + HistoryDealGetDouble(ticket, DEAL_SWAP)
            i += 1
            continue
        if entry == DEAL_ENTRY_OUT:
            volume = HistoryDealGetDouble(ticket, DEAL_VOLUME)
            pos_cp = HistoryDealGetDouble(ticket, DEAL_PRICE)
            profit = profit + HistoryDealGetDouble(ticket, DEAL_PROFIT) + HistoryDealGetDouble(ticket, DEAL_SWAP)
            i += 1
            continue
        i += 1
    if ObjectFind(0, name) < 0:
        add_shift = _int(NormalizeDouble(_fdiv(ChartGetDouble(0, CHART_PRICE_MAX) - ChartGetDouble(0, CHART_PRICE_MIN), 40 * Point()), 0)) + FontSize
        shift = shift + add_shift
        msg_str = get_lang('Position ID: ' + _str(pos_id), 'ID Позиции: ' + _str(pos_id), False)
        ObjectCreate(0, name, OBJ_TEXT, 0, 0, 0)
        ObjectSetInteger(0, name, OBJPROP_TIME, TIME)
        ObjectSetInteger(0, name, OBJPROP_COLOR, InfoColor)
        ObjectSetInteger(0, name, OBJPROP_FONTSIZE, FontSize)
        ObjectSetDouble(0, name, OBJPROP_PRICE, PRICE - (shift * Point()))
        ObjectSetString(0, name, OBJPROP_TEXT, msg_str)
        shift = shift + add_shift
        msg_str = get_lang('Close Volume: ' + DoubleToString(volume, 2), 'Объем закрытия: ' + DoubleToString(volume, 2), False)
        ObjectCreate(0, name + '1', OBJ_TEXT, 0, 0, 0)
        ObjectSetInteger(0, name + '1', OBJPROP_TIME, TIME)
        ObjectSetInteger(0, name + '1', OBJPROP_COLOR, InfoColor)
        ObjectSetInteger(0, name + '1', OBJPROP_FONTSIZE, FontSize)
        ObjectSetDouble(0, name + '1', OBJPROP_PRICE, PRICE - (shift * Point()))
        ObjectSetString(0, name + '1', OBJPROP_TEXT, msg_str)
        shift = shift + add_shift
        msg_str = get_lang('Position OP: ' + DoubleToString(pos_op, Digits()), 'Цена открытия: ' + DoubleToString(pos_op, Digits()), False)
        ObjectCreate(0, name + '2', OBJ_TEXT, 0, 0, 0)
        ObjectSetInteger(0, name + '2', OBJPROP_TIME, TIME)
        ObjectSetInteger(0, name + '2', OBJPROP_COLOR, InfoColor)
        ObjectSetInteger(0, name + '2', OBJPROP_FONTSIZE, FontSize)
        ObjectSetDouble(0, name + '2', OBJPROP_PRICE, PRICE - (shift * Point()))
        ObjectSetString(0, name + '2', OBJPROP_TEXT, msg_str)
        shift = shift + add_shift
        msg_str = get_lang('Position CP: ' + DoubleToString(pos_cp, Digits()), 'Цена закрытия: ' + DoubleToString(pos_cp, Digits()), False)
        ObjectCreate(0, name + '0', OBJ_TEXT, 0, 0, 0)
        ObjectSetInteger(0, name + '0', OBJPROP_TIME, TIME)
        ObjectSetInteger(0, name + '0', OBJPROP_COLOR, InfoColor)
        ObjectSetInteger(0, name + '0', OBJPROP_FONTSIZE, FontSize)
        ObjectSetDouble(0, name + '0', OBJPROP_PRICE, PRICE - (shift * Point()))
        ObjectSetString(0, name + '0', OBJPROP_TEXT, msg_str)
        shift = shift + (add_shift * 2)
        msg_str = get_lang('Deal Profit: ' + DoubleToString(dprofit, 2), 'Прибыль сделки: ' + DoubleToString(dprofit, 2), False)
        ObjectCreate(0, name + '4', OBJ_TEXT, 0, 0, 0)
        ObjectSetInteger(0, name + '4', OBJPROP_TIME, TIME)
        ObjectSetInteger(0, name + '4', OBJPROP_COLOR, InfoColor)
        ObjectSetInteger(0, name + '4', OBJPROP_FONTSIZE, FontSize)
        ObjectSetDouble(0, name + '4', OBJPROP_PRICE, PRICE - (shift * Point()))
        ObjectSetString(0, name + '4', OBJPROP_TEXT, msg_str)
        if dprofit > 0:
            ObjectSetInteger(0, name + '4', OBJPROP_COLOR, BuyColor)
        elif dprofit < 0:
            ObjectSetInteger(0, name + '4', OBJPROP_COLOR, SellColor)
        shift = shift + add_shift
        msg_str = get_lang('Position Profit: ' + DoubleToString(profit, 2), 'Прибыль позиции: ' + DoubleToString(profit, 2), False)
        ObjectCreate(0, name + '3', OBJ_TEXT, 0, 0, 0)
        ObjectSetInteger(0, name + '3', OBJPROP_TIME, TIME)
        ObjectSetInteger(0, name + '3', OBJPROP_COLOR, InfoColor)
        ObjectSetInteger(0, name + '3', OBJPROP_FONTSIZE, FontSize + 2)
        ObjectSetDouble(0, name + '3', OBJPROP_PRICE, PRICE - (shift * Point()))
        ObjectSetString(0, name + '3', OBJPROP_TEXT, msg_str)
        if profit > 0:
            ObjectSetInteger(0, name + '3', OBJPROP_COLOR, BuyColor)
        elif profit < 0:
            ObjectSetInteger(0, name + '3', OBJPROP_COLOR, SellColor)
    else:
        obj_delete(sparam + '_text')
    ChartRedraw()

def obj_delete(prefix):
    name = ''
    total = ObjectsTotal(0) - 1
    for i in range(total, 0 - 1, -1):
        name = ObjectName(0, i)
        if StringFind(name, prefix) >= 0:
            ObjectDelete(0, name)

def get_lang(eng, rus, add_info=True):
    info = ''
    if add_info:
        info = MQL5InfoString(MQL5_PROGRAM_NAME) + '(' + Symbol() + '): '
    if Language == ENG:
        return info + eng
    if Language == RUS:
        return info + rus
    return info + eng

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if not ShowCurrentPostion:
        obj_delete('#!#_')
        return rates_total
    ShowPosition()
    return rates_total

# ---- global variables initialised from expressions
BuyColor = _input('BuyColor', _uint(Lime))
SellColor = _input('SellColor', _uint(Red))
InfoColor = _input('InfoColor', _uint(Orange))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class IOrdersmql5(_MQL5Indicator):
    name = 'i-ordersmql5'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Language': _Choice({0: 'ENG', 1: 'RUS'}, default=0),
        'ShowCurrentPostion': True,
        'CompactPositionInfo': True,
        'ShowDealHistory': True,
        'FontSize': 8,
    }

