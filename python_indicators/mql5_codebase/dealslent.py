"""DealsLent — converted from MQL5: MQL5 Indicators/Feed of all deals/DealsLent.mq5

Copyright: Copyright 2016, prostotrader; Link: https://www.mql5.com; Version: 1.02

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2016, prostotrader', 'link': 'https://www.mql5.com', 'version': '1.02', 'window': 'separate', 'indicator_buffers': 4, 'indicator_plots': 2}, 'types': {1: 1, 2: 1}, 'colors': {1: [12695295], 2: [16436871]}, 'widths': {1: 1, 2: 1}, 'styles': {1: 0, 2: 0}, 'labels': {1: 'Sell', 2: 'Buy'}, 'levels': [], 'description': [], 'name': 'DealsLent', 'source': 'MQL5 Indicators/Feed of all deals/DealsLent.mq5', 'folder': 'Feed of all deals', 'inputs': [{'mql': 'ActSize', 'py': 'ActSize', 'param': 'ActSize', 'type': 'int', 'default': 30, 'label': 'Размер актуальной истории в буферах индикатора', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

COPY_TICKS_TRADE = 0  # MQL5 constant unknown to the converter
TICK_FLAG_BUY = 0  # MQL5 constant unknown to the converter
TICK_FLAG_SELL = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
ActSize = _input('ActSize', 30)  # Размер актуальной истории в буферах индикатора
SellBuffer = Arr(0, 0.0)
BuyBuffer = Arr(0, 0.0)
SellVol = Arr(0, 0.0)
BuyVol = Arr(0, 0.0)
sell_deals = 0
buy_deals = 0
mem_deals = 0  # Предыдущее общ. кол-во сделок с последнем временем
last_deals = 0  # Общ. кол-ва сделок с последним временем
sell_vol = 0
buy_vol = 0
start_time = 0  # Время получения пакета тиков
mem_time = 0
event_cnt = 0  # Переменная для вызова функции OnCalculate
use_book = False  # Флаг, что индикатор добавил стакан

def OnInit():
    global event_cnt, mem_time, start_time, use_book
    mem_time = 0
    start_time = 0
    event_cnt = 0
    book = Arr(0, 0, factory=MqlBookInfo)
    if not MarketBookGet(Symbol(), book):
        if not MarketBookAdd(Symbol()):
            Print('OnInit', ': Стакан символа ' + Symbol() + ' не добавден!')
            return INIT_FAILED
        else:
            use_book = True
    else:
        use_book = False
    cur_bars = Bars(Symbol(), PERIOD_CURRENT)
    if cur_bars < (ActSize + 1):
        Print('OnInit', ': Не достаточно баров на текущем таймфрейме! должно быть не менее ', ActSize + 1)
        return INIT_FAILED
    if cur_bars < 2:
        Print('OnInit', ': Не достаточно баров на текущем таймфрейме! Должно быть не менее 2.')
        return INIT_FAILED
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'DealsLent')
    SetIndexBuffer(0, SellBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(SellBuffer, True)
    SetIndexBuffer(1, BuyBuffer, INDICATOR_DATA)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(BuyBuffer, True)
    SetIndexBuffer(2, SellVol, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(SellVol, True)
    SetIndexBuffer(3, BuyVol, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(BuyVol, True)
    window = ChartWindowFind(ChartID(), 'DealsLent')
    ObjectCreate(ChartID(), 'Label_1', OBJ_LABEL, window, 0, 0)
    ObjectCreate(ChartID(), 'Label_2', OBJ_LABEL, window, 0, 0)
    ObjectCreate(ChartID(), 'Label_3', OBJ_LABEL, window, 0, 0)
    ObjectCreate(ChartID(), 'Label_4', OBJ_LABEL, window, 0, 0)
    ObjectSetInteger(ChartID(), 'Label_1', OBJPROP_YDISTANCE, 30)
    ObjectSetInteger(ChartID(), 'Label_1', OBJPROP_XDISTANCE, 0)
    ObjectSetInteger(ChartID(), 'Label_2', OBJPROP_YDISTANCE, 60)
    ObjectSetInteger(ChartID(), 'Label_2', OBJPROP_XDISTANCE, 0)
    ObjectSetInteger(ChartID(), 'Label_3', OBJPROP_YDISTANCE, 15)
    ObjectSetInteger(ChartID(), 'Label_3', OBJPROP_XDISTANCE, 0)
    ObjectSetInteger(ChartID(), 'Label_4', OBJPROP_YDISTANCE, 45)
    ObjectSetInteger(ChartID(), 'Label_4', OBJPROP_XDISTANCE, 0)
    ObjectSetInteger(ChartID(), 'Label_1', OBJPROP_COLOR, clrLightPink)
    ObjectSetInteger(ChartID(), 'Label_2', OBJPROP_COLOR, clrLightSkyBlue)
    ObjectSetInteger(ChartID(), 'Label_3', OBJPROP_COLOR, clrLightPink)
    ObjectSetInteger(ChartID(), 'Label_4', OBJPROP_COLOR, clrLightSkyBlue)
    ObjectSetString(ChartID(), 'Label_1', OBJPROP_TEXT, 'Сум. объём Sell: 0')
    ObjectSetString(ChartID(), 'Label_2', OBJPROP_TEXT, 'Сум. объём Buy: 0')
    ObjectSetString(ChartID(), 'Label_3', OBJPROP_TEXT, 'Сум. кол-во Sell: 0')
    ObjectSetString(ChartID(), 'Label_4', OBJPROP_TEXT, 'Сум. кол-во Buy: 0')
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    ChartRedraw(ChartID())
    return INIT_SUCCEEDED

def OnDeinit(reason):
    if use_book:
        MarketBookRelease(Symbol())
    ObjectDelete(ChartID(), 'Label_1')
    ObjectDelete(ChartID(), 'Label_2')
    ObjectDelete(ChartID(), 'Label_3')
    ObjectDelete(ChartID(), 'Label_4')
    if reason == REASON_INITFAILED:
        window = ChartWindowFind(ChartID(), 'DealsLent')
        ChartIndicatorDelete(ChartID(), window, 'DealsLent')

def OnBookEvent(symbol):
    global buy_deals, buy_vol, last_deals, sell_deals, sell_vol, start_time
    if symbol == Symbol():
        if start_time == 0:
            if CopyTicks(Symbol(), ticks, COPY_TICKS_TRADE, 0, 1) == 1:
                start_time = _ulong(ticks[0].time_msc)
        else:
            sell_deals = 0
            buy_deals = 0
            sell_vol = 0
            buy_vol = 0
            last_deals = 0
            result = CopyTicks(Symbol(), ticks, COPY_TICKS_TRADE, start_time, 0)
            if result > 0:
                for i in range(0, result):
                    if (ticks[i].flags & TICK_FLAG_BUY) == TICK_FLAG_BUY:
                        buy_deals += 1
                        buy_vol += ticks[i].volume
                        if ticks[i].time_msc == ticks[result - 1].time_msc:
                            last_deals += 1
                    elif (ticks[i].flags & TICK_FLAG_SELL) == TICK_FLAG_SELL:
                        sell_deals += 1
                        sell_vol += ticks[i].volume
                        if ticks[i].time_msc == ticks[result - 1].time_msc:
                            last_deals += 1
                start_time = _ulong(ticks[result - 1].time_msc + 1)
                if sell_deals == 0 and buy_deals == 0:
                    return
                price = Arr(0, 0.0)
                OnCalculate(event_cnt, event_cnt, -111, price)

def OnCalculate(rates_total, prev_calculated, begin, price):
    global buy_deals, buy_vol, event_cnt, mem_deals, mem_time, sell_deals, sell_vol
    if prev_calculated == 0:
        ArrayInitialize(SellBuffer, EMPTY_VALUE)
        ArrayInitialize(BuyBuffer, EMPTY_VALUE)
        ArrayInitialize(SellVol, EMPTY_VALUE)
        ArrayInitialize(BuyVol, EMPTY_VALUE)
    else:
        if begin == -111:
            a_size = ArraySize(ticks)
            if mem_time != ticks[0].time_msc and mem_time != 0:
                t_ticks = Arr(0, 0, factory=MqlTick)
                new_deals = 0
                add_sell = 0
                add_buy = 0
                add_s_vol = 0
                add_b_vol = 0
                result = CopyTicks(Symbol(), t_ticks, COPY_TICKS_TRADE, mem_time, 0)
                if result > 0:
                    for i in range(0, result):
                        if t_ticks[i].time_msc == mem_time:
                            if (t_ticks[i].flags & TICK_FLAG_BUY) == TICK_FLAG_BUY:
                                new_deals += 1
                            elif (t_ticks[i].flags & TICK_FLAG_SELL) == TICK_FLAG_SELL:
                                new_deals += 1
                    if new_deals > mem_deals:
                        res_deals = new_deals - mem_deals
                        result = CopyTicks(Symbol(), t_ticks, COPY_TICKS_TRADE, mem_time, _uint(new_deals))
                        if result > 0:
                            for i in range(0, result):
                                if t_ticks[i].time_msc == mem_time:
                                    if (t_ticks[i].flags & TICK_FLAG_BUY) == TICK_FLAG_BUY:
                                        if res_deals > 0:
                                            res_deals -= 1
                                            add_buy += 1
                                            add_b_vol += t_ticks[i].volume
                                    elif (t_ticks[i].flags & TICK_FLAG_SELL) == TICK_FLAG_SELL:
                                        if res_deals > 0:
                                            res_deals -= 1
                                            add_sell += 1
                                            add_s_vol += t_ticks[i].volume
                            sell_deals += add_sell
                            sell_vol += add_s_vol
                            buy_deals += add_buy
                            buy_vol += add_b_vol
            mem_deals = last_deals
            mem_time = ticks[a_size - 1].time_msc
            _sw1 = _int(sell_vol)
            if _sw1 in (0, 1):
                PlotIndexSetInteger(0, PLOT_LINE_WIDTH, 1)
            elif _sw1 in (2, 3, 4):
                PlotIndexSetInteger(0, PLOT_LINE_WIDTH, 2)
            elif _sw1 in (5, 6, 7):
                PlotIndexSetInteger(0, PLOT_LINE_WIDTH, 3)
            elif _sw1 in (8, 9, 10):
                PlotIndexSetInteger(0, PLOT_LINE_WIDTH, 4)
            else:
                PlotIndexSetInteger(0, PLOT_LINE_WIDTH, 5)
            _sw2 = _int(buy_vol)
            if _sw2 in (0, 1):
                PlotIndexSetInteger(1, PLOT_LINE_WIDTH, 1)
            elif _sw2 in (2, 3, 4):
                PlotIndexSetInteger(1, PLOT_LINE_WIDTH, 2)
            elif _sw2 in (5, 6, 7):
                PlotIndexSetInteger(1, PLOT_LINE_WIDTH, 3)
            elif _sw2 in (8, 9, 10):
                PlotIndexSetInteger(1, PLOT_LINE_WIDTH, 4)
            else:
                PlotIndexSetInteger(1, PLOT_LINE_WIDTH, 5)
            ObjectSetString(ChartID(), 'Label_1', OBJPROP_TEXT, 'Сум. объём Sell: ' + _str(sell_vol))
            ObjectSetString(ChartID(), 'Label_2', OBJPROP_TEXT, 'Сум. объём Buy: ' + _str(buy_vol))
            ObjectSetString(ChartID(), 'Label_3', OBJPROP_TEXT, 'Сум. кол-во Sell: ' + _str(sell_deals))
            ObjectSetString(ChartID(), 'Label_4', OBJPROP_TEXT, 'Сум. кол-во Buy: ' + _str(buy_deals))
            ChartRedraw(ChartID())
        if rates_total == prev_calculated:
            if begin == -111:
                if ActSize == 0:
                    for i in range(rates_total - 1, 0, -1):
                        SellBuffer[i] = SellBuffer[i - 1]
                        BuyBuffer[i] = BuyBuffer[i - 1]
                        SellVol[i] = SellVol[i - 1]
                        BuyVol[i] = BuyVol[i - 1]
                else:
                    for i in range(ActSize - 1, 0, -1):
                        SellBuffer[i] = SellBuffer[i - 1]
                        BuyBuffer[i] = BuyBuffer[i - 1]
                        SellVol[i] = SellVol[i - 1]
                        BuyVol[i] = BuyVol[i - 1]
                SellBuffer[0] = float(sell_deals)
                BuyBuffer[0] = float(buy_deals)
                SellVol[0] = float(sell_vol)
                BuyVol[0] = float(buy_vol)
        else:
            diff = rates_total - prev_calculated
            if begin == -111:
                if diff == 1:
                    if ActSize > 0:
                        SellBuffer[ActSize] = EMPTY_VALUE
                        BuyBuffer[ActSize] = EMPTY_VALUE
                        SellVol[ActSize] = EMPTY_VALUE
                        BuyVol[ActSize] = EMPTY_VALUE
                else:
                    if ActSize > 0:
                        for i in range(1, ActSize + diff):
                            if i < ActSize:
                                SellBuffer[i] = SellBuffer[i + diff - 1]
                                BuyBuffer[i] = BuyBuffer[i + diff - 1]
                                SellVol[i] = SellVol[i + diff - 1]
                                BuyVol[i] = BuyVol[i + diff - 1]
                            else:
                                SellBuffer[i] = EMPTY_VALUE
                                BuyBuffer[i] = EMPTY_VALUE
                                SellVol[i] = EMPTY_VALUE
                                BuyVol[i] = EMPTY_VALUE
                    else:
                        for i in range(1, rates_total):
                            if i <= prev_calculated:
                                SellBuffer[i] = SellBuffer[i + diff - 1]
                                BuyBuffer[i] = BuyBuffer[i + diff - 1]
                                SellVol[i] = SellVol[i + diff - 1]
                                BuyVol[i] = BuyVol[i + diff - 1]
                            else:
                                SellBuffer[i] = EMPTY_VALUE
                                BuyBuffer[i] = EMPTY_VALUE
                                SellVol[i] = EMPTY_VALUE
                                BuyVol[i] = EMPTY_VALUE
                SellBuffer[0] = float(sell_deals)
                BuyBuffer[0] = float(buy_deals)
                SellVol[0] = float(sell_vol)
                BuyVol[0] = float(buy_vol)
            else:
                if ActSize > 0:
                    for i in range(0, ActSize + diff):
                        if i < ActSize:
                            SellBuffer[i] = SellBuffer[i + diff]
                            BuyBuffer[i] = BuyBuffer[i + diff]
                            SellVol[i] = SellVol[i + diff]
                            BuyVol[i] = BuyVol[i + diff]
                        else:
                            SellBuffer[i] = EMPTY_VALUE
                            BuyBuffer[i] = EMPTY_VALUE
                            SellVol[i] = EMPTY_VALUE
                            BuyVol[i] = EMPTY_VALUE
                else:
                    for i in range(0, rates_total):
                        if i < prev_calculated:
                            SellBuffer[i] = SellBuffer[i + diff]
                            BuyBuffer[i] = BuyBuffer[i + diff]
                            SellVol[i] = SellVol[i + diff]
                            BuyVol[i] = BuyVol[i + diff]
                        else:
                            SellBuffer[i] = EMPTY_VALUE
                            BuyBuffer[i] = EMPTY_VALUE
                            SellVol[i] = EMPTY_VALUE
                            BuyVol[i] = EMPTY_VALUE
    event_cnt = rates_total
    return rates_total

# ---- global variables initialised from expressions
ticks = Arr(0, 0, factory=MqlTick)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class DealsLent(_MQL5Indicator):
    name = 'DealsLent'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ActSize': 30,  # Размер актуальной истории в буферах индикатора
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

