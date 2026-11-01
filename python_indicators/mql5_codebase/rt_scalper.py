"""RT_Scalper — converted from MQL5: MQL5 Indicators/RT Scalper/RT_Scalper.mq5

RT Scalper
Copyright: Copyright © 2016, prostotrader; Link: http://mql5.com; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, prostotrader', 'link': 'http://mql5.com', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [65535], 2: [16711935], 3: [16776960]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'Deals', 2: 'Volumes', 3: 'Orders'}, 'levels': [], 'description': ['RT Scalper'], 'name': 'RT_Scalper', 'source': 'MQL5 Indicators/RT Scalper/RT_Scalper.mq5', 'folder': 'RT Scalper', 'inputs': [{'mql': 'Deals', 'py': 'Deals', 'param': 'Deals', 'type': 'uint', 'default': 50, 'label': 'Порог сделок', 'sinput': False}], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

BOOK_TYPE_BUY = 0  # MQL5 constant unknown to the converter
BOOK_TYPE_SELL = 0  # MQL5 constant unknown to the converter
COPY_TICKS_TRADE = 0  # MQL5 constant unknown to the converter
SYMBOL_SESSION_BUY_ORDERS_VOLUME = 0  # MQL5 constant unknown to the converter
SYMBOL_SESSION_SELL_ORDERS_VOLUME = 0  # MQL5 constant unknown to the converter
TICK_FLAG_BUY = 0  # MQL5 constant unknown to the converter
TICK_FLAG_SELL = 0  # MQL5 constant unknown to the converter

# ---- inputs and global variables
Deals = _input('Deals', 50)  # Порог сделок
BuffDeals = Arr(0, 0.0)
BuffVolumes = Arr(0, 0.0)
BuffOrders = Arr(0, 0.0)
BuffSellVol = Arr(0, 0.0)
BuffSellPos = Arr(0, 0.0)
BuffBuyVol = Arr(0, 0.0)
BuffBuyPos = Arr(0, 0.0)
event_cnt = 0  # Переменная для вызова функции OnCalculate

def OnInit():
    global event_cnt
    event_cnt = 0
    IndicatorSetInteger(INDICATOR_DIGITS, 2)
    IndicatorSetString(INDICATOR_SHORTNAME, 'RT_Scalper')
    SetIndexBuffer(0, BuffDeals, INDICATOR_DATA)
    SetIndexBuffer(1, BuffVolumes, INDICATOR_DATA)
    SetIndexBuffer(2, BuffOrders, INDICATOR_DATA)
    SetIndexBuffer(3, BuffSellVol, INDICATOR_CALCULATIONS)
    SetIndexBuffer(4, BuffSellPos, INDICATOR_CALCULATIONS)
    SetIndexBuffer(5, BuffBuyVol, INDICATOR_CALCULATIONS)
    SetIndexBuffer(6, BuffBuyPos, INDICATOR_CALCULATIONS)
    ArraySetAsSeries(BuffDeals, True)
    ArraySetAsSeries(BuffVolumes, True)
    ArraySetAsSeries(BuffOrders, True)
    ArraySetAsSeries(BuffSellVol, True)
    ArraySetAsSeries(BuffSellPos, True)
    ArraySetAsSeries(BuffBuyVol, True)
    ArraySetAsSeries(BuffBuyPos, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    window = ChartWindowFind(ChartID(), 'RT_Scalper')
    ObjectCreate(ChartID(), 'RT_Scalper_1', OBJ_LABEL, window, 0, 0)
    ObjectCreate(ChartID(), 'RT_Scalper_2', OBJ_LABEL, window, 0, 0)
    ObjectCreate(ChartID(), 'RT_Scalper_3', OBJ_LABEL, window, 0, 0)
    ObjectCreate(ChartID(), 'RT_Scalper_4', OBJ_LABEL, window, 0, 0)
    ObjectSetInteger(ChartID(), 'RT_Scalper_1', OBJPROP_XDISTANCE, 5)
    ObjectSetInteger(ChartID(), 'RT_Scalper_2', OBJPROP_XDISTANCE, 5)
    ObjectSetInteger(ChartID(), 'RT_Scalper_3', OBJPROP_XDISTANCE, 5)
    ObjectSetInteger(ChartID(), 'RT_Scalper_4', OBJPROP_XDISTANCE, 5)
    ObjectSetInteger(ChartID(), 'RT_Scalper_1', OBJPROP_YDISTANCE, 15)
    ObjectSetInteger(ChartID(), 'RT_Scalper_2', OBJPROP_YDISTANCE, 30)
    ObjectSetInteger(ChartID(), 'RT_Scalper_3', OBJPROP_YDISTANCE, 45)
    ObjectSetInteger(ChartID(), 'RT_Scalper_4', OBJPROP_YDISTANCE, 60)
    ObjectSetInteger(ChartID(), 'RT_Scalper_1', OBJPROP_COLOR, clrLightPink)
    ObjectSetInteger(ChartID(), 'RT_Scalper_2', OBJPROP_COLOR, clrLightPink)
    ObjectSetInteger(ChartID(), 'RT_Scalper_3', OBJPROP_COLOR, clrLightSkyBlue)
    ObjectSetInteger(ChartID(), 'RT_Scalper_4', OBJPROP_COLOR, clrLightSkyBlue)
    ObjectSetString(ChartID(), 'RT_Scalper_1', OBJPROP_TEXT, 'Макс. объём Sell: 0')
    ObjectSetString(ChartID(), 'RT_Scalper_2', OBJPROP_TEXT, 'Поз. макс. объёма Sell: 0')
    ObjectSetString(ChartID(), 'RT_Scalper_3', OBJPROP_TEXT, 'Макс. объём Buy: 0')
    ObjectSetString(ChartID(), 'RT_Scalper_4', OBJPROP_TEXT, 'Поз. макс. объёма Buy: 0')
    ChartRedraw(ChartID())
    if not MarketBookAdd(Symbol()):
        Alert('Book not added!')
        return INIT_FAILED
    return INIT_SUCCEEDED

def OnDeinit(reason):
    MarketBookRelease(Symbol())
    ObjectDelete(ChartID(), 'RT_Scalper_1')
    ObjectDelete(ChartID(), 'RT_Scalper_2')
    ObjectDelete(ChartID(), 'RT_Scalper_3')
    ObjectDelete(ChartID(), 'RT_Scalper_4')
    if reason == REASON_INITFAILED:
        window = ChartWindowFind(ChartID(), 'RT_Scalper')
        ChartIndicatorDelete(ChartID(), window, 'RT_Scalper')

def OnBookEvent(symbol):
    if symbol == Symbol():
        price = Arr(0, 0.0)
        OnCalculate(event_cnt, event_cnt, 0, price)

def GetBookVolumes(sell_v, sell_p, buy_v, buy_p):
    sell_vol = 0
    buy_vol = 0
    book = Arr(0, 0, factory=MqlBookInfo)
    sell_v.v = 0
    sell_p.v = 0
    buy_v.v = 0
    buy_p.v = 0
    last_sell = 0
    is_buy = False
    if MarketBookGet(Symbol(), book):
        size = ArraySize(book)
        if size > 0:
            for i in range(0, size):
                if book[i].type == BOOK_TYPE_SELL:
                    sell_vol += book[i].volume
                    if book[i].volume >= sell_v.v:
                        sell_v.v = book[i].volume
                        sell_p.v = i
                elif book[i].type == BOOK_TYPE_BUY:
                    if not is_buy:
                        is_buy = True
                        last_sell = i - 1
                    buy_vol += book[i].volume
                    if book[i].volume > buy_v.v:
                        buy_v.v = book[i].volume
                        buy_p.v = i
            summ = buy_vol + sell_vol
            if summ > 0:
                sell_p.v = last_sell - sell_p.v + 1
                buy_p.v = buy_p.v - last_sell
                return _fdiv(float(sell_vol - buy_vol), float(summ)) * 100
    return 0.0

def GetDeals():
    ticks = Arr(0, 0, factory=MqlTick)
    buy_deal = 0
    sell_deal = 0
    result = CopyTicks(Symbol(), ticks, COPY_TICKS_TRADE, 0, Deals)
    if result > 0:
        for i in range(0, result):
            if (ticks[i].flags & TICK_FLAG_BUY) == TICK_FLAG_BUY:
                buy_deal += 1
            if (ticks[i].flags & TICK_FLAG_SELL) == TICK_FLAG_SELL:
                sell_deal += 1
        summ = buy_deal + sell_deal
        if summ > 0:
            return _fdiv(float(buy_deal - sell_deal), float(summ)) * 100
    return 0.0

def GetOrders():
    sell_vol = SymbolInfoDouble(Symbol(), SYMBOL_SESSION_SELL_ORDERS_VOLUME)
    buy_vol = SymbolInfoDouble(Symbol(), SYMBOL_SESSION_BUY_ORDERS_VOLUME)
    summ = sell_vol + buy_vol
    if _long(summ) > 0:
        return _fdiv(buy_vol - sell_vol, summ) * 100
    return 0.0

def OnCalculate(rates_total, prev_calculated, begin, price):
    global event_cnt
    if prev_calculated == 0:
        ArrayInitialize(BuffDeals, 0)
        ArrayInitialize(BuffVolumes, 0)
        ArrayInitialize(BuffOrders, 0)
        ArrayInitialize(BuffSellVol, 0)
        ArrayInitialize(BuffSellPos, 0)
        ArrayInitialize(BuffBuyVol, 0)
        ArrayInitialize(BuffBuyPos, 0)
    else:
        a_diff = rates_total - prev_calculated
        if a_diff > 0:
            i = a_diff - 1
            while i > 0:
                BuffDeals[i] = BuffDeals[i + 1]
                BuffVolumes[i] = BuffVolumes[i + 1]
                BuffOrders[i] = BuffOrders[i + 1]
                BuffSellVol[i] = BuffSellVol[i + 1]
                BuffSellPos[i] = BuffSellPos[i + 1]
                BuffBuyVol[i] = BuffBuyVol[i + 1]
                BuffBuyPos[i] = BuffBuyPos[i + 1]
                i += 1
    sell_vol = Box(0)
    sell_pos = Box(0)
    buy_vol = Box(0)
    buy_pos = Box(0)
    BuffDeals[0] = GetDeals()
    BuffVolumes[0] = GetBookVolumes(sell_vol, sell_pos, buy_vol, buy_pos)
    BuffOrders[0] = GetOrders()
    BuffSellVol[0] = float(sell_vol.v)
    BuffSellPos[0] = float(sell_pos.v)
    BuffBuyVol[0] = float(buy_vol.v)
    BuffBuyPos[0] = float(buy_pos.v)
    ObjectSetString(ChartID(), 'RT_Scalper_1', OBJPROP_TEXT, 'Макс. объём Sell: ' + _str(sell_vol.v))
    ObjectSetString(ChartID(), 'RT_Scalper_2', OBJPROP_TEXT, 'Поз. макс. объёма Sell: ' + _str(sell_pos.v))
    ObjectSetString(ChartID(), 'RT_Scalper_3', OBJPROP_TEXT, 'Макс. объём Buy: ' + _str(buy_vol.v))
    ObjectSetString(ChartID(), 'RT_Scalper_4', OBJPROP_TEXT, 'Поз. макс. объёма Buy: ' + _str(buy_pos.v))
    ChartRedraw(ChartID())
    event_cnt = rates_total
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RTScalper(_MQL5Indicator):
    name = 'RT_Scalper'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Deals': 50,  # Порог сделок
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

