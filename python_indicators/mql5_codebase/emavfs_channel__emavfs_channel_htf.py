"""EMAVFS_channel — converted from MQL5: MQL5 Indicators/EMAVFS_channel_HTF/EMAVFS_channel.mq5

Канал с использованием экспоненциальной скользящей средней с переменным фактором сглаживания
Copyright: Copyright © 2018, Станислав Булашев; Link: http://stan.okis.ru/file/stan/EMAVFS.pdf; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2018, Станислав Булашев', 'link': 'http://stan.okis.ru/file/stan/EMAVFS.pdf', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [16748574], 2: [9470064], 3: [9639167]}, 'widths': {1: 2, 2: 1, 3: 2}, 'styles': {1: 0, 2: 4, 3: 0}, 'labels': {1: 'EMAVFS Max', 2: 'EMAVFS', 3: 'EMAVFS Min'}, 'levels': [], 'description': ['Канал с использованием экспоненциальной скользящей средней с переменным фактором сглаживания'], 'name': 'EMAVFS_channel', 'source': 'MQL5 Indicators/EMAVFS_channel_HTF/EMAVFS_channel.mq5', 'folder': 'EMAVFS_channel_HTF', 'inputs': [{'mql': 'Wmin', 'py': 'Wmin', 'param': 'Wmin', 'type': 'double', 'default': 0.0, 'label': 'минимальная чувствительность', 'sinput': False}, {'mql': 'Wmax', 'py': 'Wmax', 'param': 'Wmax', 'type': 'double', 'default': 5.0, 'label': 'максимальная чувствительность', 'sinput': False}, {'mql': 'Efactor', 'py': 'Efactor', 'param': 'Efactor', 'type': 'double', 'default': 1.01, 'label': 'коэффициент E (менять значение около единицы на десятые и сотые доли)', 'sinput': False}, {'mql': 'Afactor', 'py': 'Afactor', 'param': 'Afactor', 'type': 'double', 'default': 1.001, 'label': 'степень A (менять значение около единицы на десятые и сотые доли)', 'sinput': False}, {'mql': 'IPC', 'py': 'IPC', 'param': 'IPC', 'type': 'int', 'default': 1, 'label': 'ценовая константа', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}, {'mql': 'PriceShift', 'py': 'PriceShift', 'param': 'PriceShift', 'type': 'int', 'default': 0, 'label': 'cдвиг индикатора по вертикали в пунктах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

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
PRICE_TRENDFOLdLow0_ = 10
PRICE_TRENDFOLdLow1_ = 11
PRICE_DEMARK_ = 12
_enum('Applied_price_', {1: 'PRICE_CLOSE_', 2: 'PRICE_OPEN_', 3: 'PRICE_HIGH_', 4: 'PRICE_LOW_', 5: 'PRICE_MEDIAN_', 6: 'PRICE_TYPICAL_', 7: 'PRICE_WEIGHTED_', 8: 'PRICE_SIMPL_', 9: 'PRICE_QUARTER_', 10: 'PRICE_TRENDFOLdLow0_', 11: 'PRICE_TRENDFOLdLow1_', 12: 'PRICE_DEMARK_'})

# ---- inputs and global variables
Wmin = _input('Wmin', 0.0)  # минимальная чувствительность
Wmax = _input('Wmax', 5.0)  # максимальная чувствительность
Efactor = _input('Efactor', 1.01)  # коэффициент E (менять значение около единицы на десятые и сотые доли)
Afactor = _input('Afactor', 1.001)  # степень A (менять значение около единицы на десятые и сотые доли)
IPC = _input('IPC', PRICE_CLOSE_)  # ценовая константа
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
PriceShift = _input('PriceShift', 0)  # cдвиг индикатора по вертикали в пунктах
IndBuffer1 = Arr(0, 0.0)
IndBuffer2 = Arr(0, 0.0)
IndBuffer3 = Arr(0, 0.0)
dPriceShift = 0.0
min_rates_total = 0

def OnInit():
    global dPriceShift, min_rates_total
    min_rates_total = 2
    SetIndexBuffer(0, IndBuffer1, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer1, False)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(1, IndBuffer2, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer2, False)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    SetIndexBuffer(2, IndBuffer3, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer3, False)
    PlotIndexSetInteger(2, PLOT_SHIFT, Shift)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    shortname = 'EMAVFS_channel'
    IndicatorSetString(INDICATOR_SHORTNAME, shortname)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits() + 1)
    dPriceShift = Point() * PriceShift

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_wema_prew
    if rates_total < min_rates_total:
        return 0
    first = 0
    bar = 0
    series = 0.0
    wema = 0.0
    w = 0.0
    eval = 0.0
    ERROR = 0.0
    ArraySetAsSeries(open, False)
    ArraySetAsSeries(high, False)
    ArraySetAsSeries(low, False)
    ArraySetAsSeries(close, False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        first = 1
        _s_OnCalculate_wema_prew = PriceSeries(IPC, first - 1, open, low, high, close)
    else:
        first = prev_calculated - 1
    bar = first
    for bar in range(bar, rates_total):
        series = PriceSeries(IPC, bar, open, low, high, close)
        w = Wmin + ((Wmax - Wmin) * (1.0 - MathExp(-MathPow(MathAbs(series - (_s_OnCalculate_wema_prew / Efactor)), Afactor))))
        wema = _s_OnCalculate_wema_prew + (w * (series - _s_OnCalculate_wema_prew))
        IndBuffer2[bar] = wema + dPriceShift
        eval = series - wema
        ERROR = wema * MathAbs(eval)
        IndBuffer1[bar] = IndBuffer2[bar] + ERROR
        IndBuffer3[bar] = IndBuffer2[bar] - ERROR
        if bar < (rates_total - 1):
            _s_OnCalculate_wema_prew = wema
    else:
        bar = _range_end(bar, rates_total, 1)
    return rates_total

def PriceSeries(applied_price, bar, dOpen, dLow, dHigh, dClose):
    _sw1 = applied_price
    if _sw1 == PRICE_CLOSE:
        return dClose[bar]
    elif _sw1 == PRICE_OPEN:
        return dOpen[bar]
    elif _sw1 == PRICE_HIGH:
        return dHigh[bar]
    elif _sw1 == PRICE_LOW:
        return dLow[bar]
    elif _sw1 == PRICE_MEDIAN:
        return (dHigh[bar] + dLow[bar]) / 2.0
    elif _sw1 == PRICE_TYPICAL:
        return (dClose[bar] + dHigh[bar] + dLow[bar]) / 3.0
    elif _sw1 == PRICE_WEIGHTED:
        return ((2 * dClose[bar]) + dHigh[bar] + dLow[bar]) / 4.0
    elif _sw1 == 8:
        return (dOpen[bar] + dClose[bar]) / 2.0
    elif _sw1 == 9:
        return (dOpen[bar] + dClose[bar] + dHigh[bar] + dLow[bar]) / 4.0
    elif _sw1 == 10:
        if dClose[bar] > dOpen[bar]:
            return dHigh[bar]
        else:
            if dClose[bar] < dOpen[bar]:
                return dLow[bar]
            else:
                return dClose[bar]
    elif _sw1 == 11:
        if dClose[bar] > dOpen[bar]:
            return (dHigh[bar] + dClose[bar]) / 2.0
        else:
            if dClose[bar] < dOpen[bar]:
                return (dLow[bar] + dClose[bar]) / 2.0
            else:
                return dClose[bar]
    elif _sw1 == 12:
        res = dHigh[bar] + dLow[bar] + dClose[bar]
        if dClose[bar] < dOpen[bar]:
            res = (res + dLow[bar]) / 2
        if dClose[bar] > dOpen[bar]:
            res = (res + dHigh[bar]) / 2
        if dClose[bar] == dOpen[bar]:
            res = (res + dClose[bar]) / 2
        return (res - dLow[bar] + (res - dHigh[bar])) / 2
    else:
        return dClose[bar]

# ---- static local variables
_s_OnCalculate_wema_prew = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class EMAVFSChannel(_MQL5Indicator):
    name = 'EMAVFS_channel'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'Wmin': 0.0,  # минимальная чувствительность
        'Wmax': 5.0,  # максимальная чувствительность
        'Efactor': 1.01,  # коэффициент E (менять значение около единицы на десятые и сотые доли)
        'Afactor': 1.001,  # степень A (менять значение около единицы на десятые и сотые доли)
        'IPC': _Choice({1: 'Close', 2: 'Open', 3: 'High', 4: 'Low', 5: 'Median Price (HL/2)', 6: 'Typical Price (HLC/3)', 7: 'Weighted Close (HLCC/4)', 8: 'Simpl Price (OC/2)', 9: 'Quarted Price (HLOC/4)', 10: 'TrendFoldLow_1 Price', 11: 'TrendFoldLow_2 Price', 12: 'Demark Price'}, default=1),  # ценовая константа
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
        'PriceShift': 0,  # cдвиг индикатора по вертикали в пунктах
    }

