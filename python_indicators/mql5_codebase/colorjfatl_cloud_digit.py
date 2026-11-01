"""ColorJFatl_Cloud_Digit — converted from MQL5: MQL5 Indicators/ColorJFatl_Cloud_Digit/ColorJFatl_Cloud_Digit.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).

Notes:
- Chart objects (labels, lines, arrows created with ObjectCreate) are kept in memory but not drawn; only indicator buffers are plotted.
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 6, 'indicator_plots': 3}, 'types': {1: 7, 2: 7, 3: 8}, 'colors': {1: [15658671], 2: [14204888], 3: [16711935, 8421504, 55295]}, 'widths': {3: 5}, 'styles': {3: 0}, 'labels': {1: 'Upper Cloud', 2: 'Lower Cloud', 3: 'JFATL'}, 'levels': [], 'description': [], 'name': 'ColorJFatl_Cloud_Digit', 'source': 'MQL5 Indicators/ColorJFatl_Cloud_Digit/ColorJFatl_Cloud_Digit.mq5', 'folder': 'ColorJFatl_Cloud_Digit', 'inputs': [{'mql': 'SirName', 'py': 'SirName', 'param': None, 'type': 'string', 'default': 'ColorJFatl_Cloud_Digit', 'label': 'Первая часть имени графических объектов', 'sinput': False}, {'mql': 'JLength', 'py': 'JLength', 'param': 'JLength', 'type': 'int', 'default': 5, 'label': 'глубина JMA сглаживания', 'sinput': False}, {'mql': 'JPhase', 'py': 'JPhase', 'param': 'JPhase', 'type': 'int', 'default': -100, 'label': 'параметр JMA сглаживания,', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'FATLShift', 'py': 'FATLShift', 'param': 'FATLShift', 'type': 'int', 'default': 0, 'label': 'сдвиг Фатла по горизонтали в барах', 'sinput': False}, {'mql': 'PriceFATLShift', 'py': 'PriceFATLShift', 'param': 'PriceFATLShift', 'type': 'int', 'default': 0, 'label': 'cдвиг Фатла по вертикали в пунктах', 'sinput': False}, {'mql': 'Dev', 'py': 'Dev', 'param': 'Dev', 'type': 'uint', 'default': 20, 'label': 'Девиация заливки фоном', 'sinput': False}, {'mql': 'Digit', 'py': 'Digit', 'param': 'Digit', 'type': 'uint', 'default': 2, 'label': 'количество разрядов округления', 'sinput': False}, {'mql': 'ShowPrice', 'py': 'ShowPrice', 'param': 'ShowPrice', 'type': 'bool', 'default': True, 'label': 'показывать ценовые метки', 'sinput': False}, {'mql': 'Price_color', 'py': 'Price_color', 'param': None, 'type': 'color', 'default': 8421504, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
SirName = _input('SirName', 'ColorJFatl_Cloud_Digit')  # Первая часть имени графических объектов
JLength = _input('JLength', 5)  # глубина JMA сглаживания
JPhase = _input('JPhase', -100)  # параметр JMA сглаживания,
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
FATLShift = _input('FATLShift', 0)  # сдвиг Фатла по горизонтали в барах
PriceFATLShift = _input('PriceFATLShift', 0)  # cдвиг Фатла по вертикали в пунктах
Dev = _input('Dev', 20)  # Девиация заливки фоном
Digit = _input('Digit', 2)  # количество разрядов округления
ShowPrice = _input('ShowPrice', True)  # показывать ценовые метки
Price_color = _input('Price_color', clrGray)
FATLPeriod = 39
LineBuffer = Arr(0, 0.0)
ColorLineBuffer = Arr(0, 0.0)
UpCloudBuffer1 = Arr(0, 0.0)
UpCloudBuffer2 = Arr(0, 0.0)
DnCloudBuffer1 = Arr(0, 0.0)
DnCloudBuffer2 = Arr(0, 0.0)
min_rates_total = 0
fstart = 0
FATLSize = 0
dPriceFATLShift = 0.0
PointPow10 = 0.0
Price_name = ""
dFATLTable = Arr.of([0.436040945, 0.3658689069, 0.2460452079, 0.1104506886, -0.0054034585, -0.0760367731, -0.0933058722, -0.0670110374, -0.0190795053, 0.0259609206, 0.0502044896, 0.0477818607, 0.0249252327, -0.0047706151, -0.0272432537, -0.0338917071, -0.0244141482, -0.0055774838, 0.0128149838, 0.0226522218, 0.0208778257, 0.0100299086, -0.0036771622, -0.013674485, -0.0160483392, -0.0108597376, -0.0016060704, 0.0069480557, 0.0110573605, 0.0095711419, 0.0040444064, -0.0023824623, -0.0067093714, -0.00720034, -0.004771771, 0.0005541115, 0.000786016, 0.0130129076, 0.0040364019], fill=0.0)

def OnInit():
    global FATLSize, PointPow10, Price_name, dPriceFATLShift, min_rates_total
    FATLSize = ArraySize(dFATLTable)
    min_rates_total = FATLSize + 30
    PointPow10 = Point() * MathPow(10, Digit)
    Price_name = SirName + 'Price'
    shortname = Box("")
    StringConcatenate(shortname, 'JFatl_Cloud_Digit(', JLength, ' ,', JPhase, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    dPriceFATLShift = Point() * PriceFATLShift
    SetIndexBuffer(0, UpCloudBuffer1, INDICATOR_DATA)
    SetIndexBuffer(1, UpCloudBuffer2, INDICATOR_DATA)
    SetIndexBuffer(2, DnCloudBuffer1, INDICATOR_DATA)
    SetIndexBuffer(3, DnCloudBuffer2, INDICATOR_DATA)
    SetIndexBuffer(4, LineBuffer, INDICATOR_DATA)
    SetIndexBuffer(5, ColorLineBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_SHIFT, FATLShift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(1, PLOT_SHIFT, FATLShift)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0.0)
    PlotIndexSetInteger(2, PLOT_SHIFT, FATLShift)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, 0.0)

def OnDeinit(reason):
    ObjectDelete(0, Price_name)
    ChartRedraw(0)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global fstart
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    jfatl = 0.0
    FATL = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = FATLPeriod - 1
        fstart = first
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        FATL = 0.0
        iii = 0
        while iii < FATLSize:
            FATL += dFATLTable[iii] * PriceSeries(IPC, bar - iii, open, low, high, close)
            iii += 1
        jfatl = _s_OnCalculate_JMA.JJMASeries(fstart, prev_calculated, rates_total, 0, JPhase, JLength, FATL, bar, False)
        LineBuffer[bar] = jfatl + dPriceFATLShift
        DnCloudBuffer1[bar] = PointPow10 * MathRound(_fdiv(LineBuffer[bar], PointPow10))
        UpCloudBuffer2[bar] = DnCloudBuffer1[bar]
        LineBuffer[bar] = UpCloudBuffer2[bar]
        UpCloudBuffer1[bar] = LineBuffer[bar] * Dev
        DnCloudBuffer2[bar] = LineBuffer[bar] / Dev
    else:
        bar = _range_end(bar, rates_total, 1)
    if ShowPrice:
        bar0 = rates_total - 1
        time0 = time[bar0] + (1 * PeriodSeconds())
        SetRightPrice(0, Price_name, 0, time0, LineBuffer[bar0], Price_color)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first += 1
    bar = first
    for bar in range(bar, rates_total):
        clr = 1.0
        trend = LineBuffer[bar] - LineBuffer[bar - 1]
        if not trend:
            clr = ColorLineBuffer[bar - 1]
        else:
            if trend > 0:
                clr = 2.0
            if trend < 0:
                clr = 0.0
        ColorLineBuffer[bar] = clr
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

# ---- static local variables
_s_OnCalculate_JMA = CJJMA()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorJFatlCloudDigit(_MQL5Indicator):
    name = 'ColorJFatl_Cloud_Digit'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'JLength': 5,  # глубина JMA сглаживания
        'JPhase': -100,  # параметр JMA сглаживания,
        'IPC': _Choice({1: 'PRICE_CLOSE', 2: 'PRICE_OPEN', 3: 'PRICE_HIGH', 4: 'PRICE_LOW', 5: 'PRICE_MEDIAN', 6: 'PRICE_TYPICAL', 7: 'PRICE_WEIGHTED', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'FATLShift': 0,  # сдвиг Фатла по горизонтали в барах
        'PriceFATLShift': 0,  # cдвиг Фатла по вертикали в пунктах
        'Dev': 20,  # Девиация заливки фоном
        'Digit': 2,  # количество разрядов округления
        'ShowPrice': True,  # показывать ценовые метки
    }

