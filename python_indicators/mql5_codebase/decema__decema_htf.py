"""decema — converted from MQL5: MQL5 Indicators/DecEMA_HTF/decema.mq5

Copyright: 2013,   Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 3.24

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library
from backtester.mql5.lib.smoothalgorithms import *  # #include SmoothAlgorithms.mqh

MQL5_META = {'props': {'copyright': '2013,   Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '3.24', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [255]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'DecEMA'}, 'levels': [], 'description': [], 'name': 'decema', 'source': 'MQL5 Indicators/DecEMA_HTF/decema.mq5', 'folder': 'DecEMA_HTF', 'inputs': [{'mql': 'EMA_Period', 'py': 'EMA_Period', 'param': 'EMA_Period', 'type': 'uint', 'default': 3, 'label': 'Период EMA', 'sinput': False}, {'mql': 'ELength', 'py': 'ELength', 'param': 'ELength', 'type': 'int', 'default': 15, 'label': 'Глубина сглаживания', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': ['SmoothAlgorithms.mqh']}

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
EMA_Period = _input('EMA_Period', 3)  # Период EMA
ELength = _input('ELength', 15)  # Глубина сглаживания
IPC = _input('IPC', PRICE_CLOSE)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
IndBuffer = Arr(0, 0.0)
min_rates_total = 0
alfa = 0.0
dPriceShift = 0.0

def OnInit():
    global alfa, dPriceShift, min_rates_total
    min_rates_total = 2
    alfa = _fdiv(2.0, 1.0 + ELength)
    dPriceShift = Point() * PriceShift
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = Box("")
    StringConcatenate(shortname, 'DecEMA(', EMA_Period, ',', ELength, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_sdEMA1, _s_OnCalculate_sdEMA10, _s_OnCalculate_sdEMA2, _s_OnCalculate_sdEMA3, _s_OnCalculate_sdEMA4, _s_OnCalculate_sdEMA5, _s_OnCalculate_sdEMA6, _s_OnCalculate_sdEMA7, _s_OnCalculate_sdEMA8, _s_OnCalculate_sdEMA9
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    maxbar = 0
    price = 0.0
    EMA0 = 0.0
    EMA1 = 0.0
    EMA2 = 0.0
    EMA3 = 0.0
    EMA4 = 0.0
    EMA5 = 0.0
    EMA6 = 0.0
    EMA7 = 0.0
    EMA8 = 0.0
    EMA9 = 0.0
    EMA10 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
        _s_OnCalculate_sdEMA1 = PriceSeries(IPC, first - 1, open, low, high, close)
        _s_OnCalculate_sdEMA2 = _s_OnCalculate_sdEMA1
        _s_OnCalculate_sdEMA3 = _s_OnCalculate_sdEMA1
        _s_OnCalculate_sdEMA4 = _s_OnCalculate_sdEMA1
        _s_OnCalculate_sdEMA5 = _s_OnCalculate_sdEMA1
        _s_OnCalculate_sdEMA6 = _s_OnCalculate_sdEMA1
        _s_OnCalculate_sdEMA7 = _s_OnCalculate_sdEMA1
        _s_OnCalculate_sdEMA8 = _s_OnCalculate_sdEMA1
        _s_OnCalculate_sdEMA9 = _s_OnCalculate_sdEMA1
        _s_OnCalculate_sdEMA10 = _s_OnCalculate_sdEMA1
    else:
        first = prev_calculated - 1
    EMA1 = _s_OnCalculate_sdEMA1
    EMA2 = _s_OnCalculate_sdEMA2
    EMA3 = _s_OnCalculate_sdEMA3
    EMA4 = _s_OnCalculate_sdEMA4
    EMA5 = _s_OnCalculate_sdEMA5
    EMA6 = _s_OnCalculate_sdEMA6
    EMA7 = _s_OnCalculate_sdEMA7
    EMA8 = _s_OnCalculate_sdEMA8
    EMA9 = _s_OnCalculate_sdEMA9
    EMA10 = _s_OnCalculate_sdEMA10
    maxbar = rates_total - 1
    bar = first
    for bar in range(bar, rates_total):
        price = PriceSeries(IPC, bar, open, low, high, close)
        EMA0 = XMA1.XMASeries(1, prev_calculated, rates_total, 1, 0, EMA_Period, price, bar, False)
        EMA1 = (alfa * EMA0) + ((1 - alfa) * EMA1)
        EMA2 = (alfa * EMA1) + ((1 - alfa) * EMA2)
        EMA3 = (alfa * EMA2) + ((1 - alfa) * EMA3)
        EMA4 = (alfa * EMA3) + ((1 - alfa) * EMA4)
        EMA5 = (alfa * EMA4) + ((1 - alfa) * EMA5)
        EMA6 = (alfa * EMA5) + ((1 - alfa) * EMA6)
        EMA7 = (alfa * EMA6) + ((1 - alfa) * EMA7)
        EMA8 = (alfa * EMA7) + ((1 - alfa) * EMA8)
        EMA9 = (alfa * EMA8) + ((1 - alfa) * EMA9)
        EMA10 = (alfa * EMA9) + ((1 - alfa) * EMA10)
        IndBuffer[bar] = (10 * EMA1) - (45 * EMA2) + (120 * EMA3) - (210 * EMA4) + (252 * EMA5) - (210 * EMA6) + (120 * EMA7) - (45 * EMA8) + (10 * EMA9) - EMA10
        IndBuffer[bar] += dPriceShift
        if bar < maxbar:
            _s_OnCalculate_sdEMA1 = EMA1
            _s_OnCalculate_sdEMA2 = EMA2
            _s_OnCalculate_sdEMA3 = EMA3
            _s_OnCalculate_sdEMA4 = EMA4
            _s_OnCalculate_sdEMA5 = EMA5
            _s_OnCalculate_sdEMA6 = EMA6
            _s_OnCalculate_sdEMA7 = EMA7
            _s_OnCalculate_sdEMA8 = EMA8
            _s_OnCalculate_sdEMA9 = EMA9
            _s_OnCalculate_sdEMA10 = EMA10
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

# ---- global variables initialised from expressions
XMA1 = _alloc(CXMA)
XMA1.__init__()

# ---- static local variables
_s_OnCalculate_sdEMA1 = 0.0
_s_OnCalculate_sdEMA2 = 0.0
_s_OnCalculate_sdEMA3 = 0.0
_s_OnCalculate_sdEMA4 = 0.0
_s_OnCalculate_sdEMA5 = 0.0
_s_OnCalculate_sdEMA6 = 0.0
_s_OnCalculate_sdEMA7 = 0.0
_s_OnCalculate_sdEMA8 = 0.0
_s_OnCalculate_sdEMA9 = 0.0
_s_OnCalculate_sdEMA10 = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Decema(_MQL5Indicator):
    name = 'decema'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'EMA_Period': 3,  # Период EMA
        'ELength': 15,  # Глубина сглаживания
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=1),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
    }

