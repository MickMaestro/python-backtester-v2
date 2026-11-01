"""WATR_Candles — converted from MQL5: MQL5 Indicators/WATR_Candles/WATR_Candles.mq5

Copyright: Written WizardSerg under article konkop in <Modern trading> #4/2001; Link: http://www.wizardserg.inweb.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Written WizardSerg under article konkop in <Modern trading> #4/2001', 'link': 'http://www.wizardserg.inweb.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 5, 'indicator_plots': 1}, 'types': {1: 17}, 'colors': {1: [16760576, 16711680, 8421504, 128, 14053594]}, 'widths': {}, 'styles': {}, 'labels': {1: 'WATROpen;WATRHigh;WATRLow;WATRClose'}, 'levels': [], 'description': [], 'name': 'WATR_Candles', 'source': 'MQL5 Indicators/WATR_Candles/WATR_Candles.mq5', 'folder': 'WATR_Candles', 'inputs': [{'mql': 'WATR_K', 'py': 'WATR_K', 'param': 'WATR_K', 'type': 'int', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'WATR_M', 'py': 'WATR_M', 'param': 'WATR_M', 'type': 'double', 'default': 4.0, 'label': '', 'sinput': False}, {'mql': 'ATR', 'py': 'ATR', 'param': 'ATR', 'type': 'int', 'default': 21, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг индикатора по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
WATR_K = _input('WATR_K', 10)
WATR_M = _input('WATR_M', 4.0)
ATR = _input('ATR', 21)
Shift = _input('Shift', 0)  # сдвиг индикатора по горизонтали в барах
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorsBuffer = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0

def AntiTrendBar(Open, Close, index, NRTR_Up_prev):
    res = (TrendUp(Close, index, NRTR_Up_prev) and Close[index] < Open[index]) or ((not TrendUp(Close, index, NRTR_Up_prev)) and Close[index] > Open[index])
    return res

def CalcIndicValue(ATRArray, Close, index, trend):
    res = Close[index]
    if trend:
        res -= (WATR_K * Point()) + (WATR_M * ATRArray[index])
    else:
        res += (WATR_K * Point()) + (WATR_M * ATRArray[index])
    return res

def TrendUp(Close, index, NRTR_Up_prev):
    return Close[index + 1] > NRTR_Up_prev and _bool(NRTR_Up_prev)

def OnInit():
    global ATR_Handle, min_rates_total
    ATR_Handle = iATR(None, 0, ATR)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    min_rates_total = ATR
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorsBuffer, INDICATOR_COLOR_INDEX)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorsBuffer, True)
    shortname = Box("")
    StringConcatenate(shortname, 'WATR_Candles(', WATR_K, ', ', WATR_M, ', ', ATR, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_Down_prev, _s_OnCalculate_Up_prev
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    limit = 0
    to_copy = 0
    bar = 0
    iATR_ = Arr(0, 0.0)
    Up = 0.0
    Down = 0.0
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(iATR_, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        to_copy = rates_total
        _s_OnCalculate_Down_prev = close[limit + 1] - (WATR_K * Point())
        _s_OnCalculate_Up_prev = _s_OnCalculate_Down_prev
    else:
        limit = rates_total - prev_calculated
        to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, iATR_) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if AntiTrendBar(open, close, bar, _s_OnCalculate_Up_prev):
            Up = _s_OnCalculate_Up_prev
            Down = _s_OnCalculate_Down_prev
        else:
            if TrendUp(close, bar, _s_OnCalculate_Up_prev):
                Up = CalcIndicValue(iATR_, close, bar, True)
                if Up < _s_OnCalculate_Up_prev:
                    Up = _s_OnCalculate_Up_prev
                Down = 0.0
            else:
                Down = CalcIndicValue(iATR_, close, bar, False)
                if Down > _s_OnCalculate_Down_prev:
                    Down = _s_OnCalculate_Down_prev
                Up = 0.0
        if TrendUp(close, bar, _s_OnCalculate_Up_prev) and close[bar] < Up:
            Down = CalcIndicValue(iATR_, close, bar, False)
            Up = 0.0
        if (not TrendUp(close, bar, _s_OnCalculate_Up_prev)) and close[bar] > Down:
            Up = CalcIndicValue(iATR_, close, bar, True)
            Down = 0.0
        ExtOpenBuffer[bar] = open[bar]
        ExtHighBuffer[bar] = high[bar]
        ExtLowBuffer[bar] = low[bar]
        ExtCloseBuffer[bar] = close[bar]
        if Up:
            if open[bar] <= close[bar]:
                ExtColorsBuffer[bar] = 0.0
            else:
                ExtColorsBuffer[bar] = 1.0
        if Down:
            if open[bar] >= close[bar]:
                ExtColorsBuffer[bar] = 4.0
            else:
                ExtColorsBuffer[bar] = 3.0
        if bar:
            _s_OnCalculate_Up_prev = Up
            _s_OnCalculate_Down_prev = Down
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_Up_prev = 0.0
_s_OnCalculate_Down_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class WATRCandles(_MQL5Indicator):
    name = 'WATR_Candles'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'WATR_K': 10,
        'WATR_M': 4.0,
        'ATR': 21,
        'Shift': 0,  # сдвиг индикатора по горизонтали в барах
    }

