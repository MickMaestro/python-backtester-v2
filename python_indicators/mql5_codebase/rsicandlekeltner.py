"""RSICandleKeltner — converted from MQL5: MQL5 Indicators/RSICandleKeltner/RSICandleKeltner.mq5

RSICandle Smoothed
Copyright: Copyright © 2017, Nikolay Kositsin; Link: farria@mail.redcom.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2017, Nikolay Kositsin', 'link': 'farria@mail.redcom.ru', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 2}, 'types': {1: 17, 2: 7}, 'colors': {1: [9639167, 16711680, 8421376], 2: [16443110]}, 'widths': {}, 'styles': {}, 'labels': {1: 'RSICandle Open;RSICandle High;RSICandle Low;RSICandle Close', 2: 'Channels'}, 'levels': [70.0, 50.0, 30.0], 'description': ['RSICandle Smoothed'], 'name': 'RSICandleKeltner', 'source': 'MQL5 Indicators/RSICandleKeltner/RSICandleKeltner.mq5', 'folder': 'RSICandleKeltner', 'inputs': [{'mql': 'RSI_Period', 'py': 'RSI_Period', 'param': 'RSI_Period', 'type': 'uint', 'default': 14, 'label': '', 'sinput': False}, {'mql': 'KeltnerPeriod', 'py': 'KeltnerPeriod', 'param': 'KeltnerPeriod', 'type': 'int', 'default': 20, 'label': 'период усреднения Келтнера', 'sinput': False}, {'mql': 'Ratio', 'py': 'Ratio', 'param': 'Ratio', 'type': 'double', 'default': 3.01, 'label': 'девиация канала', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг канала по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
RSI_Period = _input('RSI_Period', 14)
KeltnerPeriod = _input('KeltnerPeriod', 20)  # период усреднения Келтнера
Ratio = _input('Ratio', 3.01)  # девиация канала
Shift = _input('Shift', 0)  # сдвиг канала по горизонтали в барах
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
BorderTopBuffer = Arr(0, 0.0)
BorderBotBuffer = Arr(0, 0.0)
min_rates_1 = 0
min_rates_total = 0
RSI_Handle = Arr(4, 0, dyn=False)
MA_Handle = 0

def OnInit():
    global MA_Handle, min_rates_1, min_rates_total
    min_rates_1 = _int(RSI_Period)
    min_rates_total = min_rates_1 + KeltnerPeriod
    RSI_Handle[0] = iRSI(None, 0, RSI_Period, PRICE_OPEN)
    if RSI_Handle[0] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI[' + _str(0) + ']!')
        return INIT_FAILED
    RSI_Handle[1] = iRSI(None, 0, RSI_Period, PRICE_HIGH)
    if RSI_Handle[1] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI[' + _str(1) + ']!')
        return INIT_FAILED
    RSI_Handle[2] = iRSI(None, 0, RSI_Period, PRICE_LOW)
    if RSI_Handle[2] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI[' + _str(2) + ']!')
        return INIT_FAILED
    RSI_Handle[3] = iRSI(None, 0, RSI_Period, PRICE_CLOSE)
    if RSI_Handle[3] == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iRSI[' + _str(3) + ']!')
        return INIT_FAILED
    MA_Handle = iMA(None, 0, KeltnerPeriod, 0, MODE_SMA, RSI_Handle[3])
    if MA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, BorderTopBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, BorderBotBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    ArraySetAsSeries(BorderTopBuffer, True)
    ArraySetAsSeries(BorderBotBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    short_name = 'RSICandleKeltner'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if ((((BarsCalculated(RSI_Handle[0]) < rates_total or BarsCalculated(RSI_Handle[1]) < rates_total) or BarsCalculated(RSI_Handle[2]) < rates_total) or BarsCalculated(RSI_Handle[3]) < rates_total) or BarsCalculated(MA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    MA = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(RSI_Handle[0], 0, 0, to_copy, ExtOpenBuffer) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[1], 0, 0, to_copy, ExtHighBuffer) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[2], 0, 0, to_copy, ExtLowBuffer) <= 0:
        return 0
    if CopyBuffer(RSI_Handle[3], 0, 0, to_copy, ExtCloseBuffer) <= 0:
        return 0
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MA) <= 0:
        return 0
    ArraySetAsSeries(MA, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Max = MathMax(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        Min = MathMin(ExtOpenBuffer[bar], ExtCloseBuffer[bar])
        ExtHighBuffer[bar] = MathMax(Max, ExtHighBuffer[bar])
        ExtLowBuffer[bar] = MathMin(Min, ExtLowBuffer[bar])
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 2.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
        Keltner = Ratio * GetKeltner(KeltnerPeriod, bar, ExtHighBuffer, ExtLowBuffer)
        BorderTopBuffer[bar] = MA[bar] + Keltner
        BorderBotBuffer[bar] = MA[bar] - Keltner
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def GetKeltner(period, bar, High, Low):
    Resalt = 0.0
    sum_ = 0.0
    for iii in range(0, period):
        sum_ += High[bar + iii] - Low[bar + iii]
    Resalt = _fdiv(sum_, period)
    return Resalt


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class RSICandleKeltner(_MQL5Indicator):
    name = 'RSICandleKeltner'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'RSI_Period': 14,
        'KeltnerPeriod': 20,  # период усреднения Келтнера
        'Ratio': 3.01,  # девиация канала
        'Shift': 0,  # сдвиг канала по горизонтали в барах
    }

