"""tsd_pp_macd_force_ind_v1 — converted from MQL5: MQL5 Indicators/TSD_PP_MACD_FORCE_Ind_v1/tsd_pp_macd_force_ind_v1.mq5

Copyright: Copyright © 2005, Bob O'Brien; Version: 1.00

Translated automatically by backtester.mql5 (translator 1.0) on 2026-10-31. The code below follows the MQL5 source statement by statement;
see backtester/mql5/README for the conventions (Arr, Box, _idiv, ...).
"""
# flake8: noqa
from backtester.mql5.runtime import *  # MQL5 standard library

MQL5_META = {'props': {'copyright': "Copyright © 2005, Bob O'Brien", 'link': '', 'version': '1.00', 'window': 'separate', 'indicator_buffers': 2, 'indicator_plots': 1, 'indicator_minimum': -0.3, 'indicator_maximum': 1.8}, 'types': {1: 10}, 'colors': {1: [255, 8421504, 65280]}, 'widths': {1: 5}, 'styles': {}, 'labels': {1: 'INDICATOR_NAME'}, 'levels': [], 'description': [], 'name': 'tsd_pp_macd_force_ind_v1', 'source': 'MQL5 Indicators/TSD_PP_MACD_FORCE_Ind_v1/tsd_pp_macd_force_ind_v1.mq5', 'folder': 'TSD_PP_MACD_FORCE_Ind_v1', 'inputs': [{'mql': 'Force', 'py': 'Force', 'param': 'Force', 'type': 'uint', 'default': 2, 'label': '', 'sinput': False}, {'mql': 'Applied_Volume', 'py': 'Applied_Volume', 'param': 'Applied_Volume', 'type': 'int', 'default': 0, 'label': 'Volume type for calculation', 'sinput': False}, {'mql': 'FastMA', 'py': 'FastMA', 'param': 'FastMA', 'type': 'uint', 'default': 12, 'label': '', 'sinput': False}, {'mql': 'SlowMA', 'py': 'SlowMA', 'param': 'SlowMA', 'type': 'uint', 'default': 26, 'label': '', 'sinput': False}, {'mql': 'Signal', 'py': 'Signal', 'param': 'Signal', 'type': 'uint', 'default': 9, 'label': '', 'sinput': False}, {'mql': 'Shift', 'py': 'Shift', 'param': 'Shift', 'type': 'int', 'default': 0, 'label': 'Horizontal shift of the indicator in bars', 'sinput': False}], 'short_form': False, 'has_oncalculate': True, 'missing_includes': [], 'imports': [], 'libraries': []}

# ---- inputs and global variables
Force = _input('Force', 2)
Applied_Volume = _input('Applied_Volume', VOLUME_TICK)  # Volume type for calculation
FastMA = _input('FastMA', 12)
SlowMA = _input('SlowMA', 26)
Signal = _input('Signal', 9)
Shift = _input('Shift', 0)  # Horizontal shift of the indicator in bars
IndBuffer = Arr(0, 0.0)
ColorIndBuffer = Arr(0, 0.0)
min_rates_total = 0
MACD_Handle = 0
Fr_Handle = 0

def OnInit():
    global Fr_Handle, MACD_Handle, min_rates_total
    if Period() >= PERIOD_D1:
        Print('Chart period for indicator ' + 'TSD_PP_MACD_FORCE_Ind_v1' + ' cannot be greater than PERIOD_D1!')
        return INIT_FAILED
    min_rates_1 = _int(MathMax(FastMA, SlowMA) + Signal)
    min_rates_2 = _int(_idiv(Force * PeriodSeconds(PERIOD_D1), PeriodSeconds(PERIOD_CURRENT)))
    min_rates_3 = _idiv(PeriodSeconds(PERIOD_W1), PeriodSeconds(PERIOD_CURRENT))
    min_rates_total = MathMax(min_rates_1, min_rates_2) + min_rates_3
    MACD_Handle = iMACD(None, 0, FastMA, SlowMA, Signal, PRICE_CLOSE)
    if MACD_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of iMACD')
        return INIT_FAILED
    Fr_Handle = iForce(None, PERIOD_D1, Force, MODE_EMA, Applied_Volume)
    if Fr_Handle == INVALID_HANDLE:
        Print(' Failed to get the handle of iForce')
        return INIT_FAILED
    SetIndexBuffer(0, IndBuffer, INDICATOR_DATA)
    ArraySetAsSeries(IndBuffer, True)
    SetIndexBuffer(1, ColorIndBuffer, INDICATOR_COLOR_INDEX)
    ArraySetAsSeries(ColorIndBuffer, True)
    PlotIndexSetInteger(0, PLOT_DRAW_BEGIN, min_rates_total)
    IndicatorSetString(INDICATOR_SHORTNAME, 'TSD_PP_MACD_FORCE_Ind_v1')
    IndicatorSetInteger(INDICATOR_DIGITS, 0)
    return INIT_SUCCEEDED

def OnCalculate(rates_total, prev_calculated, time, open, high, low, close, tick_volume, volume, spread):
    if rates_total < min_rates_total or BarsCalculated(MACD_Handle) < rates_total:
        return 0
    Force_ = Arr(1, 0.0, dyn=False)
    MACD = Arr(2, 0.0, dyn=False)
    limit = 0
    bar = 0
    nWeek = 0
    nDay = 0
    dSun = 0
    iTimeW = Arr(1, 0, dyn=False)
    iTime_ = Arr(1, 0, dyn=False)
    if prev_calculated > rates_total or prev_calculated <= 0:
        limit = rates_total - min_rates_total - 1
    else:
        limit = rates_total - prev_calculated
    ArraySetAsSeries(time, True)
    if CopyTime(Symbol(), PERIOD_W1, 0, 1, iTimeW) <= 0:
        return 0
    bar = limit
    for bar in range(bar, 0 - 1, -1):
        tm = MqlDateTime()
        TimeToStruct(time[bar], tm)
        dSun = StringToTime(TimeToString(time[bar] - (tm.day_of_week * 86400), TIME_DATE))
        nWeek = _int(_idiv(_idiv(iTimeW[0] - dSun, 86400), 7))
        if CopyBuffer(MACD_Handle, MAIN_LINE, nWeek + 1, 2, MACD) <= 0:
            return 0
        if Period() == PERIOD_D1:
            nDay = bar
        else:
            nWeek5 = nWeek * 5
            dSun = StringToTime(TimeToString(time[bar], TIME_DATE))
            if CopyTime(Symbol(), PERIOD_D1, nWeek5, 1, iTime_) <= 0:
                return 0
            i = _int(_idiv(MathAbs(iTime_[0] - dSun), 86400))
            nDay = MathMax(nWeek5 - i, 0)
        if CopyBuffer(Fr_Handle, MAIN_LINE, nDay + 1, 1, Force_) <= 0:
            return 0
        IndBuffer[bar] = 1.0
        ColorIndBuffer[bar] = 1.0
        if MACD[1] > MACD[0] and Force_[0] > 0:
            ColorIndBuffer[bar] = 2.0
        if MACD[1] < MACD[0] and Force_[0] < 0:
            ColorIndBuffer[bar] = 0.0
    else:
        bar = _range_end(bar, 0 - 1, -1)
    return rates_total


# ---------------------------------------------------------------------- plugin
from backtester.indicators.base import Choice as _Choice, Pane as _Pane
from backtester.mql5.indicator import MQL5Indicator as _MQL5Indicator


class TsdPpMacdForceIndV1(_MQL5Indicator):
    name = 'tsd_pp_macd_force_ind_v1'
    pane = _Pane.SEPARATE
    program_file = __file__
    meta = MQL5_META
    repaint_window = 300
    params = {
        'Force': 2,
        'Applied_Volume': _Choice({0: 'Tick', 1: 'Real'}, default=0),  # Volume type for calculation
        'FastMA': 12,
        'SlowMA': 26,
        'Signal': 9,
        'Shift': 0,  # Horizontal shift of the indicator in bars
    }
    y_range = (-0.3, 1.8)

