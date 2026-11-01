"""VR Calculate Martingale Lite — converted from MQL5: MQL5 Indicators/VR Calculate Martingale Lite MT 5/VR Calculate Martingale Lite.mq5

 
 
 
Copyright: Copyright 2019, Trading-go Project.; Link: https://trading-go.ru; Version: 19.101

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- OnChartEvent is not called (no chart events).
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2019, Trading-go Project.', 'link': 'https://trading-go.ru', 'version': '19.101', 'window': 'chart', 'indicator_plots': 0, 'indicator_buffers': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': [' ', ' ', ' '], 'name': 'VR Calculate Martingale Lite', 'source': 'MQL5 Indicators/VR Calculate Martingale Lite MT 5/VR Calculate Martingale Lite.mq5', 'folder': 'VR Calculate Martingale Lite MT 5', 'inputs': [{'mql': 'iPrefix', 'py': 'iPrefix', 'param': None, 'type': 'string', 'default': '^$%#', 'label': '', 'sinput': False}, {'mql': 'iLots', 'py': 'iLots', 'param': 'iLots', 'type': 'double', 'default': 0.01, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
iPrefix = _input('iPrefix', '^$%#')
iLots = _input('iLots', 0.01)

class str_(MqlObject):
    _q_fields = ('m_name_orders', 'm_type_orders', 'm_lots_orders', 'm_cena_orders', 'tick')
    def __init__(self, *args):
        self.m_name_orders = ""
        self.m_type_orders = 0
        self.m_lots_orders = 0.0
        self.m_cena_orders = 0.0
        self.tick = MqlTick()
    def GetName(self):
        return self.m_name_orders
    def GetType(self):
        return self.m_type_orders
    def GetLots(self):
        return self.m_lots_orders
    def GetCena(self):
        return self.m_cena_orders
    def SetName(self, aName):
        self.m_name_orders = aName
    def SetType(self, aType):
        self.m_type_orders = aType
    def SetLots(self, aLots):
        self.m_lots_orders = aLots
    def SetCena(self, aCena):
        self.m_cena_orders = aCena
    def SetAWpr(self, aName, aTime, aPrice):
        ObjectSetInteger(0, iPrefix + 'D' + aName, OBJPROP_TIME, 1, TimeCurrent() + (PeriodSeconds() * 5))
        ObjectSetDouble(0, iPrefix + 'D' + aName, OBJPROP_PRICE, 1, aPrice)
    def CreateBuy(self, aName):
        if not SymbolInfoTick(Symbol(), self.tick):
            Print('SymbolInfoTick() failed, error = ', GetLastError())
            return False
        self.m_name_orders = aName
        self.m_type_orders = 0
        self.m_lots_orders = iLots
        self.m_cena_orders = NormalizeDouble(self.tick.bid, Digits())
        ButtonCreate(0, iPrefix + 'A' + aName, 0, 0, 0, 30, 18, CORNER_LEFT_UPPER, 'Buy', 'Arial', 10, clrWhite, clrBlue, clrBlue, False, False, False, True, 0)
        EditCreate(0, iPrefix + 'B' + aName, 0, 10, 30, 36, 18, DoubleToString(self.m_lots_orders, 2), 'Arial', 10, ALIGN_CENTER, False, CORNER_LEFT_UPPER, clrWhite, clrGray, clrBlue, False, False, True, 0)
        TrendCreate(0, iPrefix + 'D' + aName, 0, TimeCurrent() - (PeriodSeconds() * 10), self.m_cena_orders, TimeCurrent() + (PeriodSeconds() * 10), self.m_cena_orders, clrBlue, STYLE_SOLID, 1, False, False, False, False, True, 0)
        ArrowCreate(0, iPrefix + 'C' + aName, 0, TimeCurrent() + (PeriodSeconds() * 10), self.m_cena_orders, clrBlue, STYLE_SOLID, 2, False, True, True, 0)
        self.OrderDrag(aName)
        return True
    def CreateSel(self, aName):
        if not SymbolInfoTick(Symbol(), self.tick):
            Print('SymbolInfoTick() failed, error = ', GetLastError())
            return False
        self.m_name_orders = aName
        self.m_type_orders = 1
        self.m_lots_orders = iLots
        self.m_cena_orders = NormalizeDouble(self.tick.bid, Digits())
        ButtonCreate(0, iPrefix + 'A' + aName, 0, 0, 0, 30, 18, CORNER_LEFT_UPPER, 'Sell', 'Arial', 10, clrWhite, clrTomato, clrTomato, False, False, False, True, 0)
        EditCreate(0, iPrefix + 'B' + aName, 0, 10, 30, 36, 18, DoubleToString(self.m_lots_orders, 2), 'Arial', 10, ALIGN_CENTER, False, CORNER_LEFT_UPPER, clrWhite, clrGray, clrTomato, False, False, True, 0)
        TrendCreate(0, iPrefix + 'D' + aName, 0, TimeCurrent() - (PeriodSeconds() * 10), self.m_cena_orders, TimeCurrent() + (PeriodSeconds() * 10), self.m_cena_orders, clrTomato, STYLE_SOLID, 1, False, False, False, False, True, 0)
        ArrowCreate(0, iPrefix + 'C' + aName, 0, TimeCurrent() + (PeriodSeconds() * 10), self.m_cena_orders, clrTomato, STYLE_SOLID, 2, False, True, True, 0)
        self.OrderDrag(aName)
        return True
    def OrderDrag(self, aName):
        times = ObjectGetInteger(0, iPrefix + 'C' + aName, OBJPROP_TIME, 0)
        price = ObjectGetDouble(0, iPrefix + 'C' + aName, OBJPROP_PRICE, 0)
        text = ObjectGetString(0, iPrefix + 'B' + aName, OBJPROP_TEXT)
        self.m_lots_orders = StringToDouble(text)
        self.m_cena_orders = price
        x = Box(0)
        y = Box(0)
        if ChartTimePriceToXY(0, 0, times, price, x, y):
            ObjectSetInteger(0, iPrefix + 'A' + aName, OBJPROP_XDISTANCE, x.v + 2 - 72)
            ObjectSetInteger(0, iPrefix + 'A' + aName, OBJPROP_YDISTANCE, y.v + 2 - 10)
            ObjectSetInteger(0, iPrefix + 'B' + aName, OBJPROP_XDISTANCE, x.v + 32 - 72)
            ObjectSetInteger(0, iPrefix + 'B' + aName, OBJPROP_YDISTANCE, y.v + 2 - 10)
            ObjectSetInteger(0, iPrefix + 'D' + aName, OBJPROP_TIME, 0, times)
            ObjectSetDouble(0, iPrefix + 'D' + aName, OBJPROP_PRICE, 0, price)

class structura(MqlObject):
    _q_fields = ('orders',)
    def __init__(self, *args):
        self.orders = Arr(0, 0, factory=str_)
    def MenuCreate(self):
        EditCreate(0, iPrefix + 'Menu', 0, 10, 30, 64, 22, '', 'Arial', 10, ALIGN_CENTER, False, CORNER_LEFT_UPPER, clrWhite, clrGray, clrNONE, False, True, True, 0)
        ButtonCreate(0, iPrefix + 'Buy', 0, 0, 0, 30, 18, CORNER_LEFT_UPPER, 'Buy', 'Arial', 10, clrWhite, clrBlue, clrBlue, False, False, False, True, 0)
        ButtonCreate(0, iPrefix + 'Sel', 0, 0, 0, 30, 18, CORNER_LEFT_UPPER, 'Sell', 'Arial', 10, clrWhite, clrTomato, clrTomato, False, False, False, True, 0)
        ArrowCreate(0, iPrefix + 'AW', 0, TimeCurrent() + (PeriodSeconds() * 10), 0.0, clrGreen, STYLE_SOLID, 3, False, False, True, 0)
        self.MenuDrag()
        return True
    def MenuDrag(self):
        x = _int(ObjectGetInteger(0, iPrefix + 'Menu', OBJPROP_XDISTANCE))
        y = _int(ObjectGetInteger(0, iPrefix + 'Menu', OBJPROP_YDISTANCE))
        ObjectSetInteger(0, iPrefix + 'Buy', OBJPROP_XDISTANCE, x + 2)
        ObjectSetInteger(0, iPrefix + 'Buy', OBJPROP_YDISTANCE, y + 2)
        ObjectSetInteger(0, iPrefix + 'Sel', OBJPROP_XDISTANCE, x + 32)
        ObjectSetInteger(0, iPrefix + 'Sel', OBJPROP_YDISTANCE, y + 2)
    def GetStateBuy(self):
        return _bool(ObjectGetInteger(0, iPrefix + 'Buy', OBJPROP_STATE))
    def SetStateBuy(self):
        ObjectSetInteger(0, iPrefix + 'Buy', OBJPROP_STATE, False)
    def GetStateSel(self):
        return _bool(ObjectGetInteger(0, iPrefix + 'Sel', OBJPROP_STATE))
    def SetStateSel(self):
        ObjectSetInteger(0, iPrefix + 'Sel', OBJPROP_STATE, False)

def OnInit():
    Comment('')
    ChartSetInteger(ChartID(), CHART_EVENT_MOUSE_MOVE, True)
    st.MenuCreate()
    return INIT_SUCCEEDED

def OnChartEvent(id_, lparam, dparam, sparam):
    if id_ == CHARTEVENT_OBJECT_CLICK:
        if st.GetStateBuy():
            u = ArraySize(st.orders)
            ArrayResize(st.orders, u + 1, 100)
            st.orders[u].CreateBuy(IntegerToString(u))
            st.SetStateBuy()
        if st.GetStateSel():
            u = ArraySize(st.orders)
            ArrayResize(st.orders, u + 1, 100)
            st.orders[u].CreateSel(IntegerToString(u))
            st.SetStateSel()
    if id_ == CHARTEVENT_MOUSE_MOVE or id_ == CHARTEVENT_OBJECT_ENDEDIT:
        if sparam == '1':
            buy_price = 0.0
            sel_price = 0.0
            buy_lot = 0.0
            sel_lot = 0.0
            price_aw = 0.0
            t = 0
            i = 0
            while i < ArraySize(st.orders):
                st.orders[i].OrderDrag(IntegerToString(i))
                if st.orders[i].GetType() == 0:
                    buy_price += st.orders[i].GetCena() * st.orders[i].GetLots()
                    buy_lot += st.orders[i].GetLots()
                    t += 1
                if st.orders[i].GetType() == 1:
                    sel_price += st.orders[i].GetCena() * st.orders[i].GetLots()
                    sel_lot += st.orders[i].GetLots()
                    t += 1
                i += 1
            if t >= 2 and (buy_lot - sel_lot) != 0:
                price_aw = NormalizeDouble(_fdiv(buy_price - sel_price, buy_lot - sel_lot), Digits())
                if price_aw > 0:
                    i = 0
                    while i < ArraySize(st.orders):
                        st.orders[i].SetAWpr(IntegerToString(i), TimeCurrent(), price_aw)
                        i += 1
                ObjectSetDouble(0, iPrefix + 'AW', OBJPROP_PRICE, 0, price_aw)
                ObjectSetInteger(0, iPrefix + 'AW', OBJPROP_TIME, 0, TimeCurrent() + (PeriodSeconds() * 5))
            st.MenuDrag()
    ChartRedraw()

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    return rates_total

def OnDeinit(reason):
    ObjectsDeleteAll(0, iPrefix)

def ButtonCreate(chart_ID=0, name='Button', sub_window=0, x=0, y=0, width=50, height=18, corner=CORNER_LEFT_UPPER, text='Button', font='Arial', font_size=10, clr=clrBlack, back_clr=0xD8E9EC, border_clr=clrNONE, state=False, back=False, selection=False, hidden=True, z_order=0):
    ResetLastError()
    if ObjectCreate(chart_ID, name, OBJ_BUTTON, sub_window, 0, 0):
        ObjectSetInteger(chart_ID, name, OBJPROP_XDISTANCE, x)
        ObjectSetInteger(chart_ID, name, OBJPROP_YDISTANCE, y)
        ObjectSetInteger(chart_ID, name, OBJPROP_XSIZE, width)
        ObjectSetInteger(chart_ID, name, OBJPROP_YSIZE, height)
        ObjectSetInteger(chart_ID, name, OBJPROP_CORNER, corner)
        ObjectSetString(chart_ID, name, OBJPROP_TEXT, text)
        ObjectSetString(chart_ID, name, OBJPROP_FONT, font)
        ObjectSetInteger(chart_ID, name, OBJPROP_FONTSIZE, font_size)
        ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
        ObjectSetInteger(chart_ID, name, OBJPROP_BGCOLOR, back_clr)
        ObjectSetInteger(chart_ID, name, OBJPROP_BORDER_COLOR, border_clr)
        ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
        ObjectSetInteger(chart_ID, name, OBJPROP_STATE, state)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
        ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
        return True
    Print('ButtonCreate', ': failed to create the button! Error code = ', GetLastError())
    return False

def TrendCreate(chart_ID=0, name='TrendLine', sub_window=0, time1=0, price1=0.0, time2=0, price2=0.0, clr=clrRed, style=STYLE_SOLID, width=1, back=False, selection=True, ray_left=False, ray_right=False, hidden=True, z_order=0):
    ResetLastError()
    if ObjectCreate(chart_ID, name, OBJ_TREND, sub_window, time1, price1, time2, price2):
        ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
        ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
        ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
        ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_RAY_LEFT, ray_left)
        ObjectSetInteger(chart_ID, name, OBJPROP_RAY_RIGHT, ray_right)
        ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
        ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
        return True
    Print('TrendCreate', ': failed to create a trend line! Error code = ', GetLastError())
    return False

def EditCreate(chart_ID=0, name='Edit', sub_window=0, x=0, y=0, width=50, height=18, text='Text', font='Arial', font_size=10, align=ALIGN_CENTER, read_only=False, corner=CORNER_LEFT_UPPER, clr=clrBlack, back_clr=clrWhite, border_clr=clrNONE, back=False, selection=False, hidden=True, z_order=0):
    ResetLastError()
    if ObjectCreate(chart_ID, name, OBJ_EDIT, sub_window, 0, 0):
        ObjectSetInteger(chart_ID, name, OBJPROP_XDISTANCE, x)
        ObjectSetInteger(chart_ID, name, OBJPROP_YDISTANCE, y)
        ObjectSetInteger(chart_ID, name, OBJPROP_XSIZE, width)
        ObjectSetInteger(chart_ID, name, OBJPROP_YSIZE, height)
        ObjectSetString(chart_ID, name, OBJPROP_TEXT, text)
        ObjectSetString(chart_ID, name, OBJPROP_FONT, font)
        ObjectSetInteger(chart_ID, name, OBJPROP_FONTSIZE, font_size)
        ObjectSetInteger(chart_ID, name, OBJPROP_ALIGN, align)
        ObjectSetInteger(chart_ID, name, OBJPROP_READONLY, read_only)
        ObjectSetInteger(chart_ID, name, OBJPROP_CORNER, corner)
        ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
        ObjectSetInteger(chart_ID, name, OBJPROP_BGCOLOR, back_clr)
        ObjectSetInteger(chart_ID, name, OBJPROP_BORDER_COLOR, border_clr)
        ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
        ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
        return True
    Print('EditCreate', ': failed to create "Edit" object! Error code = ', GetLastError())
    return False

def ArrowCreate(chart_ID=0, name='Arrow', sub_window=0, time=0, price=0.0, clr=clrRed, style=STYLE_SOLID, width=3, back=False, selection=True, hidden=True, z_order=0):
    ResetLastError()
    if ObjectCreate(chart_ID, name, OBJ_ARROW_RIGHT_PRICE, sub_window, time, price):
        ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
        ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
        ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
        ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
        ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
        return True
    Print('ArrowCreate', ': failed to create an arrow! Error code = ', GetLastError())
    return False

# ---- global variables initialised from expressions
st = _alloc(structura)
st.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VRCalculateMartingaleLite(_MQL5Indicator):
    name = 'VR Calculate Martingale Lite'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'iLots': 0.01,
    }

