"""Float_Pivot_Digit — converted from MQL5: MQL5 Indicators/Float_Pivot_Digit_HTF/Float_Pivot_Digit.mq5

Copyright: Copyright © 2006, Nick A. Zhilin; Link: rebus@dialup.etr.ru; Version: 1.01

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, Nick A. Zhilin', 'link': 'rebus@dialup.etr.ru', 'version': '1.01', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 5}, 'types': {1: 7, 2: 1, 3: 1, 4: 1, 5: 7}, 'colors': {1: [15859441], 2: [3329330], 3: [13458026], 4: [16711935], 5: [16440058]}, 'widths': {2: 2, 3: 2, 4: 2}, 'styles': {2: 0, 3: 0, 4: 0}, 'labels': {1: 'Upper Cloud', 2: 'Upper FloatPivot', 3: 'Middle FloatPivot', 4: 'Lower FloatPivot', 5: 'Lower Cloud'}, 'levels': [], 'description': [], 'name': 'Float_Pivot_Digit', 'source': 'MQL5 Indicators/Float_Pivot_Digit_HTF/Float_Pivot_Digit.mq5', 'folder': 'Float_Pivot_Digit_HTF', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'Float_Pivot_Digit', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'IPeriod', 'py': 'IPeriod', 'param': 'IPeriod', 'type': 'int', 'default': 100, 'label': 'Период поиска экстремумов', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 5, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'Digit', 'py': 'Digit', 'param': 'Digit', 'type': 'uint', 'default': 2, 'label': 'количество разрядов округления', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': 'показывать ценовые метки', 'sinput': False}, {'mql': 'Upper_color', 'py': 'Upper_color', 'param': None, 'type': 'color', 'default': 8421376, 'label': 'Цвет верхней ценовой метки', 'sinput': False}, {'mql': 'Middle_color', 'py': 'Middle_color', 'param': None, 'type': 'color', 'default': 16711680, 'label': 'Цвет средней ценовой метки', 'sinput': False}, {'mql': 'Lower_color', 'py': 'Lower_color', 'param': None, 'type': 'color', 'default': 16711935, 'label': 'Цвет нижней ценовой метки', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# enum ENUM_APPLIED_PRICE_
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
_enum('ENUM_APPLIED_PRICE_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
SirName = _input('SirName', 'Float_Pivot_Digit')  # Первая часть имени графических объектов
IPeriod = _input('IPeriod', 100)  # Период поиска экстремумов
IPC = _input('IPC', PRICE_MEDIAN_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
Digit = _input('Digit', 2)  # количество разрядов округления
ShowPrice = _input('ShowPrice', True)  # показывать ценовые метки
Upper_color = _input('Upper_color', clrTeal)  # Цвет верхней ценовой метки
Middle_color = _input('Middle_color', clrBlue)  # Цвет средней ценовой метки
Lower_color = _input('Lower_color', clrMagenta)  # Цвет нижней ценовой метки
ExtUp1Buffer = Arr(0, 0.0)
ExtUp2Buffer = Arr(0, 0.0)
ExtABuffer = Arr(0, 0.0)
ExtBBuffer = Arr(0, 0.0)
ExtCBuffer = Arr(0, 0.0)
ExtDn1Buffer = Arr(0, 0.0)
ExtDn2Buffer = Arr(0, 0.0)
min_rates_total = 0
upper_name = ""
middle_name = ""
lower_name = ""
PointPow10 = 0.0

def OnInit():
    global PointPow10, lower_name, middle_name, min_rates_total, upper_name
    min_rates_total = MathMax(3, IPeriod)
    upper_name = SirName + ' upper text lable'
    middle_name = SirName + ' middle text lable'
    lower_name = SirName + ' lower text lable'
    PointPow10 = Point() * MathPow(10, Digit)
    SetIndexBuffer(0, ExtUp1Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtUp2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    SetIndexBuffer(2, ExtABuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    SetIndexBuffer(3, ExtBBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    SetIndexBuffer(4, ExtCBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    SetIndexBuffer(5, ExtDn1Buffer, INDICATOR_DATA)
    SetIndexBuffer(6, ExtDn2Buffer, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(4, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(4, PLOT_SHIFT, Shift)
    shortname = Box("")
    StringConcatenate(shortname, 'Float_Pivot_Digit( IPeriod = ', IPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnDeinit(reason):
    ObjectDelete(0, upper_name)
    ObjectDelete(0, middle_name)
    ObjectDelete(0, lower_name)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    if prev_calculated == 0:
        first = min_rates_total - 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        ArraySetAsSeries(high, True)
        ArraySetAsSeries(low, True)
        max_ = high[ArrayMaximum(high, rates_total - 1 - bar, IPeriod)]
        min_ = low[ArrayMinimum(low, rates_total - 1 - bar, IPeriod)]
        ArraySetAsSeries(high, False)
        ArraySetAsSeries(low, False)
        pivot = (PriceSeries(IPC, bar - 1, open, low, high, close) + PriceSeries(IPC, bar - 2, open, low, high, close) + PriceSeries(IPC, bar - 3, open, low, high, close)) / 3
        res = (max_ + min_ + pivot) / 3
        ExtUp1Buffer[bar] = PointPow10 * MathCeil(_fdiv(((2 * res) - min_ + res) / 2, PointPow10))
        ExtABuffer[bar] = ExtUp1Buffer[bar]
        ExtDn2Buffer[bar] = PointPow10 * MathFloor(_fdiv((res + ((2 * res) - max_)) / 2, PointPow10))
        ExtCBuffer[bar] = ExtDn2Buffer[bar]
        ExtDn1Buffer[bar] = PointPow10 * MathRound(_fdiv(res, PointPow10))
        ExtUp2Buffer[bar] = ExtDn1Buffer[bar]
        ExtBBuffer[bar] = ExtUp2Buffer[bar]
    else:
        bar = _range_end(bar, rates_total, 1)
    if ShowPrice:
        bar0 = rates_total - Shift - 1
        time0 = time[bar0]
        SetRightPrice(0, upper_name, 0, time0, ExtABuffer[bar0], Upper_color)
        SetRightPrice(0, middle_name, 0, time0, ExtBBuffer[bar0], Middle_color)
        SetRightPrice(0, lower_name, 0, time0, ExtCBuffer[bar0], Lower_color)
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

def PriceSeries(applied_price, bar, Open, Low, High, Close):
    _sw1 = applied_price
    if _sw1 == PRICE_CLOSE:
        return Close[bar]
    elif _sw1 == PRICE_OPEN:
        return Open[bar]
    elif _sw1 == PRICE_HIGH:
        return High[bar]
    elif _sw1 == PRICE_LOW:
        return Low[bar]
    elif _sw1 == PRICE_MEDIAN:
        return (High[bar] + Low[bar]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (Close[bar] + High[bar] + Low[bar]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return ((2 * Close[bar]) + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 8:
        return (Open[bar] + Close[bar]) / 2.0
    elif _sw1 == 9:
        return (Open[bar] + Close[bar] + High[bar] + Low[bar]) / 4.0
    elif _sw1 == 10:
        if Close[bar] > Open[bar]:
            return High[bar]
        else:
            if Close[bar] < Open[bar]:
                return Low[bar]
            else:
                return Close[bar]
    elif _sw1 == 11:
        if Close[bar] > Open[bar]:
            return (High[bar] + Close[bar]) / 2.0
        else:
            if Close[bar] < Open[bar]:
                return (Low[bar] + Close[bar]) / 2.0
            else:
                return Close[bar]
    elif _sw1 == 12:
        res = High[bar] + Low[bar] + Close[bar]
        if Close[bar] < Open[bar]:
            res = (res + Low[bar]) / 2
        if Close[bar] > Open[bar]:
            res = (res + High[bar]) / 2
        if Close[bar] == Open[bar]:
            res = (res + Close[bar]) / 2
        return (res - Low[bar] + (res - High[bar])) / 2
    else:
        return Close[bar]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class FloatPivotDigit(_MQL5Indicator):
    name = 'Float_Pivot_Digit'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'IPeriod': 100,  # Период поиска экстремумов
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLLOW0_', 11: 'PRICE_TRENDFOLLOW0_2', 12: 'Demark Price'}, default=5),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'Digit': 2,  # количество разрядов округления
        'ShowPrice': True,  # показывать ценовые метки
    }

