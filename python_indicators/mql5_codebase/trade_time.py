"""trade_time — converted from MQL5: MQL5 Indicators/Trade_Time/trade_time.mq5

Trade Time
Copyright: 2012, Karlson.; Link: https://login.mql5.com/ru/users/Karlson; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'version': '1.00', 'copyright': '2012, Karlson.', 'link': 'https://login.mql5.com/ru/users/Karlson', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {}, 'colors': {}, 'widths': {}, 'styles': {}, 'labels': {}, 'levels': [], 'description': ['Trade Time'], 'name': 'trade_time', 'source': 'MQL5 Indicators/Trade_Time/trade_time.mq5', 'folder': 'Trade_Time', 'inputs': [{'mql': 'st', 'py': 'st', 'param': 'st', 'type': 'int', 'default': 8, 'label': 'Trade Starttime', 'sinput': False}, {'mql': 'en', 'py': 'en', 'param': 'en', 'type': 'int', 'default': 20, 'label': 'Trade Stoptime', 'sinput': False}, {'mql': 'cl', 'py': 'cl', 'param': None, 'type': 'color', 'default': 11829830, 'label': 'Color', 'sinput': False}, {'mql': 'fill', 'py': 'fill', 'param': 'fill', 'type': 'bool', 'default': False, 'label': 'Filling', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
st = _input('st', 8)  # Trade Starttime
en = _input('en', 20)  # Trade Stoptime
cl = _input('cl', clrSteelBlue)  # Color
fill = _input('fill', False)  # Filling
hg = Arr.of([0.0], fill=0.0)
lw = Arr.of([0.0], fill=0.0)
dist = 0
ttt = 0
dd = Arr(0, 0)

def OnInit():
    global dist
    if (st >= en or st < 0) or en > 24:
        Print('Wrong parameters.')
    dist = (en - st) * 3600

def OnCalculate(rates_total, prev_calculated, Time, Open, High, Low, Close, TickVolume, Volume, Spread):
    global ttt
    limit = 0
    if prev_calculated < 1:
        limit = 0
    else:
        limit = prev_calculated - 1
    for i in range(limit, rates_total):
        TimeToStruct(Time[i], time)
        if time.hour == st and time.min == 0:
            if CopyHigh(Symbol(), PERIOD_D1, _DT(Time[i]), 1, hg) < 1:
                return 0
            if CopyLow(Symbol(), PERIOD_D1, _DT(Time[i]), 1, lw) < 1:
                return 0
            ttt = Time[i] + dist
            ObjectCreate(0, 'rec' + _str(Time[i]), OBJ_RECTANGLE, 0, Time[i], hg[0], ttt, lw[0])
            ObjectSetInteger(0, 'rec' + _str(Time[i]), OBJPROP_COLOR, cl)
            ObjectSetInteger(0, 'rec' + _str(Time[i]), OBJPROP_FILL, fill)
        if limit > (rates_total - 2):
            if CopyLow(Symbol(), PERIOD_D1, _DT(Time[rates_total - 1]), 1, lw) < 1:
                return 0
            if CopyHigh(Symbol(), PERIOD_D1, _DT(Time[rates_total - 1]), 1, hg) < 1:
                return 0
            a = TimeToString(Time[rates_total - 1])
            b = StringSubstr(a, 0, 11)
            c = b + _str(st) + ':00'
            t = StringToTime(c)
            ttt = t + dist
            ObjectDelete(0, 'rec' + _str(t))
            ObjectCreate(0, 'rec' + _str(t), OBJ_RECTANGLE, 0, t, hg[0], ttt, lw[0])
            ObjectSetInteger(0, 'rec' + _str(t), OBJPROP_COLOR, cl)
            ObjectSetInteger(0, 'rec' + _str(t), OBJPROP_FILL, fill)
            ChartRedraw(0)
    ChartRedraw(0)
    return rates_total

def OnDeinit(reason):
    for i in range(ObjectsTotal(0, 0, -1), 0, -1):
        name = ObjectName(0, i - 1, 0, -1)
        if StringFind(name, 'rec', 0) > -1:
            ObjectDelete(0, name)
    ChartRedraw(0)

# ---- global variables initialised from expressions
time = _struct_init(MqlDateTime(), [0])
start = ""
end = ""


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TradeTime(_MQL5Indicator):
    name = 'trade_time'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'st': 8,  # Trade Starttime
        'en': 20,  # Trade Stoptime
        'fill': False,  # Filling
    }

