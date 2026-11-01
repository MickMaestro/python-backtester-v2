"""finetuningma — converted from MQL5: MQL5 Indicators/FineTuningMA_StDev/finetuningma.mq5

Мувинг с более тонкой настройкой
Copyright: Copyright © 2010, gumgum; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2010, gumgum', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [14772545]}, 'widths': {1: 3}, 'styles': {1: 0}, 'labels': {1: 'FineTuningMA'}, 'levels': [], 'description': ['Мувинг с более тонкой настройкой'], 'name': 'finetuningma', 'source': 'MQL5 Indicators/FineTuningMA_StDev/finetuningma.mq5', 'folder': 'FineTuningMA_StDev', 'inputs': [{'mql': 'FTMA', 'py': 'FTMA', 'param': 'FTMA', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'rank1', 'py': 'rank1', 'param': 'rank1', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'rank2', 'py': 'rank2', 'param': 'rank2', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'rank3', 'py': 'rank3', 'param': 'rank3', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}, {'mql': 'shift1', 'py': 'shift1', 'param': 'shift1', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'shift2', 'py': 'shift2', 'param': 'shift2', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'shift3', 'py': 'shift3', 'param': 'shift3', 'type': 'double', 'default': 1.0, 'label': '', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 6, 'label': 'Ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'Сдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
FTMA = _input('FTMA', 10)
rank1 = _input('rank1', 2.0)
rank2 = _input('rank2', 2.0)
rank3 = _input('rank3', 2.0)
shift1 = _input('shift1', 1.0)
shift2 = _input('shift2', 1.0)
shift3 = _input('shift3', 1.0)
IPC = _input('IPC', PRICE_TYPICAL)  # Ценовая константа
Shift = _input('Shift', 0)  # Сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # Сдвиг индикатора по вертикали в пунктах
LineBuffer = Arr(0, 0.0)
PM = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0

def OnInit():
    global dPriceShift, min_rates_total
    dPriceShift = Point() * PriceShift
    ArrayResize(PM, FTMA)
    sum_ = 0.0
    for h in range(0, _int(FTMA)):
        PM[h] = shift1 + (MathPow(_fdiv(h, FTMA - 1.0), rank1) * (1.0 - shift1))
        PM[h] = (shift2 + (MathPow(1 - _fdiv(h, FTMA - 1.0), rank2) * (1.0 - shift2))) * PM[h]
        if _fdiv(h, FTMA - 1.0) < 0.5:
            PM[h] = (shift3 + (MathPow(1 - (_fdiv(h, FTMA - 1.0) * 2.0), rank3) * (1.0 - shift3))) * PM[h]
        else:
            PM[h] = (shift3 + (MathPow((_fdiv(h, FTMA - 1.0) * 2.0) - 1.0, rank3) * (1.0 - shift3))) * PM[h]
        sum_ += PM[h]
    sum1 = 0.0
    for h in range(0, _int(FTMA)):
        PM[h] = _fdiv(PM[h], sum_)
        sum1 += PM[h]
    min_rates_total = _int(FTMA)
    SetIndexBuffer(0, LineBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    IndicatorSetString(INDICATOR_SHORTNAME, 'FineTuningMA')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = min_rates_total
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        sum1 = 0.0
        for h in range(0, _int(FTMA)):
            sum1 += PM[h] * PriceSeries(IPC, bar - h, open, low, high, close)
        LineBuffer[bar] = sum1 + dPriceShift
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

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
    else:
        return Close[bar]


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class Finetuningma(_MQL5Indicator):
    name = 'finetuningma'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FTMA': 10,
        'rank1': 2.0,
        'rank2': 2.0,
        'rank3': 2.0,
        'shift1': 1.0,
        'shift2': 1.0,
        'shift3': 1.0,
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFollow_1 Price', 11: 'TrendFollow_2 Price', 12: 'Demark Price'}, default=6),  # Ценовая константа
        'Shift': 0,  # Сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # Сдвиг индикатора по вертикали в пунктах
    }

