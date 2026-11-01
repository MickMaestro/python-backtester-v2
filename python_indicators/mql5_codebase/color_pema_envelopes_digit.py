"""Color_PEMA_Envelopes_Digit — converted from MQL5: MQL5 Indicators/Color_PEMA_Envelopes_Digit/Color_PEMA_Envelopes_Digit.mq5

Pentuple Exponential Moving Average
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 7, 2: 8, 3: 8}, 'colors': {1: [16443110], 2: [9639167, 8421376], 3: [9639167, 8421376]}, 'widths': {2: 3, 3: 3}, 'styles': {2: 0, 3: 0}, 'labels': {1: 'PEMA_Envelopes_Digit Cloud', 2: 'PEMA_Envelopes_Digit Upper', 3: 'PEMA_Envelopes_Digit Lower'}, 'levels': [], 'description': ['Pentuple Exponential Moving Average'], 'name': 'Color_PEMA_Envelopes_Digit', 'source': 'MQL5 Indicators/Color_PEMA_Envelopes_Digit/Color_PEMA_Envelopes_Digit.mq5', 'folder': 'Color_PEMA_Envelopes_Digit', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'PEMA_Envelopes_Digit', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'EmaLength', 'py': 'EmaLength', 'param': 'EmaLength', 'type': 'double', 'default': 50.01, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Deviation', 'py': 'Deviation', 'param': 'Deviation', 'type': 'double', 'default': 0.1, 'label': 'Deviation', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора по вертикали в пунктах', 'sinput': False}, {'mql': 'Digit', 'py': 'Digit', 'param': 'Digit', 'type': 'uint', 'default': 2, 'label': 'количество разрядов округления', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': 'показывать ценовую метку', 'sinput': False}, {'mql': 'Up_Price_color', 'py': 'Up_Price_color', 'param': None, 'type': 'color', 'default': 8421376, 'label': 'цвет верхней ценовой метки', 'sinput': False}, {'mql': 'Dn_Price_color', 'py': 'Dn_Price_color', 'param': None, 'type': 'color', 'default': 255, 'label': 'цвет нижней ценовой метки', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

# enum Applied_price_
PRICE_CLOSE_ = 1
PRICE_OPEN_ = 2
PRICE_HIGH_ = 3
PRICE_LOW_ = 4
PRICE_MEDIAN_ = 5
PRICE_TYPICAL_ = 6
PRICE_WEIGHTED_ = 7
PRICE_SIMPL_ = 8
PRICE_QUARTER_ = 9
PRICE_TRENDFOLLOW0_ = 10
PRICE_TRENDFOLLOW1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
SirName = _input('SirName', 'PEMA_Envelopes_Digit')  # Первая часть имени графических объектов
EmaLength = _input('EmaLength', 50.01)  # глубина сглаживания
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Deviation = _input('Deviation', 0.1)  # Deviation
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # cдвиг индикатора по вертикали в пунктах
Digit = _input('Digit', 2)  # количество разрядов округления
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
PointPow10 = 0.0
Up_Price_name = ""
Dn_Price_name = ""
min_rates_total = 0

def OnInit():
    global Dn_Price_name, PointPow10, Up_Price_name, dPriceShift, min_rates_total
    min_rates_total = 6
    PointPow10 = Point() * MathPow(10, Digit)
    Up_Price_name = SirName + 'Up_Price'
    Dn_Price_name = SirName + 'Dn_Price'
    SetIndexBuffer(0, UpBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, DnBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    SetIndexBuffer(2, UpLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ColorUpLineBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    SetIndexBuffer(4, DnLineBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ColorDnLineBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'PEMA_Envelopes_Digit( Length = ', EmaLength, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    dPriceShift = Point() * PriceShift

def OnDeinit(reason):
    ObjectDelete(0, Up_Price_name)
    ObjectDelete(0, Dn_Price_name)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    res = Arr(9, 0.0, dyn=False)
    PEMA = 0.0
    trend = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    ArraySetAsSeries(open, False)
    ArraySetAsSeries(high, False)
    ArraySetAsSeries(low, False)
    ArraySetAsSeries(close, False)
    bar = first
    for bar in range(bar, rates_total):
        res[0] = PriceSeries(IPC, bar, open, low, high, close)
        res[1] = EMA[0].EMASeries(0, prev_calculated, rates_total, EmaLength, res[0], bar, False)
        res[2] = EMA[1].EMASeries(1, prev_calculated, rates_total, EmaLength, res[1], bar, False)
        res[3] = EMA[2].EMASeries(2, prev_calculated, rates_total, EmaLength, res[2], bar, False)
        res[4] = EMA[3].EMASeries(3, prev_calculated, rates_total, EmaLength, res[3], bar, False)
        res[5] = EMA[4].EMASeries(4, prev_calculated, rates_total, EmaLength, res[4], bar, False)
        res[6] = EMA[5].EMASeries(5, prev_calculated, rates_total, EmaLength, res[5], bar, False)
        res[7] = EMA[6].EMASeries(6, prev_calculated, rates_total, EmaLength, res[6], bar, False)
        res[8] = EMA[7].EMASeries(7, prev_calculated, rates_total, EmaLength, res[7], bar, False)
        PEMA = (8 * res[1]) - (28 * res[2]) + (56 * res[3]) - (70 * res[4]) + (56 * res[5]) - (28 * res[6]) + (8 * res[7]) - res[8]
        PEMA = PointPow10 * MathRound(_fdiv(PEMA, PointPow10))
        UpBuffer[bar] = ((1 + (Deviation / 100.0)) * PEMA) + dPriceShift
        UpLineBuffer[bar] = UpBuffer[bar]
        DnBuffer[bar] = ((1 - (Deviation / 100.0)) * PEMA) + dPriceShift
        DnLineBuffer[bar] = DnBuffer[bar]
    else:
        bar = _range_end(bar, rates_total, 1)
    if ShowPrice:
        bar0 = rates_total - 1
        time0 = time[bar0] + (1 * PeriodSeconds())
        SetRightPrice(0, Up_Price_name, 0, time0, UpBuffer[bar0], Up_Price_color)
        SetRightPrice(0, Dn_Price_name, 0, time0, DnBuffer[bar0], Dn_Price_color)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        clr = ColorUpLineBuffer[bar - 1]
        trend = UpLineBuffer[bar] - UpLineBuffer[bar - 1]
        if trend > 0:
            clr = 1.0
        if trend < 0:
            clr = 0.0
        ColorDnLineBuffer[bar] = clr
        ColorUpLineBuffer[bar] = ColorDnLineBuffer[bar]
    else:
        bar = _range_end(bar, rates_total, 1)
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

# ---- global variables initialised from expressions
EMA = Arr(8, 0, dyn=False, factory=CMoving_Average)


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorPEMAEnvelopesDigit(_MQL5Indicator):
    name = 'Color_PEMA_Envelopes_Digit'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'EmaLength': 50.01,  # глубина сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Deviation': 0.1,  # Deviation
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # cдвиг индикатора по вертикали в пунктах
        'Digit': 2,  # количество разрядов округления
        'ShowPrice': True,  # показывать ценовую метку
    }

