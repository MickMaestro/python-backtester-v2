"""ama_stl — converted from MQL5: MQL5 Indicators/AMA Slow Trend Line/ama_stl.mq5

Copyright: Copyright © 2006, MetaQuotes Software Corp.; Link: http://www.metaquotes.net; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2006, MetaQuotes Software Corp.', 'link': 'http://www.metaquotes.net', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 1, 'indicator_plots': 1}, 'types': {1: 1}, 'colors': {1: [13458026]}, 'widths': {1: 1}, 'styles': {1: 0}, 'labels': {1: 'AMA_STL'}, 'levels': [], 'description': [], 'name': 'ama_stl', 'source': 'MQL5 Indicators/AMA Slow Trend Line/ama_stl.mq5', 'folder': 'AMA Slow Trend Line', 'inputs': [{'mql': 'FastMA', 'py': 'FastMA', 'param': 'FastMA', 'type': 'uint', 'default': 3, 'label': '', 'sinput': False}, {'mql': 'SlowMA', 'py': 'SlowMA', 'param': 'SlowMA', 'type': 'uint', 'default': 100, 'label': '', 'sinput': False}, {'mql': 'Range', 'py': 'Range', 'param': 'Range', 'type': 'uint', 'default': 160, 'label': '', 'sinput': False}, {'mql': 'filter', 'py': 'filter_', 'param': 'filter_', 'type': 'uint', 'default': 25, 'label': '', 'sinput': False}, {'mql': 'Level', 'py': 'Level', 'param': 'Level', 'type': 'uint', 'default': 100, 'label': '', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
FastMA = _input('FastMA', 3)
SlowMA = _input('SlowMA', 100)
Range = _input('Range', 160)
filter_ = _input('filter_', 25)
Level = _input('Level', 100)
ExtBuffer = Arr(0, 0.0)
k1 = 0.0
k2 = 0.0
dLevel = 0.0
min_rates_total = 0
Count = Arr(0, 0)
mAMA = Arr(0, 0.0)

def Recount_ArrayZeroPos(CoArr, Size):
    global _s_Recount_ArrayZeroPos_count
    numb = 0
    Max1 = 0
    Max2 = 0
    Max2 = Size
    Max1 = Max2 - 1
    _s_Recount_ArrayZeroPos_count -= 1
    if _s_Recount_ArrayZeroPos_count < 0:
        _s_Recount_ArrayZeroPos_count = Max1
    for iii in range(0, Max2):
        numb = iii + _s_Recount_ArrayZeroPos_count
        if numb > Max1:
            numb -= Max2
        CoArr[iii] = numb

def OnInit():
    global dLevel, k1, k2, min_rates_total
    min_rates_total = _int(Range + 1)
    k1 = 2.0 / (SlowMA + 1)
    k2 = (2.0 / (FastMA + 1)) - k1
    dLevel = Level * Point()
    if ArrayResize(Count, Range) < _int(Range):
        Print('Не удалось распределить память под массив Count[]')
        return INIT_FAILED
    if ArrayResize(mAMA, Range) < _int(Range):
        Print('Не удалось распределить память под массив mAMA[]')
        return INIT_FAILED
    ArrayInitialize(Count, 0)
    SetIndexBuffer(0, ExtBuffer, INDICATOR_DATA)
    ArraySetAsSeries(ExtBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, EMPTY_VALUE)
    IndicatorSetString(INDICATOR_SHORTNAME, 'AMA_STL')
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_AMA_
    if rates_total < min_rates_total:
        return 0
    limit = 0
    bar = 0
    Noise = 0.0
    ER = 0.0
    SSC = 0.0
    AMA = 0.0
    sdAMA = 0.0
    dAMA = 0.0
    HH = 0.0
    LL = 0.0
    Res = 0.0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(close, True)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
        _s_OnCalculate_AMA_ = close[limit + 1]
        ArrayInitialize(mAMA, close[limit + 1])
    else:
        limit = rates_total - prev_calculated
    AMA = _s_OnCalculate_AMA_
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        Noise = 0.0
        for i in range(bar + _int(Range) - 1, bar - 1, -1):
            Noise += MathAbs(close[i] - close[i + 1])
        if Noise:
            ER = _fdiv(MathAbs(close[bar] - close[bar + Range]), Noise)
        else:
            ER = 0.0
        SSC = (ER * k2) + k1
        AMA += NormalizeDouble(SSC * SSC * (close[bar] - AMA), Digits())
        mAMA[Count[0]] = AMA
        if filter_ < 1:
            ExtBuffer[bar] = mAMA[Count[0]]
        else:
            sdAMA = 0.0
            for i in range(bar + _int(SlowMA) - 1, bar - 1, -1):
                sdAMA += MathAbs(mAMA[Count[0]] - mAMA[Count[1]])
            dAMA = mAMA[Count[0]] - mAMA[Count[1]]
            Res = NormalizeDouble((filter_ * sdAMA) / (100 * SlowMA), Digits())
            if dAMA >= 0:
                HH = high[ArrayMaximum(high, bar, Range)]
                if dAMA < Res and high[bar] <= (HH + dLevel):
                    ExtBuffer[bar] = ExtBuffer[bar + 1]
                else:
                    ExtBuffer[bar] = mAMA[Count[0]]
            else:
                LL = low[ArrayMinimum(low, bar, Range)]
                if (-dAMA) < Res and low[bar] > (LL - dLevel):
                    ExtBuffer[bar] = ExtBuffer[bar + 1]
                else:
                    ExtBuffer[bar] = mAMA[Count[0]]
        if bar:
            Recount_ArrayZeroPos(Count, Range)
            _s_OnCalculate_AMA_ = AMA
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total

# ---- static local variables
_s_Recount_ArrayZeroPos_count = 1
_s_OnCalculate_AMA_ = 0.0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class AmaStl(_MQL5Indicator):
    name = 'ama_stl'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
        'FastMA': 3,
        'SlowMA': 100,
        'Range': 160,
        'filter_': 25,
        'Level': 100,
    }

