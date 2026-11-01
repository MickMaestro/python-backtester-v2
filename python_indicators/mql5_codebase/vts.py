"""VTS — converted from MQL5: MQL5 Indicators/VTS/VTS.mq5

Copyright: Copyright © 2007, IZZY; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2007, IZZY', 'link': '', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 8, 'indicator_plots': 8}, 'types': {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 5, 8: 5}, 'colors': {1: [16711935], 2: [7451452], 3: [16711935], 4: [7451452], 5: [16711935], 6: [7451452], 7: [255], 8: [16711680]}, 'widths': {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2}, 'styles': {}, 'labels': {1: 'VTS Sell', 2: 'VTS Buy', 3: 'VTS Sell', 4: 'VTS Buy', 5: 'VTS Sell', 6: 'VTS Buy', 7: 'VTS Sell', 8: 'VTS Buy'}, 'levels': [], 'description': [], 'name': 'VTS', 'source': 'MQL5 Indicators/VTS/VTS.mq5', 'folder': 'VTS', 'inputs': [{'mql': 'ATR_Period', 'py': 'ATR_Period', 'param': 'ATR_Period', 'type': 'uint', 'default': 10, 'label': '', 'sinput': False}, {'mql': 'kATR', 'py': 'kATR', 'param': 'kATR', 'type': 'double', 'default': 2.0, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
ATR_Period = _input('ATR_Period', 10)
kATR = _input('kATR', 2.0)
UpIndBuffer1 = Arr(0, 0.0)
DnIndBuffer1 = Arr(0, 0.0)
UpIndBuffer2 = Arr(0, 0.0)
DnIndBuffer2 = Arr(0, 0.0)
UpIndBuffer3 = Arr(0, 0.0)
DnIndBuffer3 = Arr(0, 0.0)
UpIndBuffer4 = Arr(0, 0.0)
DnIndBuffer4 = Arr(0, 0.0)
ATR_Handle = 0
min_rates_total = 0

def OnInit():
    global ATR_Handle, min_rates_total
    min_rates_total = _int(ATR_Period) + 30
    ATR_Handle = iATR(None, 0, ATR_Period)
    if ATR_Handle == INVALID_HANDLE:
        Print(' Не удалось получить хендл индикатора ATR')
        return INIT_FAILED
    SetIndexBuffer(0, DnIndBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(DnIndBuffer1, True)
    SetIndexBuffer(1, UpIndBuffer1, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(UpIndBuffer1, True)
    SetIndexBuffer(2, DnIndBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(2, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(DnIndBuffer2, True)
    SetIndexBuffer(3, UpIndBuffer2, INDICATOR_DATA)
    PlotIndexSetInteger(3, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(UpIndBuffer2, True)
    SetIndexBuffer(4, DnIndBuffer3, INDICATOR_DATA)
    PlotIndexSetInteger(4, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(DnIndBuffer3, True)
    SetIndexBuffer(5, UpIndBuffer3, INDICATOR_DATA)
    PlotIndexSetInteger(5, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(UpIndBuffer3, True)
    SetIndexBuffer(6, DnIndBuffer4, INDICATOR_DATA)
    PlotIndexSetInteger(6, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(DnIndBuffer4, True)
    SetIndexBuffer(7, UpIndBuffer4, INDICATOR_DATA)
    PlotIndexSetInteger(7, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(UpIndBuffer4, True)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    short_name = 'VTS'
    IndicatorSetString(INDICATOR_SHORTNAME, short_name)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_VTS10_prev, _s_OnCalculate_VTS11_prev, _s_OnCalculate_VTS12_prev, _s_OnCalculate_VTS13_prev, _s_OnCalculate_VTS14_prev, _s_OnCalculate_VTS15_prev, _s_OnCalculate_VTS16_prev, _s_OnCalculate_VTS17_prev, _s_OnCalculate_VTS18_prev, _s_OnCalculate_VTS19_prev, _s_OnCalculate_VTS1_prev, _s_OnCalculate_VTS20_prev, _s_OnCalculate_VTS21_prev, _s_OnCalculate_VTS22_prev, _s_OnCalculate_VTS23_prev, _s_OnCalculate_VTS2_prev, _s_OnCalculate_VTS3_prev, _s_OnCalculate_VTS4_prev, _s_OnCalculate_VTS5_prev, _s_OnCalculate_VTS6_prev, _s_OnCalculate_VTS7_prev, _s_OnCalculate_VTS8_prev, _s_OnCalculate_VTS9_prev, _s_OnCalculate_VTS_prev
    if BarsCalculated(ATR_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    bar = 0
    ATR = Arr(0, 0.0)
    VTS = 0.0
    VTS1 = 0.0
    VTS2 = 0.0
    VTS3 = 0.0
    VTS4 = 0.0
    VTS5 = 0.0
    VTS6 = 0.0
    VTS7 = 0.0
    VTS8 = 0.0
    VTS9 = 0.0
    VTS10 = 0.0
    VTS11 = 0.0
    VTS12 = 0.0
    VTS13 = 0.0
    VTS14 = 0.0
    VTS15 = 0.0
    VTS16 = 0.0
    VTS17 = 0.0
    VTS18 = 0.0
    VTS19 = 0.0
    VTS20 = 0.0
    VTS21 = 0.0
    VTS22 = 0.0
    VTS23 = 0.0
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total
        res = close[limit + 1]
        _s_OnCalculate_VTS_prev = res
        _s_OnCalculate_VTS1_prev = res
        _s_OnCalculate_VTS2_prev = res
        _s_OnCalculate_VTS3_prev = res
        _s_OnCalculate_VTS4_prev = res
        _s_OnCalculate_VTS5_prev = res
        _s_OnCalculate_VTS6_prev = res
        _s_OnCalculate_VTS7_prev = res
        _s_OnCalculate_VTS8_prev = res
        _s_OnCalculate_VTS9_prev = res
        _s_OnCalculate_VTS10_prev = res
        _s_OnCalculate_VTS11_prev = res
        _s_OnCalculate_VTS12_prev = res
        _s_OnCalculate_VTS13_prev = res
        _s_OnCalculate_VTS14_prev = res
        _s_OnCalculate_VTS15_prev = res
        _s_OnCalculate_VTS16_prev = res
        _s_OnCalculate_VTS17_prev = res
        _s_OnCalculate_VTS18_prev = res
        _s_OnCalculate_VTS19_prev = res
        _s_OnCalculate_VTS20_prev = res
        _s_OnCalculate_VTS21_prev = res
        _s_OnCalculate_VTS22_prev = res
        _s_OnCalculate_VTS23_prev = res
    else:
        limit = rates_total - prev_calculated
    to_copy = limit + 1
    if CopyBuffer(ATR_Handle, 0, 0, to_copy, ATR) <= 0:
        return 0
    ArraySetAsSeries(ATR, True)
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        VTS = close[bar] - (kATR * ATR[bar])
        VTS1 = close[bar] + (kATR * ATR[bar])
        VTS2 = MathMax(VTS, _s_OnCalculate_VTS_prev)
        VTS3 = MathMin(VTS1, _s_OnCalculate_VTS1_prev)
        VTS4 = MathMax(VTS2, _s_OnCalculate_VTS2_prev)
        VTS5 = MathMin(VTS3, _s_OnCalculate_VTS3_prev)
        VTS6 = MathMax(VTS4, _s_OnCalculate_VTS4_prev)
        VTS7 = MathMin(VTS5, _s_OnCalculate_VTS5_prev)
        VTS8 = MathMax(VTS6, _s_OnCalculate_VTS6_prev)
        VTS9 = MathMin(VTS7, _s_OnCalculate_VTS7_prev)
        VTS10 = MathMax(VTS8, _s_OnCalculate_VTS8_prev)
        VTS11 = MathMin(VTS9, _s_OnCalculate_VTS9_prev)
        VTS12 = MathMax(VTS10, _s_OnCalculate_VTS10_prev)
        VTS13 = MathMin(VTS11, _s_OnCalculate_VTS11_prev)
        VTS14 = MathMax(VTS12, _s_OnCalculate_VTS12_prev)
        VTS15 = MathMin(VTS13, _s_OnCalculate_VTS13_prev)
        VTS16 = MathMax(VTS14, _s_OnCalculate_VTS14_prev)
        VTS17 = MathMin(VTS15, _s_OnCalculate_VTS15_prev)
        VTS18 = MathMax(VTS16, _s_OnCalculate_VTS16_prev)
        VTS19 = MathMin(VTS17, _s_OnCalculate_VTS17_prev)
        VTS20 = MathMax(VTS18, _s_OnCalculate_VTS18_prev)
        VTS21 = MathMin(VTS19, _s_OnCalculate_VTS19_prev)
        VTS22 = MathMax(VTS20, _s_OnCalculate_VTS20_prev)
        VTS23 = MathMin(VTS21, _s_OnCalculate_VTS21_prev)
        UpIndBuffer1[bar] = MathMax(VTS22, _s_OnCalculate_VTS22_prev)
        DnIndBuffer1[bar] = MathMin(VTS23, _s_OnCalculate_VTS23_prev)
        UpIndBuffer2[bar] = MathMax(UpIndBuffer1[bar], UpIndBuffer1[bar + 1])
        DnIndBuffer2[bar] = MathMin(DnIndBuffer1[bar], DnIndBuffer1[bar + 1])
        UpIndBuffer3[bar] = MathMax(UpIndBuffer2[bar], UpIndBuffer2[bar + 1])
        DnIndBuffer3[bar] = MathMin(DnIndBuffer2[bar], DnIndBuffer2[bar + 1])
        UpIndBuffer4[bar] = UpIndBuffer4[bar + 1]
        DnIndBuffer4[bar] = DnIndBuffer4[bar + 1]
        if close[bar] > DnIndBuffer3[bar]:
            UpIndBuffer4[bar] = UpIndBuffer3[bar]
            DnIndBuffer4[bar] = 0.0
        if close[bar] < UpIndBuffer3[bar]:
            DnIndBuffer4[bar] = DnIndBuffer3[bar]
            UpIndBuffer4[bar] = 0.0
        if bar:
            _s_OnCalculate_VTS_prev = VTS
            _s_OnCalculate_VTS1_prev = VTS1
            _s_OnCalculate_VTS2_prev = VTS2
            _s_OnCalculate_VTS3_prev = VTS3
            _s_OnCalculate_VTS4_prev = VTS4
            _s_OnCalculate_VTS5_prev = VTS5
            _s_OnCalculate_VTS6_prev = VTS6
            _s_OnCalculate_VTS7_prev = VTS7
            _s_OnCalculate_VTS8_prev = VTS8
            _s_OnCalculate_VTS9_prev = VTS9
            _s_OnCalculate_VTS10_prev = VTS10
            _s_OnCalculate_VTS11_prev = VTS11
            _s_OnCalculate_VTS12_prev = VTS12
            _s_OnCalculate_VTS13_prev = VTS13
            _s_OnCalculate_VTS14_prev = VTS14
            _s_OnCalculate_VTS15_prev = VTS15
            _s_OnCalculate_VTS16_prev = VTS16
            _s_OnCalculate_VTS17_prev = VTS17
            _s_OnCalculate_VTS18_prev = VTS18
            _s_OnCalculate_VTS19_prev = VTS19
            _s_OnCalculate_VTS20_prev = VTS20
            _s_OnCalculate_VTS21_prev = VTS21
            _s_OnCalculate_VTS22_prev = VTS22
            _s_OnCalculate_VTS23_prev = VTS23
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_OnCalculate_VTS_prev = 0.0
_s_OnCalculate_VTS1_prev = 0.0
_s_OnCalculate_VTS2_prev = 0.0
_s_OnCalculate_VTS3_prev = 0.0
_s_OnCalculate_VTS4_prev = 0.0
_s_OnCalculate_VTS5_prev = 0.0
_s_OnCalculate_VTS6_prev = 0.0
_s_OnCalculate_VTS7_prev = 0.0
_s_OnCalculate_VTS8_prev = 0.0
_s_OnCalculate_VTS9_prev = 0.0
_s_OnCalculate_VTS10_prev = 0.0
_s_OnCalculate_VTS11_prev = 0.0
_s_OnCalculate_VTS12_prev = 0.0
_s_OnCalculate_VTS13_prev = 0.0
_s_OnCalculate_VTS14_prev = 0.0
_s_OnCalculate_VTS15_prev = 0.0
_s_OnCalculate_VTS16_prev = 0.0
_s_OnCalculate_VTS17_prev = 0.0
_s_OnCalculate_VTS18_prev = 0.0
_s_OnCalculate_VTS19_prev = 0.0
_s_OnCalculate_VTS20_prev = 0.0
_s_OnCalculate_VTS21_prev = 0.0
_s_OnCalculate_VTS22_prev = 0.0
_s_OnCalculate_VTS23_prev = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VTS(_MQL5Indicator):
    name = 'VTS'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'ATR_Period': 10,
        'kATR': 2.0,
    }

