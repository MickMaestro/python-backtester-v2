"""VR Atr Pro Lite — converted from MQL5: MQL5 Indicators/VR Atr pro Lite MT5/VR Atr Pro Lite.mq5

Calculates the potential for price growth and fall
Copyright: Copyright 2018, Vladimir Pastushak.; Link: https://www.mql5.com/ru/users/voldemar/seller; Version: 18.080

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright 2018, Vladimir Pastushak.', 'link': 'https://www.mql5.com/ru/users/voldemar/seller', 'version': '18.080', 'window': 'chart', 'indicator_buffers': 0, 'indicator_plots': 0}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Calculates the potential for price growth and fall'], 'name': 'VR Atr Pro Lite', 'source': 'MQL5 Indicators/VR Atr pro Lite MT5/VR Atr Pro Lite.mq5', 'folder': 'VR Atr pro Lite MT5', 'inputs': [], 'short_form': True, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}


class ATR_struct(MqlObject):
    _q_fields = ('RectName', 'Time_open', 'Time_close', 'price_higth', 'price_open', 'price_low', 'point_aw_higt', 'point_aw_low', 'point_higt', 'point_low')
    def __init__(self, *args):
        self.RectName = ""
        self.Time_open = 0
        self.Time_close = 0
        self.price_higth = 0.0
        self.price_open = 0.0
        self.price_low = 0.0
        self.point_aw_higt = 0.0
        self.point_aw_low = 0.0
        self.point_higt = 0.0
        self.point_low = 0.0

def OnInit():
    Comment(' ')
    ArrayResize(atr, 40, 100)
    for i in range(0, 5):
        atr[i].RectName = 'Rectangle  ' + _str(i)
        RectangleCreate(0, atr[i].RectName, 0, 0, 0.0, 0, 0.0, clrBlue, STYLE_SOLID, 1, False, False, False, True, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, begin, price):
    if NewBar():
        for i in range(1, 20):
            atr[i].Time_open = 0
            atr[i].Time_close = 0
            atr[i].price_higth = 0.0
            atr[i].price_open = 0.0
            atr[i].price_low = 0.0
            atr[i].point_aw_higt = 0.0
            atr[i].point_aw_low = 0.0
            atr[i].point_higt = 0.0
            atr[i].point_low = 0.0
            atr[i].Time_open = iTime(Symbol(), PERIOD_D1, i)
            atr[i].Time_close = atr[i].Time_open + PeriodSeconds(PERIOD_D1)
            atr[i].price_higth = iHigh(Symbol(), PERIOD_D1, i)
            atr[i].price_open = iOpen(Symbol(), PERIOD_D1, i)
            atr[i].price_low = iLow(Symbol(), PERIOD_D1, i)
            atr[i].point_higt = atr[i].price_higth - atr[i].price_open
            atr[i].point_low = atr[i].price_open - atr[i].price_low
        for i in range(1, 5):
            for k in range(i + 1, i + 1 + 10):
                atr[i].point_aw_higt += atr[k].point_higt / 10
                atr[i].point_aw_low += atr[k].point_low / 10
        for i in range(1, 5):
            if ObjectFind(0, atr[i].RectName) == 0 and i != 0:
                ObjectSetInteger(0, atr[i].RectName, OBJPROP_TIME, 0, atr[i].Time_open)
                ObjectSetDouble(0, atr[i].RectName, OBJPROP_PRICE, 0, atr[i].price_open + atr[i].point_aw_higt)
                ObjectSetInteger(0, atr[i].RectName, OBJPROP_TIME, 1, atr[i].Time_close)
                ObjectSetDouble(0, atr[i].RectName, OBJPROP_PRICE, 1, atr[i].price_open - atr[i].point_aw_low)
        ChartRedraw(0)
    return rates_total

def OnDeinit(reason):
    for i in range(0, 5):
        atr[i].RectName = 'Rectangle  ' + _str(i)
        ObjectDelete(0, atr[i].RectName)
    EventKillTimer()

def RectangleCreate(chart_ID=0, name='Rectangle', sub_window=0, time1=0, price1=0.0, time2=0, price2=0.0, clr=clrRed, style=STYLE_SOLID, width=1, fill=False, back=False, selection=True, hidden=True, z_order=0):
    if ObjectCreate(chart_ID, name, OBJ_RECTANGLE, sub_window, time1, price1, time2, price2):
        ObjectSetInteger(chart_ID, name, OBJPROP_COLOR, clr)
        ObjectSetInteger(chart_ID, name, OBJPROP_STYLE, style)
        ObjectSetInteger(chart_ID, name, OBJPROP_WIDTH, width)
        ObjectSetInteger(chart_ID, name, OBJPROP_FILL, fill)
        ObjectSetInteger(chart_ID, name, OBJPROP_BACK, back)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTABLE, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_SELECTED, selection)
        ObjectSetInteger(chart_ID, name, OBJPROP_HIDDEN, hidden)
        ObjectSetInteger(chart_ID, name, OBJPROP_ZORDER, z_order)
    return True

def NewBar():
    global _s_NewBar_old_time
    new_time = iTime(Symbol(), Period(), 0)
    if new_time != _s_NewBar_old_time:
        _s_NewBar_old_time = new_time
        return True
    return False

# ---- global variables initialised from expressions
atr = Arr(0, 0, factory=ATR_struct)

# ---- static local variables
_s_NewBar_old_time = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VRAtrProLite(_MQL5Indicator):
    name = 'VR Atr Pro Lite'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'applied_price': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)'}, default=1),
    }

