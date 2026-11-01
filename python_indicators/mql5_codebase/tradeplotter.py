"""TradePlotter — converted from MQL5: MQL5 Indicators/TradePlotter/TradePlotter.mq5

Agianto Simanullang
Copyright: Copyright 2022, MetaQuotes Ltd.; Link: https://www.mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2022, MetaQuotes Ltd.', 'link': 'https://www.mql5.com', 'version': '1.00', 'window': 'chart', 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Agianto Simanullang'], 'name': 'TradePlotter', 'source': 'MQL5 Indicators/TradePlotter/TradePlotter.mq5', 'folder': 'TradePlotter', 'inputs': [{'mql': 'HistoryInMonths', 'py': 'HistoryInMonths', 'param': 'HistoryInMonths', 'type': 'double', 'default': 3.0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
HistoryInMonths = _input('HistoryInMonths', 3.0)
count_current_ordes_flaq = 0
count_history_orders_flaq = 0
VariableIn = Arr(0, "", dims=(8,))
VariableOut = Arr(0, "", dims=(8,))

def OnInit():
    OnDeinit(1)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global count_current_ordes_flaq, count_history_orders_flaq
    i = 0
    count_current_ordes = 0
    count_history_orders = 0
    obj_name = ''
    str_order_type = ""
    count_current_ordes = PositionsTotal()
    if count_current_ordes_flaq != count_current_ordes:
        i = count_current_ordes - 1
        for i in range(i, 0 - 1, -1):
            if PositionGetTicket(i) > 0:
                if PositionGetString(POSITION_SYMBOL) == Symbol() and PositionGetInteger(POSITION_TYPE) <= 1:
                    str_order_type = ('buy' if (PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY) else 'sell')
                    obj_name = '#' + IntegerToString(PositionGetInteger(POSITION_TICKET)) + ' ' + str_order_type + ' ' + DoubleToString(PositionGetDouble(POSITION_VOLUME), 2) + ' ' + PositionGetString(POSITION_SYMBOL) + ' at ' + DoubleToString(PositionGetDouble(POSITION_PRICE_OPEN), Digits()) + ', ' + PositionGetString(POSITION_SYMBOL) + ''
                    if PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY:
                        ObjectCreate(0, obj_name, OBJ_ARROW_BUY, 0, PositionGetInteger(POSITION_TIME), PositionGetDouble(POSITION_PRICE_OPEN))
                        ObjectSetInteger(0, obj_name, OBJPROP_COLOR, clrBlue)
                    else:
                        ObjectCreate(0, obj_name, OBJ_ARROW_SELL, 0, PositionGetInteger(POSITION_TIME), PositionGetDouble(POSITION_PRICE_OPEN))
                        ObjectSetInteger(0, obj_name, OBJPROP_COLOR, clrRed)
        else:
            i = _range_end(i, 0 - 1, -1)
        count_current_ordes_flaq = count_current_ordes
        ChartRedraw(0)
    HistorySelect(_long(TimeCurrent() - (PeriodSeconds(PERIOD_MN1) * HistoryInMonths)), TimeCurrent())
    count_history_orders = HistoryDealsTotal()
    if count_history_orders_flaq != count_history_orders:
        ArrayFree(VariableIn)
        ArrayFree(VariableOut)
        ArrayResize(VariableIn, count_history_orders)
        ArrayResize(VariableOut, count_history_orders)
        obj_name = ''
        ticket = 0
        x = 0
        y = 0
        i = count_history_orders - 1
        for i in range(i, 0 - 1, -1):
            ticket = HistoryDealGetTicket(i)
            if ticket > 0:
                if HistoryDealGetString(ticket, DEAL_SYMBOL) == Symbol() and HistoryDealGetInteger(ticket, DEAL_TYPE) <= 1:
                    if HistoryDealGetInteger(ticket, DEAL_ENTRY) == DEAL_ENTRY_IN:
                        VariableIn[x][0] = IntegerToString(HistoryDealGetInteger(ticket, DEAL_TICKET))
                        VariableIn[x][1] = HistoryDealGetString(ticket, DEAL_SYMBOL)
                        VariableIn[x][2] = IntegerToString(HistoryDealGetInteger(ticket, DEAL_TYPE))
                        VariableIn[x][3] = TimeToString(HistoryDealGetInteger(ticket, DEAL_TIME), TIME_DATE | TIME_MINUTES)
                        VariableIn[x][4] = DoubleToString(HistoryDealGetDouble(ticket, DEAL_PRICE), Digits())
                        VariableIn[x][5] = DoubleToString(HistoryDealGetDouble(ticket, DEAL_PROFIT), 2)
                        VariableIn[x][6] = DoubleToString(HistoryDealGetDouble(ticket, DEAL_VOLUME), 2)
                        VariableIn[x][7] = IntegerToString(HistoryDealGetInteger(ticket, DEAL_POSITION_ID))
                        x += 1
                    if HistoryDealGetInteger(ticket, DEAL_ENTRY) == DEAL_ENTRY_OUT:
                        VariableOut[y][0] = IntegerToString(HistoryDealGetInteger(ticket, DEAL_TICKET))
                        VariableOut[y][1] = HistoryDealGetString(ticket, DEAL_SYMBOL)
                        VariableOut[y][2] = IntegerToString(HistoryDealGetInteger(ticket, DEAL_TYPE))
                        VariableOut[y][3] = TimeToString(HistoryDealGetInteger(ticket, DEAL_TIME), TIME_DATE | TIME_MINUTES)
                        VariableOut[y][4] = DoubleToString(HistoryDealGetDouble(ticket, DEAL_PRICE), Digits())
                        VariableOut[y][5] = DoubleToString(HistoryDealGetDouble(ticket, DEAL_PROFIT), 2)
                        VariableOut[y][6] = DoubleToString(HistoryDealGetDouble(ticket, DEAL_VOLUME), 2)
                        VariableOut[y][7] = IntegerToString(HistoryDealGetInteger(ticket, DEAL_POSITION_ID))
                        y += 1
        else:
            i = _range_end(i, 0 - 1, -1)
        count_history_orders_flaq = count_history_orders
        profit_in = 0.0
        profit_out = 0.0
        price_in = 0.0
        price_out = 0.0
        volume_in = 0.0
        volume_out = 0.0
        symbol_in = ''
        symbol_out = ''
        ticket_in = 0
        ticket_out = 0
        time_in = 0
        time_out = 0
        order_type_in = -1
        order_type_out = -1
        j = 0
        i = 0
        for i in range(i, count_history_orders):
            if StringToInteger(VariableOut[i][0]) == 0 or StringToInteger(VariableOut[i][0]) == 0:
                continue
            ticket_out = StringToInteger(VariableOut[i][0])
            symbol_out = VariableOut[i][1]
            order_type_out = StringToInteger(VariableOut[i][2])
            time_out = StringToInteger(VariableOut[i][3])
            price_out = StringToDouble(VariableOut[i][4])
            profit_out = StringToDouble(VariableOut[i][5])
            volume_out = StringToDouble(VariableOut[i][6])
            obj_name = '#' + IntegerToString(ticket_out) + ' ' + ('buy' if (order_type_out == 0) else 'sell') + ' ' + DoubleToString(volume_out, 2) + ' ' + symbol_out + ' at ' + DoubleToString(price_out, Digits()) + ', profit ' + DoubleToString(profit_out, 2) + ''
            if order_type_out == 0:
                if ObjectFind(0, obj_name) < 0:
                    ObjectCreate(0, obj_name, OBJ_ARROW_BUY, 0, time_out, price_out)
                    ObjectSetInteger(0, obj_name, OBJPROP_COLOR, 0xAC5F03)
            else:
                if ObjectFind(0, obj_name) < 0:
                    ObjectCreate(0, obj_name, OBJ_ARROW_SELL, 0, time_out, price_out)
                    ObjectSetInteger(0, obj_name, OBJPROP_COLOR, 0x1D44E1)
        else:
            i = _range_end(i, count_history_orders, 1)
        j = 0
        for j in range(j, count_history_orders):
            if StringToInteger(VariableIn[j][0]) == 0 or StringToInteger(VariableIn[j][0]) == 0:
                continue
            ticket_in = StringToInteger(VariableIn[j][0])
            symbol_in = VariableIn[j][1]
            order_type_in = StringToInteger(VariableIn[j][2])
            time_in = StringToInteger(VariableIn[j][3])
            price_in = StringToDouble(VariableIn[j][4])
            profit_in = StringToDouble(VariableIn[j][5])
            volume_in = StringToDouble(VariableIn[j][6])
            obj_name = '#' + IntegerToString(ticket_in) + ' ' + ('buy' if (order_type_in == 0) else 'sell') + ' ' + DoubleToString(volume_in, 2) + ' ' + symbol_in + ' at ' + DoubleToString(price_in, Digits()) + ', ' + symbol_in + ''
            if order_type_in == 0:
                if ObjectFind(0, obj_name) < 0:
                    ObjectCreate(0, obj_name, OBJ_ARROW_BUY, 0, time_in, price_in)
                    ObjectSetInteger(0, obj_name, OBJPROP_COLOR, 0xAC5F03)
            else:
                if ObjectFind(0, obj_name) < 0:
                    ObjectCreate(0, obj_name, OBJ_ARROW_SELL, 0, time_in, price_in)
                    ObjectSetInteger(0, obj_name, OBJPROP_COLOR, 0x1D44E1)
        else:
            j = _range_end(j, count_history_orders, 1)
        i = 0
        for i in range(i, count_history_orders):
            if StringToInteger(VariableOut[i][0]) == 0 or StringToInteger(VariableOut[i][0]) == 0:
                continue
            j = 0
            for j in range(j, count_history_orders):
                if StringToInteger(VariableIn[j][0]) == 0 or StringToInteger(VariableIn[j][0]) == 0:
                    continue
                if VariableOut[i][7] == VariableIn[j][7]:
                    obj_name = '#' + VariableIn[j][0] + ' -> #' + VariableOut[i][0] + ', profit ' + DoubleToString(StringToDouble(VariableOut[i][5]), 2) + ', ' + VariableOut[i][1]
                    if ObjectFind(0, obj_name) < 0:
                        ObjectCreate(0, obj_name, OBJ_TREND, 0, StringToTime(VariableIn[j][3]), StringToDouble(VariableIn[j][4]), StringToTime(VariableOut[i][3]), StringToDouble(VariableOut[i][4]))
                        ObjectSetInteger(0, obj_name, OBJPROP_STYLE, STYLE_DOT)
                        ObjectSetInteger(0, obj_name, OBJPROP_WIDTH, 1)
                        ObjectSetInteger(0, obj_name, OBJPROP_RAY_RIGHT, False)
                        ObjectSetInteger(0, obj_name, OBJPROP_COLOR, (0xAC5F03 if (StringToInteger(VariableIn[j][2]) == 0) else 0x1D44E1))
            else:
                j = _range_end(j, count_history_orders, 1)
        else:
            i = _range_end(i, count_history_orders, 1)
        ArrayFree(VariableIn)
        ArrayFree(VariableOut)
        ChartRedraw(0)
    return rates_total

def OnDeinit(reason):
    ObjTotal = ObjectsTotal(0)
    for i in range(ObjTotal, 0 - 1, -1):
        if StringSubstr(ObjectName(0, i), 0, 2) == '#':
            ObjectDelete(0, ObjectName(0, i))


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TradePlotter(_MQL5Indicator):
    name = 'TradePlotter'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'HistoryInMonths': 3.0,
    }

