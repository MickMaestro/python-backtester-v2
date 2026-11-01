"""Volume_Weighted_MA_Digit_System — converted from MQL5: MQL5 Indicators/Volume_Weighted_MA_Digit_System/Volume_Weighted_MA_Digit_System.mq5

Пробойная система с использованием индикатора Volume_Weighted_MA_Digit
Copyright: Copyright © 2016, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2016, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 7, 'indicator_plots': 4}, 'types': {1: 7, 2: 1, 3: 1, 4: 11}, 'colors': {1: [16119285], 2: [16748574], 3: [16711935], 4: [255, 8388736, 8421504, 8421376, 65280]}, 'widths': {2: 2, 3: 2, 4: 2}, 'styles': {2: 0, 3: 0, 4: 0}, 'labels': {1: 'Volume_Weighted_MA_Digit', 2: 'Upper Volume_Weighted_MA_Digit', 3: 'Lower Volume_Weighted_MA_Digit', 4: 'Volume_Weighted_MA_Digit_BARS'}, 'levels': [], 'description': ['Пробойная система с использованием индикатора Volume_Weighted_MA_Digit'], 'name': 'Volume_Weighted_MA_Digit_System', 'source': 'MQL5 Indicators/Volume_Weighted_MA_Digit_System/Volume_Weighted_MA_Digit_System.mq5', 'folder': 'Volume_Weighted_MA_Digit_System', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'Volume_Weighted_MA_Digit', 'label': 'первая часть имени графических объектов', 'sinput': False}, {'mql': 'Length', 'py': 'Length', 'param': 'Length', 'type': 'uint', 'default': 12, 'label': 'глубина сглаживания', 'sinput': False}, {'mql': 'VolumeType', 'py': 'VolumeType', 'param': 'VolumeType', 'type': 'int', 'default': 0, 'label': 'объём', 'sinput': False}, {'mql': 'Digit', 'py': 'Digit', 'param': 'Digit', 'type': 'uint', 'default': 2, 'label': 'количество разрядов округления', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг канала по вертикали в пунктах', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'uint', 'default': 2, 'label': 'сдвиг канала по горизонтали в барах', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': 'показывать ценовые метки', 'sinput': False}, {'mql': 'Up_Price_color', 'py': 'Up_Price_color', 'param': None, 'type': 'color', 'default': 8421376, 'label': '', 'sinput': False}, {'mql': 'Dn_Price_color', 'py': 'Dn_Price_color', 'param': None, 'type': 'color', 'default': 16711935, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
SirName = _input('SirName', 'Volume_Weighted_MA_Digit')  # первая часть имени графических объектов
Length = _input('Length', 12)  # глубина сглаживания
VolumeType = _input('VolumeType', VOLUME_TICK)  # объём
Digit = _input('Digit', 2)  # количество разрядов округления
PriceShift = _input('PriceShift', 0)  # cдвиг канала по вертикали в пунктах
Shift = _input('Shift', 2)  # сдвиг канала по горизонтали в барах
ShowPrice = _input('ShowPrice', True)  # показывать ценовые метки
Up_Price_color = _input('Up_Price_color', clrTeal)
Dn_Price_color = _input('Dn_Price_color', clrMagenta)
Up1Buffer = Arr(0, 0.0)
Dn1Buffer = Arr(0, 0.0)
Up2Buffer = Arr(0, 0.0)
Dn2Buffer = Arr(0, 0.0)
UpIndBuffer = Arr(0, 0.0)
DnIndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
FATLSize = 0
dPriceShift = 0.0
PointPow10 = 0.0
Dn_Price_name = ""
Up_Price_name = ""
Vol = Arr(0, 0.0)

def OnInit():
    global Dn_Price_name, PointPow10, Up_Price_name, dPriceShift, min_rates_total
    min_rates_total = _int(Length)
    min_rates_total += _int(Shift)
    dPriceShift = Point() * PriceShift
    PointPow10 = Point() * MathPow(10, Digit)
    Up_Price_name = SirName + 'Up_Price'
    Dn_Price_name = SirName + 'Dn_Price'
    ArrayResize(Vol, Length)
    SetIndexBuffer(0, Up1Buffer, INDICATOR_DATA)
    SetIndexBuffer(1, Dn1Buffer, INDICATOR_DATA)
    SetIndexBuffer(2, Up2Buffer, INDICATOR_DATA)
    SetIndexBuffer(3, Dn2Buffer, INDICATOR_DATA)
    SetIndexBuffer(4, UpIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, DnIndBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_SHIFT, 0)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(3, PLOT_EMPTY_VALUE, 0)
    shortname = Box("")
    StringConcatenate(shortname, 'Volume_Weighted_MA_Digit_System(', Shift, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnDeinit(reason):
    ObjectDelete(0, Up_Price_name)
    ObjectDelete(0, Dn_Price_name)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    mov = 0.0
    sum_ = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total - 1
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        sum_ = 0.0
        for kkk in range(_int(bar - Length + 1), bar + 1):
            index = bar - kkk
            if VolumeType == VOLUME_TICK:
                Vol[index] = float(tick_volume[kkk])
            else:
                Vol[index] = float(volume[kkk])
            sum_ += Vol[index]
        for rrr in range(0, _int(Length)):
            Vol[rrr] = _fdiv(Vol[rrr], sum_)
        mov = 0.0
        for kkk in range(_int(bar - Length + 1), bar + 1):
            mov += high[kkk] * Vol[bar - kkk]
        mov += dPriceShift
        Up2Buffer[bar] = PointPow10 * MathRound(_fdiv(mov, PointPow10))
        Up1Buffer[bar] = Up2Buffer[bar]
        mov = 0.0
        for kkk in range(_int(bar - Length + 1), bar + 1):
            mov += low[kkk] * Vol[bar - kkk]
        mov += dPriceShift
        Dn2Buffer[bar] = PointPow10 * MathRound(_fdiv(mov, PointPow10))
        Dn1Buffer[bar] = Dn2Buffer[bar]
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    bar = first
    for bar in range(bar, rates_total):
        clr = 2
        UpIndBuffer[bar] = 0.0
        DnIndBuffer[bar] = 0.0
        if close[bar] > Up1Buffer[bar - Shift]:
            if open[bar] < close[bar]:
                clr = 4
            else:
                clr = 3
            UpIndBuffer[bar] = high[bar]
            DnIndBuffer[bar] = low[bar]
        if close[bar] < Dn1Buffer[bar - Shift]:
            if open[bar] > close[bar]:
                clr = 0
            else:
                clr = 1
            UpIndBuffer[bar] = high[bar]
            DnIndBuffer[bar] = low[bar]
        ColorIndBuffer[bar] = clr
    else:
        bar = _range_end(bar, rates_total, 1)
    if ShowPrice:
        bar0 = rates_total - 1
        time0 = time[bar0] + (Shift * PeriodSeconds())
        SetRightPrice(0, Up_Price_name, 0, time0, Up1Buffer[bar0 - Shift], Up_Price_color)
        SetRightPrice(0, Dn_Price_name, 0, time0, Dn1Buffer[bar0 - Shift], Dn_Price_color)
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


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VolumeWeightedMADigitSystem(_MQL5Indicator):
    name = 'Volume_Weighted_MA_Digit_System'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Length': 12,  # глубина сглаживания
        'VolumeType': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # объём
        'Digit': 2,  # количество разрядов округления
        'PriceShift': 0,  # cдвиг канала по вертикали в пунктах
        'Shift': 2,  # сдвиг канала по горизонтали в барах
        'ShowPrice': True,  # показывать ценовые метки
    }

