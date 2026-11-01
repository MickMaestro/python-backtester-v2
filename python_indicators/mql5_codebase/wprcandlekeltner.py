"""WPRCandleKeltner — converted from MQL5: MQL5 Indicators/WPRCandleKeltner/WPRCandleKeltner.mq5

Williams’ Percent Range
Copyright: Copyright © 2005, Dark Han; Link: http://www.metaquotes.net/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2005, Dark Han', 'link': 'http://www.metaquotes.net/', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 7, 'indicator_plots': 2}, 'types': {1: 17, 2: 7}, 'colors': {1: [9639167, 16711680, 8421376], 2: [16443110]}, 'widths': {}, 'styles': {}, 'labels': {1: 'WPRCandle Open;WPRCandle High;WPRCandle Low;WPRCandle Close', 2: 'Channels'}, 'levels': [-70.0, -50.0, -30.0], 'description': ['Williams’ Percent Range'], 'name': 'WPRCandleKeltner', 'source': 'MQL5 Indicators/WPRCandleKeltner/WPRCandleKeltner.mq5', 'folder': 'WPRCandleKeltner', 'inputs': [{'mql': 'ExtWPRPeriod', 'py': 'ExtWPRPeriod', 'param': 'ExtWPRPeriod', 'type': 'uint', 'default': 11, 'label': '', 'sinput': False}, {'mql': 'KeltnerPeriod', 'py': 'KeltnerPeriod', 'param': 'KeltnerPeriod', 'type': 'uint', 'default': 20, 'label': 'период усреднения Кёлтнера', 'sinput': False}, {'mql': 'Ratio', 'py': 'Ratio', 'param': 'Ratio', 'type': 'double', 'default': 1.5, 'label': 'девиация канала', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'сдвиг канала по горизонтали в барах', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ExtWPRPeriod = _input('ExtWPRPeriod', 11)
KeltnerPeriod = _input('KeltnerPeriod', 20)  # период усреднения Кёлтнера
Ratio = _input('Ratio', 1.5)  # девиация канала
Shift = _input('Shift', 0)  # сдвиг канала по горизонтали в барах
ExtOpenBuffer = Arr(0, 0.0)
ExtHighBuffer = Arr(0, 0.0)
ExtLowBuffer = Arr(0, 0.0)
ExtCloseBuffer = Arr(0, 0.0)
ExtColorBuffer = Arr(0, 0.0)
BorderTopBuffer = Arr(0, 0.0)
BorderBotBuffer = Arr(0, 0.0)
min_rates_total = 0
min_rates_1 = 0
WPR_Handle = 0
MA_Handle = 0

def OnInit():
    global MA_Handle, WPR_Handle, min_rates_1, min_rates_total
    min_rates_1 = _int(ExtWPRPeriod)
    min_rates_total = min_rates_1 + _int(KeltnerPeriod)
    WPR_Handle = iWPR(None, 0, ExtWPRPeriod)
    if WPR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iWPR!')
        return INIT_FAILED
    MA_Handle = iMA(None, 0, KeltnerPeriod, 0, MODE_SMA, WPR_Handle)
    if MA_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора iMA')
        return INIT_FAILED
    shortname = Box("")
    StringConcatenate(shortname, 'WPRCandleKeltner(', ExtWPRPeriod, ')')
    IndicatorSetString(INDICATOR_SHORTNAME, shortname.v)
    SetIndexBuffer(0, ExtOpenBuffer, INDICATOR_DATA)
    SetIndexBuffer(1, ExtHighBuffer, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLowBuffer, INDICATOR_DATA)
    SetIndexBuffer(3, ExtCloseBuffer, INDICATOR_DATA)
    SetIndexBuffer(4, ExtColorBuffer, INDICATOR_COLOR_INDEX)
    SetIndexBuffer(5, BorderTopBuffer, INDICATOR_DATA)
    SetIndexBuffer(6, BorderBotBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtOpenBuffer, True)
    ArraySetAsSeries(ExtHighBuffer, True)
    ArraySetAsSeries(ExtLowBuffer, True)
    ArraySetAsSeries(ExtCloseBuffer, True)
    ArraySetAsSeries(ExtColorBuffer, True)
    ArraySetAsSeries(BorderTopBuffer, True)
    ArraySetAsSeries(BorderBotBuffer, True)
    PlotIndexSetInteger(0, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(1, PLOT_SHOW_DATA, False)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(1, PLOT_SHIFT, Shift)
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if (BarsCalculated(WPR_Handle) < rates_total or BarsCalculated(MA_Handle) < rates_total) or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    range_ = 0.0
    HH = 0.0
    LL = 0.0
    MA = Arr(0, 0.0)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    ArraySetAsSeries(open, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    ArraySetAsSeries(MA, True)
    if CopyBuffer(MA_Handle, 0, 0, to_copy, MA) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        ExtCloseBuffer[bar] = 50.0
        ExtLowBuffer[bar] = ExtCloseBuffer[bar]
        ExtHighBuffer[bar] = ExtLowBuffer[bar]
        ExtOpenBuffer[bar] = ExtHighBuffer[bar]
        HH = high[ArrayMaximum(high, bar, ExtWPRPeriod)]
        LL = low[ArrayMinimum(low, bar, ExtWPRPeriod)]
        range_ = HH - LL
        if not CompareDouble(range_, 0.0):
            ExtOpenBuffer[bar] = _fdiv(-100 * (HH - open[bar]), range_)
            ExtCloseBuffer[bar] = _fdiv(-100 * (HH - close[bar]), range_)
            ExtHighBuffer[bar] = _fdiv(-100 * (HH - high[bar]), range_)
            ExtLowBuffer[bar] = _fdiv(-100 * (HH - low[bar]), range_)
        Keltner = Ratio * GetKeltner(KeltnerPeriod, bar, ExtHighBuffer, ExtLowBuffer)
        BorderTopBuffer[bar] = MA[bar] + Keltner
        BorderBotBuffer[bar] = MA[bar] - Keltner
        if ExtOpenBuffer[bar] < ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 2.0
        elif ExtOpenBuffer[bar] > ExtCloseBuffer[bar]:
            ExtColorBuffer[bar] = 0.0
        else:
            ExtColorBuffer[bar] = 1.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

def CompareDouble(Number1, Number2):
    Compare = NormalizeDouble(Number1 - Number2, 8) == 0
    return Compare

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


class WPRCandleKeltner(_MQL5Indicator):
    name = 'WPRCandleKeltner'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    params = {
        'ExtWPRPeriod': 11,
        'KeltnerPeriod': 20,  # период усреднения Кёлтнера
        'Ratio': 1.5,  # девиация канала
        'Shift': 0,  # сдвиг канала по горизонтали в барах
    }

