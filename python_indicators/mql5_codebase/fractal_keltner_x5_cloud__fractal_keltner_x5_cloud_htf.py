"""Fractal_Keltner_x5_Cloud — converted from MQL5: MQL5 Indicators/Fractal_Keltner_x5_Cloud_HTF/Fractal_Keltner_x5_Cloud.mq5

Два фрактальных канала Кёлтнера в облачном исполнении
Copyright: Copyright © 2008, jppoton@yahoo.com; Link: http://fractalfinance.blogspot.com/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2008, jppoton@yahoo.com', 'link': 'http://fractalfinance.blogspot.com/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 4}, 'types': {1: 7, 2: 7, 3: 1, 4: 7}, 'colors': {1: [3145645], 2: [16443110], 3: [14822282], 4: [12695295]}, 'widths': {3: 2}, 'styles': {3: 0}, 'labels': {1: 'Upper Keltner 2 Cloud', 2: 'Keltner Cloud', 3: 'Frasma', 4: 'Lower Keltner 2 Cloud'}, 'levels': [], 'description': ['Два фрактальных канала Кёлтнера в облачном исполнении'], 'name': 'Fractal_Keltner_x5_Cloud', 'source': 'MQL5 Indicators/Fractal_Keltner_x5_Cloud_HTF/Fractal_Keltner_x5_Cloud.mq5', 'folder': 'Fractal_Keltner_x5_Cloud_HTF', 'inputs': [{'mql': 'e_period', 'py': 'e_period', 'param': 'e_period', 'type': 'uint', 'default': 30, 'label': 'глубина  усреднения', 'sinput': False}, {'mql': 'normal_speed', 'py': 'normal_speed', 'param': 'normal_speed', 'type': 'uint', 'default': 30, 'label': '', 'sinput': False}, {'mql': 'alpha1', 'py': 'alpha1', 'param': 'alpha1', 'type': 'double', 'default': 1.0, 'label': 'девиация 1', 'sinput': False}, {'mql': 'alpha2', 'py': 'alpha2', 'param': 'alpha2', 'type': 'double', 'default': 2.0, 'label': 'девиация 2', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора по вертикали в пунктах', 'sinput': False}, {'mql': 'Upper_color', 'py': 'Upper_color', 'param': None, 'type': 'color', 'default': 32768, 'label': '', 'sinput': False}, {'mql': 'Middle_color', 'py': 'Middle_color', 'param': None, 'type': 'color', 'default': 14822282, 'label': '', 'sinput': False}, {'mql': 'Lower_color', 'py': 'Lower_color', 'param': None, 'type': 'color', 'default': 16711935, 'label': '', 'sinput': False}, {'mql': 'FontSize', 'py': 'FontSize', 'param': 'FontSize', 'type': 'uint', 'default': 2, 'label': 'размер ценовых меток', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
e_period = _input('e_period', 30)  # глубина  усреднения
normal_speed = _input('normal_speed', 30)
alpha1 = _input('alpha1', 1.0)  # девиация 1
alpha2 = _input('alpha2', 2.0)  # девиация 2
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # cдвиг индикатора по вертикали в пунктах
Upper_color = _input('Upper_color', clrGreen)
Middle_color = _input('Middle_color', clrBlueViolet)
Lower_color = _input('Lower_color', clrMagenta)
FontSize = _input('FontSize', 2)  # размер ценовых меток
ExtLineBuffer0 = Arr(0, 0.0)
UpBuffer1 = Arr(0, 0.0)
DnBuffer1 = Arr(0, 0.0)
UpBuffer2 = Arr(0, 0.0)
DnBuffer2 = Arr(0, 0.0)
UpBuffer3 = Arr(0, 0.0)
DnBuffer3 = Arr(0, 0.0)
ExtLineBuffer3 = Arr(0, 0.0)
dPriceShift = 0.0
LOG_2 = 0.0
min_rates_total = 0
g_period_minus_1 = 0
upper_name = ""
middle_name = ""
lower_name = ""

def OnInit():
    global LOG_2, dPriceShift, g_period_minus_1, lower_name, middle_name, min_rates_total, upper_name
    min_rates_total = _int(MathMax(e_period, normal_speed))
    g_period_minus_1 = _int(e_period - 1)
    LOG_2 = MathLog(2.0)
    dPriceShift = Point() * PriceShift
    upper_name = 'Fractal_Keltner upper text lable'
    middle_name = 'Fractal_Keltner middle text lable'
    lower_name = 'Fractal_Keltner lower text lable'
    SetIndexBuffer(0, ExtLineBuffer0, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(0, UpBuffer2, INDICATOR_DATA)
    SetIndexBuffer(1, DnBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, UpBuffer1, INDICATOR_DATA)
    SetIndexBuffer(3, DnBuffer1, INDICATOR_DATA)
    SetIndexBuffer(4, ExtLineBuffer0, INDICATOR_DATA)
    SetIndexBuffer(5, UpBuffer3, INDICATOR_DATA)
    SetIndexBuffer(6, DnBuffer3, INDICATOR_DATA)
    SetIndexBuffer(7, ExtLineBuffer3, INDICATOR_CALCULATIONS)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(3, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    shortname = Box('')
    StringConcatenate(shortname, 'Fractal_Keltner_x5_Cloud(', e_period, ', ', normal_speed, ', ', DoubleToString(alpha1, 2), ', ', DoubleToString(alpha2, 2), ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

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
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        ExtLineBuffer3[bar] = PriceSeries(IPC, bar, open, low, high, close)
    else:
        bar = _range_end(bar, rates_total, 1)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    FRACTAL_BANDS(first, rates_total, high, low)
    bar0 = rates_total - 1
    SetRightPrice(0, upper_name, 0, time[bar0], UpBuffer2[bar0], Upper_color, FontSize)
    SetRightPrice(0, middle_name, 0, time[bar0], ExtLineBuffer0[bar0], Middle_color, FontSize)
    SetRightPrice(0, lower_name, 0, time[bar0], DnBuffer3[bar0], Lower_color, FontSize)
    ChartRedraw(0)
    return rates_total

def FRACTAL_BANDS(lastBar, Rates_Total, High, Low):
    diff = 0.0
    priorDiff = 0.0
    length = 0.0
    priceMax = 0.0
    priceMin = 0.0
    fdi = 0.0
    trail_dim = 0.0
    beta = 0.0
    sum_ = 0.0
    deviation = 0.0
    frasma = 0.0
    hurst = 0.0
    speed = 0
    for index in range(lastBar, Rates_Total):
        priceMax = _highest(e_period, index, ExtLineBuffer3)
        priceMin = _lowest(e_period, index, ExtLineBuffer3)
        length = 0.0
        priorDiff = 0.0
        for kkk in range(0, g_period_minus_1 + 1):
            if (priceMax - priceMin) > 0.0:
                diff = _fdiv(ExtLineBuffer3[index - kkk] - priceMin, priceMax - priceMin)
                if kkk > 0:
                    length += MathSqrt(MathPow(diff - priorDiff, 2.0) + _fdiv(1.0, MathPow(e_period, 2.0)))
                priorDiff = diff
        if length > 0.0:
            fdi = 1.0 + _fdiv(MathLog(length) + LOG_2, MathLog(2 * g_period_minus_1))
        else:
            fdi = 0.0
        hurst = 2 - fdi
        trail_dim = _fdiv(1, hurst)
        beta = trail_dim / 2
        speed = _int(MathRound(normal_speed * beta))
        sum_ = 0.0
        for iii in range(0, speed):
            sum_ += ExtLineBuffer3[MathMax(index - iii, 0)]
        ExtLineBuffer0[index] = _fdiv(sum_, speed)
        frasma = ExtLineBuffer0[index]
        Keltner = GetKeltner(e_period, index, High, Low)
        deviation = alpha1 * Keltner
        DnBuffer2[index] = frasma + (deviation * MathPow(alpha1, hurst)) + dPriceShift
        UpBuffer1[index] = DnBuffer2[index]
        UpBuffer3[index] = frasma - (deviation * MathPow(alpha1, hurst)) + dPriceShift
        DnBuffer1[index] = UpBuffer3[index]
        deviation = alpha2 * Keltner
        UpBuffer2[index] = frasma + (deviation * MathPow(alpha2, hurst)) + dPriceShift
        DnBuffer3[index] = frasma - (deviation * MathPow(alpha2, hurst)) + dPriceShift

def _highest(n, index, inputData):
    highest = 0.0
    for i in range(index - n + 1, index + 1):
        if inputData[i] > highest:
            highest = inputData[i]
    return highest

def _lowest(n, index, inputData):
    lowest = 9999999999.0
    for i in range(index - n + 1, index + 1):
        if inputData[i] < lowest:
            lowest = inputData[i]
    return lowest

def GetKeltner(period, index, High, Low):
    keltner = 0.0
    sum_ = 0.0
    for iii in range(0, period):
        sum_ += High[MathMax(index - iii, 0)] - Low[MathMax(index - iii, 0)]
    keltner = _fdiv(sum_, period)
    return keltner

def CreateRightPrice(chart_id, name, nwin, time, price, Color, Font):
    ObjectCreate(chart_id, name, OBJ_ARROW_RIGHT_PRICE, nwin, time, price)
    ObjectSetInteger(chart_id, name, OBJPROP_COLOR, Color)
    ObjectSetInteger(chart_id, name, OBJPROP_WIDTH, Font)
    ObjectSetInteger(chart_id, name, OBJPROP_BACK, True)

def SetRightPrice(chart_id, name, nwin, time, price, Color, Font):
    if ObjectFind(chart_id, name) == -1:
        CreateRightPrice(chart_id, name, nwin, time, price, Color, Font)
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


class FractalKeltnerX5Cloud(_MQL5Indicator):
    name = 'Fractal_Keltner_x5_Cloud'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'e_period': 30,  # глубина  усреднения
        'normal_speed': 30,
        'alpha1': 1.0,  # девиация 1
        'alpha2': 2.0,  # девиация 2
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # cдвиг индикатора по вертикали в пунктах
        'FontSize': 2,  # размер ценовых меток
    }

