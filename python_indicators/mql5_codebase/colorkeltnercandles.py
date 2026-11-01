"""ColorKeltnerCandles — converted from MQL5: MQL5 Indicators/ColorKeltnerCandles/ColorKeltnerCandles.mq5

ColorKeltnerCandles
Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16711935, 255, 17919, 3937500, 2763429, 4294967295, 5737262, 7451452, 3329434, 65280, 16776960]}, 'widths': {}, 'styles': {}, 'labels': {1: 'ColorKeltnerCandles Десять цветов'}, 'levels': [], 'description': ['ColorKeltnerCandles'], 'name': 'ColorKeltnerCandles', 'source': 'MQL5 Indicators/ColorKeltnerCandles/ColorKeltnerCandles.mq5', 'folder': 'ColorKeltnerCandles', 'inputs': [{'mql': 'BandsPeriod', 'py': 'BandsPeriod', 'param': 'BandsPeriod', 'type': 'int', 'default': 100, 'label': 'период усреднения', 'sinput': False}, {'mql': 'BandsDeviation1', 'py': 'BandsDeviation1', 'param': 'BandsDeviation1', 'type': 'double', 'default': 1.0, 'label': 'девиация первого уровня', 'sinput': False}, {'mql': 'BandsDeviation2', 'py': 'BandsDeviation2', 'param': 'BandsDeviation2', 'type': 'double', 'default': 1.5, 'label': 'девиация второго уровня', 'sinput': False}, {'mql': 'BandsDeviation3', 'py': 'BandsDeviation3', 'param': 'BandsDeviation3', 'type': 'double', 'default': 2.0, 'label': 'девиация третьего уровня', 'sinput': False}, {'mql': 'BandsDeviation4', 'py': 'BandsDeviation4', 'param': 'BandsDeviation4', 'type': 'double', 'default': 2.5, 'label': 'девиация четвёртого уровня', 'sinput': False}, {'mql': 'BandsDeviation5', 'py': 'BandsDeviation5', 'param': 'BandsDeviation5', 'type': 'double', 'default': 3.0, 'label': 'девиация пятого уровня', 'sinput': False}, {'mql': 'MA_Method_', 'py': 'MA_Method_', 'param': 'MA_Method_', 'type': 'int', 'default': 1, 'label': 'метод усреднения индикатора', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
BandsPeriod = _input('BandsPeriod', 100)  # период усреднения
BandsDeviation1 = _input('BandsDeviation1', 1.0)  # девиация первого уровня
BandsDeviation2 = _input('BandsDeviation2', 1.5)  # девиация второго уровня
BandsDeviation3 = _input('BandsDeviation3', 2.0)  # девиация третьего уровня
BandsDeviation4 = _input('BandsDeviation4', 2.5)  # девиация четвёртого уровня
BandsDeviation5 = _input('BandsDeviation5', 3.0)  # девиация пятого уровня
MA_Method_ = _input('MA_Method_', MODE_EMA)  # метод усреднения индикатора
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorsBuffer = Arr(0, 0.0)
StartBars = 0

def OnInit():
    global StartBars
    StartBars = BandsPeriod + 1
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorsBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, StartBars)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'ColorKeltnerCandles'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < StartBars:
        return 0
    price_ = 0.0
    Keltner = 0.0
    ma = 0.0
    UpKeltner1 = 0.0
    UpKeltner2 = 0.0
    UpKeltner3 = 0.0
    UpKeltner4 = 0.0
    UpKeltner5 = 0.0
    DnKeltner1 = 0.0
    DnKeltner2 = 0.0
    DnKeltner3 = 0.0
    DnKeltner4 = 0.0
    DnKeltner5 = 0.0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 0
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        price_ = PriceSeries(IPC, bar, open, low, high, close)
        ma = MA.MASeries(0, prev_calculated, rates_total, BandsPeriod, MA_Method_, price_, bar, False)
        Keltner = GetKeltner(BandsPeriod, bar, high, low)
        UpKeltner1 = ma + (Keltner * BandsDeviation1)
        UpKeltner2 = ma + (Keltner * BandsDeviation2)
        UpKeltner3 = ma + (Keltner * BandsDeviation3)
        UpKeltner4 = ma + (Keltner * BandsDeviation4)
        UpKeltner5 = ma + (Keltner * BandsDeviation5)
        DnKeltner1 = ma - (Keltner * BandsDeviation1)
        DnKeltner2 = ma - (Keltner * BandsDeviation2)
        DnKeltner3 = ma - (Keltner * BandsDeviation3)
        DnKeltner4 = ma - (Keltner * BandsDeviation4)
        DnKeltner5 = ma - (Keltner * BandsDeviation5)
        if (price_ > UpKeltner1 or price_ < DnKeltner1) and bar > StartBars:
            if price_ > UpKeltner5:
                ExtColorsBuffer[bar] = 10.0
            elif price_ > UpKeltner4:
                ExtColorsBuffer[bar] = 9.0
            elif price_ > UpKeltner3:
                ExtColorsBuffer[bar] = 8.0
            elif price_ > UpKeltner2:
                ExtColorsBuffer[bar] = 7.0
            elif price_ > UpKeltner1:
                ExtColorsBuffer[bar] = 6.0
            elif price_ < DnKeltner5:
                ExtColorsBuffer[bar] = 0.0
            elif price_ < DnKeltner4:
                ExtColorsBuffer[bar] = 1.0
            elif price_ < DnKeltner3:
                ExtColorsBuffer[bar] = 2.0
            elif price_ < DnKeltner2:
                ExtColorsBuffer[bar] = 3.0
            elif price_ < DnKeltner1:
                ExtColorsBuffer[bar] = 4.0
            ExtOpenBuffer[bar] = open[bar]
            ExtHighBuffer[bar] = high[bar]
            ExtLowBuffer[bar] = low[bar]
            ExtCloseBuffer[bar] = close[bar]
        else:
            ExtOpenBuffer[bar] = 0.0
            ExtHighBuffer[bar] = 0.0
            ExtLowBuffer[bar] = 0.0
            ExtCloseBuffer[bar] = 0.0
            ExtColorsBuffer[bar] = 5.0
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def GetKeltner(period, bar, High, Low):
    keltner = 0.0
    sum_ = 0.0
    for iii in range(0, period):
        sum_ += High[MathMax(0, bar - iii)] - Low[MathMax(0, bar - iii)]
    keltner = _fdiv(sum_, period)
    return keltner

# ---- global variables initialised from expressions
MA = _alloc(CMoving_Average)
MA.__init__()


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class ColorKeltnerCandles(_MQL5Indicator):
    name = 'ColorKeltnerCandles'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'BandsPeriod': 100,  # период усреднения
        'BandsDeviation1': 1.0,  # девиация первого уровня
        'BandsDeviation2': 1.5,  # девиация второго уровня
        'BandsDeviation3': 2.0,  # девиация третьего уровня
        'BandsDeviation4': 2.5,  # девиация четвёртого уровня
        'BandsDeviation5': 3.0,  # девиация пятого уровня
        'MA_Method_': _Choice({0: 'Sma', 1: 'Ema', 2: 'Smma', 3: 'Lwma'}, default=1),  # метод усреднения индикатора
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
    }

