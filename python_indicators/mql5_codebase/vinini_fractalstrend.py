"""vinini_fractalstrend — converted from MQL5: MQL5 Indicators/ZigZag based on VininI_FractalsTrend/vinini_fractalstrend.mq5

VininI_FractalsTrend
Copyright: Copyright © 2011, Victor Niclolaev aka Vinin; Link: vinin@mail.ru; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': 'Copyright © 2011, Victor Niclolaev aka Vinin', 'link': 'vinin@mail.ru', 'version': '1.00', 'window': 'chart', 'indicator_buffers': 2, 'indicator_plots': 1}, 'types': {1: 6, 2: 6}, 'colors': {1: [16711935], 2: [16711935]}, 'widths': {1: 1, 2: 1}, 'styles': {}, 'labels': {1: 'INDICATOR_NAME', 2: 'INDICATOR_NAME'}, 'levels': [], 'description': ['VininI_FractalsTrend'], 'name': 'vinini_fractalstrend', 'source': 'MQL5 Indicators/ZigZag based on VininI_FractalsTrend/vinini_fractalstrend.mq5', 'folder': 'ZigZag based on VininI_FractalsTrend', 'inputs': [], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
HighBuffer = Arr(0, 0.0)
LowBuffer = Arr(0, 0.0)
min_rates_total = 0
FRA_Handle = 0

def OnInit():
    global FRA_Handle, min_rates_total
    min_rates_total = 6
    FRA_Handle = iFractals(None, 0)
    if FRA_Handle == INVALID_HANDLE:
        Print(' Failed to get handle of the iFractals indicator')
        return 1
    SetIndexBuffer(0, HighBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(HighBuffer, True)
    PlotIndexSetDouble(0, PLOT_EMPTY_VALUE, 0)
    SetIndexBuffer(1, LowBuffer, INDICATOR_DATA)
    PlotIndexSetInteger(1, PLOT_DRAW_BEGIN, min_rates_total)
    ArraySetAsSeries(LowBuffer, True)
    PlotIndexSetDouble(1, PLOT_EMPTY_VALUE, 0)
    IndicatorSetInteger(INDICATOR_DIGITS, Digits())
    IndicatorSetString(INDICATOR_SHORTNAME, 'VininI_FractalsTrend')
    return 0

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    global _s_OnCalculate_PrevHighPos, _s_OnCalculate_PrevLowPos, _s_OnCalculate_dir
    if BarsCalculated(FRA_Handle) < rates_total or rates_total < min_rates_total:
        return 0
    to_copy = 0
    limit = 0
    Fractals = 0
    UpFractal = Arr(0, 0.0)
    DnFractal = Arr(0, 0.0)
    bFractalsUpper = False
    bFractalsLower = False
    dir_ = 0
    PrevLowPos_ = 0
    PrevHighPos_ = 0
    if prev_calculated > rates_total or prev_calculated <= 0:
        to_copy = rates_total
        limit = rates_total - min_rates_total - 1
        PrevLowPos_ = rates_total
        PrevHighPos_ = rates_total
        dir_ = 0
    else:
        to_copy = rates_total - prev_calculated + 5
        limit = rates_total - prev_calculated + 4
    if CopyBuffer(FRA_Handle, 0, 0, to_copy, UpFractal) <= 0:
        return 0
    if CopyBuffer(FRA_Handle, 1, 0, to_copy, DnFractal) <= 0:
        return 0
    ArraySetAsSeries(high, True)
    ArraySetAsSeries(low, True)
    ArraySetAsSeries(UpFractal, True)
    ArraySetAsSeries(DnFractal, True)
    _s_OnCalculate_dir = dir_
    _s_OnCalculate_PrevLowPos = PrevLowPos_
    _s_OnCalculate_PrevHighPos = PrevHighPos_
    for bar in range(limit, 0 - 1, -1):
        if bar == 4:
            dir_ = _s_OnCalculate_dir
            PrevLowPos_ = _s_OnCalculate_PrevLowPos
            PrevHighPos_ = _s_OnCalculate_PrevHighPos
        if UpFractal[bar] != EMPTY_VALUE and UpFractal[bar]:
            bFractalsUpper = True
        else:
            bFractalsUpper = False
        if DnFractal[bar] != EMPTY_VALUE and DnFractal[bar]:
            bFractalsLower = True
        else:
            bFractalsLower = False
        Fractals = (bFractalsUpper * 2) + bFractalsLower
        HighBuffer[bar] = 0.0
        LowBuffer[bar] = 0.0
        _sw1 = Fractals
        if _sw1 == 3:
            if not _s_OnCalculate_dir:
                HighBuffer[bar] = high[bar]
                LowBuffer[bar] = low[bar]
                _s_OnCalculate_PrevHighPos = bar
                _s_OnCalculate_PrevLowPos = bar
            if _s_OnCalculate_dir == 1:
                LowBuffer[bar] = low[bar]
                _s_OnCalculate_PrevLowPos = bar
                if high[bar] > high[_s_OnCalculate_PrevHighPos]:
                    HighBuffer[bar] = high[bar]
                    HighBuffer[_s_OnCalculate_PrevHighPos] = 0.0
                    _s_OnCalculate_PrevHighPos = bar
            if _s_OnCalculate_dir == -1:
                HighBuffer[bar] = high[bar]
                _s_OnCalculate_PrevHighPos = bar
                if low[bar] < low[_s_OnCalculate_PrevLowPos]:
                    LowBuffer[bar] = low[bar]
                    LowBuffer[_s_OnCalculate_PrevLowPos] = 0.0
                    _s_OnCalculate_PrevLowPos = bar
            _s_OnCalculate_dir *= -1
        elif _sw1 == 2:
            if _s_OnCalculate_dir == 1:
                if high[bar] > high[_s_OnCalculate_PrevHighPos]:
                    HighBuffer[_s_OnCalculate_PrevHighPos] = 0.0
                    HighBuffer[bar] = high[bar]
                    _s_OnCalculate_PrevHighPos = bar
            else:
                HighBuffer[bar] = high[bar]
                _s_OnCalculate_PrevHighPos = bar
                _s_OnCalculate_dir = 1
        elif _sw1 == 1:
            if _s_OnCalculate_dir == -1:
                if low[bar] < low[_s_OnCalculate_PrevLowPos]:
                    LowBuffer[_s_OnCalculate_PrevLowPos] = 0.0
                    LowBuffer[bar] = low[bar]
                    _s_OnCalculate_PrevLowPos = bar
            else:
                LowBuffer[bar] = low[bar]
                _s_OnCalculate_PrevLowPos = bar
                _s_OnCalculate_dir = -1
    return rates_total

# ---- static local variables
_s_OnCalculate_dir = 0
_s_OnCalculate_PrevLowPos = 0
_s_OnCalculate_PrevHighPos = 0


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class VininiFractalstrend(_MQL5Indicator):
    name = 'vinini_fractalstrend'
    pane = _Pane.PRICE
    program_file = __file__
    meta = MQL5_META
    params = {
    }

