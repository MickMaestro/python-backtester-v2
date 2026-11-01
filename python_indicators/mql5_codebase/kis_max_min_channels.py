"""kis_max_min_channels — converted from MQL5: MQL5 Indicators/KiS_max_min_Channels/kis_max_min_channels.mq5

KiS_max_min_Channels
Copyright: Copyright © 2007, KCBT; Link: http://www.kcbt.ru/forum/index.php?/; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, KCBT', 'link': 'http://www.kcbt.ru/forum/index.php?/', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 3, 'indicator_plots': 3}, 'types': {1: 1, 2: 1, 3: 1}, 'colors': {1: [8388736], 2: [16711680], 3: [36095]}, 'widths': {1: 1, 2: 1, 3: 1}, 'styles': {1: 0, 2: 0, 3: 0}, 'labels': {1: 'KiS_max_min_Channels Middle', 2: 'KiS_max_min_Channels Upper', 3: 'KiS_max_min_Channels Lower'}, 'levels': [], 'description': ['KiS_max_min_Channels'], 'name': 'kis_max_min_channels', 'source': 'MQL5 Indicators/KiS_max_min_Channels/kis_max_min_channels.mq5', 'folder': 'KiS_max_min_Channels', 'inputs': [{'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Shift = _input('Shift', 0)  # horizontal shift of the indicator in bars
ExtLineBuffer0 = Arr(0, 0.0)
ExtLineBuffer1 = Arr(0, 0.0)
ExtLineBuffer2 = Arr(0, 0.0)
min_rates_total = 0

def OnInit():
    global min_rates_total
    min_rates_total = 100
    SetIndexBuffer(0, ExtLineBuffer0, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_SHIFT, Shift)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    ArraySetAsSeries(ExtLineBuffer0, True)
    SetIndexBuffer(1, ExtLineBuffer1, INDICATOR_DATA)
    SetIndexBuffer(2, ExtLineBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    PlotIndexSetDouble(2, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    ArraySetAsSeries(ExtLineBuffer1, True)
    ArraySetAsSeries(ExtLineBuffer2, True)
    IndicatorSetString(INDICATOR_SHORTNAME, 'KiS_max_min_Channels')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())

def OnDeinit(reason):
    Comment('')

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_LastCountBar
    if rates_total < min_rates_total:
        return 0
    D1High = Arr(1, 0.0, dyn=False)
    D1Low = Arr(1, 0.0, dyn=False)
    D1Close = Arr(1, 0.0, dyn=False)
    D1Open = Arr(1, 0.0, dyn=False)
    D1Time = Arr(1, 0, dyn=False)
    limit = 0
    bar = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_LastCountBar = rates_total
    else:
        limit = _int(_s_OnCalculate_LastCountBar) + rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        if CopyTime(Symbol(), PERIOD_D1, _DT(time[bar]), 1, D1Time) <= 0:
            return 0
        if CopyHigh(Symbol(), PERIOD_D1, _DT(time[bar]), 1, D1High) <= 0:
            return 0
        if CopyLow(Symbol(), PERIOD_D1, _DT(time[bar]), 1, D1Low) <= 0:
            return 0
        ExtLineBuffer1[bar] = D1High[0]
        ExtLineBuffer0[bar] = (D1High[0] + D1Low[0]) / 2
        ExtLineBuffer2[bar] = D1Low[0]
        if time[bar] >= D1Time[0] and time[bar + 1] < D1Time[0]:
            _s_OnCalculate_LastCountBar = bar
    else:
        bar = _range_end(bar, 0 - 1, -1)
    if CopyOpen(Symbol(), PERIOD_D1, _DT(time[0]), 1, D1Open) <= 0:
        return 0
    Comment('Daily high:', D1High[0], ' Daily low:', D1Low[0], '\n', 'Channel middle:', ExtLineBuffer0[0], ' Ширина канала:', _fdiv(D1High[0] + D1Low[0], Point()), '\n', 'From the channel middle to Open:', MathRound(_fdiv(MathAbs(ExtLineBuffer0[0] - D1Open[0]), Point())), '\n', 'From the channel middle to Close:', MathRound(_fdiv(MathAbs(ExtLineBuffer0[0] - close[0]), Point())))
    return rates_total

# ---- static local variables
_s_OnCalculate_LastCountBar = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class KisMaxMinChannels(_MQL5Indicator):
    name = 'kis_max_min_channels'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Shift': 0,  # horizontal shift of the indicator in bars
    }

