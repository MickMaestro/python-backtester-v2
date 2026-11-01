"""ColorBarRange_HTF — converted from MQL5: MQL5 Indicators/ColorBarRange_HTF/ColorBarRange_HTF.mq5

Copyright: Copyright © 2017, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.60

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.60', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 7, 2: 8, 3: 8}, 'colors': {1: [16443110], 2: [7451452, 9639167], 3: [7451452, 9639167]}, 'widths': {2: 3, 3: 3}, 'styles': {2: 0, 3: 0}, 'labels': {1: 'ColorBarRange_HTF Cloud', 2: 'ColorBarRange_HTF Upper', 3: 'ColorBarRange_HTF Lower'}, 'levels': [], 'description': [], 'name': 'ColorBarRange_HTF', 'source': 'MQL5 Indicators/ColorBarRange_HTF/ColorBarRange_HTF.mq5', 'folder': 'ColorBarRange_HTF', 'inputs': [{'mql': 'TimeFrame', 'py': 'TimeFrame', 'param': 'TimeFrame', 'type': 'int', 'default': 16396, 'label': 'Период графика', 'sinput': False}, {'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'ColorBarRange_HTF', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора по вертикали в пунктах', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': 'показывать ценовую метку', 'sinput': False}, {'mql': 'Up_Price_color', 'py': 'Up_Price_color', 'param': None, 'type': 'color', 'default': 8421376, 'label': 'цвет верхней ценовой метки', 'sinput': False}, {'mql': 'Dn_Price_color', 'py': 'Dn_Price_color', 'param': None, 'type': 'color', 'default': 255, 'label': 'цвет нижней ценовой метки', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
TimeFrame = _input('TimeFrame', PERIOD_H12)  # Период графика
SirName = _input('SirName', 'ColorBarRange_HTF')  # Первая часть имени графических объектов
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # cдвиг индикатора по вертикали в пунктах
ShowPrice = _input('ShowPrice', True)  # показывать ценовую метку
Up_Price_color = _input('Up_Price_color', clrTeal)  # цвет верхней ценовой метки
Dn_Price_color = _input('Dn_Price_color', clrRed)  # цвет нижней ценовой метки
UpLineBuffer = Arr(0, 0.0)
ColorUpLineBuffer = Arr(0, 0.0)
DnLineBuffer = Arr(0, 0.0)
ColorDnLineBuffer = Arr(0, 0.0)
UpBuffer = Arr(0, 0.0)
DnBuffer = Arr(0, 0.0)
dPriceShift = 0.0
Symbol_ = ""
Word = ""
Up_Price_name = ""
Dn_Price_name = ""
min_rates_total = 0

def OnInit():
    global Dn_Price_name, Symbol_, Up_Price_name, Word, dPriceShift, min_rates_total
    if TimeFrame < Period() and TimeFrame != PERIOD_CURRENT:
        Print('Период графика для индикатора ColorBarRange_HTF не может быть меньше периода текущего графика')
        return INIT_FAILED
    min_rates_total = 2
    Symbol_ = Symbol()
    Word = 'ColorBarRange_HTF' + ' индикатор: ' + Symbol_ + StringSubstr(EnumToString(Period(), 'ENUM_TIMEFRAMES'), 7, -1)
    dPriceShift = Point() * PriceShift
    Up_Price_name = SirName + 'Up_Price'
    Dn_Price_name = SirName + 'Dn_Price'
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    ArraySetAsSeries(UpBuffer, True)
    ArraySetAsSeries(DnBuffer, True)
    SetIndexBuffer(2, UpLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ColorUpLineBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    ArraySetAsSeries(UpLineBuffer, True)
    ArraySetAsSeries(ColorUpLineBuffer, True)
    SetIndexBuffer(4, DnLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ColorDnLineBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    ArraySetAsSeries(DnLineBuffer, True)
    ArraySetAsSeries(ColorDnLineBuffer, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'ColorBarRange_HTF')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnDeinit(reason):
    ObjectDelete(0, Up_Price_name)
    ObjectDelete(0, Dn_Price_name)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total:
        return 0
    iHigh_ = Arr(1, 0.0, dyn=False)
    iLow_ = Arr(1, 0.0, dyn=False)
    clr = 0.0
    limit = 0
    bar = 0
    iTime_ = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if CopyTime(Symbol_, TimeFrame, _DT(time[bar]), 1, iTime_) <= 0:
            return 0
        if time[bar] >= iTime_[0] and time[bar + 1] < iTime_[0]:
            _s_OnCalculate_LastCountBar = bar
            if CopyHigh(Symbol(), TimeFrame, _DT(time[bar]), 1, iHigh_) <= 0:
                return 0
            if CopyLow(Symbol(), TimeFrame, _DT(time[bar]), 1, iLow_) <= 0:
                return 0
            UpBuffer[bar] = iHigh_[0] + dPriceShift
            UpLineBuffer[bar] = UpBuffer[bar]
            DnBuffer[bar] = iLow_[0] + dPriceShift
            DnLineBuffer[bar] = DnBuffer[bar]
            if UpLineBuffer[bar + 1] < UpLineBuffer[bar]:
                clr = 0.0
            elif UpLineBuffer[bar + 1] > UpLineBuffer[bar]:
                clr = 1.0
            else:
                clr = ColorUpLineBuffer[bar + 1]
            ColorUpLineBuffer[bar] = clr
            if DnLineBuffer[bar + 1] < DnLineBuffer[bar]:
                clr = 0.0
            elif DnLineBuffer[bar + 1] > DnLineBuffer[bar]:
                clr = 1.0
            else:
                clr = ColorDnLineBuffer[bar + 1]
            ColorDnLineBuffer[bar] = clr
        else:
            UpBuffer[bar] = UpLineBuffer[bar + 1]
            UpLineBuffer[bar] = UpBuffer[bar]
            DnBuffer[bar] = DnLineBuffer[bar + 1]
            DnLineBuffer[bar] = DnBuffer[bar]
            ColorUpLineBuffer[bar] = ColorUpLineBuffer[bar + 1]
            ColorDnLineBuffer[bar] = ColorDnLineBuffer[bar + 1]
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if ShowPrice:
        bar0 = 0
        time0 = time[bar0] + (1 * PeriodSeconds())
        SetRightPrice(0, Up_Price_name, 0, time0, UpBuffer[bar0], Up_Price_color)
        SetRightPrice(0, Dn_Price_name, 0, time0, DnBuffer[bar0], Dn_Price_color)
    ChartRedraw(0)
    return rates_total

def CreateRightPrice(chart_id, name, nwin, time, price, Color):
    ObjectCreate(chart_id, name, OBJ_ARROW_RIGHT_PRICE, nwin, time, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, 2)

def SetRightPrice(chart_id, name, nwin, time, price, Color):
    if ObjectFind(chart_id, name) == -1:
        CreateRightPrice(chart_id, name, nwin, time, price, Color)
    else:
        ObjectMove(chart_id, name, 0, time, price)

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorBarRangeHTF(_MQL5Indicator):
    name = 'ColorBarRange_HTF'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'TimeFrame': _Choice({0: 'CURRENT', 1: 'M1', 2: 'M2', 3: 'M3', 4: 'M4', 5: 'M5', 6: 'M6', 10: 'M10', 12: 'M12', 15: 'M15', 20: 'M20', 30: 'M30', 16385: 'H1', 16386: 'H2', 16387: 'H3', 16388: 'H4', 16390: 'H6', 16392: 'H8', 16396: 'H12', 16408: 'D1', 32769: 'W1', 49153: 'MN1'}, default=16396),  # Период графика
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # cдвиг индикатора по вертикали в пунктах
        'ShowPrice': True,  # показывать ценовую метку
    }

